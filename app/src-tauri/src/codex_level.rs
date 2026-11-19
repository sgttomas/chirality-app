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

/// The App's default level: the row a complete launch read puts in force for the default scope when the ledger
/// holds no valid `level_chosen` for it. It is shown as the App's default, never as the person's choice, and is
/// never written as a person's choice; any usable recorded choice wins over it. The launch reader applies
/// the missing/unreadable-record and home-state exceptions before selecting it.
/// Tests replace it only through the `cfg(test)` setter `Host::set_app_default_for_test`; a shipped build has no
/// other route to it.
pub const DEFAULT_LEVEL: Option<&str> = Some("full");

/// The status's closed sentence for a level in force by the App's default.
pub const APP_DEFAULT_SENTENCE: &str = "The App's default level, not chosen by you. You can choose another level at any time.";
/// Where the status explains the App's default.
/// What allowing a command beyond the sandbox means at an asking level, at the pinned Codex (supplier_checks/level: the escalation rows and
/// `AskEachCommandInsideTheProject`; the features that would grant less are under development and off).
pub const SUPERVISED_ALLOWING: &str = "When a command needs your approval, Codex asks. If you allow it, the command can run outside the sandbox, with your account's access to all your files and to the network; Codex cannot run it limited to this project. Your own rules and hooks can allow or refuse a command without asking you.";
pub const READING_SENTENCE: &str = "Reading is not limited at any permission level.";
pub const NEXT_TURN_SENTENCE: &str = "From the next turn. Commands already running, and anything they started, keep the access they started with until they end. They end when Codex closes normally, as it ordinarily does when you stop or restart Codex or quit the App.";
pub const APP_DEFAULT_EXPLAINED: &str = "The App's default level is full access: commands run with no sandbox, with your account's access to your files and the network, including the App's own records and settings. You can choose another level at any time.";
/// The status's closed sentence for a level chosen while the App's records could not be read or saved.
/// The ask, the one exception to the App's default (V4-AUT-06): the App's record of the level is missing, holds a
/// choice that no longer matches the table, or cannot be read, while this home has been used. The App's default is
/// preselected beside it.
pub const RECORD_MISSING_SENTENCE: &str = "The App's record of your permission level is missing or could not be used, so the App cannot tell whether you chose a level before; a missing record can mean that a command removed or changed it. Choose a level to continue. The App's default, full access, is selected.";
/// Beside the App's default where the App's records could not be read on a first run.
pub const RECORDS_UNREAD_SENTENCE: &str = "The App could not read its records. A level you choose now is in force for this session; the App will show whether saving it is confirmed.";
/// The name Codex gives the state database it creates in its home when it first starts there (state/src/sqlite.rs
/// at rust-v0.167.0). The App never creates it.
pub const CODEX_STATE_NAME: &str = "state_5.sqlite";
/// Whether this home holds state from an earlier Codex start: presence of [`CODEX_STATE_NAME`] directly in it, by
/// `symlink_metadata` only. Ok(true) is present, Ok(false) is established absence, and Err is unknown.
/// Nothing is opened, nothing is followed and no other folder is looked at.
pub fn home_has_codex_state(codex_home: &Path) -> Result<bool, String> {
    match std::fs::symlink_metadata(codex_home.join(CODEX_STATE_NAME)) {
        Ok(_) => Ok(true),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(false),
        Err(error) => Err(error.to_string()),
    }
}
pub const INHERITANCE_NOT_RECORDED: &str = "The App could not confirm that this conversation's level was saved. If it is not saved before the App closes, reopening follows the default for new conversations then in force, which could allow more than this level, unless you set its level.";
pub const FOLLOWS_DEFAULT_SENTENCE: &str = "This conversation follows the default. Changing the default changes its level until you set a level for this conversation.";
pub const DEFAULT_SCOPE_SENTENCE: &str = "Changing the level here changes the default for new conversations and for saved conversations that have no level of their own. Conversations with their own level keep it.";
pub const SAVE_UNCONFIRMED_APPLIED: &str = "The App could not confirm the level was saved. It is in force for this session.";
pub const SAVE_UNCONFIRMED_NOT_APPLIED: &str = "The App could not confirm the level was saved. This session's level was not changed; reopening will show the level the records then hold.";
pub const SESSION_ONLY_SENTENCE: &str = "Chosen for now. The App could not read or save its records, so this level is not kept after the App closes.";
/// Why a session-only choice was offered: the App's own sentences, beside which any raw detail is kept apart.
pub const RECORDS_NOT_READ: &str = "The App's records could not be read when it started.";
pub const RECORDS_UNAVAILABLE: &str = "The App's records are not available in this session.";
/// How the status marks text the App did not write (a raw error detail).
pub const NOT_THE_APPS_TEXT: &str = "Text the App did not write.";

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

/// The configuration key that carries the project's trust entry on start, resume and fork.
pub const PROJECTS_CONFIG: &str = "projects";
/// Configuration keys no frame ever carries.
pub const NEVER_SENT_CONFIG: [&str; 2] = ["bypass_hook_trust", "hooks.state"];

/// Everything the App adds to a request of `method` beside what the frame's builder made: the level's fields
/// (`params`) and, on start, resume and fork, `config.projects` with its one trust entry (`projects`, see
/// [`TrustReading::projects`]).
pub fn additions(level: &Level, method: Method, projects: Option<&Value>) -> Map<String, Value> {
    let mut out = params(level, method);
    if let (Some(projects), Method::ThreadStart | Method::ThreadResume | Method::ThreadFork) = (projects, method) {
        let config = out.entry("config").or_insert_with(|| json!({}));
        config.as_object_mut().expect("level config is an object").insert(PROJECTS_CONFIG.into(), projects.clone());
    }
    out
}

/// Adds the level's fields to a request's params. Refuses a request that already carries any of them, or a
/// `config.sandbox_workspace_write`: the level is the only source of these fields.
pub fn merge(request: &mut Value, level: &Level, method: Method) -> Result<(), String> {
    merge_fields(request, &params(level, method))
}

/// Adds `fields` (from [`additions`]) to a request's params. Refuses a request that already carries a level field
/// or any configuration key `fields` adds (`sandbox_workspace_write`, `projects`): only the App adds them.
pub fn merge_fields(request: &mut Value, fields: &Map<String, Value>) -> Result<(), String> {
    let object = request.as_object_mut().ok_or("request params must be an object")?;
    if let Some(key) = LEVEL_KEYS.iter().find(|k| object.contains_key(**k)) {
        return Err(format!("level field already present: {key}"));
    }
    for key in [WORKSPACE_WRITE_CONFIG, PROJECTS_CONFIG] {
        if object.get("config").and_then(|c| c.get(key)).is_some() {
            return Err(format!("level field already present: config.{key}"));
        }
    }
    for (key, value) in fields {
        if key == "config" {
            let config = object.entry("config").or_insert_with(|| json!({}));
            let config = config.as_object_mut().ok_or("config must be an object")?;
            for (k, v) in value.as_object().ok_or("level config must be an object")? {
                config.insert(k.clone(), v.clone());
            }
        } else {
            object.insert(key.clone(), value.clone());
        }
    }
    Ok(())
}

/// The complete params a request of `method` must carry when `base` is what the App built for it and `level` the
/// level bound to it when its frame was built: `base` with the level's fields added by `merge`, the same addition
/// the frame builder made. A site comparing sent params with rebuilt or expected ones compares the whole sent params
/// with this, so a missing, partial or extra level field, an unexpected field and a configuration key `merge` would
/// refuse all still differ. It only adds; nothing is removed from what was sent. `None` (no level bound to the
/// request) is `base` unchanged. A start, resume or fork also carries its trust entry: compare those with
/// [`expected_with_bound`].
pub fn expected_with_level(base: &Value, level: Option<&Level>, method: Method) -> Result<Value, String> {
    let mut expected = base.clone();
    if let Some(level) = level {
        merge(&mut expected, level, method)?;
    }
    Ok(expected)
}

/// The complete params a request must carry when `base` is what the App built and `bound` what was bound to it
/// when its frame was built: `base` with exactly the bound additions (the level's fields and, on start, resume and
/// fork, the trust entry). `None` is `base` unchanged.
pub fn expected_with_bound(base: &Value, bound: Option<&Bound>) -> Result<Value, String> {
    let mut expected = base.clone();
    if let Some(bound) = bound {
        merge_fields(&mut expected, &bound.fields)?;
    }
    Ok(expected)
}

/// The post-condition of the frame builder, checked independently of `merge`: `sent` is exactly `built` with
/// `params(level, method)` added and nothing else.
pub fn carries_exactly(built: &Value, sent: &Value, level: &Level, method: Method) -> bool {
    carries_exactly_fields(built, sent, &params(level, method))
}

/// `sent` is exactly `built` with `fields` added and nothing else. Every field of `built` is in `sent` unchanged,
/// every added field is in `sent` with its value and was not in `built`, and `config` is `built`'s configuration (or
/// none) with the added configuration keys, none of which it already had.
pub fn carries_exactly_fields(built: &Value, sent: &Value, fields: &Map<String, Value>) -> bool {
    let (Some(b), Some(s)) = (built.as_object(), sent.as_object()) else { return false };
    let keys: std::collections::BTreeSet<&String> = b.keys().chain(s.keys()).chain(fields.keys()).collect();
    for key in keys {
        let ok = match (b.get(key), s.get(key), fields.get(key)) {
            (built_config, Some(sent_config), Some(level_config)) if key == "config" => {
                let base = match built_config {
                    None => Map::new(),
                    Some(Value::Object(c)) => c.clone(),
                    Some(_) => return false,
                };
                let Some(level_config) = level_config.as_object() else { return false };
                if level_config.keys().any(|k| base.contains_key(k)) {
                    return false;
                }
                let mut want = base;
                want.extend(level_config.clone());
                *sent_config == Value::Object(want)
            }
            (None, Some(sent), Some(field)) => sent == field,
            (Some(built), Some(sent), None) => built == sent,
            _ => false,
        };
        if !ok {
            return false;
        }
    }
    true
}

/// The configuration a start, resume or fork frame may carry, checked on the frame as it is about to be written:
/// `projects` with exactly one entry whose only field is `trust_level`, "trusted" or "untrusted"; never
/// `bypass_hook_trust`, `hooks.state` or a `hooks` table with `state`. Other methods carry no `projects`.
pub fn config_post_condition(sent: &Value, method: Method) -> Result<(), String> {
    let config = sent.get("config");
    if let Some(config) = config {
        let Some(config) = config.as_object() else { return Err("config is not an object".into()) };
        if let Some(key) = NEVER_SENT_CONFIG.iter().find(|k| config.contains_key(**k)) {
            return Err(format!("config.{key} is never sent"));
        }
        if config.get("hooks").is_some_and(|h| h.get("state").is_some()) {
            return Err("config.hooks.state is never sent".into());
        }
    }
    let projects = config.and_then(|c| c.get(PROJECTS_CONFIG));
    match method {
        Method::TurnStart => match projects {
            None => Ok(()),
            Some(_) => Err("a turn carries no projects entry".into()),
        },
        _ => {
            let entries = projects.and_then(Value::as_object).ok_or("config.projects is missing")?;
            let [(_, entry)] = entries.iter().collect::<Vec<_>>()[..] else {
                return Err(format!("config.projects has {} entries, not exactly one", entries.len()));
            };
            match entry.as_object() {
                Some(o) if o.len() == 1 && matches!(o.get("trust_level").and_then(Value::as_str), Some("trusted" | "untrusted")) => Ok(()),
                _ => Err("config.projects' entry is not exactly a trust level".into()),
            }
        }
    }
}

// ---- Project trust (Codex's `projects.<path>.trust_level`) ----

/// The project root Codex computes for a working folder with its default markers: the nearest folder, the
/// working folder included, holding `.git` (a file, or a folder with `HEAD` in it), else the working folder
/// (codex-rs/config/src/loader/mod.rs `discover_project_root` at rust-v0.167.0).
pub fn project_root(cwd: &Path) -> PathBuf {
    for ancestor in cwd.ancestors() {
        let marker = ancestor.join(".git");
        match std::fs::metadata(&marker) {
            Ok(m) if m.is_dir() && std::fs::metadata(marker.join("HEAD")).is_err() => continue,
            Ok(_) => return ancestor.to_path_buf(),
            Err(_) => continue,
        }
    }
    cwd.to_path_buf()
}

/// The spellings Codex looks a project's trust up by on macOS, in its order: the canonical path first, then the
/// path as given when it differs. It matches each exactly (loader/mod.rs:1571-1618 at rust-v0.167.0).
pub fn trust_lookup_keys(path: &Path) -> Vec<String> {
    let given = path.to_string_lossy().into_owned();
    let canonical = std::fs::canonicalize(path).map(|p| p.to_string_lossy().into_owned()).unwrap_or_else(|_| given.clone());
    if canonical == given { vec![canonical] } else { vec![canonical, given] }
}

/// What a whole, current reading of the person's settings says of a project's trust.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum TrustCase {
    /// The person's settings mark the root trusted, under `key`.
    Trusted { key: String },
    /// The person's settings mark the root untrusted, under `key`.
    MarkedUntrusted { key: String },
    /// No mark for the root in the person's settings.
    Unmarked,
    /// No whole, current reading: `reason` is the App's own sentence, `detail` any raw text it did not write.
    NotRead { reason: String, detail: Option<String> },
}

/// The status's closed sentences for the trust entry.
// "The Codex settings the App uses" are the account home's settings: the person's own Codex settings where the home
// shares them, the App's own new settings where the person chose new settings at setup. The mark is read from them by
// `config/read` (cwd set, layers included), in the user layer.
pub const TRUST_TRUSTED_PREFIX: &str = "This project is marked trusted in the Codex settings the App uses (read at ";
pub const TRUST_TRUSTED_SUFFIX: &str = "). The App sent a trusted entry for the project root shown below.";
pub const TRUST_UNTRUSTED_SENT: &str = "The App sent an untrusted entry for the project root shown below.";
pub const TRUST_MARKED_UNTRUSTED: &str = "This project is marked untrusted in the Codex settings the App uses.";
pub const TRUST_NOT_READ: &str = "The App could not read the Codex settings it uses for this project, so it sent an untrusted entry for the project root shown below.";
/// The reasons a reading is not whole and current (`TrustCase::NotRead`), in the App's own words.
pub const TRUST_READ_FAILED: &str = "The App's reading of the Codex settings it uses did not complete.";
pub const TRUST_READ_LIMITED: &str = "The App's reading of the Codex settings it uses did not include the settings files.";
pub const TRUST_READ_TIMED_OUT: &str = "The App's reading of the Codex settings it uses did not complete in time.";
pub const TRUST_READ_STALE: &str = "The App's reading of the Codex settings it uses was no longer the latest when the request was built.";

/// The App's own trust choice for the project a frame's working folder is (the owner's decision of 19 November
/// 2026; `project_trust`). Read just before each start, resume and fork, beside the settings reading.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum AppTrust {
    /// On by default: the person set this project up in Chirality and has not switched its trust off.
    OnBySetup,
    /// On by the person's switch (a confirmed act), at `at`.
    OnBySwitch { at: String },
    /// Off by the person's switch, at `at`.
    OffBySwitch { at: String },
    /// Off by the line the new-identity act writes for a project whose trust would otherwise be on, at `at`.
    OffByNewIdentity { at: String },
    /// The project's folder as given no longer resolves to the folder the App admitted: the App's choice is not
    /// applied, and the entry is untrusted.
    FolderChanged,
    /// No choice: the project was opened from the environment route. Today's rule applies.
    NoChoice,
    /// The choice could not be read: treated as an unreadable settings reading (untrusted). `detail` is the
    /// store's own account of why, kept as supplied text.
    NotRead { detail: Option<String> },
}
impl AppTrust {
    pub fn word(&self) -> &'static str {
        match self { Self::OnBySetup | Self::OnBySwitch { .. } => "on", Self::OffBySwitch { .. } | Self::OffByNewIdentity { .. } => "off", Self::NoChoice => "none", Self::NotRead { .. } => "not-read", Self::FolderChanged => "folder-changed" }
    }
}

/// The status's sentences for the App's own choice, beside the closed sentences above.
pub const TRUST_ON_BY_SETUP: &str = "Chirality's choice for this project is on (you set it up in Chirality and have not switched its trust off), so the App sent a trusted entry for the project root shown below.";
pub const TRUST_ON_BY_SWITCH_PREFIX: &str = "Chirality's choice for this project is on (switched on in Chirality at ";
pub const TRUST_ON_BY_SWITCH_SUFFIX: &str = "), so the App sent a trusted entry for the project root shown below.";
pub const TRUST_OFF_BY_SWITCH_PREFIX: &str = "Chirality's choice for this project is off (switched off in Chirality at ";
pub const TRUST_OFF_BY_SWITCH_SUFFIX: &str = "), so the App sent an untrusted entry for the project root shown below.";
pub const TRUST_CHOICE_NOT_READ: &str = "The App could not read its record of this project's trust choice, so it sent an untrusted entry for the project root shown below.";
pub const TRUST_OFF_BY_NEW_IDENTITY: &str = "Chirality's choice for this project is off (the project was given a new identity), so the App sent an untrusted entry for the project root shown below.";
pub const TRUST_FOLDER_CHANGED: &str = "The project's folder is no longer the folder Chirality opened, so the App sent an untrusted entry for the project root shown below.";

/// The project trust the App sends on one start, resume or fork, and why.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct TrustReading {
    /// The conversation's working folder, absolute, and its project root as Codex computes it.
    pub cwd: PathBuf,
    pub root: PathBuf,
    /// The spelling the entry is sent under: the first Codex looks up.
    pub key: String,
    pub case: TrustCase,
    /// The generation and request reference of the `config/read` the case comes from; None when none was made.
    pub generation: Option<Value>,
    pub request_ref: Option<String>,
    pub read_at: Option<String>,
    /// The App's choice for the project this frame's folder is; None when the folder is not the App's project
    /// (today's rule applies, exactly).
    pub choice: Option<AppTrust>,
    /// The revision of that choice as read (`project_trust::ChoiceRead::revision`), and the project's physical
    /// folder it was read for: the frame is written only while both still hold.
    pub choice_revision: Option<String>,
    pub choice_project: Option<PathBuf>,
}

/// Why the entry is what it is: the rows of the case table, in their order (DEL-01-01).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum TrustRow {
    /// 1. The settings reading is not whole and current.
    SettingsNotRead,
    /// 7. The App's choice for the project cannot be read (treated as row 1).
    ChoiceNotRead,
    /// 8. The project's folder no longer resolves to the folder the App admitted (treated as row 1).
    FolderChanged,
    /// 2. The settings mark the root untrusted.
    MarkedUntrusted,
    /// 3. The person switched trust off in the App.
    SwitchedOff,
    /// 4. The settings mark the root trusted.
    MarkedTrusted,
    /// 5. Not marked, and the App's choice is on.
    AppOn,
    /// 6. Otherwise.
    Unmarked,
}

impl TrustReading {
    /// A reading that cannot be relied on: the entry is sent as untrusted.
    pub fn not_read(cwd: PathBuf, reason: &str, detail: Option<String>) -> Self {
        let root = project_root(&cwd);
        let key = trust_lookup_keys(&root).remove(0);
        TrustReading { cwd, root, key, case: TrustCase::NotRead { reason: reason.into(), detail }, generation: None, request_ref: None, read_at: None, choice: None, choice_revision: None, choice_project: None }
    }
    /// The row of the case table this reading falls in. The order is the precedence: an unreadable settings
    /// reading or an unreadable choice over everything, then the person's untrusted mark, then the App's off,
    /// then the person's trusted mark, then the App's on.
    pub fn row(&self) -> TrustRow {
        match (&self.case, &self.choice) {
            (TrustCase::NotRead { .. }, _) => TrustRow::SettingsNotRead,
            (_, Some(AppTrust::NotRead { .. })) => TrustRow::ChoiceNotRead,
            (_, Some(AppTrust::FolderChanged)) => TrustRow::FolderChanged,
            (TrustCase::MarkedUntrusted { .. }, _) => TrustRow::MarkedUntrusted,
            (_, Some(AppTrust::OffBySwitch { .. } | AppTrust::OffByNewIdentity { .. })) => TrustRow::SwitchedOff,
            (TrustCase::Trusted { .. }, _) => TrustRow::MarkedTrusted,
            (TrustCase::Unmarked, Some(AppTrust::OnBySetup | AppTrust::OnBySwitch { .. })) => TrustRow::AppOn,
            (TrustCase::Unmarked, _) => TrustRow::Unmarked,
        }
    }
    /// What the reading becomes when it is not the newest of the frame's generation: never trusted.
    pub fn stale(mut self) -> Self {
        if !matches!(self.case, TrustCase::NotRead { .. }) {
            self.case = TrustCase::NotRead { reason: TRUST_READ_STALE.into(), detail: None };
        }
        self
    }
    pub fn trust_level(&self) -> &'static str {
        if matches!(self.row(), TrustRow::MarkedTrusted | TrustRow::AppOn) { "trusted" } else { "untrusted" }
    }
    /// The `config.projects` value: exactly one entry, for the project root under the spelling Codex looks up
    /// first.
    pub fn projects(&self) -> Value {
        json!({ self.key.clone(): {"trust_level": self.trust_level()} })
    }
    /// The status (`threads[].level.projectTrust`): what was sent, the case, and its closed sentences. The matched
    /// key, folders and any raw detail are supplied text, kept in their own fields.
    pub fn status(&self) -> Value { self.status_for_write(true) }
    pub fn status_for_write(&self, written: bool) -> Value {
        let trusted_suffix = if written { TRUST_TRUSTED_SUFFIX } else { "). The App tried to send a trusted entry for the project root shown below." };
        let untrusted = if written { TRUST_UNTRUSTED_SENT } else { "The App tried to send an untrusted entry for the project root shown below." };
        let not_read = if written { TRUST_NOT_READ } else { "The App could not read the Codex settings it uses for this project, so it tried to send an untrusted entry for the project root shown below." };
        // The App's own sentences, in the manner of the closed ones: "sent" where the frame was written, "tried to
        // send" where it was not.
        let own = |sentence: String| if written { sentence } else { sentence.replace(" sent a", " tried to send a") };
        let matched_key = match &self.case { TrustCase::Trusted { key } | TrustCase::MarkedUntrusted { key } => Some(key), _ => None };
        let (case, lines): (&str, Vec<String>) = match (self.row(), &self.choice) {
            (TrustRow::SettingsNotRead, _) => ("not-read", vec![not_read.into(), untrusted.into()]),
            (TrustRow::ChoiceNotRead, _) => ("choice-not-read", vec![own(TRUST_CHOICE_NOT_READ.into())]),
            (TrustRow::FolderChanged, _) => ("folder-changed", vec![own(TRUST_FOLDER_CHANGED.into())]),
            (TrustRow::SwitchedOff, Some(AppTrust::OffByNewIdentity { .. })) => ("switched-off-new-identity", vec![own(TRUST_OFF_BY_NEW_IDENTITY.into())]),
            (TrustRow::MarkedUntrusted, _) => ("marked-untrusted", vec![TRUST_MARKED_UNTRUSTED.into(), untrusted.into()]),
            (TrustRow::SwitchedOff, Some(AppTrust::OffBySwitch { at })) => ("switched-off", vec![own(format!("{TRUST_OFF_BY_SWITCH_PREFIX}{at}{TRUST_OFF_BY_SWITCH_SUFFIX}"))]),
            (TrustRow::MarkedTrusted, _) => ("trusted", vec![format!("{TRUST_TRUSTED_PREFIX}{}{trusted_suffix}", self.read_at.as_deref().unwrap_or("an unknown time"))]),
            (TrustRow::AppOn, Some(AppTrust::OnBySwitch { at })) => ("app-on-by-switch", vec![own(format!("{TRUST_ON_BY_SWITCH_PREFIX}{at}{TRUST_ON_BY_SWITCH_SUFFIX}"))]),
            (TrustRow::AppOn, _) => ("app-on-by-setup", vec![own(TRUST_ON_BY_SETUP.into())]),
            (TrustRow::SwitchedOff | TrustRow::Unmarked, _) => ("unmarked", vec![untrusted.into()]),
        };
        let mut out = json!({"case": case, "sent": if written {json!(self.trust_level())} else {Value::Null}, "requested":self.trust_level(), "lines": lines, "projectRoot": self.root.to_string_lossy(),
            "sentKey": if written {json!(self.key)} else {Value::Null}, "requestedKey":self.key, "matchedKey": matched_key, "readAt": self.read_at, "standing": "Folders and keys are supplied text."});
        if let TrustCase::NotRead { reason, detail } = &self.case {
            out["reason"] = json!(reason);
            out["detail"] = match detail { Some(text) => json!({"text": text, "standing": NOT_THE_APPS_TEXT}), None => Value::Null };
        }
        // Present only for a frame whose folder is the App's project: what the App's own choice was.
        if let Some(choice) = &self.choice {
            out["appChoice"] = json!(choice.word());
            match choice {
                AppTrust::OnBySwitch { at } | AppTrust::OffBySwitch { at } | AppTrust::OffByNewIdentity { at } => out["appChoiceAt"] = json!(at),
                AppTrust::NotRead { detail } if !matches!(self.case, TrustCase::NotRead { .. }) => {
                    out["detail"] = match detail { Some(text) => json!({"text": text, "standing": NOT_THE_APPS_TEXT}), None => Value::Null };
                }
                _ => {}
            }
        }
        out
    }
}

// ---- A trusted project's own settings file that stops a start (DEL-01-01) ----

/// The error code and the fixed beginning of the message with which the pinned Codex refuses a start, resume or
/// fork whose configuration it could not load (observed at the pin; `app/supplier_checks/level/`, class
/// `TrustedProject`). Nothing more of the message is parsed.
pub const CONFIG_LOAD_ERROR_CODE: i64 = -32600;
pub const CONFIG_LOAD_ERROR_PREFIX: &str = "failed to load configuration:";
pub const PROJECT_SETTINGS_NOT_LOADED: &str = "This project's own Codex settings file could not be loaded, so Codex did not start the conversation.";
pub const PROJECT_SETTINGS_REMEDY: &str = "You can fix the file, or switch this project's trust off in Chirality, and start the conversation again.";
pub const PROJECT_SETTINGS_FILE_NAMED: &str = "The file Codex named:";
pub const PROJECT_SETTINGS_FILE_CANDIDATES: &str = "Codex did not name the file. The project's own settings files it may have read are among these:";
/// Where Codex's text names none of the project's own settings files as a whole path.
pub const PROJECT_SETTINGS_NOT_ATTRIBUTED: &str = "Codex could not load its settings, so it did not start the conversation. This project was sent as trusted, so one of its own settings files may be the cause.";
/// After the notice's first sentence, as the start's, resume's or fork's own error text.
pub const PROJECT_SETTINGS_SEE_TRUST: &str = "See the project's trust in Chirality for the file and Codex's reason.";

/// The App's account of a refused start, resume or fork that carried a trusted entry when Codex says it could not
/// load the configuration; None for any other reply. `error` is the reply's `error` member. It says only what is
/// known: attributed, where Codex's text contains as a whole path one of the project's own settings files (inside
/// the folders from the root Codex computes down to the conversation's folder, after resolving); otherwise not
/// attributed, with those files as candidates, and the ones in the repository's folders above the conversation's
/// folder named as such. No file outside those folders is ever named.
pub fn project_settings_refusal(trust: &TrustReading, error: &Value) -> Option<Value> {
    if trust.trust_level() != "trusted" || error["code"].as_i64() != Some(CONFIG_LOAD_ERROR_CODE) { return None; }
    let message = error["message"].as_str()?;
    if !message.starts_with(CONFIG_LOAD_ERROR_PREFIX) { return None; }
    let root = std::fs::canonicalize(&trust.root).ok();
    // A candidate is named only where it lies inside the root's folders after resolving: resolved through its
    // nearest part that exists.
    let resolved = |c: &Path| c.ancestors().find_map(|a| std::fs::canonicalize(a).ok().and_then(|r| Some(r.join(c.strip_prefix(a).ok()?))));
    let candidates: Vec<(PathBuf, PathBuf)> = project_settings_candidates(&trust.root, &trust.cwd).into_iter()
        .filter_map(|c| { let r = resolved(&c)?; root.as_ref().is_some_and(|root| r.starts_with(root)).then_some((c, r)) }).collect();
    let named = candidates.iter().rev().find(|(given, resolved)| whole_path_in(message, given) || whole_path_in(message, resolved));
    let text = |p: &Path| p.to_string_lossy().into_owned();
    let (lines, sentence, files) = match named {
        Some((file, _)) => (PROJECT_SETTINGS_NOT_LOADED, PROJECT_SETTINGS_FILE_NAMED, vec![text(file)]),
        None => (PROJECT_SETTINGS_NOT_ATTRIBUTED, PROJECT_SETTINGS_FILE_CANDIDATES, candidates.iter().map(|(c, _)| text(c)).collect()),
    };
    let own = trust.cwd.join(".codex").join("config.toml");
    let above: Vec<String> = if named.is_none() && trust.root != trust.cwd { candidates.iter().filter(|(c, _)| *c != own).map(|(c, _)| text(c)).collect() } else { vec![] };
    Some(json!({"lines": [lines], "attributed": named.is_some(), "fileSentence": sentence, "files": files, "filesAboveProject": above,
        "filesStanding": "Folders are supplied text.", "codexReason": {"text": message, "standing": NOT_THE_APPS_TEXT}, "remedy": PROJECT_SETTINGS_REMEDY,
        "projectRoot": trust.root.to_string_lossy()}))
}
/// `path` appears in `message` as a whole path: bounded on each side by the message's edge or a character that
/// cannot continue a path in Codex's text.
fn whole_path_in(message: &str, path: &Path) -> bool {
    let path = path.to_string_lossy();
    let boundary = |c: char| c.is_whitespace() || matches!(c, '"' | '\'' | '`' | ':' | ',' | ';' | '(' | ')' | '[' | ']' | '<' | '>' | '{' | '}');
    !path.is_empty() && message.match_indices(path.as_ref()).any(|(at, _)| {
        message[..at].chars().next_back().is_none_or(boundary) && message[at + path.len()..].chars().next().is_none_or(boundary)
    })
}

/// The project's `.codex/config.toml` files Codex may read for a conversation in `cwd`: one in each folder from the
/// project root down to `cwd`, in that order. `cwd` outside `root` gives the root's alone.
pub fn project_settings_candidates(root: &Path, cwd: &Path) -> Vec<PathBuf> {
    let mut out = vec![root.join(".codex").join("config.toml")];
    if let Ok(below) = cwd.strip_prefix(root) {
        let mut at = root.to_path_buf();
        for part in below.components() {
            at.push(part);
            out.push(at.join(".codex").join("config.toml"));
        }
    }
    out
}

/// The person's mark for `root` in a `config/read` result with layers: the user layers' `projects` table, looked
/// up by Codex's spellings in Codex's order, so a mark under either spelling is honoured. `Err` (a limited reading)
/// when the result carries no layers or no user layer, or when a user layer's settings cannot be read for the mark:
/// its `config` is not a table, its `projects` is present and not a table, or an entry or its `trust_level` under
/// one of the root's spellings is present and not one Codex accepts. An absent mark is `Unmarked`; an unusable one
/// is never taken for absent. Where the spellings carry conflicting marks, untrusted wins.
pub fn person_mark(result: &Value, root: &Path) -> Result<TrustCase, String> {
    let layers = result.get("layers").and_then(Value::as_array).ok_or(TRUST_READ_LIMITED)?;
    let user: Vec<&Value> = layers.iter().filter(|l| l["name"]["type"] == "user").collect();
    if user.is_empty() {
        return Err(TRUST_READ_LIMITED.into());
    }
    let mut marks = Vec::new();
    for key in trust_lookup_keys(root) {
        let mut mark = None;
        for layer in &user {
            let config = layer.get("config").and_then(Value::as_object).ok_or(TRUST_READ_LIMITED)?;
            let projects = match config.get("projects") {
                None => continue,
                Some(projects) => projects.as_object().ok_or(TRUST_READ_LIMITED)?,
            };
            let entry = match projects.get(&key) {
                None => continue,
                Some(entry) => entry.as_object().ok_or(TRUST_READ_LIMITED)?,
            };
            let level = match entry.get("trust_level") {
                None => continue,
                Some(level) => level.as_str().filter(|l| matches!(*l, "trusted" | "untrusted")).ok_or(TRUST_READ_LIMITED)?,
            };
            // The first user layer that marks this spelling, as before.
            if mark.is_none() { mark = Some(level); }
        }
        if let Some(level) = mark { marks.push((key, level)); }
    }
    if let Some((key, _)) = marks.iter().find(|(_, level)| *level == "untrusted") {
        return Ok(TrustCase::MarkedUntrusted { key: key.clone() });
    }
    Ok(match marks.into_iter().next() { Some((key, _)) => TrustCase::Trusted { key }, None => TrustCase::Unmarked })
}

/// The conversation a level was taken for when a frame was built.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Target {
    /// An existing conversation: a turn or a Continue names it.
    Conversation(String),
    /// The conversation a start creates; its id is learned from the reply.
    New,
    /// The conversation a fork creates from the named source; its id is learned from the reply.
    ForkOf(String),
}

/// Where a level in force comes from (`origin` in the status).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum LevelOrigin {
    /// The person's choice, recorded in the ledger.
    Chosen,
    /// The App's default, put in force by a complete launch read that found no valid choice for the default scope.
    /// Never written as a choice; a conversation association can retain this origin.
    AppDefault,
    /// The person's choice, held in memory only because the App's records could not be read or saved.
    SessionOnly,
    /// The choice is in force, but an attempted append was not confirmed.
    SaveUnconfirmed,
}
impl LevelOrigin {
    pub(crate) fn as_str(self) -> &'static str {
        match self { Self::Chosen => "chosen", Self::AppDefault => "app-default", Self::SessionOnly => "session-only", Self::SaveUnconfirmed => "save-unconfirmed" }
    }
}

/// The level bound to one request when its frame was built: what was checked, written and is recorded as sent.
/// Every later comparison for that request uses this value, never the level in force at that later moment.
#[derive(Clone, Debug, PartialEq)]
pub struct Bound {
    pub level: &'static Level,
    pub method: Method,
    /// Exactly `additions(level, method, trust)`: the fields the frame carries for the level, and on start, resume
    /// and fork its `config.projects` trust entry.
    pub fields: Map<String, Value>,
    /// The project trust sent on a start, resume or fork (None on a turn).
    pub trust: Option<TrustReading>,
    /// The Host's level revision when the frame was built; a frame built under an older revision is not written.
    pub revision: u64,
    pub target: Target,
    /// The ledger's `level_chosen` entry the level comes from, when the person's choice was recorded (None for a
    /// level set without a record, as the unit tests' Host is).
    pub chosen: Option<String>,
    pub origin: Option<LevelOrigin>,
    pub chosen_at: Option<String>,
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

/// Characters the App refuses anywhere in the path of a Codex home it starts Codex in.
pub const REFUSED_HOME_CHARACTERS: [char; 4] = ['$', '`', '"', '\\'];

/// The first component of `path`, as written or as resolved through links, that holds one of
/// `REFUSED_HOME_CHARACTERS`, with the character. Every component counts, the part above the App's own folders
/// included. A path that cannot be resolved is checked as written only.
pub fn refused_home_component(path: &Path) -> Option<(char, PathBuf)> {
    let resolved = std::fs::canonicalize(path).ok();
    for candidate in std::iter::once(path.to_path_buf()).chain(resolved) {
        let mut so_far = PathBuf::new();
        for component in candidate.components() {
            so_far.push(component.as_os_str());
            if let Component::Normal(name) = component {
                let name = name.to_string_lossy();
                if let Some(c) = REFUSED_HOME_CHARACTERS.iter().find(|c| name.contains(**c)) {
                    return Some((*c, so_far));
                }
            }
        }
    }
    None
}

/// The file in a Codex home that names where Codex runs commands. The App checks only whether an entry of this
/// name exists, by `symlink_metadata`; it never opens or reads it, because it may hold a credential.
pub const ENVIRONMENTS_FILE: &str = "environments.toml";

/// Why the App does not start Codex in a home (`levelStartRefusal` in the Host status).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum StartRefusal {
    /// An entry named `environments.toml` is in the home (`present`), or whether there is one could not be
    /// established (`present` false). Never opened.
    EnvironmentsFile { path: PathBuf, present: bool },
    /// A folder in the home's path, as written or as resolved, holds a refused character.
    HomePath { character: char, folder: PathBuf },
}

impl StartRefusal {
    /// The status value: `{refused: "environments-file", path, presence}` or
    /// `{refused: "home-path", character, folder}`.
    pub fn status(&self) -> Value {
        match self {
            Self::EnvironmentsFile { path, present } => json!({
                "refused": "environments-file", "path": path.to_string_lossy(),
                "presence": if *present { "present" } else { "not-established" }}),
            Self::HomePath { character, folder } => json!({
                "refused": "home-path", "character": character.to_string(), "folder": folder.to_string_lossy()}),
        }
    }
    /// The start refusal's reason, naming which check refused. Says what is refused and what the person can do.
    pub fn reason(&self) -> String {
        match self {
            Self::EnvironmentsFile { path, present: true } => format!(
                "Codex was not started: the App's Codex folder holds a file named environments.toml ({}). It can tell Codex to run commands somewhere other than this Mac, where the level you set does not apply. The App has not opened, moved or removed it. Remove it, then start Codex again.",
                path.display()),
            Self::EnvironmentsFile { path, present: false } => format!(
                "Codex was not started: whether the App's Codex folder holds a file named environments.toml ({}) could not be established. Make the folder readable, or remove the file if it is there, then start Codex again.",
                path.display()),
            Self::HomePath { character, folder } => format!(
                "Codex was not started: the folder {} in the path of the App's Codex folder contains the character {character}, which the App refuses in that path. Rename the folder so that its name contains none of $ ` \" \\, or use the App from a Mac account whose home folder's name contains none of them.",
                folder.display()),
        }
    }
}

/// The checks made before every Codex start in an App-owned home: the home's path (every component, as written
/// and as resolved), then the presence of `environments.toml`, by `symlink_metadata` alone.
pub fn start_refusal(home: &Path) -> Option<StartRefusal> {
    if let Some((character, folder)) = refused_home_component(home) {
        return Some(StartRefusal::HomePath { character, folder });
    }
    let path = home.join(ENVIRONMENTS_FILE);
    match std::fs::symlink_metadata(&path) {
        Ok(_) => Some(StartRefusal::EnvironmentsFile { path, present: true }),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
        Err(_) => Some(StartRefusal::EnvironmentsFile { path, present: false }),
    }
}

/// The sha-256 digest of the committed level table, as the ledger's `tableDigest` names it.
pub fn table_digest() -> &'static str {
    static DIGEST: OnceLock<String> = OnceLock::new();
    DIGEST.get_or_init(|| crate::util::sha256_hex(TABLE.as_bytes()))
}

/// A level's exact values as the ledger's `level_chosen.level` records them.
pub fn recorded_values(level: &Level) -> Value {
    json!({
        "id": level.id, "tableDigest": table_digest(), "approvalPolicy": level.approval_policy,
        "approvalsReviewer": "user", "sandbox": level.sandbox, "sandboxPolicy": level.sandbox_policy,
        "workspaceWrite": level.workspace_write,
    })
}

/// The level a recorded `level_chosen.level` names, accepted only when its id is in the table, its table digest
/// is this table's and every value equals that row exactly. Anything else is no level.
pub fn accept_recorded(values: &Value) -> Option<&'static Level> {
    let level = level(values["id"].as_str()?)?;
    (*values == recorded_values(level)).then_some(level)
}

/// The writable roots a level names beyond the project (none at the pin, but checked as any person-given root).
pub fn writable_roots(level: &Level) -> Vec<PathBuf> {
    level.workspace_write.as_ref().and_then(|w| w["writable_roots"].as_array())
        .map(|roots| roots.iter().filter_map(Value::as_str).map(PathBuf::from).collect())
        .unwrap_or_default()
}

/// Whether a project's path, as given or as resolved, holds a double quote. Every sandboxed level is refused for
/// such a project; the person can rename the folder, choose another, or choose full access.
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
    if !level.writes_in_the_project() {
        return None;
    }
    // The project (unless it is the no-project folder) and every further writable root the level names.
    let project_root = (!exempt.is_some_and(|e| same_folder(e, project))).then(|| project.to_path_buf());
    for folder in project_root.into_iter().chain(writable_roots(level)) {
        for (reaches, reserved) in protected {
            match crate::working_folder::may_overlap(&folder, reserved) {
                Ok(false) => {}
                Ok(true) | Err(()) => return Some(Refusal::EditsReachAppFolders { folder, reaches }),
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

/// What the unit tests' Host sends for `params` built for `method`: the params plus exactly the "edits" level, the
/// default a `cfg(test)` Host is made with (V4-AUT-06); a method that carries no level, the params unchanged. Test
/// material only.
#[cfg(test)]
pub(crate) fn with_test_level(params: &Value, method: &str) -> Value {
    let cwd = PathBuf::from(params["cwd"].as_str().unwrap_or("/invented"));
    let cwd = if cwd.is_relative() { PathBuf::from("/invented").join(cwd) } else { cwd };
    with_test_level_at(params, method, &cwd)
}

/// [`with_test_level`] for a conversation whose folder is `cwd` (the folder the test Host resolves for it: as sent,
/// else the conversation's, else the folder Codex was started in). Test material only.
#[cfg(test)]
pub(crate) fn with_test_level_at(params: &Value, method: &str, cwd: &Path) -> Value {
    match Method::of(method) {
        Some(Method::TurnStart) => expected_with_level(params, level("edits"), Method::TurnStart).expect("the test level merges"),
        Some(method) => {
            // The unit tests' Host makes no settings reading, so its trust entry is untrusted, for the project root of
            // the conversation's folder.
            let trust = TrustReading::not_read(cwd.to_path_buf(), TRUST_READ_FAILED, None);
            let mut out = params.clone();
            merge_fields(&mut out, &additions(level("edits").unwrap(), method, Some(&trust.projects()))).expect("the test level merges");
            out
        }
        None => params.clone(),
    }
}

#[cfg(test)]
#[path = "codex_level_tests.rs"]
mod tests;
