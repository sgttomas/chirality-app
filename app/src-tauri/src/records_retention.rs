//! RS §13.8 / U-STORE-1: no expiry, native administrative acts, legal hold
//! and verified-export disposition. Administration survives the disposed subtree.
use crate::{records_store, storage, util};
use serde_json::{json, Value};
use std::io::Read;
use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
use std::path::{Path, PathBuf};

#[path = "records_administration.rs"]
mod administration;
pub(crate) use administration::{
    plan_package_restore, restore_package_history, resume_package_restore, validate_package_snapshot,
    AdministrationRestore, PackageAdministration,
};

const FORMAT: &str = "chirality.records-administration";
// A complete event visible after uncertain publication is still not a durable
// receipt in this process. After a relaunch it either survived, or the original
// disposal remains incomplete. Never discard that original act.
static UNCERTAIN_COMPLETIONS: std::sync::LazyLock<
    std::sync::Mutex<std::collections::HashSet<PathBuf>>,
> = std::sync::LazyLock::new(|| std::sync::Mutex::new(std::collections::HashSet::new()));

fn validate_event(event: &Value) -> Result<(), String> {
    static VALIDATOR: std::sync::OnceLock<Result<jsonschema::Validator, String>> =
        std::sync::OnceLock::new();
    let v = VALIDATOR
        .get_or_init(|| {
            serde_json::from_str::<Value>(include_str!(
                "../resources/runtime_core/records-administration.entry.schema.json"
            ))
            .map_err(|e| e.to_string())
            .and_then(|s| {
                jsonschema::options()
                    .offline()
                    .build(&s)
                    .map_err(|e| e.to_string())
            })
        })
        .as_ref()
        .map_err(Clone::clone)?;
    v.validate(event).map_err(|e| {
        format!(
            "administrative event invalid; no disposition: {} at {}",
            e.masked(),
            e.instance_path()
        )
    })
}

#[cfg(test)]
thread_local! {static AFTER_ADMIN_METADATA:std::cell::RefCell<Option<Box<dyn FnOnce(&Path)>>> = const{std::cell::RefCell::new(None)};}
pub(crate) fn read_plain(path: &Path) -> Result<Vec<u8>, String> {
    storage::check_path(path)?;
    let before = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !before.is_file() || before.nlink() != 1 {
        return Err("administrative history has a non-plain member; no disposition".into());
    }
    let stamp = crate::records_index::Stamp::of(&before);
    #[cfg(test)]
    if let Some(hook) = AFTER_ADMIN_METADATA.with(|h| h.borrow_mut().take()) {
        hook(path);
    }
    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
        .map_err(|e| e.to_string())?;
    let opened = file.metadata().map_err(|e| e.to_string())?;
    if !opened.is_file() || opened.nlink() != 1 || crate::records_index::Stamp::of(&opened) != stamp
    {
        return Err("administrative member changed while opening; no disposition".into());
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    storage::check_path(path)?;
    if crate::records_index::Stamp::of(&file.metadata().map_err(|e| e.to_string())?) != stamp
        || crate::records_index::Stamp::of(
            &std::fs::symlink_metadata(path).map_err(|e| e.to_string())?,
        ) != stamp
    {
        return Err("administrative member changed while reading; no disposition".into());
    }
    Ok(bytes)
}
fn control(dir: &Path) -> Result<PathBuf, String> {
    let key = dir.file_name().ok_or("project subtree has no key")?;
    let store = dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project subtree has no store")?;
    Ok(store.join("administration").join(key))
}
fn gate(dir: &Path) -> Result<PathBuf, String> {
    Ok(control(dir)?.join(".admission.lock"))
}

#[derive(Clone, Debug, Default)]
struct State {
    closed: bool,
    hold: bool,
    disposition: Option<Value>,
    completed: bool,
    completion_uncertain: bool,
    sequence: u64,
    head: Option<String>,
}
impl State {
    fn view(&self) -> Value {
        json!({"closed":self.closed,"legalHold":self.hold,"disposition":if self.completed && self.completion_uncertain {"completion durability uncertain"} else if self.completed {"disposed"} else if self.disposition.is_some() {"disposal incomplete"} else {"kept"},"sequence":self.sequence,"head":self.head,"disposal":self.disposition})
    }
    fn writable(&self) -> Result<(), String> {
        if self.disposition.is_some() {
            return Err("project records are disposed or disposal is incomplete; no recording or reassociation".into());
        }
        if self.closed {
            return Err(
                "project is closed; reopen it through the native records control before recording"
                    .into(),
            );
        }
        Ok(())
    }
}
// Accepted prefixes remain known even when a later read fails. This detects
// removed/replaced links in this App process; unsigned cold valid-tail removal
// is a stated limit, rather than an inference that a hold was released.
static ACCEPTED_HEADS: std::sync::LazyLock<
    std::sync::Mutex<std::collections::HashMap<PathBuf, (u64, String)>>,
> = std::sync::LazyLock::new(|| std::sync::Mutex::new(std::collections::HashMap::new()));
fn remember_prefix(dir: &Path, sequence: u64, head: Option<&str>) -> Result<(), String> {
    let mut known = ACCEPTED_HEADS.lock().unwrap_or_else(|p| p.into_inner());
    if let Some((seen, hash)) = known.get(dir) {
        if sequence == *seen && head != Some(hash.as_str()) {
            return Err("administrative history previously observed prefix changed; no recording or disposition".into());
        }
    }
    if sequence > 0 && known.get(dir).is_none_or(|(seen, _)| sequence > *seen) {
        known.insert(
            dir.to_path_buf(),
            (
                sequence,
                head.ok_or("administrative head missing")?.to_owned(),
            ),
        );
    }
    Ok(())
}
fn require_known_tail(dir: &Path, sequence: u64) -> Result<(), String> {
    if ACCEPTED_HEADS
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .is_some_and(|(seen, _)| sequence < *seen)
    {
        return Err(
            "administrative history previously observed links removed; restore the original history from verified evidence before retrying; no recording or disposition"
                .into(),
        );
    }
    Ok(())
}
fn history_marker(dir: &Path) -> Result<PathBuf, String> {
    Ok(control(dir)?.join("history-started.json"))
}
fn marker_head(dir: &Path) -> Result<Option<String>, String> {
    let path = history_marker(dir)?;
    match std::fs::symlink_metadata(&path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(format!("administrative history marker unavailable: {e}")),
        Ok(_) => {
            let marker: Value = serde_json::from_slice(&read_plain(&path)?)
                .map_err(|e| format!("administrative history marker unreadable: {e}"))?;
            if marker["format"] != "chirality.records-administration-started"
                || marker["formatVersion"] != "0.1"
                || marker["projectKey"] != dir.file_name().unwrap().to_string_lossy().as_ref()
                || marker["firstHead"]
                    .as_str()
                    .is_none_or(|h| h.len() != 64 || !h.bytes().all(|b| b.is_ascii_hexdigit()))
            {
                return Err(
                    "administrative history marker invalid; no recording or disposition".into(),
                );
            }
            Ok(Some(marker["firstHead"].as_str().unwrap().to_owned()))
        }
    }
}
fn ensure_history_marker(dir: &Path) -> Result<(), String> {
    let first = control(dir)?.join("events/00000000000000000001.json");
    if first.exists() {
        let head = util::sha256_hex(&read_plain(&first)?);
        if let Some(expected) = marker_head(dir)? {
            if expected != head {
                return Err("administrative first event changed since history began".into());
            }
        } else {
            storage::create_json(
                &history_marker(dir)?,
                &json!({"format":"chirality.records-administration-started","formatVersion":"0.1","projectKey":dir.file_name().unwrap().to_string_lossy(),"firstHead":head}),
            )?;
        }
    }
    Ok(())
}
// Shared pure transition validation. Filesystem custody, first-event markers and
// remembered local prefixes remain the responsibility of the caller.
fn advance_event(key: &str, project_id: Option<&str>, name: &str, bytes: &[u8], out: &mut State) -> Result<(), String> {
    let event: Value = crate::records_package::parse_json_unique(bytes)
        .map_err(|e| format!("administrative history unreadable; no disposition: {e}"))?;
    validate_event(&event)?;
    let next = out
        .sequence
        .checked_add(1)
        .ok_or("administrative sequence exhausted")?;
    if Some(name) != Some(format!("{next:020}.json").as_str())
        || event["format"] != FORMAT
        || event["formatVersion"] != "0.1"
        || event["sequence"].as_u64() != Some(next)
        || event["previous"] != json!(out.head)
        || event["projectKey"] != key
        || event["projectId"].as_str().is_none_or(|id| {
            storage::key(id) != key
        })
    {
        return Err(
            "administrative history identity/order is inconsistent; no disposition".into(),
        );
    }
    if project_id.is_some_and(|id| event["projectId"] != id || event["scope"]["projectId"] != id) {
        return Err("administrative event project identity disagrees with snapshot".into());
    }
    let native = || -> Result<(), String> {
        if event["actorKind"] != "person"
            || event["actor"]["identityVerified"] != false
            || event["recorder"] != "App interface"
            || !event["context"].is_object()
        {
            return Err(
                "administrative act has no native person/context evidence; no disposition"
                    .into(),
            );
        }
        Ok(())
    };
    match event["action"].as_str() {
        Some("close") if !out.closed && out.disposition.is_none() => {
            native()?;
            out.closed = true;
        }
        Some("reopen") if out.closed && out.disposition.is_none() => {
            native()?;
            out.closed = false;
        }
        Some("set-hold") if !out.hold && !out.completed => {
            native()?;
            out.hold = true;
        }
        Some("release-hold") if out.hold && !out.completed => {
            native()?;
            out.hold = false;
        }
        Some("dispose") if out.closed && !out.hold && out.disposition.is_none() => {
            native()?;
            if !event["export"]["folder"].is_string()
                || !event["export"]["identity"].is_string()
                || !event["payload"].is_object()
            {
                return Err(
                    "disposal has no bound verified payload/export; no disposition".into(),
                );
            }
            out.disposition = Some(event.clone());
        }
        Some("disposal-completed")
            if out.disposition.is_some()
                && !out.completed
                && event["recorder"] == "App"
                && event["originalAct"] == out.disposition.as_ref().unwrap()["sequence"] =>
        {
            out.completed = true
        }
        _ => return Err(
            "administrative history has an unknown or conflicting transition; no disposition"
                .into(),
        ),
    }
    if event["stateAfter"]
        != json!({"closed":out.closed,"legalHold":out.hold,"disposition":if out.completed {"disposed"} else if out.disposition.is_some() {"disposal incomplete"} else {"kept"}})
    {
        return Err("administrative state disagrees with its act; no disposition".into());
    }
    out.sequence = next;
    out.head = Some(util::sha256_hex(bytes));
    Ok(())
}

fn state(dir: &Path) -> Result<State, String> {
    records_store::package::require_complete(dir)?;
    history_state(dir)
}

/// Administration survives payload disposal. Package-control readers use only
/// this validated ledger fact to distinguish lawful receipt removal from loss;
/// it grants no payload read/write permission and bypasses no history checks.
pub(crate) fn disposition_started(dir: &Path) -> Result<bool, String> {
    Ok(history_state(dir)?.disposition.is_some())
}

fn history_state(dir: &Path) -> Result<State, String> {
    let folder = control(dir)?.join("events");
    storage::check_path(&folder)?;
    let first_head = marker_head(dir)?;
    let mut paths = match std::fs::read_dir(&folder) {
        Ok(entries) => entries
            .map(|e| e.map(|e| e.path()).map_err(|e| e.to_string()))
            .collect::<Result<Vec<_>, _>>()?,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Vec::new(),
        Err(e) => {
            return Err(format!(
                "administrative history unavailable; no disposition: {e}"
            ))
        }
    };
    paths.sort();
    if paths.is_empty() && first_head.is_some() {
        return Err("administrative history previously started but its events are absent; restore the original history from verified evidence before retrying; no recording or disposition".into());
    }
    let mut out = State::default();
    for path in paths {
        storage::check_path(&path)?;
        let bytes = read_plain(&path)?;
        let name = path.file_name().and_then(|n| n.to_str()).ok_or("administrative event name is not UTF-8")?;
        advance_event(dir.file_name().unwrap().to_string_lossy().as_ref(), None, name, &bytes, &mut out)?;
        let next = out.sequence;
        if next == 1
            && first_head
                .as_ref()
                .is_some_and(|expected| Some(expected) != out.head.as_ref())
        {
            return Err("administrative first event differs from surviving history marker; no recording or disposition".into());
        }
        remember_prefix(dir, out.sequence, out.head.as_deref())?;
    }
    require_known_tail(dir, out.sequence)?;
    out.completion_uncertain = out.completed
        && UNCERTAIN_COMPLETIONS
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .contains(dir);
    Ok(out)
}

/// Permission is checked after taking the stable lock. A path resolved before
/// closure can never recreate the subtree after disposal, even in another process.
pub(crate) fn write_path(path: &Path) -> Result<Option<storage::Ownership>, String> {
    let Some(dir) = records_store::configured_project_dir(path) else {
        return Ok(None);
    };
    if records_store::package::owns(&dir) { return Ok(None); }
    let guard = storage::lock_shared(&gate(&dir)?)?;
    state(&dir)?.writable()?;
    records_store::package::check_write_binding(&dir)?;
    Ok(Some(guard))
}
pub(crate) fn read_path(path: &Path) -> Result<Option<storage::Ownership>, String> {
    let Some(dir) = records_store::configured_project_dir(path) else {
        return Ok(None);
    };
    if records_store::package::owns(&dir) { return Ok(None); }
    let guard = storage::lock_shared(&gate(&dir)?)?;
    if state(&dir)?.disposition.is_some() {
        return Err(
            "project records disposed or disposal incomplete; no store payload available".into(),
        );
    }
    Ok(Some(guard))
}
pub(crate) fn check_write(dir: &Path) -> Result<(), String> {
    state(dir)?.writable()
}
pub(crate) fn terminal(dir: &Path) -> Result<bool, String> {
    Ok(state(dir)?.disposition.is_some())
}
pub(crate) fn view(dir: &Path) -> Value {
    match state(dir) {
        Ok(s) => s.view(),
        Err(e) => json!({"disposition":"unavailable","limit":e}),
    }
}

/// Held for the supplier's lifetime, outside the deletable subtree. Closing
/// requires every supplier using this project's identity to have ended.
pub(crate) fn activity(project: &Path) -> Result<Option<storage::Ownership>, String> {
    // An absent cwd cannot host a supplier; preserve the host's own spawn
    // failure (and generation/counter evidence), without minting an identity.
    if !project.exists() {
        return Ok(None);
    }
    if let Err(error) = records_store::current() {
        if std::fs::symlink_metadata(project.join(records_store::PROJECT_LINK)).is_ok()
            || records_store::known_project_root(project)
        {
            return Err(format!(
                "project retention unavailable; no Codex start: {error}"
            ));
        }
        return Ok(None);
    }
    // App startup attaches its explicit project before any supplier starts.
    // A no-project supplier (whose cwd is only a temporary folder) must not
    // mint a project or write into its cwd merely to acquire a lifetime lease.
    let attachment = records_store::attach(project, false)?;
    if attachment.dir.is_none() && attachment.refusal.is_none() {
        return Ok(None);
    }
    let dir = attachment.dir.ok_or_else(|| {
        attachment
            .refusal
            .unwrap_or_else(|| "project identity unavailable".into())
    })?;
    let _admission = write_path(&dir)?.ok_or("project admission unavailable")?;
    Ok(Some(storage::lock_shared(
        &control(&dir)?.join(".activity.lock"),
    )?))
}
fn idle(dir: &Path) -> Result<storage::Ownership, String> {
    storage::try_lock_exclusive(&control(dir)?.join(".activity.lock"))?.ok_or_else(||"Project activity is still held by a supplier, workflow run or pending native capture/recording in this or another App process; stop Codex and use the owning run/act record continuation to settle pending evidence before closing or disposing".into())
}
fn attachment(project: &Path) -> Result<(records_store::Attachment, PathBuf), String> {
    let attachment = records_store::attach(project, false)?;
    if attachment.refusal.is_some() {
        return Err(attachment.refusal.clone().unwrap());
    }
    if !attachment.limits.is_empty() {
        return Err("resolve the project identity limits before a retention action".into());
    }
    let dir = attachment
        .dir
        .clone()
        .ok_or("project has no attached store identity")?;
    Ok((attachment, dir))
}
fn physical(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    let m = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !m.is_dir() {
        return Err("project/store payload folder is not a directory".into());
    }
    Ok(json!({"device":m.dev(),"inode":m.ino()}))
}
fn context(
    project: &Path,
    dir: &Path,
    action: &str,
    bag: Option<&Path>,
    actor: &Value,
    observed: &Value,
) -> Result<Value, String> {
    let s = state(dir)?;
    match action {
        "close" if !s.closed && s.disposition.is_none() => {},
        "reopen" if s.closed && s.disposition.is_none() => {},
        "set-hold" if !s.hold && !s.completed => {},
        "release-hold" if s.hold && !s.completed => {},
        "dispose" if s.closed && !s.hold && s.disposition.is_none() => {},
        "resume-disposal" if s.closed && !s.hold && s.disposition.is_some() && (!s.completed || s.completion_uncertain) => {},
        _ => return Err("retention action is unavailable for the current project state (legal hold blocks disposal)".into()),
    }
    let attachment = records_store::attach(project, false)?;
    if attachment.refusal.is_some()
        || !attachment.limits.is_empty()
        || attachment.dir.as_deref() != Some(dir)
    {
        return Err("project identity changed or has limits; review again".into());
    }
    let store = dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project store absent")?;
    let store_bytes = read_plain(&store.join("store.json"))?;
    let store_identity: Value = serde_json::from_slice(&store_bytes).map_err(|e| e.to_string())?;
    if store_identity["storeId"] != records_store::status(None)["storeId"] {
        return Err("store identity changed since it was opened; no retention act".into());
    }
    let link = read_plain(&project.join(records_store::PROJECT_LINK))?;
    let mut out = json!({"storeFolder":physical(store)?,"storeIdentityBytes":util::sha256_hex(&store_bytes),"projectLinkBytes":util::sha256_hex(&link),"action":action,"projectId":attachment.project,"projectRoot":project,"projectFolder":physical(project)?,"store":dir.parent().and_then(Path::parent),"storeId":records_store::status(None)["storeId"],"projectKey":dir.file_name().unwrap().to_string_lossy(),"state":s.view(),"actor":actor,"observed":observed});
    if matches!(action, "close" | "dispose" | "resume-disposal") {
        let _idle = idle(dir)?;
    }
    if action == "dispose" {
        let folder =
            bag.ok_or("choose a verified export of the current complete project payload first")?;
        if control(dir)?.join("removal").exists() {
            return Err("unexplained disposal staging is present; no new disposal act".into());
        }
        out["payloadFolder"] = physical(dir)?;
        out["export"] = crate::records_export::matches_current(dir, folder, false)?;
    }
    if action == "resume-disposal" {
        let original = s.disposition.as_ref().unwrap();
        let folder = Path::new(
            original["export"]["folder"]
                .as_str()
                .ok_or("original export path absent")?,
        );
        if dir.exists() && physical(dir)? != original["context"]["payloadFolder"] {
            return Err(
                "original project payload folder was replaced; nothing more disposed".into(),
            );
        }
        let checked = crate::records_export::matches_current(dir, folder, true)?;
        if checked["identity"] != original["export"]["identity"] {
            return Err("original verified export has changed; nothing more disposed".into());
        }
        out["stagedPayload"] =
            crate::records_export::staged_payload(&control(dir)?.join("removal"), folder)?;
        out["export"] = checked;
    }
    Ok(out)
}

/// Exact UTF-8 event bytes (including whitespace/newlines), reversibly encoded
/// in one protected BagIt tag. Controls and temporary files confer no act.
pub(crate) fn export_snapshot(
    dir: &Path,
    project_id: &str,
    before: Option<u64>,
) -> Result<Value, String> {
    let s = state(dir)?;
    let folder = control(dir)?.join("events");
    let mut events = std::collections::BTreeMap::new();
    if folder.exists() {
        for entry in std::fs::read_dir(&folder).map_err(|e| e.to_string())? {
            let path = entry.map_err(|e| e.to_string())?.path();
            let name = path
                .file_name()
                .and_then(|n| n.to_str())
                .ok_or("administrative event name unreadable")?
                .to_owned();
            let number = name
                .strip_suffix(".json")
                .and_then(|n| n.parse::<u64>().ok())
                .ok_or("administrative event name invalid")?;
            if before.is_some_and(|last| number > last) {
                continue;
            }
            let bytes = read_plain(&path)?;
            events.insert(name, String::from_utf8(bytes).map_err(|e| e.to_string())?);
        }
    }
    Ok(
        json!({"format":"chirality.records-administration-snapshot","formatVersion":"0.1","projectId":project_id,"projectKey":dir.file_name().unwrap().to_string_lossy(),"events":events,"standing":"Exact bytes of prior administrative acts; unsigned, identity not verified","sequence":before.unwrap_or(s.sequence)}),
    )
}

/// The original plan stays in Rust across the native question; webview data
/// cannot author attribution, closure evidence, export verification or an act.
pub(crate) struct Plan {
    project: PathBuf,
    dir: PathBuf,
    action: String,
    bag: Option<PathBuf>,
    pub(crate) context: Value,
}
pub(crate) fn prepare(
    project: &Path,
    action: &str,
    bag: Option<&Path>,
    actor: &Value,
    observed: &Value,
) -> Result<Plan, String> {
    let (_, dir) = attachment(project)?;
    let _admission = storage::lock_shared(&gate(&dir)?)?;
    let frozen = context(project, &dir, action, bag, actor, observed)?;
    Ok(Plan {
        project: project.into(),
        dir,
        action: action.into(),
        bag: bag.map(Path::to_path_buf),
        context: frozen,
    })
}
pub(crate) fn statement(
    plan: &Plan,
) -> Result<crate::act_control::native_statement::NativeStatement, String> {
    let purpose=match plan.action.as_str() {
        "close"=>"Close this project to all new App recording and Codex starts?",
        "reopen"=>"Reopen this project for App recording and Codex starts?",
        "set-hold"=>"Set a legal hold blocking disposal of this project's records?",
        "release-hold"=>"Release this project's legal hold? Disposal becomes available after closure and a verified export.",
        "dispose"=>"Permanently dispose of this closed project's App store payload? The verified export and administrative history survive; project and library files remain.",
        "resume-disposal"=>"Finish the previously confirmed disposal? Only unchanged remaining members of the original verified export may be removed.",
        _=>return Err("unknown administrative act".into()),
    };
    let full=format!("{purpose}\n\nProject: {}\nRoot: {}\nClosed: {}\nLegal hold: {}\nActor (identity not verified): {}\n\nFrozen context:\n{}",plan.context["projectId"],plan.project.display(),plan.context["state"]["closed"],plan.context["state"]["legalHold"],crate::act_control::native_statement::actor_line(&plan.context["actor"]),serde_json::to_string_pretty(&plan.context).map_err(|e|e.to_string())?);
    crate::act_control::native_statement::whole_or_in_app(
        "records retention",
        "records administration",
        full,
        &plan.context,
        |digest| {
            format!("{purpose}\n\nThe complete project, actor, closure, hold and verified byte identity context is shown in the App under this confirmation. sha-256: {digest}\nNothing changes if it changed while this question was open.")
        },
    )
}
fn event(
    dir: &Path,
    s: &State,
    action: &str,
    actor: Option<&Value>,
    context: &Value,
) -> Result<Value, String> {
    let seq = s
        .sequence
        .checked_add(1)
        .ok_or("administrative sequence exhausted")?;
    let mut v = json!({"format":FORMAT,"formatVersion":"0.1","sequence":seq,"previous":s.head,"projectKey":dir.file_name().unwrap().to_string_lossy(),"projectId":context["projectId"],"at":util::now_rfc3339(),"action":action,"purpose":action,"scope":{"projectId":context["projectId"],"projectRoot":context["projectRoot"],"storeId":context["storeId"]},"context":context,"recorder":if actor.is_some(){"App interface"}else{"App"}});
    if let Some(actor) = actor {
        v["actor"] = actor.clone();
        v["actorKind"] = json!("person");
    }
    let closed = if action == "close" {
        true
    } else if action == "reopen" {
        false
    } else {
        s.closed
    };
    let hold = if action == "set-hold" {
        true
    } else if action == "release-hold" {
        false
    } else {
        s.hold
    };
    v["stateAfter"] = json!({"closed":closed,"legalHold":hold,"disposition":if action=="disposal-completed" {"disposed"}else if action=="dispose" || s.disposition.is_some() {"disposal incomplete"}else{"kept"}});
    if action == "dispose" {
        v["export"] = context["export"].clone();
        v["payload"] = context["export"]["payload"].clone();
    }
    if action == "disposal-completed" {
        v["originalAct"] = s
            .disposition
            .as_ref()
            .ok_or("original disposal act missing")?["sequence"]
            .clone();
    }
    validate_event(&v)?;
    let path = control(dir)?.join("events").join(format!("{seq:020}.json"));
    #[cfg(test)]
    if FAIL_ADMIN_PUBLICATION.with(|flag| flag.get())
        || (action == "disposal-completed" && FAIL_COMPLETION_PUBLICATION.with(|flag| flag.get()))
    {
        storage::fail_directory_for_test(Some(control(dir)?.join("events")));
    }
    let published = storage::create_json(&path, &v);
    // A visible event whose fsync failed is still an observed native fact: keep
    // its accepted prefix before reporting uncertainty, never guess it away.
    let _ = state(dir);
    let marker = ensure_history_marker(dir);
    published.and(marker).and_then(|()|durable_history(dir)).map_err(|e|format!("administrative publication not confirmed durable; re-read its actual state before acting: {e}"))?;
    Ok(v)
}
fn durable_history(dir: &Path) -> Result<(), String> {
    ensure_history_marker(dir)?;
    if history_marker(dir)?.exists() {
        storage::sync_publication(&history_marker(dir)?)?;
    }
    let folder = control(dir)?.join("events");
    if folder.exists() {
        for e in std::fs::read_dir(folder).map_err(|e| e.to_string())? {
            storage::sync_publication(&e.map_err(|e| e.to_string())?.path())?;
        }
    }
    let control = control(dir)?;
    // Existing-but-unflushed directories can survive a previous failed attempt.
    // Re-establish every administrative link, not just each event's parent.
    for folder in [
        control.clone(),
        control
            .parent()
            .ok_or("administration has no parent")?
            .to_path_buf(),
        dir.parent()
            .and_then(Path::parent)
            .ok_or("store absent")?
            .to_path_buf(),
    ] {
        storage::sync_dir(&folder)?;
    }
    Ok(())
}
#[cfg(test)]
thread_local! { static AFTER_DISPOSAL_ACT:std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const {std::cell::RefCell::new(None)}; static FAIL_COMPLETION_PUBLICATION: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; static FAIL_ADMIN_PUBLICATION: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; static FAIL_REMOVE: std::cell::Cell<bool> = const { std::cell::Cell::new(false) }; }
#[cfg(test)]
pub(crate) fn fail_remove_for_test(fail: bool) {
    FAIL_REMOVE.with(|v| v.set(fail));
}

/// Called only following the original native person's choice, with current
/// host attribution observed again. No caller-selected act/actor DTO crosses IPC.
pub(crate) fn apply(plan: Plan, actor: &Value, observed: &Value) -> Result<Value, String> {
    let _admission = storage::lock(&gate(&plan.dir)?)?;
    let current = context(
        &plan.project,
        &plan.dir,
        &plan.action,
        plan.bag.as_deref(),
        actor,
        observed,
    )?;
    let _idle = if matches!(
        plan.action.as_str(),
        "close" | "dispose" | "resume-disposal"
    ) {
        Some(idle(&plan.dir)?)
    } else {
        None
    };
    if current != plan.context {
        return Err("project, actor, closure, hold, export or payload changed during native confirmation; nothing changed; review again".into());
    }
    durable_history(&plan.dir)?;
    let mut s = state(&plan.dir)?;
    if plan.action == "resume-disposal" && s.completed {
        if plan.dir.exists() {
            return Err(
                "completed disposal's subtree reappeared; no second removal performed".into(),
            );
        }
        // durable_history just synced the existing create-once completion event
        // and every administrative ancestor. This is reconciliation, not a new act.
        UNCERTAIN_COMPLETIONS
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .remove(&plan.dir);
        return Ok(
            json!({"state":"disposed","completion":"existing completion evidence synced; no new disposal act","administration":state(&plan.dir)?.view()}),
        );
    }
    if plan.action != "resume-disposal" {
        event(&plan.dir, &s, &plan.action, Some(actor), &current)?;
        s = state(&plan.dir)?;
    }
    if !matches!(plan.action.as_str(), "dispose" | "resume-disposal") {
        return Ok(
            json!({"state":"recorded","action":plan.action,"projectId":current["projectId"],"administration":s.view()}),
        );
    }
    // The durable original act, including the original complete export identity,
    // precedes deletion. Failure leaves a terminal admission fence for safe retry.
    let result: Result<(), String> = (|| {
        #[cfg(test)]
        if FAIL_REMOVE.with(|v| v.get()) {
            return Err("injected removal failure".to_owned());
        }
        #[cfg(test)]
        if let Some(hook) = AFTER_DISPOSAL_ACT.with(|h| h.borrow_mut().take()) {
            hook();
        }
        let original = s
            .disposition
            .as_ref()
            .ok_or("original disposal act missing")?;
        let bag = Path::new(
            original["export"]["folder"]
                .as_str()
                .ok_or("original export missing")?,
        );
        if plan.dir.exists() && physical(&plan.dir)? != original["context"]["payloadFolder"] {
            return Err("original payload folder changed after act publication; no removal".into());
        }
        let verified = crate::records_export::matches_current(&plan.dir, bag, true)?;
        if verified["identity"] != original["export"]["identity"] {
            return Err(
                "original verified export changed after act publication; no removal".into(),
            );
        }
        crate::records_export::dispose_members(
            &plan.dir,
            bag,
            &control(&plan.dir)?.join("removal"),
            original["export"]["identity"]
                .as_str()
                .ok_or("original export identity absent")?,
        )?;
        event(&plan.dir, &s, "disposal-completed", None, &current)?;
        Ok(())
    })();
    match result {
        Ok(()) => Ok(
            json!({"state":"disposed","projectId":current["projectId"],"administration":state(&plan.dir)?.view(),"export":current["export"],"standing":"Only this project's App store payload was removed. Administrative evidence and the verified export survive."}),
        ),
        Err(e) => {
            if state(&plan.dir).is_ok_and(|s| s.completed) {
                UNCERTAIN_COMPLETIONS
                    .lock()
                    .unwrap_or_else(|p| p.into_inner())
                    .insert(plan.dir.clone());
                Err(format!("records removed; completion publication durability uncertain; original disposal act retained and recording blocked; use Finish disposal to sync the existing completion evidence: {e}"))
            } else {
                Err(format!("disposal incomplete; original act retained and recording blocked; use Finish disposal to verify the original export and remaining bytes: {e}"))
            }
        }
    }
}

#[cfg(test)]
#[path = "records_retention_tests.rs"]
mod tests;
