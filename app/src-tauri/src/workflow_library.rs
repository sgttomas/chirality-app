//! Owner-held hot registration. Readable ledger facts do not authenticate old acts.
use super::{
    DraftKey, RegisteredRevision, Review, Selection, Snapshot, WorkflowIdentity, SNAPSHOT_METHOD,
};
use crate::{act_control::HotA15Receipt, storage};
use serde_json::{json, Value};
use std::{
    cell::Cell,
    collections::HashMap,
    fs::{self, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
};

pub(crate) struct LibraryOwner {
    root: PathBuf,
    origin: String,
    source_root: String,
    bases: std::sync::Arc<std::sync::Mutex<HashMap<String, WorkflowIdentity>>>,
}
impl LibraryOwner {
    pub(crate) fn open(root: PathBuf, origin: &str, source_root: &str) -> Result<Self, String> {
        if !root.is_absolute()
            || !["project", "user"].contains(&origin)
            || source_root.is_empty()
            || source_root.contains(['\n', '\r'])
        {
            return Err("opened library context not established".into());
        }
        storage::check_path(&root)?;
        Ok(Self {
            root,
            origin: origin.into(),
            source_root: source_root.into(),
            bases: std::sync::Arc::new(std::sync::Mutex::new(HashMap::new())),
        })
    }
    /// Records only an actual closed source selection; draft-file tuples are not bases.
    pub(crate) fn record_base(&mut self, name: &str, selection: &Selection) -> Result<(), String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        self.bases
            .lock()
            .map_err(|_| "App-kept base state unavailable")?
            .insert(name.into(), selection.identity().clone());
        Ok(())
    }
    /// WR D-2/RB-1 listing observation: actual package bytes, not request identity.
    /// This digest is comparison data; it grants no review/capture/registration.
    pub(crate) fn listed_draft_revision(&self, name: &str) -> Result<String, String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        let path = self.root.join(".chirality/workflow-drafts").join(name);
        storage::check_path(&path)?;
        Ok(Snapshot::capture(&path)?.revision().to_string())
    }
    pub(crate) fn review_draft(
        &self,
        name: &str,
        list_revision: &str,
    ) -> Result<ReviewSession, String> {
        self.review(vec![name.into()], false, Some(list_revision))
    }
    pub(crate) fn review_in_place(&self, names: &[String]) -> Result<ReviewSession, String> {
        self.review(names.to_vec(), true, None)
    }
    fn review(
        &self,
        names: Vec<String>,
        in_place: bool,
        list_revision: Option<&str>,
    ) -> Result<ReviewSession, String> {
        if names.is_empty() || (!in_place && names.len() != 1) {
            return Err("one draft or ordered in-place entries required".into());
        }
        let mut unique = std::collections::HashSet::new();
        let ledger = read_ledger(&self.root)?;
        let review_ref = crate::util::opaque_id("review:")?;
        let descriptor_id = format!("descriptor:{review_ref}");
        let mut entries = Vec::new();
        for name in names {
            if !super::valid_name(&name) || !unique.insert(name.clone()) {
                return Err("invalid/duplicate review name".into());
            }
            let live = self
                .root
                .join(".chirality")
                .join(if in_place {
                    "workflows"
                } else {
                    "workflow-drafts"
                })
                .join(&name);
            storage::check_path(&live)?;
            let snapshot = Snapshot::capture(&live)?;
            let reread = Snapshot::capture(&live)?;
            let slot = slot_lines(&ledger, &self.origin, &self.source_root, &name);
            let prior = latest(&slot)?;
            let base = if in_place {
                None
            } else {
                self.bases
                    .lock()
                    .map_err(|_| "App-kept base state unavailable")?
                    .get(&name)
                    .cloned()
            };
            let identity =
                snapshot.identity(&self.origin, &self.source_root, &name, base.clone())?;
            let published = self.root.join(".chirality/workflows").join(&name);
            if in_place && prior.is_some() {
                return Err(
                    "entry has registration history; review its disclosed standing separately"
                        .into(),
                );
            }
            let disposition = if in_place {
                "in place"
            } else if let Some(prior) = &prior {
                if !base.as_ref().is_some_and(|b| lineage_reaches(b, prior)) {
                    return Err("DS-3: name taken; draft has no App-kept base in this slot".into());
                }
                if slot.iter().any(|e| {
                    e["outcome"] == "registered" && e["identity"]["revision"] == snapshot.revision()
                }) {
                    return Err(
                        "DS-4: identical revision; select existing standing separately".into(),
                    );
                }
                "new revision"
            } else if published.exists() {
                storage::check_path(&published)?;
                if Snapshot::capture(&published)?.files() != snapshot.files() {
                    return Err(
                        "DS-3: unrecorded same-name content differs; choose a new name".into(),
                    );
                }
                "in place"
            } else {
                "new workflow"
            };
            let draft = DraftKey {
                draft_location: self.origin.clone(),
                draft_root: live.parent().unwrap().display().to_string(),
                name: name.clone(),
            };
            // Validate byte/list/name/hygiene independently before adding observed prior.
            let mut review = Review::open(
                snapshot.clone(),
                &reread,
                list_revision.unwrap_or(snapshot.revision()),
                identity,
                None,
                draft,
                review_ref.clone(),
            )?;
            review.prior = prior;
            let reference = format!(
                "{}:{}:{}@{}",
                if in_place { "entry" } else { "draft" },
                self.origin,
                name,
                snapshot.revision()
            );
            entries.push(ReviewedEntry {
                review,
                live,
                slot,
                disposition: disposition.into(),
                reference,
                in_place,
            });
        }
        let mode = if !in_place {
            ReviewMode::Draft
        } else if entries.len() == 1 {
            ReviewMode::SingleInPlace
        } else {
            ReviewMode::MultiInPlace
        };
        let mut session = ReviewSession {
            root: self.root.clone(),
            bases: self.bases.clone(),
            act_log: storage::library_log(&self.root),
            origin: self.origin.clone(),
            source_root: self.source_root.clone(),
            review_ref,
            descriptor_id,
            mode,
            entries,
            descriptor: Value::Null,
            presentation: Value::Null,
            withdrawn: Cell::new(false),
        };
        session.descriptor = session.compose_descriptor();
        super::wr_validate(session.descriptor_kind(), &session.descriptor)?;
        session.presentation = session.compose_presentation();
        session.current()?;
        Ok(session)
    }
}
fn lineage_reaches(base: &WorkflowIdentity, target: &WorkflowIdentity) -> bool {
    base.same_slot(target)
        || base
            .derived_from
            .as_deref()
            .is_some_and(|p| lineage_reaches(p, target))
}
#[derive(Clone, Copy)]
enum ReviewMode {
    Draft,
    SingleInPlace,
    MultiInPlace,
}
struct ReviewedEntry {
    review: Review,
    live: PathBuf,
    slot: Vec<Value>,
    disposition: String,
    reference: String,
    in_place: bool,
}
pub(crate) struct ReviewSession {
    bases: std::sync::Arc<std::sync::Mutex<HashMap<String, WorkflowIdentity>>>,
    root: PathBuf,
    act_log: PathBuf,
    origin: String,
    source_root: String,
    review_ref: String,
    descriptor_id: String,
    mode: ReviewMode,
    entries: Vec<ReviewedEntry>,
    descriptor: Value,
    presentation: Value,
    withdrawn: Cell<bool>,
}
impl ReviewSession {
    fn descriptor_kind(&self) -> &'static str {
        if matches!(self.mode, ReviewMode::MultiInPlace) {
            "a15_multi_descriptor"
        } else {
            "a15_descriptor"
        }
    }
    pub(crate) fn withdraw(&self) {
        self.withdrawn.set(true);
    }
    pub(crate) fn current(&self) -> Result<CurrentReviewView<'_>, String> {
        if self.withdrawn.get() {
            return Err("review descriptor withdrawn".into());
        }
        let ledger = read_ledger(&self.root)?;
        for e in &self.entries {
            storage::check_path(&e.live)?;
            if Snapshot::capture(&e.live)?.files() != e.review.snapshot().files()
                || slot_lines(
                    &ledger,
                    &self.origin,
                    &self.source_root,
                    &e.review.identity.name,
                ) != e.slot
            {
                self.withdrawn.set(true);
                return Err("changed since review; review again".into());
            }
        }
        Ok(CurrentReviewView { session: self })
    }
    fn compose_descriptor(&self) -> Value {
        if matches!(self.mode, ReviewMode::MultiInPlace) {
            json!({"record_kind":"a15_multi_descriptor","descriptor_id":self.descriptor_id,"act_kind":"A15","wording":"register workflow revisions","disposition":"in place","library":{"origin":self.origin,"source_root":self.source_root},"entries":self.entries.iter().map(|e|json!({"subject":e.review.identity,"bound_content":content(e),"reviewed_entry":e.reference})).collect::<Vec<_>>(),"scope":self.source_root,"purpose":format!("make them available in the {} library",self.origin),"review_ref":self.review_ref})
        } else {
            let e = &self.entries[0];
            let mut d = e.review.descriptor();
            d["descriptor_id"] = json!(self.descriptor_id);
            d["disposition"] = json!(e.disposition);
            d
        }
    }
    fn compose_presentation(&self) -> Value {
        json!({"review_ref":self.review_ref,"descriptor_id":self.descriptor_id,"library":self.root,"origin":self.origin,"source_root":self.source_root,"entries":self.entries.iter().map(|e| {
            let comparison=|id:Option<&WorkflowIdentity>|->Value {match id {None=>Value::Null,Some(id)=> {
                let path=store_path(&self.root,id);
                match Snapshot::capture(&path){Ok(previous)=>json!({"identity":id,"files":previous.manifest(),"changes":diff(previous.files(),e.review.snapshot().files()),"limit":"comparison with stored bytes; old native origin not authenticated"}),Err(error)=>json!({"identity":id,"comparison":"unavailable","reason":error})}
            }}};
            json!({"identity":e.review.identity,"disposition":e.disposition,"message":format!("Registers {} in the {} library; earlier revisions are kept",e.disposition,self.origin),"content":content(e),"files":e.review.snapshot().manifest(),"workflow_text":e.review.snapshot().workflow_text(),"declaration":e.review.snapshot().declaration().map(|d|serde_json::to_value(d).unwrap_or(Value::Null)).unwrap_or_else(|error|json!({"unavailable":error})),"hygiene":e.review.snapshot().hygiene_findings(),"prior_revision":e.review.prior,"base":e.review.identity.derived_from,"lineage":e.review.identity.derived_from,"stale_base":e.review.prior.as_ref()!=e.review.identity.derived_from.as_deref(),"prior_comparison":comparison(e.review.prior.as_ref()),"base_comparison":comparison(e.review.identity.derived_from.as_deref()),"reviewed_reference":e.reference,"evidence_limits":["prior/base ledger facts are disclosed observations; no earlier native-act authentication"],"registration_notice":"Registering makes this revision available in the library. It is not a check that the workflow can run here."})
        }).collect::<Vec<_>>(),"same_name_elsewhere":{"standing":"not observed by this library owner; receiving catalog must supply collision inventory"},"compatibility":"not established; separate environment check"})
    }
    pub(crate) fn begin_hot_registration(
        self,
        receipt: HotA15Receipt,
    ) -> Result<HotRegistrationAttempt, String> {
        let matched = receipt.review_ref() == self.review_ref
            && receipt.descriptor_id() == self.descriptor_id
            && receipt.descriptor_kind() == self.descriptor_kind()
            && receipt.library_root() == self.root
            && receipt.act_log() == storage::library_log(&self.root)
            && receipt.ordered_bindings().len() == self.entries.len()
            && receipt
                .ordered_bindings()
                .iter()
                .zip(&self.entries)
                .all(|(a, e)| {
                    a.subject() == &e.review.identity
                        && a.content_method() == SNAPSHOT_METHOD
                        && a.content_value() == e.review.snapshot().revision()
                        && a.reviewed_id3() == e.reference
                        && a.reviewed_content_method() == SNAPSHOT_METHOD
                        && a.reviewed_content_value() == e.review.snapshot().revision()
                        && a.prior() == e.review.prior.as_ref()
                });
        if !matched {
            return Err("captured A15 does not bind this review/context; no registration; original act retained".into());
        }
        let progress = (0..self.entries.len()).map(|_| Progress::Fresh).collect();
        Ok(HotRegistrationAttempt {
            session: self,
            receipt,
            progress,
        })
    }
}
pub(crate) struct CurrentReviewView<'a> {
    session: &'a ReviewSession,
}
impl CurrentReviewView<'_> {
    pub(crate) fn revalidate(&self) -> Result<(), String> {
        self.session.current().map(|_| ())
    }
    pub(crate) fn descriptor(&self) -> &Value {
        &self.session.descriptor
    }
    pub(crate) fn descriptor_kind(&self) -> &'static str {
        self.session.descriptor_kind()
    }
    pub(crate) fn review_ref(&self) -> &str {
        &self.session.review_ref
    }
    pub(crate) fn descriptor_id(&self) -> &str {
        &self.session.descriptor_id
    }
    pub(crate) fn library_root(&self) -> &Path {
        &self.session.root
    }
    pub(crate) fn act_log(&self) -> &Path {
        &self.session.act_log
    }
    pub(crate) fn review_presentation(&self) -> &Value {
        &self.session.presentation
    }
    pub(crate) fn ordered_bindings(
        &self,
    ) -> impl ExactSizeIterator<Item = BorrowedReviewBinding<'_>> {
        self.session
            .entries
            .iter()
            .map(|entry| BorrowedReviewBinding { entry })
    }
}
pub(crate) struct BorrowedReviewBinding<'a> {
    entry: &'a ReviewedEntry,
}
impl BorrowedReviewBinding<'_> {
    pub(crate) fn subject(&self) -> &WorkflowIdentity {
        &self.entry.review.identity
    }
    pub(crate) fn content_method(&self) -> &str {
        SNAPSHOT_METHOD
    }
    pub(crate) fn content_value(&self) -> &str {
        self.entry.review.snapshot().revision()
    }
    pub(crate) fn reviewed_id3(&self) -> &str {
        &self.entry.reference
    }
    pub(crate) fn reviewed_content_method(&self) -> &str {
        SNAPSHOT_METHOD
    }
    pub(crate) fn reviewed_content_value(&self) -> &str {
        self.content_value()
    }
    pub(crate) fn prior(&self) -> Option<&WorkflowIdentity> {
        self.entry.review.prior.as_ref()
    }
}
fn content(e: &ReviewedEntry) -> Value {
    json!({"method":SNAPSHOT_METHOD,"value":e.review.snapshot().revision()})
}
fn diff(
    before: &std::collections::BTreeMap<String, Vec<u8>>,
    after: &std::collections::BTreeMap<String, Vec<u8>>,
) -> Vec<Value> {
    before.keys().chain(after.keys()).collect::<std::collections::BTreeSet<_>>().into_iter().filter(|p|before.get(*p)!=after.get(*p)).map(|p|json!({"path":p,"before":before.get(p).map(|b|crate::util::sha256_hex(b)),"after":after.get(p).map(|b|crate::util::sha256_hex(b))})).collect()
}
fn read_ledger(root: &Path) -> Result<Vec<Value>, String> {
    let path = root.join(".chirality/workflow-registry.jsonl");
    storage::check_path(&path)?;
    let bytes = match fs::read(path) {
        Ok(b) => b,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
        Err(e) => return Err(e.to_string()),
    };
    if !bytes.is_empty() && !bytes.ends_with(b"\n") {
        return Err("registration ledger has incomplete tail".into());
    }
    let mut rows = Vec::new();
    for line in bytes.split(|b| *b == b'\n').filter(|b| !b.is_empty()) {
        let value: Value = serde_json::from_slice(line).map_err(|e| e.to_string())?;
        super::wr_validate("library_entry", &value)?;
        if value["ledger_seq"].as_u64() != Some(rows.len() as u64 + 1) {
            return Err("registration ledger sequence ambiguous".into());
        }
        rows.push(value);
    }
    Ok(rows)
}
fn slot_lines(rows: &[Value], origin: &str, source: &str, name: &str) -> Vec<Value> {
    rows.iter()
        .filter(|v| {
            v["identity"]["origin"] == origin
                && v["identity"]["source_root"] == source
                && v["identity"]["name"] == name
        })
        .cloned()
        .collect()
}
fn latest(rows: &[Value]) -> Result<Option<WorkflowIdentity>, String> {
    rows.iter()
        .rev()
        .find(|v| v["outcome"] == "registered")
        .map(|v| serde_json::from_value(v["identity"].clone()).map_err(|e| e.to_string()))
        .transpose()
}
fn store_path(root: &Path, id: &WorkflowIdentity) -> PathBuf {
    root.join(".chirality/workflow-revisions")
        .join(&id.name)
        .join(storage::key(&id.revision))
        .join(&id.name)
}

enum Progress {
    Fresh,
    Intended(Value),
    Committed(RegisteredRevision, PublicationOutcome),
    Failed(String),
    Pending(String),
}
pub(crate) struct HotRegistrationAttempt {
    session: ReviewSession,
    receipt: HotA15Receipt,
    progress: Vec<Progress>,
}
#[derive(Clone, Debug)]
pub(crate) enum PublicationOutcome {
    Current,
    RepairPending(String),
}
#[derive(Clone, Debug)]
pub(crate) enum EntryOutcome {
    Registered {
        revision: RegisteredRevision,
        publication: PublicationOutcome,
    },
    NotCompleted {
        identity: WorkflowIdentity,
        reason: String,
    },
    Pending {
        identity: WorkflowIdentity,
        reason: String,
    },
}
impl HotRegistrationAttempt {
    pub(crate) fn advance(&mut self) -> Vec<EntryOutcome> {
        let locked = storage::lock(&self.session.root.join(".chirality/workflow-registry.lock"));
        if let Err(error) = locked {
            return self
                .session
                .entries
                .iter()
                .map(|e| EntryOutcome::Pending {
                    identity: e.review.identity.clone(),
                    reason: error.clone(),
                })
                .collect();
        }
        let _lock = locked.unwrap();
        for index in 0..self.progress.len() {
            if matches!(
                self.progress[index],
                Progress::Committed(..) | Progress::Failed(..)
            ) {
                continue;
            }
            if let Err(error) = self.advance_entry(index) {
                if !matches!(self.progress[index], Progress::Intended(_)) {
                    self.progress[index] = Progress::Pending(error);
                }
            }
        }
        self.progress
            .iter()
            .zip(&self.session.entries)
            .map(|(p, e)| match p {
                Progress::Committed(r, c) => EntryOutcome::Registered {
                    revision: r.clone(),
                    publication: c.clone(),
                },
                Progress::Failed(error) => EntryOutcome::NotCompleted {
                    identity: e.review.identity.clone(),
                    reason: error.clone(),
                },
                Progress::Pending(error) => EntryOutcome::Pending {
                    identity: e.review.identity.clone(),
                    reason: error.clone(),
                },
                _ => EntryOutcome::Pending {
                    identity: e.review.identity.clone(),
                    reason: "registration ledger durability uncertain; same hot attempt retained"
                        .into(),
                },
            })
            .collect()
    }
    fn advance_entry(&mut self, index: usize) -> Result<(), String> {
        let e = &self.session.entries[index];
        let root = &self.session.root;
        let rows = read_ledger(root)?;
        let intended = match &self.progress[index] {
            Progress::Intended(v) => Some(v.clone()),
            _ => None,
        };
        if let Some(line) = intended {
            let store = store_path(root, &e.review.identity);
            if line["outcome"] == "registered"
                && Snapshot::capture(&store)?.files() != e.review.snapshot().files()
            {
                return Err("intended commit store changed; no append".into());
            }
            if line["outcome"] == "registered" {
                sync_package(&store)?;
                storage::sync_dir(store.parent().ok_or("revision store has no parent")?)?;
            }
            if rows.iter().any(|v| v == &line) {
                storage::sync_publication(&root.join(".chirality/workflow-registry.jsonl"))?;
                return self.finish_line(index, line);
            }
            if line["ledger_seq"].as_u64() != Some(rows.len() as u64 + 1) {
                return Err(
                    "intended ledger line no longer appendable; no duplicate/rebase".into(),
                );
            }
            append_line(root, &line)?;
            return self.finish_line(index, line);
        }
        if slot_lines(
            &rows,
            &self.session.origin,
            &self.session.source_root,
            &e.review.identity.name,
        ) != e.slot
        {
            return self.fail_entry(index, "slot moved on; review again".into(), &rows);
        }
        if e.in_place
            && !Snapshot::capture(&e.live)
                .is_ok_and(|live| live.files() == e.review.snapshot().files())
        {
            return self.fail_entry(
                index,
                "in-place entry changed/unavailable after capture; review again (ME-5)".into(),
                &rows,
            );
        }
        let store = store_path(root, &e.review.identity);
        storage::check_path(&store)?;
        if store.exists() {
            if Snapshot::capture(&store)?.files() != e.review.snapshot().files() {
                return self.fail_entry(index, "store conflict".into(), &rows);
            }
        } else {
            storage::ensure_directory(store.parent().unwrap())?;
            if let Err(error) = publish_reserved_store(e.review.snapshot(), &store) {
                return self.fail_entry(
                    index,
                    format!("snapshot store publication failed: {error}"),
                    &rows,
                );
            }
        }
        if Snapshot::capture(&store)?.files() != e.review.snapshot().files() {
            return self.fail_entry(index, "copy verification failed".into(), &rows);
        }
        sync_package(&store)?;
        // G2/G3: the new store directory name must be durable before G4.
        storage::sync_dir(store.parent().ok_or("revision store has no parent")?)?;
        let sequence = e
            .slot
            .iter()
            .filter(|v| v["outcome"] == "registered")
            .count()
            + 1;
        let mut line = self.line(index, &rows, "registered");
        line["sequence"] = json!(sequence);
        line["disposition"] = json!(e.disposition);
        line["store_path"] = json!(store.strip_prefix(root).unwrap().to_string_lossy());
        super::wr_validate("library_entry", &line)?;
        self.progress[index] = Progress::Intended(line.clone());
        append_line(root, &line)?;
        self.finish_commit(index, line)
    }
    fn line(&self, index: usize, rows: &[Value], outcome: &str) -> Value {
        let e = &self.session.entries[index];
        let mut v = json!({"record_kind":"library_entry","ledger_seq":rows.len()+1,"outcome":outcome,"identity":e.review.identity,"act":{"record_id":self.receipt.record_id(),"capture_evidence":self.receipt.capture_id()},"prior_revision":e.review.prior,"written_at":crate::util::now_rfc3339(),"evidence_limits":["identity not verified; original hot native A15; no historical native-origin promotion"]});
        if e.in_place {
            v["reviewed_entry"] = json!({"entry":e.reference,"content":content(e)});
        } else {
            v["reviewed_draft"] = json!({"draft":e.review.draft,"content":content(e)});
        }
        v
    }
    fn fail_entry(&mut self, index: usize, reason: String, rows: &[Value]) -> Result<(), String> {
        let mut line = self.line(index, rows, "not completed");
        line["reason"] = json!(reason);
        super::wr_validate("library_entry", &line)?;
        self.progress[index] = Progress::Intended(line.clone());
        append_line(&self.session.root, &line)?;
        self.progress[index] = Progress::Failed(reason);
        Ok(())
    }
    fn finish_line(&mut self, index: usize, line: Value) -> Result<(), String> {
        if line["outcome"] == "not completed" {
            self.progress[index] =
                Progress::Failed(line["reason"].as_str().unwrap_or("not completed").into());
            return Ok(());
        }
        self.finish_commit(index, line)
    }
    fn finish_commit(&mut self, index: usize, _line: Value) -> Result<(), String> {
        let e = &self.session.entries[index];
        let store = store_path(&self.session.root, &e.review.identity);
        if Snapshot::capture(&store)?.files() != e.review.snapshot().files() {
            return Err("committed store no longer matches; registered value withheld".into());
        }
        let revision = RegisteredRevision {
            identity: e.review.identity.clone(),
            snapshot: e.review.snapshot().clone(),
            act_ref: self.receipt.record_id().into(),
        };
        let base_update = self
            .session
            .bases
            .lock()
            .map(|mut bases| {
                bases.insert(e.review.identity.name.clone(), e.review.identity.clone());
            })
            .map_err(|_| "App-kept base update pending".to_string());
        let mut publication = match self.publish_copy(index) {
            Ok(()) => PublicationOutcome::Current,
            Err(error) => PublicationOutcome::RepairPending(error),
        };
        if let Err(error) = base_update {
            publication = PublicationOutcome::RepairPending(error);
        }
        self.progress[index] = Progress::Committed(revision, publication);
        Ok(())
    }
    fn publish_copy(&self, index: usize) -> Result<(), String> {
        let e = &self.session.entries[index];
        if e.in_place {
            return Ok(());
        }
        let root = &self.session.root;
        let copy = root
            .join(".chirality/workflows")
            .join(&e.review.identity.name);
        storage::check_path(&copy)?;
        if copy.exists() && Snapshot::capture(&copy)?.files() == e.review.snapshot().files() {
            return Ok(());
        }
        let staging = root
            .join(".chirality/.workflow-staging")
            .join(crate::util::opaque_id("publish-")?);
        storage::ensure_directory(staging.parent().unwrap())?;
        e.review.snapshot().publish_new(&staging)?;
        sync_package(&staging)?;
        storage::ensure_directory(copy.parent().unwrap())?;
        if copy.exists() {
            let old = Snapshot::capture(&copy)?;
            let kept = root
                .join(".chirality/workflow-unrecorded")
                .join(&e.review.identity.name)
                .join(old.revision());
            storage::ensure_directory(kept.parent().unwrap())?;
            if kept.exists() {
                if Snapshot::capture(&kept)?.files() != old.files() {
                    return Err("kept-aside content conflict; published copy not replaced".into());
                }
                return Err("changed copy already kept aside; current copy retained for explicit reconciliation".into());
            }
            fs::rename(&copy, &kept).map_err(|e| e.to_string())?;
            storage::sync_dir(copy.parent().unwrap())?;
            storage::sync_dir(kept.parent().unwrap())?;
        }
        fs::rename(&staging, &copy).map_err(|e| e.to_string())?;
        storage::sync_dir(copy.parent().unwrap())
    }
}
#[cfg(test)]
thread_local! { static FAIL_LEDGER_SYNC: Cell<bool> = const { Cell::new(false) }; }
fn append_line(root: &Path, line: &Value) -> Result<(), String> {
    let path = root.join(".chirality/workflow-registry.jsonl");
    storage::check_path(&path)?;
    storage::ensure_directory(path.parent().unwrap())?;
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&path)
        .map_err(|e| e.to_string())?;
    let mut bytes = serde_json::to_vec(line).map_err(|e| e.to_string())?;
    bytes.push(b'\n');
    file.write_all(&bytes).map_err(|e| e.to_string())?;
    #[cfg(test)]
    if FAIL_LEDGER_SYNC.with(|fail| fail.replace(false)) {
        return Err("injected ledger sync uncertainty after write".into());
    }
    file.sync_all().map_err(|e| e.to_string())?;
    storage::sync_dir(path.parent().unwrap())
}
fn sync_package(path: &Path) -> Result<(), String> {
    for entry in fs::read_dir(path).map_err(|e| e.to_string())? {
        let p = entry.map_err(|e| e.to_string())?.path();
        storage::check_path(&p)?;
        if p.is_dir() {
            sync_package(&p)?;
        } else {
            fs::File::open(&p)
                .and_then(|f| f.sync_all())
                .map_err(|e| e.to_string())?;
        }
    }
    storage::sync_dir(path)
}

#[cfg(test)]
#[path = "workflow_library_tests.rs"]
mod tests;

// Only remove files/directories this attempt actually created, never an existing
// directory when exclusive reservation fails. Unknown external contents remain.
fn publish_reserved_store(snapshot: &Snapshot, store: &Path) -> Result<(), String> {
    fs::create_dir(store).map_err(|e| format!("exclusive store reservation: {e}"))?;
    let mut created = Vec::new();
    let result = (|| {
        for (relative, bytes) in snapshot.files() {
            let path = store.join(relative);
            storage::ensure_directory(path.parent().ok_or("store entry has no parent")?)?;
            let mut file = OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&path)
                .map_err(|e| e.to_string())?;
            created.push((path.clone(), bytes.clone()));
            file.write_all(bytes).map_err(|e| e.to_string())?;
            file.sync_all().map_err(|e| e.to_string())?;
        }
        Ok::<(), String>(())
    })();
    if result.is_err() {
        for (path, expected) in created.iter().rev() {
            if fs::read(path).is_ok_and(|actual| expected.starts_with(&actual)) {
                let _ = fs::remove_file(path);
                let mut parent = path.parent();
                while let Some(directory) = parent {
                    if !directory.starts_with(store) || fs::remove_dir(directory).is_err() {
                        break;
                    }
                    parent = directory.parent();
                }
            }
        }
        let _ = fs::remove_dir(store); // fails safely if an unknown entry remains
    }
    result
}
