//! Text on a native sheet. A native sheet is a control the page cannot box, so a value someone
//! other than the App supplied reaches one only in a closed form, or in the form its caller
//! chooses for a value that does not fit: withheld behind a sentence of the App's own, or set
//! apart as supplied words. The Records lane owns this module; its shape was settled with the
//! Execution and recovery lane, with the same categories as the view side.
//!
//! The contract for every function: what comes back is either matched to its closed form, or
//! the caller's chosen unfit form. Nothing raw reaches a sheet.
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
/// or a whole non-negative number.
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
/// A whole non-negative number, in decimal.
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
/// marks, line breaks shown and continued on an indented line, and the value bounded. It lands
/// in the Records lane's standing-decision unit; until then no sheet passes `Unfit::Supplied`.
pub(crate) fn supplied(_label: &'static str, _source: Source, _value: &Value) -> Supplied {
    todo!("the Records lane's supplied form lands in its standing-decision unit; no sheet passes Unfit::Supplied before it")
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
    /// The Host's process states.
    pub(crate) const HOST_STATES: &[(&str, &str)] = &[
        ("absent", "absent"), ("verifying", "verifying"), ("handshaking", "handshaking"), ("ready", "ready"),
        ("stopping", "stopping"), ("stopped", "stopped"), ("refused", "refused"), ("failed", "failed"),
    ];
    /// The home classes (`home_resources::HomeClass::as_str`).
    pub(crate) const HOME_CLASSES: &[(&str, &str)] = &[("account", "account"), ("api-key", "api-key"), ("local-provider", "local-provider"), ("probe", "probe")];
}

#[cfg(test)]
#[path = "native_text_tests.rs"]
mod tests;
