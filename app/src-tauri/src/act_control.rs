//! App act control: A16 decide and closed native A15 registration capture.
//!
//! DEL-01-04 APP_ACT_CONTROL.md (AAC-v0.3):
//! - §1.2 row A16: one decision package per act, wording "decide", no decline,
//!   actor the person, subject bound by the package file's content identity,
//!   the alternative chosen, relation to its `act_request`;
//! - §2 AI-9: the package reaches the control as a runtime value from the decision
//!   view; absent or changed package file -> not offered; fewer than two alternatives
//!   -> not offered;
//! - §3 transitions AX-01, AX-02, AX-03, AX-04, AX-05, AX-06, AX-08, AX-12, AX-13,
//!   and the refusals listed under the table (capture from AC-1, second capture);
//! - §4.1 steps 2-7 (compose from authoritative sources, present, re-read identity,
//!   capture evidence, write the record), AK-c, AK-e;
//! - §5.1 offer + offer digest, §5.2 capture evidence, §5.3 the RS entry;
//! - §6.1 NA-3/NA-4: only a host-native confirmation captures (the Tauri layer
//!   presents a native dialog; see lib.rs); §7 the person's identity.
//!
//! The RS `human_act` body follows DEL-04-03 RECORD_SEMANTICS.md §6.1 (A16 rows)
//! and HA-11; act class from DEL-04-01 ACT_AND_POLICY_CONTRACT.md §2.1 (A16,
//! "person's act (V4-PM-04)").

#[path = "act_control_file.rs"]
mod file_act;
pub(crate) use file_act::{FileActKind, FileActOfferRef, confirm_file_native};

#[path = "act_control_a15.rs"]
mod a15;
pub(crate) use a15::{review_digest, A15OfferRef, A15Variant, HotA15Receipt, HotA15Result};
use crate::canonical::{offer_digest, OFFER_DIGEST_METHOD};
use crate::recorder::LOG;
use crate::records;
use crate::storage;
use crate::util::{file_identity, now_rfc3339, package_snapshot, FILE_IDENTITY_METHOD};
use serde_json::{json, Value};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

pub const CAPTURE_STORE: &str = ".chirality/captures";
#[cfg(test)]
thread_local! {static FIXED_CAPTURE_TIME:std::cell::RefCell<Option<String>>=const {std::cell::RefCell::new(None)};}
fn capture_time() -> String {
    #[cfg(test)]
    if let Some(time) = FIXED_CAPTURE_TIME.with(|time| time.borrow().clone()) {
        return time;
    }
    now_rfc3339()
}

const STANDING: &str = "no arrival: a standing act (RC-6)";

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum InputSource {
    /// The host-owned native confirmation (§6.2 P-2).
    HostNativeConfirmation,
    WebviewScript,
    AgentTool,
    AppRule,
}

impl InputSource {
    fn label(self) -> &'static str {
        match self {
            InputSource::HostNativeConfirmation => "host-native-confirmation",
            InputSource::WebviewScript => "a webview script",
            InputSource::AgentTool => "an agent tool",
            InputSource::AppRule => "an App rule",
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub enum OfferState {
    Composed,      // AC-1
    Presented,     // AC-2
    Captured,      // AC-3
    Dismissed,     // AC-5
    Stale,         // AC-6
    Recorded,      // AC-7
    RecordPending, // AC-8
}

pub struct OfferSlot {
    pub offer: Value,
    pub state: OfferState,
    pub package_path: PathBuf,
    selected: Option<String>,
    frozen_offer: Option<Value>,
    frozen_actor: Option<Value>,
    // Actual complete RS request observed at compose; never supplied by renderer.
    request_record: Value,
}

struct NativeCapture {
    ordinal: usize,
    target_log: String,
    a15: Option<a15::A15Custody>,
    written: bool,
    delay_pending: bool,
    capture: Value,
    pending: Option<Value>,
    failure: Option<String>,
}

pub struct ActControl {
    pub workspace: PathBuf,
    pub offers: HashMap<String, OfferSlot>,
    native_captures: HashMap<String, NativeCapture>,
    a15_offers: HashMap<String, a15::A15OfferSlot>,
    file_offers: HashMap<String, file_act::FileActSlot>,
    file_capture_roots: HashMap<String, PathBuf>,
}

/// Preserve the exact request bound when this offer was composed. Identical
/// copies remain a reader-presentation case; compose still refuses incomplete
/// record sets, and native confirmation never chooses among bound-ID duplicates.
/// Unrelated append failure stays a recording matter. No filename/clock winner.
fn check_request_binding(
    workspace: &Path,
    original: &Value,
    offered_ref: &Value,
) -> Result<(), String> {
    if original["kind"] != "act_request" || offered_ref != &original["recordId"] {
        return Err(
            "request binding changed: offer no longer names its composed request; nothing captured"
                .into(),
        );
    }
    let (entries, limits) = storage::read_all(workspace);
    // Compose admitted this exact request from a complete schema/sequence-checked
    // set. Later unrelated partial append tails must not discard native capture
    // facts; existing recorder/recovery guards still hold those writes. Recheck
    // the bound, validated readable target rather than inventing a global veto.
    let matching = entries
        .iter()
        .filter(|entry| entry["recordId"] == original["recordId"])
        .collect::<Vec<_>>();
    if matching.len() > 1 {
        return Err(
            "request binding unavailable: duplicate bound request identity; nothing captured"
                .into(),
        );
    }
    if matching.first().copied() != Some(original) {
        return Err(format!("request binding changed or absent since offer composition; nothing captured; compose again from current sources; read limits: {limits:?}"));
    }
    Ok(())
}
/// The person as the App observes them (AAC §7; RS $defs/person; identity never verified).
pub fn person(display_name: Option<&str>, os_account: Option<&str>) -> Value {
    let mut p = json!({"identityVerified": false});
    if let Some(n) = display_name.filter(|s| !s.is_empty()) {
        p["displayName"] = json!(n);
    }
    if let Some(a) = os_account.filter(|s| !s.is_empty()) {
        p["osAccount"] = json!(a);
    }
    // Codex account: absent unless Codex reports one (never guessed); not signed in here.
    p
}

/// Presentation only (J6 D-1/D-3, V14 repairs): native confirmation statements
/// a person can read whole, with every button on screen. The alert has no
/// scrolling. A statement that does not fit is never truncated: where the
/// content can be named, the App shows it whole while the alert is open and the
/// alert names its digest; otherwise presentation is refused with its cause
/// (AAC §4.1a). Nothing here changes what an offer or capture binds.
pub(crate) mod native_statement {
    use serde_json::Value;
    use tauri_plugin_dialog::{MessageDialogButtons, MessageDialogResult};

    /// Logical lines in one native statement. Tunable after a native re-witness.
    pub(crate) const MAX_LINES: usize = 30;
    /// Characters in one native statement. Tunable after a native re-witness.
    pub(crate) const MAX_CHARS: usize = 1500;
    /// Shown before a full identity on its own (copyable) line.
    pub(crate) const SHORT: usize = 12;

    /// Refuses a statement that would not fit a readable native alert.
    pub(crate) fn bounded(what: &str, text: String) -> Result<String, String> {
        let (lines, chars) = (text.lines().count(), text.chars().count());
        if lines > MAX_LINES || chars > MAX_CHARS {
            return Err(format!(
                "{what}: the statement ({lines} lines, {chars} characters) exceeds the readable native confirmation ({MAX_LINES} lines, {MAX_CHARS} characters); nothing presented, nothing captured or sent"
            ));
        }
        Ok(text)
    }
    /// The first `SHORT` characters of an identity (it is then shown in full).
    pub(crate) fn short(value: &str) -> &str {
        value
            .char_indices()
            .nth(SHORT)
            .map_or(value, |(i, _)| &value[..i])
    }
    /// "name · OS account a · Codex account c (identity not verified)".
    pub(crate) fn actor_line(actor: &Value) -> String {
        let mut parts = vec![actor["displayName"]
            .as_str()
            .unwrap_or("no name set in the App")
            .to_owned()];
        if let Some(os) = actor["osAccount"].as_str() {
            parts.push(format!("OS account {os}"));
        }
        if let Some(codex) = actor["codexAccount"].as_str() {
            parts.push(format!("Codex account {codex}"));
        }
        format!("{} (identity not verified)", parts.join(" · "))
    }
    /// True only for the explicit act/confirm label: Cancel, Escape, closing the
    /// alert or any other result is not that choice.
    pub(crate) fn chose(result: &MessageDialogResult, label: &str) -> bool {
        matches!(result, MessageDialogResult::Custom(chosen) if chosen == label)
    }
    /// A native path identity (`attachments::native_path_identity`) as readable
    /// text. Display only: identities and comparisons keep the exact value.
    /// Valid UTF-8 is shown as itself; otherwise invalid bytes are shown as
    /// `\xNN` behind an explicit marker. `None` when `v` is not a path identity.
    pub(crate) fn native_path_text(v: &Value) -> Option<String> {
        let object = v.as_object()?;
        match object.get("encoding")?.as_str()? {
            "unix_bytes" | "native_encoded_bytes" => {
                let bytes = object
                    .get("bytes")?
                    .as_array()?
                    .iter()
                    .map(|b| b.as_u64().filter(|b| *b <= 255).map(|b| b as u8))
                    .collect::<Option<Vec<u8>>>()?;
                Some(match std::str::from_utf8(&bytes) {
                    Ok(text) => text.to_owned(),
                    Err(_) => format!(
                        "[path is not valid UTF-8; invalid bytes shown as \\xNN] {}",
                        escape_invalid(&bytes)
                    ),
                })
            }
            "windows_utf16" => {
                let units = object
                    .get("codeUnits")?
                    .as_array()?
                    .iter()
                    .map(|u| u.as_u64().filter(|u| *u <= 0xFFFF).map(|u| u as u16))
                    .collect::<Option<Vec<u16>>>()?;
                Some(match String::from_utf16(&units) {
                    Ok(text) => text,
                    Err(_) => format!(
                        "[path is not valid UTF-16; unpaired code units shown as \\u{{NNNN}}] {}",
                        char::decode_utf16(units.iter().copied())
                            .map(|r| r.map_or_else(
                                |e| format!("\\u{{{:04x}}}", e.unpaired_surrogate()),
                                String::from
                            ))
                            .collect::<String>()
                    ),
                })
            }
            _ => None,
        }
    }
    fn escape_invalid(mut bytes: &[u8]) -> String {
        let mut out = String::new();
        while !bytes.is_empty() {
            match std::str::from_utf8(bytes) {
                Ok(text) => {
                    out.push_str(text);
                    break;
                }
                Err(e) => {
                    let (valid, rest) = bytes.split_at(e.valid_up_to());
                    out.push_str(std::str::from_utf8(valid).unwrap_or_default());
                    let bad = e.error_len().unwrap_or(rest.len());
                    for b in &rest[..bad] {
                        out.push_str(&format!("\\x{b:02x}"));
                    }
                    bytes = &rest[bad..];
                }
            }
        }
        out
    }
    /// A JSON value as indented "key: value" lines, with native paths as text.
    /// Every member is shown; nothing is elided.
    pub(crate) fn readable(v: &Value) -> String {
        let mut out = Vec::new();
        render(None, v, 0, &mut out);
        out.join("\n")
    }
    fn scalar(v: &Value) -> Option<String> {
        if let Some(path) = native_path_text(v) {
            return Some(path);
        }
        match v {
            Value::Null => Some("null".into()),
            Value::Bool(b) => Some(b.to_string()),
            Value::Number(n) => Some(n.to_string()),
            Value::String(s) => Some(s.clone()),
            Value::Array(a) if a.is_empty() => Some("none".into()),
            Value::Object(o) if o.is_empty() => Some("none".into()),
            _ => None,
        }
    }
    fn render(key: Option<&str>, v: &Value, indent: usize, out: &mut Vec<String>) {
        let pad = "  ".repeat(indent);
        let label = key.map(|k| format!("{k}: ")).unwrap_or_default();
        if let Some(text) = scalar(v) {
            out.push(format!("{pad}{label}{text}"));
            return;
        }
        let child = if key.is_some() { indent + 1 } else { indent };
        match v {
            Value::Array(items) if items.iter().all(|i| scalar(i).is_some()) => {
                let joined = items.iter().filter_map(scalar).collect::<Vec<_>>().join(", ");
                out.push(format!("{pad}{label}{joined}"));
            }
            Value::Array(items) => {
                if let Some(k) = key {
                    out.push(format!("{pad}{k}:"));
                }
                for (i, item) in items.iter().enumerate() {
                    render(Some(&format!("{}", i + 1)), item, child, out);
                }
            }
            Value::Object(members) => {
                if let Some(k) = key {
                    out.push(format!("{pad}{k}:"));
                }
                for (k, member) in members {
                    render(Some(k), member, child, out);
                }
            }
            _ => unreachable!("scalars are handled above"),
        }
    }

    fn count(v: &Value) -> usize {
        v.as_array().map_or(0, Vec::len)
    }
    fn text_or<'a>(v: &'a Value, absent: &'a str) -> &'a str {
        v.as_str().unwrap_or(absent)
    }
    fn rows<'a>(v: &'a Value) -> impl Iterator<Item = &'a Value> {
        v.as_array().into_iter().flatten()
    }
    fn cell(v: &Value) -> String {
        scalar(v).unwrap_or_else(|| v.to_string())
    }
    /// One short line per item the assessment observed (DEL-01-05 AE-12,
    /// KE-13, Q-5: live turns, outstanding requests and active delegated
    /// children are all listed), plus the items it could not resolve.
    fn live_work_lines(view: &Value) -> Vec<String> {
        let mut t = Vec::new();
        for r in rows(&view["observedLiveTurns"]) {
            t.push(format!("Live turn: {} / {} ({})", cell(&r["threadId"]), cell(&r["turnId"]), cell(&r["status"])));
        }
        for r in rows(&view["observedOutstandingRequests"]) {
            t.push(format!(
                "Outstanding request: {} #{} in {}",
                cell(&r["method"]),
                cell(&r["requestIdentity"]),
                cell(&r["threadId"])
            ));
        }
        for r in rows(&view["observedActiveChildren"]) {
            t.push(format!(
                "Active child: {} (parent {}; {})",
                cell(&r["threadId"]),
                cell(&r["parentThreadId"]),
                cell(&r["reportedStatus"])
            ));
        }
        for r in rows(&view["knownChildActivityUnknown"]) {
            t.push(format!(
                "Child, activity unknown: {} (parent {})",
                cell(&r["threadId"]),
                cell(&r["parentThreadId"])
            ));
        }
        for r in rows(&view["coverage"]["turns"]["unresolved"]) {
            t.push(format!(
                "Turn observation unresolved: {} / {}",
                cell(&r["threadId"]),
                r["turnId"].as_str().unwrap_or("turn not reported")
            ));
        }
        t
    }
    /// Native logout or key-removal confirmation. Every observed item is listed
    /// one per line. When the list does not fit, the App shows the frozen
    /// assessment in full while the alert is open, and the alert gives the
    /// counts and names that assessment by digest; counts alone are never the
    /// whole statement.
    pub(crate) fn logout_statement(view: &Value) -> Result<NativeStatement, String> {
        let account = &view["account"];
        let generation = &view["generation"];
        let head = vec![
            "Log out through Codex for this exact native home?".to_owned(),
            format!(
                "Home: {} · App session {} · Codex process start {}",
                text_or(&view["modeHomeClass"], "not reported"),
                text_or(&generation["appSession"], "not reported"),
                cell(&generation["spawnCounter"])
            ),
            format!("Account: {}; native type {}", cell(&account["state"]), cell(&account["nativeType"])),
            format!("Account read: {}", text_or(&account["readAvailability"], "not reported")),
            format!("Current report: {}", text_or(&account["currentReport"]["state"], "not reported")),
            format!(
                "Observed: {} live turns, {} outstanding requests, {} active children, {} children with unknown activity, {} unresolved turn observations.",
                count(&view["observedLiveTurns"]),
                count(&view["observedOutstandingRequests"]),
                count(&view["observedActiveChildren"]),
                count(&view["knownChildActivityUnknown"]),
                count(&view["coverage"]["turns"]["unresolved"])
            ),
        ];
        let tail = vec![
            "Coverage of turns, requests and children is not complete.".to_owned(),
            text_or(&view["warning"], "").to_owned(),
            format!("Observed at {}.", text_or(&view["observedAt"], "not reported")),
            "OK sends the logout request once; Cancel sends nothing.".into(),
        ];
        let listed = live_work_lines(view);
        let whole = [head.clone(), listed, tail.clone()].concat().join("\n");
        whole_or_in_app("Logout confirmation", "logout assessment", whole, view, |digest| {
            [head, vec![format!("Each of these is listed in the frozen assessment, {IN_APP}"), digest.to_owned()], tail]
                .concat()
                .join("\n")
        })
    }
    /// Labels of the Stop/Restart Codex question (the owner's default-safe
    /// layout, `act_buttons`: Return keeps Codex running).
    pub(crate) const KEEP_CODEX: &str = "Keep Codex running";
    pub(crate) const STOP_CODEX: &str = "Stop Codex";
    pub(crate) const RESTART_CODEX: &str = "Restart Codex";
    /// DEL-01-04 §5.2 Stop Codex / Restart Codex question (C-12, K-4): the
    /// live turns, waiting requests, delegated agents and workflow runs in
    /// force, one per line; with none observed, a simple confirmation. When
    /// the list does not fit, the App shows the assessment in full while the
    /// alert is open and the alert names it by digest, as for logout.
    pub(crate) fn codex_stop_statement(view: &Value) -> Result<NativeStatement, String> {
        let restart = view["restart"] == true;
        let act = if restart { RESTART_CODEX } else { STOP_CODEX };
        let generation = &view["generation"];
        let runs = &view["runsInForce"];
        let live = count(&view["observedLiveTurns"]);
        let others = count(&view["observedOutstandingRequests"])
            + count(&view["observedActiveChildren"])
            + count(&view["knownChildActivityUnknown"])
            + count(&view["coverage"]["turns"]["unresolved"])
            + count(runs);
        let mut head = vec![
            format!("{act} for this home?"),
            format!(
                "Home: {} · App session {} · Codex process start {} · state {}",
                text_or(&view["modeHomeClass"], "not reported"),
                text_or(&generation["appSession"], "not reported"),
                cell(&generation["spawnCounter"]),
                text_or(&view["state"], "not reported")
            ),
        ];
        if view["changedWhileAsking"] == true {
            head.push("Live work changed while this question was open; this is the current list.".into());
        }
        if let Some(note) = view["notReady"].as_str() {
            head.push(format!("{note}."));
        }
        let mut listed = live_work_lines(view);
        for r in rows(runs) {
            listed.push(format!(
                "Workflow run in force: {} (run {}) in {}{}",
                text_or(&r["workflow"]["name"], "workflow not established"),
                cell(&r["run"]),
                cell(&r["conversation"]),
                if r["state"] == "open" { String::new() } else { format!("; {}", cell(&r["state"])) }
            ));
        }
        let mut tail = Vec::new();
        if live + others == 0 {
            head.push("Observed: no live turns, waiting requests, delegated agents or workflow runs in force.".into());
            tail.push(format!("{act} stops this Codex process{}.", if restart { " and starts it again" } else { "" }));
        } else {
            head.push(format!(
                "Observed: {live} live turns, {} waiting requests, {} delegated agents, {} workflow runs in force.",
                count(&view["observedOutstandingRequests"]),
                count(&view["observedActiveChildren"]) + count(&view["knownChildActivityUnknown"]),
                count(runs)
            ));
            tail.push(format!(
                "{act} interrupts each live turn, waits up to {} s for Codex to report it ended, then stops this Codex process{}.",
                cell(&view["stopWaitLimitSeconds"]),
                if restart { " and starts it again" } else { "" }
            ));
            tail.push("Waiting requests are not answered; they end with the process. Workflow runs stay open: stopping Codex ends no run.".into());
        }
        if restart {
            tail.push("No conversation is continued automatically; continue one yourself.".into());
        }
        tail.push("None observed is not none: coverage is not complete.".into());
        tail.push("This is your operational choice, not a recorded act. No stop record survives a relaunch.".into());
        tail.push(format!("Observed at {}.", text_or(&view["observedAt"], "not reported")));
        tail.push(format!("{act} proceeds; {KEEP_CODEX} (the default) and Cancel change nothing."));
        let whole = [head.clone(), listed, tail.clone()].concat().join("\n");
        whole_or_in_app("Stop Codex question", "live work at Stop Codex", whole, view, |digest| {
            [head, vec![format!("Each item is listed in the assessment, {IN_APP}"), digest.to_owned()], tail]
                .concat()
                .join("\n")
        })
    }
    /// Native cancellation of a pending sign-in: the safe observation as lines.
    /// The observation is a fixed set of short fields, so it is shown whole or
    /// refused with its cause (reported as a refusal, V14 F4).
    pub(crate) fn oauth_cancel_statement(safe: &Value) -> Result<NativeStatement, String> {
        bounded(
            "Sign-in cancellation confirmation",
            format!(
                "Cancel this original Codex sign-in?\n\n{}\n\nOK sends one cancellation request; Cancel keeps the pending sign-in.",
                readable(safe)
            ),
        )
        .map(|text| NativeStatement { text, in_app: None })
    }
    fn source_lines(label: &str, s: &Value, out: &mut Vec<String>) {
        out.push(format!("{label}: {}", text_or(&s["displayName"], "name not reported")));
        out.push(format!(
            "  Path: {}",
            native_path_text(&s["nativePath"])
                .unwrap_or_else(|| text_or(&s["displayPath"], "not reported").to_owned())
        ));
        let identity = &s["identityAtSelection"];
        out.push(format!(
            "  Content ({}), in full:",
            text_or(&identity["method"], "method not reported")
        ));
        out.push(format!("  {}", text_or(&identity["value"], "not reported")));
    }
    /// Native confirmation of a refreshed attachment source: both selections
    /// with readable paths and full content identities.
    pub(crate) fn attachment_source_statement(comparison: &Value) -> Result<NativeStatement, String> {
        let (old, new) = (&comparison["oldSelection"], &comparison["tentativeSelection"]);
        let changed = format!(
            "Content: {}",
            if old["identityAtSelection"] == new["identityAtSelection"] {
                "unchanged"
            } else {
                "changed"
            }
        );
        let standing = format!("Standing: {}", text_or(&comparison["standing"], "not reported"));
        let footer = "This changes only the selected source. Nothing is sent or registered.";
        let mut t = vec!["Confirm current attachment source".to_owned(), String::new()];
        source_lines("Original selection", old, &mut t);
        source_lines("Current source", new, &mut t);
        t.extend([changed.clone(), standing.clone(), String::new(), footer.into()]);
        whole_or_in_app("Attachment source confirmation", "attachment source comparison", t.join("\n"), comparison, |digest| {
            [
                "Confirm current attachment source".to_owned(),
                format!("Original selection: {}", text_or(&old["displayName"], "name not reported")),
                format!("Current source: {}", text_or(&new["displayName"], "name not reported")),
                changed,
                standing,
                format!("Both selections, with full paths and content identities, are {IN_APP}"),
                digest.to_owned(),
                footer.into(),
            ]
            .join("\n")
        })
    }
    /// Labels of the request-answer confirmation (owner's three-button layout).
    pub(crate) const SEND_ANSWER: &str = "Send answer";
    pub(crate) const DONT_SEND: &str = "Don't send";
    /// Native confirmation of a request answer: the masked preview as lines,
    /// or, when it does not fit, named by digest and shown whole in the App.
    pub(crate) fn request_answer_statement(preview: &Value) -> Result<NativeStatement, String> {
        let footer = "Send answer sends it once; Don't send (the default) and Cancel send nothing.";
        whole_or_in_app(
            "Request answer confirmation",
            "request answer",
            format!("Send this native request answer?\n\n{}\n\n{footer}", readable(preview)),
            preview,
            |digest| {
                format!(
                    "Send this native request answer?\n\nRequest: {} #{}\nThe complete answer, as it will be sent (secret values masked), is {IN_APP}\n{digest}\n\n{footer}",
                    cell(&preview["method"]),
                    cell(&preview["requestIdentity"])
                )
            },
        )
    }

    /// The default-safe layout the owner chose for act confirmations
    /// (OWNER_DECISIONS "Native confirmation default key — 2026-10-08"):
    /// slot 1 "Don't ‹act›" is the default (Return); slot 2 is the act; slot 3
    /// is "Cancel", which tauri-plugin-dialog 2.7.2 also reports for any
    /// unmatched, failed or aborted dialog. Only slot 2 acts (see `chose`).
    /// Used for A15, A16 and request answers; not for file acts, whose three
    /// slots are act, decline and cancel.
    pub(crate) fn act_buttons(dont: &str, act: &str) -> MessageDialogButtons {
        MessageDialogButtons::YesNoCancelCustom(dont.into(), act.into(), CANCEL.into())
    }
    pub(crate) const CANCEL: &str = "Cancel";
    /// Labels of the A16 confirmation.
    pub(crate) const DECIDE: &str = "Decide";
    pub(crate) const DONT_DECIDE: &str = "Don't decide";

    /// Content the App shows in full while an open native confirmation names
    /// it by digest. A reading aid: the binding is checked host-side.
    pub(crate) struct InApp {
        pub(crate) kind: &'static str,
        pub(crate) digest: String,
        pub(crate) content: Value,
    }
    /// What a native confirmation shows, and what the App shows beside it.
    pub(crate) struct NativeStatement {
        pub(crate) text: String,
        pub(crate) in_app: Option<InApp>,
    }
    const IN_APP: &str = "shown in full in the App now, under \"Content named by an open native confirmation\". Its sha-256 digest:";

    fn non_integer_at(v: &Value, at: &str) -> Option<String> {
        match v {
            Value::Number(n) if n.as_i64().is_none() && n.as_u64().is_none() => {
                Some(if at.is_empty() { "/".into() } else { at.into() })
            }
            Value::Array(items) => items
                .iter()
                .enumerate()
                .find_map(|(i, x)| non_integer_at(x, &format!("{at}/{i}"))),
            Value::Object(members) => members.iter().find_map(|(k, x)| {
                non_integer_at(x, &format!("{at}/{}", k.replace('~', "~0").replace('/', "~1")))
            }),
            _ => None,
        }
    }
    /// sha-256 (lowercase hex) of `v` in the `aac-offer-digest/0.1` canonical
    /// form (canonical.rs). AAC §5.1 defines that form over integers only, so a
    /// non-integer number is refused with its JSON Pointer location.
    pub(crate) fn content_digest(what: &str, v: &Value) -> Result<String, String> {
        if let Some(at) = non_integer_at(v, "") {
            return Err(format!(
                "{what} holds a non-integer number at {at}; the aac-offer-digest/0.1 canonical form (AAC §5.1) defines integers only, so it cannot be named by digest; nothing presented, captured or sent"
            ));
        }
        let mut canonical = String::new();
        crate::canonical::canonical(v, &mut canonical).map_err(|e| format!("{what}: {e}"))?;
        Ok(crate::util::sha256_hex(canonical.as_bytes()))
    }
    /// `whole` when it fits; otherwise the App shows `content` in full while the
    /// alert is open, and the alert shows `summary` naming its digest. Refused
    /// with its cause only when even the summary does not fit.
    pub(crate) fn whole_or_in_app(
        what: &str,
        kind: &'static str,
        whole: String,
        content: &Value,
        summary: impl FnOnce(&str) -> String,
    ) -> Result<NativeStatement, String> {
        if let Ok(text) = bounded(what, whole) {
            return Ok(NativeStatement { text, in_app: None });
        }
        let digest = content_digest(what, content)?;
        let text = bounded(what, summary(&digest))?;
        Ok(NativeStatement {
            text,
            in_app: Some(InApp {
                kind,
                digest,
                content: content.clone(),
            }),
        })
    }

    static SHOWN: std::sync::Mutex<Vec<(u64, Value)>> = std::sync::Mutex::new(Vec::new());
    static NEXT: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(1);
    struct Shown(u64);
    impl Drop for Shown {
        fn drop(&mut self) {
            if let Ok(mut shown) = SHOWN.lock() {
                shown.retain(|(id, _)| *id != self.0);
            }
        }
    }
    /// Publishes `in_app` for the App to show while `present` runs (the native
    /// alert is open), and withdraws it afterwards, also on unwind.
    pub(crate) fn showing_in_app<T>(in_app: Option<&InApp>, present: impl FnOnce() -> T) -> T {
        let _shown = in_app.map(|c| {
            let id = NEXT.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
            let entry = serde_json::json!({"kind":c.kind,"digest":c.digest,"digestMethod":"sha-256 of the aac-offer-digest/0.1 canonical form","content":c.content,
                "standing":"reading aid while a native confirmation is open; the host checks the binding at capture"});
            SHOWN.lock().unwrap_or_else(|e| e.into_inner()).push((id, entry));
            Shown(id)
        });
        present()
    }
    /// What the App shows now (read-only; empty when no confirmation names content).
    pub(crate) fn shown_in_app() -> Value {
        Value::Array(
            SHOWN
                .lock()
                .unwrap_or_else(|e| e.into_inner())
                .iter()
                .map(|(_, v)| v.clone())
                .collect(),
        )
    }
    /// F4: a host refusal is reported as a refusal with its cause, never as the
    /// person's cancel. `refused` is set when the statement was not presented.
    pub(crate) fn refusal_or(
        refused: Option<String>,
        result: Result<Value, String>,
    ) -> Result<Value, String> {
        match refused {
            Some(cause) => Err(cause),
            None => result,
        }
    }

    /// How tauri-plugin-dialog 2.7.2 (desktop.rs `show_message_dialog`) with
    /// rfd 0.16 reports each way an alert can end: the default (Return) is
    /// slot 1; an unmatched, failed or aborted alert (rfd `Cancel`) is
    /// reported as the cancel-slot label. Test model of the dependency only.
    #[cfg(test)]
    pub(crate) mod dialog_model {
        use tauri_plugin_dialog::{MessageDialogButtons as B, MessageDialogResult as R};
        pub(crate) fn outcomes(b: &B) -> Vec<(&'static str, R)> {
            match b {
                B::YesNoCancelCustom(y, n, c) => vec![
                    ("default (Return)", R::Custom(y.clone())),
                    ("middle", R::Custom(n.clone())),
                    ("third", R::Custom(c.clone())),
                    ("abort or failure", R::Custom(c.clone())),
                ],
                B::OkCancelCustom(o, c) => vec![
                    ("default (Return)", R::Custom(o.clone())),
                    ("second", R::Custom(c.clone())),
                    ("abort or failure", R::Custom(c.clone())),
                ],
                _ => panic!("layout not modelled"),
            }
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use serde_json::json;
        fn generation() -> Value {
            json!({"appSession":"app-session:0123456789abcdef","home":"home-a","spawnCounter":3})
        }
        fn assessment(turns: usize, requests: usize, children: usize) -> Value {
            let g = generation();
            json!({"modeHomeClass":"account","generation":g,"observedAt":"2026-10-08T00:00:00Z",
                "account":{"state":"signed in","nativeType":"chatgpt","readAvailability":"typed native account read observed","currentReport":{"state":"native type reported; identity not established"}},
                "observedLiveTurns":(0..turns).map(|i| json!({"generation":g,"threadId":format!("thread-{i}"),"turnId":format!("turn-{i}"),"status":"inProgress","source":"s"})).collect::<Vec<_>>(),
                "observedOutstandingRequests":(0..requests).map(|i| json!({"generation":g,"requestIdentity":i,"method":"item/tool/requestUserInput","state":"outstanding","threadId":"thread-r","turnId":"t"})).collect::<Vec<_>>(),
                "observedActiveChildren":(0..children).map(|i| json!({"generation":g,"threadId":format!("child-{i}"),"parentThreadId":"thread-0","reportedStatus":"running"})).collect::<Vec<_>>(),
                "knownChildActivityUnknown":[{"generation":g,"threadId":"child-u","parentThreadId":"thread-0","reportedStatus":null}],
                "coverage":{"turns":{"unresolved":[{"threadId":"thread-x","limit":"l"}]}},"warning":"None observed is not none."})
        }
        /// V14 F1: each live turn, request and child is listed (DEL-01-05
        /// AE-12, KE-13, Q-5); counts are never the whole statement.
        #[test]
        fn logout_lists_every_item_or_names_the_whole_assessment_by_digest() {
            let view = assessment(2, 1, 1);
            let s = logout_statement(&view).unwrap();
            assert!(s.in_app.is_none());
            for needle in ["Live turn: thread-0 / turn-0 (inProgress)", "Live turn: thread-1 / turn-1", "Outstanding request: item/tool/requestUserInput #0 in thread-r",
                "Active child: child-0 (parent thread-0; running)", "Child, activity unknown: child-u (parent thread-0)", "Turn observation unresolved: thread-x / turn not reported",
                "Observed: 2 live turns, 1 outstanding requests, 1 active children", "None observed is not none.", "Cancel sends nothing", "0123456789abcdef"] {
                assert!(s.text.contains(needle), "{needle} in\n{}", s.text);
            }
            assert!(!s.text.contains('{'), "{}", s.text);
            // Too many to list: the App shows the frozen assessment whole while
            // the alert is open; the alert gives the counts and names it by digest.
            let view = assessment(60, 30, 30);
            let s = logout_statement(&view).unwrap();
            let shown = s.in_app.as_ref().expect("named by digest, shown in the App");
            assert_eq!(shown.content, view);
            assert_eq!(shown.digest, content_digest("x", &view).unwrap());
            assert!(s.text.lines().any(|l| l == shown.digest), "{}", s.text);
            assert!(s.text.contains("Observed: 60 live turns, 30 outstanding requests, 30 active children"));
            assert!(s.text.contains("Each of these is listed in the frozen assessment, shown in full in the App now"), "{}", s.text);
            assert!(bounded("x", s.text.clone()).is_ok());
        }
        #[test]
        fn operational_dialogs_are_readable_and_route_overflow_to_the_app() {
            let path = |p: &str| json!({"encoding":"unix_bytes","bytes":p.as_bytes()});
            let old = json!({"displayName":"notes.txt","nativePath":path("/work/notes.txt"),"displayPath":"/work/notes.txt","identityAtSelection":{"method":"sha256","value":"a".repeat(64)}});
            let mut new = old.clone();
            new["identityAtSelection"]["value"] = json!("b".repeat(64));
            let s = attachment_source_statement(&json!({"oldSelection":old,"tentativeSelection":new,"standing":"explicit refresh"})).unwrap();
            assert!(s.in_app.is_none());
            assert!(s.text.contains("  Path: /work/notes.txt") && s.text.contains(&"b".repeat(64)) && s.text.contains("Content: changed"), "{}", s.text);
            assert!(!s.text.contains("bytes") && !s.text.contains("47,"), "{}", s.text);
            let deep = format!("/{}", "deep/".repeat(150));
            let mut far = old.clone();
            far["nativePath"] = path(&deep);
            let comparison = json!({"oldSelection":far,"tentativeSelection":far,"standing":"explicit refresh"});
            let s = attachment_source_statement(&comparison).unwrap();
            let shown = s.in_app.as_ref().expect("deep paths: shown in the App");
            assert_eq!(shown.content, comparison);
            assert!(s.text.contains("Content: unchanged") && s.text.lines().any(|l| l == shown.digest), "{}", s.text);
            let safe = json!({"generation":generation(),"requestIdentity":7,"phase":"Pending","cancelAvailable":true,"standing":"source observation"});
            let text = oauth_cancel_statement(&safe).unwrap().text;
            assert!(text.contains("cancelAvailable: true") && text.contains("spawnCounter: 3") && !text.contains('{'), "{text}");
            let preview = json!({"method":"item/tool/requestUserInput","generation":generation(),"requestIdentity":9,"answer":{"answers":{"q1":{"answers":["yes"]}}},"actorRef":"R"});
            let s = request_answer_statement(&preview).unwrap();
            assert!(s.in_app.is_none());
            assert!(s.text.contains("q1:") && s.text.contains("answers: yes") && s.text.contains("Don't send (the default) and Cancel send nothing"), "{}", s.text);
            // A long free-text answer is no longer impossible to send (V14 F5).
            let long = json!({"method":"item/tool/requestUserInput","requestIdentity":9,"answer":{"text":"x".repeat(MAX_CHARS * 3)}});
            let s = request_answer_statement(&long).unwrap();
            let shown = s.in_app.as_ref().unwrap();
            assert_eq!(shown.content, long);
            assert!(s.text.contains("Request: item/tool/requestUserInput #9") && s.text.lines().any(|l| l == shown.digest), "{}", s.text);
        }
        #[test]
        fn content_digest_refuses_non_integers_with_location_and_keeps_big_integers_exact() {
            let err = content_digest("The answer", &json!({"a":[{"b~/c":2.5}]})).unwrap_err();
            assert!(err.contains("non-integer number at /a/0/b~0~1c") && err.contains("integers only"), "{err}");
            assert!(content_digest("x", &json!(1.0)).unwrap_err().contains("at /"));
            assert!(content_digest("x", &json!({"n":u64::MAX,"m":i64::MIN})).is_ok());
            // whole_or_in_app: a non-integer in content that must go to the App
            // is a refusal with that cause, not a silent fallback.
            let long = json!({"text":"x".repeat(MAX_CHARS * 2),"f":0.5});
            let err = whole_or_in_app("W", "k", "x".repeat(MAX_CHARS * 2), &long, |d| d.to_owned()).err().unwrap();
            assert!(err.contains("non-integer number at /f"), "{err}");
            // Summary still too long: refused with the bound's cause.
            let err = whole_or_in_app("W", "k", "x".repeat(MAX_CHARS * 2), &json!(1), |_| "y".repeat(MAX_CHARS * 2)).err().unwrap();
            assert!(err.contains("exceeds the readable native confirmation"), "{err}");
        }
        /// The owner's layout: [Don't ‹act› (default)] [‹Act›] [Cancel]. The
        /// default (Return), the third button and any abort never act.
        #[test]
        fn act_buttons_only_the_middle_slot_acts() {
            for (dont, act) in [(DONT_DECIDE, DECIDE), (DONT_SEND, SEND_ANSWER), ("Don't register", "Register")] {
                let ends = dialog_model::outcomes(&act_buttons(dont, act));
                assert_eq!(ends.len(), 4);
                for (how, result) in ends {
                    assert_eq!(chose(&result, act), how == "middle", "{act}: {how} {result:?}");
                }
                assert!(matches!(act_buttons(dont, act), MessageDialogButtons::YesNoCancelCustom(d, a, c) if d == dont && a == act && c == CANCEL));
            }
        }
        /// V14 F4: a host refusal is reported as a refusal with its cause.
        #[test]
        fn refusal_is_reported_as_refusal_not_as_the_persons_cancel() {
            let cancelled = Ok(json!({"state":"native confirmation cancelled; no logout request"}));
            assert_eq!(refusal_or(Some("Logout confirmation: too long".into()), cancelled.clone()).unwrap_err(), "Logout confirmation: too long");
            assert_eq!(refusal_or(None, cancelled.clone()).unwrap(), cancelled.unwrap());
        }
        #[test]
        fn shown_in_app_only_while_the_alert_is_open() {
            let c = InApp { kind: "test content", digest: "f".repeat(64) + "-shown-test", content: json!({"a":1}) };
            let during = showing_in_app(Some(&c), shown_in_app);
            assert!(during.as_array().unwrap().iter().any(|e| e["digest"] == c.digest.as_str() && e["content"] == c.content && e["standing"].as_str().unwrap().contains("reading aid")));
            assert!(!shown_in_app().as_array().unwrap().iter().any(|e| e["digest"] == c.digest.as_str()));
            let _ = std::panic::catch_unwind(|| showing_in_app(Some(&c), || panic!("alert failed")));
            assert!(!shown_in_app().as_array().unwrap().iter().any(|e| e["digest"] == c.digest.as_str()), "withdrawn on unwind");
        }
        #[test]
        fn bound_refuses_with_cause_and_never_truncates() {
            let ok = "a\n".repeat(MAX_LINES);
            assert_eq!(bounded("X", ok.clone()).unwrap(), ok);
            let long_lines = "a\n".repeat(MAX_LINES + 1);
            let err = bounded("X", long_lines).unwrap_err();
            assert!(err.contains("nothing presented") && err.contains(&format!("{}", MAX_LINES + 1)));
            assert!(bounded("X", "é".repeat(MAX_CHARS)).is_ok(), "characters, not bytes");
            assert!(bounded("X", "a".repeat(MAX_CHARS + 1)).is_err());
        }
        #[test]
        fn native_paths_are_readable_with_explicit_non_utf8_marker() {
            let utf8 = json!({"encoding":"unix_bytes","bytes":"/tmp/Prüfung lib".as_bytes()});
            assert_eq!(native_path_text(&utf8).unwrap(), "/tmp/Prüfung lib");
            let bad = json!({"encoding":"unix_bytes","bytes":[47,97,0xff,98,0xc3]});
            let text = native_path_text(&bad).unwrap();
            assert!(text.starts_with("[path is not valid UTF-8"), "{text}");
            assert!(text.ends_with("/a\\xffb\\xc3"), "{text}");
            let wide = json!({"encoding":"windows_utf16","codeUnits":[67,58,0xD800]});
            let wide = native_path_text(&wide).unwrap();
            assert!(wide.starts_with("[path is not valid UTF-16") && wide.ends_with("C:\\u{d800}"), "{wide}");
            assert!(native_path_text(&json!({"bytes":12,"path":"x"})).is_none(), "manifest sizes are not paths");
            assert!(native_path_text(&json!({"encoding":"unix_bytes","bytes":[300]})).is_none());
        }
        #[test]
        fn readable_shows_every_member_without_json_or_byte_arrays() {
            let v = json!({"old":{"nativePath":{"encoding":"unix_bytes","bytes":"/a/b.txt".as_bytes()},"identity":{"method":"sha256","value":"ab"}},"list":[1,2],"rows":[{"x":null}],"empty":[]});
            let text = readable(&v);
            assert!(!text.contains('{') && !text.contains("47,"), "{text}");
            for needle in ["old:", "  nativePath: /a/b.txt", "    method: sha256", "list: 1, 2", "rows:", "    x: null", "empty: none"] {
                assert!(text.contains(needle), "{needle} in\n{text}");
            }
        }
        #[test]
        fn actor_line_and_choice() {
            let line = actor_line(&json!({"displayName":"R","osAccount":"r","codexAccount":"c@x","identityVerified":false}));
            assert_eq!(line, "R · OS account r · Codex account c@x (identity not verified)");
            assert!(actor_line(&json!({"osAccount":"r"})).starts_with("no name set in the App · OS account r"));
            assert!(chose(&MessageDialogResult::Custom("Register".into()), "Register"));
            for other in [MessageDialogResult::Custom("Cancel".into()), MessageDialogResult::Ok, MessageDialogResult::Yes, MessageDialogResult::Cancel] {
                assert!(!chose(&other, "Register"));
            }
            assert_eq!(short("0123456789abcdef"), "0123456789ab");
            assert_eq!(short("abc"), "abc");
        }
    }
}

impl ActControl {
    pub fn new(workspace: &Path) -> Self {
        ActControl {
            workspace: workspace.to_path_buf(),
            offers: HashMap::new(),
            native_captures: HashMap::new(),
            a15_offers: HashMap::new(),
            file_offers: HashMap::new(),
            file_capture_roots: HashMap::new(),
        }
    }

    /// AX-01 / AX-02. Compose an A16 offer for the `act_request` `request_ref`.
    pub fn compose_a16(&mut self, request_ref: &str) -> Result<Value, String> {
        refuse_unresolved_capture(&self.workspace, request_ref)?;
        let (entries, limits) = storage::read_all(&self.workspace);
        if !limits.is_empty() {
            return Err(format!("not offered: incomplete record set: {limits:?}"));
        }
        let req = entries
            .iter()
            .find(|e| e["recordId"] == json!(request_ref) && e["kind"] == "act_request")
            .ok_or_else(|| format!("not offered: no act_request {request_ref} in the record"))?;
        let b = &req["body"];
        if b["form"] != "decision package file" || b["actKind"] != "A16" {
            return Err(
                "not offered: the control serves A16 only on a decision package (AAC §1.2)".into(),
            );
        }
        let rel = b["evidence"]["ref"]
            .as_str()
            .ok_or("not offered: the request names no package file")?;
        if Path::new(rel).is_absolute()
            || Path::new(rel)
                .components()
                .any(|c| !matches!(c, std::path::Component::Normal(_)))
        {
            return Err("not offered: unsafe package reference".into());
        }
        let path = self.workspace.join(rel);
        storage::check_path(&path)?;
        // AI-1 / AI-9: the subject's identity at compose.
        let bytes =
            std::fs::read(&path).map_err(|e| format!("not offered: package unavailable: {e}"))?;
        let (pkg, now) = package_snapshot(&bytes)?;
        if b["evidence"]["claimedIdentity"].as_str() != Some(now.as_str()) {
            return Err(
                "not offered: the package file changed since the request was recorded (AI-9)"
                    .into(),
            );
        }
        let alts = pkg["alternatives"].as_array().cloned().unwrap_or_default();
        if alts.len() < 2 {
            return Err("not offered: the package names fewer than two alternatives (AI-9)".into());
        }
        let scope = pkg
            .get("scope")
            .and_then(|s| s.as_str())
            .filter(|s| !s.is_empty())
            .unwrap_or("not named by the package");
        let mut ids = std::collections::HashSet::new();
        if alts
            .iter()
            .any(|a| !ids.insert(a["id"].as_str().unwrap_or("")))
        {
            return Err("not offered: duplicate alternative identities".into());
        }
        let offer_id = crate::util::opaque_id("offer:")?;
        let mut offer = json!({
            "format": "chirality.aac.offer", "formatVersion": "0.3", "offerId": offer_id,
            "actKind": "A16", "wording": "decide",
            "subject": {"class": "App file", "ref": rel,
                        "contentIdentity": {"method": FILE_IDENTITY_METHOD, "value": now}},
            "scope": scope, "purpose": pkg["purpose"], "actorRequirement": "the person",
            "declineAvailable": false, "answers": {"standing": STANDING},
            "requestRef": request_ref, "composedAt": now_rfc3339(),
            "alternatives": alts.iter().map(|a| json!({
                "id": a["id"], "statement": a["statement"], "consequences": a["consequences"]})).collect::<Vec<_>>(),
        });
        let digest = offer_digest(&offer)?;
        offer["offerDigest"] = json!({"method": OFFER_DIGEST_METHOD, "value": digest});
        self.offers.insert(
            offer_id.clone(),
            OfferSlot {
                offer: offer.clone(),
                state: OfferState::Composed,
                package_path: path,
                selected: None,
                frozen_offer: None,
                frozen_actor: None,
                request_record: req.clone(),
            },
        );
        Ok(offer)
    }

    /// AX-03: the host shows the offer in its native confirmation.
    pub fn present(&mut self, offer_id: &str) -> Result<(), String> {
        let s = self.offers.get_mut(offer_id).ok_or("no such offer")?;
        if s.state != OfferState::Composed {
            return Err(format!("cannot present an offer in state {:?}", s.state));
        }
        s.state = OfferState::Presented;
        Ok(())
    }

    /// AX-05.
    pub fn dismiss(&mut self, offer_id: &str) {
        if let Some(s) = self.offers.get_mut(offer_id) {
            if s.state == OfferState::Presented {
                s.state = OfferState::Dismissed;
            }
        }
    }

    /// The text the native confirmation shows, composed by the host from the offer (§6.2 P-2).
    pub fn confirmation_text(
        &mut self,
        offer_id: &str,
        alternative: &str,
        actor: &Value,
    ) -> Result<String, String> {
        self.confirmation_statement(offer_id, alternative, actor)
            .map(|s| s.text)
    }
    /// The native statement, and the App-shown content when the chosen
    /// alternative's statement and consequences do not fit the alert whole
    /// (then the alert names them by digest; the capture still binds the frozen
    /// offer and its digest, unchanged).
    pub(crate) fn confirmation_statement(
        &mut self,
        offer_id: &str,
        alternative: &str,
        actor: &Value,
    ) -> Result<native_statement::NativeStatement, String> {
        let workspace = self.workspace.clone();
        let s = self.offers.get_mut(offer_id).ok_or("no such offer")?;
        if let Err(error) = check_request_binding(&workspace, &s.request_record, &s.offer["requestRef"]) {
            s.state = OfferState::Stale;
            return Err(error);
        }
        if s.selected
            .as_deref()
            .is_some_and(|chosen| chosen != alternative)
        {
            return Err("native confirmation already frozen for another alternative".into());
        }
        let o = &s.offer;
        if s.frozen_offer.as_ref().is_some_and(|f| f != o)
            || s.frozen_actor.as_ref().is_some_and(|a| a != actor)
        {
            return Err("native confirmation facts already frozen".into());
        }
        if offer_digest(o)? != o["offerDigest"]["value"].as_str().unwrap_or("") {
            return Err("offer digest mismatch".into());
        }
        crate::schema_validation::validate_offer(o)?;
        let alt = o["alternatives"]
            .as_array()
            .unwrap()
            .iter()
            .find(|a| a["id"] == json!(alternative))
            .ok_or("the package names no such alternative")?;
        let who = [actor.get("displayName"), actor.get("osAccount")]
            .iter()
            .filter_map(|v| v.and_then(|x| x.as_str()))
            .collect::<Vec<_>>()
            .join(" / ");
        let consequences = alt["consequences"].as_array().unwrap();
        let cons = consequences
            .iter()
            .filter_map(|c| c.as_str())
            .map(|c| format!("  - {c}"))
            .collect::<Vec<_>>()
            .join("\n");
        let head = format!(
            "Decide (A16)\n\nPackage: {}\nContent identity: {}\nPurpose: {}\nScope: {}\n",
            o["subject"]["ref"].as_str().unwrap_or(""),
            o["subject"]["contentIdentity"]["value"].as_str().unwrap_or(""),
            o["purpose"].as_str().unwrap_or(""),
            o["scope"].as_str().unwrap_or("")
        );
        let tail = format!(
            "\nActor: {who} (identity not verified)\nAnswers: {STANDING}\nOnly Decide records this decision. Don't decide (the default) records nothing; no decline exists for A16; Cancel closes the control."
        );
        let whole = format!(
            "{head}\nChosen alternative: {alternative} — {}\nConsequences:\n{cons}\n{tail}",
            alt["statement"].as_str().unwrap_or("")
        );
        // AAC §4.1a: all selected text without silent truncation. When the alert
        // cannot hold it, the App shows the chosen alternative whole (CI-22);
        // nothing is frozen for a refused statement.
        let content = json!({"package":o["subject"]["ref"],"contentIdentity":o["subject"]["contentIdentity"],
            "offerId":o["offerId"],"offerDigest":o["offerDigest"],"chosenAlternative":alt});
        let statement = native_statement::whole_or_in_app(
            "A16 native confirmation",
            "A16 chosen alternative",
            whole,
            &content,
            |digest| {
                format!(
                    "{head}\nChosen alternative: {alternative}. Its statement and all {} consequences are shown in full in the App now, under \"Content named by an open native confirmation\". Their sha-256 digest:\n{digest}\n{tail}",
                    consequences.len()
                )
            },
        )?;
        s.selected = Some(alternative.into());
        s.frozen_offer = Some(o.clone());
        s.frozen_actor = Some(actor.clone());
        Ok(statement)
    }

    /// AX-04, AX-06, AX-08, then AX-12/AX-13. Returns {state, capture, record?}.
    pub fn confirm(
        &mut self,
        offer_id: &str,
        alternative: &str,
        source: InputSource,
        actor: Value,
    ) -> Result<Value, String> {
        if source != InputSource::HostNativeConfirmation {
            // AX-04 (CAP-4): unchanged; nothing captured.
            return Err(format!("not operable from {}", source.label()));
        }
        let ws = self.workspace.clone();
        let slot = self.offers.get_mut(offer_id).ok_or("no such offer")?;
        match slot.state {
            OfferState::Presented => {}
            OfferState::Composed => {
                return Err("refused: capture from an offer not presented".into())
            }
            ref s => {
                return Err(format!(
                    "refused: the offer is {s:?}; a second capture is refused"
                ))
            }
        }
        let o = slot.offer.clone();
        if slot.selected.as_deref() != Some(alternative)
            || slot.frozen_offer.as_ref() != Some(&o)
            || slot.frozen_actor.as_ref() != Some(&actor)
        {
            return Err(
                "refused: choice or content differs from the frozen native confirmation".into(),
            );
        }
        if !o["alternatives"]
            .as_array()
            .unwrap()
            .iter()
            .any(|a| a["id"] == json!(alternative))
        {
            return Err("refused: the package names no such alternative; nothing captured".into());
        }
        // NA-4: the confirmation is for the presented offer (identity and digest).
        if offer_digest(&o)? != o["offerDigest"]["value"].as_str().unwrap_or("") {
            return Err("refused: offer digest does not match the presented offer".into());
        }
        // AK-c: re-read the subject's identity (§4.1 step 5).
        let now = file_identity(&slot.package_path);
        if now.as_deref() != o["subject"]["contentIdentity"]["value"].as_str() {
            slot.state = OfferState::Stale; // AX-06
            return Err(
                "content changed since it was shown: review it again (AC-6); nothing captured"
                    .into(),
            );
        }
        // Request identity/facts may have changed while the native confirmation
        // was shown. Refuse before capture; prior ACT-history ambiguity is not
        // an authorization rule, and existing complete-record guards are retained.
        if let Err(error) = check_request_binding(&ws, &slot.request_record, &o["requestRef"]) {
            slot.state = OfferState::Stale;
            return Err(error);
        }
        // §4.1 step 6: capture evidence (§5.2), before any record (AK-e).
        let request_ref = o["requestRef"].as_str().unwrap().to_string();
        let capture_id = crate::util::opaque_id("cap:")?;
        let bound = o["subject"]["contentIdentity"].clone();
        let capture = json!({
            "format": "chirality.aac.capture-evidence", "formatVersion": "0.3",
            "captureId": capture_id, "offerId": offer_id, "offerDigest": o["offerDigest"],
            "choice": "act", "actKind": "A16", "actor": actor,
            "boundSubject": [format!("decision package {request_ref}")],
            "boundContent": [bound],
            "scope": o["scope"], "purpose": o["purpose"], "capturedAt": capture_time(),
            "surface": "App interface", "inputSource": "host-native-confirmation",
            "answers": o["answers"], "requestRef": request_ref, "alternativeChosen": alternative,
            "evidenceLimits": ["identity not verified"],
        });
        crate::schema_validation::validate_capture(&capture)?;
        let cap_file = storage::capture_path(&ws, &capture_id);
        let _ownership = storage::lock(&ws.join(CAPTURE_STORE).join(".capture.lock"))?;
        let mut native = NativeCapture {
            ordinal: self.native_captures.len(),
            target_log: LOG.into(),
            a15: None,
            written: false,
            delay_pending: false,
            capture: capture.clone(),
            pending: None,
            failure: None,
        };
        let publication = storage::create_json(&cap_file, &capture);
        // This proof comes from this process's native event, never imported JSON.
        if let Err(e) = publication {
            native.failure = Some(e.clone());
            self.native_captures.insert(capture_id.clone(), native);
            self.offers.get_mut(offer_id).unwrap().state = OfferState::RecordPending;
            return Ok(
                json!({"state":"AC-8 record pending","captureDurability":"not established","writeFailure":e,"captureId":capture_id}),
            );
        }
        self.offers.get_mut(offer_id).unwrap().state = OfferState::Captured;
        match records::prepare_capture_submission(&ws, &capture, LOG) {
            Ok(pending) => {
                native.pending = Some(pending);
                if let Err(e) =
                    records::persist_capture_submission(&ws, native.pending.as_ref().unwrap())
                {
                    pending_failure(&ws, &mut native, &e);
                }
            }
            Err(e) => native.failure = Some(e),
        }
        // The next writer admission first drains earlier trusted submissions and their delay account.
        self.flush_native_locked();
        let out = if self.writer_ready() {
            recover_capture(&ws, &capture, Some(&mut native), None, true)
        } else {
            let error="older trusted native submission remains pending; new captured facts retained in writer admission order";
            pending_failure(&ws, &mut native, error);
            Ok(json!({"state":"AC-8 record pending","capture":capture,"writeFailure":error}))
        };
        if let Ok(result) = &out {
            native.written = result["state"] == "AC-7 recorded";
            native.delay_pending = result["delayEvidencePending"] == true;
        }
        self.native_captures.insert(capture_id, native);
        self.offers.get_mut(offer_id).unwrap().state =
            if out.as_ref().is_ok_and(|v| v["state"] == "AC-7 recorded") {
                OfferState::Recorded
            } else {
                OfferState::RecordPending
            };
        out
    }

    fn writer_ready(&self) -> bool {
        self.native_captures
            .values()
            .all(|n| n.written && !n.delay_pending)
    }

    /// Explicit App startup/command writer continuation uses this boundary; reader calls do not.
    pub fn refresh_recording(
        &mut self,
    ) -> (Result<Vec<Value>, String>, Result<Vec<Value>, String>) {
        let recovery = self.recover_pending();
        let requests = if self.writer_ready() {
            crate::recorder::identify_packages(&self.workspace)
        } else {
            Err(
                "older trusted native submission remains pending; recorder continuation held"
                    .into(),
            )
        };
        (recovery, requests)
    }

    /// Caller holds capture ownership; untrusted files never enter this native admission queue.
    fn flush_native_locked(&mut self) -> Vec<Value> {
        let mut ids = self
            .native_captures
            .iter()
            .map(|(id, n)| (n.ordinal, id.clone()))
            .collect::<Vec<_>>();
        ids.sort_by_key(|(ordinal, _)| *ordinal);
        let mut results = vec![];
        let mut earlier_held = false;
        for (_, id) in &ids {
            let native = self.native_captures.get_mut(id).unwrap();
            let original = native.capture.clone();
            let result = if self.file_capture_roots.get(id).is_some_and(|root| root != &self.workspace) {
                json!({"state":"AC-8 record pending","capture":original,"writeFailure":"File act original workspace changed; no write or relocation"})
            } else if native.a15.as_ref().is_some_and(|a|!a.belongs_to(&self.workspace)) {
                json!({"state":"AC-8 record pending","capture":original,"writeFailure":"A15 original library custody changed; no write or relocation"})
            } else if earlier_held && !native.written {
                let error="older trusted native submission remains pending; captured facts retained in writer admission order";
                pending_failure(&self.workspace, native, error);
                json!({"state":"AC-8 record pending","capture":original,"writeFailure":error})
            } else {
                match recover_capture(&self.workspace, &original, Some(native), None, false) {
                    Ok(result) => result,
                    Err(error) => {
                        pending_failure(&self.workspace, native, &error);
                        json!({"state":"AC-8 record pending","capture":original,"writeFailure":error})
                    }
                }
            };
            if result["state"] == "AC-7 recorded" {
                native.written = true;
                native.delay_pending = result["delayEvidencePending"] == true;
            }
            if !native.written || result["state"] != "AC-7 recorded" {
                earlier_held = true;
            }
            if let Some(offer) = native.capture["offerId"]
                .as_str()
                .and_then(|id| self.offers.get_mut(id))
            {
                offer.state = if result["state"] == "AC-7 recorded" {
                    OfferState::Recorded
                } else {
                    OfferState::RecordPending
                };
            }
            if let Some(slot) = original["offerId"].as_str().and_then(|id| self.file_offers.get_mut(id)) {
                slot.set_recording_state(result["state"] == "AC-7 recorded");
            }
            results.push(result);
        }
        // W-2 pending acts precede the delay accounts; continuation follows both.
        for ((_, id), result) in ids.iter().zip(results.iter_mut()) {
            let native = self.native_captures.get_mut(id).unwrap();
            if result["state"] == "AC-7 recorded" && result["delayEvidencePending"] == true {
                if let Some(pending) = &native.pending {
                    match records::finish_capture_delay(&self.workspace, pending) {
                        Ok(()) => {
                            result
                                .as_object_mut()
                                .unwrap()
                                .remove("delayEvidencePending");
                            native.delay_pending = false;
                        }
                        Err(e) => {
                            result["delayEvidenceFailure"] = json!(e);
                            native.delay_pending = true;
                        }
                    }
                }
            }
        }
        results
    }

    /// Relaunch/late-write reconciliation; never captures again or changes act facts.
    pub fn recover_pending(&mut self) -> Result<Vec<Value>, String> {
        let _ownership = storage::lock(&self.workspace.join(CAPTURE_STORE).join(".capture.lock"))?;
        let mut results = self.flush_native_locked();
        let mut candidates = HashMap::<String, (Value, Option<Value>)>::new();
        let dir = self.workspace.join(CAPTURE_STORE);
        for (directory, is_pending) in [(&dir, false), (&dir.join("pending"), true)] {
            let rd = match std::fs::read_dir(directory) {
                Ok(rd) => rd,
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => continue,
                Err(e) => {
                    results.push(cold_file_limit(directory, &e.to_string()));
                    continue;
                }
            };
            for entry in rd {
                let path = match entry {
                    Ok(e) => e.path(),
                    Err(e) => {
                        results.push(cold_file_limit(directory, &e.to_string()));
                        continue;
                    }
                };
                if path.extension().is_none_or(|e| e != "json") {
                    continue;
                }
                if self.native_captures.keys().any(|id| {
                    path == if is_pending {
                        storage::pending_path(&self.workspace, id)
                    } else {
                        storage::capture_path(&self.workspace, id)
                    }
                }) {
                    continue;
                }
                let parsed = (|| -> Result<Value, String> {
                    storage::check_path(&path)?;
                    serde_json::from_slice(&std::fs::read(&path).map_err(|e| e.to_string())?)
                        .map_err(|e| e.to_string())
                })();
                let mut value = match parsed {
                    Ok(v) => v,
                    Err(e) => {
                        results.push(cold_file_limit(&path, &e));
                        continue;
                    }
                };
                let mut original = if is_pending {
                    value["capture"].clone()
                } else {
                    value.clone()
                };
                if let Some(object) = original.as_object_mut() {
                    object.remove("recordId");
                }
                if let Err(e) = crate::schema_validation::validate_capture(&original) {
                    results.push(cold_file_limit(&path, &e));
                    continue;
                }
                let id = original["captureId"].as_str().unwrap().to_owned();
                if self.native_captures.contains_key(&id) {
                    continue;
                }
                if is_pending {
                    value["capture"] = original.clone();
                    candidates.entry(id).or_insert((original, None)).1 = Some(value);
                } else {
                    candidates.entry(id).or_insert((original, None));
                }
            }
        }
        let mut candidates = candidates.into_iter().collect::<Vec<_>>();
        candidates.sort_by(|a, b| a.0.cmp(&b.0));
        for (_, (original, pending)) in candidates {
            match recover_capture(&self.workspace,&original,None,pending.as_ref(),false) {
                Ok(result)=>results.push(result),Err(error)=>results.push(json!({"state":"AC-8 record pending","capture":original,"originLimit":ORIGIN_HOLD,"writeFailure":error})),
            }
        }
        Ok(results)
    }
}

pub(crate) fn act_body(capture: &Value) -> Value {
    if matches!(capture["actKind"].as_str(),Some("A4"|"A6"|"A7")) { return file_act::body(capture); }
    if capture["actKind"] == "A15" { return a15::a15_body(capture); }
    json!({
        "actKind":"A16", "actClass":{"value":"person's act (V4-PM-04)"},
        "decisionActor":capture["actor"],"recordingMode":"direct capture",
        "boundSubject":capture["boundSubject"],"boundContent":capture["boundContent"],
        "scope":capture["scope"],"purpose":capture["purpose"],
        "captureEvidence":[{"kind":"capture evidence","ref":capture["captureId"],"resolutionAtWrite":"resolved"}],
        "captureTime":capture["capturedAt"],"evidenceLimits":capture["evidenceLimits"],
        "relations":{"requestRef":capture["requestRef"],"alternativeChosen":capture["alternativeChosen"]}
    })
}
const ORIGIN_HOLD: &str = "capture origin not verified; automatic act replay held";
fn cold_file_limit(path: &Path, error: &str) -> Value {
    json!({"state":"unverified capture file — automatic replay held","sourceFile":path.display().to_string(),"originLimit":ORIGIN_HOLD,"writeFailure":error})
}

fn pending_failure(root: &Path, hot: &mut NativeCapture, error: &str) {
    hot.failure = Some(error.into());
    if let Some(pending) = hot.pending.as_mut() {
        let _ = records::note_capture_submission_failure(root, pending, error);
    }
}
fn recover_capture(
    root: &Path,
    original: &Value,
    mut hot: Option<&mut NativeCapture>,
    disk_pending: Option<&Value>,
    account_delay: bool,
) -> Result<Value, String> {
    crate::schema_validation::validate_capture(original)?;
    let id = original["captureId"]
        .as_str()
        .ok_or("capture identity absent")?;
    if hot.as_ref().is_some_and(|h| h.capture != *original) {
        return Err("capture disagrees with original native custody; no replay".into());
    }
    let target_log = hot.as_ref().map(|h| h.target_log.clone()).unwrap_or_else(|| {
        if original["actKind"] == "A15" { ".chirality/records/acts.jsonl".into() } else { LOG.into() }
    });
    if disk_pending.is_some_and(|p| p["capture"] != *original || p["log"] != target_log) {
        return Err("pending capture/owning log disagreement; no replay".into());
    }
    let cap_path = storage::capture_path(root, id);
    if !cap_path.exists() {
        if hot.is_none() {
            return Ok(
                json!({"state":"AC-8 record pending","capture":original,"captureDurability":"not established","originLimit":ORIGIN_HOLD}),
            );
        }
        storage::create_json(&cap_path, original)?;
    }
    let durable: Value =
        serde_json::from_slice(&std::fs::read(&cap_path).map_err(|e| e.to_string())?)
            .map_err(|e| e.to_string())?;
    let mut facts = durable.clone();
    facts
        .as_object_mut()
        .ok_or("capture not object")?
        .remove("recordId");
    if facts != *original {
        return Err("capture disagreement: original act facts differ; no replay".into());
    }
    if let Err(e) = storage::sync_publication(&cap_path) {
        if let Some(h) = hot.as_deref_mut() {
            pending_failure(root, h, &e);
        }
        return Ok(json!({"state":"AC-8 record pending","capture":durable,"writeFailure":e}));
    }
    let (entries, limits) = storage::read_all(root);
    if !limits.is_empty() {
        let e = format!("incomplete/ambiguous record set: {limits:?}; no replay");
        if let Some(h) = hot.as_deref_mut() {
            pending_failure(root, h, &e);
        }
        return Ok(json!({"state":"AC-8 record pending","capture":durable,"writeFailure":e}));
    }
    let body = act_body(original);
    let matches: Vec<_> = entries
        .iter()
        .filter(|e| {
            matches!(e["kind"].as_str(),Some("human_act" | "act_declined"))
                && e["body"]["captureEvidence"]
                    .as_array()
                    .is_some_and(|refs| refs.iter().any(|r| r["ref"] == id))
        })
        .collect();
    let expected = hot
        .as_ref()
        .and_then(|h| h.pending.as_ref())
        .or(disk_pending)
        .and_then(|p| p["recordId"].as_str());
    if matches.len() > 1
        || matches
            .first()
            .is_some_and(|e| e["kind"] != records::capture_record_kind(original).unwrap_or("invalid") || e["body"] != body || expected.is_some_and(|rid| e["recordId"] != rid))
    {
        return Err("capture/record disagreement or duplicate; no replay".into());
    }
    let existing = matches.first().copied();
    if existing.is_none() && hot.as_ref().is_some_and(|h| h.written) {
        return Err("previously recorded native submission is now unresolvable; no replay".into());
    }
    if let Some(link) = durable.get("recordId") {
        if existing.is_none_or(|r| r["recordId"] != *link) {
            return Err("capture backlink unresolved/disagrees; no replay".into());
        }
    }
    let record = if let Some(record) = existing {
        for path in storage::discover(root)? {
            if let Err(e) = storage::sync_publication(&path) {
                return Ok(
                    json!({"state":"AC-8 record pending","capture":durable,"writeFailure":format!("record durability uncertain: {e}; no replay")}),
                );
            }
        }
        record.clone()
    } else {
        let Some(native) = hot.as_deref_mut() else {
            return Ok(
                json!({"state":"AC-8 record pending","capture":durable,"originLimit":ORIGIN_HOLD,"writeFailure":ORIGIN_HOLD}),
            );
        };
        if native.pending.is_none() {
            match records::prepare_capture_submission(root, original, &target_log) {
                Ok(mut p) => {
                    if let Some(e) = &native.failure {
                        p["delayed"] = json!(true);
                        p["writeFailure"] = json!(e);
                    }
                    native.pending = Some(p);
                }
                Err(e) => {
                    pending_failure(root, native, &e);
                    return Ok(
                        json!({"state":"AC-8 record pending","capture":durable,"writeFailure":e}),
                    );
                }
            }
        }
        let pending = native.pending.as_ref().unwrap();
        if let Err(e) = records::persist_capture_submission(root, pending) {
            pending_failure(root, native, &e);
            return Ok(json!({"state":"AC-8 record pending","capture":durable,"writeFailure":e}));
        }
        match records::append_capture_submission(root, native.pending.as_ref().unwrap(), body) {
            Ok(record) => record,
            Err(e) => {
                pending_failure(root, native, &e);
                return Ok(
                    json!({"state":"AC-8 record pending","capture":durable,"writeFailure":e}),
                );
            }
        }
    };
    let mut result = json!({"state":"AC-7 recorded","record":record,"recordDurable":true,"capture":durable,"captureFile":cap_path.display().to_string(),"provenance":"recorded claim; this recovery does not verify native capture origin"});
    if let Some(native) = hot.as_deref_mut() {
        if let Some(pending) = &native.pending {
            if pending["delayed"] == true {
                if account_delay {
                    if let Err(e) = records::finish_capture_delay(root, pending) {
                        result["delayEvidencePending"] = json!(true);
                        result["delayEvidenceFailure"] = json!(e);
                    }
                } else {
                    result["delayEvidencePending"] = json!(true);
                }
            }
        }
    }
    let rid = result["record"]["recordId"]
        .as_str()
        .ok_or("matching record identity absent")?
        .to_owned();
    match storage::backlink(&cap_path, &rid) {
        Ok(capture) => result["capture"] = capture,
        Err(e) => {
            result["backlinkPending"] = json!(true);
            result["backlinkFailure"] = json!(e);
            result["statusDetail"] = json!("act recorded; capture record link pending");
        }
    }
    Ok(result)
}

/// A pending original capture is not a fresh decision opportunity after relaunch.
fn refuse_unresolved_capture(root: &Path, request_ref: &str) -> Result<(), String> {
    let dir = root.join(CAPTURE_STORE).join("pending");
    let rd = match std::fs::read_dir(&dir) {
        Ok(rd) => Some(rd),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(e) => return Err(format!("not offered: capture discovery incomplete: {e}")),
    };
    for entry in rd.into_iter().flatten() {
        let path = entry.map_err(|e| e.to_string())?.path();
        storage::check_path(&path)?;
        let pending: Value =
            serde_json::from_slice(&std::fs::read(path).map_err(|e| e.to_string())?)
                .map_err(|e| format!("not offered: pending capture unreadable: {e}"))?;
        if pending["capture"]["requestRef"].as_str() == Some(request_ref) {
            let id = pending["capture"]["captureId"]
                .as_str()
                .ok_or("not offered: pending capture identity absent")?;
            let durable: Value =
                serde_json::from_slice(&std::fs::read(storage::capture_path(root, id)).map_err(
                    |e| format!("not offered: pending capture durability not established: {e}"),
                )?)
                .map_err(|e| e.to_string())?;
            if durable.get("recordId") != pending.get("recordId")
                && !has_recorded_capture_claim(
                    root,
                    &pending["capture"],
                    pending["recordId"].as_str(),
                )?
            {
                return Err("not offered: original capture is record pending; reconcile it instead of capturing again".into());
            }
        }
    }
    // The publication-before-submission interruption can leave a capture without metadata.
    let captures = root.join(CAPTURE_STORE);
    if let Ok(rd) = std::fs::read_dir(captures) {
        for entry in rd {
            let path = entry.map_err(|e| e.to_string())?.path();
            if path.extension().is_none_or(|e| e != "json") {
                continue;
            }
            storage::check_path(&path)?;
            let capture: Value =
                serde_json::from_slice(&std::fs::read(path).map_err(|e| e.to_string())?)
                    .map_err(|e| e.to_string())?;
            if capture["requestRef"].as_str() == Some(request_ref)
                && capture.get("recordId").is_none()
                && !has_recorded_capture_claim(root, &capture, None)?
            {
                return Err("not offered: original capture is record pending; native origin must be established before replay".into());
            }
        }
    }
    Ok(())
}
fn has_recorded_capture_claim(
    root: &Path,
    capture: &Value,
    expected: Option<&str>,
) -> Result<bool, String> {
    let (entries, limits) = storage::read_all(root);
    if !limits.is_empty() {
        return Err(format!("not offered: incomplete record set: {limits:?}"));
    }
    let id = capture["captureId"]
        .as_str()
        .ok_or("capture identity absent")?;
    let body = act_body(capture);
    let matches = entries
        .iter()
        .filter(|e| {
            e["kind"] == "human_act"
                && e["body"]["captureEvidence"]
                    .as_array()
                    .is_some_and(|refs| refs.iter().any(|r| r["ref"] == id))
        })
        .collect::<Vec<_>>();
    Ok(matches.len() == 1
        && matches[0]["body"] == body
        && expected.is_none_or(|rid| matches[0]["recordId"] == rid))
}
#[cfg(test)]
mod persistence_tests {
    use super::*;
    fn scratch() -> PathBuf {
        let root = std::env::temp_dir().join(crate::util::opaque_id("act-fault-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        std::fs::create_dir_all(root.join("project/decisions")).unwrap();
        std::fs::copy(
            Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../tests/fixtures/FX-DP1/project/decisions/PKG-1.json"),
            root.join("project/decisions/PKG-1.json"),
        )
        .unwrap();
        root
    }
    fn prepared(root: &Path) -> (ActControl, String, Value) {
        let request = crate::recorder::identify_packages(root).unwrap().remove(0);
        let mut control = ActControl::new(root);
        let offer = control
            .compose_a16(request["recordId"].as_str().unwrap())
            .unwrap();
        let id = offer["offerId"].as_str().unwrap().to_owned();
        let actor = person(Some("Fixture person"), Some("fixture"));
        control.confirmation_text(&id, "ALT-2", &actor).unwrap();
        control.present(&id).unwrap();
        (control, id, actor)
    }
    #[test]
    fn a16_statement_is_bounded_and_an_over_long_one_is_refused_before_presentation() {
        let edited = |edit: &dyn Fn(&mut Value)| {
            let root = scratch();
            let package = root.join("project/decisions/PKG-1.json");
            let mut p: Value = serde_json::from_slice(&std::fs::read(&package).unwrap()).unwrap();
            edit(&mut p);
            std::fs::write(&package, serde_json::to_vec_pretty(&p).unwrap()).unwrap();
            let request = crate::recorder::identify_packages(&root).unwrap().remove(0);
            let mut control = ActControl::new(&root);
            let offer = control.compose_a16(request["recordId"].as_str().unwrap()).unwrap();
            let id = offer["offerId"].as_str().unwrap().to_owned();
            (root, control, id, p)
        };
        let actor = person(Some("Fixture person"), Some("fixture"));
        // V14 F5: forty consequences do not fit the alert. The App shows the
        // chosen alternative whole and the alert names it by digest; the
        // decision is still possible and binds the frozen offer as before.
        let (root, mut control, id, p) = edited(&|p| {
            p["alternatives"][1]["consequences"] =
                json!((0..40).map(|i| format!("invented consequence {i}")).collect::<Vec<_>>());
        });
        let s = control.confirmation_statement(&id, "ALT-2", &actor).unwrap();
        let shown = s.in_app.as_ref().expect("shown whole in the App");
        assert_eq!(shown.content["chosenAlternative"], p["alternatives"][1]);
        assert_eq!(shown.content["offerDigest"], control.offers[&id].offer["offerDigest"]);
        assert_eq!(shown.digest, native_statement::content_digest("x", &shown.content).unwrap());
        assert!(s.text.lines().any(|l| l == shown.digest), "{}", s.text);
        assert!(s.text.contains("Chosen alternative: ALT-2. Its statement and all 40 consequences are shown in full in the App now"), "{}", s.text);
        assert!(s.text.contains("Only Decide records this decision.") && s.text.contains("Cancel closes the control"));
        assert!(native_statement::bounded("x", s.text.clone()).is_ok());
        control.present(&id).unwrap();
        let out = control.confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor.clone()).unwrap();
        assert_eq!(out["capture"]["alternativeChosen"], "ALT-2");
        assert_eq!(out["capture"]["offerDigest"], control.offers[&id].offer["offerDigest"]);
        std::fs::remove_dir_all(root).unwrap();
        // Every consequence of a shorter alternative is shown whole.
        let (root, mut control, id, _) = edited(&|_| {});
        let s = control.confirmation_statement(&id, "ALT-1", &actor).unwrap();
        assert!(s.in_app.is_none());
        assert!(s.text.lines().count() <= native_statement::MAX_LINES);
        assert!(s.text.contains("Stage 2 starts today; any changed supplier fact reopens the affected parts"));
        std::fs::remove_dir_all(root).unwrap();
        // Hard refusal only where even the summary cannot fit (a purpose longer
        // than the alert): nothing frozen, nothing captured.
        let (root, mut control, id, _) = edited(&|p| p["purpose"] = json!("invented purpose ".repeat(120)));
        let err = control.confirmation_text(&id, "ALT-2", &actor).unwrap_err();
        assert!(err.contains("exceeds the readable native confirmation"), "{err}");
        assert!(control.offers[&id].selected.is_none() && control.offers[&id].frozen_offer.is_none());
        let refused = control.confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor.clone());
        assert!(refused.is_err() || refused.unwrap()["recorded"] != true);
        assert!(control.native_captures.is_empty());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn capture_directory_failure_precedes_writer_reservation_then_hot_retry_accounts_delay() {
        let root = scratch();
        let (mut control, id, actor) = prepared(&root);
        storage::ensure_directory(&root.join(CAPTURE_STORE)).unwrap();
        storage::fail_directory_for_test(Some(root.join(CAPTURE_STORE)));
        let result = control.confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor);
        storage::fail_directory_for_test(None);
        let result = result.unwrap();
        assert_eq!(result["state"], "AC-8 record pending");
        assert_eq!(result["captureDurability"], "not established");
        let capture_id = result["captureId"].as_str().unwrap();
        assert!(
            !storage::pending_path(&root, capture_id).exists(),
            "no RS ID reserved before durable capture"
        );
        assert!(control.native_captures[capture_id].pending.is_none());
        let recovered = control.recover_pending().unwrap().remove(0);
        assert_eq!(recovered["state"], "AC-7 recorded");
        let log = crate::records::read_log(&root.join(LOG)).0;
        assert_eq!(log.len(), 4);
        assert_eq!(log[3]["body"]["label"], "record write failed");
        assert_eq!(log[2]["observedAt"], recovered["capture"]["capturedAt"]);
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn existing_match_directory_sync_failure_holds_backlink_until_publication_durable() {
        let root = scratch();
        let (mut control, id, actor) = prepared(&root);
        let result = control
            .confirm(&id, "ALT-2", InputSource::HostNativeConfirmation, actor)
            .unwrap();
        let mut original = result["capture"].clone();
        original.as_object_mut().unwrap().remove("recordId");
        let path = storage::capture_path(&root, original["captureId"].as_str().unwrap());
        std::fs::write(&path, serde_json::to_vec(&original).unwrap()).unwrap();
        let oldlog = std::fs::read(root.join(LOG)).unwrap();
        storage::fail_directory_for_test(Some(root.join(LOG).parent().unwrap().to_path_buf()));
        let attempted = ActControl::new(&root).recover_pending();
        storage::fail_directory_for_test(None);
        let attempted = attempted.unwrap().remove(0);
        assert_eq!(attempted["state"], "AC-8 record pending");
        assert!(attempted["writeFailure"]
            .as_str()
            .unwrap()
            .contains("directory sync"));
        assert!(
            serde_json::from_slice::<Value>(&std::fs::read(&path).unwrap())
                .unwrap()
                .get("recordId")
                .is_none()
        );
        let recovered = ActControl::new(&root).recover_pending().unwrap().remove(0);
        assert_eq!(recovered["state"], "AC-7 recorded");
        assert_eq!(std::fs::read(root.join(LOG)).unwrap(), oldlog);
        assert!(recovered["provenance"]
            .as_str()
            .unwrap()
            .contains("does not verify"));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn equal_observed_times_keep_writer_admission_order_at_fresh_append_and_refresh() {
        for recorder_continuation in [false, true] {
            let root = scratch();
            let (mut control, first_id, actor) = prepared(&root);
            let request_ref = control.offers[&first_id].offer["requestRef"]
                .as_str()
                .unwrap()
                .to_owned();
            let next = control.compose_a16(&request_ref).unwrap();
            let next_id = next["offerId"].as_str().unwrap().to_owned();
            control
                .confirmation_text(&next_id, "ALT-1", &actor)
                .unwrap();
            control.present(&next_id).unwrap();
            let before = std::fs::read(root.join(LOG)).unwrap();
            let mut torn = before.clone();
            torn.extend(b"{torn");
            std::fs::write(root.join(LOG), torn).unwrap();
            FIXED_CAPTURE_TIME
                .with(|time| *time.borrow_mut() = Some("2026-10-04T00:00:00Z".into()));
            let first = control
                .confirm(
                    &first_id,
                    "ALT-2",
                    InputSource::HostNativeConfirmation,
                    actor.clone(),
                )
                .unwrap();
            if recorder_continuation {
                let second = control
                    .confirm(
                        &next_id,
                        "ALT-1",
                        InputSource::HostNativeConfirmation,
                        actor.clone(),
                    )
                    .unwrap();
                assert_eq!(second["state"], "AC-8 record pending");
                std::fs::copy(
                    Path::new(env!("CARGO_MANIFEST_DIR"))
                        .join("../tests/fixtures/FX-DP1/project/decisions/PKG-2.json"),
                    root.join("project/decisions/PKG-2.json"),
                )
                .unwrap();
                std::fs::write(root.join(LOG), &before).unwrap();
                let (_, requests) = control.refresh_recording();
                assert_eq!(requests.unwrap().len(), 1);
            } else {
                std::fs::write(root.join(LOG), &before).unwrap();
                assert_eq!(
                    control
                        .confirm(
                            &next_id,
                            "ALT-1",
                            InputSource::HostNativeConfirmation,
                            actor.clone()
                        )
                        .unwrap()["state"],
                    "AC-7 recorded"
                );
            }
            FIXED_CAPTURE_TIME.with(|time| *time.borrow_mut() = None);
            let entries = crate::records::read_log(&root.join(LOG)).0;
            let acts = entries
                .iter()
                .filter(|e| e["kind"] == "human_act")
                .collect::<Vec<_>>();
            assert_eq!(acts.len(), 2);
            assert_eq!(acts[0]["body"]["relations"]["alternativeChosen"], "ALT-2");
            assert_eq!(acts[1]["body"]["relations"]["alternativeChosen"], "ALT-1");
            assert_eq!(acts[0]["observedAt"], "2026-10-04T00:00:00Z");
            assert_eq!(acts[0]["observedAt"], acts[1]["observedAt"]);
            assert_eq!(
                acts[0]["body"]["captureEvidence"][0]["ref"],
                first["capture"]["captureId"]
            );
            if recorder_continuation {
                let last = entries
                    .iter()
                    .position(|e| {
                        e["kind"] == "act_request"
                            && e["body"]["evidence"]["ref"] == "project/decisions/PKG-2.json"
                    })
                    .unwrap();
                assert!(
                    entries[..last]
                        .iter()
                        .filter(|e| e["kind"] == "human_act")
                        .count()
                        == 2
                );
            }
            std::fs::remove_dir_all(root).unwrap();
        }
    }
}
