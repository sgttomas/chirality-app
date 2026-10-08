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
    /// Digest of the complete review the native statement named (J6 D-1).
    review_digest: Option<String>,
}
/// sha-256 (lowercase hex) of the complete review presentation in the
/// `aac-offer-digest/0.1` canonical serialization (canonical.rs). The native
/// statement names it; the App computes the same value beside the review it
/// shows, so the person can tie the statement to the complete review.
pub(crate) fn review_digest(presentation: &Value) -> Result<String, String> {
    let mut canonical = String::new();
    crate::canonical::canonical(presentation, &mut canonical).map_err(|e| {
        format!("A15 complete review digest unavailable ({e}); nothing presented or captured")
    })?;
    Ok(crate::util::sha256_hex(canonical.as_bytes()))
}
/// The bounded native A15 statement (J6 D-1). It names the act, every entry's
/// workflow identity (short and full revision), the prior revision, the
/// library, scope and purpose, the complete review by reference and digest,
/// the offer, the consequence, the actor and its limit, and what Cancel does.
/// The complete review itself is shown in the App (AAC §4.2 step 1, §6.2).
fn a15_statement(o: &Value, bound: &BoundReview, actor: &Value, review_digest: &str) -> String {
    use super::native_statement::{actor_line, short};
    let n = bound.bindings.len();
    let wording = o["wording"].as_str().unwrap_or("");
    let mut t = vec![if n == 1 {
        format!("{wording} (A15)")
    } else {
        format!("{wording} (A15, {n} entries)")
    }];
    let methods = bound
        .bindings
        .iter()
        .map(|b| b.subject.revision_method.as_str())
        .collect::<std::collections::BTreeSet<_>>();
    let one_method = (methods.len() == 1).then(|| methods.iter().next().copied()).flatten();
    if let Some(method) = one_method {
        t.push(format!("Revision method: {method}"));
    }
    let disposition = bound.descriptor["disposition"].as_str().unwrap_or("not stated");
    for (i, b) in bound.bindings.iter().enumerate() {
        let s = &b.subject;
        let number = if n == 1 { String::new() } else { format!(" {}", i + 1) };
        let reviewed = if b.reviewed_id3.starts_with("draft:") {
            "; reviewed draft"
        } else {
            ""
        };
        t.push(format!(
            "Workflow{number}: {} ({} library; {disposition}{reviewed})",
            s.name, s.origin
        ));
        match one_method {
            Some(_) => t.push(format!("Revision {}, in full:", short(&s.revision))),
            None => t.push(format!(
                "Revision {} ({}), in full:",
                short(&s.revision),
                s.revision_method
            )),
        }
        t.push(s.revision.clone());
        match &b.prior {
            None => t.push("Prior revision: none".into()),
            Some(p) => {
                t.push(format!("Prior revision {}, in full:", short(&p.revision)));
                t.push(p.revision.clone());
            }
        }
        if let Some(base) = &s.derived_from {
            t.push(format!("Derived from: {} revision {}", base.name, short(&base.revision)));
        }
    }
    let library = bound.library_root.display().to_string();
    let scope = o["scope"].as_str().unwrap_or("");
    if scope == library {
        // The App's library scope is its source root: one exact line, not two.
        t.push(format!("Library and scope: {library}"));
    } else {
        t.push(format!("Library: {library}"));
        t.push(format!("Scope: {scope}"));
    }
    t.push(format!("Purpose: {}", o["purpose"].as_str().unwrap_or("")));
    t.push(format!("Answers: {}", o["answers"]["standing"].as_str().unwrap_or(STANDING)));
    t.push(String::new());
    t.push(format!("Complete review: in the App, {}", bound.review_ref));
    t.push("Its sha-256 digest (compare with the App):".into());
    t.push(review_digest.into());
    t.push(format!(
        "Offer: {} (digest {})",
        o["offerId"].as_str().unwrap_or(""),
        short(o["offerDigest"]["value"].as_str().unwrap_or(""))
    ));
    t.push(String::new());
    t.push("Registering makes these reviewed bytes available in this library; earlier revisions are kept. It is not a check that the workflow can run here.".into());
    t.push(format!("Actor: {}. Required: {}.", actor_line(actor), o["actorRequirement"].as_str().unwrap_or("the person")));
    t.push("Register records this act. Cancel closes without an act: nothing is captured or registered.".into());
    t.push("Native confirmation; apps with Accessibility access could press these buttons.".into());
    t.join("\n")
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
                review_digest: None,
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
        // Composed from the frozen binding (equal to `now`, checked above).
        let frozen = slot.bound.as_ref().ok_or("A15 binding absent")?;
        let digest = review_digest(&frozen.presentation)?;
        let text = super::native_statement::bounded(
            "A15 native confirmation",
            a15_statement(&slot.offer, frozen, actor, &digest),
        )?;
        slot.actor = Some(actor.clone());
        slot.context = Some(context.clone());
        slot.review_digest = Some(digest);
        Ok(text)
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
        // The complete review the native statement named by digest is still the
        // review now bound (in addition to the full equality above).
        if slot.review_digest.as_deref() != Some(review_digest(&now.presentation)?.as_str()) {
            slot.state = OfferState::Stale;
            return Err("A15 complete review differs from the one the native statement named; nothing captured".into());
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
        // Retain the consumed native event's original facts/once guard even at
        // the first storage boundary. No record ID is reserved before capture
        // publication. This hot continuation choice does not redefine AAC's
        // permitted pre-capture "nothing captured" refusal or old A16 behavior.
        let _lock = match storage::lock(&root.join(CAPTURE_STORE).join(".capture.lock")) {
            Ok(lock) => lock,
            Err(error) => {
                native.failure = Some(error.clone());
                slot.state = OfferState::RecordPending;
                self.native_captures.insert(cap_id.clone(), native);
                return Ok(HotA15Result::RecordPending { capture_id: cap_id, reason: error });
            }
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
    /// J6 D-1 control (written before the repair, kept): the native A15
    /// statement must fit a readable alert and still name every binding element.
    /// Limits are literal here so the control does not depend on the repair.
    #[test]
    fn control_a15_native_statement_is_bounded_and_names_every_binding() {
        for (names, in_place) in [(&["sample"][..], false), (&["second", "first"][..], true)] {
            let (root, session) = library(names, in_place);
            let mut ac = ActControl::new(&root);
            let current = session.current().unwrap();
            let offer = ac.compose_a15(&current).unwrap();
            let actor = person(Some("Synthetic test person"), Some("fixture-os"));
            let context = json!({"fixture":"synthetic owning context"});
            let text = ac
                .a15_confirmation_text(&offer, &current, &actor, &context)
                .unwrap();
            let (lines, chars) = (text.lines().count(), text.chars().count());
            assert!(
                lines <= 30 && chars <= 1400,
                "native A15 statement unbounded: {lines} lines, {chars} chars"
            );
            assert!(!text.contains("{\""), "raw JSON in native statement:\n{text}");
            let wording = ac.a15_offers[offer.id()].offer["wording"].as_str().unwrap().to_owned();
            assert!(text.starts_with(&wording), "{text}");
            assert!(text.contains("(A15"), "{text}");
            for b in current.ordered_bindings() {
                let s = b.subject();
                assert!(text.contains(&s.name) && text.contains(&s.origin), "{text}");
                assert!(text.contains(&s.revision[..12]), "short revision: {text}");
                assert!(
                    text.lines().any(|l| l.trim() == s.revision),
                    "full revision on its own copyable line:\n{text}"
                );
                assert!(text.contains(&s.revision_method), "{text}");
            }
            assert!(text.contains("Prior revision: none"), "{text}");
            assert!(text.contains(&root.display().to_string()), "library: {text}");
            let descriptor = current.descriptor();
            assert!(text.contains(descriptor["scope"].as_str().unwrap()), "{text}");
            assert!(text.contains(descriptor["purpose"].as_str().unwrap()), "{text}");
            assert!(text.contains(current.review_ref()), "{text}");
            let mut canonical = String::new();
            crate::canonical::canonical(current.review_presentation(), &mut canonical).unwrap();
            let review_digest = crate::util::sha256_hex(canonical.as_bytes());
            assert!(
                text.lines().any(|l| l.trim() == review_digest),
                "complete-review digest on its own line:\n{text}"
            );
            assert!(text.contains(offer.id()), "{text}");
            assert!(text.contains("Synthetic test person") && text.contains("fixture-os"));
            assert!(text.contains("identity not verified"), "{text}");
            assert!(text.contains("not a check that the workflow can run here"), "{text}");
            assert!(text.contains("Cancel closes without an act"), "{text}");
            assert!(text.contains("Accessibility"), "{text}");
            drop(current);
            std::fs::remove_dir_all(root).unwrap();
        }
    }
    /// Shared vector with app/tests/presentation.test.mjs: the App's review
    /// digest (src/presentation.ts) must equal the one the native statement names.
    #[test]
    fn review_digest_vector_is_shared_with_the_app_view() {
        let vector = json!({"b":"x\u{2028}ü≈\u{7f}\u{1}\n\"\\","a":[1,-2,true,null,{"z":"😀","é":0,"y":"\t\u{8}\u{c}\r"}],"😀":"astral key","\u{ffff}":"bmp max key"});
        let mut canonical = String::new();
        crate::canonical::canonical(&vector, &mut canonical).unwrap();
        assert!(canonical.find("\"\u{ffff}\":").unwrap() < canonical.find("\"😀\":").unwrap(), "code-point key order");
        // Also computed independently (Python, code-point key order) during J6.
        assert_eq!(
            review_digest(&vector).unwrap(),
            "f0320f0cb802f23b0ca96ae972832215676a3c76e825efceb37c941e8e0e6d6b"
        );
        assert!(review_digest(&json!({"x":1.5})).unwrap_err().contains("nothing presented"));
    }
    /// A realistic large single registration (long library path used as scope,
    /// prior revision, derived-from base, full actor) still fits the bound; a
    /// multi-entry act fits up to a stated count and is refused above it.
    #[test]
    fn realistic_large_statements_fit_or_are_refused_whole() {
        let library = PathBuf::from(format!(
            "/private/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/tmp.{}/workspace",
            "x".repeat(40)
        ));
        let id = |name: &str, rev: char, base: Option<WorkflowIdentity>| WorkflowIdentity {
            kind: "workflow".into(),
            origin: "project".into(),
            source_root: library.display().to_string(),
            name: name.into(),
            revision: rev.to_string().repeat(64),
            revision_method: crate::workflow_workspace::SNAPSHOT_METHOD.into(),
            derived_from: base.map(Box::new),
        };
        // `prior`: a new revision of a draft with a prior and a derived-from
        // base; otherwise an in-place entry (neither).
        let binding = |name: &str, rev: char, prior: bool| {
            let base = prior.then(|| id("coordinated-knowledge-work", 'b', None));
            let subject = id(name, rev, base);
            A15Binding {
                content_method: subject.revision_method.clone(),
                content_value: subject.revision.clone(),
                reviewed_id3: format!("draft:project:{name}@{}", subject.revision),
                reviewed_content_method: subject.revision_method.clone(),
                reviewed_content_value: subject.revision.clone(),
                prior: prior.then(|| id(name, 'p', None)),
                subject,
            }
        };
        let bound = |bindings: Vec<A15Binding>| BoundReview {
            review_ref: format!("review:{}", uuid_like()),
            descriptor_id: "descriptor:x".into(),
            descriptor_kind: "a15_descriptor".into(),
            library_root: library.clone(),
            act_log: library.join(".chirality/records/acts.jsonl"),
            descriptor: json!({"disposition":"new revision"}),
            presentation: json!({}),
            bindings,
        };
        let offer = json!({"wording":"register workflow revision","scope":library.display().to_string(),
            "purpose":"make it available in the project library","answers":{"standing":STANDING},
            "offerId":format!("offer:{}", uuid_like()),"offerDigest":{"value":"d".repeat(64)},"actorRequirement":"the person"});
        let mut actor = person(Some("Ryan, accountable workflow owner"), Some("ryan"));
        actor["codexAccount"] = json!("someone.with.a.long.address@example.invalid");
        let single = a15_statement(&offer, &bound(vec![binding("coordinated-knowledge-work", 'a', true)]), &actor, &"e".repeat(64));
        let single = super::super::native_statement::bounded("A15", single).unwrap();
        assert!(single.contains("Library and scope: /private/var/folders"), "{single}");
        assert!(single.lines().any(|l| l == "p".repeat(64)), "full prior revision line:\n{single}");
        assert!(single.contains("Derived from: coordinated-knowledge-work revision bbbbbbbbbbbb"));
        let multi = |n: usize| {
            let entries = (0..n).map(|i| binding(&format!("workflow-entry-{i}"), 'a', false)).collect();
            let mut b = bound(entries);
            b.descriptor_kind = "a15_multi_descriptor".into();
            b.descriptor = json!({"disposition":"in place"});
            super::super::native_statement::bounded("A15", a15_statement(&offer, &b, &actor, &"e".repeat(64)))
        };
        // With this long library path, two in-place entries fit; a third is
        // refused whole with its cause (the person registers fewer per act).
        let fits = (2..=12).take_while(|n| multi(*n).is_ok()).count() + 1;
        assert_eq!(fits, 2, "entries that fit at this library path");
        assert!(multi(fits + 1).unwrap_err().contains("exceeds the readable native confirmation"));
    }
    fn uuid_like() -> String {
        "01234567-89ab-4cde-8f01-23456789abcd".into()
    }
    fn facts() -> (Value, Value) {
        (
            person(Some("Synthetic test person"), Some("fixture-os")),
            json!({"fixture":"synthetic owning context"}),
        )
    }
    #[test]
    fn native_adapter_only_explicit_register_captures_and_sees_bounded_statement() {
        use tauri_plugin_dialog::MessageDialogResult as R;
        for result in [R::Custom("Cancel".into()), R::Cancel, R::Ok, R::Yes, R::No, R::Custom("register".into())] {
            let (root, session) = library(&["sample"], false);
            let mut ac = ActControl::new(&root);
            let offer = ac.compose_a15(&session.current().unwrap()).unwrap();
            let mut shown = String::new();
            let out = crate::a15_native::synthetic_a15_native(&mut ac, &session, &offer, || Ok(facts()), |text| {
                shown = text;
                result
            })
            .unwrap();
            assert!(out.is_none());
            assert!(shown.lines().count() <= super::super::native_statement::MAX_LINES);
            assert!(shown.contains("Cancel closes without an act"));
            assert_eq!(ac.a15_offers[offer.id()].state, OfferState::Dismissed);
            assert!(ac.native_captures.is_empty());
            assert!(!storage::library_log(&root).exists());
            assert!(!root.join(CAPTURE_STORE).exists() || std::fs::read_dir(root.join(CAPTURE_STORE)).unwrap().next().is_none());
            std::fs::remove_dir_all(root).unwrap();
        }
        let (root, session) = library(&["sample"], false);
        let mut ac = ActControl::new(&root);
        let offer = ac.compose_a15(&session.current().unwrap()).unwrap();
        let out = crate::a15_native::synthetic_a15_native(&mut ac, &session, &offer, || Ok(facts()), |_| {
            R::Custom(crate::a15_native::REGISTER.into())
        })
        .unwrap();
        assert!(matches!(out, Some(HotA15Result::Recorded(_))));
        assert_eq!(records::read_log(&storage::library_log(&root)).0.len(), 1);
        std::fs::remove_dir_all(root).unwrap();
        // The act label stays out of the cancel slot, which the dialog plugin
        // also returns for an unmatched or aborted modal result.
        assert!(matches!(crate::a15_native::a15_buttons(),
            tauri_plugin_dialog::MessageDialogButtons::OkCancelCustom(ok, cancel)
                if ok == crate::a15_native::REGISTER && cancel == "Cancel"));
    }
    #[test]
    fn over_long_statement_is_refused_before_presentation_with_its_cause() {
        let names = ["one", "two", "three", "four", "five", "six", "seven"];
        let (root, session) = library(&names, true);
        let mut ac = ActControl::new(&root);
        let offer = ac.compose_a15(&session.current().unwrap()).unwrap();
        let mut called = false;
        let err = crate::a15_native::synthetic_a15_native(&mut ac, &session, &offer, || Ok(facts()), |_| {
            called = true;
            tauri_plugin_dialog::MessageDialogResult::Custom(crate::a15_native::REGISTER.into())
        })
        .err()
        .unwrap();
        assert!(!called, "an over-long statement is never presented");
        assert!(err.contains("exceeds the readable native confirmation") && err.contains("nothing captured"), "{err}");
        assert!(ac.frozen_a15_offer_digest(&offer).is_err(), "not frozen, not presented");
        assert_eq!(ac.a15_offers[offer.id()].state, OfferState::Composed);
        assert!(ac.native_captures.is_empty());
        assert!(!storage::library_log(&root).exists());
        std::fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn capture_still_requires_the_frozen_offer_and_the_named_review_digest() {
        // The digest named in the statement is checked at capture; a review
        // that differs from it captures nothing, as a stale review always has.
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        let named = ac.a15_offers[offer.id()].review_digest.clone().unwrap();
        assert_eq!(named, review_digest(session.current().unwrap().review_presentation()).unwrap());
        ac.a15_offers.get_mut(offer.id()).unwrap().review_digest = Some("0".repeat(64));
        let refused = ac.confirm_a15_after_native_event(
            &offer,
            event(&offer, digest, actor, context),
            &session.current().unwrap(),
        );
        assert!(refused.err().unwrap().contains("nothing captured"));
        assert_eq!(ac.a15_offers[offer.id()].state, OfferState::Stale);
        assert!(ac.native_captures.is_empty());
        assert!(!storage::library_log(&root).exists());
        std::fs::remove_dir_all(root).unwrap();
        // A review changed after the statement was shown still refuses:
        // synthetic_retained_old_view_rechecks_live_freshness_before_capture.
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
    #[test]
    fn synthetic_capture_lock_failure_retains_original_event_for_once_only_hot_retry() {
        let (root, session) = library(&["sample"], false);
        let (mut ac, offer, actor, context, digest) = ready(&root, &session);
        let lock_path = root.join(CAPTURE_STORE).join(".capture.lock");
        std::fs::create_dir_all(&lock_path).unwrap(); // actual open fails: lock is a directory
        let pending = ac.confirm_a15_after_native_event(
            &offer, event(&offer, digest, actor, context), &session.current().unwrap());
        assert!(matches!(pending, Ok(HotA15Result::RecordPending { .. })),
            "confirmed native event must remain original hot pending after capture-lock failure");
        assert_eq!(ac.native_captures.len(), 1);
        let original = ac.native_captures.values().next().unwrap().capture.clone();
        assert!(ac.native_captures.values().next().unwrap().pending.is_none(),
            "no writer identity reserved before original capture publication");
        assert!(!storage::library_log(&root).exists());
        std::fs::remove_dir(&lock_path).unwrap();
        let HotA15Result::Recorded(receipt) = ac.continue_a15(&offer).unwrap() else {
            panic!("must finish original event after repairing lock path")
        };
        assert_eq!(receipt.capture_id(), original["captureId"].as_str().unwrap());
        assert_eq!(receipt.witness.original_capture, original);
        assert_eq!(receipt.witness.durable_record["observedAt"], original["capturedAt"]);
        assert!(matches!(ac.continue_a15(&offer).unwrap(), HotA15Result::AlreadyTransferred { .. }));
        let (lines, limits) = records::read_log(&storage::library_log(&root));
        assert!(limits.is_empty());
        assert_eq!(lines.iter().filter(|r| r["kind"] == "human_act").count(), 1);
        std::fs::remove_dir_all(root).unwrap();
    }

}
