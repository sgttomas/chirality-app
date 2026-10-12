//! RS format 0.1 log writer and reader (DEL-04-03 RECORD_SEMANTICS.md §13.1 S-A,
//! §13.2 entry header, §14.1 W-0/W-1, §14.2 R-2).
//!
//! One append-only JSON Lines log per writer; one entry per line; `seq` taken only
//! by a successful write; a written entry is never rewritten (OF-5).
//!
//! W-0 (§14.1, FC-2): a writer that opens its log on an unterminated last line
//! terminates it (the torn bytes stay in place, never truncated or edited) and
//! appends "partial entry not recovered" naming that line; readers never read
//! a line so named. A torn tail in another writer's log is a partial, never an
//! entry (§14.2 R-2), so it does not make the record set incomplete for a
//! writer; its own writer recovers it on its next open.
//!
//! AAC pending recovery supplies its originally reserved ID for a bounded W-2 late write.

/// Historical WR supply correspondence; not a live observation or append capability.
#[path = "record_supply.rs"]
pub mod supply;

use crate::util::now_rfc3339;
use serde_json::{json, Value};
use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;

pub struct Recorder<'a> {
    pub role: &'a str,
    pub identity: &'a str,
}

pub const APP_WRITER: Recorder<'static> = Recorder {
    role: "App writer",
    identity: "app-writer:local",
};
pub const APP_INTERFACE: Recorder<'static> = Recorder {
    role: "App interface (capturing surface)",
    identity: "app-interface:local",
};

/// What the writer requires of the project's other logs before an append. The
/// owning log must always be complete (W-0/W-1; RS §13.7: an unreadable or
/// unwritable owning target refuses new recording).
#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum RecordSet {
    /// Every discovered log is complete, so an identity collision anywhere is
    /// detected (CC-ID). The default for recording outside an explicit end.
    Complete,
    /// Other logs may be incomplete: the new identity is checked against every
    /// readable entry (only the owning log's if discovery itself fails); an
    /// unread line cannot be checked. Used only for the
    /// person's explicit end (EXEC A-11), including the live run's ordered
    /// pending observations and late-write limits. Their reserved identities
    /// are writer-minted (CC-ID); unread act records are named by a limit.
    ReadableBesideIncomplete,
}

/// Reconciliation before an unresolved append. In end mode the owning log is
/// checked separately: discovery can fail before returning even its readable
/// entries, and a matching prefix must not hide an incomplete owning target.
///
/// Returns the readable entries holding `id` across the project, and those in
/// the owning log: the record set is read through the bounded index
/// (`records_index`), so the cost does not grow with the project's history.
pub(crate) fn append_record_set(root: &Path, log: &Path, set: RecordSet, id: &str) -> Result<(Vec<Value>, Vec<Value>), String> {
    let (mut entries, limits) = crate::records_index::with_index(root, |ix| (ix.entries_with(id), ix.limits()));
    if set == RecordSet::Complete && !limits.is_empty() {
        return Err(format!("RS record set incomplete; nothing written: {limits:?}"));
    }
    crate::storage::check_path(log)?;
    // W-0 at the writer's open: its own torn tail is terminated and named first.
    if read_log_parts(log).partial_tail.is_some() {
        w0_open(root, log)?;
    }
    let own_read = read_log_parts(log);
    let (own, own_limits) = (own_read.entries, own_read.limits);
    if !own_limits.is_empty() {
        return Err(format!("RS owning log incomplete; nothing written: {own_limits:?}"));
    }
    let own: Vec<Value> = own.into_iter().filter(|e| e["recordId"].as_str() == Some(id)).collect();
    if set == RecordSet::ReadableBesideIncomplete {
        for entry in &own {
            if !entries.contains(entry) {
                entries.push(entry.clone());
            }
        }
    }
    Ok((entries, own))
}

/// The label of W-0's limit for a torn line it terminated (RS §14.1, R11).
pub(crate) const PARTIAL_NOT_RECOVERED: &str = "partial entry not recovered";
/// RS §14.1 W-0, FC-2: the (0-based) lines a writer terminated on reopen. Each
/// is followed directly by that writer's "partial entry not recovered" limit
/// naming it as `line ‹n›`. Such a line is kept, never read as an entry.
pub(crate) fn recovered_partial_lines(lines: &[&str]) -> std::collections::BTreeSet<usize> {
    recovered_partial_lines_from(lines, 0)
}
/// As [`recovered_partial_lines`], for lines that start at the log's
/// `first`-th line (0-based); the indices returned are into `lines`.
pub(crate) fn recovered_partial_lines_from(lines: &[&str], first: usize) -> std::collections::BTreeSet<usize> {
    let mut out = std::collections::BTreeSet::new();
    for i in 0..lines.len().saturating_sub(1) {
        if let Ok(next) = serde_json::from_str::<Value>(lines[i + 1]) {
            if next["kind"] == "evidence_limit" && next["body"]["label"] == PARTIAL_NOT_RECOVERED
                && next["body"]["subjectRef"] == format!("line {}", first + i + 1) {
                out.insert(i);
            }
        }
    }
    out
}
/// One log as read (R-2): its entries, the limits that leave it incomplete,
/// and the torn final line (a partial, never an entry), apart.
pub(crate) struct LogRead {
    pub entries: Vec<Value>,
    pub limits: Vec<String>,
    pub partial_tail: Option<String>,
}
/// R-2: entries in written order; an unreadable line is kept as a limit, never used.
pub fn read_log(path: &Path) -> (Vec<Value>, Vec<String>) {
    let read = read_log_parts(path);
    let mut limits = read.limits;
    limits.extend(read.partial_tail);
    (read.entries, limits)
}
pub(crate) fn read_log_parts(path: &Path) -> LogRead {
    let mut entries = Vec::new();
    let mut limits = Vec::new();
    let mut partial_tail = None;
    let text = match std::fs::read_to_string(path) {
        Ok(t) => t,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return LogRead { entries, limits, partial_tail },
        Err(e) => {
            return LogRead { entries, limits: vec![format!("incomplete record: {}: {e}", path.display())], partial_tail }
        }
    };
    let name = path
        .file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default();
    let lines: Vec<&str> = text.lines().collect();
    let n_lines = lines.len();
    let recovered = recovered_partial_lines(&lines);
    let mut expected_seq = 1u64;
    for (n, line) in lines.iter().enumerate() {
        if line.trim().is_empty() || recovered.contains(&n) {
            continue;
        }
        match serde_json::from_str::<Value>(line) {
            Ok(_) if n + 1 == n_lines && !text.ends_with('\n') => {
                partial_tail = Some(format!("{name}: partial entry at end (not read)"));
            }
            Ok(v) => {
                match crate::schema_validation::bundled()
                    .and_then(|validator| validator.validate(&v))
                {
                    Ok(()) => {
                        let seq = v["seq"].as_u64().unwrap();
                        if seq != expected_seq {
                            limits.push(format!("{name}: sequence incomplete/disagrees: expected {expected_seq}, found {seq} at line {}",n+1));
                        }
                        expected_seq = seq.checked_add(1).unwrap_or(seq);
                        entries.push(v);
                    }
                    Err(e) => limits.push(format!("{name}: invalid line {}: {e}", n + 1)),
                }
            }
            Err(_) if n + 1 == n_lines && !text.ends_with('\n') => {
                partial_tail = Some(format!("{name}: partial entry at end (not read)"));
            }
            Err(_) => limits.push(format!("{name}: unreadable line {}", n + 1)),
        }
    }
    LogRead { entries, limits, partial_tail }
}

/// W-0 + W-1: open, take the next seq, complete the header, write one line in one write, sync.
pub fn append(log: &Path, kind: &str, recorder: &Recorder, body: Value) -> Result<Value, String> {
    append_validated(
        log,
        kind,
        recorder,
        body,
        crate::schema_validation::bundled(),
    )
}

fn append_validated(
    log: &Path,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    validation: Result<&crate::schema_validation::RecordValidator, String>,
) -> Result<Value, String> {
    append_minted(
        log,
        kind,
        recorder,
        body,
        crate::util::opaque_id("rec:app:"),
        validation,
    )
}

fn append_minted(
    log: &Path,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    identity: Result<String, String>,
    validation: Result<&crate::schema_validation::RecordValidator, String>,
) -> Result<Value, String> {
    append_reserved(log, kind, recorder, body, identity?, None, None, RecordSet::Complete, validation)
}

pub fn append_with_id(
    log: &Path,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    id: &str,
) -> Result<Value, String> {
    append_reserved(
        log,
        kind,
        recorder,
        body,
        id.to_owned(),
        None,
        None,
        RecordSet::Complete,
        crate::schema_validation::bundled(),
    )
}

/// One project log per run and actual writer; run identity is retained in the entry.
pub fn append_project(
    root: &Path,
    run: Option<&str>,
    writer: &str,
    kind: &str,
    recorder: &Recorder,
    body: Value,
) -> Result<Value, String> {
    let log = crate::storage::project_log(root, run, writer);
    append_reserved(
        &log,
        kind,
        recorder,
        body,
        crate::util::opaque_id("rec:app:")?,
        run,
        None,
        RecordSet::Complete,
        crate::schema_validation::bundled(),
    )
}

/// W-1/W-2 for an observation whose identity was reserved when it was observed:
/// the run log keeps the reserved `recordId` and the original `observedAt`,
/// whether written now or late. W-1 validation still applies.
pub(crate) fn append_project_reserved(
    root: &Path,
    run: &str,
    writer: &str,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    id: &str,
    observed_at: &str,
) -> Result<Value, String> {
    append_project_reserved_in(root, run, writer, kind, recorder, body, id, observed_at, RecordSet::Complete)
}
/// As `append_project_reserved`, with what the writer requires of the other logs.
#[allow(clippy::too_many_arguments)]
pub(crate) fn append_project_reserved_in(
    root: &Path,
    run: &str,
    writer: &str,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    id: &str,
    observed_at: &str,
    set: RecordSet,
) -> Result<Value, String> {
    if run.is_empty() || id.is_empty() || observed_at.is_empty() {
        return Err("run, reserved identity and original observation time required".into());
    }
    append_reserved(
        &crate::storage::project_log(root, Some(run), writer),
        kind,
        recorder,
        body,
        id.to_owned(),
        Some(run),
        Some(observed_at),
        set,
        crate::schema_validation::bundled(),
    )
}
/// W-2: after late entries are written, one `evidence_limit` "record write
/// failed" names the subject. Idempotent: an existing limit for it is kept.
pub(crate) fn note_project_late_write(
    root: &Path,
    run: &str,
    writer: &str,
    subject: &str,
    detail: &str,
    set: RecordSet,
) -> Result<(), String> {
    let log = crate::storage::project_log(root, Some(run), writer);
    // The readable "record write failed" limits naming `subject`, across the
    // project (bounded index) and in the owning log.
    let (mut all, limits) = crate::records_index::with_index(root, |ix| (ix.late_limits_for(subject), ix.limits()));
    if set == RecordSet::Complete && !limits.is_empty() {
        return Err(format!("RS record set incomplete; nothing written: {limits:?}"));
    }
    crate::storage::check_path(&log)?;
    if read_log_parts(&log).partial_tail.is_some() {
        w0_open(root, &log)?;
    }
    let own_read = read_log_parts(&log);
    if !own_read.limits.is_empty() {
        return Err(format!("RS owning log incomplete; nothing written: {:?}", own_read.limits));
    }
    let own: Vec<Value> = own_read.entries.into_iter().filter(|e| e["kind"] == "evidence_limit" && e["body"]["label"] == "record write failed" && e["body"]["subjectRef"] == subject).collect();
    if set == RecordSet::ReadableBesideIncomplete {
        for entry in &own {
            if !all.contains(entry) {
                all.push(entry.clone());
            }
        }
    }
    let entries = if set == RecordSet::ReadableBesideIncomplete {
        // Only this writer's own limit settles its uncertain late append.
        &own
    } else {
        &all
    };
    if let Some(limit) = entries.iter().find(|e| {
        e["kind"] == "evidence_limit"
            && e["body"]["label"] == "record write failed"
            && e["body"]["subjectRef"] == subject
            && (set == RecordSet::Complete || e["runId"] == run)
    }) {
        if set == RecordSet::ReadableBesideIncomplete {
            let id = limit["recordId"].as_str().unwrap_or_default();
            let mut holding = crate::records_index::with_index(root, |ix| ix.entries_with(id));
            if !holding.contains(limit) { holding.push(limit.clone()); }
            if holding.len() > 1 {
                return Err(format!("late-write limit identity {} has readable duplicate or conflicting content; owning limit cannot be reconciled", limit["recordId"]));
            }
            crate::storage::sync_publication(&log)?;
        }
        return Ok(());
    }
    append_reserved(
        &log,
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"record write failed","subjectRef":subject,"detail":detail}),
        crate::util::opaque_id("rec:app:")?,
        Some(run),
        None,
        set,
        crate::schema_validation::bundled(),
    )?;
    Ok(())
}

/// Writer owns reservation; this is called only after actual capture publication is durable.
pub(crate) fn prepare_capture_submission(
    root: &Path,
    capture: &Value,
    log: &str,
) -> Result<Value, String> {
    crate::schema_validation::validate_capture(capture)?;
    let id = capture["captureId"]
        .as_str()
        .ok_or("capture identity absent")?;
    let path = crate::storage::capture_path(root, id);
    let durable: Value = serde_json::from_slice(&std::fs::read(&path).map_err(|e| e.to_string())?)
        .map_err(|e| e.to_string())?;
    if &durable != capture || durable.get("recordId").is_some() {
        return Err("writer reservation requires original durable unlinked capture".into());
    }
    crate::storage::sync_publication(&path)?;
    Ok(
        json!({"capture":capture,"recordId":crate::util::opaque_id("rec:app:")?,"log":log,"observedAt":capture["capturedAt"],"delayed":false}),
    )
}
pub(crate) fn persist_capture_submission(root: &Path, pending: &Value) -> Result<(), String> {
    let id = pending["capture"]["captureId"]
        .as_str()
        .ok_or("submission capture absent")?;
    let path = crate::storage::pending_path(root, id);
    if path.exists() {
        let existing: Value =
            serde_json::from_slice(&std::fs::read(&path).map_err(|e| e.to_string())?)
                .map_err(|e| e.to_string())?;
        if existing["capture"] != pending["capture"]
            || existing["recordId"] != pending["recordId"]
            || existing["observedAt"] != pending["observedAt"]
        {
            return Err("writer pending identity/facts conflict".into());
        }
        crate::storage::replace_json(&path, pending)
    } else {
        crate::storage::create_json(&path, pending)
    }
}
pub(crate) fn note_capture_submission_failure(
    root: &Path,
    pending: &mut Value,
    error: &str,
) -> Result<(), String> {
    pending["delayed"] = json!(true);
    pending["writeFailure"] = json!(error);
    persist_capture_submission(root, pending)
}
/// Kind is derived from the original schema-validated capture, never a caller label.
pub(crate) fn capture_record_kind(capture: &Value) -> Result<&'static str, String> {
    crate::schema_validation::validate_capture(capture)?;
    match capture["choice"].as_str() {
        Some("act") => Ok("human_act"),
        Some("decline") if matches!(capture["actKind"].as_str(), Some("A4" | "A6" | "A7")) => Ok("act_declined"),
        _ => Err("Unsupported capture choice/kind".into()),
    }
}
pub(crate) fn append_capture_submission(
    root: &Path,
    pending: &Value,
    body: Value,
) -> Result<Value, String> {
    if body != crate::act_control::act_body(&pending["capture"]) {
        return Err("Record body differs from original capture projection".into());
    }
    let log = pending["log"].as_str().ok_or("pending log absent")?;
    let rid = pending["recordId"]
        .as_str()
        .ok_or("writer pending identity absent")?;
    let observed = pending["observedAt"]
        .as_str()
        .ok_or("pending original observedAt absent")?;
    append_reserved(
        &root.join(log),
        capture_record_kind(&pending["capture"])?,
        &APP_INTERFACE,
        body,
        rid.into(),
        None,
        Some(observed),
        RecordSet::Complete,
        crate::schema_validation::bundled(),
    )
}
pub(crate) fn finish_capture_delay(root: &Path, pending: &Value) -> Result<(), String> {
    if pending["delayed"] != true {
        return Ok(());
    }
    let (entries, limits) = crate::storage::read_all(root);
    if !limits.is_empty() {
        return Err(format!("delay evidence record set incomplete: {limits:?}"));
    }
    let rid = pending["recordId"]
        .as_str()
        .ok_or("pending record absent")?;
    if entries.iter().any(|e| {
        e["kind"] == "evidence_limit"
            && e["body"]["label"] == "record write failed"
            && e["body"]["subjectRef"] == rid
    }) {
        return Ok(());
    }
    append(
        &root.join(pending["log"].as_str().ok_or("pending log absent")?),
        "evidence_limit",
        &APP_WRITER,
        json!({"label":"record write failed","subjectRef":rid,"detail":pending["writeFailure"].as_str().unwrap_or("captured act was written after its original observation")}),
    )?;
    Ok(())
}

/// The RS entry `append_reserved` writes, with its writer sequence.
pub(crate) fn envelope(kind: &str, recorder: &Recorder, body: Value, id: String, seq: u64, run: Option<&str>, observed_at: Option<&str>) -> Value {
    let mut entry = json!({
        "format": "chirality.rs.record",
        "formatVersion": "0.1",
        "recordId": id,
        "kind": kind,
        "recorder": {"role": recorder.role, "identity": recorder.identity},
        "context": {"surface": "App"},
        "seq": seq,
        "writtenAt": now_rfc3339(),
        "body": body,
    });
    if let Some(run) = run {
        entry["runId"] = json!(run);
    }
    if let Some(observed) = observed_at {
        entry["observedAt"] = json!(observed);
    }
    entry
}
/// RS §14.1 Permanent refusals, RS W-1 (a): why the App writer's entry for this reserved
/// observation would be refused as nonconformant on every write. None when it
/// conforms, or when validation itself is unavailable (not a definite refusal).
pub(crate) fn nonconformance(kind: &str, body: &Value, id: &str, run: &str, observed_at: &str) -> Option<String> {
    let validator = crate::schema_validation::bundled().ok()?;
    let entry = envelope(kind, &APP_WRITER, body.clone(), id.to_owned(), 1, Some(run), Some(observed_at));
    validator.validate(&entry).err()
}
/// RS §14.1 W-0: the bytes that terminate `existing`'s torn last line and
/// append the writer's "partial entry not recovered" limit (taking `seq`)
/// naming that line, with the torn bytes' length and digest. `all` is every
/// readable entry the identity is checked against.
fn w0_bytes(log: &Path, tail: &[u8], line_no: usize, seq: u64, run: Option<&str>, holds: &dyn Fn(&str) -> bool, validator: &crate::schema_validation::RecordValidator) -> Result<Vec<u8>, String> {
    let limit_id = crate::util::opaque_id("rec:app:")?;
    if holds(&limit_id) {
        return Err(format!("record identity conflict: {limit_id}; nothing written"));
    }
    let name = log.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
    let limit = envelope("evidence_limit", &APP_WRITER, json!({"label":PARTIAL_NOT_RECOVERED,"subjectRef":format!("line {line_no}"),
        "detail":format!("{} torn bytes at the end of {name} (sha256 {}) were terminated and kept unread when the writer reopened the log (RS §14.1 W-0, FC-2)", tail.len(), crate::util::sha256_hex(tail))}),
        limit_id, seq, run, run.map(|_| now_rfc3339()).as_deref());
    validator.validate(&limit)?;
    let mut bytes = b"\n".to_vec();
    bytes.extend(serde_json::to_vec(&limit).map_err(|e| e.to_string())?);
    bytes.push(b'\n');
    Ok(bytes)
}
fn read_tail(log: &Path, from: u64) -> Result<Vec<u8>, String> {
    use std::io::{Read, Seek, SeekFrom};
    let mut f = std::fs::File::open(log).map_err(|e| format!("read owning log: {e}"))?;
    f.seek(SeekFrom::Start(from)).map_err(|e| format!("read owning log: {e}"))?;
    let mut b = Vec::new();
    f.read_to_end(&mut b).map_err(|e| format!("read owning log: {e}"))?;
    Ok(b)
}
fn w0_write(log: &Path, bytes: &[u8]) -> Result<(), String> {
    let mut f = OpenOptions::new().append(true).open(log).map_err(|e| format!("open log: {e}"))?;
    f.write_all(bytes).map_err(|e| format!("W-0 repair write: {e}; nothing more written"))?;
    f.sync_all().map_err(|e| format!("W-0 repair sync uncertain: {e}; nothing more written"))?;
    crate::storage::sync_publication(log)
}
/// W-0 when a writer opens its log for reconciliation rather than an append:
/// under the writer lock, a torn last line is terminated and named (the
/// owning log is then complete). `all` is every readable entry of the set.
fn w0_open(root: &Path, log: &Path) -> Result<(), String> {
    let validator = crate::schema_validation::bundled().map_err(|e| format!("RS W-1 validation unavailable; nothing written: {e}"))?;
    let lock_path = crate::storage::records_root(log).map(|r| r.join(".writer.lock")).unwrap_or_else(|| log.with_extension("ownership.lock"));
    let _ownership = crate::storage::lock(&lock_path)?;
    let existing = std::fs::read(log).map_err(|e| format!("read owning log: {e}"))?;
    if existing.is_empty() || existing.ends_with(b"\n") {
        return Ok(());
    }
    let own = read_log_parts(log);
    if !own.limits.is_empty() {
        return Err(format!("RS owning log incomplete; nothing written: {:?}", own.limits));
    }
    let seq = own.entries.iter().filter_map(|e| e["seq"].as_u64()).max().unwrap_or(0).checked_add(1).ok_or("writer sequence exhausted; nothing written")?;
    let run = own.entries.iter().find_map(|e| e["runId"].as_str()).map(str::to_owned);
    let start = existing.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
    let line_no = existing[..start].iter().filter(|b| **b == b'\n').count() + 1;
    let bytes = crate::records_index::with_index(root, |ix| w0_bytes(log, &existing[start..], line_no, seq, run.as_deref(), &|id| ix.holds(id), validator))?;
    w0_write(log, &bytes)
}
fn append_reserved(
    log: &Path,
    kind: &str,
    recorder: &Recorder,
    body: Value,
    id: String,
    run: Option<&str>,
    observed_at: Option<&str>,
    set: RecordSet,
    validation: Result<&crate::schema_validation::RecordValidator, String>,
) -> Result<Value, String> {
    let validator =
        validation.map_err(|e| format!("RS W-1 validation unavailable; nothing written: {e}"))?;
    crate::storage::check_path(log)?;
    let records_root = crate::storage::records_root(log);
    let lock_path = records_root
        .as_ref()
        .map(|r| r.join(".writer.lock"))
        .unwrap_or_else(|| log.with_extension("ownership.lock"));
    let _ownership = crate::storage::lock(&lock_path)?;
    let project = records_root.as_ref().and_then(|r| r.parent()).and_then(|r| r.parent()).map(Path::to_path_buf);
    // The owning log and the project's record set, through the bounded index
    // (`records_index`): limits, identities and the next `seq` without
    // reading the history again. Another writer's torn tail is a partial,
    // never an entry (R-2): it cannot hold an identity and does not make the
    // set incomplete. If discovery itself fails, only the owning log is read.
    let indexed = project.as_ref().map(|root| crate::records_index::with_index(root, |ix| {
        let own = ix.own(log);
        let held = ix.holds(&id);
        (own.map(|o| (o.limits, o.partial, o.next_seq, o.complete_end, o.complete_lines)), ix.limits(), ix.discovery_failed(), held)
    }));
    let (own_limits, torn, next_seq, complete_end, complete_lines, set_limits, held) = match indexed {
        Some((Some((limits, partial, next, end, lines)), set_limits, false, held)) => (limits, partial, next, end, lines, set_limits, held),
        Some((None, set_limits, false, held)) if !log.exists() => (vec![], false, Some(1), 0, 0, set_limits, held),
        other => {
            // Outside a records tree, or discovery failed: the owning log alone.
            let own = read_log_parts(log);
            let existing = std::fs::read(log).unwrap_or_default();
            let end = existing.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1) as u64;
            let lines = existing[..end as usize].iter().filter(|b| **b == b'\n').count();
            let next = own.entries.iter().filter_map(|e| e["seq"].as_u64()).max().unwrap_or(0).checked_add(1);
            let held = own.entries.iter().any(|e| e["recordId"].as_str() == Some(id.as_str())) || other.as_ref().is_some_and(|o| o.3);
            let set_limits = other.map(|o| o.1).unwrap_or_default();
            (own.limits, own.partial_tail.is_some(), next, end, lines, set_limits, held)
        }
    };
    if !own_limits.is_empty() {
        return Err(format!("incomplete owning log: {own_limits:?}"));
    }
    if !set_limits.is_empty() && set == RecordSet::Complete {
        return Err(format!("record-set conflict/incomplete: {set_limits:?}"));
    }
    if held {
        return Err(format!("record identity conflict: {id}; nothing written"));
    }
    let mut seq = next_seq.ok_or("writer sequence exhausted; nothing written")?;
    // W-0: terminate the torn last line in place and record that it was not
    // recovered, in one write, before this append.
    let repair = if torn {
        let tail = read_tail(log, complete_end)?;
        let holds = |candidate: &str| candidate == id || project.as_ref().is_some_and(|root| crate::records_index::with_index(root, |ix| ix.holds(candidate)));
        Some(w0_bytes(log, &tail, complete_lines + 1, seq, run, &holds, validator)?)
    } else { None };
    if repair.is_some() {
        seq = seq.checked_add(1).ok_or("writer sequence exhausted; nothing written")?;
    }
    let entry = envelope(kind, recorder, body, id, seq, run, observed_at);
    validator.validate(&entry)?;
    if let Some(bytes) = repair {
        w0_write(log, &bytes)?;
    }
    let mut line = serde_json::to_string(&entry).map_err(|e| e.to_string())?;
    line.push('\n');
    if let Some(dir) = log.parent() {
        crate::storage::ensure_directory(dir)?;
    }
    let mut f = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log)
        .map_err(|e| format!("open log: {e}"))?;
    f.write_all(line.as_bytes())
        .map_err(|e| format!("write: {e}"))?;
    f.sync_all()
        .map_err(|e| format!("sync uncertain: {e}; do not replay before reconciliation"))?;
    crate::storage::sync_publication(log)?;
    Ok(entry)
}

#[cfg(test)]
#[path = "records_durability_tests.rs"]
mod durability_tests;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn entropy_failure_refuses_without_log_or_sequence() {
        let path =
            std::env::temp_dir().join(format!("entropy-refusal-{}.jsonl", std::process::id()));
        assert!(!path.exists());
        let identity =
            crate::util::opaque_id_with("rec:app:", |_| Err("fixture entropy failure".into()));
        assert!(append_minted(
            &path,
            "evidence_limit",
            &APP_WRITER,
            json!({"label":"unresolvable reference"}),
            identity,
            crate::schema_validation::bundled()
        )
        .unwrap_err()
        .contains("entropy"));
        assert!(!path.exists());
    }

    #[test]
    fn unavailable_validation_refuses_without_creating_a_log() {
        let path = std::env::temp_dir().join(format!(
            "w1-unavailable-{}-{}.jsonl",
            std::process::id(),
            now_rfc3339()
        ));
        assert!(!path.exists());
        let result = append_validated(
            &path,
            "human_act",
            &APP_INTERFACE,
            json!({}),
            Err("schema setup failed".into()),
        );
        assert!(result.unwrap_err().contains("validation unavailable"));
        assert!(!path.exists());
        // Preserve an existing log on setup failure too, including unresolved refs.
        std::fs::write(&path, b"existing bytes\n").unwrap();
        let mut root: Value =
            serde_json::from_str(crate::schema_validation::RESOURCES[0].1).unwrap();
        root["$defs"]["missing"] = json!({"$ref": "https://example.invalid/schema"});
        let text = serde_json::to_string(&root).unwrap();
        let mut resources = crate::schema_validation::RESOURCES.to_vec();
        resources[0].1 = &text;
        let validation = crate::schema_validation::RecordValidator::from_resources(&resources);
        assert!(validation.is_err());
        let result = append_validated(
            &path,
            "human_act",
            &APP_INTERFACE,
            json!({}),
            validation.as_ref().map_err(Clone::clone),
        );
        assert!(result.unwrap_err().contains("validation unavailable"));
        assert_eq!(std::fs::read(&path).unwrap(), b"existing bytes\n");
        std::fs::remove_file(path).unwrap();
    }
}
