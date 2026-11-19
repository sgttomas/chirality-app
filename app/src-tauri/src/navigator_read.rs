//! The navigator's one read: every project of the person's records store, and
//! under each its conversations and the workflow runs they carry, as one
//! answer for the left panel (the interface lane's navigator, after 3.0.1's).
//!
//! **A read only.** It changes nothing anywhere, starts nothing and sends
//! nothing to Codex, so it is safe on a timer.
//!
//! - **Other listed projects are enumerated, not read.** For a folder of the
//!   store's registry that is not the launched project, the read takes the
//!   registry's complete lines (`records_store::listed_folders`, which
//!   publishes nothing) and the folder's own `symlink_metadata`, and nothing
//!   else: no status, attachment, census or run reading. So such a project
//!   carries the registry's identity, no store fault word (it is not
//!   examined), and runs not read. The store's readers were made for the one
//!   opened project: reading another project's records through them would
//!   remember its folder for later writers and take its admission.
//! - **The launched project's attachment** comes from `records_store::status`,
//!   which `host_status` reads every second for the same folder. Its recorded
//!   runs are not read.
//! - **Codex's side is memory.** Each home's Host is read through
//!   `Host::navigator_projection` (no reply write is settled, unlike
//!   `snapshot`), its history view through the rows it has received, and its
//!   native view as last received; nothing is dispatched or received.
//!
//! **Where a conversation goes.** Under the project the App recorded for it
//! (the recovery ledger's `conversation_index` row of its home and thread);
//! else under the listed project whose recorded root is exactly the folder
//! Codex reports; else in `unassigned` when that folder is the one set aside
//! for conversations without a project; else under a folder section with no
//! identity, so that no conversation of the sign-in is hidden. A reported
//! folder only places a conversation the App has no record for, and is marked
//! so; it is never written or taken as the App's record. Delegated children
//! (a `parentThreadId` in the list, or a child in the native view's
//! descendants) are not entries; their requests count on their root
//! conversation's entry.
//!
//! The pure composition (`compose`) takes what `gather` collected; the tests
//! drive it with invented material.
use crate::records::supply::RecordedLifecycle;
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};

/// The longest title made from a conversation's preview, in characters.
pub const TITLE_CHARS: usize = 60;
/// The `runsRead` reason of the launched project while its runs are not read.
pub const LAUNCHED_RUNS_NOT_READ: &str = "The navigator does not read the project's recorded runs.";
/// What `conversations[].list` names.
pub const LIST_WORDS: &str = "saved conversations, not archived, as Codex listed them when it became ready";
/// The `runsRead` reason of a listed project that is not the launched one.
pub const NOT_OPEN_RUNS: &str = "Chirality reads a project's recorded runs once the project is open in this running App.";

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
    /// Requests awaiting the person on a thread whose chain of parents reaches
    /// no entry (or on no thread), by home and thread.
    pub unplaced_requests: Vec<UnplacedRequests>,
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

/// One configured Codex home's conversations: `{home, list, readAt, state, reason?}`.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ConversationsRead {
    /// The home class word the host uses (`account`, `api-key`, `local-provider`).
    pub home: String,
    /// Which list this is: `LIST_WORDS`.
    pub list: String,
    /// When that list was read: null, since the App does not record when its
    /// ready-time read finished.
    pub read_at: Option<String>,
    #[serde(flatten)]
    pub outcome: ReadOutcome,
}

#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct NavigatorProject {
    /// The records store's identity of the project (for a listed project not
    /// open here, the registry's), or null for a folder section that has none.
    pub project_id: Option<String>,
    /// The folder path as recorded.
    pub root: String,
    /// The folder's name, widened to `parent/name` where two listed folders
    /// share a name.
    pub label: String,
    /// True for the project new conversations open in (the launched project),
    /// whatever its state.
    pub current: bool,
    pub state: ProjectState,
    pub notice: Option<ProjectNotice>,
    pub runs_read: RunsRead,
    /// Recorded runs of this project that name no conversation (counted, not
    /// shown under any entry).
    pub unplaced_runs: usize,
    /// A loaded entry with no time first, then newest first by `updatedAt`.
    pub entries: Vec<NavigatorEntry>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum ProjectState {
    /// The launched project, attached to its records: usable now.
    Open,
    /// Known, not open in this running App.
    Listed,
    /// The folder is gone or cannot be examined, or (the launched project)
    /// its attachment to its records is refused.
    Unavailable,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct ProjectNotice {
    /// For the launched project, the store's fault word where there is one
    /// (`link missing`, `link unreadable`, `link changed`, `link names another
    /// store`, `several identities`, `moved`, `duplicated`, `another store`,
    /// `no folder recorded`, `association not known`). For any folder, `gone`
    /// (it is not there), `unavailable` (it, or the store, cannot be examined,
    /// or the attachment is refused without a fault word) or `no-identity`.
    /// A listed project that is not the launched one is not examined, so it
    /// never carries a store fault word.
    pub kind: String,
    /// One sentence a person can read.
    pub message: String,
    /// The store's own acts that resolve it (`restore-link`, `adopt`,
    /// `new-identity`); empty where none applies.
    pub resolutions: Vec<String>,
}

/// Whether the project's recorded runs were read.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct RunsRead {
    #[serde(flatten)]
    pub outcome: RunsOutcome,
    /// Every limit the run reader and the store's routing reported, as they
    /// word them (including that originals not yet imported may be missing).
    pub limits: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(tag = "state")]
pub enum RunsOutcome {
    /// Every source read.
    #[serde(rename = "read")]
    Read,
    /// Some sources read, some not: `limits` says which.
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "not-read")]
    NotRead { reason: String },
}

/// One conversation. A conversation that carries a workflow run is that
/// run's entry.
#[derive(Clone, Debug, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct NavigatorEntry {
    /// The thread id.
    pub id: String,
    /// The home class word, or null for a conversation known only from a run
    /// record whose home the App's ledger does not establish.
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
    /// Requests awaiting the person on this conversation's own thread and on
    /// its delegated descendants' threads (from the Host's local register,
    /// walked up the native view's parents to this root).
    pub needs_answer: u64,
    /// Each thread those requests are really on, with its count (this
    /// entry's own thread included when it has some).
    pub needs_answer_on: Vec<RequestsOn>,
    /// False for a row of Codex's list, which holds no archived conversations;
    /// null for a loaded-only or record-only entry, whose standing is not known.
    pub archived: Option<bool>,
    pub open: OpenWith,
    pub run: Option<EntryRun>,
    /// How many recorded runs name this conversation (in its home).
    pub run_count: usize,
    /// Null in this unit: the host holds no count of running descendants
    /// without a further read.
    pub children_running: Option<u64>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RequestsOn {
    pub thread_id: String,
    pub count: u64,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct UnplacedRequests {
    pub home: String,
    /// Null for requests that name no thread.
    pub thread_id: Option<String>,
    pub count: u64,
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
    /// Codex's `preview` (usually, not always, the first message), cut to
    /// `TITLE_CHARS` characters on a word boundary (no ellipsis is added).
    Preview,
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
    /// Why the record leaves the run `unknown`, as the reader says it; null
    /// otherwise.
    pub state_reason: Option<String>,
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
    /// An incomplete or conflicting record (`stateReason` says which).
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
    /// The launched project (examined) and every other listed folder
    /// (enumerated only).
    pub folders: Vec<FolderInput>,
    pub homes: Vec<HomeInput>,
    pub index: Vec<IndexRow>,
    /// Runs this process holds in force: whether the finished report is
    /// offered for each, or `None` where it cannot be told.
    pub finished: Vec<(String, Option<bool>)>,
    pub catalog: CatalogInput,
}

#[derive(Clone)]
pub(crate) struct FolderInput {
    pub root: String,
    pub examined: Examined,
    pub runs: RunsInput,
}

#[derive(Clone)]
pub(crate) enum Examined {
    /// A listed folder that is not the launched project: it is there, and
    /// nothing else of it was read.
    Listed,
    /// The folder is not there.
    Gone,
    /// The folder cannot be examined (the reason as the reader gave it).
    Unexaminable(String),
    /// How the store attaches the launched project (its `status`).
    Attached { project: Option<String>, fault: Option<String>, refusal: Option<String>, resolutions: Vec<String> },
}

#[derive(Clone)]
pub(crate) enum RunsInput {
    /// Not read, for what `Examined` says.
    NotAttempted,
    NotRead(String),
    /// Read; `limits` are the reader's and the routing's, empty when whole.
    Read { runs: Vec<RunInput>, limits: Vec<String> },
}

#[derive(Clone)]
pub(crate) struct RunInput {
    pub run_id: String,
    pub conversation: Option<String>,
    pub workflow: Value,
    pub lifecycle: RecordedLifecycle,
    /// When the run started, as recorded: its run-start record, else its
    /// `run_opened` entry, else its earliest entry. Orders a conversation's runs.
    pub started_at: Option<String>,
}

pub(crate) struct HomeInput {
    /// The home class word.
    pub class: String,
    /// The Host's state word (`ready`, `absent`, ...).
    pub state: String,
    pub generation: Value,
    /// Ready and its generation not closed.
    pub current: bool,
    /// The Host's loaded conversation rows of the current generation.
    pub loaded: Vec<Value>,
    pub history: Option<HistoryInput>,
    /// Requests awaiting the person per thread (null: no thread), current generation.
    pub waiting: Vec<(Option<String>, u64)>,
    /// The native view's delegated children of the current generation, as
    /// (child thread, parent thread).
    pub descendants: Vec<(String, String)>,
}

pub(crate) struct HistoryInput {
    pub generation: Value,
    pub selection_epoch: u64,
    /// The Codex `Thread` rows received.
    pub threads: Vec<Value>,
    pub read_at_ready: Option<Value>,
}

/// A recovery ledger `conversation_index` row: the App's own record of a
/// conversation's project, and the runs it tags there.
pub(crate) struct IndexRow {
    /// The home class word.
    pub home: String,
    pub thread: String,
    /// The project reference the App recorded (the launched root as given).
    pub project: String,
    /// The run identities the row tags (owner `run_restart::RUN_TAG_OWNER`).
    pub runs: Vec<String>,
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
    id: String,
    cwd: Option<String>,
    name: Option<String>,
    preview: Option<String>,
    created: Option<f64>,
    updated: Option<f64>,
    live: Live,
    open: OpenWith,
    archived: Option<bool>,
}

/// Where an entry goes before the sections are final.
enum Target {
    Root(String),
    Unassigned,
}

/// A run with the home the App's ledger establishes for it, and the folder
/// whose records hold it.
struct PlacedRun<'a> {
    run: &'a RunInput,
    home: Option<String>,
    folder: &'a str,
    order: usize,
}

/// The read, composed from what was gathered. Pure.
pub(crate) fn compose(g: Gathered) -> NavigatorRead {
    let (listed, registry_limits) = match &g.registry {
        Ok(r) => (r.folders.clone(), r.torn.iter().cloned().chain(r.limits.iter().cloned()).collect::<Vec<_>>()),
        Err(e) => (vec![], vec![format!("The records store's list of project folders was not read ({e}), so only the project open now is shown.")]),
    };
    let mut sections: Vec<Section> = Vec::new();
    let mut roots: Vec<String> = g.current_root.iter().cloned().collect();
    roots.extend(listed.iter().map(|f| f.root.clone()).filter(|r| Some(r) != g.current_root.as_ref()));
    for root in &roots {
        let folder = g.folders.iter().find(|f| &f.root == root);
        let listing = listed.iter().find(|f| &f.root == root);
        sections.push(section(root, folder, listing, g.current_root.as_ref() == Some(root)));
    }
    let resolve = |root: &str| -> String { g.aliases.iter().find(|(alias, _)| alias == root).map_or(root, |(_, to)| to.as_str()).to_owned() };

    // The conversations each current home reports.
    let mut reported: Vec<(String, Conversation)> = Vec::new();
    let mut conversations = Vec::new();
    for home in &g.homes {
        let (found, outcome) = home_conversations(home);
        conversations.push(ConversationsRead { home: home.class.clone(), list: LIST_WORDS.into(), read_at: None, outcome });
        reported.extend(found.into_iter().map(|c| (home.class.clone(), c)));
    }
    let children: BTreeSet<(&str, &str)> = g.homes.iter().flat_map(|h| h.descendants.iter().map(move |(c, _)| (h.class.as_str(), c.as_str()))).collect();

    // Recorded runs, each with its home where the App's ledger establishes it.
    let known_homes = |thread: &str| -> BTreeSet<&str> {
        reported.iter().filter(|(_, c)| c.id == thread).map(|(h, _)| h.as_str())
            .chain(g.index.iter().filter(|r| r.thread == thread).map(|r| r.home.as_str())).collect()
    };
    let mut placed: Vec<PlacedRun> = Vec::new();
    let mut unplaced_runs: BTreeMap<&str, usize> = BTreeMap::new();
    for folder in &g.folders {
        if let RunsInput::Read { runs, .. } = &folder.runs {
            for run in runs {
                let Some(thread) = run.conversation.as_deref() else { *unplaced_runs.entry(folder.root.as_str()).or_default() += 1; continue };
                if placed.iter().any(|p| p.run.run_id == run.run_id) { continue; }
                let tagged: BTreeSet<&str> = g.index.iter().filter(|r| r.thread == thread && r.runs.iter().any(|x| x == &run.run_id)).map(|r| r.home.as_str()).collect();
                let homes = if tagged.is_empty() { known_homes(thread) } else { tagged };
                let home = (homes.len() == 1).then(|| homes.iter().next().unwrap().to_string());
                placed.push(PlacedRun { run, home, folder: folder.root.as_str(), order: placed.len() });
            }
        }
    }
    let finished: BTreeMap<&str, Option<bool>> = g.finished.iter().map(|(r, f)| (r.as_str(), *f)).collect();
    let runs_for = |home: Option<&str>, thread: &str| -> Vec<&PlacedRun> {
        placed.iter().filter(|p| p.run.conversation.as_deref() == Some(thread) && p.home.as_deref() == home).collect()
    };
    let run_part = |runs: &[&PlacedRun]| -> (Option<EntryRun>, usize) {
        let latest = runs.iter().max_by(|a, b| (a.run.started_at.as_deref(), a.order).cmp(&(b.run.started_at.as_deref(), b.order)));
        (latest.map(|p| entry_run(p.run, &finished, &g.catalog)), runs.len())
    };
    let recorded = |home: Option<&str>, thread: &str| -> Option<String> {
        let rows: Vec<&IndexRow> = g.index.iter().filter(|r| r.thread == thread && home.is_none_or(|h| r.home == h)).collect();
        let projects: BTreeSet<&str> = rows.iter().map(|r| r.project.as_str()).collect();
        // Without a home, only an index that names one project for the thread.
        if home.is_none() && projects.len() != 1 { return None; }
        rows.last().map(|r| resolve(&r.project))
    };
    let listed_root = |root: &str| sections.iter().any(|s| s.project.root == root);

    let mut entries: Vec<(Target, NavigatorEntry)> = Vec::new();
    let mut seen: BTreeSet<(Option<String>, String)> = BTreeSet::new();
    for (home, c) in &reported {
        seen.insert((Some(home.clone()), c.id.clone()));
        let (run, run_count) = run_part(&runs_for(Some(home), &c.id));
        let (title, title_source) = title(c.name.as_deref(), c.preview.as_deref());
        let mut entry = NavigatorEntry {
            id: c.id.clone(), home: Some(home.clone()), project_root: None, project_source: ProjectSource::ReportedFolder,
            title, title_source, created_at: c.created.map(rfc3339), updated_at: c.updated.map(rfc3339),
            live: c.live, needs_answer: 0, needs_answer_on: vec![], archived: c.archived, open: c.open.clone(), run, run_count, children_running: None,
        };
        let target = if let Some(project) = recorded(Some(home), &c.id) {
            entry.project_source = ProjectSource::Recorded;
            Target::Root(project)
        } else {
            match c.cwd.as_deref() {
                Some(cwd) if listed_root(&resolve(cwd)) => Target::Root(resolve(cwd)),
                Some(cwd) if g.no_project_folders.iter().any(|f| f == cwd) => Target::Unassigned,
                Some(cwd) => Target::Root(cwd.to_owned()),
                None => Target::Unassigned,
            }
        };
        if matches!(target, Target::Unassigned) { entry.project_root = c.cwd.clone(); }
        entries.push((target, entry));
    }
    let homes_read: BTreeMap<&str, bool> = conversations.iter().map(|c| (c.home.as_str(), c.outcome == ReadOutcome::Read)).collect();
    let absent_reason = |home: Option<&str>, by_run: bool| -> String {
        let known = if by_run { "This conversation is known from a run record" } else { "This conversation is known from the App's own record" };
        match home.and_then(|h| homes_read.get(h).copied()) {
            Some(true) => format!("{known}, but it is not in the list Codex gave for its home (it may have been archived or removed), so it cannot be opened from here."),
            Some(false) => format!("{known} only, and its home's conversations were not read, so it cannot be opened from here yet."),
            None if home.is_some() => format!("{known} only, and its Codex home is not configured in this App, so it cannot be opened from here."),
            None => format!("{known} only, and the App does not know which Codex home holds it, so it cannot be opened from here."),
        }
    };
    let record_only = |home: Option<String>, thread: &str, source: ProjectSource, root: String, run: Option<EntryRun>, run_count: usize| -> (Target, NavigatorEntry) {
        let reason = absent_reason(home.as_deref(), run.is_some());
        (Target::Root(root), NavigatorEntry {
            id: thread.to_owned(), home, project_root: None, project_source: source, title: None, title_source: TitleSource::None,
            created_at: None, updated_at: None, live: Live::Unknown, needs_answer: 0, needs_answer_on: vec![], archived: None,
            open: OpenWith::NotOpenable { reason }, run, run_count, children_running: None,
        })
    };
    // A conversation named only by a run record: its run is still shown.
    let keys: BTreeSet<(Option<String>, String)> = placed.iter().filter_map(|p| Some((p.home.clone(), p.run.conversation.clone()?))).collect();
    for (home, thread) in keys {
        if seen.contains(&(home.clone(), thread.clone())) { continue; }
        if home.as_deref().is_some_and(|h| children.contains(&(h, thread.as_str()))) { continue; }
        let runs = runs_for(home.as_deref(), &thread);
        let (run, run_count) = run_part(&runs);
        let (root, source) = match recorded(home.as_deref(), &thread) {
            Some(project) => (project, ProjectSource::Recorded),
            None => (runs[0].folder.to_owned(), ProjectSource::RunRecord),
        };
        seen.insert((home.clone(), thread.clone()));
        entries.push(record_only(home, &thread, source, root, run, run_count));
    }
    // A conversation the App recorded, in neither Codex's list nor a run record.
    for row in &g.index {
        let key = (Some(row.home.clone()), row.thread.clone());
        if seen.contains(&key) || children.contains(&(row.home.as_str(), row.thread.as_str())) { continue; }
        seen.insert(key);
        let root = recorded(Some(&row.home), &row.thread).unwrap_or_else(|| resolve(&row.project));
        entries.push(record_only(Some(row.home.clone()), &row.thread, ProjectSource::Recorded, root, None, 0));
    }

    // Requests awaiting the person, counted on the root conversation's entry.
    let mut unplaced_requests = Vec::new();
    for home in g.homes.iter().filter(|h| h.current) {
        let parents: BTreeMap<&str, &str> = home.descendants.iter().map(|(c, p)| (c.as_str(), p.as_str())).collect();
        for (thread, count) in &home.waiting {
            let root = thread.as_deref().map(|t| root_of(t, &parents));
            let at = root.and_then(|r| entries.iter_mut().find(|(_, e)| e.home.as_deref() == Some(home.class.as_str()) && e.id == r));
            match (at, thread) {
                (Some((_, entry)), Some(thread)) => {
                    entry.needs_answer += count;
                    entry.needs_answer_on.push(RequestsOn { thread_id: thread.clone(), count: *count });
                }
                _ => unplaced_requests.push(UnplacedRequests { home: home.class.clone(), thread_id: thread.clone(), count: *count }),
            }
        }
    }

    let mut unassigned = Vec::new();
    for (target, mut entry) in entries {
        match target {
            Target::Unassigned => unassigned.push(entry),
            Target::Root(root) => {
                let at = sections.iter().position(|s| s.project.root == root).unwrap_or_else(|| { sections.push(folder_section(&root)); sections.len() - 1 });
                entry.project_root = Some(sections[at].project.root.clone());
                sections[at].project.entries.push(entry);
            }
        }
    }
    for s in &mut sections {
        if let Some(n) = unplaced_runs.get(s.project.root.as_str()).copied().filter(|n| *n > 0) {
            s.project.unplaced_runs = n;
            s.project.runs_read.limits.push(format!("{n} recorded run{} of this project name{} no conversation, so {} not shown under any conversation.", if n == 1 { "" } else { "s" }, if n == 1 { "s" } else { "" }, if n == 1 { "it is" } else { "they are" }));
            if s.project.runs_read.outcome == RunsOutcome::Read { s.project.runs_read.outcome = RunsOutcome::Partial; }
        }
        sort_entries(&mut s.project.entries);
    }
    sort_entries(&mut unassigned);
    sections.sort_by(|a, b| {
        let newest = |s: &Section| s.project.entries.iter().filter_map(|e| e.updated_at.clone()).max();
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
    NavigatorRead { read_at: g.read_at, projects, unassigned, conversations, registry_limits, unplaced_requests }
}

/// A thread's root conversation by the native view's parents (a cycle stops
/// where it repeats), as `WaitingOnYou.tsx` `rootConversation` walks it.
fn root_of<'a>(thread: &'a str, parents: &BTreeMap<&'a str, &'a str>) -> &'a str {
    let mut current = thread;
    let mut seen = BTreeSet::new();
    while seen.insert(current) {
        match parents.get(current) {
            Some(parent) if !parent.is_empty() => current = parent,
            _ => break,
        }
    }
    current
}

fn section(root: &str, folder: Option<&FolderInput>, listing: Option<&crate::records_store::ListedFolder>, current: bool) -> Section {
    let identities = listing.map(|l| l.identities.clone()).unwrap_or_default();
    let mut project_id = (identities.len() == 1).then(|| identities[0].clone());
    let unavailable = |kind: &str, message: String| Some(ProjectNotice { kind: kind.into(), message, resolutions: vec![] });
    let (state, notice, not_attempted) = match folder.map(|f| &f.examined) {
        _ if !current && folder.is_none_or(|f| matches!(f.examined, Examined::Listed)) => (ProjectState::Listed, None, NOT_OPEN_RUNS.to_owned()),
        Some(Examined::Gone) => (ProjectState::Unavailable, Some(ProjectNotice { kind: "gone".into(), message: "The folder is not there any more; its conversations stay listed, and its recorded runs cannot be read until it is located.".into(), resolutions: vec![] }),
            if current { "The folder is not there, so its recorded runs cannot be read until it is located.".to_owned() } else { NOT_OPEN_RUNS.to_owned() }),
        Some(Examined::Unexaminable(e)) => (ProjectState::Unavailable, unavailable("unavailable", format!("The folder could not be examined ({e}).")),
            if current { "The folder could not be examined, so its recorded runs were not read.".to_owned() } else { NOT_OPEN_RUNS.to_owned() }),
        Some(Examined::Attached { project, fault, refusal, resolutions }) => {
            if project.is_some() { project_id = project.clone(); }
            match (fault, refusal, project) {
                (Some(fault), _, _) => (ProjectState::Unavailable, Some(ProjectNotice { kind: fault.clone(), message: fault_message(fault), resolutions: resolutions.clone() }),
                    "Its recorded runs are not read until the folder's link to its records is resolved.".to_owned()),
                (None, Some(refusal), _) => (ProjectState::Unavailable, unavailable("unavailable", format!("The records store does not attach this folder to its records ({refusal})."), ),
                    format!("Its recorded runs were not read ({refusal}).")),
                (None, None, None) => (ProjectState::Unavailable, Some(no_identity()), "Its recorded runs were not read.".to_owned()),
                (None, None, Some(_)) => (if current { ProjectState::Open } else { ProjectState::Listed }, None, "Its recorded runs were not read.".to_owned()),
            }
        }
        Some(Examined::Listed) | None => (if current { ProjectState::Open } else { ProjectState::Listed }, (project_id.is_none()).then(no_identity), NOT_OPEN_RUNS.to_owned()),
    };
    let runs_read = match folder.map(|f| &f.runs) {
        Some(RunsInput::Read { limits, .. }) => RunsRead { outcome: if limits.is_empty() { RunsOutcome::Read } else { RunsOutcome::Partial }, limits: limits.clone() },
        Some(RunsInput::NotRead(reason)) => RunsRead { outcome: RunsOutcome::NotRead { reason: reason.clone() }, limits: vec![] },
        Some(RunsInput::NotAttempted) | None => RunsRead { outcome: RunsOutcome::NotRead { reason: not_attempted }, limits: vec![] },
    };
    Section {
        project: NavigatorProject { project_id, root: root.to_owned(), label: String::new(), current, state, notice, runs_read, unplaced_runs: 0, entries: vec![] },
        position: listing.map(|l| l.first_line),
    }
}

/// A folder no listed project names: shown so its conversations are not hidden.
fn folder_section(root: &str) -> Section {
    Section {
        project: NavigatorProject {
            project_id: None, root: root.to_owned(), label: String::new(), current: false, state: ProjectState::Listed,
            notice: Some(no_identity()),
            runs_read: RunsRead { outcome: RunsOutcome::NotRead { reason: "This folder has no project identity in the records store, so no runs are recorded for it there.".into() }, limits: vec![] },
            unplaced_runs: 0,
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
    let mut children: BTreeSet<&str> = home.descendants.iter().map(|(c, _)| c.as_str()).collect();
    children.extend(history.into_iter().flat_map(|h| &h.threads)
        .filter(|t| t["parentThreadId"].as_str().is_some_and(|p| !p.is_empty())).filter_map(|t| t["id"].as_str()));
    let mut found: Vec<Conversation> = Vec::new();
    if let Some(h) = history {
        for t in &h.threads {
            let Some(id) = t["id"].as_str().filter(|s| !s.is_empty()) else { continue };
            if children.contains(id) || found.iter().any(|c| c.id == id) { continue; }
            found.push(Conversation {
                id: id.to_owned(), cwd: text(&t["cwd"]), name: text(&t["name"]), preview: text(&t["preview"]),
                created: t["createdAt"].as_f64(), updated: t["updatedAt"].as_f64(), live: live(&t["status"]),
                open: OpenWith::History { home: home.class.clone(), generation: h.generation.clone(), selection_epoch: h.selection_epoch, thread_id: id.to_owned() },
                archived: Some(false),
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
                    id: id.to_owned(), cwd: text(&row["cwd"]), name: text(&row["name"]), preview: text(&row["preview"]),
                    created: None, updated: None, live: live(&row["status"]), open, archived: None,
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
        return (Some(words), TitleSource::Preview);
    }
    let head: String = words.chars().take(TITLE_CHARS).collect();
    let next_is_space = words.chars().nth(TITLE_CHARS) == Some(' ');
    let cut = if next_is_space { head.as_str() } else { head.rfind(' ').map_or(head.as_str(), |at| &head[..at]) };
    (Some(cut.trim_end().to_owned()), TitleSource::Preview)
}

fn rfc3339(seconds: f64) -> String {
    crate::util::rfc3339_from_ms((seconds * 1000.0).round() as i64)
}

fn entry_run(run: &RunInput, finished: &BTreeMap<&str, Option<bool>>, catalog: &CatalogInput) -> EntryRun {
    let (state, state_reason, ended_by) = match &run.lifecycle {
        RecordedLifecycle::OpenInterrupted => (RunState::Open, None, None),
        RecordedLifecycle::Ended { stopped_by, cause } => (RunState::Ended, None, Some(EndedBy { stopped_by: stopped_by.clone(), cause: cause.clone() })),
        RecordedLifecycle::StartNotConfirmed => (RunState::StartNotConfirmed, None, None),
        RecordedLifecycle::Unknown(reason) => (RunState::Unknown, Some(reason.clone()), None),
    };
    let finished_reported = if state == RunState::Open { finished.get(run.run_id.as_str()).copied().flatten() } else { None };
    EntryRun { run_id: run.run_id.clone(), workflow: workflow_words(&run.workflow, catalog), state, state_reason, ended_by, finished_reported, result_count: None }
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

/// A loaded entry with no time first (it is in use now and not yet in the
/// list read), then newest first by `updatedAt`, then any other entry with no
/// time; ties by thread id.
fn sort_entries(entries: &mut [NavigatorEntry]) {
    let group = |e: &NavigatorEntry| match (&e.updated_at, &e.open) {
        (None, OpenWith::Loaded { .. }) => 0,
        (Some(_), _) => 1,
        (None, _) => 2,
    };
    entries.sort_by(|a, b| group(a).cmp(&group(b)).then_with(|| b.updated_at.cmp(&a.updated_at)).then_with(|| a.id.cmp(&b.id)));
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

/// What the read is taken from: the App's state, or a test's own parts.
pub(crate) struct Sources<'a> {
    pub homes: Vec<std::sync::Arc<crate::runtime_session::HomeSession>>,
    pub workflows: &'a std::sync::Mutex<crate::runtime_session::WorkflowRootSession>,
    pub workspace: Option<&'a Path>,
    pub app_data: Option<PathBuf>,
}

/// `navigator_read`: gather, then compose.
pub(crate) fn read(state: &crate::AppState) -> NavigatorRead {
    let homes = state.homes.lock().unwrap().entries();
    let app_data = state.app_user_data_root.lock().unwrap().clone().ok();
    read_from(Sources { homes, workflows: &state.workflows, workspace: state.workspace.as_deref(), app_data })
}

/// The read as the command makes it, from its sources.
pub(crate) fn read_from(sources: Sources) -> NavigatorRead {
    compose(gather(sources))
}

/// What the read rests on. Each lock is taken briefly and none is held across
/// a file read: the Host, history and native views are memory, and the store
/// and project folders are read after every lock is released.
fn gather(sources: Sources) -> Gathered {
    let read_at = crate::util::now_rfc3339();
    let mut homes = Vec::new();
    let mut index = Vec::new();
    let mut finished = Vec::new();
    for home in &sources.homes {
        let class = home.class();
        let host = home.host.navigator_projection();
        let current = host.state == "ready" && !host.generation_closed;
        let history = {
            let history = home.history.lock().unwrap();
            history.history().map(|view| HistoryInput {
                generation: view.generation().clone(),
                selection_epoch: view.selection_epoch(),
                threads: view.received_threads().cloned().collect(),
                read_at_ready: history.read_at_ready().cloned(),
            })
        };
        let waiting = crate::waiting_requests::groups_in(class, &json!(host.state), &host.generation, &host.server_requests).iter()
            .map(|g| (g["threadId"].as_str().map(str::to_owned), g["count"].as_u64().unwrap_or(0))).collect();
        for row in &host.conversation_index {
            let class = match row["home"].as_str() { Some("H-acct") => "account", Some("H-key") => "api-key", Some("H-omlx") => "local-provider", _ => continue };
            let (Some(thread), Some(project)) = (row["threadId"].as_str(), row["project"].as_str()) else { continue };
            let runs: Vec<String> = row["tags"].as_array().into_iter().flatten()
                .filter(|t| t["owner"] == crate::run_restart::RUN_TAG_OWNER).filter_map(|t| t["value"].as_str().map(str::to_owned)).collect();
            match index.iter_mut().find(|r: &&mut IndexRow| r.home == class && r.thread == thread && r.project == project) {
                Some(r) => for x in runs { if !r.runs.contains(&x) { r.runs.push(x); } },
                None => index.push(IndexRow { home: class.into(), thread: thread.into(), project: project.into(), runs }),
            }
        }
        // The native view as last received (no frame is received here): the
        // delegated children, and the run guide's finished-report reading.
        let view = home.runtime.lock().unwrap().native_view();
        let view_current = current && view["generation"] == host.generation && view["home"] == host.generation["home"];
        let descendants = if view_current {
            view["descendants"].as_array().into_iter().flatten()
                .filter_map(|n| Some((n["threadId"].as_str()?.to_owned(), n["parentThreadId"].as_str().filter(|p| !p.is_empty())?.to_owned()))).collect()
        } else { vec![] };
        if view_current {
            finished.extend(sources.workflows.lock().unwrap().finished_offers_in(&view));
        }
        homes.push(HomeInput {
            class: class.as_str().to_owned(), state: host.state, generation: host.generation, current,
            loaded: host.threads, history, waiting, descendants,
        });
    }
    let catalog = crate::workflow_workspace::production_catalog::ProductionCatalog::load()
        .map(|c| CatalogInput { identities: c.entries().filter_map(|e| serde_json::to_value(e.identity()).ok()).collect(), release: release_words(c.source()) })
        .unwrap_or_default();
    let mut no_project_folders = Vec::new();
    if let Some(data) = sources.app_data.as_deref() {
        let folder = crate::working_folder::no_project_folder(data);
        no_project_folders.extend(folder.to_str().map(str::to_owned));
        if let Ok(resolved) = std::fs::canonicalize(&folder) { no_project_folders.extend(resolved.to_str().map(str::to_owned)); }
    }
    let (current_root, aliases) = match sources.workspace {
        None => (None, vec![]),
        Some(path) => {
            let given = path.to_str().map(str::to_owned).unwrap_or_else(|| crate::attachments::native_path_identity(path).to_string());
            let physical = std::fs::canonicalize(path).ok().and_then(|p| p.to_str().map(str::to_owned)).unwrap_or_else(|| given.clone());
            let aliases = if physical != given { vec![(given, physical.clone())] } else { vec![] };
            (Some(physical), aliases)
        }
    };
    let (registry, folders) = gather_projects(current_root.as_deref());
    Gathered { read_at, current_root, aliases, no_project_folders, registry, folders, homes, index, finished, catalog }
}

/// The store's registry, the launched project's attachment and every other
/// listed folder enumerated. File reads only; no App lock is held.
fn gather_projects(current: Option<&str>) -> (Result<crate::records_store::ListedFolders, String>, Vec<FolderInput>) {
    let registry = crate::records_store::listed_folders();
    let mut folders: Vec<FolderInput> = current.iter().map(|root| launched(root)).collect();
    if let Ok(listed) = &registry {
        folders.extend(listed.folders.iter().filter(|f| Some(f.root.as_str()) != current).map(|f| enumerate(&f.root)));
    }
    (registry, folders)
}

/// A listed folder that is not the launched project: its own metadata only.
fn enumerate(root: &str) -> FolderInput {
    let examined = match std::fs::symlink_metadata(root) {
        Ok(meta) if meta.is_dir() => Examined::Listed,
        Ok(_) => Examined::Unexaminable("it is not a folder".into()),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Examined::Gone,
        Err(e) => Examined::Unexaminable(e.to_string()),
    };
    FolderInput { root: root.to_owned(), examined, runs: RunsInput::NotAttempted }
}

/// The launched project's attachment, as the store's `status` gives it. Its
/// recorded runs are not read here.
fn launched(root: &str) -> FolderInput {
    let path = Path::new(root);
    match std::fs::symlink_metadata(path) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return FolderInput { root: root.into(), examined: Examined::Gone, runs: RunsInput::NotAttempted },
        Err(e) => return FolderInput { root: root.into(), examined: Examined::Unexaminable(e.to_string()), runs: RunsInput::NotAttempted },
        Ok(_) => {}
    }
    let status = crate::records_store::status(Some(path));
    let Some(view) = status["project"].get("attachment").filter(|a| a.is_object()) else {
        let error = status["project"]["error"].as_str().or_else(|| status["error"].as_str()).unwrap_or("its standing with the records store was not given");
        return FolderInput { root: root.into(), examined: Examined::Unexaminable(error.to_owned()), runs: RunsInput::NotAttempted };
    };
    let string = |key: &str| view[key].as_str().map(str::to_owned);
    let examined = Examined::Attached {
        project: string("projectId"),
        fault: string("fault"),
        refusal: string("refusal"),
        resolutions: view["resolutions"].as_array().into_iter().flatten().filter_map(|r| r.as_str().map(str::to_owned)).collect(),
    };
    FolderInput { root: root.into(), examined, runs: RunsInput::NotRead(LAUNCHED_RUNS_NOT_READ.to_owned()) }
}

#[cfg(test)]
#[path = "navigator_read_tests.rs"]
mod tests;
