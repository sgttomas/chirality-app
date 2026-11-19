//! The navigator's one read: every project of the person's records store, and
//! under each its conversations and the workflow runs they carry, as one
//! answer for the left panel (the interface lane's navigator, after 3.0.1's).
//!
//! **A read only.** It changes nothing anywhere, starts nothing and sends
//! nothing to Codex, so it is safe on a timer. In the store it opens what
//! exists (`records_store::opened_existing`, `listed_folders`, `attach` without
//! minting, through `records_store::status`), and in each listed folder it reads the recorded runs as Reopen
//! reads them (`record_supply::read_project_runs`); no identity is minted, no
//! index is built or refreshed, no ledger row or lease is written. Those
//! readers take a shared advisory lock on a project's existing admission file
//! while they read; they create none. Codex's side is what the App already
//! holds in memory: each home's Host snapshot (its loaded conversations and
//! waiting requests), its history view (the `thread/list` rows received), and
//! the recovery ledger rows the Host holds; nothing is dispatched.
//!
//! **Where a conversation goes.** Under the project the App recorded for it
//! (the recovery ledger's `conversation_index` row of its home and thread);
//! else under the listed project whose recorded root is exactly the folder
//! Codex reports; else in `unassigned` when that folder is the one set aside
//! for conversations without a project; else under a folder section with no
//! identity, so that no conversation of the sign-in is hidden. A reported
//! folder only places a conversation the App has no record for, and is marked
//! so; it is never written or taken as the App's record. Delegated children
//! (a `parentThreadId`) are not entries.
//!
//! The pure composition (`compose`) takes what `gather` collected; the tests
//! drive it with invented material.
use crate::records::supply::RecordedLifecycle;
use serde::Serialize;
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

/// The longest title made from a conversation's first message, in characters.
pub const TITLE_CHARS: usize = 60;

// ---- What the read returns (the shape the interface reads) ----

/// The whole answer of `navigator_read`.
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct NavigatorRead {
    /// When this read began (RFC 3339).
    pub read_at: String,
    /// In the order to show: the project new conversations open in first,
    /// then the others by their newest entry's `updatedAt` (newest first),
    /// then by when the registry recorded them.
    pub projects: Vec<NavigatorProject>,
    /// Conversations that belong to no project: their folder is the one set
    /// aside for conversations without a project (or Codex reports none).
    pub unassigned: Vec<NavigatorEntry>,
    /// One per configured Codex home: whether its conversations were read.
    pub conversations: Vec<ConversationsRead>,
    /// What the records store's registry of project folders could not give
    /// (not read, or read only to its last complete line), as sentences.
    /// Empty when it was read whole.
    pub registry_limits: Vec<String>,
}

/// Whether something was read, and why not where it was not.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(tag = "state")]
pub enum ReadOutcome {
    #[serde(rename = "read")]
    Read,
    #[serde(rename = "not-read")]
    NotRead {
        /// One sentence a person can read.
        reason: String,
    },
}

/// One configured Codex home's conversations: `{home, state, reason?}`.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct ConversationsRead {
    /// The home class word the host uses (`account`, `api-key`, `local-provider`).
    pub home: String,
    #[serde(flatten)]
    pub outcome: ReadOutcome,
}

#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct NavigatorProject {
    /// The records store's identity of the project, or null for a folder
    /// section that has none.
    pub project_id: Option<String>,
    /// The folder path as recorded.
    pub root: String,
    /// The folder's name, widened to `parent/name` where two listed folders
    /// share a name.
    pub label: String,
    /// True for the project new conversations open in (the launched project).
    pub current: bool,
    pub state: ProjectState,
    pub notice: Option<ProjectNotice>,
    pub runs_read: RunsRead,
    /// Newest first by `updatedAt`; entries with none last.
    pub entries: Vec<NavigatorEntry>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum ProjectState {
    /// The launched project, usable now.
    Open,
    /// Known, not open in this running App.
    Listed,
    /// The folder is gone or cannot be examined.
    Unavailable,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct ProjectNotice {
    /// The store's fault word where there is one (`link missing`, `link
    /// unreadable`, `link changed`, `link names another store`, `several
    /// identities`, `moved`, `duplicated`, `another store`, `no folder
    /// recorded`, `association not known`); else `gone` (the folder is not
    /// there), `unavailable` (it cannot be examined) or `no-identity` (the
    /// store holds no identity for it).
    pub kind: String,
    /// One sentence a person can read.
    pub message: String,
    /// The store's own acts that resolve it (`restore-link`, `adopt`,
    /// `new-identity`); empty where none applies.
    pub resolutions: Vec<String>,
}

/// Whether the project's recorded runs were read: `{state: "read"}` or
/// `{state: "not-read", reason}`, with the records reader's own limits.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct RunsRead {
    #[serde(flatten)]
    pub outcome: ReadOutcome,
    /// What the records reader reported it could not read, as it words it.
    pub limits: Vec<String>,
}

/// One conversation. A conversation that carries a workflow run is that
/// run's entry.
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct NavigatorEntry {
    /// The thread id.
    pub id: String,
    /// The home class word, or null for a conversation known only from a run
    /// record whose home the App's ledger does not name.
    pub home: Option<String>,
    /// The project folder this entry is placed under; null in `unassigned`
    /// where Codex reports no folder.
    pub project_root: Option<String>,
    pub project_source: ProjectSource,
    pub title: Option<String>,
    pub title_source: TitleSource,
    /// RFC 3339, null where not known (a conversation not in the list read).
    pub created_at: Option<String>,
    pub updated_at: Option<String>,
    pub live: Live,
    /// Requests awaiting the person on this conversation's own thread, from
    /// the Host's local register. A delegated child's request is raised on
    /// the child's thread and is not counted on its parent in this unit.
    pub needs_answer: u64,
    /// False for everything this unit returns: the list it reads holds no
    /// archived conversations. Kept for the next unit.
    pub archived: bool,
    pub open: OpenWith,
    pub run: Option<EntryRun>,
    /// How many recorded runs name this conversation.
    pub run_count: usize,
    /// Null in this unit: the host holds no count of running descendants
    /// without a further read.
    pub children_running: Option<u64>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum ProjectSource {
    /// The App's own record (the recovery ledger's conversation index) names
    /// the project.
    Recorded,
    /// Only the folder Codex reports placed it.
    ReportedFolder,
    /// Only a run's record names the conversation.
    RunRecord,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum TitleSource {
    /// Codex's `name`.
    Name,
    /// Codex's `preview`, cut to `TITLE_CHARS` characters on a word boundary
    /// (no ellipsis is added).
    FirstMessage,
    None,
}

/// What Codex reports for the conversation in the current generation of its
/// home. Never `running` from a record alone.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum Live {
    /// Codex reports it `active`.
    Running,
    /// Codex reports it `idle`.
    Idle,
    /// Codex reports it `notLoaded`.
    NotLoaded,
    /// Anything else: no current report, a `systemError`, an unknown status,
    /// a home not running, or a conversation known only from a record.
    Unknown,
}

/// What the interface's existing paths take to open the conversation. No new
/// way of opening anything.
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(tag = "kind", rename_all = "kebab-case")]
pub enum OpenWith {
    /// Loaded in the current generation: select it by generation and thread
    /// id, as a host status thread row is selected.
    Loaded {
        generation: Value,
        #[serde(rename = "threadId")]
        thread_id: String,
    },
    /// Not loaded, and in the list the home's current history view received:
    /// History's own path, `history_select(generation, selectionEpoch,
    /// threadId)` and then `history_action(generation, <the epoch that
    /// select returns>, "continue", ...)`. The epoch is the view's as read;
    /// a later selection makes History refuse and ask to select again.
    History {
        home: String,
        generation: Value,
        #[serde(rename = "selectionEpoch")]
        selection_epoch: u64,
        #[serde(rename = "threadId")]
        thread_id: String,
    },
    /// A further host step would be needed first; the sentence says which.
    NotOpenable { reason: String },
}

/// The latest run the conversation carries.
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct EntryRun {
    pub run_id: String,
    pub workflow: RunWorkflow,
    pub state: RunState,
    /// Who ended it and why, as recorded; null unless ended.
    pub ended_by: Option<EndedBy>,
    /// For an open run this process holds in force: true where the run guide
    /// is offered the agent's finished statement for it (the same reading as
    /// the run guide's offers), false where it is offered none. Null where it
    /// cannot be told: the run is not open, the run is not held live in this
    /// process (a run recorded open by an earlier session), or its operation
    /// is pending.
    pub finished_reported: Option<bool>,
    /// Null in this unit: the number of file changes Codex reported is not at
    /// hand without a further read per run.
    pub result_count: Option<u64>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct RunWorkflow {
    pub name: Option<String>,
    /// The package's display title: null in this unit, since no package the
    /// App reads declares one (the run guide shows the name).
    pub title: Option<String>,
    /// As the run guide words a workflow's source: "included with the App",
    /// "a bundled copy (source …)", or "‹origin› library".
    pub origin: Option<String>,
    /// The Library release, as the run guide words it ("Chirality Library
    /// 3.4.0"), for a workflow included with the App; null otherwise.
    pub release: Option<String>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum RunState {
    /// Opened and not ended in a complete record (open, or interrupted by a
    /// relaunch; it stays open until the person ends it).
    Open,
    Ended,
    /// A published run start with no opening: not confirmed in the record.
    StartNotConfirmed,
    /// An incomplete or conflicting record.
    Unknown,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct EndedBy {
    pub stopped_by: String,
    pub cause: String,
}

// ---- What `gather` collects for `compose` ----

pub(crate) struct Gathered {
    pub read_at: String,
    /// The launched project's root, as the store names folders (physical).
    pub current_root: Option<String>,
    /// Other spellings of a section's root (the launched project as given,
    /// which the App's conversation index records), with the root they name.
    pub aliases: Vec<(String, String)>,
    /// The folder set aside for conversations without a project, as spelled
    /// and as resolved.
    pub no_project_folders: Vec<String>,
    pub registry: Result<crate::records_store::ListedFolders, String>,
    /// The listed folders and the launched project, each examined.
    pub folders: Vec<FolderInput>,
    pub homes: Vec<HomeInput>,
    pub index: Vec<IndexRow>,
    /// Runs this process holds in force: whether the finished report is
    /// offered for each, or `None` where it cannot be told.
    pub finished: Vec<(String, Option<bool>)>,
    pub catalog: CatalogInput,
}

pub(crate) struct FolderInput {
    pub root: String,
    pub examined: Examined,
    pub runs: RunsInput,
}

pub(crate) enum Examined {
    /// The folder is not there.
    Gone,
    /// The folder cannot be examined (the reason as the reader gave it).
    Unexaminable(String),
    /// The records store cannot be read, so no folder is attached.
    StoreUnavailable(String),
    /// How the store attaches the folder (`records_store::Attachment`).
    Attached { project: Option<String>, fault: Option<String>, refusal: Option<String>, resolutions: Vec<String> },
}

pub(crate) enum RunsInput {
    /// Not read, for what `Examined` says.
    NotAttempted,
    NotRead(String),
    Read { runs: Vec<RunInput>, limits: Vec<String> },
}

pub(crate) struct RunInput {
    pub run_id: String,
    pub conversation: Option<String>,
    pub workflow: Value,
    pub lifecycle: RecordedLifecycle,
    /// When the run was opened (its `run_opened` entry), else its latest
    /// written entry; orders a conversation's runs.
    pub recorded_at: Option<String>,
}

pub(crate) struct HomeInput {
    /// The home class word.
    pub class: String,
    /// The Host's state word (`ready`, `absent`, ...).
    pub state: String,
    pub generation: Value,
    /// Ready and its generation not closed.
    pub current: bool,
    /// The Host's loaded conversation rows (`snapshot()["threads"]`).
    pub loaded: Vec<Value>,
    pub history: Option<HistoryInput>,
    /// Requests awaiting the person, per thread id, current generation.
    pub waiting: Vec<(String, u64)>,
}

pub(crate) struct HistoryInput {
    pub generation: Value,
    pub selection_epoch: u64,
    /// The Codex `Thread` rows received.
    pub threads: Vec<Value>,
    pub read_at_ready: Option<Value>,
}

/// A recovery ledger `conversation_index` row: the App's own record of a
/// conversation's project.
pub(crate) struct IndexRow {
    /// The home class word.
    pub home: String,
    pub thread: String,
    /// The project reference the App recorded (the launched root as given).
    pub project: String,
}

#[derive(Default)]
pub(crate) struct CatalogInput {
    /// The identities of the workflows included with the App.
    pub identities: Vec<Value>,
    /// The Library release they come from, worded.
    pub release: Option<String>,
}

// ---- Composition ----

struct Section {
    project: NavigatorProject,
    position: Option<usize>,
}

/// One conversation as Codex reports it (list and loaded rows merged).
struct Conversation {
    home: String,
    id: String,
    cwd: Option<String>,
    name: Option<String>,
    preview: Option<String>,
    created: Option<f64>,
    updated: Option<f64>,
    live: Live,
    open: OpenWith,
    waiting: u64,
}

/// The read, composed from what was gathered. Pure.
pub(crate) fn compose(g: Gathered) -> NavigatorRead {
    let (listed, registry_limits) = match &g.registry {
        Ok(r) => (r.folders.clone(), r.torn.iter().cloned().chain(r.limits.iter().cloned()).collect::<Vec<_>>()),
        Err(e) => (vec![], vec![format!("The records store's list of project folders was not read ({e}), so only the project open now is shown.")]),
    };
    let mut sections: Vec<Section> = Vec::new();
    // The launched project, then every listed folder.
    let mut roots: Vec<String> = g.current_root.iter().cloned().collect();
    roots.extend(listed.iter().map(|f| f.root.clone()).filter(|r| Some(r) != g.current_root.as_ref()));
    for root in &roots {
        let folder = g.folders.iter().find(|f| &f.root == root);
        let listing = listed.iter().find(|f| &f.root == root);
        sections.push(section(root, folder, listing, g.current_root.as_ref() == Some(root)));
    }
    let section_of = |sections: &Vec<Section>, root: &str| -> Option<usize> {
        let root = g.aliases.iter().find(|(alias, _)| alias == root).map_or(root, |(_, to)| to.as_str());
        sections.iter().position(|s| s.project.root == root)
    };

    // Recorded runs by conversation, each with the folder that records it.
    let mut runs_of: BTreeMap<&str, Vec<(&RunInput, &str, usize)>> = BTreeMap::new();
    let mut order = 0;
    for folder in &g.folders {
        if let RunsInput::Read { runs, .. } = &folder.runs {
            for run in runs {
                order += 1;
                if let Some(conversation) = run.conversation.as_deref() {
                    let list = runs_of.entry(conversation).or_default();
                    if !list.iter().any(|(r, _, _)| r.run_id == run.run_id) { list.push((run, folder.root.as_str(), order)); }
                }
            }
        }
    }
    let finished: BTreeMap<&str, Option<bool>> = g.finished.iter().map(|(r, f)| (r.as_str(), *f)).collect();
    let recorded = |home: Option<&str>, thread: &str| -> Option<&str> {
        let mut rows = g.index.iter().filter(|r| r.thread == thread && home.is_none_or(|h| r.home == h));
        let first = rows.next()?;
        // Without a home, only an index that names one project for the thread.
        if home.is_none() && rows.any(|r| r.project != first.project) { return None; }
        g.index.iter().rev().find(|r| r.thread == thread && home.is_none_or(|h| r.home == h)).map(|r| r.project.as_str())
    };
    let run_part = |thread: &str| -> (Option<EntryRun>, usize) {
        let Some(runs) = runs_of.get(thread) else { return (None, 0) };
        let latest = runs.iter().max_by(|a, b| (a.0.recorded_at.as_deref(), a.2).cmp(&(b.0.recorded_at.as_deref(), b.2)));
        (latest.map(|(run, _, _)| entry_run(run, &finished, &g.catalog)), runs.len())
    };

    let mut unassigned: Vec<NavigatorEntry> = Vec::new();
    let mut conversations = Vec::new();
    let mut seen: BTreeSet<String> = BTreeSet::new();
    for home in &g.homes {
        let (found, outcome) = home_conversations(home);
        conversations.push(ConversationsRead { home: home.class.clone(), outcome });
        for c in found {
            seen.insert(c.id.clone());
            let (run, run_count) = run_part(&c.id);
            let (title, title_source) = title(c.name.as_deref(), c.preview.as_deref());
            let mut entry = NavigatorEntry {
                id: c.id.clone(), home: Some(c.home.clone()), project_root: None, project_source: ProjectSource::ReportedFolder,
                title, title_source, created_at: c.created.map(rfc3339), updated_at: c.updated.map(rfc3339),
                live: c.live, needs_answer: c.waiting, archived: false, open: c.open, run, run_count, children_running: None,
            };
            let place = if let Some(project) = recorded(Some(&c.home), &c.id) {
                entry.project_source = ProjectSource::Recorded;
                Some(project.to_owned())
            } else {
                match c.cwd.as_deref() {
                    Some(cwd) if section_of(&sections, cwd).is_some() => Some(cwd.to_owned()),
                    Some(cwd) if g.no_project_folders.iter().any(|f| f == cwd) => None,
                    Some(cwd) => Some(cwd.to_owned()),
                    None => None,
                }
            };
            match place {
                Some(root) => {
                    let at = section_of(&sections, &root).unwrap_or_else(|| { sections.push(folder_section(&root)); sections.len() - 1 });
                    entry.project_root = Some(sections[at].project.root.clone());
                    sections[at].project.entries.push(entry);
                }
                None => {
                    entry.project_root = c.cwd.clone();
                    unassigned.push(entry);
                }
            }
        }
    }
    // A conversation named only by a run record: its run is still shown.
    let homes_read: BTreeMap<&str, bool> = conversations.iter().map(|c| (c.home.as_str(), c.outcome == ReadOutcome::Read)).collect();
    for (thread, runs) in &runs_of {
        if seen.contains(*thread) { continue; }
        let homes: BTreeSet<&str> = g.index.iter().filter(|r| r.thread == *thread).map(|r| r.home.as_str()).collect();
        let home = (homes.len() == 1).then(|| homes.iter().next().unwrap().to_string());
        let (run, run_count) = run_part(thread);
        let read = home.as_deref().and_then(|h| homes_read.get(h).copied());
        let reason = match read {
            Some(true) => "This conversation is in the App's records but not in the list Codex gave for its home (it may have been archived or removed), so it cannot be opened from here.",
            Some(false) => "This conversation is known from a run record only, and its home's conversations were not read, so it cannot be opened from here yet.",
            None => "This conversation is known from a run record only, and the App does not know which Codex home holds it, so it cannot be opened from here.",
        };
        let waiting = home.as_deref().and_then(|h| g.homes.iter().find(|x| x.class == h))
            .and_then(|x| x.waiting.iter().find(|(t, _)| t == thread)).map_or(0, |(_, n)| *n);
        let (root, source) = match recorded(home.as_deref(), thread) {
            Some(project) => (project.to_owned(), ProjectSource::Recorded),
            None => (runs[0].1.to_owned(), ProjectSource::RunRecord),
        };
        let entry = NavigatorEntry {
            id: thread.to_string(), home, project_root: None, project_source: source, title: None, title_source: TitleSource::None,
            created_at: None, updated_at: None, live: Live::Unknown, needs_answer: waiting, archived: false,
            open: OpenWith::NotOpenable { reason: reason.into() }, run, run_count, children_running: None,
        };
        let at = section_of(&sections, &root).unwrap_or_else(|| { sections.push(folder_section(&root)); sections.len() - 1 });
        let mut entry = entry;
        entry.project_root = Some(sections[at].project.root.clone());
        sections[at].project.entries.push(entry);
    }

    for s in &mut sections { sort_entries(&mut s.project.entries); }
    sort_entries(&mut unassigned);
    sections.sort_by(|a, b| {
        let newest = |s: &Section| s.project.entries.first().and_then(|e| e.updated_at.clone());
        b.project.current.cmp(&a.project.current)
            .then_with(|| match (newest(a), newest(b)) {
                (Some(x), Some(y)) => y.cmp(&x),
                (Some(_), None) => std::cmp::Ordering::Less,
                (None, Some(_)) => std::cmp::Ordering::Greater,
                (None, None) => std::cmp::Ordering::Equal,
            })
            .then_with(|| a.position.unwrap_or(usize::MAX).cmp(&b.position.unwrap_or(usize::MAX)))
            .then_with(|| a.project.root.cmp(&b.project.root))
    });
    let mut projects: Vec<NavigatorProject> = sections.into_iter().map(|s| s.project).collect();
    widen_labels(&mut projects);
    NavigatorRead { read_at: g.read_at, projects, unassigned, conversations, registry_limits }
}

fn section(root: &str, folder: Option<&FolderInput>, listing: Option<&crate::records_store::ListedFolder>, current: bool) -> Section {
    let identities = listing.map(|l| l.identities.clone()).unwrap_or_default();
    let only = (identities.len() == 1).then(|| identities[0].clone());
    let mut project_id = only.clone();
    let mut state = if current { ProjectState::Open } else { ProjectState::Listed };
    let notice;
    let not_attempted;
    match folder.map(|f| &f.examined) {
        Some(Examined::Gone) => {
            state = ProjectState::Unavailable;
            notice = Some(ProjectNotice { kind: "gone".into(), message: "The folder is not there any more; its conversations stay listed, and its recorded runs cannot be read until it is located.".into(), resolutions: vec![] });
            not_attempted = "The folder is not there, so its recorded runs cannot be read until it is located.".to_owned();
        }
        Some(Examined::Unexaminable(e)) => {
            state = ProjectState::Unavailable;
            notice = Some(ProjectNotice { kind: "unavailable".into(), message: format!("The folder could not be examined ({e})."), resolutions: vec![] });
            not_attempted = "The folder could not be examined, so its recorded runs were not read.".to_owned();
        }
        Some(Examined::StoreUnavailable(e)) => {
            notice = None;
            not_attempted = format!("The records store could not be read ({e}), so the recorded runs were not read.");
        }
        Some(Examined::Attached { project, fault, refusal, resolutions }) => {
            if project.is_some() { project_id = project.clone(); }
            notice = match fault {
                Some(fault) => Some(ProjectNotice { kind: fault.clone(), message: fault_message(fault), resolutions: resolutions.clone() }),
                None if project.is_none() && only.is_none() => Some(no_identity()),
                None => None,
            };
            not_attempted = match (fault, refusal) {
                (Some(_), _) => "Its recorded runs are not read until the folder's link to its records is resolved.".to_owned(),
                (None, Some(refusal)) => format!("Its recorded runs were not read ({refusal})."),
                (None, None) => "Its recorded runs were not read.".to_owned(),
            };
        }
        None => {
            notice = (only.is_none()).then(no_identity);
            not_attempted = "Its recorded runs were not read.".to_owned();
        }
    }
    let runs_read = match folder.map(|f| &f.runs) {
        Some(RunsInput::Read { limits, .. }) => RunsRead { outcome: ReadOutcome::Read, limits: limits.clone() },
        Some(RunsInput::NotRead(reason)) => RunsRead { outcome: ReadOutcome::NotRead { reason: format!("The recorded runs were not read ({reason}).") }, limits: vec![] },
        Some(RunsInput::NotAttempted) | None => RunsRead { outcome: ReadOutcome::NotRead { reason: not_attempted }, limits: vec![] },
    };
    Section {
        project: NavigatorProject { project_id, root: root.to_owned(), label: String::new(), current, state, notice, runs_read, entries: vec![] },
        position: listing.map(|l| l.first_line),
    }
}

/// A folder no listed project names: shown so its conversations are not hidden.
fn folder_section(root: &str) -> Section {
    Section {
        project: NavigatorProject {
            project_id: None, root: root.to_owned(), label: String::new(), current: false, state: ProjectState::Listed,
            notice: Some(no_identity()),
            runs_read: RunsRead { outcome: ReadOutcome::NotRead { reason: "This folder has no project identity in the records store, so no runs are recorded for it there.".into() }, limits: vec![] },
            entries: vec![],
        },
        position: None,
    }
}

fn no_identity() -> ProjectNotice {
    ProjectNotice { kind: "no-identity".into(), message: "This folder has no project identity in the records store; its conversations are shown here by the folder Codex reports or the App recorded.".into(), resolutions: vec![] }
}

/// One sentence for each of the store's fault words.
fn fault_message(fault: &str) -> String {
    match fault {
        "link missing" => "The folder's project link (.chirality/project.json) is missing, so its records are not read until the link is restored or the folder is given a new identity.".into(),
        "link unreadable" => "The folder's project link (.chirality/project.json) cannot be read, so its records are not read until it is restored or the folder is given a new identity.".into(),
        "link changed" => "The folder's project link names another project than the records store recorded here, so nothing is read for it until that is resolved.".into(),
        "link names another store" => "The folder's project link names another records store, so nothing is read for it until the link is restored.".into(),
        "several identities" => "The records store records this folder for several projects, so nothing is read for it until one is chosen.".into(),
        "moved" => "This folder's project is recorded at another folder, so nothing is read here until you confirm this is that project or give it a new identity.".into(),
        "duplicated" => "This folder carries the identity of another project folder, so nothing is read here until it is given a new identity.".into(),
        "another store" => "This project's records were kept in another records store, so nothing is read here until it is adopted into this one.".into(),
        "no folder recorded" => "The records store holds this project's identity with no folder recorded for it, so nothing is read here until you confirm this folder is that project.".into(),
        "association not known" => "The records store's list of project folders ends in an incomplete line, so which project this folder belongs to is not known yet.".into(),
        other => format!("The records store reports this folder as {other}, so nothing is read for it until that is resolved."),
    }
}

/// The conversations one home reports, and whether its list was read.
fn home_conversations(home: &HomeInput) -> (Vec<Conversation>, ReadOutcome) {
    let history = home.history.as_ref().filter(|h| home.current && h.generation == home.generation);
    let outcome = if !home.current {
        ReadOutcome::NotRead { reason: match home.state.as_str() {
            "absent" => "Codex is not running for this home, so its conversations were not read.".into(),
            "ready" => "The Codex that was running for this home has ended, so its conversations were not read.".into(),
            state => format!("Codex is not ready for this home (it is {state}), so its conversations were not read."),
        } }
    } else if history.is_none() {
        ReadOutcome::NotRead { reason: "The App holds no list of this home's conversations from the Codex now running.".into() }
    } else {
        let ready = history.and_then(|h| h.read_at_ready.as_ref()).filter(|r| r["generation"] == home.generation);
        match ready.and_then(|r| r["state"].as_str()) {
            Some("read-to-end") => ReadOutcome::Read,
            Some("reading") => ReadOutcome::NotRead { reason: "The App is still reading this home's list of conversations.".into() },
            Some("stopped") => ReadOutcome::NotRead { reason: format!("The list of this home's conversations was not read to its end: {}.", ready.and_then(|r| r["reason"].as_str()).unwrap_or("the reason was not recorded")) },
            _ => ReadOutcome::NotRead { reason: "The App has not read this home's whole list of conversations since Codex started (only the account home's list is read when Codex becomes ready).".into() },
        }
    };
    let waiting = |thread: &str| home.waiting.iter().find(|(t, _)| t == thread).map_or(0, |(_, n)| *n);
    let children: BTreeSet<&str> = history.into_iter().flat_map(|h| &h.threads)
        .filter(|t| t["parentThreadId"].as_str().is_some_and(|p| !p.is_empty())).filter_map(|t| t["id"].as_str()).collect();
    let mut found: Vec<Conversation> = Vec::new();
    if let Some(h) = history {
        for t in &h.threads {
            let Some(id) = t["id"].as_str().filter(|s| !s.is_empty()) else { continue };
            if children.contains(id) || found.iter().any(|c| c.id == id) { continue; }
            found.push(Conversation {
                home: home.class.clone(), id: id.to_owned(), cwd: text(&t["cwd"]), name: text(&t["name"]), preview: text(&t["preview"]),
                created: t["createdAt"].as_f64(), updated: t["updatedAt"].as_f64(), live: live(&t["status"]),
                open: OpenWith::History { home: home.class.clone(), generation: h.generation.clone(), selection_epoch: h.selection_epoch, thread_id: id.to_owned() },
                waiting: waiting(id),
            });
        }
    }
    if home.current {
        for row in home.loaded.iter().filter(|r| r["generation"] == home.generation) {
            let Some(id) = row["threadId"].as_str().filter(|s| !s.is_empty()) else { continue };
            if children.contains(id) { continue; }
            let open = OpenWith::Loaded { generation: home.generation.clone(), thread_id: id.to_owned() };
            match found.iter_mut().find(|c| c.id == id) {
                Some(c) => {
                    c.open = open;
                    c.live = live(&row["status"]);
                    if let Some(name) = text(&row["name"]) { c.name = Some(name); }
                    if c.preview.is_none() { c.preview = text(&row["preview"]); }
                    if c.cwd.is_none() { c.cwd = text(&row["cwd"]); }
                }
                None => found.push(Conversation {
                    home: home.class.clone(), id: id.to_owned(), cwd: text(&row["cwd"]), name: text(&row["name"]), preview: text(&row["preview"]),
                    created: None, updated: None, live: live(&row["status"]), open, waiting: waiting(id),
                }),
            }
        }
    }
    (found, outcome)
}

fn text(v: &Value) -> Option<String> {
    v.as_str().map(str::to_owned).filter(|s| !s.trim().is_empty())
}

/// Codex's `ThreadStatus` as the navigator shows it.
pub(crate) fn live(status: &Value) -> Live {
    match status["type"].as_str() {
        Some("active") => Live::Running,
        Some("idle") => Live::Idle,
        Some("notLoaded") => Live::NotLoaded,
        _ => Live::Unknown,
    }
}

/// A conversation's title: Codex's `name`, else its `preview` with its
/// whitespace made single spaces and cut to `TITLE_CHARS` characters on a
/// word boundary (a single longer word is cut at the limit), else none.
pub(crate) fn title(name: Option<&str>, preview: Option<&str>) -> (Option<String>, TitleSource) {
    if let Some(name) = name.map(str::trim).filter(|n| !n.is_empty()) {
        return (Some(name.to_owned()), TitleSource::Name);
    }
    let words = preview.map(|p| p.split_whitespace().collect::<Vec<_>>().join(" ")).unwrap_or_default();
    if words.is_empty() {
        return (None, TitleSource::None);
    }
    if words.chars().count() <= TITLE_CHARS {
        return (Some(words), TitleSource::FirstMessage);
    }
    let head: String = words.chars().take(TITLE_CHARS).collect();
    let next_is_space = words.chars().nth(TITLE_CHARS) == Some(' ');
    let cut = if next_is_space { head.as_str() } else { head.rfind(' ').map_or(head.as_str(), |at| &head[..at]) };
    (Some(cut.trim_end().to_owned()), TitleSource::FirstMessage)
}

fn rfc3339(seconds: f64) -> String {
    crate::util::rfc3339_from_ms((seconds * 1000.0).round() as i64)
}

fn entry_run(run: &RunInput, finished: &BTreeMap<&str, Option<bool>>, catalog: &CatalogInput) -> EntryRun {
    let (state, ended_by) = match &run.lifecycle {
        RecordedLifecycle::OpenInterrupted => (RunState::Open, None),
        RecordedLifecycle::Ended { stopped_by, cause } => (RunState::Ended, Some(EndedBy { stopped_by: stopped_by.clone(), cause: cause.clone() })),
        RecordedLifecycle::StartNotConfirmed => (RunState::StartNotConfirmed, None),
        RecordedLifecycle::Unknown(_) => (RunState::Unknown, None),
    };
    let finished_reported = if state == RunState::Open { finished.get(run.run_id.as_str()).copied().flatten() } else { None };
    EntryRun { run_id: run.run_id.clone(), workflow: workflow_words(&run.workflow, catalog), state, ended_by, finished_reported, result_count: None }
}

/// The workflow as the run guide words its source (`RunJourney.tsx`
/// `chosenSource`, `IncludedWorkflows.tsx` `librarySourceWords`): included
/// with the App where the recorded identity is a catalogue entry's (kind,
/// origin, source root, name and revision, and the revision method where
/// recorded); a bundled copy with its source otherwise; else its origin's
/// library.
pub(crate) fn workflow_words(workflow: &Value, catalog: &CatalogInput) -> RunWorkflow {
    let field = |v: &Value, snake: &str, camel: &str| v.get(snake).or_else(|| v.get(camel)).and_then(Value::as_str).map(str::to_owned);
    let name = field(workflow, "name", "name");
    let origin = field(workflow, "origin", "origin");
    let source_root = field(workflow, "source_root", "sourceRoot");
    let method = field(workflow, "revision_method", "revisionMethod");
    let included = catalog.identities.iter().any(|id| {
        ["kind", "origin", "name", "revision"].iter().all(|k| workflow[k].as_str().is_some() && workflow[k] == id[k])
            && source_root.as_deref().is_some_and(|s| id["source_root"] == s)
            && method.as_deref().is_none_or(|m| id["revision_method"] == m)
    });
    let (origin, release) = if included {
        (Some("included with the App".to_owned()), catalog.release.clone())
    } else {
        match origin.as_deref() {
            Some("bundled") => (Some(match source_root.as_deref() { Some(s) if !s.is_empty() => format!("a bundled copy (source {s})"), _ => "a bundled copy".to_owned() }), None),
            Some(o) if !o.is_empty() => (Some(format!("{o} library")), None),
            _ => (None, None),
        }
    };
    RunWorkflow { name, title: None, origin, release }
}

/// The Library release as the run guide words it from the catalogue's source.
pub(crate) fn release_words(source: &Value) -> Option<String> {
    let tag = source["tag"].as_str().unwrap_or("");
    match tag.strip_prefix("library-v") {
        Some(version) if !version.is_empty() => Some(format!("Chirality Library {version}")),
        _ if !tag.is_empty() => Some(format!("Chirality Library ({tag})")),
        _ => None,
    }
}

fn sort_entries(entries: &mut [NavigatorEntry]) {
    entries.sort_by(|a, b| match (&a.updated_at, &b.updated_at) {
        (Some(x), Some(y)) => y.cmp(x),
        (Some(_), None) => std::cmp::Ordering::Less,
        (None, Some(_)) => std::cmp::Ordering::Greater,
        (None, None) => std::cmp::Ordering::Equal,
    }.then_with(|| a.id.cmp(&b.id)));
}

/// Each project's label: its folder's name, or `parent/name` where another
/// project's folder has the same name.
fn widen_labels(projects: &mut [NavigatorProject]) {
    let name = |root: &str| Path::new(root).file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_else(|| root.to_owned());
    let names: Vec<String> = projects.iter().map(|p| name(&p.root)).collect();
    for (i, project) in projects.iter_mut().enumerate() {
        let clash = names.iter().enumerate().any(|(j, n)| j != i && *n == names[i]);
        project.label = match Path::new(&project.root).parent().and_then(Path::file_name) {
            Some(parent) if clash => format!("{}/{}", parent.to_string_lossy(), names[i]),
            _ => names[i].clone(),
        };
    }
}

// ---- Gathering ----

/// `navigator_read`: gather, then compose.
pub(crate) fn read(state: &crate::AppState) -> NavigatorRead {
    compose(gather(state))
}

/// What the read rests on, taken from the App's state. Each lock is taken
/// briefly and none is held across a file read: the Host and history parts
/// are memory, and the store and project folders are read after every lock
/// is released.
fn gather(state: &crate::AppState) -> Gathered {
    let read_at = crate::util::now_rfc3339();
    let homes = state.homes.lock().unwrap().entries();
    let mut inputs = Vec::new();
    let mut index = Vec::new();
    let mut finished = Vec::new();
    for home in &homes {
        let class = home.class();
        let snapshot = home.host.snapshot();
        let generation = snapshot["generation"].clone();
        let current = snapshot["state"] == "ready" && snapshot["generationClosed"] == false;
        let history = {
            let history = home.history.lock().unwrap();
            history.history().map(|view| HistoryInput {
                generation: view.generation().clone(),
                selection_epoch: view.selection_epoch(),
                threads: view.received_threads().cloned().collect(),
                read_at_ready: history.read_at_ready().cloned(),
            })
        };
        let waiting = crate::waiting_requests::groups(class, &snapshot).iter()
            .filter_map(|g| Some((g["threadId"].as_str()?.to_owned(), g["count"].as_u64().unwrap_or(0)))).collect();
        for row in home.host.recovery_entries().iter().filter(|r| r["kind"] == "conversation_index") {
            let class = match row["home"].as_str() { Some("H-acct") => "account", Some("H-key") => "api-key", Some("H-omlx") => "local-provider", _ => continue };
            if let (Some(thread), Some(project)) = (row["threadId"].as_str(), row["project"].as_str()) {
                if !index.iter().any(|r: &IndexRow| r.home == class && r.thread == thread && r.project == project) {
                    index.push(IndexRow { home: class.into(), thread: thread.into(), project: project.into() });
                }
            }
        }
        // As the run guide's offers: only for the view of the generation running now.
        let view = home.runtime.lock().unwrap().native_view();
        if current && view["generation"] == generation && view["home"] == generation["home"] {
            finished.extend(state.workflows.lock().unwrap().finished_offers_in(&view));
        }
        inputs.push(HomeInput {
            class: class.as_str().to_owned(), state: snapshot["state"].as_str().unwrap_or("unknown").to_owned(), generation, current,
            loaded: snapshot["threads"].as_array().cloned().unwrap_or_default(), history, waiting,
        });
    }
    let catalog = crate::workflow_workspace::production_catalog::ProductionCatalog::load()
        .map(|c| CatalogInput { identities: c.entries().filter_map(|e| serde_json::to_value(e.identity()).ok()).collect(), release: release_words(c.source()) })
        .unwrap_or_default();
    let data = state.app_user_data_root.lock().unwrap().clone().ok();
    let mut no_project_folders = Vec::new();
    if let Some(data) = data {
        let folder = crate::working_folder::no_project_folder(&data);
        no_project_folders.extend(folder.to_str().map(str::to_owned));
        if let Ok(resolved) = std::fs::canonicalize(&folder) { no_project_folders.extend(resolved.to_str().map(str::to_owned)); }
    }
    let (current_root, aliases) = match state.workspace.as_deref() {
        None => (None, vec![]),
        Some(path) => {
            let given = path.to_str().map(str::to_owned).unwrap_or_else(|| crate::attachments::native_path_identity(path).to_string());
            let physical = std::fs::canonicalize(path).ok().and_then(|p| p.to_str().map(str::to_owned)).unwrap_or_else(|| given.clone());
            let aliases = if physical != given { vec![(given, physical.clone())] } else { vec![] };
            (Some(physical), aliases)
        }
    };
    let (registry, folders) = gather_projects(current_root.as_deref());
    Gathered { read_at, current_root, aliases, no_project_folders, registry, folders, homes: inputs, index, finished, catalog }
}

/// The store's registry and each listed folder (and the launched project's),
/// examined and its recorded runs read. File reads only; no App lock is held.
pub(crate) fn gather_projects(current: Option<&str>) -> (Result<crate::records_store::ListedFolders, String>, Vec<FolderInput>) {
    let store = crate::records_store::opened_existing().map(|_| ());
    let registry = store.clone().and_then(|_| crate::records_store::listed_folders());
    let mut roots: Vec<String> = current.iter().map(|s| s.to_string()).collect();
    if let Ok(listed) = &registry {
        roots.extend(listed.folders.iter().map(|f| f.root.clone()).filter(|r| Some(r.as_str()) != current));
    }
    let folders = roots.into_iter().map(|root| {
        let (examined, runs) = examine(&root, store.as_ref().err());
        FolderInput { root, examined, runs }
    }).collect();
    (registry, folders)
}

fn examine(root: &str, store: Option<&String>) -> (Examined, RunsInput) {
    let path = Path::new(root);
    match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return (Examined::Gone, RunsInput::NotAttempted),
        Err(e) => return (Examined::Unexaminable(e.to_string()), RunsInput::NotAttempted),
        Ok(_) => {}
    }
    if let Some(error) = store {
        return (Examined::StoreUnavailable(error.clone()), RunsInput::NotAttempted);
    }
    // The store's own status of the folder: its attachment as `attach`
    // without minting gives it, read only (the store's tests hold `status`
    // to writing nothing). No place is taken from it; the runs are read
    // through the reading home's decision below.
    let status = crate::records_store::status(Some(path));
    let Some(view) = status["project"].get("attachment").filter(|a| a.is_object()) else {
        let error = status["project"]["error"].as_str().or_else(|| status["error"].as_str()).unwrap_or("its standing with the records store was not given");
        return (Examined::Unexaminable(error.to_owned()), RunsInput::NotAttempted);
    };
    let string = |key: &str| view[key].as_str().map(str::to_owned);
    let refused = !view["refusal"].is_null();
    let examined = Examined::Attached {
        project: string("projectId"),
        fault: string("fault"),
        refusal: string("refusal"),
        resolutions: view["resolutions"].as_array().into_iter().flatten().filter_map(|r| r.as_str().map(str::to_owned)).collect(),
    };
    if refused {
        return (examined, RunsInput::NotAttempted);
    }
    let runs = match crate::workflow_workspace::publication::ProjectRecords::open(path) {
        Err(e) => RunsInput::NotRead(e),
        Ok(records) => {
            let reading = crate::records::supply::read_project_runs(&records, &[]);
            let runs = reading.runs.into_iter().map(|run| {
                let opened = run.records.iter().find(|e| e["kind"] == "run_opened").and_then(|e| e["writtenAt"].as_str()).map(str::to_owned);
                let latest = run.records.iter().filter_map(|e| e["writtenAt"].as_str()).max().map(str::to_owned);
                RunInput { run_id: run.run, conversation: run.conversation, workflow: run.workflow, lifecycle: run.lifecycle, recorded_at: opened.or(latest) }
            }).collect();
            RunsInput::Read { runs, limits: reading.limits }
        }
    };
    (examined, runs)
}

#[cfg(test)]
#[path = "navigator_read_tests.rs"]
mod tests;
