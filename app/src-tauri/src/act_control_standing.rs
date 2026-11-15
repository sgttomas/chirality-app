//! A16's facts from one decision-view read. Request identity and exact recorded path are
//! separate: another request at that path establishes neither the same file nor a version.
use crate::native_text::{self as nt, Placed, Source, Unfit};
use serde_json::{json, Value};
use std::path::Path;

pub(super) const CAUSES: &[&str] = &[
    "The decision records could not all be read",
    "The record history may be incomplete",
    "The request could not be resolved uniquely",
    "The request was not found in the decision view",
    "The request's recorded standing could not be resolved",
];
pub(super) const CHANGED: &str = "The recorded standing of this request or other requests for this path changed since this was shown: review it again; nothing captured.";
fn unknown(cause: usize) -> Value {
    json!({"form":"unknown","cause":CAUSES[cause]})
}
fn whole(view: &Value) -> bool {
    view["limits"].as_array().is_some_and(Vec::is_empty)
        && view["historyNotices"].as_array().is_some_and(Vec::is_empty)
}
fn resolved_limits(row: &Value) -> bool {
    row["limits"].as_array().is_some_and(|limits| {
        limits.iter().all(|limit| {
            matches!(limit.as_str(),
        Some("package file differs from the content the request recorded" |
            "lapse history is a recorded observation claim; native origin not verified"))
        })
    })
}
fn form(view: &Value, row: Option<&Value>) -> Value {
    if !view["limits"].as_array().is_some_and(Vec::is_empty) {
        return unknown(0);
    }
    if !view["historyNotices"].as_array().is_some_and(Vec::is_empty) {
        return unknown(1);
    }
    let Some(row) = row else { return unknown(3) };
    if row["state"] == "unresolvable request identity" {
        return unknown(2);
    }
    if row["state"] == "ambiguous current standing" {
        return json!({"form":"several-unordered"});
    }
    if !resolved_limits(row) {
        return unknown(4);
    }
    if row["state"] == "decided" && row["decision"]["alternativeChosen"].as_str().is_some() {
        // Equivalent records of one capture can have no single act/recording time. Do not
        // pick a clock winner or demote the established alternative. time() renders this
        // App-owned absence label as an explicit placeholder in either presentation.
        let recorded = row["decision"]["recordedAt"]
            .as_str()
            .unwrap_or("not uniquely established");
        return json!({"form":"decided","alternative":row["decision"]["alternativeChosen"],"recordedAt":recorded});
    }
    if row["state"] == "pending — awaiting the person's decision"
        && row["limits"].as_array().is_some_and(Vec::is_empty)
        && row["contenders"].as_array().is_some_and(Vec::is_empty)
    {
        return json!({"form":"none-recorded"});
    }
    unknown(4)
}

/// Both offer properties from every row of one derive. No writer/act/capture lock is taken
/// here; the native caller holds its act mutex, before capture and writer ownership.
pub(super) fn read(root: &Path, request: &str, path: &str) -> (Value, Value) {
    from_view(&crate::decision_view::derive(root, &[]), request, path)
}
fn from_view(view: &Value, request: &str, path: &str) -> (Value, Value) {
    let all = view["rows"]
        .as_array()
        .map(Vec::as_slice)
        .unwrap_or_default();
    let own: Vec<_> = all.iter().filter(|row| row["package"] == request).collect();
    let standing = if own.len() > 1 {
        unknown(2)
    } else {
        form(view, own.first().copied())
    };
    let mut rows = Vec::new();
    // Completeness of other requests is independent of the own row's standing.
    // Its ambiguity is already carried by packageStanding.
    let mut read_whole = whole(view);
    for row in all
        .iter()
        .filter(|row| row["packageFile"] == path && row["package"] != request)
    {
        let standing = form(view, Some(row));
        read_whole &= standing["form"] != "unknown" && resolved_limits(row);
        let relation = own.first().map_or("another", |own| relation(row, own));
        let mut other = standing;
        other["requestRef"] = row["package"].clone();
        other["relation"] = json!(relation);
        if let Some(own) = own.first() {
            let (a, b) = (&row["requestContent"], &own["requestContent"]);
            // Values are comparable only under the same recorded method. No replacement
            // identity is computed, and an incomparable method is never called different.
            if a["method"].as_str().is_some()
                && a["method"] == b["method"]
                && a["value"].as_str().is_some()
                && b["value"].as_str().is_some()
            {
                other["differentContent"] = json!(a["value"] != b["value"]);
            }
        }
        rows.push(other);
    }
    // Use only log sequence evidence for order. Equivalent duplicated sources and different
    // logs do not acquire an order from vector position, record id or wall-clock time.
    // Group unrelated logs in their existing display order; only within a single proved
    // log is descending sequence meaningful. This is a total display sort, not a claim
    // that requests from different logs are ordered.
    let mut logs = Vec::new();
    let mut ordered: Vec<_> = rows
        .into_iter()
        .enumerate()
        .map(|(index, row)| {
            let source = all
                .iter()
                .find(|r| r["package"] == row["requestRef"])
                .and_then(|r| r["requestSources"].as_array())
                .filter(|s| s.len() == 1)
                .map(|s| &s[0]);
            let log = source.and_then(|s| s["log"].as_str()).map(str::to_owned);
            let key = log.unwrap_or_else(|| format!("unresolved:{index}"));
            let group = logs.iter().position(|l| l == &key).unwrap_or_else(|| {
                logs.push(key);
                logs.len() - 1
            });
            (
                group,
                std::cmp::Reverse(source.and_then(|s| s["seq"].as_u64()).unwrap_or(0)),
                row,
            )
        })
        .collect();
    ordered.sort_by_key(|(group, seq, _)| (*group, *seq));
    let rows: Vec<_> = ordered.into_iter().map(|(_, _, row)| row).collect();
    (
        standing,
        json!({"state":if read_whole {"read-whole"} else {"not-read-whole"},"rows":rows}),
    )
}
fn relation(a: &Value, b: &Value) -> &'static str {
    let sources = |r: &Value| {
        r["requestSources"]
            .as_array()
            .filter(|s| s.len() == 1)
            .and_then(|s| s.first())
            .cloned()
    };
    if let Some((a, b)) = sources(a).zip(sources(b)) {
        if a["log"] == b["log"] {
            if let Some((a, b)) = a["seq"].as_u64().zip(b["seq"].as_u64()) {
                if a < b {
                    return "earlier";
                }
                if a > b {
                    return "later";
                }
            }
        }
    }
    "another"
}

/// Inline values are closed; unfit identifiers travel after the sentence, under their own
/// supplied label. The sentence's placeholder never carries any of the original value.
fn inline(placed: Placed, extra: &mut Vec<String>) -> String {
    match placed {
        Placed::Inline(c) => c.to_string(),
        Placed::Lines(s) => {
            extra.extend_from_slice(s.lines());
            nt::VALUE_NOT_SHOWN.into()
        }
    }
}
fn id(value: &Value, label: &'static str, extra: &mut Vec<String>, whole: bool) -> String {
    let placed = nt::identifier(
            value,
            Unfit::Supplied {
                label,
                source: Source::Record,
            },
        );
    let placed = match placed {
        Placed::Lines(_) if whole => Placed::Lines(nt::supplied_whole(label, Source::Record, value)),
        placed => placed,
    };
    inline(placed, extra)
}
fn time(value: &Value) -> String {
    inline(
        nt::time(
            value,
            Unfit::Withhold("(recording time not uniquely established)"),
        ),
        &mut Vec::new(),
    )
}
pub(super) fn line(standing: &Value) -> Vec<String> {
    standing_line(standing, false, false)
}
pub(super) fn line_whole(standing: &Value) -> Vec<String> {
    standing_line(standing, true, false)
}
/// The fallback summary's form: closed words only. A recorded alternative that is not a
/// plain identifier is named as shown in the App, where its whole marked value is.
pub(super) fn line_summary(standing: &Value) -> Vec<String> {
    standing_line(standing, false, true)
}
fn standing_line(standing: &Value, whole: bool, summary: bool) -> Vec<String> {
    let mut extra = Vec::new();
    let words = match standing["form"].as_str() {
        Some("decided") => {
            let alternative = match nt::identifier(&standing["alternative"], Unfit::Withhold("")) {
                Placed::Inline(closed) if summary && !closed.as_str().is_empty() => format!("alternative {closed}"),
                _ if summary => "an alternative shown in the App".into(),
                _ => format!("alternative {}", id(&standing["alternative"], "Recorded alternative", &mut extra, whole)),
            };
            format!("A decision on this request is already recorded: {alternative}, recorded at {}. Deciding again records another decision; both are kept.", time(&standing["recordedAt"]))
        }
        Some("several-unordered") => "Several decisions on this request are recorded, and the records do not establish which stands. Deciding again records another decision; all are kept.".into(),
        Some("none-recorded") => "No decision on this request is in the records as read; the log is not signed, so a removed entry would not show.".into(),
        _ => {
            let cause = standing["cause"].as_str().filter(|c| CAUSES.contains(c)).unwrap_or(CAUSES[4]);
            format!("Whether a decision on this request is already recorded is not known: {cause}.")
        }
    };
    [vec![words], extra].concat()
}
fn other_line(row: &Value, whole: bool) -> Vec<String> {
    let mut extra = Vec::new();
    let prefix = match row["relation"].as_str() {
        Some("earlier") => "An earlier request",
        Some("later") => "A later request",
        _ => "Another request",
    };
    let reference = id(&row["requestRef"], "Other request", &mut extra, whole);
    let mut words = match row["form"].as_str() {
        Some("decided") => format!("{prefix} for the file at this path has a recorded decision: alternative {}, recorded at {} (request {reference}).", id(&row["alternative"], "Recorded alternative", &mut extra, whole), time(&row["recordedAt"])),
        Some("several-unordered") => format!("{prefix} for the file at this path: decisions recorded, order not established (request {reference})."),
        Some("none-recorded") => format!("{prefix} for the file at this path: no decision in the records as read (request {reference})."),
        _ => {
            let cause = row["cause"].as_str().filter(|c| CAUSES.contains(c)).unwrap_or(CAUSES[4]);
            format!("{prefix} for the file at this path: standing not known: {cause} (request {reference}).")
        }
    };
    if row["differentContent"] == true {
        words.push_str(" It was made on different content.");
    }
    [vec![words], extra].concat()
}
pub(super) fn other_lines(other: &Value, limit: usize) -> Vec<String> {
    limited_other_lines(other, limit, false)
}
pub(super) fn other_lines_uncut(other: &Value, limit: usize) -> Vec<String> {
    limited_other_lines(other, limit, true)
}
fn limited_other_lines(other: &Value, limit: usize, whole: bool) -> Vec<String> {
    let mut out = Vec::new();
    if other["state"] != "read-whole" {
        out.push("Other requests for the file at this path could not all be read.".into());
    }
    let rows = other["rows"]
        .as_array()
        .map(Vec::as_slice)
        .unwrap_or_default();
    let decided: Vec<_> = rows.iter().filter(|r| r["form"] == "decided").collect();
    let selected: Vec<_> = if decided.is_empty() {
        rows.iter().take(limit).collect()
    } else {
        decided.into_iter().take(limit).collect()
    };
    for row in &selected {
        out.extend(other_line(row, whole));
    }
    let left = rows.len() - selected.len();
    if left > 0 && selected.is_empty() {
        out.push(format!("{left} other {} for the file at this path: shown in the App", if left == 1 { "request" } else { "requests" }));
    } else if left > 0 {
        out.push(format!("and {left} more, shown in the App"));
    }
    out
}

/// The App counterpart retains every row and every marked value without alert cuts.
pub(super) fn other_lines_whole(other: &Value) -> Vec<String> {
    let mut out = Vec::new();
    if other["state"] != "read-whole" {
        out.push("Other requests for the file at this path could not all be read.".into());
    }
    for row in other["rows"].as_array().map(Vec::as_slice).unwrap_or_default() {
        out.extend(other_line(row, true));
    }
    out
}

/// One account of A16 shown-statement evidence, shared by the decision reader and capture
/// reconciliation. A digest's presence is not agreement with any reconstructed statement.
/// The record chain covers the record's capture ID, not this separate file or its digest.
pub(crate) fn shown_statement_binding(root: &Path, body: &Value) -> Value {
    let read = || -> Result<Value, String> {
        let refs = body["captureEvidence"]
            .as_array()
            .ok_or("capture reference unavailable")?;
        if refs.len() != 1 {
            return Err("one original capture reference required".into());
        }
        let id = refs[0]["ref"]
            .as_str()
            .ok_or("capture identity unavailable")?;
        let path = crate::storage::capture_path(root, id)?;
        crate::storage::check_path(&path)?;
        let meta = std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?;
        if !meta.is_file() {
            return Err("capture is not a regular file".into());
        }
        let before = crate::records_index::Stamp::of(&meta);
        let mut file = crate::records_index::open_log(&path).map_err(|e| e.to_string())?;
        if crate::records_index::Stamp::of(&file.metadata().map_err(|e| e.to_string())?) != before {
            return Err("capture changed before read".into());
        }
        let mut bytes = Vec::new();
        std::io::Read::read_to_end(&mut file, &mut bytes).map_err(|e| e.to_string())?;
        let capture: Value = serde_json::from_slice(&bytes).map_err(|e| e.to_string())?;
        let after = crate::records_index::Stamp::of(
            &std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?,
        );
        if before != after
            || crate::records_index::Stamp::of(&file.metadata().map_err(|e| e.to_string())?)
                != before
        {
            return Err("capture changed while read".into());
        }
        crate::schema_validation::validate_capture(&capture)?;
        if capture["captureId"] != id
            || capture["actKind"] != "A16"
            || super::act_body(&capture) != *body
        {
            return Err("capture facts do not match this decision record".into());
        }
        Ok(capture)
    };
    let Ok(capture) = read() else {
        return json!({"state":"not-bound","statement":"Whether what was shown is bound in this capture could not be established."});
    };
    let Some(digest) = capture.get("shownStatement") else {
        return json!({"state":"not-bound","statement":"What was shown is not bound in this capture."});
    };
    // Earlier captures and failed publications can be unsealed. Check a seal when recorded;
    // a digest alone establishes neither the writer's identity nor physical display.
    if capture.get("seal").is_some() && crate::capture_seal::verify(root, &capture).is_err() {
        return json!({"state":"not-bound","statement":"A statement digest is recorded, but this capture's seal could not be checked; what was shown is not bound here."});
    }
    json!({"state":"bound","digest":digest,"statement":"What was shown is bound by the statement digest stored in this capture. The chained human_act record cites only the capture ID, carrying neither that digest nor a hash of the capture file. The records chain does not protect any capture field; an edited unsealed digest still reads bound. This does not establish who wrote the capture, that macOS displayed those bytes or that the person read them."})
}
