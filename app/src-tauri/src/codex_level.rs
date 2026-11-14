//! DEL-01-01 (carrying it to Codex), DEL-01-04 (capturing it), DEL-04-02 (showing it): the permission level the
//! person sets in the App (PRD V4-AUT-06). The person's own setting: never a reserved act, never set by an agent,
//! a tool or an App rule.
//!
//! The levels are one table, `codex_levels.json`, which `supplier_checks/level` sends row by row to the pinned
//! Codex. This module turns a level into the exact fields of each request, checks what Codex reports back
//! against it, and holds the checks that decide whether a level may be sent at all for a given project and home.
use serde_json::{json, Map, Value};
use std::path::{Component, Path, PathBuf};
use std::sync::OnceLock;

pub const TABLE: &str = include_str!("codex_levels.json");

/// The level marked as recommended beside the others. A mark only: never applied and never preselected. None
/// applies until the person has chosen (V4-AUT-06). The owner's to set.
pub const RECOMMENDED_LEVEL: Option<&str> = None;

/// The fields of a request that belong to the level and to nothing else. No other code may put them in a
/// request; `merge` refuses a request that already carries one.
pub const LEVEL_KEYS: [&str; 4] = ["approvalPolicy", "approvalsReviewer", "sandbox", "sandboxPolicy"];
const WORKSPACE_WRITE_CONFIG: &str = "sandbox_workspace_write";

#[derive(Clone, Debug, PartialEq)]
pub struct Level {
    pub id: String,
    pub dimensions: Value,
    pub approval_policy: String,
    pub sandbox: String,
    pub sandbox_policy: Value,
    pub workspace_write: Option<Value>,
}

impl Level {
    /// Whether the level lets commands write anywhere (every level but supervised).
    pub fn allows_writing(&self) -> bool {
        self.sandbox != "read-only"
    }
    /// Whether the level runs commands in a sandbox (every level but full access).
    pub fn sandboxed(&self) -> bool {
        self.sandbox != "danger-full-access"
    }
    /// Whether the level makes the project a writable root (the edits levels).
    pub fn writes_in_the_project(&self) -> bool {
        self.sandbox == "workspace-write"
    }
}

fn parse(table: &str) -> Result<Vec<Level>, String> {
    let root: Value = serde_json::from_str(table).map_err(|e| format!("level table: {e}"))?;
    if root["format"] != "chirality.app-v4.codex-levels.v1" {
        return Err("level table: unknown format".into());
    }
    let rows = root["levels"].as_array().ok_or("level table: no levels")?;
    let mut out: Vec<Level> = Vec::new();
    for row in rows {
        let text = |k: &str| row[k].as_str().map(str::to_owned).ok_or(format!("level table: {k} missing"));
        let level = Level {
            id: text("id")?,
            dimensions: row["dimensions"].clone(),
            approval_policy: text("approvalPolicy")?,
            sandbox: text("sandbox")?,
            sandbox_policy: row["sandboxPolicy"].clone(),
            workspace_write: if row["workspaceWrite"].is_null() { None } else { Some(row["workspaceWrite"].clone()) },
        };
        if !["untrusted", "on-request", "never"].contains(&level.approval_policy.as_str())
            || !["read-only", "workspace-write", "danger-full-access"].contains(&level.sandbox.as_str())
            || level.writes_in_the_project() != level.workspace_write.is_some()
            || out.iter().any(|l| l.id == level.id)
        {
            return Err(format!("level table: row {} is inconsistent", level.id));
        }
        out.push(level);
    }
    Ok(out)
}

/// The levels the App offers, in the table's order.
pub fn levels() -> &'static [Level] {
    static LEVELS: OnceLock<Vec<Level>> = OnceLock::new();
    LEVELS.get_or_init(|| parse(TABLE).expect("the committed level table parses"))
}

pub fn level(id: &str) -> Option<&'static Level> {
    levels().iter().find(|l| l.id == id)
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Method {
    ThreadStart,
    ThreadResume,
    ThreadFork,
    TurnStart,
}

impl Method {
    pub fn of(method: &str) -> Option<Self> {
        Some(match method {
            "thread/start" => Self::ThreadStart,
            "thread/resume" => Self::ThreadResume,
            "thread/fork" => Self::ThreadFork,
            "turn/start" => Self::TurnStart,
            _ => return None,
        })
    }
}

/// The exact fields a level adds to a request of `method`. The reviewer is always the person: with every level
/// the App sends that the person answers the harness's requests (V4-AUT-06).
///
/// - start, resume and fork take only a sandbox mode name, so `config.sandbox_workspace_write` carries the
///   network, the two temporary-folder exclusions and the writable roots. Writable roots are always sent: a root
///   named in the person's own configuration widens workspace write, and only this override removes it.
/// - a turn takes the structured sandbox policy.
pub fn params(level: &Level, method: Method) -> Map<String, Value> {
    let mut out = Map::new();
    out.insert("approvalPolicy".into(), json!(level.approval_policy));
    out.insert("approvalsReviewer".into(), json!("user"));
    match method {
        Method::TurnStart => {
            out.insert("sandboxPolicy".into(), level.sandbox_policy.clone());
        }
        Method::ThreadStart | Method::ThreadResume | Method::ThreadFork => {
            out.insert("sandbox".into(), json!(level.sandbox));
            if let Some(options) = &level.workspace_write {
                out.insert("config".into(), json!({ WORKSPACE_WRITE_CONFIG: options }));
            }
        }
    }
    out
}

/// Adds the level's fields to a request's params. Refuses a request that already carries any of them, or a
/// `config.sandbox_workspace_write`: the level is the only source of these fields.
pub fn merge(request: &mut Value, level: &Level, method: Method) -> Result<(), String> {
    let object = request.as_object_mut().ok_or("request params must be an object")?;
    if let Some(key) = LEVEL_KEYS.iter().find(|k| object.contains_key(**k)) {
        return Err(format!("level field already present: {key}"));
    }
    if object.get("config").and_then(|c| c.get(WORKSPACE_WRITE_CONFIG)).is_some() {
        return Err(format!("level field already present: config.{WORKSPACE_WRITE_CONFIG}"));
    }
    for (key, value) in params(level, method) {
        if key == "config" {
            let config = object.entry("config").or_insert_with(|| json!({}));
            let config = config.as_object_mut().ok_or("config must be an object")?;
            for (k, v) in value.as_object().expect("level config is an object") {
                config.insert(k.clone(), v.clone());
            }
        } else {
            object.insert(key, value);
        }
    }
    Ok(())
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Agreement {
    Agrees,
    /// The reply reports something else: the named fields, as reported.
    Differs(Vec<String>),
}

/// Whether a start, resume or fork reply reports the level as sent: approval, reviewer and the whole structured
/// sandbox, writable roots included. Codex echoes nothing on a turn; a level sent on a turn is unconfirmed until
/// the next such reply.
pub fn agreement(level: &Level, reply: &Value) -> Agreement {
    let mut differs = Vec::new();
    if reply["approvalPolicy"] != json!(level.approval_policy) {
        differs.push(format!("approvalPolicy={}", reply["approvalPolicy"]));
    }
    if reply["approvalsReviewer"] != json!("user") {
        differs.push(format!("approvalsReviewer={}", reply["approvalsReviewer"]));
    }
    if reply["sandbox"] != level.sandbox_policy {
        differs.push(format!("sandbox={}", reply["sandbox"]));
    }
    if differs.is_empty() {
        Agreement::Agrees
    } else {
        Agreement::Differs(differs)
    }
}

/// Characters the App does not accept anywhere in the path of a Codex home it starts Codex in.
pub const UNSAFE_HOME_CHARACTERS: [char; 4] = ['$', '`', '"', '\\'];

/// The first component of `path`, as written or as resolved through links, that holds one of
/// `UNSAFE_HOME_CHARACTERS`, with the character. Every component counts, the part above the App's own folders
/// included. A path that cannot be resolved is checked as written only; the caller has already established the
/// home exists before it starts Codex there.
pub fn unsafe_home_component(path: &Path) -> Option<(char, PathBuf)> {
    let resolved = std::fs::canonicalize(path).ok();
    for candidate in std::iter::once(path.to_path_buf()).chain(resolved) {
        let mut so_far = PathBuf::new();
        for component in candidate.components() {
            so_far.push(component.as_os_str());
            if let Component::Normal(name) = component {
                let name = name.to_string_lossy();
                if let Some(c) = UNSAFE_HOME_CHARACTERS.iter().find(|c| name.contains(**c)) {
                    return Some((*c, so_far));
                }
            }
        }
    }
    None
}

/// Whether a project's path, as given or as resolved, holds a double quote: at the pin the macOS sandbox profile
/// Codex writes for it does not parse, and every sandboxed command fails without running (it fails closed).
pub fn project_path_breaks_sandbox(project: &Path) -> bool {
    let resolved = std::fs::canonicalize(project).ok();
    std::iter::once(project.to_path_buf())
        .chain(resolved)
        .any(|p| p.to_string_lossy().contains('"'))
}

/// Why a level may not be sent for a conversation, as the status names it. `None` means it may.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Refusal {
    /// A person-given writable folder is at, in or contains one of the App's own folders (or that could not be
    /// established); only an edits level is refused for it.
    EditsReachAppFolders { folder: PathBuf, reaches: &'static str },
    /// The project's path holds a double quote; every sandboxed level is refused for it.
    ProjectPathBreaksSandbox,
}

impl Refusal {
    pub fn cause(&self) -> Value {
        match self {
            Self::EditsReachAppFolders { folder, reaches } => json!({
                "refused": "edits-level-reaches-app-folders", "which": reaches, "folder": folder.to_string_lossy()}),
            Self::ProjectPathBreaksSandbox => json!({
                "refused": "project-path-breaks-codex-sandbox", "character": "\""}),
        }
    }
}

/// The checks made each time a level is about to be sent for a conversation: the App's own folders against the
/// person-given writable folders (by identity, `working_folder::may_overlap`, which counts containment), and the
/// double quote in the project's path. `protected` names each of the App's own folders with what it is
/// ("app-data", "codex-home", "working-files"). `exempt` is the no-project folder, which lies in the App data
/// folder by construction and is kept apart from the other App folders by its own checks.
pub fn refusal(
    level: &Level,
    project: &Path,
    protected: &[(&'static str, &Path)],
    exempt: Option<&Path>,
) -> Option<Refusal> {
    if level.sandboxed() && project_path_breaks_sandbox(project) {
        return Some(Refusal::ProjectPathBreaksSandbox);
    }
    if !level.writes_in_the_project() || exempt.is_some_and(|e| same_folder(e, project)) {
        return None;
    }
    for (reaches, reserved) in protected {
        match crate::working_folder::may_overlap(project, reserved) {
            Ok(false) => {}
            Ok(true) | Err(()) => {
                return Some(Refusal::EditsReachAppFolders { folder: project.to_path_buf(), reaches })
            }
        }
    }
    None
}

fn same_folder(a: &Path, b: &Path) -> bool {
    use std::os::unix::fs::MetadataExt;
    match (std::fs::metadata(a), std::fs::metadata(b)) {
        (Ok(x), Ok(y)) => x.dev() == y.dev() && x.ino() == y.ino(),
        _ => false,
    }
}

#[cfg(test)]
#[path = "codex_level_tests.rs"]
mod tests;
