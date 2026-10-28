//! DEL-06-01: observational file reader of quoted 0.1 and native-links 0.2.
//! Project claims and the App's protected observation order stay distinct.
use crate::{records_index::Stamp, records_store, storage};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::io::Read;
use std::os::fd::AsRawFd;
use std::os::fd::IntoRawFd;
use std::os::unix::ffi::OsStringExt;
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

const FOLDER: &str = ".chirality/fleet";
const LOG: &str = "coordination.fleet.jsonl";
const SCHEMA_ID: &str = "urn:chirality:app-v4:del-06-01:fleet-record:0.1";
const OBSERVED: &[&str] = &["dispatch_observed", "child_observed", "observation_ended", "related_conversation", "recording_limit", "recording_recovered"];
const STANDING: &str = "Read-only file observations. Records say what was recorded, not that it happened. Records retain their claimed recorder. Prepared work, supplier observations, returns, review, integration and human acts remain separate. The workspace derives file-based claims only; it establishes no current native execution or human act.";

#[path = "fleet_views.rs"]
mod views;

fn validator() -> Result<&'static jsonschema::Validator, String> {
    static VALUE: OnceLock<Result<jsonschema::Validator, String>> = OnceLock::new();
    VALUE.get_or_init(|| {
        crate::schema_validation::compile_targets(
            &[("fleet.record.schema.json", include_str!("../schemas/fleet.record.schema.json"))],
            &[SCHEMA_ID], &[SCHEMA_ID],
        ).map(|mut v| v.remove(0))
    }).as_ref().map_err(Clone::clone)
}

/// This census has no admission/lock/create path. Its final comparison spans
/// both logs and every identity/admin source used to associate the protected one.
#[derive(Default)]
struct Census {
    stamps: BTreeMap<PathBuf, Option<Stamp>>,
    directories: BTreeMap<PathBuf, Vec<PathBuf>>,
}
/// fdopendir owns the already opened directory. Names come from that
/// descriptor, never from a re-resolved pathname or a /dev/fd alias.
fn directory_names(file: &std::fs::File) -> Result<Vec<std::ffi::OsString>,String> {
    #[cfg(target_os = "macos")]
    let errno = unsafe { libc::__error() };
    #[cfg(target_os = "linux")]
    let errno = unsafe { libc::__errno_location() };
    #[cfg(not(any(target_os = "macos",target_os = "linux")))]
    let errno = std::ptr::null_mut::<libc::c_int>();
    if errno.is_null() { return Err("held-directory enumeration unavailable on this platform".into()); }
    let fd = file.try_clone().map_err(|e|e.to_string())?.into_raw_fd();
    let stream = unsafe { libc::fdopendir(fd) };
    if stream.is_null() {
        let error = std::io::Error::last_os_error().to_string();
        unsafe { libc::close(fd); }
        return Err(error);
    }
    struct Stream(*mut libc::DIR);
    impl Drop for Stream { fn drop(&mut self) { unsafe { libc::closedir(self.0); } } }
    let stream = Stream(stream);
    let mut names = Vec::new();
    loop {
        unsafe { *errno = 0; }
        let entry = unsafe { libc::readdir(stream.0) };
        if entry.is_null() {
            let code = unsafe { *errno };
            if code != 0 { return Err(std::io::Error::from_raw_os_error(code).to_string()); }
            break;
        }
        let name = unsafe { std::ffi::CStr::from_ptr((*entry).d_name.as_ptr()) }.to_bytes();
        if name != b"." && name != b".." { names.push(std::ffi::OsString::from_vec(name.to_vec())); }
    }
    names.sort();
    Ok(names)
}
impl Census {
    fn metadata(&mut self, path: &Path) -> Result<Option<std::fs::Metadata>, String> {
        storage::check_path(path)?;
        let meta = match std::fs::symlink_metadata(path) {
            Ok(m) => Some(m),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
            Err(e) => return Err(format!("source metadata unavailable: {e}")),
        };
        let stamp = meta.as_ref().map(Stamp::of);
        if self.stamps.get(path).is_some_and(|first| *first != stamp) {
            return Err("source changed between reads in the same packet".into());
        }
        self.stamps.insert(path.to_owned(), stamp);
        Ok(meta)
    }
    fn directory(&mut self, path: &Path) -> Result<Vec<PathBuf>, String> {
        let Some(meta) = self.metadata(path)? else { return Ok(vec![]); };
        if !meta.is_dir() { return Err("source folder is not a directory".into()); }
        let file = crate::records_index::open_directory(path).map_err(|e|e.to_string())?;
        if Stamp::of(&file.metadata().map_err(|e|e.to_string())?) != Stamp::of(&meta) { return Err("source directory changed while opening".into()); }
        let paths = directory_names(&file)?.into_iter().map(|name|path.join(name)).collect::<Vec<_>>();
        if Stamp::of(&file.metadata().map_err(|e|e.to_string())?) != Stamp::of(&meta) { return Err("source directory changed while enumerating".into()); }
        if self.directories.get(path).is_some_and(|first| *first != paths) {
            return Err("source directory inventory changed between reads".into());
        }
        self.directories.insert(path.to_owned(), paths.clone());
        Ok(paths)
    }
    fn read(&mut self, path: &Path) -> Result<Option<Vec<u8>>, String> {
        let Some(meta) = self.metadata(path)? else { return Ok(None); };
        if !meta.is_file() || meta.nlink() != 1 { return Err("source is not a regular single-link file".into()); }
        let stamp = Stamp::of(&meta);
        let mut file = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
        let opened = file.metadata().map_err(|e| e.to_string())?;
        if !opened.is_file() || opened.nlink() != 1 || Stamp::of(&opened) != stamp {
            return Err("source changed while opening".into());
        }
        let mut bytes = Vec::new();
        file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
        if Stamp::of(&file.metadata().map_err(|e| e.to_string())?) != stamp {
            return Err("source changed while reading".into());
        }
        Ok(Some(bytes))
    }
    fn unchanged(&self) -> Result<(), String> {
        for (path, stamp) in &self.stamps {
            storage::check_path(path)?;
            let current = match std::fs::symlink_metadata(path) {
                Ok(m) => Some(Stamp::of(&m)),
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => None,
                Err(e) => return Err(e.to_string()),
            };
            if &current != stamp { return Err("source inventory/stamp changed while reading; refresh the packet".into()); }
        }
        for (path, original) in &self.directories {
            let file = crate::records_index::open_directory(path).map_err(|e|e.to_string())?;
            let before = Stamp::of(&file.metadata().map_err(|e|e.to_string())?);
            if self.stamps.get(path) != Some(&Some(before)) { return Err("source directory changed before final inventory".into()); }
            let current = directory_names(&file)?.into_iter().map(|name|path.join(name)).collect::<Vec<_>>();
            if Stamp::of(&file.metadata().map_err(|e|e.to_string())?) != before { return Err("source directory changed during final inventory".into()); }
            if &current != original { return Err("source folder inventory changed while reading; refresh the packet".into()); }
        }
        Ok(())
    }
}

#[derive(Clone)]
struct Row {
    record: Value,
    bytes: Vec<u8>,
    source: Value,
    /// End of this exact source line, including its line ending. File records
    /// have no log offset. A line crossing an imported prefix stays quoted.
    log_end: Option<u64>,
}
impl Row {
    fn id(&self) -> &str { self.record["observationId"].as_str().or_else(||self.record["recordId"].as_str()).unwrap() }
    fn kind(&self) -> &str { self.record["kind"].as_str().unwrap() }
    fn view(&self, standing: &str) -> Value {
        json!({"record":self.record,"source":self.source,"standing":standing})
    }
    fn follows_quoted_prefix(&self, prefix: u64) -> bool {
        self.log_end.and_then(|end| end.checked_sub(self.bytes.len() as u64))
            .is_some_and(|start| start >= prefix)
    }
}
fn source(path: &Path, root: &Path, protected: bool, line: Option<usize>) -> Value {
    let rel = path.strip_prefix(root).unwrap_or(path);
    json!({"path":rel.to_string_lossy(),"nativePath":crate::attachments::native_path_identity(rel),
        "home":if protected {"configured records store"} else {"selected project"},"line":line})
}
fn issue(source: &Value, reason: &str) -> Value { json!({"source":source,"reason":reason}) }
fn valid(bytes: &[u8], validation: &jsonschema::Validator) -> Result<Value, &'static str> {
    let record: Value = serde_json::from_slice(bytes).map_err(|_| "not JSON (not read)")?;
    if record["format"] != "chirality.fleet.record" {
        return Err("unknown fleet format/version (not read)");
    }
    match record["formatVersion"].as_str(){
        Some("0.1")=>validation.validate(&record).map_err(|_| "fleet schema invalid or unknown kind (not read)")?,
        Some("0.2")=>crate::native_conversation_links::validate_record(&record).map_err(|_| "native-links schema/association invalid (not read)")?,
        _=>return Err("unknown fleet format/version (not read)"),
    }
    Ok(record)
}
/// Mixed-version validation for the App writer; references remain quoted.
pub(crate) fn validate_line(bytes:&[u8])->Result<Value,String>{valid(bytes,validator()?).map_err(str::to_owned)}

struct LogRead { rows: Vec<Row>, bytes: Option<Vec<u8>>, complete: bool, view: Value }
/// A pathname replacement cannot reset proof for this source. Paths retain
/// native bytes; configured aliases converge on the same physical source.
#[derive(Clone, Ord, PartialOrd, Eq, PartialEq)]
struct HistorySource {
    selected_project: PathBuf,
    store: PathBuf,
    store_id: String,
    project_id: String,
    log: PathBuf,
}
struct AcceptedPrefix { length: usize, digest: String }
static ACCEPTED_PREFIXES: std::sync::LazyLock<
    std::sync::Mutex<BTreeMap<HistorySource, AcceptedPrefix>>,
> = std::sync::LazyLock::new(|| std::sync::Mutex::new(BTreeMap::new()));
fn observe_prefix(source: &HistorySource, bytes: Option<&[u8]>, accept: bool) -> Result<(), String> {
    let mut known = ACCEPTED_PREFIXES.lock().unwrap_or_else(|p|p.into_inner());
    if let Some(prefix) = known.get(source) {
        if !bytes.and_then(|bytes|bytes.get(..prefix.length)).is_some_and(|bytes|crate::util::sha256_hex(bytes)==prefix.digest) {
            return Err("previously accepted protected fleet history changed or disappeared; no governing projection or App provenance; restore the original accepted prefix before refreshing".into());
        }
    }
    // Only the complete, schema-valid, duplicate-free, stable snapshot becomes
    // a bounded length/digest proof of those exact bytes (not Fleet graph
    // identity). Refusal retains earlier proof and cannot shorten/reset it.
    if accept {
        let bytes = bytes.ok_or("complete protected fleet source has no bytes")?;
        if known.get(source).is_none_or(|prefix|bytes.len()>prefix.length) {
            known.insert(source.clone(),AcceptedPrefix {length:bytes.len(),digest:crate::util::sha256_hex(bytes)});
        }
    }
    Ok(())
}
pub(crate) fn writer_prefix(root:&Path,store:&Path,store_id:&str,project_id:&str,dir:&Path,bytes:&[u8])->Result<(),String>{
    observe_prefix(&HistorySource {selected_project:root.to_owned(),store:store.to_owned(),store_id:store_id.to_owned(),project_id:project_id.to_owned(),log:dir.join("fleet").join(LOG)},Some(bytes),true)
}
fn read_log(census: &mut Census, path: &Path, root: &Path, protected: bool, validation: &jsonschema::Validator, limits: &mut Vec<Value>) -> LogRead {
    let origin = source(path, root, protected, None);
    let mut rows = Vec::new();
    let (status, mut complete, bytes) = match census.read(path) {
        Ok(Some(bytes)) => {
            let mut complete = true;
            let mut end = 0u64;
            for (index, line) in bytes.split_inclusive(|b| *b == b'\n').enumerate() {
                end += line.len() as u64;
                let origin = source(path, root, protected, Some(index + 1));
                let result = if !line.ends_with(b"\n") { Err("unclosed final line (not read)") }
                    else { valid(line, validation) };
                match result {
                    Ok(record) if !["brief", "work_graph"].contains(&record["kind"].as_str().unwrap()) =>
                        rows.push(Row { record, bytes: line.to_vec(), source: origin, log_end: Some(end) }),
                    Ok(_) => { complete = false; limits.push(issue(&origin, "brief/graph belongs in its own file (not used as a log entry)")); },
                    Err(reason) => { complete = false; limits.push(issue(&origin, reason)); },
                }
            }
            ("read", complete, Some(bytes))
        }
        Ok(None) => { limits.push(issue(&origin, "source missing; no empty-work conclusion")); ("missing", false, None) },
        Err(reason) => { limits.push(issue(&origin, &format!("source unreadable: {reason}"))); ("unreadable", false, None) },
    };
    if protected {
        for row in &rows {
            if !OBSERVED.contains(&row.kind()) || row.record["recorder"]["kind"] != "App" {
                complete = false;
                limits.push(issue(&row.source, "protected fleet log contains a record outside the App observation kinds"));
            }
        }
    }
    LogRead { rows, bytes, complete, view: json!({"source":origin,"status":status,"complete":complete}) }
}

fn files(census: &mut Census, root: &Path, folder: &Path, graphs: bool, validation: &jsonschema::Validator, limits: &mut Vec<Value>) -> Vec<Row> {
    let mut rows = Vec::new();
    let paths = match census.directory(folder) {
        Ok(paths) => paths,
        Err(reason) => { limits.push(issue(&source(folder,root,false,None), &reason)); return rows; },
    };
    if census.stamps.get(folder) == Some(&None) {
        limits.push(issue(&source(folder,root,false,None), "fleet folder missing; no empty-work conclusion"));
    }
    for path in paths {
        if graphs {
            let revisions = match census.directory(&path) {
                Ok(paths) => paths,
                Err(reason) => { limits.push(issue(&source(&path,root,false,None), &reason)); continue; },
            };
            for file in revisions { read_record_file(census, root, &file, "work_graph", validation, limits, &mut rows); }
        } else {
            read_record_file(census, root, &path, "brief", validation, limits, &mut rows);
        }
    }
    rows
}
fn read_record_file(census: &mut Census, root: &Path, path: &Path, kind: &str, validation: &jsonschema::Validator, limits: &mut Vec<Value>, rows: &mut Vec<Row>) {
    let origin = source(path,root,false,None);
    if path.extension().is_none_or(|e| e != "json") {
        limits.push(issue(&origin, "unknown fleet file member (not read)"));
        return;
    }
    match census.read(path) {
        Ok(Some(bytes)) => match valid(&bytes, validation) {
            Ok(record) if record["kind"] == kind => rows.push(Row {record,bytes,source:origin,log_end:None}),
            Ok(_) => limits.push(issue(&origin, "record kind does not belong in this folder (not read)")),
            Err(reason) => limits.push(issue(&origin,reason)),
        },
        Ok(None) => limits.push(issue(&origin,"source disappeared (not read)")),
        Err(reason) => limits.push(issue(&origin,&format!("source unreadable: {reason}"))),
    }
}

struct Protected { dir: PathBuf, store: PathBuf, history: HistorySource, retention: Value, provenance_protected: bool, package_provenance: Result<Value,String>, view: Value, _admission: std::fs::File }
/// Read-only identity inspection. It deliberately calls neither attach/opened
/// nor a creating admission helper: absent identity/guard files stay absent.
fn protected(census: &mut Census, root: &Path, limits: &mut Vec<Value>) -> Result<Protected, String> {
    let configured = records_store::current()?;
    let store = configured.root.canonicalize().map_err(|_| "configured records store is absent/unavailable; nothing created")?;
    if store.starts_with(root) || root.starts_with(&store) { return Err("records store overlaps the selected project; no protected counterpart".into()); }
    // Use the existing placement check, not its human-readable warning text.
    // Test placement is an invented source fixture, never a production route.
    let protection_limits = records_store::placement_problems(&store,Some(root),&[],configured.placement == records_store::Placement::Test);
    let provenance_protected = protection_limits.is_empty();
    for reason in &protection_limits {
        limits.push(json!({"source":{"home":"configured records store"},"reason":format!("store placement cannot establish protected App provenance: {reason}; matching bytes/order remain quoted evidence")}));
    }
    census.directory(&store)?;
    let read_json = |census: &mut Census, path: &Path| -> Result<Value,String> {
        let bytes = census.read(path)?.ok_or("identity source missing; nothing minted or registered")?;
        serde_json::from_slice(&bytes).map_err(|_| "identity source is not JSON".into())
    };
    let identity = read_json(census,&store.join("store.json"))?;
    if identity["format"] != "chirality.records-store" || identity["formatVersion"] != "0.1"
        || identity["storeId"].as_str().is_none_or(str::is_empty) { return Err("configured store identity invalid".into()); }
    if let Some((known_root,known_id)) = records_store::known_identity_for_read(&configured.root,&store) {
        if known_root != store || identity["storeId"] != known_id {
            return Err("already opened records store identity/alias changed; no silent reassociation".into());
        }
    }
    let roots_path = store.join("roots.jsonl");
    let bytes = census.read(&roots_path)?.ok_or("protected root registry absent; nothing attached")?;
    if !bytes.is_empty() && !bytes.ends_with(b"\n") { return Err("protected root registry has an unclosed final line; association unknown".into()); }
    let mut roots = BTreeMap::new();
    for line in bytes.split_inclusive(|b| *b == b'\n') {
        let row: Value = serde_json::from_slice(line).map_err(|_| "protected root registry unreadable")?;
        if row["format"] != "chirality.records-store.root" || row["formatVersion"] != "0.1"
            || row["root"].as_str().is_none_or(str::is_empty) || row["projectId"].as_str().is_none_or(str::is_empty)
            || !matches!(row["how"].as_str(),Some("minted" | "registered" | "adopted" | "released")) {
                return Err("protected root registry invalid/unknown transition; association unknown".into());
            }
        roots.insert((row["projectId"].as_str().unwrap().to_owned(), row["root"].as_str().unwrap().to_owned()), row["how"] != "released");
    }
    let canonical = root.to_str().ok_or("project path has no supported store association")?;
    let here: Vec<_> = roots.iter().filter(|((_, r), on)| **on && r == canonical).map(|((p,_),_)|p.clone()).collect();
    if here.len() != 1 { return Err("selected root has no unique protected project association; nothing attached".into()); }
    let project = here[0].clone();
    if roots.iter().any(|((p,r), on)| *on && p == &project && r != canonical) { return Err("protected identity has multiple current roots; association unknown".into()); }
    let link_path = root.join(records_store::PROJECT_LINK);
    let link = read_json(census,&link_path)?;
    if link["format"] != "chirality.project-link" || link["formatVersion"] != "0.1"
        || link["projectId"].as_str().is_none_or(str::is_empty) || link["storeId"].as_str().is_none_or(str::is_empty) {
        return Err("project identity link missing/unreadable; nothing attached".into());
    }
    if link["projectId"] != project || link["storeId"] != identity["storeId"] {
        limits.push(issue(&source(&link_path,root,false,None), "project link differs from the protected root association, which governs"));
    }
    let dir = records_store::project_dir(&store,&project);
    let admin = store.join("administration").join(storage::key(&project));
    // Share only an existing stable gate, without creating or repairing it.
    // Native disposal takes the exclusive side; a busy source is explicit.
    let gate = admin.join(".admission.lock");
    let metadata = census.metadata(&gate)?.ok_or("protected admission file absent; nothing created")?;
    if !metadata.is_file() || metadata.nlink() != 1 { return Err("protected admission file is not regular/single-link".into()); }
    let admission = crate::records_index::open_log(&gate).map_err(|e|e.to_string())?;
    if Stamp::of(&admission.metadata().map_err(|e|e.to_string())?) != Stamp::of(&metadata) {
        return Err("protected admission file changed while opening".into());
    }
    if unsafe { libc::flock(admission.as_raw_fd(),libc::LOCK_SH | libc::LOCK_NB) } != 0 {
        return Err("protected project admission busy/unavailable; refresh later".into());
    }
    // Observe the complete administrative inventory before the existing pure
    // state reader. No lock or history marker is created by this read.
    census.directory(&admin)?;
    let events = census.directory(&admin.join("events"))?;
    census.read(&admin.join("history-started.json"))?;
    for path in events { census.read(&path)?.ok_or("administrative source disappeared")?; }
    let retention = crate::records_retention::view(&dir);
    if retention["disposition"] != "kept" {
        return Err(format!("protected project payload unavailable ({})",retention["disposition"].as_str().unwrap_or("unknown")));
    }
    let project_identity = read_json(census,&dir.join("project.json"))?;
    if project_identity["format"] != "chirality.records-store.project" || project_identity["formatVersion"] != "0.1" || project_identity["projectId"] != project {
        return Err("protected project identity invalid; nothing attached".into());
    }
    let history = HistorySource {selected_project:root.to_owned(),store:store.clone(),
        store_id:identity["storeId"].as_str().unwrap().to_owned(),project_id:project.clone(),log:dir.join("fleet").join(LOG)};
    // Controls are observed before payload bytes and again after the packet.
    // Missing/changed origin evidence never acquires authority from placement.
    let package_provenance = records_store::package::provenance_context(&dir);
    Ok(Protected {dir,store:store.clone(),history,retention,provenance_protected,package_provenance,_admission:admission,
        view:json!({"state":"attached","projectId":project,"storeId":identity["storeId"],"placement":configured.placement.label(),"placementLimits":configured.limits,"protectionLimits":protection_limits,"provenanceProtected":provenance_protected,"root":store.to_string_lossy(),"nativeRoot":crate::attachments::native_path_identity(&store),"standing":"configured store file observations; unsigned, no person or supplier origin authenticated"})})
}

fn duplicates(rows: &[Row], limits: &mut Vec<Value>, where_: &str) -> BTreeSet<String> {
    let mut seen = BTreeSet::new();
    let mut duplicate = BTreeSet::new();
    for row in rows {
        if !seen.insert(row.id().to_owned()) { duplicate.insert(row.id().to_owned()); }
    }
    for row in rows {
        if duplicate.contains(row.id()) { limits.push(issue(&row.source,&format!("duplicate/conflicting recordId in {where_}; no copy chosen"))); }
    }
    let mut native_receipts:BTreeMap<String,Vec<&Row>>=BTreeMap::new();
    for row in rows.iter().filter(|r|r.record["formatVersion"]=="0.2"&&r.kind()=="related_conversation") {
        if let Ok(key)=crate::native_conversation_links::receipt_key(&row.record){native_receipts.entry(key).or_default().push(row);}
    }
    for copies in native_receipts.values().filter(|rows|rows.len()>1){for row in copies{
        duplicate.insert(row.id().to_owned());
        limits.push(issue(&row.source,&format!("duplicate/conflicting original native request identity in {where_}; no relationship chosen")));
    }}
    duplicate
}

/// The native adapter supplies its selected workspace, never a webview path.
pub(crate) fn read_for_workspace(workspace: Option<&Path>) -> Result<Value,String> {
    let configured = workspace.ok_or("no selected project workspace; no fleet source read")?;
    let root = configured.canonicalize().map_err(|_| "selected project workspace unavailable")?;
    let before = std::fs::metadata(&root).map_err(|e|e.to_string())?;
    if !before.is_dir() { return Err("selected workspace is not a folder".into()); }
    let validation = validator()?;
    let mut census = Census::default();
    let mut limits = Vec::new();
    let _ = census.directory(&root.join(".chirality")).map_err(|e| limits.push(issue(&source(&root.join(".chirality"),&root,false,None),&e)));
    let folder = root.join(FOLDER);
    let _ = census.directory(&folder).map_err(|e| limits.push(issue(&source(&folder,&root,false,None),&e)));
    let briefs = files(&mut census,&root,&folder.join("briefs"),false,validation,&mut limits);
    let graphs = files(&mut census,&root,&folder.join("graphs"),true,validation,&mut limits);
    let project_log = read_log(&mut census,&folder.join(LOG),&root,false,validation,&mut limits);
    let mut all_project = briefs.clone(); all_project.extend(graphs.clone()); all_project.extend(project_log.rows.clone());
    let project_duplicates = duplicates(&all_project,&mut limits,"project fleet sources");
    let attachment = protected(&mut census,&root,&mut limits);
    let (mut protected_view, mut protected_log, healthy) = match &attachment {
        Ok(attached) => {
            let mut log = read_log(&mut census,&attached.dir.join("fleet").join(LOG),&attached.dir,true,validation,&mut limits);
            let duplicate = duplicates(&log.rows,&mut limits,"protected fleet log");
            log.complete &= duplicate.is_empty();
            log.view["complete"] = json!(log.complete);
            (attached.view.clone(), Some(log), true)
        },
        Err(reason) => {
            limits.push(json!({"source":{"home":"protected records store"},"reason":reason}));
            (json!({"state":"unavailable","reason":reason}), None, false)
        }
    };
    let mut complete_copy = healthy && protected_log.as_ref().is_some_and(|log|log.complete);
    let quoted_prefix = match (&attachment, &protected_log) {
        (Ok(attached),Some(log)) => {
            let origin = attached.package_provenance.as_ref().map_err(Clone::clone).and_then(|_| {
                let bytes = log.bytes.as_deref().ok_or("protected log bytes unavailable for package-origin comparison")?;
                let prefix = records_store::package::quoted_prefix(&attached.dir,&format!("fleet/{LOG}"),bytes)?;
                if prefix > bytes.len() as u64 { return Err("imported prefix exceeds the protected log length".into()); }
                Ok(prefix)
            });
            match origin {
                Ok(prefix) => {
                    if prefix > 0 { limits.push(issue(&source(&attached.history.log,&attached.dir,true,None),
                        "imported package prefix is quoted evidence; its bytes establish no App observation or native relationship")); }
                    Some(prefix)
                },
                Err(reason) => {
                    limits.push(issue(&source(&attached.history.log,&attached.dir,true,None),
                        &format!("package provenance unavailable; no protected App provenance: {reason}")));
                    None
                },
            }
        },
        _ => None,
    };
    for row in project_log.rows.iter().filter(|r|r.kind() == "current_graph") {
        if row.record["body"]["graphContent"]["method"] != crate::util::FILE_IDENTITY_METHOD {
            limits.push(issue(&row.source,"graph-content identity method is unselected/unsupported; selector is quoted and no graph is selected"));
        }
    }
    let view_inputs = views::read_inputs(&mut census, &root, &graphs);
    #[cfg(test)] AFTER_READ.with(|h| { if let Some(hook) = h.borrow_mut().take() { hook(); } });
    let final_physical = configured.canonicalize().ok().filter(|p|p == &root).and_then(|p|std::fs::metadata(p).ok());
    if final_physical.as_ref().is_none_or(|m|m.dev()!=before.dev() || m.ino()!=before.ino()) {
        return Err("selected physical project changed while reading; refresh without reassigning the snapshot".into());
    }
    let final_check = census.unchanged().and_then(|()| match &attachment {
        Ok(attached) if records_store::current()?.root.canonicalize().map_err(|e|e.to_string())? != attached.store =>
            Err("configured records store changed while reading".into()),
        Ok(attached) if crate::records_retention::view(&attached.dir) != attached.retention =>
            Err("protected project administration changed while reading".into()),
        _ => Ok(()),
    });
    let snapshot_stable = final_check.is_ok();
    if let Err(reason) = final_check {
        complete_copy = false;
        protected_view["state"] = json!("source changed while reading");
        limits.push(json!({"source":{"home":"fleet snapshot"},"reason":reason}));
        if let Some(log) = &mut protected_log {
            log.view["complete"] = json!(false);
            log.rows.clear();
        }
    }
    let provenance_stable = match &attachment {
        Ok(attached) => match (&attached.package_provenance,records_store::package::provenance_context(&attached.dir)) {
            (Ok(before),Ok(after)) if before == &after => true,
            (Ok(_),Ok(_)) => {
                limits.push(issue(&source(&attached.history.log,&attached.dir,true,None),
                    "package provenance changed while reading; stable bytes/order remain quoted, with no protected App provenance"));
                false
            },
            (_,Err(reason)) => {
                limits.push(issue(&source(&attached.history.log,&attached.dir,true,None),
                    &format!("package provenance unavailable after reading; no protected App provenance: {reason}")));
                false
            },
            (Err(_),Ok(_)) => false,
        },
        Err(_) => false,
    };
    if let (Ok(attached),Some(log)) = (&attachment,&mut protected_log) {
        if let Err(reason) = observe_prefix(&attached.history,log.bytes.as_deref(),complete_copy) {
            complete_copy = false;
            log.complete = false;
            log.view["complete"] = json!(false);
            protected_view["state"] = json!("history changed/unavailable");
            limits.push(issue(&source(&attached.history.log,&attached.dir,true,None),&reason));
        }
    }
    let trusted = complete_copy && provenance_stable && quoted_prefix.is_some()
        && attachment.as_ref().is_ok_and(|a|a.provenance_protected);
    let row_trusted = |row: &Row| trusted && quoted_prefix.is_some_and(|prefix|row.follows_quoted_prefix(prefix));
    let row_imported = |row: &Row| quoted_prefix.is_some_and(|prefix|!row.follows_quoted_prefix(prefix));
    let quoted_standing = "configured store bytes/order as quoted evidence; protected App provenance is not established";
    let imported_standing = "imported package row; quoted evidence, with no local App observation or native relationship established";
    let mut observations = Vec::new();
    let mut governing_store = Vec::new();
    if complete_copy {
        let log = protected_log.as_ref().unwrap();
        for (order,row) in log.rows.iter().enumerate() {
            let matches: Vec<_> = project_log.rows.iter().filter(|p|p.bytes == row.bytes).map(|p|p.source.clone()).collect();
            if matches.is_empty() { limits.push(issue(&row.source,"store row has no exact project counterpart; store copy/order still governs")); }
            let mut value = row.view(if row_imported(row) {imported_standing} else if row.record["formatVersion"]=="0.1" {"quoted 0.1 compatibility record; undertaking/thread fields establish no native conversation relationship"} else if row_trusted(row) {"App observation from the attached protected copy; unsigned"} else {quoted_standing});
            value["storeOrder"] = json!(order + 1);
            value["protectedOrder"] = json!(row_trusted(row).then_some(order + 1));
            value["projectCounterparts"] = json!(matches);
            if row_trusted(row) { observations.push(value.clone()); }
            governing_store.push(value);
        }
    }
    let project_rows: Vec<_> = project_log.rows.iter().map(|row| {
        let mut value = row.view("project-file claim; recorder as recorded");
        if OBSERVED.contains(&row.kind()) {
            let matched = complete_copy.then(|| protected_log.as_ref().unwrap().rows.iter().position(|p|p.bytes == row.bytes)).flatten();
            let matched_trusted = matched.is_some_and(|n|row_trusted(&protected_log.as_ref().unwrap().rows[n]));
            let matched_imported = matched.is_some_and(|n|row_imported(&protected_log.as_ref().unwrap().rows[n]));
            value["storeOrder"] = json!(matched.map(|n|n+1));
            value["protectedOrder"] = json!(matched.filter(|_|matched_trusted).map(|n|n+1));
            value["reconciliation"] = json!(if matched_trusted {"exact protected counterpart; protected order governs"} else if matched_imported {"exact imported package counterpart; store order governs as quoted evidence, with no local App provenance"} else if matched.is_some() {"exact configured store counterpart; store order governs, but protected App provenance is not established"} else {"no healthy exact protected counterpart; not an App observation"});
            if !matched_trusted { limits.push(issue(&row.source,"App-named project entry lacks a healthy exact protected counterpart; retained only as the recorder's claim")); }
            if project_duplicates.contains(row.id()) { value["projectReplayOrConflict"] = json!(true); }
        }
        value
    }).collect();
    let protected_rows: Vec<_> = protected_log.as_ref().map(|log|log.rows.iter().map(|row|row.view(if !complete_copy {"configured-store claim; source incomplete/unavailable"} else if row_imported(row) {imported_standing} else if row_trusted(row) {"protected copy; see governing order"} else {quoted_standing})).collect()).unwrap_or_default();
    let native_relationships:Vec<_>=observations.iter().filter(|v|v["record"]["formatVersion"]=="0.2"&&v["record"]["kind"]=="related_conversation").cloned().collect();
    let recording_events:Vec<_>=observations.iter().filter(|v|v["record"]["formatVersion"]=="0.2"&&v["record"]["kind"]!="related_conversation").cloned().collect();
    let workspace = views::derive(&briefs, &graphs, &project_log, &project_duplicates,
        &observations, &view_inputs, snapshot_stable);
    Ok(json!({"format":"chirality.fleet.read","formatVersion":"0.2","standing":STANDING,
        "project":{"configuredRoot":configured.to_string_lossy(),"canonicalRoot":root.to_string_lossy(),"nativeRoot":crate::attachments::native_path_identity(&root),"physical":{"device":before.dev(),"inode":before.ino()}},
        "schema":{"format":"chirality.fleet.record","versions":["0.1 quoted compatibility","0.2 native-links"]},
        "briefs":briefs.iter().map(|r|r.view("prepared brief; quoted file, no dispatch inferred")).collect::<Vec<_>>(),
        "graphs":graphs.iter().map(|r|r.view("graph revision; quoted file; see workspace for verified selector and derived file claims")).collect::<Vec<_>>(),
        "coordination":{"project":project_log.view,"projectRecords":project_rows,"protected":protected_view,
            "protectedLog":protected_log.as_ref().map(|log|&log.view),"protectedRecords":protected_rows,"governingStoreRecords":governing_store,"appObservations":observations,"nativeRelationships":native_relationships,"recordingEvents":recording_events},
        "workspace":workspace,
        "limits":limits,"nativeRecording":"Only actual App Fork/Continue-as source-issued request/result observations produce 0.2 relationships. Source files are quoted on read, never native authority; 0.1 undertaking fields establish no native join. Completed spawn prompt remains unavailable; no current native dispatch or child state is inferred from the derived file workspace."}))
}

#[cfg(test)]
thread_local! { static AFTER_READ: std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const { std::cell::RefCell::new(None) }; }
#[cfg(test)]
#[path = "fleet_records_tests.rs"]
mod tests;
