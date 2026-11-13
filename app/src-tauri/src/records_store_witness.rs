//! The store's witness of legacy imports: `<store>/legacy-imports.jsonl` (a
//! layout addition, decided by App Agent 0). It is written by the store's
//! appender under the store lock, outside every project's subtree, so it
//! survives the disposal of a project's payload and the loss of the project's
//! own import account (`imports.jsonl`, unchanged in form).
//!
//! - Its first line records when the witness began, whether the store
//!   already existed then, and the store folder key of every project present
//!   at that moment (`projectsPresent`), listed under the store lock from the
//!   store's project folders and from its registry ([`BEGAN_FORMAT`]). That
//!   list is the boundary: a project named in it predates the witness, a
//!   project not named in it was made after, and no time is compared. A
//!   project's store folder key comes from its identity and no act changes
//!   it: giving a folder a new identity makes a new project with its own
//!   folder and leaves the earlier project, its records and its key as they
//!   were. If the projects cannot be listed whole (a folder that cannot be
//!   read, a registry not read whole) the witness does not begin and the act
//!   that would have begun it is refused; a partial list is never written.
//!   The list is never changed afterwards, and a witness begins once: if the
//!   file is lost and a new one begins, every project then present is in the
//!   new list, which errs toward "origin not established" and never toward
//!   "no import". The file is created whole, with
//!   that line and, for every project whose import account was readable and
//!   held an import then, one line per import marked as established from that
//!   account when the witness began ([`FROM_ACCOUNT`]) — never taken for a line
//!   written before the copies. So that backfill happens once and only once:
//!   it exists exactly when the file does.
//! - The witness begins at the first of: the startup recovery, a project's
//!   registration (before its identity record is created, so a project
//!   created after the witness began is known as such), and an import.
//! - Every import writes its line ([`WITNESS_FORMAT`], [`BEFORE_COPIES`])
//!   before its "started" account line and before any copy: wherever imported
//!   bytes exist in a subtree, the witness exists.
//!
//! The reader ([`legacy_import_origin`]): a witness line shows an import
//! was begun (not that anything was copied); for a project not named in the
//! first line's list, no witness line means no import; for a project named
//! there, no witness line and no readable account showing an import means
//! the origin is not established, never "no import". A witness not read
//! whole is an error, never "no import".
use super::*;

pub(crate) const WITNESS_FILE: &str = "legacy-imports.jsonl";
const BEGAN_FORMAT: &str = "chirality.records-store.legacy-imports-began";
const WITNESS_FORMAT: &str = "chirality.records-store.legacy-import";
/// The basis of a line written by an import before any copy.
pub(crate) const BEFORE_COPIES: &str = "written by the import before any copy was made";
/// The basis of a line established from a project's own account when the witness began.
pub(crate) const FROM_ACCOUNT: &str = "established when the witness began, from the project's own import account; not written before the copies";
/// The basis of an import read from the project's account alone, with no witness line.
pub(crate) const ACCOUNT_ONLY: &str = "read from the project's own import account; no witness line holds it";

#[cfg_attr(not(test), allow(dead_code))]
/// One file an import placed (or was to place) in the project's subtree.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct WitnessedFile {
    /// Relative to the project's store folder.
    pub copy: String,
    pub length: u64,
    pub sha256: String,
}
#[cfg_attr(not(test), allow(dead_code))]
/// One import as witnessed.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct WitnessedImport {
    pub import_id: String,
    pub at: String,
    /// Which of [`BEFORE_COPIES`], [`FROM_ACCOUNT`] or [`ACCOUNT_ONLY`].
    pub basis: String,
    pub files: Vec<WitnessedFile>,
}
#[cfg_attr(not(test), allow(dead_code))]
/// What the store shows of a project's legacy import.
#[derive(Clone, Debug, PartialEq)]
pub(crate) enum LegacyOrigin {
    /// The project was not present when the witness began (it is not in the
    /// first line's list), and no import is witnessed.
    NoImport,
    /// Imports shown by the witness (or, failing it, by the project's account).
    Imported(Vec<WitnessedImport>),
    /// Neither an import nor its absence can be established; the reason.
    NotEstablished(String),
}

/// Begins the witness if it has not begun (the caller holds the store lock).
/// Returns what was left out of the backfill, and why.
pub(crate) fn begin(store: &Path) -> Result<Vec<String>, String> {
    let path = store.join(WITNESS_FILE);
    match std::fs::symlink_metadata(&path) {
        Ok(_) => return Ok(vec![]),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(format!("the store's witness of legacy imports is unreadable: {e}; nothing changed")),
    }
    let existed = ["roots.jsonl", "projects"].iter().any(|n| std::fs::symlink_metadata(store.join(n)).is_ok());
    let at = now_rfc3339();
    // The projects present now, listed whole or not at all: every project
    // folder in the store, and every project the registry names.
    let not_begun = "the store's witness of legacy imports was not begun, and nothing changed";
    let mut dirs: Vec<PathBuf> = Vec::new();
    match std::fs::read_dir(store.join("projects")) {
        Ok(rd) => {
            for entry in rd {
                dirs.push(entry.map_err(|e| format!("the store's project folders could not be listed whole ({e}); {not_begun}"))?.path());
            }
        }
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(format!("the store's project folders could not be listed ({e}); {not_begun}")),
    }
    dirs.sort();
    let mut present = std::collections::BTreeSet::new();
    for dir in &dirs {
        present.insert(dir.file_name().and_then(|n| n.to_str()).ok_or_else(|| format!("a project folder's name in the store is not Unicode; {not_begun}"))?.to_owned());
    }
    let (registered, whole, limits) = roots_read(store).map_err(|e| format!("{e}; {not_begun}"))?;
    if !whole {
        return Err(format!("{}; so the projects present cannot be listed whole, and {not_begun}", lines::not_read_whole(&store.join("roots.jsonl"), &limits)));
    }
    for line in &registered {
        if let Some(project) = line["projectId"].as_str() {
            present.insert(folder_key(store, project)?);
        }
    }
    let mut lines = vec![json!({"format":BEGAN_FORMAT,"formatVersion":VERSION,"at":at,"storeExisted":existed,
        "projectsPresent":present.into_iter().collect::<Vec<_>>(),"by":"writer"})];
    let mut left = Vec::new();
    for dir in dirs {
        let Some(project) = project_identity(&dir) else {
            left.push(format!("{}: no readable project identity; no witness line established", dir.display()));
            continue;
        };
        let account = dir.join("imports.jsonl");
        let read = match read_store_file(&account) {
            Ok(read) if read.whole => read,
            Ok(read) => {
                left.push(lines::not_read_whole(&account, &read.limits));
                continue;
            }
            Err(e) => {
                left.push(e);
                continue;
            }
        };
        for (import, at_started, files) in account_imports(&read.values) {
            lines.push(json!({"format":WITNESS_FORMAT,"formatVersion":VERSION,"projectId":project,"importId":import,
                "at":at,"importedAt":at_started,"files":files,"basis":FROM_ACCOUNT}));
        }
    }
    let mut bytes = Vec::new();
    for line in &lines {
        bytes.extend(serde_json::to_vec(line).map_err(|e| e.to_string())?);
        bytes.push(b'\n');
    }
    create_whole(&path, &bytes)?;
    Ok(left)
}
/// The witness line of an import, before any copy (the caller holds the store lock).
pub(crate) fn record(store: &Path, project: &str, import: &str, files: &[WitnessedFile]) -> Result<(), String> {
    begin(store)?;
    let files: Vec<Value> = files.iter().map(|f| json!({"copy":f.copy,"length":f.length,"sha256":f.sha256})).collect();
    append_line(&store.join(WITNESS_FILE), &json!({"format":WITNESS_FORMAT,"formatVersion":VERSION,"projectId":project,"importId":import,
        "at":now_rfc3339(),"files":files,"basis":BEFORE_COPIES}))
}

#[cfg_attr(not(test), allow(dead_code))]
/// For `project` in `store`: whether the witness shows a legacy import, with
/// each imported file's copy path, length and digest. The witness's own
/// unread state is an error, never "no import".
///
/// No product code calls this yet (the decision reader of pull request 247 is
/// to). What a caller may conclude: `Imported`, that an import of this
/// project's was begun (a witness line says begun, not copied); `NoImport`,
/// only that this store's witness, read in full with every line wholly
/// formed, began before the project's folder existed and names no legacy
/// import of it, and that its account (if there) shows none: it says nothing
/// of records that arrived by package import, which carries no witness line,
/// nor of an account removed or cut from outside; `NotEstablished` and an
/// error, that neither can be concluded. A caller may not read
/// `NotEstablished` or an error as "no import".
pub(crate) fn legacy_import_origin(store: &Path, project: &str) -> Result<LegacyOrigin, String> {
    let path = store.join(WITNESS_FILE);
    let dir = project_dir(store, project);
    let present = match std::fs::symlink_metadata(&path) {
        Ok(_) => true,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => false,
        Err(e) => return Err(format!("the store's witness of legacy imports is unreadable: {e}")),
    };
    if !present {
        return Ok(from_account(&dir)?.unwrap_or_else(|| LegacyOrigin::NotEstablished(
            "The origin of this project's records is not established: the store's witness of legacy imports has not begun yet, and the project's own import account shows no import. Until the witness has begun, whether it holds imported records cannot be known.".into())));
    }
    let read = read_store_file(&path)?;
    // Whether every byte of the witness was read: no partial last line, no
    // closed line (named or not) and nothing else left unread. A line left
    // unread may have been this project's; "no import" is never concluded
    // from a witness that was not read in full (review round 4).
    let read_in_full = read.whole && read.limits.is_empty() && read.set_aside.is_empty() && read.unnamed_closures.is_empty() && read.tail.is_none();
    let values = read.require_whole(&path)?;
    let began = values.first().filter(|v| v["format"] == BEGAN_FORMAT && v["formatVersion"] == VERSION)
        .ok_or("the store's witness of legacy imports does not begin with its first line; nothing is concluded from it")?;
    let mut witnessed = Vec::new();
    for value in &values[1..] {
        if value["format"] != WITNESS_FORMAT || value["formatVersion"] != VERSION {
            return Err(format!("the store's witness of legacy imports holds a line of an unknown format ({}); nothing is concluded from it", value["format"]));
        }
        // A line that does not name a project as a string, or is not in its
        // stated form, says nothing of whose import it is: nothing is
        // concluded (review round 4: "not this project" is not evidence).
        let Some(named) = value["projectId"].as_str() else {
            return Err("a line of the store's witness of legacy imports does not name a project in its stated form; nothing is concluded from it".into());
        };
        let import = witnessed_import(value).ok_or("a line of the store's witness of legacy imports is not in its stated form; nothing is concluded from it")?;
        if named == project {
            witnessed.push(import);
        }
    }
    if !witnessed.is_empty() {
        return Ok(LegacyOrigin::Imported(witnessed));
    }
    // An import the project's account shows is never read as no import, even
    // without its witness line (which the App always writes first).
    if let Some(found) = from_account(&dir)? {
        return Ok(found);
    }
    // The boundary is a recorded fact: the projects present when the witness
    // began. No time is compared, and a first line without the list concludes
    // nothing.
    let present = began["projectsPresent"].as_array()
        .and_then(|listed| listed.iter().map(Value::as_str).collect::<Option<Vec<&str>>>())
        .ok_or("the first line of the store's witness of legacy imports does not list the projects present when it began; nothing is concluded from it")?;
    if !present.contains(&folder_key(store, project)?.as_str()) {
        if !read_in_full {
            return Ok(LegacyOrigin::NotEstablished("The origin of this project's records is not established: the store's witness of legacy imports was not read in full (a line in it is partial or closed and not read), and a line left unread may have been an import of this project's.".into()));
        }
        return Ok(LegacyOrigin::NoImport);
    }
    Ok(LegacyOrigin::NotEstablished(format!(
        "The origin of this project's records is not established: the project was present in the store when the store's witness of legacy imports began ({}), no witness line names an import for it, and its own import account is {}. So whether it holds imported records cannot be known. This does not change.",
        began["at"].as_str().unwrap_or("at a time its first line does not give"),
        if dir.join("imports.jsonl").exists() { "unreadable or shows no import" } else { "absent" })))
}
/// The name of `project`'s folder in the store: what the witness's first line
/// lists. It comes from the project's identity and no act changes it.
fn folder_key(store: &Path, project: &str) -> Result<String, String> {
    project_dir(store, project).file_name().and_then(|n| n.to_str()).map(str::to_owned).ok_or_else(|| "project store folder has no name".into())
}

/// The imports a readable account shows, as witnessed by it alone. The
/// account is read by the store's own strict reading first (`imports`): one
/// that exists and cannot be read is an error, never "no account evidence",
/// from which a project the witness does not list would read "no import".
fn from_account(dir: &Path) -> Result<Option<LegacyOrigin>, String> {
    let path = dir.join("imports.jsonl");
    imports(dir)?;
    let values = read_store_file(&path)?.require_whole(&path)?;
    let found: Vec<WitnessedImport> = account_imports(&values).into_iter().filter_map(|(import, at, files)| {
        witnessed_import(&json!({"importId":import,"at":at,"files":files,"basis":ACCOUNT_ONLY}))
    }).collect();
    Ok((!found.is_empty()).then_some(LegacyOrigin::Imported(found)))
}

/// Each import an account's lines show: (identifier, time started, files as
/// witness members) — a completed import's files, or a started one's census.
fn account_imports(values: &[Value]) -> Vec<(String, Value, Vec<Value>)> {
    let mut order: Vec<String> = Vec::new();
    let mut started: HashMap<String, &Value> = HashMap::new();
    let mut completed: HashMap<String, &Value> = HashMap::new();
    for line in values.iter().filter(|l| l["format"] == IMPORT_FORMAT) {
        let Some(id) = line["importId"].as_str() else { continue };
        if !order.iter().any(|o| o == id) {
            order.push(id.to_owned());
        }
        match line["event"].as_str() {
            Some("started") => { started.insert(id.to_owned(), line); }
            Some("completed") => { completed.insert(id.to_owned(), line); }
            _ => {}
        }
    }
    order.into_iter().map(|id| {
        let files = completed.get(&id).map(|c| &c["files"]).or_else(|| started.get(&id).map(|s| &s["census"]));
        let files = files.and_then(Value::as_array).into_iter().flatten()
            .map(|f| json!({"copy":f["copy"],"length":f["bytes"],"sha256":f["sha256"]})).collect();
        let at = started.get(&id).map(|s| s["at"].clone()).unwrap_or(Value::Null);
        (id, at, files)
    }).collect()
}
fn witnessed_import(value: &Value) -> Option<WitnessedImport> {
    let files = value["files"].as_array()?.iter().map(|f| Some(WitnessedFile {
        copy: f["copy"].as_str()?.to_owned(), length: f["length"].as_u64()?, sha256: f["sha256"].as_str()?.to_owned(),
    })).collect::<Option<Vec<_>>>()?;
    Some(WitnessedImport {
        import_id: value["importId"].as_str()?.to_owned(),
        at: value["importedAt"].as_str().or(value["at"].as_str()).unwrap_or_default().to_owned(),
        basis: value["basis"].as_str()?.to_owned(),
        files,
    })
}
fn project_identity(dir: &Path) -> Option<String> {
    let bytes = crate::records_retention::read_plain(&dir.join("project.json")).ok()?;
    let v: Value = serde_json::from_slice(&bytes).ok()?;
    (v["format"] == PROJECT_FORMAT).then(|| v["projectId"].as_str().map(str::to_owned)).flatten()
}
