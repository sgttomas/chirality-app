//! DEL-01-01, the owner's decision of 19 November 2026: a project the person set up (or, later, added) through the
//! App is sent to Codex as trusted, nothing withheld; the App says so per project, with what trust turns on, and
//! the person can switch it off.
//!
//! **The App's choice for a project** is on, off or none. The default follows how the project came to be known
//! ([`how_known`]): on where the person set it up through the App, none on the environment route (today's rule
//! there, unchanged). The person's latest switch replaces the default: on, only by a confirmed act
//! ([`ProjectTrust::confirm_on`], a native confirmation of the whole [`EFFECTS_TEXT`]); off, at once
//! ([`ProjectTrust::switch_off`]). The switches are kept in the project's own folder of the records store
//! (`records_store::TRUST_SWITCHES`), following its identity; the default writes nothing.
//!
//! **Where it applies.** To a frame whose working folder is the App's project folder for that conversation, and
//! only that: [`ProjectTrust::project_for`] is the one lookup. The choice is read just before each start, resume
//! and fork (`Host::trust_reading`), and the case table that combines it with the Codex settings' own mark is
//! `codex_level::TrustReading::row`. Every home the App offers shares one [`ProjectTrust`].
use crate::act_control::native_statement as ns;
use crate::codex_level::{self as cl, AppTrust};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::sync::{Mutex, MutexGuard};

/// What trust turns on, said wherever the person meets trust: setup's review, the switch-on confirmation and the
/// per-project view (and, later, the add confirmation). One source; no softer summary anywhere.
pub const EFFECTS_TEXT: &str = "Chirality marks this project as trusted when it starts, continues or forks a conversation in it, unless your own Codex settings mark the project untrusted or cannot be read. Codex then loads the project's own instructions (its AGENTS.md files) and its own Codex settings and rules (in the project's .codex folder). With them, the project's own files can:
- start MCP server programs on this Mac when a conversation starts, outside the sandbox, and have Codex connect to MCP servers at addresses they name;
- set the shell environment of every command the agent runs, and through it have a start-up file of the project's own run inside each command, under the same access level as that command;
- let commands run outside the sandbox without asking you, through the project's rules. Chirality cannot switch that off while the project is trusted;
- stop new conversations from starting in this project, where Codex cannot load the project's settings file, until the file is fixed or trust is switched off.
You can switch trust off for this project in Chirality while the project is open.";
/// Setup's review, before the effects text, where a route names a project.
pub const WILL_TRUST: &str = "Setting this project up switches Chirality's trust on for it.";
/// After the effects text, only where the root Codex computes is not the project's folder; the root between them,
/// as supplied text.
pub const INSIDE_REPOSITORY_BEFORE: &str = "This project's folder is inside the Git repository at ";
pub const INSIDE_REPOSITORY_AFTER: &str = ". Trust is marked for that repository's top folder, so Codex also loads the AGENTS.md files in the folders from there down to this one, and can load .codex settings in those folders.";
pub const TAKES_EFFECT: &str = "A change applies to conversations you start, continue or fork after it.";
pub const RUNNING_UNCHANGED: &str = "Conversations already running are not changed.";
/// The control's limit sentence; the store's own reason follows as detail.
pub const CANNOT_SWITCH: &str = "Trust can be switched only for a project that is open in Chirality with its identity in the App's records store. A closed or disposed project, or one with no identity, cannot be switched, and the records store can refuse a switch; its reason is shown.";
/// The switch-on confirmation's title and labels.
pub const TITLE: &str = "Project trust";
pub const PERFORM: &str = "Trust this project";
pub const DECLINE: &str = "Keep untrusted";
/// The view's sentences for the App's choice.
pub const CHOICE_ON_BY_SETUP: &str = "Chirality's choice for this project is on: you set it up in Chirality and have not switched its trust off.";
pub const CHOICE_ON_BY_SWITCH_PREFIX: &str = "Chirality's choice for this project is on: you switched it on in Chirality at ";
pub const CHOICE_OFF_BY_SWITCH_PREFIX: &str = "Chirality's choice for this project is off: you switched it off in Chirality at ";
pub const CHOICE_NONE: &str = "Chirality makes no trust choice for this project: it was opened from the environment, not set up in Chirality, so the Codex settings the App uses decide.";
pub const CHOICE_NOT_READ: &str = "The App could not read its record of this project's trust choice, so a conversation started in this project's folder is sent as untrusted until the record can be read.";
pub const CHOICE_OFF_BY_NEW_IDENTITY: &str = "Chirality's choice for this project is off: the project was given a new identity in the App's records store, and trust is not carried to a new identity. Switch it on to trust the project again.";
/// Not among the agreed sentences: the view's own account of `AppTrust::FolderChanged` (the status has its own).
pub const CHOICE_FOLDER_CHANGED: &str = "The project's folder is no longer the folder Chirality opened, so a conversation started in it is sent as untrusted.";
/// Beside any "on": the App's choice is not the entry itself.
pub const CHOICE_SETTINGS_CAN_OVERRIDE: &str = "Your own Codex settings can still make a conversation untrusted. What each start sent is shown with the conversation's access level.";
/// Where an on line made for another store or identity was passed over.
pub const CHOICE_PASSED_OVER: &str = "A switch-on recorded for another installation or another project identity is not used here.";
/// The switch-on confirmation's native line naming its content, where the whole does not fit (not among the agreed
/// sentences: setup's pointer without its setup line, which would be false here).
pub const SWITCH_ON_POINTER: &str = "What trust turns on for this project is shown in full in the App now, under \"Content named by an open native confirmation\". Its sha-256 digest: ";
/// The new-identity act's added line, for a project whose trust would otherwise be on.
pub const NEW_IDENTITY_TRUST_LINE: &str = "The project's trust will be off under its new identity until you switch it on.";
/// The refusal when what the person reviewed changed while the confirmation was open.
pub const CHANGED_WHILE_OPEN: &str = "The project or its trust changed while the confirmation was open; nothing written; review it again";
/// The schema word of a switch line, and the reason the new-identity act's off line carries. A line is exactly
/// `format`, `at` (an RFC 3339 instant), `trust` ("on" or "off"), `storeId` and `projectId` (the records store and
/// project identity it was written under), and, on that off line only, `reason`.
pub const SWITCH_FORMAT: &str = "chirality.project-trust-switch";
pub const NEW_IDENTITY_REASON: &str = "new identity";

/// How the App came to know a project. A later unit's "add a project in the running App" records
/// `AddedInApp` here, through [`ProjectTrust::add`], with no second mechanism.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Known {
    /// From the App's saved setup request (the desktop setup route).
    SetUpInApp,
    /// From the environment route (`CHIRALITY_WORKSPACE`).
    EnvironmentRoute,
}
impl Known {
    fn word(self) -> &'static str {
        match self { Known::SetUpInApp => "set-up-in-app", Known::EnvironmentRoute => "environment-route" }
    }
}

/// How the launched project came to be known, from the launch's source (`desktop_startup::Launch::source`): the
/// saved setup request is the person's setup through the App; everything else is the environment route. A project
/// set up before this rule existed is set up the same way, so it is on by the same derivation: no migration.
pub(crate) fn how_known(launch_source: &str) -> Known {
    if launch_source == crate::desktop_startup::SAVED_REQUEST_SOURCE { Known::SetUpInApp } else { Known::EnvironmentRoute }
}


/// Where the root Codex computes differs from `project`: the sentence's two parts and the root between them, as
/// supplied text. None where the project's folder is its own root. Computed by the function the trust entry uses
/// (`codex_level::project_root`), so the words and the entry cannot disagree.
#[cfg(test)]
pub(crate) fn inside_repository(project: &Path) -> Option<Value> {
    TrustObservation::of(project).inside_repository()
}

/// One observation of what trust turns on for a project: its folder as given and as resolved, and the root Codex
/// computes for it, each read once. Setup's review, the lines it stores and its statement are all made from one.
#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct TrustObservation {
    pub project: PathBuf,
    pub resolved: Option<PathBuf>,
    pub root: PathBuf,
}
#[cfg(test)]
thread_local! { static AFTER_OBSERVATION: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) }; }
/// Runs `hook` once, on this thread, right after the next observation is made.
#[cfg(test)]
pub(crate) fn after_trust_observation_for_test(hook: Option<Box<dyn FnOnce()>>) {
    AFTER_OBSERVATION.with(|h| *h.borrow_mut() = hook);
}
impl TrustObservation {
    pub(crate) fn of(project: &Path) -> Self {
        let observed = Self { project: project.to_path_buf(), resolved: std::fs::canonicalize(project).ok(), root: cl::project_root(project) };
        #[cfg(test)]
        if let Some(hook) = AFTER_OBSERVATION.with(|h| h.borrow_mut().take()) { hook(); }
        observed
    }
    fn inside_repository(&self) -> Option<Value> {
        (self.root != self.project).then(|| json!({"before": INSIDE_REPOSITORY_BEFORE, "root": self.root.to_string_lossy(), "after": INSIDE_REPOSITORY_AFTER,
            "standing": "The folder is supplied text."}))
    }
    /// The lines every surface shows, in this order: the effects text, then the repository sentence where it applies.
    pub(crate) fn lines(&self) -> Vec<String> {
        let mut lines = vec![EFFECTS_TEXT.to_owned()];
        if self.root != self.project { lines.push(format!("{INSIDE_REPOSITORY_BEFORE}{}{INSIDE_REPOSITORY_AFTER}", self.root.to_string_lossy())); }
        lines
    }
    /// The effects text, the repository sentence where it applies, and both as the lines shown.
    pub(crate) fn effects(&self) -> Value {
        json!({"text": EFFECTS_TEXT, "insideRepository": self.inside_repository(), "lines": self.lines()})
    }
    /// Setup's statement: the trust line, then what trust turns on.
    pub(crate) fn setup_lines(&self) -> String {
        format!("{WILL_TRUST}\n{}", self.lines().join("\n"))
    }
}

/// What trust turns on for `project`, as the lines every surface shows in this order: the effects text, then the
/// repository sentence where it applies. The one source for setup's review and statement, the switch-on
/// confirmation and the view.
pub(crate) fn effects_lines(project: &Path) -> Vec<String> {
    TrustObservation::of(project).lines()
}

/// The effects text for `project`, the repository sentence where it applies, and both as the lines shown.
pub(crate) fn effects_for(project: &Path) -> Value {
    TrustObservation::of(project).effects()
}

/// Setup's statement, where a route names a project: the trust line, then what trust turns on.
#[cfg(test)]
pub(crate) fn setup_trust_lines(project: &Path) -> String {
    TrustObservation::of(project).setup_lines()
}
/// What setup's confirmation shows in the App beside its native statement, when the setup lines fit the native
/// statement and the effects do not: the trust lines as the person reads them, frozen at review.
pub(crate) fn setup_trust_content(lines: &str) -> Value {
    json!(lines)
}
/// The native line that names that content.
pub(crate) fn setup_trust_pointer(digest: &str) -> String {
    format!("{WILL_TRUST} What that turns on is shown in full in the App now, under \"Content named by an open native confirmation\". Its sha-256 digest: {digest}")
}
/// The line the whole fallback adds, when even the setup lines do not fit the native statement.
pub const SETUP_TRUST_AMONG_EFFECTS: &str = "Setting this project up switches Chirality's trust on for it; what that turns on is among the complete effects shown in the App.";

/// The effects as one plain text, for a native confirmation.
fn effects_plain(project: &Path) -> String {
    effects_lines(project).join("\n")
}

/// A project the App knows: the folder as given and its physical spelling, and how it came to be known.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct KnownProject {
    pub folder: PathBuf,
    pub physical: PathBuf,
    pub known: Known,
    /// The folder's own identity (device and file number) when the App came to know it: another folder later put
    /// at the same path is not this project.
    pub identity: Option<(u64, u64)>,
}

/// The App's choice for a project as read now, with what it was read under.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ChoiceRead {
    pub choice: AppTrust,
    /// Changes whenever the choice could read differently: the store and project identities, the number of the
    /// validated switch lines and the last of them, or why none could be read.
    pub revision: String,
    /// The records store's and the project's identities the switches were read under, where the folder has one.
    pub identity: Option<(String, String)>,
    /// An on line made for another store or identity was passed over.
    pub passed_over: bool,
}

/// One validated switch line.
#[derive(Clone, Debug, PartialEq, Eq)]
struct Switch {
    on: bool,
    at: String,
    store: String,
    project: String,
    new_identity: bool,
}

/// A switch line the App writes: exactly its members, its time an RFC 3339 instant.
fn parse_switch(line: &Value) -> Option<Switch> {
    let members = line.as_object()?;
    let reason = members.get("reason");
    if members.len() != if reason.is_some() { 6 } else { 5 } || line["format"] != SWITCH_FORMAT { return None; }
    let at = line["at"].as_str().filter(|at| crate::after_run_end::instant(at).is_some())?.to_owned();
    let store = line["storeId"].as_str().filter(|s| !s.is_empty())?.to_owned();
    let project = line["projectId"].as_str().filter(|s| !s.is_empty())?.to_owned();
    let on = match line["trust"].as_str()? { "on" => true, "off" => false, _ => return None };
    let new_identity = match reason {
        None => false,
        Some(reason) if reason == NEW_IDENTITY_REASON && !on => true,
        Some(_) => return None,
    };
    Some(Switch { on, at, store, project, new_identity })
}
/// Every complete line validated, before any is selected or another appended: one the App does not write makes
/// the whole choice unreadable.
fn valid_switches(lines: &[Value]) -> Result<Vec<Switch>, String> {
    lines.iter().enumerate().map(|(n, line)| parse_switch(line)
        .ok_or_else(|| format!("line {} of the project's trust switches is not one the App writes", n + 1))).collect()
}
/// One switch line for the store and project identity it is written under.
fn switch_line(on: bool, store: &str, project: &str, reason: Option<&str>) -> Value {
    let mut line = json!({"format": SWITCH_FORMAT, "at": crate::util::now_rfc3339(), "trust": if on {"on"} else {"off"}, "storeId": store, "projectId": project});
    if let Some(reason) = reason { line["reason"] = json!(reason); }
    line
}
fn revision(parts: Value) -> String {
    crate::util::sha256_hex(parts.to_string().as_bytes())
}

struct Preview {
    token: String,
    project: PathBuf,
    /// What the person reviewed: the project's identity with the store, the choice's revision, the folder it
    /// resolved to and the root Codex computes, and the content shown.
    identity: Option<(String, String)>,
    revision: String,
    physical: PathBuf,
    root: Option<PathBuf>,
    content: Value,
}

/// The App's projects and their trust, shared by every home's Host.
#[derive(Default)]
pub struct ProjectTrust {
    projects: Mutex<Vec<KnownProject>>,
    /// The one open switch-on preview; a confirmation consumes it.
    preview: Mutex<Option<Preview>>,
    /// The token of the switch-on confirmation now in its native dialog: at most one at a time.
    confirming: Mutex<Option<String>>,
    /// Held across a switch's write, across the new-identity act, and by a Host across the write of a frame whose
    /// entry rests on the choice: a switch never lands between a frame's last check and its write.
    switching: Mutex<()>,
    /// What the last frame for a known project carried (its `projectTrust` status).
    last_sent: Mutex<Option<Value>>,
    #[cfg(test)]
    pub(crate) after_confirmation: Mutex<Option<Box<dyn FnOnce() + Send>>>,
    #[cfg(test)]
    pub(crate) before_preview_install: Mutex<Option<Box<dyn FnOnce() + Send>>>,
}

impl ProjectTrust {
    /// The launch's project, known as [`how_known`] says.
    pub(crate) fn for_launch(workspace: Option<&Path>, launch_source: &str) -> Self {
        let trust = ProjectTrust::default();
        if let Some(project) = workspace { trust.add(project, how_known(launch_source)); }
        trust
    }
    /// Records that the App knows `folder`, and how. Today's one caller is [`Self::for_launch`].
    pub(crate) fn add(&self, folder: &Path, known: Known) {
        let physical = std::fs::canonicalize(folder).unwrap_or_else(|_| folder.to_path_buf());
        let identity = cl::folder_binding(folder).folder;
        let mut projects = self.projects.lock().unwrap_or_else(|p| p.into_inner());
        projects.retain(|p| p.folder != folder);
        projects.push(KnownProject { folder: folder.to_path_buf(), physical, known, identity });
    }
    /// The launched project (the first the App knows).
    pub(crate) fn launched(&self) -> Option<KnownProject> {
        self.projects.lock().unwrap_or_else(|p| p.into_inner()).first().cloned()
    }
    /// The App's project a frame's working folder is: the folder as given or its physical spelling, compared
    /// exactly. Nothing is inferred from a folder below or above a project.
    pub(crate) fn project_for(&self, cwd: &Path) -> Option<KnownProject> {
        self.projects.lock().unwrap_or_else(|p| p.into_inner()).iter().find(|p| p.folder == cwd || p.physical == cwd).cloned()
    }
    /// The project a command names, by the view's `project` value; refused, writing nothing, when it is not one the
    /// App holds.
    fn held(&self, project: &str) -> Result<KnownProject, String> {
        self.launched().filter(|p| p.folder.to_string_lossy() == project)
            .ok_or_else(|| "This project is not one the App holds; nothing written".to_owned())
    }
    /// The App's choice for the frame whose working folder is `cwd`, read now; None where `cwd` is no project of
    /// the App's.
    pub(crate) fn choice_for(&self, cwd: &Path) -> Option<AppTrust> {
        self.choice_read_for(cwd).map(|read| read.choice)
    }
    /// As [`Self::choice_for`], with its revision.
    pub(crate) fn choice_read_for(&self, cwd: &Path) -> Option<ChoiceRead> {
        let project = self.project_for(cwd)?;
        Some(Self::read_choice(&project, Some(cwd)))
    }
    /// Held by a Host across the write of a frame whose entry rests on the choice.
    pub(crate) fn hold_switches(&self) -> MutexGuard<'_, ()> {
        self.switching.lock().unwrap_or_else(|p| p.into_inner())
    }
    /// The App's choice for `project`, read from its switches now.
    pub(crate) fn choice(project: &KnownProject) -> AppTrust {
        Self::read_choice(project, None).choice
    }
    /// The App's choice for `project`, read now, for a frame whose working folder is `cwd` where one is given.
    pub(crate) fn read_choice(project: &KnownProject, cwd: Option<&Path>) -> ChoiceRead {
        let plain = |choice: AppTrust, why: &str| ChoiceRead { choice, revision: revision(json!([why])), identity: None, passed_over: false };
        // The folder: as given, and as the frame names it, it must still resolve to the folder the App admitted (the
        // same path and the same folder there, by its own identity), and its root to the same root, or the App's
        // choice is not applied.
        let physical = |p: &Path| std::fs::canonicalize(p).ok();
        let resolves = |p: &Path| physical(p).as_deref() == Some(project.physical.as_path())
            && project.identity.is_some() && cl::folder_binding(p).folder == project.identity;
        let same_root = |cwd: &Path| physical(&cl::project_root(cwd)) == physical(&cl::project_root(&project.folder));
        if !resolves(&project.folder) || cwd.is_some_and(|cwd| !resolves(cwd) || !same_root(cwd)) {
            return plain(AppTrust::FolderChanged, "folder-changed");
        }
        let default = match project.known { Known::SetUpInApp => AppTrust::OnBySetup, Known::EnvironmentRoute => AppTrust::NoChoice };
        // A run with no records store (none named, or the one named refused): no switch can be read or made in it.
        // On the environment route that is no choice, so the route behaves as before; on the setup route the
        // choice is not readable (below), and the entry goes untrusted.
        if project.known == Known::EnvironmentRoute && crate::records_store::current().is_err() {
            return plain(AppTrust::NoChoice, "no-store");
        }
        let switches = match crate::records_store::trust_switches(&project.physical) {
            Err(detail) => return ChoiceRead { revision: revision(json!(["not-read", detail])), choice: AppTrust::NotRead { detail: Some(detail) }, identity: None, passed_over: false },
            Ok(None) => return plain(default, "no-identity"),
            Ok(Some(switches)) => switches,
        };
        let identity = Some((switches.store_id.clone(), switches.project_id.clone()));
        let revision = revision(json!([switches.store_id, switches.project_id, switches.lines]));
        let valid = match valid_switches(&switches.lines) {
            Err(detail) => return ChoiceRead { choice: AppTrust::NotRead { detail: Some(detail) }, revision, identity, passed_over: false },
            Ok(valid) => valid,
        };
        // The latest line that counts: an off line whatever its origin (it only removes trust); an on line only
        // where it was made under this store and this project identity, else passed over.
        let mut passed_over = false;
        let mut choice = default;
        for switch in valid.iter().rev() {
            if !switch.on {
                choice = if switch.new_identity { AppTrust::OffByNewIdentity { at: switch.at.clone() } } else { AppTrust::OffBySwitch { at: switch.at.clone() } };
                break;
            }
            if switch.store == switches.store_id && switch.project == switches.project_id {
                choice = AppTrust::OnBySwitch { at: switch.at.clone() };
                break;
            }
            passed_over = true;
        }
        ChoiceRead { choice, revision, identity, passed_over }
    }

    // ---- The acts ----

    /// What the switch-on confirmation will show for the project the view named, and the token that confirms
    /// exactly it. Writes nothing. Refused while another trust confirmation is open: the check and the install are
    /// one step under the confirmation's lock, so no preview is installed while a confirmation is in its dialog.
    pub(crate) fn preview_on(&self, project: &str) -> Result<Value, String> {
        let project = self.held(project)?;
        let confirming = self.confirming.lock().unwrap_or_else(|p| p.into_inner());
        if confirming.is_some() {
            return Err("A trust confirmation is already open; finish it first; nothing written".into());
        }
        let read = Self::read_choice(&project, None);
        if let Some(reason) = Self::switch_refusal(&project, &read.choice) {
            return Err(format!("{CANNOT_SWITCH} {reason}"));
        }
        let content = Self::content(&project);
        let token = crate::util::opaque_id("project-trust-on-")?;
        #[cfg(test)]
        if let Some(hook) = self.before_preview_install.lock().unwrap().take() { hook(); }
        *self.preview.lock().unwrap_or_else(|p| p.into_inner()) = Some(Preview { token: token.clone(), project: project.folder.clone(),
            identity: read.identity, revision: read.revision, physical: project.physical.clone(), root: Self::root_of(&project), content: content.clone() });
        drop(confirming);
        Ok(json!({"token": token, "content": content, "perform": PERFORM, "decline": DECLINE}))
    }
    /// Why no switch can be written for `project` now, its choice read as `choice`: what the records store refuses,
    /// a folder that is no longer the one admitted, or a choice whose record could not be read (its detail, supplied
    /// text). The view offers no switch, and the acts write none, where this is given.
    fn switch_refusal(project: &KnownProject, choice: &AppTrust) -> Option<String> {
        crate::records_store::trust_switch_refusal(&project.physical).or_else(|| match choice {
            AppTrust::FolderChanged => Some(CHOICE_FOLDER_CHANGED.to_owned()),
            AppTrust::NotRead { detail } => Some(detail.clone().unwrap_or_default()),
            _ => None,
        })
    }
    fn root_of(project: &KnownProject) -> Option<PathBuf> {
        std::fs::canonicalize(cl::project_root(&project.folder)).ok()
    }
    fn content(project: &KnownProject) -> Value {
        json!({"project": project.folder.to_string_lossy(), "projectStanding": "The folder is supplied text.", "effects": effects_for(&project.folder),
            "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED})
    }
    /// The person's switch on: only with the token of the open preview, only while what it showed is still what
    /// would be shown, only once, and only when `confirm` (the native confirmation, given the statement and the
    /// decline and perform labels) returns that the person chose to perform. After the answer, one "on" line is
    /// written only where the project's identity, the choice's revision, the folder and its root, and the content
    /// are all as reviewed.
    pub(crate) fn confirm_on(&self, token: &str, confirm: impl FnOnce(ns::NativeStatement, &str, &str) -> Result<bool, String>) -> Result<Value, String> {
        // Consumed by this attempt, whatever its end: a token is never confirmed twice.
        let preview = self.preview.lock().unwrap_or_else(|p| p.into_inner()).take()
            .filter(|p| p.token == token).ok_or("This trust preview is not the open one; review it again")?;
        let project = self.launched().filter(|p| p.folder == preview.project).ok_or("The project changed since the preview; review it again")?;
        if Self::content(&project) != preview.content { return Err("What trust turns on for this project changed since the preview; review it again".into()); }
        if let Some(reason) = crate::records_store::trust_switch_refusal(&project.physical) { return Err(format!("{CANNOT_SWITCH} {reason}")); }
        let whole = format!("{}\n{TAKES_EFFECT} {RUNNING_UNCHANGED}", effects_plain(&project.folder));
        let statement = ns::whole_or_in_app("project trust", "project trust effects", whole.clone(), &json!(whole),
            |digest| format!("{SWITCH_ON_POINTER}{digest}\n{TAKES_EFFECT}"))?;
        // At most one confirmation in its native dialog; a second preview is refused meanwhile, and one installed
        // before the dialog opened is withdrawn with it.
        {
            let mut confirming = self.confirming.lock().unwrap_or_else(|p| p.into_inner());
            if confirming.is_some() { return Err("A trust confirmation is already open; finish it first; nothing written".into()); }
            *confirming = Some(token.to_owned());
            *self.preview.lock().unwrap_or_else(|p| p.into_inner()) = None;
        }
        let answer = confirm(statement, DECLINE, PERFORM);
        *self.confirming.lock().unwrap_or_else(|p| p.into_inner()) = None;
        if !answer? {
            return Ok(json!({"state": "cancelled; trust not switched on"}));
        }
        #[cfg(test)]
        if let Some(hook) = self.after_confirmation.lock().unwrap().take() { hook(); }
        self.write(&project, true, Some(&preview))
    }
    /// The person's switch off for the project the view named: at once, with no confirmation.
    pub(crate) fn switch_off(&self, project: &str) -> Result<Value, String> {
        let project = self.held(project)?;
        self.write(&project, false, None)
    }
    fn write(&self, project: &KnownProject, on: bool, reviewed: Option<&Preview>) -> Result<Value, String> {
        let _one = self.hold_switches();
        let read = Self::read_choice(project, None);
        if let Some(reviewed) = reviewed {
            let unchanged = read.identity == reviewed.identity && read.revision == reviewed.revision && project.physical == reviewed.physical
                && Self::root_of(project) == reviewed.root && Self::content(project) == reviewed.content && read.choice != AppTrust::FolderChanged;
            if !unchanged { return Err(CHANGED_WHILE_OPEN.into()); }
        }
        if read.choice == AppTrust::FolderChanged { return Err(format!("{CANNOT_SWITCH} {CHOICE_FOLDER_CHANGED}")); }
        let (store, identity) = match (&read.identity, &read.choice) {
            (Some(identity), _) => identity.clone(),
            (None, AppTrust::NotRead { detail }) => return Err(format!("{CANNOT_SWITCH} {}", detail.clone().unwrap_or_default())),
            (None, _) => return Err(format!("{CANNOT_SWITCH} the project has no identity in the records store")),
        };
        let line = switch_line(on, &store, &identity, None);
        crate::records_store::append_trust_switch(&project.physical, &line, |lines| valid_switches(lines).map(|_| ())).map_err(|e| format!("{CANNOT_SWITCH} {e}"))?;
        drop(_one);
        Ok(json!({"state": if on {"switched-on"} else {"switched-off"}, "at": line["at"], "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED, "view": self.view()}))
    }
    /// For the new-identity act on `root`: the off line it writes under the new identity, where the App holds the
    /// project, however it was opened (DEL-01-01); None otherwise.
    pub(crate) fn new_identity_off_line(&self, root: &Path) -> Option<impl Fn(&str, &str) -> Value> {
        let physical = std::fs::canonicalize(root).ok()?;
        let held = self.projects.lock().unwrap_or_else(|p| p.into_inner()).iter().any(|p| p.physical == physical);
        held.then_some(|store: &str, project: &str| switch_line(false, store, project, Some(NEW_IDENTITY_REASON)))
    }

    // ---- What the person is shown ----

    /// Notes what a frame for a known project carried (`threads[].level.projectTrust`).
    pub(crate) fn note_sent(&self, status: Value) {
        *self.last_sent.lock().unwrap_or_else(|p| p.into_inner()) = Some(status);
    }
    /// The per-project view, for the launched project (host status `projectTrustChoice`); None without a project.
    pub(crate) fn view(&self) -> Value {
        let Some(project) = self.launched() else { return Value::Null };
        let read = Self::read_choice(&project, None);
        let choice = read.choice.clone();
        let (sentence, at, detail) = match &choice {
            AppTrust::OnBySetup => (CHOICE_ON_BY_SETUP.to_owned(), None, None),
            AppTrust::OnBySwitch { at } => (format!("{CHOICE_ON_BY_SWITCH_PREFIX}{at}."), Some(at.clone()), None),
            AppTrust::OffBySwitch { at } => (format!("{CHOICE_OFF_BY_SWITCH_PREFIX}{at}."), Some(at.clone()), None),
            AppTrust::OffByNewIdentity { at } => (CHOICE_OFF_BY_NEW_IDENTITY.to_owned(), Some(at.clone()), None),
            AppTrust::NoChoice => (CHOICE_NONE.to_owned(), None, None),
            AppTrust::NotRead { detail } => (CHOICE_NOT_READ.to_owned(), None, detail.clone()),
            AppTrust::FolderChanged => (CHOICE_FOLDER_CHANGED.to_owned(), None, None),
        };
        let why = match &choice {
            AppTrust::OnBySetup => "set-up", AppTrust::OnBySwitch { .. } => "switched-on", AppTrust::OffBySwitch { .. } => "switched-off",
            AppTrust::OffByNewIdentity { .. } => "new-identity", AppTrust::NoChoice => "environment-route", AppTrust::NotRead { .. } => "not-read",
            AppTrust::FolderChanged => "folder-changed",
        };
        let refusal = Self::switch_refusal(&project, &choice);
        let on = matches!(choice, AppTrust::OnBySetup | AppTrust::OnBySwitch { .. });
        json!({
            "project": project.folder.to_string_lossy(), "projectStanding": "The folder is supplied text.", "known": project.known.word(),
            "choice": choice.word(), "why": why, "sentence": sentence, "switchedAt": at,
            "detail": detail.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT})),
            "settingsCanOverride": if on { json!(CHOICE_SETTINGS_CAN_OVERRIDE) } else { Value::Null },
            "passedOver": if read.passed_over { json!(CHOICE_PASSED_OVER) } else { Value::Null },
            "lastSent": self.last_sent.lock().unwrap_or_else(|p| p.into_inner()).clone(),
            "effects": if on { effects_for(&project.folder) } else { Value::Null },
            "canSwitch": refusal.is_none(),
            "offers": if refusal.is_some() { json!([]) } else if on { json!(["switch-off"]) } else { json!(["switch-on"]) },
            "cannotSwitch": refusal.as_ref().map(|_| CANNOT_SWITCH),
            "cannotSwitchDetail": refusal.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT})),
            "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED,
            // Beside the records store's "Give this folder a new identity", for every held project: the act writes
            // one off line under the new identity.
            "newIdentity": NEW_IDENTITY_TRUST_LINE,
        })
    }
}

#[cfg(test)]
impl ProjectTrust {
    /// The commands as the view names the launched project.
    fn launched_name(&self) -> String { self.launched().map(|p| p.folder.to_string_lossy().into_owned()).unwrap_or_default() }
    pub(crate) fn switch_off_launched(&self) -> Result<Value, String> { self.switch_off(&self.launched_name()) }
    pub(crate) fn preview_on_launched(&self) -> Result<Value, String> { self.preview_on(&self.launched_name()) }
}

#[cfg(test)]
#[path = "project_trust_tests.rs"]
mod tests;
