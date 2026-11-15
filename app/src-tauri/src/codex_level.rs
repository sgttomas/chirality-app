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
/// never written to the ledger; any recorded choice wins over it. An unreadable or limited ledger never takes it.
/// Tests replace it only through the `cfg(test)` setter `Host::set_app_default_for_test`; a shipped build has no
/// other route to it.
pub const DEFAULT_LEVEL: Option<&str> = Some("full");

/// The status's closed sentence for a level in force by the App's default.
pub const APP_DEFAULT_SENTENCE: &str = "The App's default level, not chosen by you. You can choose another level at any time.";
/// Where the status explains the App's default.
/// What allowing a command means at Supervised, at the pinned Codex (supplier_checks/level: the escalation rows and
/// `AskEachCommandInsideTheProject`; the features that would grant less are under development and off).
pub const SUPERVISED_ALLOWING: &str = "When a command needs your approval, Codex asks. If you allow it, the command can run outside the sandbox, with your account's access to all your files and to the network; Codex cannot run it limited to this project. Your own rules and hooks can allow or refuse a command without asking you.";
pub const APP_DEFAULT_EXPLAINED: &str = "The App's default level is full access: commands run with no sandbox, with your account's access to your files and the network, including the App's own records and settings. You can choose another level at any time.";
/// The status's closed sentence for a level chosen while the App's records could not be read or saved.
/// Where the App's record of the level is missing although this home has been used (V4-AUT-06): no default is named.
pub const RECORD_MISSING_SENTENCE: &str = "The App's record of your permission level is missing. Choose a level to continue. A missing record can mean that a command removed it.";
/// The name Codex gives the state database it creates in its home when it first starts there (state/src/sqlite.rs
/// at rust-v0.167.0). The App never creates it.
pub const CODEX_STATE_NAME: &str = "state_5.sqlite";
/// Whether this home holds state from an earlier Codex start: presence of [`CODEX_STATE_NAME`] directly in it, by
/// `symlink_metadata` only. Nothing is opened, nothing is followed and no other folder is looked at.
pub fn home_has_codex_state(codex_home: &Path) -> bool {
    std::fs::symlink_metadata(codex_home.join(CODEX_STATE_NAME)).is_ok()
}
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
pub const TRUST_TRUSTED_SUFFIX: &str = "). Its own Codex folder (.codex) applies to conversations here.";
pub const TRUST_NOT_USED: &str = "This project's own Codex folder (.codex) is not used in the App.";
pub const TRUST_MARKED_UNTRUSTED: &str = "This project is marked untrusted in the Codex settings the App uses.";
pub const TRUST_NOT_READ: &str = "The App could not read the Codex settings it uses for this project, so its own Codex folder (.codex) is not used here, even if those settings mark it trusted.";
/// The reasons a reading is not whole and current (`TrustCase::NotRead`), in the App's own words.
pub const TRUST_READ_FAILED: &str = "The App's reading of the Codex settings it uses did not complete.";
pub const TRUST_READ_LIMITED: &str = "The App's reading of the Codex settings it uses did not include the settings files.";
pub const TRUST_READ_TIMED_OUT: &str = "The App's reading of the Codex settings it uses did not complete in time.";
pub const TRUST_READ_STALE: &str = "The App's reading of the Codex settings it uses was no longer the latest when the request was built.";

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
}

impl TrustReading {
    /// A reading that cannot be relied on: the entry is sent as untrusted.
    pub fn not_read(cwd: PathBuf, reason: &str, detail: Option<String>) -> Self {
        let root = project_root(&cwd);
        let key = trust_lookup_keys(&root).remove(0);
        TrustReading { cwd, root, key, case: TrustCase::NotRead { reason: reason.into(), detail }, generation: None, request_ref: None, read_at: None }
    }
    /// What the reading becomes when it is not the newest of the frame's generation: never trusted.
    pub fn stale(mut self) -> Self {
        if !matches!(self.case, TrustCase::NotRead { .. }) {
            self.case = TrustCase::NotRead { reason: TRUST_READ_STALE.into(), detail: None };
        }
        self
    }
    pub fn trust_level(&self) -> &'static str {
        if matches!(self.case, TrustCase::Trusted { .. }) { "trusted" } else { "untrusted" }
    }
    /// The `config.projects` value: exactly one entry, for the project root under the spelling Codex looks up
    /// first.
    pub fn projects(&self) -> Value {
        json!({ self.key.clone(): {"trust_level": self.trust_level()} })
    }
    /// The status (`threads[].level.projectTrust`): what was sent, the case, and its closed sentences. The matched
    /// key, folders and any raw detail are supplied text, kept in their own fields.
    pub fn status(&self) -> Value {
        let (case, lines, matched): (&str, Vec<String>, Option<&String>) = match &self.case {
            TrustCase::Trusted { key } => ("trusted", vec![format!("{TRUST_TRUSTED_PREFIX}{}{TRUST_TRUSTED_SUFFIX}", self.read_at.as_deref().unwrap_or("an unknown time"))], Some(key)),
            TrustCase::MarkedUntrusted { key } => ("marked-untrusted", vec![TRUST_MARKED_UNTRUSTED.into(), TRUST_NOT_USED.into()], Some(key)),
            TrustCase::Unmarked => ("not-used", vec![TRUST_NOT_USED.into()], None),
            TrustCase::NotRead { .. } => ("not-read", vec![TRUST_NOT_READ.into(), TRUST_NOT_USED.into()], None),
        };
        let mut out = json!({"case": case, "sent": self.trust_level(), "lines": lines, "projectRoot": self.root.to_string_lossy(),
            "sentKey": self.key, "matchedKey": matched, "readAt": self.read_at, "standing": "Folders and keys are supplied text."});
        if let TrustCase::NotRead { reason, detail } = &self.case {
            out["reason"] = json!(reason);
            out["detail"] = match detail { Some(text) => json!({"text": text, "standing": NOT_THE_APPS_TEXT}), None => Value::Null };
        }
        out
    }
}

/// The person's mark for `root` in a `config/read` result with layers: the user layers' `projects` table, looked
/// up by Codex's spellings in Codex's order, so a mark under either spelling is honoured. `Err` when the result
/// carries no layers or no user layer (a limited reading).
pub fn person_mark(result: &Value, root: &Path) -> Result<TrustCase, String> {
    let layers = result.get("layers").and_then(Value::as_array).ok_or(TRUST_READ_LIMITED)?;
    let user: Vec<&Value> = layers.iter().filter(|l| l["name"]["type"] == "user").collect();
    if user.is_empty() {
        return Err(TRUST_READ_LIMITED.into());
    }
    for key in trust_lookup_keys(root) {
        for layer in &user {
            match layer["config"]["projects"][&key]["trust_level"].as_str() {
                Some("trusted") => return Ok(TrustCase::Trusted { key }),
                Some("untrusted") => return Ok(TrustCase::MarkedUntrusted { key }),
                _ => {}
            }
        }
    }
    Ok(TrustCase::Unmarked)
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
