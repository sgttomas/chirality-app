//! Closed hot A15 owner. Native origin is an in-process event, never a file/DTO.
use super::*;
use crate::a15_native::ConfirmedA15Event;
use crate::workflow_workspace::{registration::CurrentReviewView, WorkflowIdentity};

#[derive(PartialEq, Eq)]
pub(crate) struct A15Binding {
    subject: WorkflowIdentity,
    content_method: String,
    content_value: String,
    reviewed_id3: String,
    reviewed_content_method: String,
    reviewed_content_value: String,
    prior: Option<WorkflowIdentity>,
}
impl A15Binding {
    pub(crate) fn subject(&self) -> &WorkflowIdentity {
        &self.subject
    }
    pub(crate) fn content_method(&self) -> &str {
        &self.content_method
    }
    pub(crate) fn content_value(&self) -> &str {
        &self.content_value
    }
    pub(crate) fn reviewed_id3(&self) -> &str {
        &self.reviewed_id3
    }
    pub(crate) fn reviewed_content_method(&self) -> &str {
        &self.reviewed_content_method
    }
    pub(crate) fn reviewed_content_value(&self) -> &str {
        &self.reviewed_content_value
    }
    pub(crate) fn prior(&self) -> Option<&WorkflowIdentity> {
        self.prior.as_ref()
    }
    fn content(&self) -> Value {
        json!({"method":self.content_method,"value":self.content_value})
    }
    fn reviewed(&self) -> Value {
        json!({"draft":self.reviewed_id3,"content":{"method":self.reviewed_content_method,"value":self.reviewed_content_value}})
    }
    fn subject_ref(&self) -> Result<String, String> {
        Ok(format!(
            "workflow revision {}",
            serde_json::to_string(&rs_tuple(&self.subject)).map_err(|e| e.to_string())?
        ))
    }
}
fn rs_tuple(tuple: &WorkflowIdentity) -> Value {
    let mut value = json!({"kind":tuple.kind,"origin":tuple.origin,"sourceRoot":tuple.source_root,
        "name":tuple.name,"revision":tuple.revision,"revisionMethod":tuple.revision_method});
    if let Some(base) = &tuple.derived_from {
        value["derivedFrom"] = rs_tuple(base);
    }
    value
}
struct BoundReview {
    review_ref: String,
    descriptor_id: String,
    descriptor_kind: String,
    library_root: PathBuf,
    act_log: PathBuf,
    descriptor: Value,
    presentation: Value,
    bindings: Vec<A15Binding>,
}
impl BoundReview {
    fn observe(view: &CurrentReviewView<'_>) -> Result<Self, String> {
        view.revalidate()?;
        let library_root = view.library_root().to_path_buf();
        if !library_root.is_absolute() || view.act_log() != storage::library_log(&library_root) {
            return Err("A15 owning library/log disagreement".into());
        }
        storage::check_path(&library_root)?;
        let bindings = view
            .ordered_bindings()
            .map(|b| A15Binding {
                subject: b.subject().clone(),
                content_method: b.content_method().into(),
                content_value: b.content_value().into(),
                reviewed_id3: b.reviewed_id3().into(),
                reviewed_content_method: b.reviewed_content_method().into(),
                reviewed_content_value: b.reviewed_content_value().into(),
                prior: b.prior().cloned(),
            })
            .collect::<Vec<_>>();
        let kind = view.descriptor_kind();
        if !matches!(kind, "a15_descriptor" | "a15_multi_descriptor")
            || bindings.is_empty()
            || (kind == "a15_descriptor" && bindings.len() != 1)
            || (kind == "a15_multi_descriptor" && bindings.len() < 2)
        {
            return Err("A15 descriptor entry count/kind disagreement".into());
        }
        let mut slots = std::collections::HashSet::new();
        for b in &bindings {
            b.subject.validate()?;
            if !matches!(b.subject.origin.as_str(), "project" | "user")
                || b.subject.revision_method != b.content_method
                || b.subject.revision != b.content_value
                || b.content_method != b.reviewed_content_method
                || b.content_value != b.reviewed_content_value
                || b.reviewed_id3
                    != format!(
                        "{}:{}:{}@{}",
                        if b.reviewed_id3.starts_with("draft:") {
                            "draft"
                        } else {
                            "entry"
                        },
                        b.subject.origin,
                        b.subject.name,
                        b.content_value
                    )
                || !slots.insert((
                    b.subject.origin.clone(),
                    b.subject.source_root.clone(),
                    b.subject.name.clone(),
                ))
            {
                return Err("A15 complete ordered content/ID-3/tuple binding disagreement".into());
            }
            if kind == "a15_multi_descriptor"
                && (!b.reviewed_id3.starts_with("entry:") || b.prior.is_some())
            {
                return Err("A15 multi descriptor accepts only prior-free in-place entries".into());
            }
            if let Some(prior) = &b.prior {
                prior.validate()?;
                if !prior.same_slot(&b.subject) {
                    return Err("A15 prior is in another slot".into());
                }
            }
        }
        let descriptor = view.descriptor().clone();
        if descriptor["descriptor_id"] != view.descriptor_id()
            || descriptor["record_kind"] != kind
            || descriptor["act_kind"] != "A15"
            || descriptor["review_ref"] != view.review_ref()
            || view.review_ref().is_empty()
            || view.descriptor_id().is_empty()
        {
            return Err("A15 owning descriptor identity disagreement".into());
        }
        // Closed source and mirrored field facts must ALSO match the descriptor.
        if kind == "a15_descriptor" {
            let b = &bindings[0];
            if descriptor["subject"]
                != serde_json::to_value(&b.subject).map_err(|e| e.to_string())?
                || descriptor["bound_content"] != b.content()
                || descriptor["relations"]["reviewed_draft"]["content"] != b.content()
                || descriptor["relations"]["reviewed_draft"]["draft"]["draft_location"]
                    != b.subject.origin
                || descriptor["relations"]["reviewed_draft"]["draft"]["name"] != b.subject.name
                || descriptor["relations"]["reviewed_draft"]["draft"]["draft_root"]
                    != library_root
                        .join(if b.reviewed_id3.starts_with("draft:") {
                            ".chirality/workflow-drafts"
                        } else {
                            ".chirality/workflows"
                        })
                        .display()
                        .to_string()
                || descriptor["relations"]["prior_revision"]
                    != serde_json::to_value(&b.prior).map_err(|e| e.to_string())?
            {
                return Err("A15 single descriptor and current binding facts disagree".into());
            }
        } else {
            let entries = descriptor["entries"]
                .as_array()
                .ok_or("A15 multi descriptor entries absent")?;
            if entries.len() != bindings.len() {
                return Err("A15 multi descriptor count disagreement".into());
            }
            for (entry, b) in entries.iter().zip(&bindings) {
                if entry["subject"]
                    != serde_json::to_value(&b.subject).map_err(|e| e.to_string())?
                    || entry["bound_content"] != b.content()
                    || entry["reviewed_entry"] != b.reviewed_id3
                    || b.prior.is_some()
                {
                    return Err("A15 multi descriptor ordered facts disagree".into());
                }
            }
        }
        Ok(Self {
            review_ref: view.review_ref().into(),
            descriptor_id: view.descriptor_id().into(),
            descriptor_kind: kind.into(),
            library_root,
            act_log: view.act_log().to_path_buf(),
            descriptor,
            presentation: view.review_presentation().clone(),
            bindings,
        })
    }
    fn matches(&self, other: &Self) -> bool {
        self.review_ref == other.review_ref
            && self.descriptor_id == other.descriptor_id
            && self.descriptor_kind == other.descriptor_kind
            && self.library_root == other.library_root
            && self.act_log == other.act_log
            && self.descriptor == other.descriptor
            && self.presentation == other.presentation
            && self.bindings == other.bindings
    }
}
struct A15NativeWitness {
    original_capture: Value,
    durable_record: Value,
    original_offer: Value,
}
/// Origin-bearing move-only value. No constructor/serde/Clone/file loader.
pub(crate) struct HotA15Receipt {
    bound: BoundReview,
    record_id: String,
    capture_id: String,
    witness: std::sync::Arc<A15NativeWitness>,
}
impl HotA15Receipt {
    pub(crate) fn review_ref(&self) -> &str {
        &self.bound.review_ref
    }
    pub(crate) fn descriptor_id(&self) -> &str {
        &self.bound.descriptor_id
    }
    pub(crate) fn descriptor_kind(&self) -> &str {
        &self.bound.descriptor_kind
    }
    pub(crate) fn library_root(&self) -> &Path {
        &self.bound.library_root
    }
    pub(crate) fn act_log(&self) -> &Path {
        &self.bound.act_log
    }
    pub(crate) fn record_id(&self) -> &str {
        &self.record_id
    }
    pub(crate) fn capture_id(&self) -> &str {
        &self.capture_id
    }
    pub(crate) fn ordered_bindings(&self) -> &[A15Binding] {
        &self.bound.bindings
    }
}
pub(crate) struct A15OfferRef {
    id: String,
}
impl A15OfferRef {
    pub(crate) fn id(&self) -> &str {
        &self.id
    }
}
pub(crate) enum HotA15Result {
    Recorded(HotA15Receipt),
    RecordPending {
        capture_id: String,
        reason: String,
    },
    AlreadyTransferred {
        capture_id: String,
        record_id: String,
    },
}
pub(super) struct A15Custody {
    library_root: PathBuf,
    bound: Option<BoundReview>,
    original_offer: Value,
    record_id: Option<String>,
    receipt_issued: bool,
}
impl A15Custody {
    pub(super) fn belongs_to(&self, root: &Path) -> bool {
        self.library_root == root
    }
}
pub(super) struct A15OfferSlot {
    bound: Option<BoundReview>,
    offer: Value,
    state: OfferState,
    actor: Option<Value>,
    context: Option<Value>,
    capture_id: Option<String>,
}
impl ActControl {
    pub(crate) fn compose_a15(
        &mut self,
        current: &CurrentReviewView<'_>,
    ) -> Result<A15OfferRef, String> {
        let bound = BoundReview::observe(current)?;
        if self.workspace != bound.library_root {
            return Err("A15 control belongs to another owning library".into());
        }
        let id = crate::util::opaque_id("offer:")?;
        let entries = bound
            .bindings
            .iter()
            .map(|b| {
                Ok(
                    json!({"subject":{"ref":b.subject_ref()?,"contentIdentity":b.content()},
            "reviewedDraft":b.reviewed(),"priorRevision":b.prior.as_ref().map(rs_tuple)}),
                )
            })
            .collect::<Result<Vec<_>, String>>()?;
        let mut offer = json!({"format":"chirality.aac.offer","formatVersion":"0.3","offerId":id,"actKind":"A15",
            "wording":bound.descriptor["wording"],"descriptorId":bound.descriptor_id,"descriptorKind":bound.descriptor_kind,"entries":entries,
            "scope":bound.descriptor["scope"],"purpose":bound.descriptor["purpose"],"actorRequirement":"the person","declineAvailable":false,
            "answers":{"standing":STANDING},"composedAt":now_rfc3339()});
        offer["offerDigest"] = json!({"method":OFFER_DIGEST_METHOD,"value":offer_digest(&offer)?});
        crate::schema_validation::validate_offer(&offer)?;
        self.a15_offers.insert(
            id.clone(),
            A15OfferSlot {
                bound: Some(bound),
                offer,
                state: OfferState::Composed,
                actor: None,
                context: None,
                capture_id: None,
            },
        );
        Ok(A15OfferRef { id })
    }
    pub(crate) fn a15_confirmation_text(
        &mut self,
        offer: &A15OfferRef,
        current: &CurrentReviewView<'_>,
        actor: &Value,
        context: &Value,
    ) -> Result<String, String> {
        let now = BoundReview::observe(current)?;
        if self.workspace != now.library_root {
            return Err("A15 control owning root changed".into());
        }
        let slot = self
            .a15_offers
            .get_mut(&offer.id)
            .ok_or("A15 offer absent")?;
        if slot.state != OfferState::Composed
            || !slot.bound.as_ref().is_some_and(|b| b.matches(&now))
        {
            slot.state = OfferState::Stale;
            return Err("A15 review changed; nothing captured".into());
        }
        if slot.actor.as_ref().is_some_and(|a| a != actor)
            || slot.context.as_ref().is_some_and(|c| c != context)
        {
            return Err("A15 actor/context already frozen".into());
        }
        if actor["identityVerified"] != false {
            return Err("A15 observed actor must retain identity not verified".into());
        }
        crate::schema_validation::validate_offer(&slot.offer)?;
        if offer_digest(&slot.offer)? != slot.offer["offerDigest"]["value"].as_str().unwrap_or("") {
            return Err("A15 frozen offer digest mismatch".into());
        }
        slot.actor = Some(actor.clone());
        slot.context = Some(context.clone());
        Ok(format!("{} (A15)\n\nOwning library: {}\nComplete review:\n{}\n\nNative offer:\n{}\n\nActor: {} (identity not verified)\n\nRegistering makes these reviewed bytes available in this library. It is not a check that the workflow can run here.\nNative confirmation only; Accessibility-authorized processes may operate native buttons. Cancel closes without an act.",
            slot.offer["wording"].as_str().unwrap_or(""),now.library_root.display(),serde_json::to_string_pretty(&now.presentation).map_err(|e|e.to_string())?,
            serde_json::to_string_pretty(&slot.offer).map_err(|e|e.to_string())?,serde_json::to_string(actor).map_err(|e|e.to_string())?))
    }
    pub(crate) fn frozen_a15_offer_digest(&self, offer: &A15OfferRef) -> Result<&Value, String> {
        let slot = self.a15_offers.get(&offer.id).ok_or("A15 offer absent")?;
        if !matches!(slot.state, OfferState::Composed | OfferState::Presented)
            || slot.actor.is_none()
            || slot.context.is_none()
            || offer_digest(&slot.offer)?
                != slot.offer["offerDigest"]["value"].as_str().unwrap_or("")
        {
            return Err("A15 offer absent/unfrozen/stale or digest mismatch".into());
        }
        Ok(&slot.offer["offerDigest"])
    }
    pub(crate) fn present_a15(&mut self, offer: &A15OfferRef) -> Result<(), String> {
        self.frozen_a15_offer_digest(offer)?;
        let slot = self.a15_offers.get_mut(&offer.id).unwrap();
        if slot.state != OfferState::Composed {
            return Err("A15 offer already presented".into());
        }
        slot.state = OfferState::Presented;
        Ok(())
    }
    pub(crate) fn dismiss_a15(&mut self, offer: &A15OfferRef) {
        if let Some(slot) = self.a15_offers.get_mut(&offer.id) {
            if matches!(slot.state, OfferState::Composed | OfferState::Presented) {
                slot.state = OfferState::Dismissed;
            }
        }
    }
    pub(crate) fn confirm_a15_after_native_event(
        &mut self,
        offer: &A15OfferRef,
        event: ConfirmedA15Event,
        current: &CurrentReviewView<'_>,
    ) -> Result<HotA15Result, String> {
        let now = BoundReview::observe(current)?;
        if self.workspace != now.library_root {
            return Err("A15 control owning root changed".into());
        }
        let slot = self
            .a15_offers
            .get_mut(&offer.id)
            .ok_or("A15 offer absent")?;
        if slot.state != OfferState::Presented {
            return Err("A15 not presented or already captured".into());
        }
        if !slot.bound.as_ref().is_some_and(|b| b.matches(&now)) {
            slot.state = OfferState::Stale;
            return Err("A15 review stale; nothing captured".into());
        }
        if event.offer_id() != offer.id
            || event.offer_digest() != &slot.offer["offerDigest"]
            || slot.actor.as_ref() != Some(event.actor())
            || slot.context.as_ref() != Some(event.owning_context())
            || offer_digest(&slot.offer)? != event.offer_digest()["value"].as_str().unwrap_or("")
        {
            return Err("A15 native event does not match frozen offer/actor/context".into());
        }
        let cap_id = crate::util::opaque_id("cap:")?;
        let o = slot.offer.clone();
        let es = o["entries"].as_array().ok_or("A15 entries absent")?;
        let capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":cap_id,"offerId":offer.id,
            "offerDigest":o["offerDigest"],"choice":"act","actKind":"A15","actor":event.actor(),
            "boundSubject":es.iter().map(|e|e["subject"]["ref"].clone()).collect::<Vec<_>>(),
            "boundContent":es.iter().map(|e|e["subject"]["contentIdentity"].clone()).collect::<Vec<_>>(),
            "scope":o["scope"],"purpose":o["purpose"],"capturedAt":capture_time(),"surface":"App interface","inputSource":"host-native-confirmation",
            "answers":o["answers"],"descriptorId":o["descriptorId"],"descriptorKind":o["descriptorKind"],
            "entries":es.iter().map(|e|json!({"revision":e["subject"]["ref"],"reviewedDraft":e["reviewedDraft"],"priorRevision":e["priorRevision"]})).collect::<Vec<_>>(),
            "evidenceLimits":["identity not verified"]});
        crate::schema_validation::validate_capture(&capture)?;
        let root = self.workspace.clone();
        let target_log = storage::library_log(&root)
            .strip_prefix(&root)
            .map_err(|e| e.to_string())?
            .to_str()
            .ok_or("A15 non-UTF8 owning log")?
            .to_owned();
        let _lock = storage::lock(&root.join(CAPTURE_STORE).join(".capture.lock"))?;
        let bound = slot.bound.take().ok_or("A15 binding already captured")?;
        slot.capture_id = Some(cap_id.clone());
        slot.state = OfferState::Captured;
        let mut native = NativeCapture {
            ordinal: self.native_captures.len(),
            target_log,
            a15: Some(A15Custody {
                library_root: root.clone(),
                bound: Some(bound),
                original_offer: o,
                record_id: None,
                receipt_issued: false,
            }),
            written: false,
            delay_pending: false,
            capture: capture.clone(),
            pending: None,
            failure: None,
        };
        if let Err(e) = storage::create_json(&storage::capture_path(&root, &cap_id), &capture) {
            native.failure = Some(e);
        } else {
            match records::prepare_capture_submission(&root, &capture, &native.target_log) {
                Ok(p) => {
                    native.pending = Some(p);
                    if let Err(e) =
                        records::persist_capture_submission(&root, native.pending.as_ref().unwrap())
                    {
                        pending_failure(&root, &mut native, &e);
                    }
                }
                Err(e) => native.failure = Some(e),
            }
        }
        self.native_captures.insert(cap_id, native);
        self.flush_native_locked();
        self.finish_a15_delivery(offer)
    }
    pub(crate) fn continue_a15(&mut self, offer: &A15OfferRef) -> Result<HotA15Result, String> {
        if self
            .a15_offers
            .get(&offer.id)
            .is_none_or(|s| s.capture_id.is_none())
        {
            return Err("A15 original captured offer absent".into());
        }
        let id = self
            .a15_offers
            .get(&offer.id)
            .and_then(|s| s.capture_id.as_ref())
            .ok_or("A15 captured offer absent")?;
        if self
            .native_captures
            .get(id)
            .and_then(|n| n.a15.as_ref())
            .is_none_or(|a| !a.belongs_to(&self.workspace))
        {
            return Err("A15 original library custody changed".into());
        }
        let _lock = storage::lock(&self.workspace.join(CAPTURE_STORE).join(".capture.lock"))?;
        self.flush_native_locked();
        self.finish_a15_delivery(offer)
    }
    fn finish_a15_delivery(&mut self, offer: &A15OfferRef) -> Result<HotA15Result, String> {
        let slot = self
            .a15_offers
            .get_mut(&offer.id)
            .ok_or("A15 offer absent")?;
        let id = slot.capture_id.as_ref().ok_or("A15 not captured")?.clone();
        let native = self
            .native_captures
            .get_mut(&id)
            .ok_or("A15 original native custody absent")?;
        let a15 = native.a15.as_mut().ok_or("A15 native custody absent")?;
        if !a15.belongs_to(&self.workspace) {
            return Err("A15 original library custody changed".into());
        }
        if a15.receipt_issued {
            return Ok(HotA15Result::AlreadyTransferred {
                capture_id: id,
                record_id: a15
                    .record_id
                    .clone()
                    .ok_or("A15 issued record identity absent")?,
            });
        }
        if !native.written || native.delay_pending {
            slot.state = OfferState::RecordPending;
            return Ok(HotA15Result::RecordPending {
                capture_id: id,
                reason: native.failure.clone().unwrap_or_else(|| {
                    "original native capture/record durability or delayed account pending".into()
                }),
            });
        }
        // Equality validates original witness; it does not create origin. Only this
        // retained A15 native object can reach receipt construction.
        let original = native.capture.clone();
        let result = recover_capture(&self.workspace, &original, Some(native), None, true)?;
        if result["state"] != "AC-7 recorded"
            || result["recordDurable"] != true
            || result["delayEvidencePending"] == true
        {
            native.written = false;
            slot.state = OfferState::RecordPending;
            return Ok(HotA15Result::RecordPending {
                capture_id: id,
                reason: result["writeFailure"]
                    .as_str()
                    .unwrap_or("A15 original record durability pending")
                    .into(),
            });
        }
        let a15 = native.a15.as_mut().unwrap();
        let rid = result["record"]["recordId"]
            .as_str()
            .ok_or("A15 matching record identity absent")?
            .to_owned();
        let bound = a15
            .bound
            .take()
            .ok_or("A15 original binding already transferred")?;
        let witness = std::sync::Arc::new(A15NativeWitness {
            original_capture: original,
            durable_record: result["record"].clone(),
            original_offer: a15.original_offer.clone(),
        });
        a15.receipt_issued = true;
        a15.record_id = Some(rid.clone());
        slot.state = OfferState::Recorded;
        Ok(HotA15Result::Recorded(HotA15Receipt {
            bound,
            record_id: rid,
            capture_id: id,
            witness,
        }))
    }
}
pub(super) fn a15_body(capture: &Value) -> Value {
    let entries = capture["entries"].as_array();
    let relations = if capture["descriptorKind"] == "a15_descriptor" {
        json!({"reviewedDraft":capture["entries"][0]["reviewedDraft"],"priorRevision":capture["entries"][0]["priorRevision"]})
    } else {
        json!({"registeredEntries":entries.map(|es|es.iter().map(|e|json!({"subject":e["revision"],"reviewedDraft":e["reviewedDraft"],"priorRevision":e["priorRevision"]})).collect::<Vec<_>>()).unwrap_or_default()})
    };
    json!({"actKind":"A15","actClass":{"value":"person's act (V4-WF-02)"},"decisionActor":capture["actor"],"recordingMode":"direct capture",
        "boundSubject":capture["boundSubject"],"boundContent":capture["boundContent"],"scope":capture["scope"],"purpose":capture["purpose"],
        "captureEvidence":[{"kind":"capture evidence","ref":capture["captureId"],"resolutionAtWrite":"resolved"}],
        "captureTime":capture["capturedAt"],"evidenceLimits":capture["evidenceLimits"],"relations":relations})
}

#[cfg(test)]
mod tests {
    //! Synthetic events, actual owner reads/writer/receipt; no native event evidence.
    use super::*;
    use crate::workflow_workspace::{
        registration::{LibraryOwner, ReviewSession},
        Snapshot,
    };
    fn library(names: &[&str], in_place: bool) -> (PathBuf, ReviewSession) {
        let root = std::env::temp_dir().join(crate::util::opaque_id("aac-a15-test-").unwrap());
        std::fs::create_dir(&root).unwrap();
        let root = std::fs::canonicalize(root).unwrap();
        for name in names {
            let path = root
                .join(if in_place {
                    ".chirality/workflows"
                } else {
                    ".chirality/workflow-drafts"
                })
                .join(name);
            std::fs::create_dir_all(&path).unwrap();
            std::fs::write(
                path.join("WORKFLOW.md"),
                format!("---\nname: {name}\n---\n# Method\nDo bounded work.\n"),
            )
            .unwrap();
        }
        let owner = LibraryOwner::open(root.clone(), "project", "fixture-library").unwrap();
        let session = if in_place {
            owner
                .review_in_place(&names.iter().map(|n| n.to_string()).collect::<Vec<_>>())
                .unwrap()
        } else {
            let rev =
                Snapshot::capture(&root.join(".chirality/workflow-drafts").join(names[0])).unwrap();
            owner.review_draft(names[0], rev.revision()).unwrap()
        };
        (root, session)
    }
    fn ready(
        root: &Path,
        session: &ReviewSession,
    ) -> (ActControl, A15OfferRef, Value, Value, Value) {
        let mut ac = ActControl::new(root);
        let current = session.current().unwrap();
        let offer = ac.compose_a15(&current).unwrap();
        assert!(ac.frozen_a15_offer_digest(&offer).is_err());
        let actor = person(Some("Synthetic test person"), Some("fixture"));
        let context = json!({"fixture":"synthetic owning context"});
        let text = ac
            .a15_confirmation_text(&offer, &current, &actor, &context)
            .unwrap();
        assert!(text.contains("identity not verified"));
        assert!(text.contains("Accessibility"));
        let digest = ac.frozen_a15_offer_digest(&offer).unwrap().clone();
        ac.present_a15(&offer).unwrap();
        (ac, offer, actor, context, digest)
    }
    fn event(
        offer: &A15OfferRef,
        digest: Value,
        actor: Value,
        context: Value,
    ) -> ConfirmedA15Event {
        ConfirmedA15Event::synthetic_for_test(offer.id().into(), digest, actor, context)
    }
    #[test]
    fn synthetic_single_receipt_durable_library_record_once_and_cold_cannot_transfer() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        let current = session.current().unwrap();
        let result = ac
            .confirm_a15_after_native_event(&offer, event(&offer, digest, actor, context), &current)
            .unwrap();
        let HotA15Result::Recorded(receipt) = result else {
            panic!("expected durable real-writer receipt from synthetic event")
        };
        assert_eq!(receipt.review_ref(), current.review_ref());
        assert_eq!(receipt.library_root(), root);
        assert_eq!(receipt.ordered_bindings().len(), 1);
        assert!(receipt.witness.original_capture["actKind"] == "A15");
        assert_eq!(
            receipt.witness.durable_record["body"],
            a15_body(&receipt.witness.original_capture)
        );
        assert_eq!(receipt.witness.original_offer["offerId"], offer.id());
        let (records, limits) = records::read_log(&storage::library_log(&root));
        assert!(limits.is_empty());
        assert_eq!(records.len(), 1);
        assert_eq!(records[0]["recordId"], receipt.record_id());
        assert!(!root.join(LOG).exists());
        assert!(matches!(
            ac.continue_a15(&offer).unwrap(),
            HotA15Result::AlreadyTransferred { .. }
        ));
        let before_cold = std::fs::read(storage::library_log(&root)).unwrap();
        let mut cold = ActControl::new(&root);
        cold.recover_pending().unwrap();
        assert!(cold.continue_a15(&offer).is_err());
        assert_eq!(
            std::fs::read(storage::library_log(&root)).unwrap(),
            before_cold
        );
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn synthetic_wrong_frozen_digest_captures_nothing() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, mut digest) = ready(&root, &session);
        digest["value"] = json!("wrong");
        let result = ac.confirm_a15_after_native_event(
            &offer,
            event(&offer, digest, actor, context),
            &session.current().unwrap(),
        );
        assert!(result.is_err());
        assert!(ac.native_captures.is_empty());
        assert!(!storage::library_log(&root).exists());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn synthetic_retained_old_view_rechecks_live_freshness_before_capture() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        let old = session.current().unwrap();
        std::fs::write(
            root.join(".chirality/workflow-drafts/sample/WORKFLOW.md"),
            "changed externally",
        )
        .unwrap();
        assert!(ac
            .confirm_a15_after_native_event(&offer, event(&offer, digest, actor, context), &old)
            .is_err());
        assert!(ac.native_captures.is_empty());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn synthetic_failed_capture_publication_retains_original_pending_then_one_receipt() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        storage::ensure_directory(&root.join(CAPTURE_STORE)).unwrap();
        storage::fail_directory_for_test(Some(root.join(CAPTURE_STORE)));
        let pending = ac.confirm_a15_after_native_event(
            &offer,
            event(&offer, digest, actor, context),
            &session.current().unwrap(),
        );
        storage::fail_directory_for_test(None);
        assert!(matches!(
            pending.unwrap(),
            HotA15Result::RecordPending { .. }
        ));
        let original = ac.native_captures.values().next().unwrap().capture.clone();
        let HotA15Result::Recorded(receipt) = ac.continue_a15(&offer).unwrap() else {
            panic!("hot continuation must finish original")
        };
        assert_eq!(
            receipt.capture_id(),
            original["captureId"].as_str().unwrap()
        );
        assert_eq!(receipt.witness.original_capture, original);
        assert_eq!(
            receipt.witness.durable_record["observedAt"],
            original["capturedAt"]
        );
        assert!(matches!(
            ac.continue_a15(&offer).unwrap(),
            HotA15Result::AlreadyTransferred { .. }
        ));
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn synthetic_multi_preserves_requested_entry_order_and_full_tuple_refs() {
        let (root, session) = library(&["second", "first"], true);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        let HotA15Result::Recorded(receipt) = ac
            .confirm_a15_after_native_event(
                &offer,
                event(&offer, digest, actor, context),
                &session.current().unwrap(),
            )
            .unwrap()
        else {
            panic!("expected multi receipt")
        };
        assert_eq!(receipt.ordered_bindings()[0].subject().name, "second");
        assert_eq!(receipt.ordered_bindings()[1].subject().name, "first");
        let body = &receipt.witness.durable_record["body"];
        assert_eq!(
            body["relations"]["registeredEntries"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
        for (i, b) in receipt.ordered_bindings().iter().enumerate() {
            assert_eq!(body["boundSubject"][i], b.subject_ref().unwrap());
            assert_eq!(
                body["relations"]["registeredEntries"][i]["subject"],
                body["boundSubject"][i]
            );
            assert!(body["boundSubject"][i]
                .as_str()
                .unwrap()
                .contains("sourceRoot"));
            assert!(b.prior().is_none());
        }
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn synthetic_changed_control_root_never_redirects_original_capture() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        ac.workspace = root.join("other-root");
        assert!(ac
            .confirm_a15_after_native_event(
                &offer,
                event(&offer, digest, actor, context),
                &session.current().unwrap()
            )
            .is_err());
        assert!(ac.native_captures.is_empty());
        assert!(!ac.workspace.exists());
        std::fs::remove_dir_all(root).unwrap();
    }
}
