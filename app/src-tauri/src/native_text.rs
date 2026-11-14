//! Text on a native sheet. A native sheet is a control the page cannot box, so a value someone
//! other than the App supplied reaches one only in a closed form, or in the form its caller
//! chooses for a value that does not fit: withheld behind a sentence of the App's own, or set
//! apart as supplied words. The Records lane owns this module; its shape was settled with the
//! Execution and recovery lane, with the same categories as the view side.
//!
//! The contract for every function: what comes back is either matched to its closed form, or
//! the caller's chosen unfit form. Nothing raw reaches a sheet.
//!
//! What it checks and what it trusts: it checks every value that comes from outside the App's
//! source (a supplier, a file, a record); it trusts as written the caller's own static words, the
//! sentence given to `Unfit::Withhold` and any table given to `vocabulary`, which are text in the
//! App's source. A reviewer of a new caller must read those words.
use serde_json::Value;

/// The usual withheld form of a value Codex reported that is not in its closed form.
pub(crate) const CODEX_VALUE_NOT_SHOWN: &str = "(a value Codex reported that the App does not show here)";
/// The usual withheld form of any other value that is not in its closed form.
pub(crate) const VALUE_NOT_SHOWN: &str = "(a value the App does not show here)";

/// Who supplied a value (the same set as the view's supplied-text sources).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Source {
    Agent,
    Tool,
    Person,
    Codex,
    File,
    Record,
}

/// What a sheet does with a value that is not in its closed form.
#[derive(Clone, Copy, Debug)]
pub(crate) enum Unfit {
    /// Show this sentence of the App's own in its place (a literal, by its type).
    Withhold(&'static str),
    /// Set the value apart, on its own lines, as supplied words.
    Supplied { label: &'static str, source: Source },
}

/// Text matched to a closed form, or a sentence of the App's own: it holds no line break,
/// control, format, direction or invisible character, so it may sit inside an App sentence.
/// Only this module makes one.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Closed(String);
impl Closed {
    pub(crate) fn as_str(&self) -> &str {
        &self.0
    }
}
impl std::fmt::Display for Closed {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

/// Supplied words set apart on their own lines, never inside an App sentence. Only this module
/// makes them.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Supplied(Vec<String>);
impl Supplied {
    pub(crate) fn lines(&self) -> &[String] {
        &self.0
    }
}

/// Where a value goes on a sheet.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum Placed {
    /// Inside an App sentence.
    Inline(Closed),
    /// On lines of their own.
    Lines(Supplied),
}

fn unfit(value: &Value, unfit: Unfit) -> Placed {
    match unfit {
        Unfit::Withhold(literal) => Placed::Inline(Closed(literal.to_owned())),
        Unfit::Supplied { label, source } => Placed::Lines(supplied(label, source, value)),
    }
}
fn string_fitting(value: &Value, fits: impl Fn(&str) -> bool) -> Option<Closed> {
    value.as_str().filter(|s| fits(s)).map(|s| Closed(s.to_owned()))
}

/// A plain identifier, as written: 1 to 128 ASCII letters, digits, `-`, `_`, `.`, `:` or `/`,
/// or a whole non-negative number that fits in 64 bits (a JSON integer; `1.0` is withheld).
pub(crate) fn identifier(value: &Value, otherwise: Unfit) -> Placed {
    let fits = |s: &str| (1..=128).contains(&s.len()) && s.bytes().all(|b| b.is_ascii_alphanumeric() || b"-_.:/".contains(&b));
    match value {
        Value::Number(n) if n.is_u64() => Placed::Inline(Closed(n.to_string())),
        _ => string_fitting(value, fits).map_or_else(|| unfit(value, otherwise), Placed::Inline),
    }
}
/// A value in the App's table becomes the App's word for it; anything else takes the unfit form.
pub(crate) fn vocabulary(value: &Value, known: &'static [(&'static str, &'static str)], otherwise: Unfit) -> Placed {
    value
        .as_str()
        .and_then(|s| known.iter().find(|(v, _)| *v == s))
        .map_or_else(|| unfit(value, otherwise), |(_, word)| Placed::Inline(Closed((*word).to_owned())))
}
/// A time as the App writes it: 1 to 40 digits and `-`, `:`, `T`, `.`, `Z`, `+`, beginning with a
/// digit.
pub(crate) fn time(value: &Value, otherwise: Unfit) -> Placed {
    let fits = |s: &str| (1..=40).contains(&s.len()) && s.as_bytes()[0].is_ascii_digit() && s.bytes().all(|b| b.is_ascii_digit() || b"-:T.Z+".contains(&b));
    string_fitting(value, fits).map_or_else(|| unfit(value, otherwise), Placed::Inline)
}
/// A whole non-negative number that fits in 64 bits, in decimal (a JSON integer; `1.0` is
/// withheld).
pub(crate) fn number(value: &Value, otherwise: Unfit) -> Placed {
    match value {
        Value::Number(n) if n.is_u64() => Placed::Inline(Closed(n.to_string())),
        _ => unfit(value, otherwise),
    }
}
/// A registered workflow name (`workflow_workspace::valid_name`).
pub(crate) fn workflow_name(value: &Value, otherwise: Unfit) -> Placed {
    string_fitting(value, crate::workflow_workspace::valid_name).map_or_else(|| unfit(value, otherwise), Placed::Inline)
}
/// The Records lane's supplied form: the value on its own lines under "<label> (supplied by
/// <source>, not the App's words):", with control, direction and invisible characters shown as
/// marks, line breaks shown and continued on an indented line, and the original value bounded
/// at 600 Unicode scalar characters before marking.
pub(crate) fn supplied(label: &'static str, source: Source, value: &Value) -> Supplied {
    let source = match source {
        Source::Agent => "agent", Source::Tool => "a tool", Source::Person => "the person",
        Source::Codex => "Codex", Source::File => "a file", Source::Record => "a record",
    };
    let text = value.as_str().map(str::to_owned).unwrap_or_else(|| value.to_string());
    let mut out = vec![format!("{label} (supplied by {source}, not the App's words):")];
    let mut line = String::from("  ");
    let mut chars = text.chars().take(600).peekable();
    while let Some(c) = chars.next() {
        if c == '\r' || c == '\n' {
            line.push_str(&mark(c));
            if c == '\r' && chars.peek() == Some(&'\n') {
                line.push_str(&mark(chars.next().unwrap()));
            }
            out.push(line);
            line = String::from("  ");
        } else if marked_character(c) {
            line.push_str(&mark(c));
        } else {
            line.push(c);
        }
    }
    out.push(line);
    if text.chars().count() > 600 { out.push("  (cut after 600 characters)".into()); }
    Supplied(out)
}

fn mark(c: char) -> String { format!("\\u{{{:04X}}}", c as u32) }
/// Unicode format characters, default-ignorable characters and blank separators in addition
/// to controls. Keep visible letters and accents readable; no direction/zero-width instruction
/// or invisible separator is passed through to the native renderer.
fn marked_character(c: char) -> bool {
    c.is_control() || (c.is_whitespace() && c != ' ') || matches!(c,
        '\u{00AD}' | '\u{034F}' | '\u{0600}'..='\u{0605}' | '\u{061C}' | '\u{06DD}' |
        '\u{070F}' | '\u{0890}'..='\u{0891}' |
        '\u{08E2}' | '\u{115F}'..='\u{1160}' | '\u{17B4}'..='\u{17B5}' |
        '\u{180B}'..='\u{180F}' | '\u{2000}'..='\u{200F}' | '\u{2028}'..='\u{202F}' |
        '\u{205F}'..='\u{206F}' | '\u{2800}' | '\u{3164}' | '\u{FE00}'..='\u{FE0F}' |
        '\u{FEFF}' | '\u{FFA0}' | '\u{FFF0}'..='\u{FFFB}' | '\u{110BD}' | '\u{110CD}' |
        '\u{13430}'..='\u{13455}' | '\u{1BCA0}'..='\u{1BCAF}' |
        '\u{1D173}'..='\u{1D17A}' | '\u{E0000}'..='\u{E0FFF}')
}

/// The pinned supplier's own values (0.167.0 schema), each its own App word.
pub(crate) mod supplier {
    /// `TurnStatus`.
    pub(crate) const TURN_STATUSES: &[(&str, &str)] = &[("completed", "completed"), ("interrupted", "interrupted"), ("failed", "failed"), ("inProgress", "inProgress")];
    /// `CollabAgentStatus`.
    pub(crate) const AGENT_STATUSES: &[(&str, &str)] = &[
        ("pendingInit", "pendingInit"), ("running", "running"), ("interrupted", "interrupted"), ("completed", "completed"),
        ("errored", "errored"), ("shutdown", "shutdown"), ("notFound", "notFound"),
    ];
    /// `ServerRequest`'s methods.
    pub(crate) const SERVER_REQUEST_METHODS: &[(&str, &str)] = &[
        ("item/commandExecution/requestApproval", "item/commandExecution/requestApproval"),
        ("item/fileChange/requestApproval", "item/fileChange/requestApproval"),
        ("item/tool/requestUserInput", "item/tool/requestUserInput"),
        ("mcpServer/elicitation/request", "mcpServer/elicitation/request"),
        ("item/permissions/requestApproval", "item/permissions/requestApproval"),
        ("item/tool/call", "item/tool/call"),
        ("account/chatgptAuthTokens/refresh", "account/chatgptAuthTokens/refresh"),
        ("attestation/generate", "attestation/generate"),
        ("currentTime/read", "currentTime/read"),
        ("applyPatchApproval", "applyPatchApproval"),
        ("execCommandApproval", "execCommandApproval"),
    ];
}
/// The App's own values, each its own word.
pub(crate) mod app {
    /// The Host's process states: exactly the lifecycle schema's (`hosting.lifecycle-event`,
    /// `$defs.state`).
    pub(crate) const HOST_STATES: &[(&str, &str)] = &[
        ("absent", "absent"), ("verifying", "verifying"), ("refused", "refused"), ("spawning", "spawning"),
        ("handshaking", "handshaking"), ("ready", "ready"), ("exited-unexpectedly", "exited-unexpectedly"),
        ("restart-waiting", "restart-waiting"), ("halted-after-repeated-failure", "halted-after-repeated-failure"),
        ("stopping", "stopping"), ("stopped", "stopped"),
    ];
    /// The home classes (`home_resources::HomeClass::as_str`).
    pub(crate) const HOME_CLASSES: &[(&str, &str)] = &[("account", "account"), ("api-key", "api-key"), ("local-provider", "local-provider"), ("probe", "probe")];
}

#[cfg(test)]
#[path = "native_text_tests.rs"]
mod tests;
#[cfg(test)]
#[path = "native_text_supplied_tests.rs"]
mod supplied_tests;
