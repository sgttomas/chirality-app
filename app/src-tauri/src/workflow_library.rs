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
    /// Memory-only counterpart of a stored base record's *registered, unchanged
    /// since* state (§5.1), for drafts whose base was recorded at G-6.
    registered_bases: std::sync::Arc<std::sync::Mutex<std::collections::HashSet<String>>>,
    /// WR §3 "Draft bases": the App data folder, once Root attaches it.
    base_store: Option<PathBuf>,
    /// WR §4.8 RC-2: revisions whose registration (G-4) or re-confirmation (G-4R)
    /// result this App process holds. Filled only by this process's own hot
    /// commits; never rebuilt from the ledger or any record read from disk.
    held: Held,
    /// SQ-X X-2 outcomes for re-confirmation attempts found at open, with causes.
    reconciliation: Vec<String>,
}
type Held = std::sync::Arc<std::sync::Mutex<std::collections::HashSet<(String, String)>>>;
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
        let mut owner = Self {
            root,
            origin: origin.into(),
            source_root: source_root.into(),
            bases: std::sync::Arc::new(std::sync::Mutex::new(HashMap::new())),
            registered_bases: Default::default(),
            base_store: None,
            held: Default::default(),
            reconciliation: vec![],
        };
        // SQ-X X-1/X-2 at App start, per library: close re-confirmation attempts
        // a lost process left *stored*. Never completes one (RC-7).
        owner.reconciliation = reconcile_reconfirmations(&owner.root);
        Ok(owner)
    }
    /// What SQ-X X-2 did for re-confirmation attempts at open (WR §4.8 RC-7).
    pub(crate) fn reconciliation(&self) -> &[String] {
        &self.reconciliation
    }
    fn is_held(&self, identity: &WorkflowIdentity) -> bool {
        is_held(&self.held, identity)
    }
    /// WR PR-2: the slot's latest registered revision as the ledger reads now. A
    /// ledger reading never selects or authenticates; the caller still needs a
    /// revision this process holds.
    pub(crate) fn latest_registered(&self, name: &str) -> Result<Option<WorkflowIdentity>, String> {
        let rows = read_ledger(&self.root)?;
        latest(&slot_lines(&rows, &self.origin, &self.source_root, name))
    }
    /// WR PR-3: whether this library has a draft of that name (a draft is no identity).
    pub(crate) fn has_draft(&self, name: &str) -> bool {
        super::valid_name(name) && self.root.join(".chirality/workflow-drafts").join(name).is_dir()
    }
    /// The published copy, then the immutable revision store, of a revision; the
    /// caller verifies whichever it uses against the revision.
    pub(crate) fn revision_copies(&self, identity: &WorkflowIdentity) -> [PathBuf; 2] {
        [self.root.join(".chirality/workflows").join(&identity.name), store_path(&self.root, identity)]
    }
    /// WR §4.6 LS-1 "as read": the registered line's A15 record found with the
    /// same bound content, and store bytes that recompute to the revision. A cold
    /// read of App-kept files (V13 R2-N2): it gates the DS-8 offer only and is
    /// never a trust signal or a selection.
    /// Returns the store snapshot it verified (V15 F3: copy exactly these bytes).
    fn standing_as_read(&self, line: &Value, k: &WorkflowIdentity) -> Result<Snapshot, String> {
        act_record_found(&self.root, line, k).map_err(|fault| fault.to_string())?;
        let store = store_path(&self.root, k);
        storage::check_path(&store)?;
        let read = Snapshot::capture(&store)
            .map_err(|e| format!("revision store {} not readable: {e}", store.display()))?;
        if read.revision() != k.revision {
            return Err(format!(
                "revision store {} does not recompute to the revision",
                store.display()
            ));
        }
        Ok(read)
    }
    /// V15 F5 (WR §4.6 LS-1 note, §5.4): the library's registered revisions as
    /// read, for listing and per-row Refine. LS-1 is not checked here; a row is
    /// "selectable in this App session" only when this process holds its result.
    pub(crate) fn registered_listing(&self) -> Value {
        let rows = match read_ledger(&self.root) {
            Ok(rows) => rows,
            Err(cause) => return json!({"limit":cause}),
        };
        json!(rows
            .iter()
            .filter(|v| v["outcome"] == "registered"
                && v["identity"]["origin"] == self.origin.as_str()
                && v["identity"]["source_root"] == self.source_root.as_str())
            .map(|v| {
                let held = serde_json::from_value::<WorkflowIdentity>(v["identity"].clone())
                    .is_ok_and(|k| self.is_held(&k));
                json!({"name":v["identity"]["name"],"sequence":v["sequence"],"revision":v["identity"]["revision"],
                    "registeredAt":v["written_at"],"disposition":v["disposition"],
                    "label":if held {"registered — selectable in this App session"} else {"registered — re-confirm to use in this App session"},
                    "offered":"Refine (RF-1); Review a draft with its bytes (DS-8)"})
            })
            .collect::<Vec<_>>())
    }
    /// WR §4.6 RF-1: Refine an LS-1 revision from the revision store, with no
    /// selection. The store bytes are recomputed; the App records the revision,
    /// read from the ledger now, as the new draft's base (shown and frozen at
    /// review). Covers revisions registered in place. D-1: never overwrites.
    pub(crate) fn refine_from_store(&self, name: &str, revision: &str) -> Result<Value, String> {
        if !super::valid_name(name) {
            return Err("invalid workflow name".into());
        }
        let rows = read_ledger(&self.root)?;
        let slot = slot_lines(&rows, &self.origin, &self.source_root, name);
        latest(&slot)?;
        let line = slot
            .iter()
            .find(|v| v["outcome"] == "registered" && v["identity"]["revision"] == revision)
            .ok_or_else(|| format!("revision {revision} is not registered in this slot"))?;
        let k: WorkflowIdentity = serde_json::from_value(line["identity"].clone())
            .map_err(|e| format!("registered identity not readable: {e}"))?;
        // V15 F3: copy exactly the bytes standing_as_read verified.
        let store = self.standing_as_read(line, &k).map_err(|cause| {
            format!("LS-4 registration record incomplete: {cause}; no draft made (RF-1)")
        })?;
        let target = self.root.join(".chirality/workflow-drafts").join(name);
        storage::check_path(&target)?;
        if fs::symlink_metadata(&target).is_ok() {
            return Err(format!(
                "a draft named {name} already exists; rename or remove the draft (D-1)"
            ));
        }
        let parent = target.parent().ok_or("draft has no parent")?;
        storage::ensure_directory(parent)?;
        // Exclusive create; a part-way failure removes only what it wrote.
        publish_reserved_store(&store, &target)
            .map_err(|e| format!("draft copy failed ({e}); nothing kept; refine again"))?;
        // Every later failure removes the App's own copy (exact-bytes check), so
        // no draft is left that can only be DS-3 (V11 J5-2; V15 F3).
        let published = sync_package(&target).and_then(|()| storage::sync_dir(parent));
        let recorded = published.and_then(|()| {
            self.base_custody()
                .put(name, &k, false)
                .map_err(|e| format!("App-kept base not recorded ({e})"))
        });
        if let Err(error) = recorded {
            return Err(match self.discard_unbased_copy(name, &store) {
                Ok(()) => format!("{error}; the draft copy was removed, nothing kept; refine again"),
                Err(kept) => format!("Draft copied but not completed ({error}); the copy was not removed ({kept}); remove {} and refine again", target.display()),
            });
        }
        Ok(
            json!({"state":"draft made from the revision store (RF-1); no selection made","name":name,
            "base":k,"sequence":line["sequence"],"standing":"LS-1 registered, as read (registered earlier; not verified in this session)",
            "next":"left unchanged it reviews as re-confirmation (DS-8) or DS-4; changed, as a new revision (DS-2)"}),
        )
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
            registered_memory: self.registered_bases.clone(),
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
    /// V11 J5-2: undo the App's own just-written draft copy when its base could
    /// not be recorded, so no draft is left that can only be DS-3 and that D-1
    /// forbids the App to overwrite. Only exactly the copied bytes are removed;
    /// anything else in the folder keeps the whole draft.
    pub(crate) fn discard_unbased_copy(&self, name: &str, copied: &Snapshot) -> Result<(), String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        let draft = self.root.join(".chirality/workflow-drafts").join(name);
        storage::check_path(&draft)?;
        if Snapshot::capture(&draft)?.files() != copied.files() {
            return Err("the draft folder differs from the App's copy; kept".into());
        }
        let mut directories = std::collections::BTreeSet::new();
        for relative in copied.files().keys() {
            let path = draft.join(relative);
            fs::remove_file(&path).map_err(|e| format!("{}: {e}", path.display()))?;
            let mut parent = path.parent();
            while let Some(directory) = parent.filter(|d| d.starts_with(&draft) && *d != draft) {
                directories.insert(directory.to_path_buf());
                parent = directory.parent();
            }
        }
        for directory in directories.iter().rev() {
            fs::remove_dir(directory).map_err(|e| format!("{}: {e}", directory.display()))?;
        }
        fs::remove_dir(&draft).map_err(|e| format!("{}: {e}", draft.display()))?;
        storage::sync_dir(draft.parent().ok_or("draft has no parent")?)
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
    /// §5.1 "Folder removed → the App's base pointer is dropped", for a review
    /// whose listed content identity the caller already holds (RB-1).
    pub(crate) fn drop_removed_draft_base(&self, name: &str) -> Result<(), String> {
        if !super::valid_name(name) {
            return Err("invalid draft name".into());
        }
        let path = self.root.join(".chirality/workflow-drafts").join(name);
        storage::check_path(&path)?;
        self.base_custody().drop_if_removed(name, &path)
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
            // HY-3/HY-5 from metadata before any byte is read (U-WR-7); the
            // capture itself also enforces the bound while reading.
            drafts::prescan(&live).map_err(|e| {
                if e.starts_with("HY-") { format!("DS-5: {e}") } else { e }
            })?;
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
            let mut identity =
                snapshot.identity(&self.origin, &self.source_root, &name, base.clone())?;
            let published = self.root.join(".chirality/workflows").join(&name);
            if in_place && prior.is_some() {
                return Err(
                    "entry has registration history; review its disclosed standing separately"
                        .into(),
                );
            }
            // SP-4a: DS-5 and DS-6 first, then SP-3 (DS-3), then identical
            // content (DS-4 or DS-8), and otherwise DS-2.
            if !in_place && prior.is_some() {
                let findings = snapshot.hygiene_findings();
                if !findings.is_empty() {
                    return Err(format!("DS-5: {}", findings.join("; ")));
                }
                if reread.revision() != snapshot.revision()
                    || list_revision.is_some_and(|l| l != snapshot.revision())
                {
                    return Err("DS-6: draft changed while read; review again".into());
                }
            }
            let mut reconfirm = None;
            let disposition = if in_place {
                "in place"
            } else if let Some(prior) = &prior {
                lineage_reaches(base.as_ref(), prior, &slot)?;
                if let Some(line) = slot.iter().find(|e| {
                    e["outcome"] == "registered" && e["identity"]["revision"] == snapshot.revision()
                }) {
                    let k: WorkflowIdentity = serde_json::from_value(line["identity"].clone())
                        .map_err(|e| format!("registered identity not readable: {e}"))?;
                    let sequence = line["sequence"].as_u64().unwrap_or(0);
                    if self.is_held(&k) {
                        return Err(format!(
                            "DS-4: identical to revision {sequence}; select it instead"
                        ));
                    }
                    if let Err(cause) = self.standing_as_read(line, &k) {
                        return Err(format!(
                            "DS-4: identical to revision {sequence}, whose standing is LS-4 registration record incomplete: {cause}. Restore the record or bytes (WR §5.3), then review again"
                        ));
                    }
                    reconfirm = Some(Reconfirm::from_line(line)?);
                    // RC-3: the subject is ‹k›'s tuple exactly as its line records it.
                    identity = k;
                    "re-confirmation"
                } else {
                    "new revision"
                }
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
                reconfirm,
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
            held: self.held.clone(),
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
/// SP-3: a draft is made from the slot when its App-kept base "is a revision of
/// that slot", or the base's derived-from lineage reaches one. The first tuple in
/// that lineage naming this slot must be a revision the ledger registered in it;
/// otherwise the lineage is not established (DS-3), shown as ID-4's "lineage
/// incomplete at ‹tuple›". The App-kept record is a claim, not proof (CI-21).
fn lineage_reaches(
    base: Option<&WorkflowIdentity>,
    target: &WorkflowIdentity,
    slot: &[Value],
) -> Result<(), String> {
    let mut node = base;
    while let Some(n) = node {
        if n.same_slot(target) {
            let registered = slot.iter().any(|v| {
                v["outcome"] == "registered"
                    && v["identity"]["revision"] == n.revision.as_str()
                    && v["identity"]["revision_method"] == n.revision_method.as_str()
            });
            if registered {
                return Ok(());
            }
            return Err(format!(
                "DS-3: name taken; App-kept base lineage incomplete at {}:{}@{} (not a revision registered in this slot; WR SP-3, ID-4)",
                n.origin, n.name, n.revision
            ));
        }
        node = n.derived_from.as_deref();
    }
    Err("DS-3: name taken; draft has no App-kept base in this slot".into())
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
    /// DS-8 only: the registered line ‹k› this review re-confirms (WR §4.8).
    reconfirm: Option<Reconfirm>,
    disposition: String,
    reference: String,
    in_place: bool,
}
/// WR §4.8 RC-3/RC-4: ‹k›'s registered line, read at review and frozen. Its
/// facts are disclosed ("registered earlier; not verified in this session").
#[derive(Clone)]
struct Reconfirm {
    line: Value,
    ledger_seq: u64,
    sequence: u64,
    /// ‹k›'s own prior revision, as its registered line records it (RC-4).
    prior: Option<WorkflowIdentity>,
}
impl Reconfirm {
    fn from_line(line: &Value) -> Result<Self, String> {
        Ok(Self {
            line: line.clone(),
            ledger_seq: line["ledger_seq"]
                .as_u64()
                .ok_or("registered line ledger_seq not readable")?,
            sequence: line["sequence"]
                .as_u64()
                .ok_or("registered line sequence not readable")?,
            prior: serde_json::from_value(line["prior_revision"].clone())
                .map_err(|e| format!("registered line prior not readable: {e}"))?,
        })
    }
    fn reconfirms(&self) -> Value {
        json!({"identity":self.line["identity"],"ledger_seq":self.ledger_seq,"sequence":self.sequence})
    }
}
/// The prior the act binds: ‹k›'s own for DS-8 (RC-4), else the slot's latest
/// at review (SP-6).
fn act_prior(e: &ReviewedEntry) -> Option<&WorkflowIdentity> {
    match &e.reconfirm {
        Some(r) => r.prior.as_ref(),
        None => e.review.prior.as_ref(),
    }
}
pub(crate) struct ReviewSession {
    custody: BaseCustody,
    held: Held,
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
    /// The draft this review reads, for a draft review (not an in-place entry).
    pub(crate) fn draft_name(&self) -> Option<&str> {
        match self.mode {
            ReviewMode::Draft => self.entries.first().map(|e| e.review.identity.name.as_str()),
            _ => None,
        }
    }
    /// The library root this review belongs to.
    pub(crate) fn library_root(&self) -> &Path {
        &self.root
    }
    pub(crate) fn current(&self) -> Result<CurrentReviewView<'_>, String> {
        if self.withdrawn.get() {
            return Err("review descriptor withdrawn".into());
        }
        let ledger = read_ledger(&self.root)?;
        for e in &self.entries {
            storage::check_path(&e.live)?;
            // RB-3 (b) / RC-5: the slot's latest *registered* revision is still the
            // one at review (`freshness.slot_latest`); re-confirmed and not
            // completed lines never change it (RC-9; F14).
            if Snapshot::capture(&e.live)?.files() != e.review.snapshot().files()
                || slot_latest_now(&ledger, &self.origin, &self.source_root, e)? != e.review.prior
            {
                self.withdrawn.set(true);
                return Err("changed since review; review again".into());
            }
            if let Some(r) = &e.reconfirm {
                if let Err(cause) = self.reconfirm_current(&ledger, e, r) {
                    self.withdrawn.set(true);
                    return Err(format!("changed since review ({cause}); review again"));
                }
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
    /// RC-5 (c) and (d): the registered line ‹ledger_seq› still reads with ‹k›'s
    /// tuple, ‹k› is still LS-1 as read, and ‹k› has not become selectable here.
    fn reconfirm_current(
        &self,
        ledger: &[Value],
        e: &ReviewedEntry,
        r: &Reconfirm,
    ) -> Result<(), String> {
        let k = &e.review.identity;
        if ledger.get(r.ledger_seq as usize - 1) != Some(&r.line) {
            return Err(format!(
                "registered line {} no longer reads as reviewed",
                r.ledger_seq
            ));
        }
        act_record_found(&self.root, &r.line, k).map_err(|c| {
            format!(
                "revision {} registration record incomplete: {c}",
                r.sequence
            )
        })?;
        let store = Snapshot::capture(&store_path(&self.root, k))
            .map_err(|c| format!("revision {} store no longer recomputes: {c}", r.sequence))?;
        if store.revision() != k.revision {
            return Err(format!(
                "revision {} store no longer recomputes",
                r.sequence
            ));
        }
        if is_held(&self.held, k) {
            return Err(format!(
                "revision {} already selectable in this App session",
                r.sequence
            ));
        }
        Ok(())
    }
    /// RC-10: what a DS-8 review shows beside RB-2.
    fn reconfirmation_view(&self, e: &ReviewedEntry) -> Value {
        let Some(r) = &e.reconfirm else {
            return Value::Null;
        };
        let k = &e.review.identity;
        json!({"revision":k.revision,"sequence":r.sequence,"reconfirms":r.reconfirms(),
            "standing":"LS-1 registered, as read (registered earlier; not verified in this session)",
            "registered_earlier":{"written_at":r.line["written_at"],"act":r.line["act"],"label":"registered earlier; not verified in this session"},
            "slot_latest":if e.review.prior.as_ref()!=Some(k){json!(e.review.prior)}else{Value::Null},
            "statement":format!("Re-confirm revision {} of {}:{} for use in this App session. This registers no new revision.",r.sequence,k.origin,k.name),
            "limit":"LS-1 as read is a cold read of App-kept files; it only gates this offer. Authority comes from the new A15; the earlier act is not replayed (RC-2, RC-8)"})
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
            if let Some(r) = &e.reconfirm {
                // RC-4: the re-confirmation form. Subject ‹k›; relations.prior
                // and derived_from are ‹k›'s own; freshness.slot_latest stays the
                // slot's latest at review (RC-5).
                d["wording"] = json!("re-confirm workflow revision for use");
                d["purpose"] = json!(format!(
                    "make it available again in this App session from the {} library",
                    self.origin
                ));
                d["relations"]["prior_revision"] = json!(r.prior);
                d["relations"]["derived_from"] = json!(e.review.identity.derived_from);
                d["reconfirms"] = r.reconfirms();
            }
            d
        }
    }
    fn compose_presentation(&self) -> Value {
        json!({"review_ref":self.review_ref,"descriptor_id":self.descriptor_id,"library":self.root,"origin":self.origin,"source_root":self.source_root,"entries":self.entries.iter().map(|e| {
            let comparison=|id:Option<&WorkflowIdentity>|->Value {match id {None=>Value::Null,Some(id)=> {
                let path=store_path(&self.root,id);
                match Snapshot::capture(&path){Ok(previous)=>json!({"identity":id,"files":previous.manifest(),"changes":diff(previous.files(),e.review.snapshot().files()),"limit":"comparison with stored bytes; old native origin not authenticated"}),Err(error)=>json!({"identity":id,"comparison":"unavailable","reason":error})}
            }}};
            let app_base=e.base.as_ref().and_then(|b|b.base.clone());
            json!({"identity":e.review.identity,"disposition":e.disposition,"message":entry_message(e,&self.origin),"reconfirmation":self.reconfirmation_view(e),"content":content(e),"files":e.review.snapshot().manifest(),"workflow_text":e.review.snapshot().workflow_text(),"declaration":e.review.snapshot().declaration().map(|d|serde_json::to_value(d).unwrap_or(Value::Null)).unwrap_or_else(|error|json!({"unavailable":error})),"hygiene":e.review.snapshot().hygiene_findings(),"prior_revision":e.review.prior,"base":app_base,"lineage":e.review.identity.derived_from,"stale_base":e.review.prior.as_ref()!=app_base.as_ref(),"prior_comparison":comparison(e.review.prior.as_ref()),"base_comparison":comparison(app_base.as_ref()),"reviewed_reference":e.reference,"evidence_limits":["prior/base ledger facts are disclosed observations; no earlier native-act authentication"],"ledger_observation":{"ledger":".chirality/workflow-registry.jsonl","slot_lines":e.slot.len(),"standing":"schema-readable registration ledger claim, frozen at review and rechecked under the ledger lock; equality is freshness evidence, not replay proof; the earlier native A15 is not authenticated and the earlier revision is not made selectable"},"base_observation":e.base.as_ref().map(|b|json!({"observed":b.source,"standing":"App-kept pointer (WR §3, R17-4), frozen at review and rechecked under the ledger lock; freshness evidence, not native-authenticated and not replay proof"})),"registration_notice":if e.reconfirm.is_some(){format!("Re-confirming makes revision {} available in this App session. It registers no new revision, and it is not a check that the workflow can run here.",e.reconfirm.as_ref().map_or(0,|r|r.sequence))}else{"Registering makes this revision available in the library. It is not a check that the workflow can run here.".into()}})
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
                        && a.prior() == act_prior(e)
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
    /// The act's prior: ‹k›'s own for a re-confirmation (RC-4).
    pub(crate) fn prior(&self) -> Option<&WorkflowIdentity> {
        act_prior(self.entry)
    }
}
/// The review's message (SP-4 substance).
fn entry_message(e: &ReviewedEntry, origin: &str) -> String {
    match &e.reconfirm {
        Some(r) => format!("Identical to revision {}, registered earlier (not verified in this session). Re-confirm revision {} for use in this App session; no new revision is registered", r.sequence, r.sequence),
        None => format!("Registers {} in the {} library; earlier revisions are kept", e.disposition, origin),
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
pub(super) fn read_ledger(root: &Path) -> Result<Vec<Value>, String> {
    let path = root.join(".chirality/workflow-registry.jsonl");
    storage::check_path(&path)?;
    let shown = path.display();
    let bytes = match super::read_regular_file(&path) {
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
    check_reconfirmation_lines(&rows, &shown.to_string())?;
    Ok(rows)
}
/// WR §4.8 RC-9 reader checks. A line with disposition *re-confirmation* names
/// (in `reconfirms`) an earlier *registered* line of the same slot. A
/// *re-confirmed* line also repeats that line's identity, sequence, prior and
/// store path, its reviewed draft content is the revision, and the A15 it cites
/// is cited by no other ledger line (RB-8). A breach makes the ledger ambiguous
/// at that line.
fn check_reconfirmation_lines(rows: &[Value], shown: &str) -> Result<(), String> {
    let mut citations: HashMap<&Value, usize> = HashMap::new();
    for v in rows {
        *citations.entry(&v["act"]["record_id"]).or_default() += 1;
    }
    for v in rows
        .iter()
        .filter(|v| v["disposition"] == "re-confirmation")
    {
        let at = format!(
            "registration ledger ambiguous: {shown}: line {} ({})",
            v["ledger_seq"],
            v["outcome"].as_str().unwrap_or("?")
        );
        let cited = v["reconfirms"]["ledger_seq"].as_u64().unwrap_or(0);
        let own = v["ledger_seq"].as_u64().unwrap_or(0);
        let registered = (cited >= 1 && cited < own)
            .then(|| &rows[cited as usize - 1])
            .filter(|r| r["outcome"] == "registered")
            .ok_or_else(|| {
                format!("{at} re-confirms line {cited}, which is not an earlier registered line")
            })?;
        let same_slot = ["origin", "source_root", "name"]
            .iter()
            .all(|f| v["identity"][f] == registered["identity"][f]);
        if !same_slot
            || v["reconfirms"]["identity"] != registered["identity"]
            || v["reconfirms"]["sequence"] != registered["sequence"]
        {
            return Err(format!(
                "{at} names line {cited} with another slot, tuple or sequence"
            ));
        }
        if v["outcome"] == "re-confirmed" {
            for field in ["identity", "sequence", "prior_revision", "store_path"] {
                if v[field] != registered[field] {
                    return Err(format!("{at}: {field} differs from line {cited}"));
                }
            }
            if v["reviewed_draft"]["content"]
                != json!({"method":registered["identity"]["revision_method"],"value":registered["identity"]["revision"]})
            {
                return Err(format!(
                    "{at}: reviewed content is not the re-confirmed revision"
                ));
            }
            if citations.get(&v["act"]["record_id"]).copied() != Some(1) {
                return Err(format!(
                    "{at}: its A15 {} is cited by another ledger line",
                    v["act"]["record_id"]
                ));
            }
        }
    }
    Ok(())
}
/// RB-3 (b), RC-5, G-1, G-1R: the slot's latest *registered* revision now.
fn slot_latest_now(
    rows: &[Value],
    origin: &str,
    source: &str,
    e: &ReviewedEntry,
) -> Result<Option<WorkflowIdentity>, String> {
    latest(&slot_lines(rows, origin, source, &e.review.identity.name))
}
fn is_held(held: &Held, identity: &WorkflowIdentity) -> bool {
    held.lock()
        .map(|h| h.contains(&(identity.name.clone(), identity.revision.clone())))
        .unwrap_or(false)
}
/// Why LS-1's act condition does not hold as read (V15 F4). WR LS-4 names
/// "A15 record missing or bound to other content"; an act log that cannot be
/// read completely is a read limit, not a finding about the record.
enum ActRecordFault {
    /// The act log could not be read completely (a line, a gap, an I/O error).
    LogUnreadable(String),
    /// The record is missing, or bound to other content (LS-4).
    Incomplete(String),
}
impl std::fmt::Display for ActRecordFault {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::LogUnreadable(cause) | Self::Incomplete(cause) => f.write_str(cause),
        }
    }
}
/// LS-1's act condition as read: the line's A15 record is in the library act
/// log with the same bound content. A cold read; it never authenticates the act.
fn act_record_found(root: &Path, line: &Value, k: &WorkflowIdentity) -> Result<(), ActRecordFault> {
    let log = storage::library_log(root);
    let (acts, limits) = crate::records::read_log(&log);
    if !limits.is_empty() {
        return Err(ActRecordFault::LogUnreadable(format!(
            "act log not completely readable: {}",
            limits.join("; ")
        )));
    }
    let record = &line["act"]["record_id"];
    let act = acts
        .iter()
        .find(|a| &a["recordId"] == record)
        .ok_or_else(|| {
            ActRecordFault::Incomplete(format!(
                "A15 record {record} not found in {}",
                log.display()
            ))
        })?;
    let bound = json!({"method":k.revision_method,"value":k.revision});
    if act["kind"] != "human_act"
        || act["body"]["actKind"] != "A15"
        || !act["body"]["boundContent"]
            .as_array()
            .is_some_and(|b| b.contains(&bound))
    {
        return Err(ActRecordFault::Incomplete(format!(
            "A15 record {record} is bound to other content"
        )));
    }
    Ok(())
}
/// V15 F1: before any append of a line with disposition *re-confirmation*, run
/// the App's own RC-9 reader over the ledger as it would then read. A line the
/// reader would refuse is never appended (it would make the whole library
/// ledger unreadable); the caller keeps the attempt pending with this cause.
fn rc9_guard(root: &Path, rows: &[Value], line: &Value) -> Result<(), String> {
    if line["disposition"] != "re-confirmation" {
        return Ok(());
    }
    let mut after = rows.to_vec();
    after.push(line.clone());
    let path = root.join(".chirality/workflow-registry.jsonl");
    check_reconfirmation_lines(&after, &path.display().to_string()).map_err(|cause| {
        format!(
            "re-confirmation line not appended: the App's RC-9 reader would refuse it ({cause})"
        )
    })
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
    /// G-4R durable: ‹k› selectable in this process (RC-2). The outcome is the
    /// App-kept base update (G-6R), as for a registration.
    ReConfirmed(RegisteredRevision, PublicationOutcome),
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
    /// WR §4.8: revision ‹k› re-confirmed by a new A15; no new revision. The
    /// value cites the new act; `publication` reports the G-6R base update only.
    ReConfirmed {
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
                Progress::Committed(..) | Progress::ReConfirmed(..) | Progress::Failed(..)
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
                Progress::ReConfirmed(r, c) => EntryOutcome::ReConfirmed {
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
            let commit = line["outcome"] == "registered" || line["outcome"] == "re-confirmed";
            if commit && Snapshot::capture(&store)?.files() != e.review.snapshot().files() {
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
            // V15-R1 R1-1 (RC-7, RB-8): another process's X-2 may have closed this
            // attempt with its own line meanwhile; end with that line, so the
            // outcome is definite rather than "durability uncertain" for ever.
            if self.end_if_a15_has_line(index, &rows)? {
                return Ok(());
            }
            let root = &self.session.root;
            if line["ledger_seq"].as_u64() != Some(rows.len() as u64 + 1) {
                return Err(
                    "intended ledger line no longer appendable; no duplicate/rebase".into(),
                );
            }
            rc9_guard(root, &rows, &line)?;
            append_line(root, &line)?;
            return self.finish_line(index, line);
        }
        if self.end_if_a15_has_line(index, &rows)? {
            return Ok(());
        }
        let e = &self.session.entries[index];
        // G-1 / G-1R (F14): compare the slot's latest *registered* revision, so
        // re-confirmed and not completed lines never fail a concurrent attempt.
        if slot_latest_now(&rows, &self.session.origin, &self.session.source_root, e)?
            != e.review.prior
        {
            return self.fail_entry(index, "slot moved on; review again".into(), &rows);
        }
        if let Some(r) = e.reconfirm.clone() {
            return self.advance_reconfirmation(index, r, &rows);
        }
        if self.base_changed(index, &rows)? {
            return Ok(());
        }
        let e = &self.session.entries[index];
        let root = &self.session.root;
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
    /// G1 (under the ledger lock): the frozen App-kept base is still the one
    /// observed. A changed base ends this attempt (Ok(true), line written); an
    /// unreadable one keeps it pending with its exact cause (Err).
    fn base_changed(&mut self, index: usize, rows: &[Value]) -> Result<bool, String> {
        let e = &self.session.entries[index];
        let Some(frozen) = &e.base else {
            return Ok(false);
        };
        let now = self
            .session
            .custody
            .get(&e.review.identity.name)
            .map_err(|cause| format!("App-kept base not established at registration: {cause}"))?;
        if &now == frozen {
            return Ok(false);
        }
        self.fail_entry(
            index,
            "App-kept base changed since review; review again".into(),
            rows,
        )?;
        Ok(true)
    }
    /// V15 F1 (RC-7, RB-8): one act never has two ledger lines. If the ledger
    /// already cites this re-confirmation attempt's A15 (for example X-2 of
    /// another process closed it as lost), append nothing and end the attempt in
    /// this process, naming that line. Checked on the first pass and (V15-R1
    /// R1-1) on the intended-line path, where an append that wrote nothing left
    /// the attempt *Intended*.
    fn end_if_a15_has_line(&mut self, index: usize, rows: &[Value]) -> Result<bool, String> {
        if self.session.entries[index].reconfirm.is_none() {
            return Ok(false);
        }
        let record = self.receipt.record_id();
        let Some(existing) = rows.iter().find(|v| v["act"]["record_id"] == record) else {
            return Ok(false);
        };
        let reason = format!(
            "A15 {record} already has ledger line {} ({}); nothing appended, one act has one line (RC-7, RB-8); review again",
            existing["ledger_seq"],
            existing["outcome"].as_str().unwrap_or("?")
        );
        close_attempt_journal(&self.session.root, &json!({"act":{"record_id":record}}))?;
        self.progress[index] = Progress::Failed(reason);
        Ok(true)
    }
    /// WR §4.8 RC-6: G-1R…G-4R and G-6R. Never creates, rewrites or repairs a
    /// store folder; publishes no copy (no G-5).
    fn advance_reconfirmation(
        &mut self,
        index: usize,
        r: Reconfirm,
        rows: &[Value],
    ) -> Result<(), String> {
        let e = &self.session.entries[index];
        let k = e.review.identity.clone();
        let root = self.session.root.clone();
        // G-1R (under the ledger lock; slot latest already checked above).
        if rows.get(r.ledger_seq as usize - 1) != Some(&r.line) {
            let reason = format!(
                "registered line {} no longer reads as reviewed; review again",
                r.ledger_seq
            );
            return self.fail_entry(index, reason, rows);
        }
        // V15 F4: an act log that cannot be read completely is a read limit: the
        // attempt stays pending with its cause instead of spending the act.
        if let Err(ActRecordFault::LogUnreadable(cause)) = act_record_found(&root, &r.line, &k) {
            return Err(format!(
                "revision {} standing not readable at G-1R: {cause}; attempt kept pending",
                r.sequence
            ));
        }
        if let Err(cause) = act_record_found(&root, &r.line, &k) {
            let reason = format!(
                "revision {} registration record incomplete: {cause}; review again",
                r.sequence
            );
            return self.fail_entry(index, reason, rows);
        }
        if is_held(&self.session.held, &k) {
            let reason = format!(
                "revision {} already selectable in this App session; select it",
                r.sequence
            );
            return self.fail_entry(index, reason, rows);
        }
        if self.base_changed(index, rows)? {
            return Ok(());
        }
        let e = &self.session.entries[index];
        // G-2R, G-3R: ‹k›'s store still recomputes; nothing is written to it.
        let store = store_path(&root, &k);
        storage::check_path(&store)?;
        if !Snapshot::capture(&store).is_ok_and(|s| s.files() == e.review.snapshot().files()) {
            let reason = format!(
                "revision {} store no longer recomputes (LS-4); review again",
                r.sequence
            );
            return self.fail_entry(index, reason, rows);
        }
        // G-4R: the intended line; the attempt is *stored* (attempt journal) first.
        let mut line = self.line(index, rows, "re-confirmed");
        line["sequence"] = r.line["sequence"].clone();
        line["store_path"] = r.line["store_path"].clone();
        super::wr_validate("library_entry", &line)?;
        rc9_guard(&root, rows, &line)?;
        write_attempt_journal(&root, &line)?;
        #[cfg(test)]
        if STOP_AFTER_STORED.with(|stop| stop.replace(false)) {
            return Err("injected process loss after the attempt was stored".into());
        }
        self.progress[index] = Progress::Intended(line.clone());
        append_line(&root, &line)?;
        self.finish_reconfirm(index, line)
    }
    /// G-6R once G-4R is durable: the App holds the result, so ‹k› is selectable
    /// in this process only (RC-2); ‹k› becomes the draft's base.
    fn finish_reconfirm(&mut self, index: usize, line: Value) -> Result<(), String> {
        let e = &self.session.entries[index];
        let store = store_path(&self.session.root, &e.review.identity);
        if Snapshot::capture(&store)?.files() != e.review.snapshot().files() {
            return Err("re-confirmed store no longer matches; selectable value withheld".into());
        }
        close_attempt_journal(&self.session.root, &line)?;
        let revision = RegisteredRevision {
            identity: e.review.identity.clone(),
            snapshot: e.review.snapshot().clone(),
            act_ref: self.receipt.record_id().into(),
        };
        hold(&self.session.held, &e.review.identity);
        let publication =
            match self
                .session
                .custody
                .put(&e.review.identity.name, &e.review.identity, true)
            {
                Ok(()) => PublicationOutcome::Current,
                Err(error) => PublicationOutcome::RepairPending(format!(
                    "App-kept base update pending: {error}"
                )),
            };
        self.progress[index] = Progress::ReConfirmed(revision, publication);
        Ok(())
    }
    fn line(&self, index: usize, rows: &[Value], outcome: &str) -> Value {
        let e = &self.session.entries[index];
        let mut v = json!({"record_kind":"library_entry","ledger_seq":rows.len()+1,"outcome":outcome,"identity":e.review.identity,"act":{"record_id":self.receipt.record_id(),"capture_evidence":self.receipt.capture_id()},"prior_revision":act_prior(e),"written_at":crate::util::now_rfc3339(),"evidence_limits":["identity not verified; original hot native A15; no historical native-origin promotion"]});
        if e.in_place {
            v["reviewed_entry"] = json!({"entry":e.reference,"content":content(e)});
        } else {
            v["reviewed_draft"] = json!({"draft":e.review.draft,"content":content(e)});
        }
        if let Some(r) = &e.reconfirm {
            v["disposition"] = json!("re-confirmation");
            v["reconfirms"] = r.reconfirms();
            v["evidence_limits"] = json!(["identity not verified; new hot native A15 re-confirms an earlier registered revision; the earlier act is not verified in this session and is not replayed (WR §4.8 RC-8)"]);
        }
        v
    }
    fn fail_entry(&mut self, index: usize, reason: String, rows: &[Value]) -> Result<(), String> {
        let mut line = self.line(index, rows, "not completed");
        line["reason"] = json!(reason);
        super::wr_validate("library_entry", &line)?;
        // V15 F1: a re-confirmation's *not completed* line must satisfy RC-9 too;
        // otherwise nothing is appended and the attempt stays pending (CI-25).
        rc9_guard(&self.session.root, rows, &line)?;
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
        if line["outcome"] == "re-confirmed" {
            return self.finish_reconfirm(index, line);
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
        // RC-2: this process now holds the registration result.
        hold(&self.session.held, &e.review.identity);
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
/// One append fails before anything is written (V15-R1 P6).
#[cfg(test)]
thread_local! { static FAIL_LEDGER_APPEND: Cell<bool> = const { Cell::new(false) }; }
#[cfg(test)]
thread_local! { static STOP_AFTER_STORED: Cell<bool> = const { Cell::new(false) }; }
fn hold(held: &Held, identity: &WorkflowIdentity) {
    if let Ok(mut h) = held.lock() {
        h.insert((identity.name.clone(), identity.revision.clone()));
    }
}
/// §5.2 attempt journal for a re-confirmation in *stored* (RC-6 G-3R): App-kept
/// and temporary, in the library's staging area (§3 "Review snapshots, staging";
/// X-1 reads "each library's attempt journal"). Removed when the attempt closes.
fn attempt_journal(root: &Path, line: &Value) -> PathBuf {
    root.join(".chirality/.workflow-staging/attempts")
        .join(format!(
            "{}.json",
            storage::key(&line["act"]["record_id"].to_string())
        ))
}
fn write_attempt_journal(root: &Path, line: &Value) -> Result<(), String> {
    let path = attempt_journal(root, line);
    storage::check_path(&path)?;
    let entry = json!({"record_kind":"wr_reconfirmation_attempt","state":"stored","act":line["act"],"intended":line});
    if let Ok(bytes) = fs::read(&path) {
        let existing: Value = serde_json::from_slice(&bytes)
            .map_err(|e| format!("attempt journal malformed: {}: {e}", path.display()))?;
        if existing["act"] == line["act"] {
            return Ok(());
        }
        return Err(format!(
            "attempt journal {} names another act",
            path.display()
        ));
    }
    storage::create_json(&path, &entry)
}
fn close_attempt_journal(root: &Path, line: &Value) -> Result<(), String> {
    let path = attempt_journal(root, line);
    storage::check_path(&path)?;
    match fs::remove_file(&path) {
        Ok(()) => storage::sync_dir(path.parent().ok_or("journal has no parent")?),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(()),
        Err(e) => Err(format!(
            "attempt journal not closed: {}: {e}",
            path.display()
        )),
    }
}
/// SQ-X X-1/X-2 for re-confirmation attempts (WR §4.8 RC-7; V13 F3). A *stored*
/// re-confirmation is never completed here. Under the ledger lock the ledger is
/// reread for a line citing the attempt's A15: if one exists nothing is written;
/// otherwise *not completed* "process lost before re-confirmation committed",
/// citing that A15. Either way the attempt closes and ‹k› is not selectable.
fn reconcile_reconfirmations(root: &Path) -> Vec<String> {
    let dir = root.join(".chirality/.workflow-staging/attempts");
    if storage::check_path(&dir).is_err() {
        return vec![format!(
            "attempt journal not established: {}",
            dir.display()
        )];
    }
    let list = || match fs::read_dir(&dir) {
        Ok(entries) => Ok(entries
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .filter(|p| {
                p.extension().is_some_and(|x| x == "json")
                    && !p
                        .file_name()
                        .is_some_and(|n| n.to_string_lossy().starts_with('.'))
            })
            .collect::<Vec<_>>()),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(vec![]),
        Err(e) => Err(format!(
            "attempt journal unreadable: {}: {e}",
            dir.display()
        )),
    };
    // A cheap look first, so a library with no journal takes no lock.
    match list() {
        Ok(files) if files.is_empty() => return vec![],
        Ok(_) => {}
        Err(cause) => return vec![cause],
    }
    let _lock = match storage::lock(&root.join(".chirality/workflow-registry.lock")) {
        Ok(lock) => lock,
        Err(e) => return vec![format!("X-2 pending: {e}")],
    };
    // V15 F8: list again under the lock; another process may have closed some.
    let files = match list() {
        Ok(files) => files,
        Err(cause) => return vec![cause],
    };
    let mut outcomes = vec![];
    for file in files {
        let result = (|| -> Result<String, String> {
            let bytes = match fs::read(&file) {
                Ok(bytes) => bytes,
                Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                    return Ok(format!(
                        "re-confirmation attempt journal {} already closed",
                        file.display()
                    ))
                }
                Err(e) => return Err(format!("{}: {e}", file.display())),
            };
            let journal: Value = serde_json::from_slice(&bytes)
                .map_err(|e| format!("attempt journal malformed: {}: {e}", file.display()))?;
            let intended = &journal["intended"];
            if journal["record_kind"] != "wr_reconfirmation_attempt"
                || intended["disposition"] != "re-confirmation"
                || journal["act"] != intended["act"]
            {
                return Err(format!("attempt journal malformed: {}", file.display()));
            }
            let record = &intended["act"]["record_id"];
            let rows = read_ledger(root)?;
            if rows.iter().any(|v| &v["act"]["record_id"] == record) {
                close_attempt_journal(root, intended)?;
                return Ok(format!(
                    "re-confirmation attempt of A15 {record} closed: a ledger line already cites it; nothing written"
                ));
            }
            let mut line = intended.clone();
            let fields = line.as_object_mut().ok_or("intended line not an object")?;
            fields.remove("sequence");
            fields.remove("store_path");
            line["outcome"] = json!("not completed");
            line["reason"] = json!("process lost before re-confirmation committed");
            line["ledger_seq"] = json!(rows.len() + 1);
            line["written_at"] = json!(crate::util::now_rfc3339());
            super::wr_validate("library_entry", &line)?;
            // V15 F1: never append a line the App's RC-9 reader would refuse;
            // the journal stays and the cause is reported.
            rc9_guard(root, &rows, &line)?;
            append_line(root, &line)?;
            close_attempt_journal(root, intended)?;
            Ok(format!(
                "re-confirmation attempt of A15 {record} not completed: process lost before re-confirmation committed"
            ))
        })();
        outcomes.push(result.unwrap_or_else(|cause| format!("X-2 pending: {cause}")));
    }
    outcomes
}
fn append_line(root: &Path, line: &Value) -> Result<(), String> {
    let path = root.join(".chirality/workflow-registry.jsonl");
    storage::check_path(&path)?;
    storage::ensure_directory(path.parent().unwrap())?;
    #[cfg(test)]
    if FAIL_LEDGER_APPEND.with(|fail| fail.replace(false)) {
        return Err("injected ledger append failure before any write".into());
    }
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
    registered_memory: std::sync::Arc<std::sync::Mutex<std::collections::HashSet<String>>>,
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
            let mut source = json!({"source":"process memory only; App data folder not attached","limit":"lost with this process (WR §3, U-WR-12)"});
            if base.is_some()
                && self
                    .registered_memory
                    .lock()
                    .map_err(|_| "App-kept base state unavailable")?
                    .contains(name)
            {
                source["record"] = json!({"state":"registered, unchanged since"});
            }
            return Ok(BaseObservation { base, source });
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
            let mut registered_names = self
                .registered_memory
                .lock()
                .map_err(|_| "App-kept base state unavailable")?;
            if registered {
                registered_names.insert(name.into());
            } else {
                registered_names.remove(name);
            }
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
            if let Ok(mut names) = self.registered_memory.lock() {
                names.remove(name);
            }
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

/// Draft workspace (WR SQ-D D-2…D-4, §5.1, TT-3, TT-4), in the Rust host under
/// the owner's OI-008 ruling for this workspace.
#[path = "workflow_drafts.rs"]
pub(crate) mod drafts;

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
