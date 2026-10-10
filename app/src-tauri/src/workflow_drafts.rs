//! Workflow draft workspace in the Rust host (WR §3, §4.2 TT-3/TT-4, §5.1, §6
//! SQ-D D-2…D-4). The owner's OI-008 ruling for this workspace places draft
//! observation, content identity, hygiene and the trial pointer here; the
//! TypeScript interface only lists and presents what this module reports.
//!
//! Nothing here is registration, review, a run or an act. A listed draft has no
//! workflow identity (EXEC TR-1); trying one is ordinary conversation input
//! that the person sends (K-7; NIR AT-8); a trial pointer is an App-kept
//! pointer, not a run record, compatibility evidence or A15 evidence (TT-4).
use super::{read_ledger, slot_lines, LibraryOwner};
use crate::attachments::{DraftTrialReference, SelectedTextAttachment, TEXT_FILE_BOUND};
use crate::storage;
use crate::workflow_workspace::{valid_name, Snapshot, SNAPSHOT_METHOD};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    fs,
    path::{Path, PathBuf},
};

/// WR §3: drafts of a library live in `<library>/.chirality/workflow-drafts/<name>/`.
pub(crate) const DRAFTS: &str = ".chirality/workflow-drafts";
/// WR §3 "Trial pointers | App data folder | The App": this sub-path is the
/// implementation's, beside the App-kept draft bases (`runtime/wr/draft-bases`).
pub(crate) const TRIAL_POINTERS: &str = "runtime/wr/trial-pointers";
/// U-WR-7 as resolved by the integrator (WR §4.5 HY-5): at most 1 000 regular
/// files and 16 MiB of regular-file bytes per package.
pub(crate) const MAX_FILES: usize = crate::workflow_workspace::PACKAGE_MAX_FILES;
pub(crate) const MAX_BYTES: u64 = crate::workflow_workspace::PACKAGE_MAX_BYTES;
/// TT-4's fixed standing sentence (WR schema `trial_pointer.standing`).
pub(crate) const TRIAL_STANDING: &str =
    "draft tried in conversation; not a run of any workflow identity";

/// Metadata-only pre-scan before any file is read: refuses non-regular entries
/// (HY-3) and stops as soon as the HY-5 bound is exceeded, so an oversized or
/// linked folder is never read into memory. Returns (files, bytes).
pub(crate) fn prescan(root: &Path) -> Result<(usize, u64), String> {
    fn walk(base: &Path, dir: &Path, files: &mut usize, bytes: &mut u64) -> Result<(), String> {
        let mut entries = fs::read_dir(dir)
            .map_err(|e| format!("draft folder unreadable: {}: {e}", dir.display()))?
            .collect::<Result<Vec<_>, _>>()
            .map_err(|e| format!("draft folder unreadable: {}: {e}", dir.display()))?;
        entries.sort_by_key(|e| e.file_name());
        for entry in entries {
            let path = entry.path();
            let relative = path.strip_prefix(base).unwrap_or(&path).display().to_string();
            let meta = fs::symlink_metadata(&path)
                .map_err(|e| format!("draft entry unreadable: {relative}: {e}"))?;
            let ty = meta.file_type();
            if ty.is_dir() {
                walk(base, &path, files, bytes)?;
            } else if ty.is_file() {
                *files += 1;
                *bytes = bytes.saturating_add(meta.len());
                if *files > MAX_FILES || *bytes > MAX_BYTES {
                    return Err(format!(
                        "HY-5: package exceeds review bound ({MAX_FILES} files / 16 MiB)"
                    ));
                }
            } else {
                return Err(format!("HY-3: non-regular entry {relative}"));
            }
        }
        Ok(())
    }
    let (mut files, mut bytes) = (0, 0);
    walk(root, root, &mut files, &mut bytes)?;
    Ok((files, bytes))
}

/// HY-2: the folder name follows WD's name rule and equals the front-matter
/// `name` (read the same way the review reads it, `Review::open`).
fn name_finding(folder: &str, snapshot: &Snapshot) -> Option<String> {
    if !valid_name(folder) {
        return Some(format!(
            "HY-2: folder name {folder:?} does not follow the workflow name rule"
        ));
    }
    let normalized = snapshot
        .workflow_text()
        .replace("\r\n", "\n")
        .replace('\r', "\n");
    let declared = normalized
        .strip_prefix("---\n")
        .and_then(|s| s.split_once("\n---"))
        .and_then(|(fm, _)| {
            fm.lines()
                .find_map(|l| l.strip_prefix("name:").map(str::trim))
        });
    match declared {
        Some(name) if name == folder => None,
        Some(name) => Some(format!(
            "HY-2: front-matter name {name:?} differs from the folder name {folder:?}"
        )),
        None => Some("HY-2: WORKFLOW.md front matter names no workflow".into()),
    }
}

/// D-2 over one folder: content identity and hygiene, or the reason the content
/// identity is not obtainable. Never reads past the HY-5 bound.
pub(crate) struct FolderReading {
    pub content: Result<Snapshot, String>,
    pub findings: Vec<String>,
}
pub(crate) fn read_folder(folder: &str, path: &Path) -> FolderReading {
    if let Err(cause) = storage::check_path(path) {
        return FolderReading {
            content: Err(cause.clone()),
            findings: vec![format!("HY-3: non-regular entry: {cause}")],
        };
    }
    if let Err(cause) = prescan(path) {
        let findings = if cause.starts_with("HY-") {
            vec![cause.clone()]
        } else {
            vec![]
        };
        return FolderReading {
            content: Err(cause),
            findings,
        };
    }
    match Snapshot::capture(path) {
        Ok(snapshot) => {
            let mut findings = snapshot.hygiene_findings();
            findings.extend(name_finding(folder, &snapshot));
            FolderReading {
                content: Ok(snapshot),
                findings,
            }
        }
        Err(cause) => FolderReading {
            findings: if cause.starts_with("HY-") {
                vec![cause.clone()]
            } else {
                vec![]
            },
            content: Err(cause),
        },
    }
}

/// One observed draft (D-2), kept between observations to derive D-4 transitions.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct ObservedDraft {
    pub name: String,
    pub state: String,
    /// The draft content identity value (SNAPSHOT_METHOD), when established.
    pub content: Option<String>,
}

/// The observation of one library's drafts folder at one time.
#[derive(Clone, Debug, Default)]
pub(crate) struct DraftObservation {
    pub drafts: Vec<Value>,
    pub transitions: Vec<Value>,
    pub limit: Option<String>,
    /// Transitions observed but not conforming to the WR schema: named, never
    /// silently dropped.
    pub transition_limits: Vec<String>,
    pub observed: Vec<ObservedDraft>,
}

/// Where a draft's files were last changed, as far as this App observed it
/// (D-3). `app_made` maps a draft name to the content the App itself wrote.
pub(crate) struct Attribution<'a> {
    pub native_items: &'a Value,
    pub app_made: &'a BTreeMap<String, String>,
}
impl Attribution<'_> {
    fn of(&self, name: &str, content: Option<&str>, folder: &Path) -> Value {
        if content.is_some() && self.app_made.get(name).map(String::as_str) == content {
            return json!({"kind":"app action"});
        }
        // D-3: a supplier fileChange item naming a path in the folder
        // (observed-in-generated-types: FileChangeThreadItem.changes[].path).
        // Only absolute paths are compared; a relative path is not resolved.
        let mut found: Option<(u64, Value)> = None;
        for row in self.native_items.as_array().into_iter().flatten() {
            let native = &row["native"];
            if native["type"] != "fileChange" {
                continue;
            }
            let names_folder = native["changes"].as_array().into_iter().flatten().any(|c| {
                [c["path"].as_str(), c["kind"]["move_path"].as_str()]
                    .into_iter()
                    .flatten()
                    .any(|p| Path::new(p).is_absolute() && Path::new(p).starts_with(folder))
            });
            let order = row["observedOrder"].as_u64().unwrap_or(0);
            if names_folder && found.as_ref().is_none_or(|(o, _)| order >= *o) {
                if let (Some(thread), Some(item)) = (row["threadId"].as_str(), native["id"].as_str()) {
                    found = Some((order, json!({"kind":"file change item","thread":thread,"item":item})));
                }
            }
        }
        found
            .map(|(_, a)| a)
            .unwrap_or_else(|| json!({"kind":"not observed"}))
    }
}

/// WR finding codes for the schema; an unmapped cause stays in `content`.
fn finding(detail: &str) -> Option<Value> {
    super::finding(detail)
}

impl LibraryOwner {
    fn drafts_root(&self) -> PathBuf {
        self.root.join(DRAFTS)
    }
    /// D-2/D-4 observation of every draft folder of this library, with WR §5.1
    /// states. `review_state(name)` supplies the state of a review this process
    /// holds for the draft (*under review* / *changed since review*), if any.
    /// The first observation of a library is a baseline: no transition is
    /// invented for changes that happened before it.
    pub(crate) fn observe_drafts(
        &self,
        previous: Option<&[ObservedDraft]>,
        attribution: &Attribution<'_>,
        review_state: &dyn Fn(&str) -> Option<String>,
    ) -> DraftObservation {
        let root = self.drafts_root();
        let mut out = DraftObservation::default();
        if let Err(cause) = storage::check_path(&root) {
            out.limit = Some(format!(
                "drafts folder refused ({cause}); nothing outside the library is listed"
            ));
            return out;
        }
        let entries = match fs::read_dir(&root) {
            Ok(entries) => entries,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                out.limit = Some(format!(
                    "no drafts folder yet ({DRAFTS}); a draft appears here when the agent, the person or the App writes one"
                ));
                return self.finish(out, previous, attribution);
            }
            Err(e) => {
                out.limit = Some(format!("drafts folder unreadable: {}: {e}", root.display()));
                return out;
            }
        };
        let mut names = vec![];
        for entry in entries {
            match entry {
                Ok(entry) => names.push(entry.file_name()),
                Err(e) => {
                    out.limit = Some(format!("drafts folder listing incomplete: {e}"));
                }
            }
        }
        names.sort();
        let ledger = read_ledger(&self.root);
        for os_name in names {
            let Some(name) = os_name.to_str().map(str::to_owned) else {
                out.drafts.push(json!({"name":os_name.to_string_lossy(),"state":"not valid",
                    "findings":[{"code":"HY-2 name","detail":"folder name is not UTF-8"}],
                    "content":{"not_established":"folder name is not UTF-8"},
                    "tryLimit":"not listed as a draft: its name cannot be represented","reviewLimit":"not reviewable"}));
                continue;
            };
            if name.starts_with('.') {
                continue; // hidden staging/editor entries are not drafts
            }
            let path = root.join(&name);
            let meta = fs::symlink_metadata(&path);
            if !meta.as_ref().is_ok_and(|m| m.file_type().is_dir()) {
                let detail = match &meta {
                    Ok(m) if m.file_type().is_symlink() => "a symbolic link, not a draft folder; links are never followed".to_string(),
                    Ok(_) => "not a folder".to_string(),
                    Err(e) => format!("unreadable: {e}"),
                };
                let finding = format!("HY-3: {name} is {detail}");
                let reference = json!({"record_kind":"draft_reference","draft":self.draft_key(&name),"state":"not valid",
                    "content":{"not_established":detail},"base":null,"base_recorded_by":"none",
                    "findings":[{"code":"HY-3 non-regular entry","detail":finding}],"observed_at":crate::util::now_rfc3339()});
                out.drafts.push(json!({"name":name,"state":"not valid","reference":reference,
                    "schemaLimit":crate::workflow_workspace::wr_validate("draft_reference", &reference).err(),
                    "findings":[finding],"content":{"not_established":detail},"attribution":{"kind":"not observed"},
                    "tryLimit":"cannot be tried: not a draft folder","reviewLimit":"cannot be reviewed for registration (DS-5): not a draft folder"}));
                out.observed.push(ObservedDraft { name, state: "not valid".into(), content: None });
                continue;
            }
            out.drafts.push(self.observe_one(&name, &path, attribution, review_state, &ledger, &mut out.observed));
        }
        self.finish(out, previous, attribution)
    }

    fn observe_one(
        &self,
        name: &str,
        path: &Path,
        attribution: &Attribution<'_>,
        review_state: &dyn Fn(&str) -> Option<String>,
        ledger: &Result<Vec<Value>, String>,
        observed: &mut Vec<ObservedDraft>,
    ) -> Value {
        let reading = read_folder(name, path);
        let base = self.base_custody().get(name);
        let (base_value, base_state, base_source) = match &base {
            Ok(o) => (
                o.base.clone(),
                o.source["record"]["state"].as_str().map(str::to_owned),
                o.source.clone(),
            ),
            Err(cause) => (None, None, json!({"limit":cause})),
        };
        let content = reading.content.as_ref().ok().map(|s| s.revision().to_string());
        let findings: Vec<Value> = reading.findings.iter().filter_map(|f| finding(f)).collect();
        // WR §5.1 state, in this order: not valid; a review this process holds;
        // registered and unchanged since (the App recorded it at G-6 and the
        // bytes still equal that revision); otherwise draft.
        let state = if content.is_none() || !reading.findings.is_empty() {
            "not valid".to_string()
        } else if let Some(review) = review_state(name) {
            review
        } else if base_state.as_deref() == Some("registered, unchanged since")
            && base_value.as_ref().map(|b| b.revision.as_str()) == content.as_deref()
        {
            "registered, unchanged since".to_string()
        } else {
            "draft".to_string()
        };
        let key = self.draft_key(name);
        let mut reference = json!({"record_kind":"draft_reference","draft":key,"state":state,
            "base":base_value,"base_recorded_by":if base_value.is_some(){"app"}else{"none"},
            "findings":findings,"observed_at":crate::util::now_rfc3339()});
        match &reading.content {
            Ok(snapshot) => {
                reference["content"] = json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()});
                reference["file_count"] = json!(snapshot.files().len());
            }
            Err(cause) => reference["content"] = json!({"not_established":cause}),
        }
        let schema = crate::workflow_workspace::wr_validate("draft_reference", &reference).err();
        // Registered revisions of the target slot, for the reader (SP-2: the
        // target slot is this library under the draft's folder name).
        let slot = match ledger {
            Ok(rows) if valid_name(name) => {
                let lines = slot_lines(rows, &self.origin, &self.source_root, name);
                let registered = lines.iter().filter(|l| l["outcome"] == "registered").count();
                json!({"registeredRevisions":registered,
                    "identicalTo":lines.iter().find(|l|l["outcome"]=="registered"&&content.as_deref().is_some_and(|c|l["identity"]["revision"]==c)).map(|l|l["sequence"].clone())})
            }
            Ok(_) => json!({"limit":"no target slot: the folder name is not a workflow name"}),
            Err(cause) => json!({"limit":cause}),
        };
        observed.push(ObservedDraft {
            name: name.into(),
            state: state.clone(),
            content: content.clone(),
        });
        let try_limit = match &reading.content {
            Err(cause) => Some(format!("cannot be tried: content identity not established ({cause})")),
            Ok(_) => None,
        };
        let review_limit = if state == "not valid" {
            Some(format!(
                "cannot be reviewed for registration (DS-5): {}",
                if reading.findings.is_empty() {
                    reading.content.as_ref().err().cloned().unwrap_or_default()
                } else {
                    reading.findings.join("; ")
                }
            ))
        } else {
            None
        };
        json!({"name":name,"state":state,"reference":reference,"schemaLimit":schema,
            "content":reference["content"],"fileCount":reference["file_count"],
            "findings":reading.findings,"base":base_value,"baseSource":base_source,
            "baseLimit":if base_value.is_none(){Some("no App-recorded base: a draft the agent or person wrote, or whose App-kept base is not in this App's data (WR §3, U-WR-12). A same-name registration is refused (DS-3); Refine a registered revision to make a draft with a base")}else{None},
            "attribution":attribution.of(name, content.as_deref(), path),
            "slot":slot,"tryLimit":try_limit,"reviewLimit":review_limit,
            "standing":"draft — not a registered workflow; no workflow identity (EXEC TR-1)"})
    }

    /// D-4 transitions against the previous observation of this library.
    fn finish(
        &self,
        mut out: DraftObservation,
        previous: Option<&[ObservedDraft]>,
        attribution: &Attribution<'_>,
    ) -> DraftObservation {
        let Some(previous) = previous else {
            return out; // baseline: earlier changes were not observed
        };
        let time = crate::util::now_rfc3339();
        let mut transitions = vec![];
        let folder = |name: &str| self.drafts_root().join(name);
        for now in &out.observed {
            let before = previous.iter().find(|p| p.name == now.name);
            let event = match before {
                None => Some("written"),
                Some(b) if b.state == "under review" && now.state == "changed since review" => Some("review stale"),
                Some(b) if b.content != now.content => Some("changed"),
                Some(b) if b.state != "under review" && now.state == "under review" => Some("review shown"),
                Some(_) => None,
            };
            if let Some(event) = event {
                let mut t = json!({"record_kind":"draft_transition","event":event,"draft":self.draft_key(&now.name),
                    "from":before.map_or("absent",|b|b.state.as_str()),"to":now.state,
                    "cause":match event {"written"=>"files appeared in the drafts folder","changed"=>"the folder's content identity changed","review stale"=>"changed since review (RB-3)","review shown"=>"review opened in this App",_=>"observed"},
                    "time":time,"attribution":attribution.of(&now.name, now.content.as_deref(), &folder(&now.name))});
                if let Some(c) = &now.content {
                    t["content"] = json!({"method":SNAPSHOT_METHOD,"value":c});
                }
                match crate::workflow_workspace::wr_validate("draft_transition", &t) {
                    Ok(()) => transitions.push(t),
                    Err(e) => out.transition_limits.push(format!("draft {}: {event} transition not reported: {e}", now.name)),
                }
            }
        }
        for gone in previous.iter().filter(|p| !out.observed.iter().any(|n| n.name == p.name)) {
            // §5.1 "Folder removed → the App's base pointer is dropped".
            let _ = self.base_custody().drop_if_removed(&gone.name, &folder(&gone.name));
            let t = json!({"record_kind":"draft_transition","event":"removed","draft":self.draft_key(&gone.name),
                "from":gone.state,"to":"removed","cause":"the draft folder is no longer present","time":time,
                "attribution":{"kind":"not observed"}});
            match crate::workflow_workspace::wr_validate("draft_transition", &t) {
                Ok(()) => transitions.push(t),
                Err(e) => out.transition_limits.push(format!("draft {}: removed transition not reported: {e}", gone.name)),
            }
        }
        out.transitions = transitions;
        out
    }

    pub(crate) fn draft_key(&self, name: &str) -> Value {
        json!({"draft_location":self.origin,"draft_root":self.drafts_root().display().to_string(),"name":name})
    }

    /// TT-3 (NIR AT-8, AT-9, AT-10): the draft's files as attachment sources for
    /// the composer, each carrying the draft reference. `WORKFLOW.md` first,
    /// then the other files in UTF-8 byte order of their paths. Pre-filling is
    /// not sending: the caller only adds these to the person's private list.
    /// Refuses a folder outside this library, a link, an unreadable or
    /// oversized package, and a `WORKFLOW.md` that cannot go as text.
    pub(crate) fn draft_trial_sources(&self, name: &str) -> Result<TrialSources, String> {
        if !valid_name(name) {
            return Err("Not a draft name of this library; nothing pre-filled".into());
        }
        let root = self.drafts_root();
        let path = root.join(name);
        storage::check_path(&path).map_err(|e| format!("Draft refused ({e}); nothing pre-filled"))?;
        match fs::symlink_metadata(&path) {
            Ok(m) if m.file_type().is_dir() => {}
            Ok(_) => return Err(format!("Draft {name} is not a folder; nothing pre-filled")),
            Err(e) => return Err(format!("Draft {name} not found ({e}); nothing pre-filled")),
        }
        prescan(&path).map_err(|e| format!("Draft {name} cannot be tried: {e}; nothing pre-filled"))?;
        let snapshot = Snapshot::capture(&path)
            .map_err(|e| format!("Draft {name} cannot be tried: {e}; nothing pre-filled"))?;
        let content = json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()});
        let draft = DraftTrialReference::new(&self.origin, name, content.clone())?
            .with_root(&root.display().to_string());
        let mut order: Vec<&String> = vec![];
        order.extend(snapshot.files().keys().filter(|p| p.as_str() == "WORKFLOW.md"));
        order.extend(snapshot.files().keys().filter(|p| p.as_str() != "WORKFLOW.md"));
        let mut selections = vec![];
        let mut not_attached = vec![];
        for relative in order {
            let bytes = &snapshot.files()[relative];
            let carriable = bytes.len() <= TEXT_FILE_BOUND
                && !bytes.contains(&0)
                && std::str::from_utf8(bytes).is_ok();
            if !carriable {
                if relative == "WORKFLOW.md" {
                    return Err(format!("Draft {name}: WORKFLOW.md cannot go as a text element (UTF-8, no NUL, at most {TEXT_FILE_BOUND} bytes; NIR AT-9); nothing pre-filled"));
                }
                not_attached.push(json!({"path":relative,"bytes":bytes.len(),
                    "reason":"not a text file within the text-element bound (NIR AT-9); the named-path carrier (AT-10) is not supplied by this App, so it is not attached"}));
                continue;
            }
            let file = path.join(relative);
            match SelectedTextAttachment::from_native_selection(file, Some(draft.clone())) {
                Ok(selected) => {
                    // The bytes selected must be the bytes observed in the draft.
                    if selected.snapshot()["identityAtSelection"]["value"]
                        != crate::util::sha256_hex(bytes)
                    {
                        return Err(format!("Draft {name} changed while it was read; try again. Nothing pre-filled"));
                    }
                    selections.push(selected);
                }
                Err(hold) => {
                    if relative == "WORKFLOW.md" {
                        return Err(format!("Draft {name}: WORKFLOW.md not attachable ({}); nothing pre-filled", hold.message));
                    }
                    not_attached.push(json!({"path":relative,"bytes":bytes.len(),"reason":hold.message}));
                }
            }
        }
        let reread = Snapshot::capture(&path)
            .map_err(|e| format!("Draft {name} changed while it was read ({e}); nothing pre-filled"))?;
        if reread.revision() != snapshot.revision() {
            return Err(format!("Draft {name} changed while it was read; try again. Nothing pre-filled"));
        }
        Ok(TrialSources {
            key: self.draft_key(name),
            content,
            selections,
            not_attached,
        })
    }
}

/// TT-3's composer sources for one draft.
#[derive(Debug)]
pub(crate) struct TrialSources {
    pub key: Value,
    pub content: Value,
    pub selections: Vec<SelectedTextAttachment>,
    pub not_attached: Vec<Value>,
}

/// TT-4 trial pointers, App-kept in the App data folder. Each pointer is one
/// WR `trial_pointer` record in its own create-once file; a pointer that
/// cannot be read back is reported, never dropped silently or rewritten.
#[derive(Default)]
pub(crate) struct TrialPointers {
    dir: Option<PathBuf>,
    pointers: Vec<Value>,
    limits: Vec<String>,
}
impl TrialPointers {
    /// Reads every pointer already kept under `app_data`.
    pub(crate) fn open(app_data: &Path) -> Self {
        let dir = app_data.join(TRIAL_POINTERS);
        let mut store = Self {
            dir: Some(dir.clone()),
            pointers: vec![],
            limits: vec![],
        };
        if let Err(cause) = storage::check_path(&dir) {
            store.limits.push(format!("trial pointers not readable: {cause}"));
            store.dir = None;
            return store;
        }
        let entries = match fs::read_dir(&dir) {
            Ok(entries) => entries,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return store,
            Err(e) => {
                store.limits.push(format!("trial pointers unreadable: {}: {e}", dir.display()));
                return store;
            }
        };
        let mut files: Vec<PathBuf> = vec![];
        for entry in entries {
            match entry {
                Ok(entry) => files.push(entry.path()),
                Err(e) => store.limits.push(format!("trial pointers listing incomplete: {}: {e}", dir.display())),
            }
        }
        let mut files: Vec<PathBuf> = files
            .into_iter()
            .filter(|p| {
                p.extension().is_some_and(|x| x == "json")
                    && !p.file_name().is_some_and(|n| n.to_string_lossy().starts_with('.'))
            })
            .collect();
        files.sort();
        for file in files {
            let shown = file.display().to_string();
            let read = crate::workflow_workspace::read_regular_file(&file)
                .map_err(|e| format!("trial pointer unreadable: {shown}: {e}"))
                .and_then(|bytes| {
                    serde_json::from_slice::<Value>(&bytes)
                        .map_err(|e| format!("trial pointer malformed: {shown}: {e}"))
                })
                .and_then(|value| {
                    crate::workflow_workspace::wr_validate("trial_pointer", &value)
                        .map(|()| value)
                        .map_err(|e| format!("trial pointer malformed: {shown}: {e}"))
                });
            match read {
                Ok(value) => store.pointers.push(value),
                Err(limit) => store.limits.push(limit),
            }
        }
        store
            .pointers
            .sort_by(|a, b| a["time"].as_str().cmp(&b["time"].as_str()));
        store
    }
    /// Records that the person sent this draft's content into `conversation`.
    /// Without an App data folder the pointer is held in this process only.
    pub(crate) fn record(&mut self, key: &Value, content: &Value, conversation: &str) -> Result<Value, String> {
        let pointer = json!({"record_kind":"trial_pointer","draft":key,"content":content,
            "conversation":conversation,"time":crate::util::now_rfc3339(),"standing":TRIAL_STANDING});
        crate::workflow_workspace::wr_validate("trial_pointer", &pointer)?;
        match &self.dir {
            Some(dir) => {
                let file = dir.join(format!("{}.json", crate::util::opaque_id("trial-")?));
                storage::create_json(&file, &pointer)?;
            }
            None => self
                .limits
                .push("trial pointer held in process memory only: App data folder not attached (WR §3)".into()),
        }
        self.pointers.push(pointer.clone());
        Ok(pointer)
    }
    /// The pointers of one draft key, oldest first.
    pub(crate) fn for_draft(&self, key: &Value) -> Vec<Value> {
        self.pointers
            .iter()
            .filter(|p| &p["draft"] == key)
            .cloned()
            .collect()
    }
    pub(crate) fn limits(&self) -> &[String] {
        &self.limits
    }
}

#[cfg(test)]
#[path = "workflow_drafts_tests.rs"]
mod tests;
