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
    /// WR §3 "Draft bases": the App data folder, once Root attaches it.
    base_store: Option<PathBuf>,
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
            base_store: None,
        })
    }
    /// WR §3 "Draft bases | App data folder, keyed by draft key | The App only |
    /// App-kept pointer (R17-4); lost if the App data is lost — then the draft has
    /// no base (U-WR-12)". Root supplies its App user-data root; without it the
    /// pointer lives in process memory only and does not survive process loss.
    pub(crate) fn attach_app_kept_bases(&mut self, app_user_data: &Path) -> Result<(), String> {
        if !app_user_data.is_absolute() {
            return Err("App user-data root not established; App-kept bases not attached".into());
        }
        storage::check_path(app_user_data)?;
        self.base_store = Some(app_user_data.join(BASE_STORE));
        Ok(())
    }
    fn base_custody(&self) -> BaseCustody {
        BaseCustody {
            memory: self.bases.clone(),
            store: self.base_store.clone(),
            draft_root: self.root.join(".chirality/workflow-drafts"),
            origin: self.origin.clone(),
        }
    }
    /// Records only an actual closed source selection; draft-file tuples are not bases.
    pub(crate) fn record_base(&mut self, name: &str, selection: &Selection) -> Result<(), String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        self.base_custody().put(name, selection.identity(), false)
    }
    /// WR D-2/RB-1 listing observation: actual package bytes, not request identity.
    /// This digest is comparison data; it grants no review/capture/registration.
    pub(crate) fn listed_draft_revision(&self, name: &str) -> Result<String, String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        let path = self.root.join(".chirality/workflow-drafts").join(name);
        storage::check_path(&path)?;
        self.base_custody().drop_if_removed(name, &path)?;
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
            if !in_place {
                self.base_custody().drop_if_removed(&name, &live)?;
            }
            let snapshot = Snapshot::capture(&live)?;
            let reread = Snapshot::capture(&live)?;
            let slot = slot_lines(&ledger, &self.origin, &self.source_root, &name);
            let prior = latest(&slot)?;
            // The App-kept base is an observed claim: disclosed, frozen here and
            // rechecked at current() and under the ledger lock (G1). It is
            // freshness evidence, never proof that an earlier act occurred.
            let base_observed = if in_place {
                None
            } else {
                Some(self.base_custody().get(&name).map_err(|cause| {
                    format!("App-kept base for draft {name} not established: {cause}")
                })?)
            };
            let base = base_observed.as_ref().and_then(|o| o.base.clone());
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
                base: base_observed,
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
            custody: self.base_custody(),
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
    /// Frozen App-kept base observation (draft entries only).
    base: Option<BaseObservation>,
    disposition: String,
    reference: String,
    in_place: bool,
}
pub(crate) struct ReviewSession {
    custody: BaseCustody,
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
            if let Some(frozen) = &e.base {
                if let Err(cause) = self.base_unchanged(&e.review.identity.name, frozen) {
                    self.withdrawn.set(true);
                    return Err(format!("changed since review ({cause}); review again"));
                }
            }
        }
        Ok(CurrentReviewView { session: self })
    }
    /// Rereads the App-kept base and compares it with the frozen observation.
    fn base_unchanged(&self, name: &str, frozen: &BaseObservation) -> Result<(), String> {
        let now = self
            .custody
            .get(name)
            .map_err(|cause| format!("App-kept base not established: {cause}"))?;
        if &now != frozen {
            return Err("App-kept base changed since review".into());
        }
        Ok(())
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
            json!({"identity":e.review.identity,"disposition":e.disposition,"message":format!("Registers {} in the {} library; earlier revisions are kept",e.disposition,self.origin),"content":content(e),"files":e.review.snapshot().manifest(),"workflow_text":e.review.snapshot().workflow_text(),"declaration":e.review.snapshot().declaration().map(|d|serde_json::to_value(d).unwrap_or(Value::Null)).unwrap_or_else(|error|json!({"unavailable":error})),"hygiene":e.review.snapshot().hygiene_findings(),"prior_revision":e.review.prior,"base":e.review.identity.derived_from,"lineage":e.review.identity.derived_from,"stale_base":e.review.prior.as_ref()!=e.review.identity.derived_from.as_deref(),"prior_comparison":comparison(e.review.prior.as_ref()),"base_comparison":comparison(e.review.identity.derived_from.as_deref()),"reviewed_reference":e.reference,"evidence_limits":["prior/base ledger facts are disclosed observations; no earlier native-act authentication"],"ledger_observation":{"ledger":".chirality/workflow-registry.jsonl","slot_lines":e.slot.len(),"standing":"schema-readable registration ledger claim, frozen at review and rechecked under the ledger lock; equality is freshness evidence, not replay proof; the earlier native A15 is not authenticated and the earlier revision is not made selectable"},"base_observation":e.base.as_ref().map(|b|json!({"observed":b.source,"standing":"App-kept pointer (WR §3, R17-4), frozen at review and rechecked under the ledger lock; freshness evidence, not native-authenticated and not replay proof"})),"registration_notice":"Registering makes this revision available in the library. It is not a check that the workflow can run here."})
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
/// Reads the registration ledger. Each refusal names its exact cause (unreadable,
/// malformed or ambiguous) with the ledger path and line; nothing is skipped.
fn read_ledger(root: &Path) -> Result<Vec<Value>, String> {
    let path = root.join(".chirality/workflow-registry.jsonl");
    storage::check_path(&path)?;
    let shown = path.display();
    let bytes = match fs::read(&path) {
        Ok(b) => b,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(vec![]),
        Err(e) => return Err(format!("registration ledger unreadable: {shown}: {e}")),
    };
    if !bytes.is_empty() && !bytes.ends_with(b"\n") {
        return Err(format!(
            "registration ledger malformed: {shown}: incomplete final line (no newline) at line {}",
            bytes.split(|b| *b == b'\n').count()
        ));
    }
    let mut rows = Vec::new();
    for (index, line) in bytes.split(|b| *b == b'\n').enumerate() {
        let number = index + 1;
        if line.is_empty() {
            continue;
        }
        let value: Value = serde_json::from_slice(line).map_err(|e| {
            format!("registration ledger malformed: {shown}: line {number} is not JSON: {e}")
        })?;
        super::wr_validate("library_entry", &value)
            .map_err(|e| format!("registration ledger malformed: {shown}: line {number}: {e}"))?;
        if value["ledger_seq"].as_u64() != Some(rows.len() as u64 + 1) {
            return Err(format!(
                "registration ledger ambiguous: {shown}: line {number} has ledger_seq {}, expected {}",
                value["ledger_seq"],
                rows.len() + 1
            ));
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
/// The slot's latest registered revision. The slot's registered lines must form
/// one series (SP-1, G-4): sequence 1, 2, … in ledger order, each naming the
/// previous registered revision as its prior, no revision twice. Otherwise the
/// latest is ambiguous and the exact break is named.
fn latest(rows: &[Value]) -> Result<Option<WorkflowIdentity>, String> {
    let mut previous: Option<&Value> = None;
    let mut seen = std::collections::HashSet::new();
    for (k, v) in rows
        .iter()
        .filter(|v| v["outcome"] == "registered")
        .enumerate()
    {
        let at = format!(
            "registration ledger ambiguous for slot {}:{}: ledger_seq {}",
            v["identity"]["origin"].as_str().unwrap_or("?"),
            v["identity"]["name"].as_str().unwrap_or("?"),
            v["ledger_seq"]
        );
        if v["sequence"].as_u64() != Some(k as u64 + 1) {
            return Err(format!(
                "{at} has sequence {}, expected {}",
                v["sequence"],
                k + 1
            ));
        }
        let expected_prior = previous.map(|p| &p["identity"]).unwrap_or(&Value::Null);
        if &v["prior_revision"] != expected_prior {
            return Err(format!(
                "{at} names prior revision {}, but the slot's latest before it is {}",
                v["prior_revision"]["revision"], expected_prior["revision"]
            ));
        }
        if !seen.insert(v["identity"]["revision"].to_string()) {
            return Err(format!(
                "{at} registers revision {} a second time",
                v["identity"]["revision"]
            ));
        }
        previous = Some(v);
    }
    previous
        .map(|v| {
            serde_json::from_value(v["identity"].clone())
                .map_err(|e| format!("registration ledger malformed: latest identity: {e}"))
        })
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
        // G1 (under the ledger lock): the frozen App-kept base is still the one
        // observed. A changed base ends this attempt; an unreadable one keeps it
        // pending with its exact cause.
        if let Some(frozen) = &e.base {
            let name = e.review.identity.name.clone();
            let now = self.session.custody.get(&name).map_err(|cause| {
                format!("App-kept base not established at registration: {cause}")
            })?;
            if &now != frozen {
                return self.fail_entry(
                    index,
                    "App-kept base changed since review; review again".into(),
                    &rows,
                );
            }
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
        // G-6 / §5.1: "the App records the new revision as the draft's base".
        // An in-place entry has no draft, so no draft base is recorded for it.
        let base_update = if e.in_place {
            Ok(())
        } else {
            self.session
                .custody
                .put(&e.review.identity.name, &e.review.identity, true)
                .map_err(|error| format!("App-kept base update pending: {error}"))
        };
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

/// Where App-kept draft bases live under the App user-data root (WR §3 names the
/// App data folder; this sub-path is the implementation's, CONTRACT_ISSUES CI-21).
pub(crate) const BASE_STORE: &str = "runtime/wr/draft-bases";

/// WR §3 "Draft bases": written by the App only, keyed by draft key
/// {draft location, draft root, name}. Each pointer is one WR `draft_reference`
/// record (§8 "App-recorded base"; schema: `base` only when `base_recorded_by`
/// is *app*), validated before it is written and when it is read back. Without
/// an attached App data folder the pointer is held in process memory only.
#[derive(Clone)]
struct BaseCustody {
    memory: std::sync::Arc<std::sync::Mutex<HashMap<String, WorkflowIdentity>>>,
    store: Option<PathBuf>,
    draft_root: PathBuf,
    origin: String,
}
/// One observation of a draft's App-kept base: the base and where it was read.
#[derive(Clone, Debug, PartialEq)]
struct BaseObservation {
    base: Option<WorkflowIdentity>,
    source: Value,
}
impl BaseCustody {
    fn key(&self, name: &str) -> Value {
        json!({"draft_location":self.origin,"draft_root":self.draft_root.display().to_string(),"name":name})
    }
    fn file(&self, store: &Path, name: &str) -> PathBuf {
        store.join(format!(
            "{}.json",
            storage::key(&self.key(name).to_string())
        ))
    }
    fn get(&self, name: &str) -> Result<BaseObservation, String> {
        let Some(store) = &self.store else {
            let base = self
                .memory
                .lock()
                .map_err(|_| "App-kept base state unavailable")?
                .get(name)
                .cloned();
            return Ok(BaseObservation {
                base,
                source: json!({"source":"process memory only; App data folder not attached","limit":"lost with this process (WR §3, U-WR-12)"}),
            });
        };
        let path = self.file(store, name);
        storage::check_path(&path)?;
        let shown = path.display();
        let bytes = match fs::read(&path) {
            Ok(bytes) => bytes,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                return Ok(BaseObservation {
                    base: None,
                    source: json!({"source":"App data folder","record":"none for this draft key"}),
                })
            }
            Err(e) => return Err(format!("App-kept base record unreadable: {shown}: {e}")),
        };
        let record: Value = serde_json::from_slice(&bytes)
            .map_err(|e| format!("App-kept base record malformed: {shown}: not JSON: {e}"))?;
        super::wr_validate("draft_reference", &record)
            .map_err(|e| format!("App-kept base record malformed: {shown}: {e}"))?;
        if record["draft"] != self.key(name) {
            return Err(format!(
                "App-kept base record ambiguous: {shown} names draft key {}, not this draft",
                record["draft"]
            ));
        }
        let base = if record["base_recorded_by"] == "app" {
            let base: WorkflowIdentity = serde_json::from_value(record["base"].clone())
                .map_err(|e| format!("App-kept base record malformed: {shown}: base: {e}"))?;
            base.validate()
                .map_err(|e| format!("App-kept base record malformed: {shown}: base: {e}"))?;
            Some(base)
        } else {
            None
        };
        Ok(BaseObservation {
            base,
            source: json!({"source":"App data folder","record":record}),
        })
    }
    /// Records `base` for the draft. `registered`: the draft's content was just
    /// registered as `base` (§5.1 *registered, unchanged since*, when it still is).
    fn put(&self, name: &str, base: &WorkflowIdentity, registered: bool) -> Result<(), String> {
        let Some(store) = &self.store else {
            self.memory
                .lock()
                .map_err(|_| "App-kept base state unavailable")?
                .insert(name.into(), base.clone());
            return Ok(());
        };
        let draft = self.draft_root.join(name);
        storage::check_path(&draft)?;
        let mut record = json!({"record_kind":"draft_reference","draft":self.key(name),"base":base,"base_recorded_by":"app","observed_at":crate::util::now_rfc3339()});
        match Snapshot::capture(&draft) {
            Ok(snapshot) => {
                let findings: Vec<Value> = snapshot
                    .hygiene_findings()
                    .iter()
                    .filter_map(|f| finding(f))
                    .collect();
                record["state"] = json!(if !findings.is_empty() {
                    "not valid"
                } else if registered && snapshot.revision() == base.revision {
                    "registered, unchanged since"
                } else {
                    "draft"
                });
                record["content"] = json!({"method":SNAPSHOT_METHOD,"value":snapshot.revision()});
                record["file_count"] = json!(snapshot.files().len());
                record["findings"] = json!(findings);
            }
            Err(error) => {
                let findings: Vec<Value> = finding(&error).into_iter().collect();
                record["state"] = json!(if findings.is_empty() {
                    "draft"
                } else {
                    "not valid"
                });
                record["content"] = json!({ "not_established": error });
                record["findings"] = json!(findings);
            }
        }
        super::wr_validate("draft_reference", &record)?;
        storage::ensure_directory(store)?;
        storage::replace_json(&self.file(store, name), &record)
    }
    /// §5.1 "Folder removed → the App's base pointer is dropped", when the App
    /// observes the draft folder absent. The App does not watch the folder
    /// between its own observations (D3).
    fn drop_if_removed(&self, name: &str, draft: &Path) -> Result<(), String> {
        match fs::symlink_metadata(draft) {
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
            _ => return Ok(()),
        }
        let Some(store) = &self.store else {
            self.memory
                .lock()
                .map_err(|_| "App-kept base state unavailable")?
                .remove(name);
            return Ok(());
        };
        let path = self.file(store, name);
        storage::check_path(&path)?;
        match fs::remove_file(&path) {
            Ok(()) => storage::sync_dir(store),
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(()),
            Err(e) => Err(format!(
                "App-kept base pointer not dropped: {}: {e}",
                path.display()
            )),
        }
    }
}
/// A WR `finding` for a hygiene refusal or finding, by its HY code.
fn finding(detail: &str) -> Option<Value> {
    let code = [
        ("HY-1", "HY-1 no WORKFLOW.md"),
        ("HY-2", "HY-2 name"),
        ("HY-3", "HY-3 non-regular entry"),
        ("HY-4", "HY-4 operating-system file"),
        ("HY-5", "HY-5 size bound"),
        ("HY-7", "HY-7 not UTF-8"),
    ]
    .iter()
    .find(|(prefix, _)| detail.starts_with(prefix))?
    .1;
    Some(json!({"code":code,"detail":detail}))
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
