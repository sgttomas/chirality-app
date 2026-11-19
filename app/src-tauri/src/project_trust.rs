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
use std::sync::Mutex;

/// What trust turns on, said wherever the person meets trust: setup's review, the switch-on confirmation and the
/// per-project view (and, later, the add confirmation). One source; no softer summary anywhere.
pub const EFFECTS_TEXT: &str = "Chirality sends this project to Codex as trusted. Codex then loads the project's own instructions (AGENTS.md) and its own Codex settings (the .codex folder in the project). With them:
- MCP servers that the project's settings name are started on this Mac when a conversation starts, outside the sandbox.
- The project's shell environment applies to every command the agent runs, and a start-up file of the project's own runs inside each command, under the same access level as that command.
- The project's rules can let commands run outside the sandbox without asking you.
- If Codex cannot load the project's settings file, no new conversation starts in this project until the file is fixed or trust is switched off.
You can switch trust off for this project in Chirality at any time.";
/// Setup's review, before the effects text, where a route names a project.
pub const WILL_TRUST: &str = "Chirality will trust this project.";
/// After the effects text, only where the root Codex computes is not the project's folder; the root between them,
/// as supplied text.
pub const INSIDE_REPOSITORY_BEFORE: &str = "This project's folder is inside the Git repository at ";
pub const INSIDE_REPOSITORY_AFTER: &str = ". Trust is sent for that repository's top folder, so Codex also loads the AGENTS.md files and .codex settings in the folders between it and this one.";
pub const TAKES_EFFECT: &str = "A change applies from the next conversation you start, continue or fork.";
pub const RUNNING_UNCHANGED: &str = "Conversations already running are not changed.";
/// The control's limit sentence; the store's own reason follows as detail.
pub const CANNOT_SWITCH: &str = "Trust can be switched only for an open project with its identity in the App's records store. A closed or disposed project, or one with no identity, cannot be switched.";
/// The switch-on confirmation's title and labels.
pub const TITLE: &str = "Project trust";
pub const PERFORM: &str = "Trust this project";
pub const DECLINE: &str = "Keep untrusted";
/// The view's sentences for the App's choice.
pub const CHOICE_ON_BY_SETUP: &str = "Trust is on: you set this project up in Chirality and have not switched its trust off.";
pub const CHOICE_ON_BY_SWITCH_PREFIX: &str = "Trust is on: you switched it on in Chirality at ";
pub const CHOICE_OFF_BY_SWITCH_PREFIX: &str = "Trust is off: you switched it off in Chirality at ";
pub const CHOICE_NONE: &str = "Chirality makes no trust choice for this project: it was opened from the environment, not set up in Chirality, so the Codex settings the App uses decide.";
pub const CHOICE_NOT_READ: &str = "The App could not read this project's trust choice, so it sends an untrusted entry until the choice can be read.";
/// The schema word of a switch line.
pub const SWITCH_FORMAT: &str = "chirality.project-trust-switch";

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
pub(crate) fn inside_repository(project: &Path) -> Option<Value> {
    let root = cl::project_root(project);
    (root != project).then(|| json!({"before": INSIDE_REPOSITORY_BEFORE, "root": root.to_string_lossy(), "after": INSIDE_REPOSITORY_AFTER,
        "standing": "The folder is supplied text."}))
}

/// The effects text for `project`, and the repository sentence where it applies.
pub(crate) fn effects_for(project: &Path) -> Value {
    json!({"text": EFFECTS_TEXT, "insideRepository": inside_repository(project)})
}

/// The effects as one plain text, for a native confirmation.
fn effects_plain(project: &Path) -> String {
    match cl::project_root(project) {
        root if root != project => format!("{EFFECTS_TEXT}\n{INSIDE_REPOSITORY_BEFORE}{}{INSIDE_REPOSITORY_AFTER}", root.to_string_lossy()),
        _ => EFFECTS_TEXT.to_owned(),
    }
}

/// A project the App knows: the folder as given and its physical spelling, and how it came to be known.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct KnownProject {
    pub folder: PathBuf,
    pub physical: PathBuf,
    pub known: Known,
}

struct Preview {
    token: String,
    project: PathBuf,
    content: Value,
}

/// The App's projects and their trust, shared by every home's Host.
#[derive(Default)]
pub struct ProjectTrust {
    projects: Mutex<Vec<KnownProject>>,
    /// The one open switch-on preview; a confirmation consumes it.
    preview: Mutex<Option<Preview>>,
    /// Held across a switch's write: one switch at a time in this App.
    switching: Mutex<()>,
    /// What the last frame for a known project carried (its `projectTrust` status).
    last_sent: Mutex<Option<Value>>,
    #[cfg(test)]
    pub(crate) after_confirmation: Mutex<Option<Box<dyn FnOnce() + Send>>>,
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
        let mut projects = self.projects.lock().unwrap_or_else(|p| p.into_inner());
        projects.retain(|p| p.folder != folder);
        projects.push(KnownProject { folder: folder.to_path_buf(), physical, known });
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
    /// The App's choice for the frame whose working folder is `cwd`, read now; None where `cwd` is no project of
    /// the App's.
    pub(crate) fn choice_for(&self, cwd: &Path) -> Option<AppTrust> {
        self.project_for(cwd).map(|project| Self::choice(&project))
    }
    /// The App's choice for `project`, read from its switches now.
    pub(crate) fn choice(project: &KnownProject) -> AppTrust {
        let default = match project.known { Known::SetUpInApp => AppTrust::OnBySetup, Known::EnvironmentRoute => AppTrust::NoChoice };
        match crate::records_store::trust_switches(&project.physical) {
            Err(detail) => AppTrust::NotRead { detail: Some(detail) },
            Ok(None) => default,
            Ok(Some(lines)) => match lines.last() {
                None => default,
                Some(line) => match parse_switch(line) {
                    Some((true, at)) => AppTrust::OnBySwitch { at },
                    Some((false, at)) => AppTrust::OffBySwitch { at },
                    None => AppTrust::NotRead { detail: Some("the latest switch line is not one the App writes".into()) },
                },
            },
        }
    }

    // ---- The acts ----

    /// What the switch-on confirmation will show for the launched project, and the token that confirms exactly
    /// it. Writes nothing.
    pub(crate) fn preview_on(&self) -> Result<Value, String> {
        let project = self.launched().ok_or("no project is open; trust cannot be switched")?;
        if let Some(reason) = crate::records_store::trust_switch_refusal(&project.physical) {
            return Err(format!("{CANNOT_SWITCH} {reason}"));
        }
        let content = Self::content(&project);
        let token = crate::util::opaque_id("project-trust-on-")?;
        *self.preview.lock().unwrap_or_else(|p| p.into_inner()) = Some(Preview { token: token.clone(), project: project.folder.clone(), content: content.clone() });
        Ok(json!({"token": token, "content": content, "perform": PERFORM, "decline": DECLINE}))
    }
    fn content(project: &KnownProject) -> Value {
        json!({"project": project.folder.to_string_lossy(), "projectStanding": "The folder is supplied text.", "effects": effects_for(&project.folder),
            "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED})
    }
    /// The person's switch on: only with the token of the open preview, only while what it showed is still what
    /// would be shown, only once, and only when `confirm` (the native confirmation, given the statement and the
    /// decline and perform labels) returns that the person chose to perform. Then one "on" line is written.
    pub(crate) fn confirm_on(&self, token: &str, confirm: impl FnOnce(ns::NativeStatement, &str, &str) -> Result<bool, String>) -> Result<Value, String> {
        // Consumed by this attempt, whatever its end: a token is never confirmed twice.
        let preview = self.preview.lock().unwrap_or_else(|p| p.into_inner()).take()
            .filter(|p| p.token == token).ok_or("This trust preview is not the open one; review it again")?;
        let project = self.launched().filter(|p| p.folder == preview.project).ok_or("The project changed since the preview; review it again")?;
        if Self::content(&project) != preview.content { return Err("What trust turns on for this project changed since the preview; review it again".into()); }
        if let Some(reason) = crate::records_store::trust_switch_refusal(&project.physical) { return Err(format!("{CANNOT_SWITCH} {reason}")); }
        let whole = format!("{}\n{TAKES_EFFECT} {RUNNING_UNCHANGED}", effects_plain(&project.folder));
        let statement = ns::whole_or_in_app("project trust", "project trust effects", whole, &preview.content,
            |digest| format!("{WILL_TRUST} What that turns on is shown in full in the App now, under \"Content named by an open native confirmation\". Its sha-256 digest: {digest}\n{TAKES_EFFECT}"))?;
        if !confirm(statement, DECLINE, PERFORM)? {
            return Ok(json!({"state": "cancelled; trust not switched on"}));
        }
        #[cfg(test)]
        if let Some(hook) = self.after_confirmation.lock().unwrap().take() { hook(); }
        if Self::content(&project) != preview.content { return Err("What trust turns on for this project changed during the confirmation; nothing written; review it again".into()); }
        self.write(&project, true)
    }
    /// The person's switch off: at once, with no confirmation.
    pub(crate) fn switch_off(&self) -> Result<Value, String> {
        let project = self.launched().ok_or("no project is open; trust cannot be switched")?;
        self.write(&project, false)
    }
    fn write(&self, project: &KnownProject, on: bool) -> Result<Value, String> {
        let _one = self.switching.lock().unwrap_or_else(|p| p.into_inner());
        let at = crate::util::now_rfc3339();
        let line = json!({"format": SWITCH_FORMAT, "at": at, "trust": if on {"on"} else {"off"}});
        crate::records_store::append_trust_switch(&project.physical, &line).map_err(|e| format!("{CANNOT_SWITCH} {e}"))?;
        Ok(json!({"state": if on {"switched-on"} else {"switched-off"}, "at": at, "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED, "view": self.view()}))
    }

    // ---- What the person is shown ----

    /// Notes what a frame for a known project carried (`threads[].level.projectTrust`).
    pub(crate) fn note_sent(&self, status: Value) {
        *self.last_sent.lock().unwrap_or_else(|p| p.into_inner()) = Some(status);
    }
    /// The per-project view, for the launched project (host status `projectTrustChoice`); None without a project.
    pub(crate) fn view(&self) -> Value {
        let Some(project) = self.launched() else { return Value::Null };
        let choice = Self::choice(&project);
        let (sentence, at, detail) = match &choice {
            AppTrust::OnBySetup => (CHOICE_ON_BY_SETUP.to_owned(), None, None),
            AppTrust::OnBySwitch { at } => (format!("{CHOICE_ON_BY_SWITCH_PREFIX}{at}."), Some(at.clone()), None),
            AppTrust::OffBySwitch { at } => (format!("{CHOICE_OFF_BY_SWITCH_PREFIX}{at}."), Some(at.clone()), None),
            AppTrust::NoChoice => (CHOICE_NONE.to_owned(), None, None),
            AppTrust::NotRead { detail } => (CHOICE_NOT_READ.to_owned(), None, detail.clone()),
        };
        let why = match &choice {
            AppTrust::OnBySetup => "set-up", AppTrust::OnBySwitch { .. } => "switched-on", AppTrust::OffBySwitch { .. } => "switched-off",
            AppTrust::NoChoice => "environment-route", AppTrust::NotRead { .. } => "not-read",
        };
        let refusal = crate::records_store::trust_switch_refusal(&project.physical);
        let on = matches!(choice, AppTrust::OnBySetup | AppTrust::OnBySwitch { .. });
        json!({
            "project": project.folder.to_string_lossy(), "projectStanding": "The folder is supplied text.", "known": project.known.word(),
            "choice": choice.word(), "why": why, "sentence": sentence, "switchedAt": at,
            "detail": detail.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT})),
            "lastSent": self.last_sent.lock().unwrap_or_else(|p| p.into_inner()).clone(),
            "effects": if on { effects_for(&project.folder) } else { Value::Null },
            "canSwitch": refusal.is_none(),
            "offers": if refusal.is_some() { json!([]) } else if on { json!(["switch-off"]) } else { json!(["switch-on"]) },
            "cannotSwitch": refusal.as_ref().map(|_| CANNOT_SWITCH),
            "cannotSwitchDetail": refusal.map(|text| json!({"text": text, "standing": cl::NOT_THE_APPS_TEXT})),
            "takesEffect": TAKES_EFFECT, "running": RUNNING_UNCHANGED,
        })
    }
}

/// A switch line the App writes: exactly its three members. `(on, at)`.
fn parse_switch(line: &Value) -> Option<(bool, String)> {
    let members = line.as_object()?;
    if members.len() != 3 || line["format"] != SWITCH_FORMAT { return None; }
    let at = line["at"].as_str()?.to_owned();
    match line["trust"].as_str()? { "on" => Some((true, at)), "off" => Some((false, at)), _ => None }
}

#[cfg(test)]
#[path = "project_trust_tests.rs"]
mod tests;
