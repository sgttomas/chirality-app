//! Verified package restoration. The durable intent is outside the payload it
//! fences. An interruption is finished from that same intent, never rolled back
//! or treated as another native import act. Unsigned source claims stay quoted.
use super::*;
use crate::{records_package as bag, records_retention as retention, storage};
use serde::{Deserialize, Serialize};
use std::cell::RefCell;
use std::collections::BTreeSet;
use std::fs::File;
use std::os::fd::AsRawFd;
use std::os::fd::FromRawFd;
use std::os::unix::fs::MetadataExt;

const FORMAT: &str = "chirality.records-package-import";
const STANDING: &str = "Verified exact package bytes, unsigned. Source actors, human acts, installation and native relationships are not authenticated. Imported observations remain quoted evidence; capture and capability authority is not restored.";
thread_local! { static OWNER: RefCell<Option<PathBuf>> = const { RefCell::new(None) }; }
static UNCERTAIN: std::sync::LazyLock<Mutex<BTreeMap<PathBuf, String>>> =
    std::sync::LazyLock::new(|| Mutex::new(BTreeMap::new()));
static SEEN: std::sync::LazyLock<Mutex<BTreeMap<PathBuf, BTreeSet<String>>>> =
    std::sync::LazyLock::new(|| Mutex::new(BTreeMap::new()));

pub(crate) fn owns(dir: &Path) -> bool {
    OWNER.with(|o| o.borrow().as_deref() == Some(dir))
}
struct Owner;
impl Owner {
    fn enter(dir: &Path) -> Result<Self, String> {
        OWNER.with(|o| {
            if o.borrow().is_some() {
                return Err("nested package import is refused".into());
            }
            *o.borrow_mut() = Some(dir.to_owned());
            Ok(Self)
        })
    }
}
impl Drop for Owner {
    fn drop(&mut self) {
        OWNER.with(|o| *o.borrow_mut() = None);
    }
}
fn controls(dir: &Path) -> Result<PathBuf, String> {
    Ok(dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project has no store")?
        .join("administration")
        .join(dir.file_name().ok_or("project has no key")?))
}
fn journal(dir: &Path) -> Result<PathBuf, String> {
    Ok(controls(dir)?.join("package-imports"))
}
fn physical(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    let m = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !m.is_dir() {
        return Err("import folder is not a physical directory".into());
    }
    Ok(json!({"device":m.dev(),"inode":m.ino()}))
}
fn plain(path: &Path) -> Result<Vec<u8>, String> {
    retention::read_plain(path)
}
fn optional(path: &Path) -> Result<Option<Vec<u8>>, String> {
    match std::fs::symlink_metadata(path) {
        Ok(_) => plain(path).map(Some),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e.to_string()),
    }
}
fn json_bytes(value: &impl Serialize) -> Result<Vec<u8>, String> {
    serde_json::to_vec_pretty(value).map_err(|e| e.to_string())
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Intent {
    format: String,
    version: String,
    id: String,
    at: String,
    store: PathBuf,
    store_id: String,
    root: PathBuf,
    project: String,
    physical_root: Value,
    physical_store: Value,
    physical_payload: Value,
    link_before: Vec<u8>,
    link_after: Vec<u8>,
    roots_before: Value,
    roots_original: Vec<u8>,
    roots_final: Vec<u8>,
    stage: PathBuf,
    package_identity: String,
    payload: BTreeMap<String, bag::Member>,
    before: BTreeMap<String, bag::Member>,
    copied: BTreeMap<String, bag::Member>,
    administration: Value,
    source_context: Value,
    actor: Value,
    observed: Value,
    source: PathBuf,
    duplicates: Vec<String>,
}
impl Intent {
    fn dir(&self) -> PathBuf {
        project_dir(&self.store, &self.project)
    }
    fn folder(&self) -> Result<PathBuf, String> {
        journal(&self.dir())
    }
    fn path(&self) -> Result<PathBuf, String> {
        Ok(self.folder()?.join(format!("{}.json", self.id)))
    }
    fn completion_path(&self) -> Result<PathBuf, String> {
        Ok(self.folder()?.join(format!("{}.completed.json", self.id)))
    }
    fn publish(&self, path: &Path, bytes: &[u8]) -> Result<(), String> {
        bag::create_or_match_staged(
            path,
            bytes,
            &self.stage.parent().unwrap().join("control-staging"),
        )
    }
    fn receipt_relative(&self) -> String {
        format!("package-imports/{}.json", self.id)
    }
    fn receipt(&self) -> Value {
        json!({"format":FORMAT,"formatVersion":"0.1","importId":self.id,
        "projectId":self.project,"packageIdentity":self.package_identity,"copied":self.copied,
        "standing":STANDING})
    }
    fn valid(&self, dir: &Path, id: &str) -> Result<(), String> {
        if self.format != FORMAT
            || self.version != "0.1"
            || self.id != id
            || self.dir() != dir
            || self.id.len() != 64
            || !self.id.bytes().all(|b| b.is_ascii_hexdigit())
            || self.stage
                != self
                    .store
                    .join("package-staging")
                    .join(&self.id)
                    .join("bag")
            || self.package_identity.len() != 64
        {
            return Err("package import intent identity/profile is invalid".into());
        }
        for (name, member) in &self.copied {
            if self.payload.get(name) != Some(member) || self.before.contains_key(name) {
                return Err("package import intent copy plan is invalid".into());
            }
        }
        if self
            .payload
            .iter()
            .any(|(name, m)| self.before.get(name).is_some_and(|old| old != m))
        {
            return Err("package import intent overwrites original evidence".into());
        }
        Ok(())
    }
}
struct Entry {
    intent: Intent,
    bytes: Vec<u8>,
    done: Option<Vec<u8>>,
}
fn entries(dir: &Path) -> Result<Vec<Entry>, String> {
    let folder = journal(dir)?;
    storage::check_path(&folder)?;
    let mut names = match std::fs::read_dir(&folder) {
        Ok(rows) => rows
            .map(|r| {
                r.map_err(|e| e.to_string())?
                    .file_name()
                    .into_string()
                    .map_err(|_| "non-UTF8 package journal name".into())
            })
            .collect::<Result<Vec<String>, String>>()?,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Vec::new(),
        Err(e) => return Err(e.to_string()),
    };
    names.sort();
    let observed: BTreeSet<_> = names.iter().cloned().collect();
    if SEEN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .is_some_and(|seen| !seen.is_subset(&observed))
    {
        return Err("previously observed package import evidence disappeared".into());
    }
    let mut result = Vec::new();
    for name in &names {
        if let Some(id) = name.strip_suffix(".completed.json") {
            if !observed.contains(&format!("{id}.json")) {
                return Err("package completion has lost its original intent".into());
            }
            continue;
        }
        let id = name
            .strip_suffix(".json")
            .ok_or("unknown package journal member")?;
        if id.len() != 64 || !id.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err("unknown package journal member".into());
        }
        let bytes = plain(&folder.join(name))?;
        let intent: Intent = serde_json::from_slice(&bytes)
            .map_err(|e| format!("package intent unreadable: {e}"))?;
        intent.valid(dir, id)?;
        let done = optional(&intent.completion_path()?)?;
        if let Some(bytes_done) = &done {
            let v: Value = serde_json::from_slice(bytes_done).map_err(|e| e.to_string())?;
            if v != completion(&intent, &bytes) {
                return Err("package completion does not bind its original intent".into());
            }
            let receipt = plain(&dir.join(intent.receipt_relative()))?;
            if receipt != json_bytes(&intent.receipt())? {
                return Err("package import origin receipt changed or disappeared".into());
            }
        }
        result.push(Entry {
            intent,
            bytes,
            done,
        });
    }
    let after = std::fs::read_dir(&folder).map(|rows| {
        rows.map(|r| r.map(|e| e.file_name().to_string_lossy().into_owned()))
            .collect::<Result<BTreeSet<_>, _>>()
    });
    match after {
        Ok(Ok(now)) if now == observed => {}
        Err(e) if observed.is_empty() && e.kind() == std::io::ErrorKind::NotFound => {}
        _ => return Err("package import journal changed while reading".into()),
    }
    SEEN.lock()
        .unwrap_or_else(|p| p.into_inner())
        .entry(dir.to_owned())
        .or_default()
        .extend(observed);
    Ok(result)
}
fn completion(intent: &Intent, bytes: &[u8]) -> Value {
    json!({"format":"chirality.records-package-import-completion","formatVersion":"0.1",
    "importId":intent.id,"intentSha256":sha256_hex(bytes),"packageIdentity":intent.package_identity})
}
pub(crate) fn require_complete(dir: &Path) -> Result<(), String> {
    if owns(dir) {
        return Ok(());
    }
    if UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .contains_key(dir)
    {
        return Err("package import publication is uncertain; finish the original import before reading or recording".into());
    }
    if entries(dir)?.iter().any(|e| e.done.is_none()) {
        return Err(
            "package import incomplete; finish the original import before reading or recording"
                .into(),
        );
    }
    Ok(())
}
pub(crate) fn complete_exists(dir: &Path) -> bool {
    require_complete(dir).is_ok()
        && entries(dir).is_ok_and(|rows| rows.iter().any(|e| e.done.is_some()))
}
pub(crate) fn provenance_context(dir: &Path) -> Result<Value, String> {
    require_complete(dir)?;
    let rows = entries(dir)?;
    let mut stamps = BTreeMap::new();
    for path in [controls(dir)?, journal(dir)?, dir.join("package-imports")] {
        stamps.insert(path.to_string_lossy().into_owned(), stamp(&path)?);
    }
    let mut evidence = Vec::new();
    for e in rows {
        for path in [
            e.intent.path()?,
            e.intent.completion_path()?,
            dir.join(e.intent.receipt_relative()),
        ] {
            stamps.insert(path.to_string_lossy().into_owned(), stamp(&path)?);
        }
        evidence.push(json!({"importId":e.intent.id,"intent":sha256_hex(&e.bytes),"completion":e.done.as_ref().map(|b|sha256_hex(b))}));
    }
    Ok(json!({"evidence":evidence,"stamps":stamps}))
}
fn stamp(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    match std::fs::symlink_metadata(path) {
        Ok(m) => Ok(
            json!({"device":m.dev(),"inode":m.ino(),"mode":m.mode(),"links":m.nlink(),"bytes":m.len(),
            "mtime":m.mtime(),"mtimeNanos":m.mtime_nsec(),"ctime":m.ctime(),"ctimeNanos":m.ctime_nsec()}),
        ),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(Value::Null),
        Err(e) => Err(e.to_string()),
    }
}
pub(crate) fn quoted_prefix(dir: &Path, relative: &str, bytes: &[u8]) -> Result<u64, String> {
    require_complete(dir)?;
    let mut prefix = 0;
    for e in entries(dir)? {
        if let Some(member) = e.intent.copied.get(relative) {
            let count =
                usize::try_from(member.bytes).map_err(|_| "quoted prefix length unsupported")?;
            if count > bytes.len() || sha256_hex(&bytes[..count]) != member.sha256 {
                return Err(
                    "imported observation prefix changed; App provenance is unavailable".into(),
                );
            }
            prefix = prefix.max(member.bytes);
        }
    }
    Ok(prefix)
}
pub(crate) fn status(root: &Path) -> Value {
    let result = (|| -> Result<Value, String> {
        let (store, _) = opened()?;
        let project = match read_link(root) {
            Link::Present { project, .. } => project,
            _ => return Ok(json!({"state":"none"})),
        };
        let dir = project_dir(&store, &project);
        let rows = entries(&dir)?;
        let uncertain_id = UNCERTAIN
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .get(&dir)
            .cloned();
        let row = rows.iter().find(|e| e.done.is_none()).or_else(|| {
            rows.iter()
                .find(|e| Some(&e.intent.id) == uncertain_id.as_ref())
        });
        if let Some(e) = row {
            return Ok(
                json!({"state":"incomplete","importId":e.intent.id,"packageIdentity":e.intent.package_identity,"limit":"Ordinary reads and recording are fenced until this same import finishes."}),
            );
        }
        Ok(json!({"state":if rows.is_empty(){"none"}else{"complete"}}))
    })();
    result.unwrap_or_else(|limit| json!({"state":"unavailable","limit":limit}))
}

struct Lease(File);
impl Drop for Lease {
    fn drop(&mut self) {
        unsafe {
            libc::flock(self.0.as_raw_fd(), libc::LOCK_UN);
        }
    }
}
fn exclusive(path: &Path) -> Result<Lease, String> {
    bag::create_or_match(path, b"")?;
    let f = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    if f.metadata().map_err(|e| e.to_string())?.nlink() != 1 {
        return Err("import lock is hardlinked".into());
    }
    if unsafe { libc::flock(f.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } != 0 {
        return Err(
            "project records are busy; retry when native recording, captures and readers are idle"
                .into(),
        );
    }
    Ok(Lease(f))
}
struct Guards {
    _owner: Owner,
    _writer: Lease,
    _capture: Lease,
    _activity: Lease,
    _admission: Lease,
    _store: storage::Ownership,
}
fn lock(store: &Path, dir: &Path) -> Result<Guards, String> {
    let store_guard = store_lock(store)?;
    let admission = exclusive(&controls(dir)?.join(".admission.lock"))?;
    let owner = Owner::enter(dir)?;
    let activity = exclusive(&controls(dir)?.join(".activity.lock"))?;
    let capture = exclusive(&dir.join("captures/.capture.lock"))?;
    let writer = exclusive(&dir.join(".writer.lock"))?;
    Ok(Guards {
        _owner: owner,
        _writer: writer,
        _capture: capture,
        _activity: activity,
        _admission: admission,
        _store: store_guard,
    })
}
fn roots_context(store: &Path, root: &Path, project: &str) -> Result<Value, String> {
    let rows = roots(store)?;
    let at = root.to_str().ok_or("project root is not UTF-8")?;
    let here = listed(&rows, at);
    if here.iter().any(|p| p != project) {
        return Err("selected folder already belongs to a different store project".into());
    }
    let mut others = BTreeMap::new();
    for other in roots_of(&rows, project).into_iter().filter(|r| r != at) {
        if matches!(read_link(Path::new(&other)),Link::Present{project:p,..} if p==project) {
            return Err("another live folder holds this project identity; import refused".into());
        }
        others.insert(
            other.clone(),
            optional(&Path::new(&other).join(PROJECT_LINK))?,
        );
    }
    Ok(json!({"here":here,"others":others}))
}
fn identities(
    root: &Path,
    inventory: &BTreeMap<String, bag::Member>,
    strict: bool,
) -> Result<(BTreeSet<String>, Vec<String>), String> {
    let mut ids = BTreeSet::new();
    let mut duplicates = BTreeSet::new();
    for name in inventory.keys().filter(|n| n.ends_with(".jsonl")) {
        let bytes = plain(&root.join(name))?;
        if strict && !bytes.is_empty() && !bytes.ends_with(b"\n") {
            return Err(
                "target identity inventory has a partial log; safe collision check unavailable"
                    .into(),
            );
        }
        for line in bytes.split(|b| *b == b'\n').filter(|b| !b.is_empty()) {
            let v:Value=match serde_json::from_slice(line){Ok(v)=>v,Err(_) if !strict=>continue,Err(_)=>return Err("target identity inventory has an unreadable log line; safe collision check unavailable".into())};
            let entries = if v["format"] == "chirality.rs.group" {
                v["entries"].as_array().cloned().unwrap_or_default()
            } else {
                vec![v]
            };
            for entry in entries {
                if let Some(id) = entry["recordId"].as_str() {
                    if !ids.insert(id.to_owned()) {
                        duplicates.insert(id.to_owned());
                    }
                }
            }
        }
    }
    Ok((ids, duplicates.into_iter().collect()))
}
fn collision_check(
    snapshot: &bag::Snapshot,
    before: &BTreeMap<String, bag::Member>,
    copied: &BTreeMap<String, bag::Member>,
    dir: &Path,
) -> Result<Vec<String>, String> {
    let (source, duplicates) =
        identities(&snapshot.root().join("data"), snapshot.payload(), false)?;
    if !copied.is_empty() {
        // Ignore exact same-path copies. All other surviving identities must be
        // known, including entries nested inside an RS group line.
        let other = before
            .iter()
            .filter(|(name, _)| !snapshot.payload().contains_key(*name))
            .map(|(n, m)| (n.clone(), m.clone()))
            .collect();
        let (held, _) = identities(dir, &other, true)?;
        if let Some(id) = source.intersection(&held).next() {
            return Err(format!(
                "target already holds record identity {id} in another member; nothing merged"
            ));
        }
    }
    Ok(duplicates)
}
fn validate_target(
    intent: &Intent,
    snapshot: &bag::Snapshot,
    resuming: bool,
) -> Result<Value, String> {
    let (store, id) = opened()?;
    if store != intent.store
        || id != intent.store_id
        || physical(&store)? != intent.physical_store
        || physical(&intent.root)? != intent.physical_root
        || physical(&intent.dir())? != intent.physical_payload
    {
        return Err("physical project, store or store identity changed; import refused".into());
    }
    snapshot.verify_unchanged()?;
    let link = plain(&intent.root.join(PROJECT_LINK))?;
    if link != intent.link_before && !(resuming && link == intent.link_after) {
        return Err("project link changed; review again".into());
    }
    let registry = roots_context(&store, &intent.root, &intent.project)?;
    let registry_bytes = optional(&store.join("roots.jsonl"))?.unwrap_or_default();
    if (!resuming && registry_bytes != intent.roots_original)
        || (resuming && !compatible_roots(intent, &registry_bytes)?)
    {
        return Err(
            "roots registry differs from original intent's exact append prefix; import refused"
                .into(),
        );
    }
    let resumed_registry = resuming
        && registry["here"]
            .as_array()
            .is_some_and(|here| here.is_empty() || *here == vec![json!(intent.project)])
        && registry["others"].as_object().is_some_and(|others| {
            others
                .iter()
                .all(|(root, link)| intent.roots_before["others"][root] == *link)
        });
    if registry != intent.roots_before && !resumed_registry {
        return Err("project root association changed; review again".into());
    }
    let current = bag::payload_inventory(&intent.dir())?;
    for (name, old) in &intent.before {
        if current.get(name) != Some(old) {
            return Err(format!(
                "original target member changed or disappeared: {name}"
            ));
        }
    }
    for (name, member) in &current {
        let receipt = name == &intent.receipt_relative()
            && *member
                == bag::Member {
                    sha256: sha256_hex(&json_bytes(&intent.receipt())?),
                    bytes: json_bytes(&intent.receipt())?.len() as u64,
                };
        if !intent.before.contains_key(name)
            && !(resuming && (intent.copied.get(name) == Some(member) || receipt))
        {
            return Err(format!(
                "target gained an unreviewed or conflicting member: {name}"
            ));
        }
    }
    let administration =
        retention::validate_package_snapshot(&intent.project, snapshot.administration())?;
    let plan =
        retention::resume_package_restore(&intent.dir(), &administration, &intent.source_context)?;
    Ok(
        json!({"link":sha256_hex(&link),"registry":registry,"registryBytes":sha256_hex(&registry_bytes),"registryStamp":stamp(&store.join("roots.jsonl"))?,"payload":current,"administration":plan.summary(),
        "root":physical(&intent.root)?,"store":physical(&store)?,"payloadFolder":physical(&intent.dir())?}),
    )
}
fn compatible_roots(intent: &Intent, bytes: &[u8]) -> Result<bool, String> {
    if bytes.len() >= intent.roots_original.len() && intent.roots_final.starts_with(bytes) {
        return Ok(true);
    }
    let Some(tail) = bytes.strip_prefix(intent.roots_final.as_slice()) else {
        return Ok(false);
    };
    if !tail.is_empty() && !tail.ends_with(b"\n") {
        return Ok(false);
    }
    let root = intent.root.to_str().ok_or("project root is not UTF-8")?;
    Ok(parse_lines(tail, &intent.store.join("roots.jsonl"))?
        .iter()
        .all(|row| {
            row["format"] == ROOT_FORMAT
                && row["formatVersion"] == VERSION
                && row["projectId"]
                    .as_str()
                    .is_some_and(|p| !p.is_empty() && p != intent.project)
                && row["root"]
                    .as_str()
                    .is_some_and(|r| !r.is_empty() && r != root)
                && matches!(
                    row["how"].as_str(),
                    Some("minted" | "registered" | "adopted" | "released")
                )
        }))
}

pub(crate) struct Plan {
    intent: Intent,
    snapshot: bag::Snapshot,
    context: Value,
    resuming: bool,
    noop: bool,
    actor: Value,
    observed: Value,
}
pub(crate) fn prepare(
    root: &Path,
    source: &Path,
    actor: &Value,
    observed: &Value,
) -> Result<Plan, String> {
    storage::check_path(root)?;
    if root.canonicalize().map_err(|e| e.to_string())? != root {
        return Err("select the physical project folder".into());
    }
    let (store, store_id) = opened()?;
    require_native_actor(actor)?;
    let (project,linked)=match read_link(root){Link::Present{project,store} => (project,store),_=>return Err("package import requires this folder's existing readable project identity link; resolve its identity first".into())};
    let dir = project_dir(&store, &project);
    let id = storage::key(&crate::util::opaque_id("package-import:")?);
    let stage = store.join("package-staging").join(&id).join("bag");
    storage::check_path(source)?;
    let source = source.canonicalize().map_err(|e| e.to_string())?;
    if source.starts_with(&store)
        || store.starts_with(&source)
        || source.starts_with(root)
        || root.starts_with(&source)
    {
        return Err("choose a separate package outside the current store and project".into());
    }
    bag::create_or_match(
        &stage.parent().unwrap().join("review.json"),
        &json_bytes(&json!({"source":source,"actor":actor,"observed":observed}))?,
    )?;
    let snapshot = bag::snapshot(&source, &stage)?;
    if snapshot.project_id() != project {
        return Err("package project identity differs from the selected folder; nothing replaced or reminted".into());
    }
    let _guards = lock(&store, &dir)?;
    // Owner bypass is only for our own operation; a different unfinished
    // journal must still be refused before any new native act is prepared.
    if UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .contains_key(&dir)
        || entries(&dir)?.iter().any(|e| e.done.is_none())
    {
        return Err("finish the existing package import first".into());
    }
    let before = bag::payload_inventory(&dir)?;
    for (name, member) in snapshot.payload() {
        if before.get(name).is_some_and(|old| old != member) {
            return Err(format!(
                "conflicting target member {name}; nothing overwritten"
            ));
        }
    }
    let copied = snapshot
        .payload()
        .iter()
        .filter(|(name, _)| !before.contains_key(*name))
        .map(|(n, m)| (n.clone(), m.clone()))
        .collect();
    let duplicates = collision_check(&snapshot, &before, &copied, &dir)?;
    let admin = retention::validate_package_snapshot(&project, snapshot.administration())?;
    let restore = retention::plan_package_restore(&dir, &admin)?;
    let link_before = plain(&root.join(PROJECT_LINK))?;
    let link_after = if linked == store_id {
        link_before.clone()
    } else {
        json_bytes(&link_value(&project, &store_id))?
    };
    let no_admin_change = restore.missing_events.is_empty() && !restore.marker_needed;
    let intent = Intent {
        format: FORMAT.into(),
        version: "0.1".into(),
        id,
        at: now_rfc3339(),
        store: store.clone(),
        store_id,
        root: root.into(),
        project,
        physical_root: physical(root)?,
        physical_store: physical(&store)?,
        physical_payload: physical(&dir)?,
        link_before,
        link_after,
        roots_before: Value::Null,
        roots_original: Vec::new(),
        roots_final: Vec::new(),
        stage,
        package_identity: snapshot.identity().into(),
        payload: snapshot.payload().clone(),
        before,
        copied,
        administration: snapshot.administration().clone(),
        source_context: restore.source_context,
        actor: actor.clone(),
        observed: observed.clone(),
        source,
        duplicates,
    };
    let mut intent = intent;
    intent.roots_before = roots_context(&store, root, &intent.project)?;
    intent.roots_original = optional(&store.join("roots.jsonl"))?.unwrap_or_default();
    if !intent.roots_original.is_empty() && !intent.roots_original.ends_with(b"\n") {
        return Err(
            "roots registry has an incomplete prior line; resolve it before importing".into(),
        );
    }
    intent.roots_final = intent.roots_original.clone();
    let mut rows = Vec::new();
    for old in intent.roots_before["others"].as_object().unwrap().keys() {
        rows.push(json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":intent.project,"root":old,"how":"released","at":intent.at,"packageImport":intent.id}));
    }
    if intent.roots_before["here"] != json!([intent.project]) {
        rows.push(json!({"format":ROOT_FORMAT,"formatVersion":VERSION,"projectId":intent.project,"root":intent.root,"how":"adopted","at":intent.at,"packageImport":intent.id}));
    }
    for row in rows {
        intent
            .roots_final
            .extend(serde_json::to_vec(&row).map_err(|e| e.to_string())?);
        intent.roots_final.push(b'\n');
    }
    snapshot.source_unchanged()?;
    let context = validate_target(&intent, &snapshot, false)?;
    let noop = intent.copied.is_empty()
        && no_admin_change
        && intent.link_before == intent.link_after
        && intent.roots_before == json!({"here":[intent.project],"others":{}});
    Ok(Plan {
        intent,
        snapshot,
        context,
        resuming: false,
        noop,
        actor: actor.clone(),
        observed: observed.clone(),
    })
}
fn require_native_actor(actor: &Value) -> Result<(), String> {
    if !actor.is_object() || actor["identityVerified"] != false {
        return Err("native import actor context unavailable".into());
    }
    Ok(())
}
/// Append under the store lock through its held physical parent. A torn or
/// changed roots file is evidence to reconcile, never silently repaired.
fn publish_roots(intent: &Intent) -> Result<(), String> {
    let store = &intent.store;
    let path = store.join("roots.jsonl");
    if optional(&path)?.is_none() {
        bag::create_or_match(&path, b"")?;
    }
    let before = plain(&path)?;
    if !compatible_roots(intent, &before)? {
        return Err("roots registry is not the frozen original append prefix or compatible newer tail; association remains fenced".into());
    }
    let parent = crate::records_index::open_directory(store).map_err(|e| e.to_string())?;
    let parent_id = physical(store)?;
    let metadata = std::fs::symlink_metadata(&path).map_err(|e| e.to_string())?;
    let expected = crate::records_index::Stamp::of(&metadata);
    let name = std::ffi::CString::new("roots.jsonl").unwrap();
    let fd = unsafe {
        libc::openat(
            parent.as_raw_fd(),
            name.as_ptr(),
            libc::O_WRONLY | libc::O_APPEND | libc::O_CLOEXEC | libc::O_NOFOLLOW | libc::O_NONBLOCK,
        )
    };
    if fd < 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    let mut file = unsafe { File::from_raw_fd(fd) };
    let opened = file.metadata().map_err(|e| e.to_string())?;
    if !opened.is_file()
        || opened.nlink() != 1
        || crate::records_index::Stamp::of(&opened) != expected
        || plain(&path)? != before
        || physical(store)? != parent_id
    {
        return Err("roots registry changed before association; import remains fenced".into());
    }
    let suffix = if before.len() < intent.roots_final.len() {
        &intent.roots_final[before.len()..]
    } else {
        &[]
    };
    #[cfg(test)]
    if STOP.with(|s| s.borrow().as_ref() == Some(&"roots-partial")) && !suffix.is_empty() {
        file.write_all(&suffix[..suffix.len().div_ceil(2)])
            .map_err(|e| e.to_string())?;
        file.sync_all().map_err(|e| e.to_string())?;
        checkpoint("roots-partial")?;
    }
    file.write_all(suffix).map_err(|e| e.to_string())?;
    file.sync_all().map_err(|e| e.to_string())?;
    parent.sync_all().map_err(|e| e.to_string())?;
    let mut after = before;
    after.extend(suffix);
    if plain(&path)? != after
        || physical(store)? != parent_id
        || std::fs::symlink_metadata(&path)
            .map_err(|e| e.to_string())?
            .ino()
            != opened.ino()
    {
        return Err("roots registry publication uncertain; import remains fenced".into());
    }
    Ok(())
}
pub(crate) fn prepare_resume(root: &Path, actor: &Value, observed: &Value) -> Result<Plan, String> {
    let (store, _) = opened()?;
    let project = match read_link(root) {
        Link::Present { project, .. } => project,
        _ => {
            return Err("restore the original project identity link before finishing import".into())
        }
    };
    let dir = project_dir(&store, &project);
    let _guards = lock(&store, &dir)?;
    let rows = entries(&dir)?;
    let uncertain_id = UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(&dir)
        .cloned();
    let pending: Vec<_> = rows
        .into_iter()
        .filter(|e| e.done.is_none() || Some(&e.intent.id) == uncertain_id.as_ref())
        .collect();
    if pending.len() != 1 {
        return Err(
            "there is no single recoverable package import; no new import act performed".into(),
        );
    }
    let intent = pending.into_iter().next().unwrap().intent;
    if intent.root != root {
        return Err("finish import from its original physical project folder".into());
    }
    let snapshot = bag::inspect(&intent.stage)?;
    if snapshot.identity() != intent.package_identity
        || snapshot.payload() != &intent.payload
        || snapshot.administration() != &intent.administration
    {
        return Err("retained package differs from the durable original intent".into());
    }
    let context = validate_target(&intent, &snapshot, true)?;
    Ok(Plan {
        intent,
        snapshot,
        context,
        resuming: true,
        noop: false,
        actor: actor.clone(),
        observed: observed.clone(),
    })
}
pub(crate) fn statement(
    plan: &Plan,
) -> Result<crate::act_control::native_statement::NativeStatement, String> {
    let i = &plan.intent;
    let full=format!("{}\n\nProject: {}\nFolder: {}\nDestination store: {}\nPackage SHA-256: {}\nSource members: {}; missing members: {}; exact existing members: {}\n\n{}\n\nRetention after restoration: {}\n\n{}\n\nActor (identity not verified): {}",
        if plan.resuming{"Finish the original interrupted package import. This retries its frozen publications; it performs no second import act."}else{"Import this verified package and associate this folder with its original project identity in this store?"},
        i.project,i.root.display(),i.store.display(),i.package_identity,i.payload.len(),i.copied.len(),i.payload.len()-i.copied.len(),
        "Existing differing files and record identity collisions are refused. Source package and project originals stay unchanged. Valid newer local history, holds and closure survive.",
        plan.context["administration"]["resultingRetention"],STANDING,crate::act_control::native_statement::actor_line(&plan.actor));
    let detail = json!({"intent":i,"review":plan.context,"resume":plan.resuming,"actor":plan.actor,"observed":plan.observed});
    crate::act_control::native_statement::whole_or_in_app(
        "records package import",
        "records package",
        full,
        &detail,
        |digest| {
            format!("{}\n\nThe complete package, project, destination, actor and retention context is shown in the App under this confirmation. sha-256: {digest}\nUnsigned imported content remains quoted evidence. Changed context refuses publication.",if plan.resuming{"Finish the original package import?"}else{"Import this verified package?"})
        },
    )
}
pub(crate) fn apply(plan: Plan, actor: &Value, observed: &Value) -> Result<Value, String> {
    if *actor != plan.actor || *observed != plan.observed {
        return Err("native actor or home context changed; review again".into());
    }
    let i = &plan.intent;
    let dir = i.dir();
    let _guards = lock(&i.store, &dir)?;
    if validate_target(i, &plan.snapshot, plan.resuming)? != plan.context {
        return Err("import context changed after the native question; review again".into());
    }
    if plan.noop {
        plan.snapshot.source_unchanged()?;
        return Ok(
            json!({"state":"package already present","projectId":i.project,"packageIdentity":i.package_identity,"copied":0,
            "alreadyPresent":i.payload.len(),"duplicateIdentities":i.duplicates,"retention":retention::view(&dir),"standing":STANDING}),
        );
    }
    if !plan.resuming {
        plan.snapshot.source_unchanged()?;
        if entries(&dir)?.iter().any(|e| e.done.is_none()) {
            return Err("another package import is incomplete".into());
        }
        let bytes = json_bytes(i)?;
        // Mark uncertain before create: an error can mean the complete intent
        // is visible but its parent flush has not been confirmed.
        UNCERTAIN
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .insert(dir.clone(), i.id.clone());
        if let Err(error) = i.publish(&i.path()?, &bytes) {
            if optional(&i.path()?)?.is_none() {
                UNCERTAIN
                    .lock()
                    .unwrap_or_else(|p| p.into_inner())
                    .remove(&dir);
            }
            return Err(error);
        }
    }
    UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .insert(dir.clone(), i.id.clone());
    finish(i, &plan.snapshot)?;
    UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .remove(&dir);
    remember(&dir, &i.root);
    Ok(
        json!({"state":"package imported","importId":i.id,"projectId":i.project,"packageIdentity":i.package_identity,
        "copied":i.copied.len(),"alreadyPresent":i.payload.len()-i.copied.len(),"duplicateIdentities":i.duplicates,
        "retention":retention::view(&dir),"standing":STANDING}),
    )
}
fn finish(i: &Intent, snapshot: &bag::Snapshot) -> Result<(), String> {
    let dir = i.dir();
    // Retry syncs the existing immutable intent; it never creates a second act.
    i.publish(&i.path()?, &json_bytes(i)?)?;
    for (name, member) in &i.copied {
        bag::restore_member(
            &snapshot.root().join("data").join(name),
            &dir,
            name,
            &i.stage
                .parent()
                .unwrap()
                .join("scratch")
                .join(storage::key(name)),
            member,
        )?;
        checkpoint("payload")?;
    }
    let incoming = retention::validate_package_snapshot(&i.project, &i.administration)?;
    let restore = retention::resume_package_restore(&dir, &incoming, &i.source_context)?;
    retention::restore_package_history(&dir, &restore)?;
    checkpoint("administration")?;
    publish_roots(i)?;
    checkpoint("roots")?;
    if i.link_before != i.link_after {
        bag::replace_control(&i.root.join(PROJECT_LINK), &i.link_before, &i.link_after)?;
    }
    checkpoint("link")?;
    i.publish(&dir.join(i.receipt_relative()), &json_bytes(&i.receipt())?)?;
    snapshot.verify_unchanged()?;
    validate_target(i, snapshot, true)?;
    let actual = bag::payload_inventory(&dir)?;
    for (name, m) in &i.payload {
        if actual.get(name) != Some(m) {
            return Err("restored package payload is incomplete or differs".into());
        }
    }
    // Flush current roots/link again even on retries whose complete bytes were
    // visible before an earlier uncertain sync.
    for path in [i.store.join("roots.jsonl"), i.root.join(PROJECT_LINK)] {
        crate::records_index::open_log(&path)
            .map_err(|e| e.to_string())?
            .sync_all()
            .map_err(|e| e.to_string())?;
        storage::sync_dir(path.parent().unwrap())?;
    }
    checkpoint("completion")?;
    let bytes = plain(&i.path()?)?;
    i.publish(&i.completion_path()?, &json_bytes(&completion(i, &bytes))?)?;
    checkpoint("completion-published")?;
    storage::sync_dir(&i.folder()?)?;
    Ok(())
}
#[cfg(not(test))]
fn checkpoint(_: &str) -> Result<(), String> {
    Ok(())
}
#[cfg(test)]
thread_local! {static STOP:RefCell<Option<&'static str>>=const{RefCell::new(None)};}
#[cfg(test)]
fn checkpoint(at: &str) -> Result<(), String> {
    STOP.with(|s| {
        if s.borrow().as_ref().is_some_and(|wanted| *wanted == at) {
            s.borrow_mut().take();
            Err(format!("test interruption after {at}"))
        } else {
            Ok(())
        }
    })
}

#[cfg(test)]
#[path = "records_package_import_tests.rs"]
mod tests;

#[cfg(test)]
#[path = "records_package_capture_tests.rs"]
mod capture_tests;
