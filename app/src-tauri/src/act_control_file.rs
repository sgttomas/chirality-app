//! App-content A4/A6/A7 standing capture. No record/renderer/native-flag admission.
use super::*;
#[path = "file_act_native.rs"]
mod native;
pub(crate) use native::confirm_file_native;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum FileActKind {
    Check,
    Approve,
    Rely,
}
impl FileActKind {
    pub(crate) fn code(self) -> &'static str {
        match self {
            Self::Check => "A4",
            Self::Approve => "A6",
            Self::Rely => "A7",
        }
    }
    pub(crate) fn wording(self) -> &'static str {
        match self {
            Self::Check => "mark checked",
            Self::Approve => "approve (engineering approval)",
            Self::Rely => "rely (professional reliance)",
        }
    }
    fn requirement(self) -> &'static str {
        match self {
            Self::Check => "the person",
            Self::Approve => "the accountable person",
            Self::Rely => "the accountable professional (the person's own statement; not verified)",
        }
    }
}
/// Owning reference, not deserializable. Root retains it; renderer receives only a view.
pub(crate) struct FileActOfferRef {
    id: String,
}
impl FileActOfferRef {
    pub(crate) fn id(&self) -> &str {
        &self.id
    }
}
#[derive(Debug, PartialEq, Eq)]
enum FileActState {
    Composed,
    Presented,
    Dismissed,
    Stale,
    CaptureUncertain,
    Captured,
    Recorded,
    RecordPending,
}
pub(super) struct FileActSlot {
    root: PathBuf,
    path: PathBuf,
    bytes: Vec<u8>,
    kind: FileActKind,
    offer: Value,
    state: FileActState,
    actor: Option<Value>,
    context: Option<Value>,
    capture_id: Option<String>,
    uncertain_capture: Option<Value>,
}
impl FileActSlot {
    pub(super) fn set_recording_state(&mut self, recorded: bool) {
        self.state = if recorded {
            FileActState::Recorded
        } else {
            FileActState::RecordPending
        };
    }
}
#[cfg(test)]
thread_local! { static BEFORE_FILE_OPEN: std::cell::RefCell<Option<Box<dyn FnOnce(&Path)>>> = const { std::cell::RefCell::new(None) }; }
/// The file must be inside the physical App workspace, never a host proxy.
/// Recheck every component and the open file metadata before/after reading.
fn read_subject(root: &Path, path: &Path) -> Result<Vec<u8>, String> {
    use std::io::Read;
    use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
    if !root.is_absolute()
        || !path.is_absolute()
        || path.components().any(|c| {
            matches!(
                c,
                std::path::Component::ParentDir | std::path::Component::CurDir
            )
        })
        || !path.starts_with(root)
        || path == root
    {
        return Err("App file must be an absolute contained physical workspace file".into());
    }
    storage::check_path(root)?;
    storage::check_path(path)?;
    if std::fs::canonicalize(root).map_err(|e| e.to_string())? != root
        || std::fs::canonicalize(path).map_err(|e| e.to_string())? != path
    {
        return Err("App file/root alias refused".into());
    }
    if !std::fs::symlink_metadata(path)
        .map_err(|e| e.to_string())?
        .is_file()
    {
        return Err("App subject is not a regular file".into());
    }
    #[cfg(test)]
    BEFORE_FILE_OPEN.with(|hook| {
        if let Some(hook) = hook.borrow_mut().take() {
            hook(path);
        }
    });
    let mut file = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
        .map_err(|e| e.to_string())?;
    let before = file.metadata().map_err(|e| e.to_string())?;
    if !before.is_file() {
        return Err("App subject is not a regular file".into());
    }
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    let after = file.metadata().map_err(|e| e.to_string())?;
    storage::check_path(path)?;
    let named = std::fs::metadata(path).map_err(|e| e.to_string())?;
    let stamp = |m: &std::fs::Metadata| {
        (
            m.dev(),
            m.ino(),
            m.len(),
            m.mtime(),
            m.mtime_nsec(),
            m.ctime(),
            m.ctime_nsec(),
        )
    };
    if stamp(&before) != stamp(&after)
        || stamp(&after) != stamp(&named)
        || std::fs::canonicalize(path).map_err(|e| e.to_string())? != path
    {
        return Err("App subject changed while reading; review again".into());
    }
    Ok(bytes)
}
impl ActControl {
    /// Caller selects App content. Selection/compose confers no human-act authority.
    /// This bounded first path is standing only; no arrival/request is invented.
    pub(crate) fn compose_file_act(
        &mut self,
        path: &Path,
        kind: FileActKind,
        scope: &str,
        purpose: &str,
    ) -> Result<FileActOfferRef, String> {
        if scope.trim().is_empty() || purpose.trim().is_empty() {
            return Err("Explicit scope and purpose are required".into());
        }
        let bytes = read_subject(&self.workspace, path)?;
        let id = crate::util::opaque_id("offer:")?;
        let mut offer = json!({"format":"chirality.aac.offer","formatVersion":"0.3","offerId":id,
            "actKind":kind.code(),"wording":kind.wording(),"subject":{"class":"App file","ref":path.to_str().ok_or("App file path is not UTF-8")?,"contentIdentity":{"method":FILE_IDENTITY_METHOD,"value":crate::util::sha256_hex(&bytes)}},
            "scope":scope,"purpose":purpose,"actorRequirement":kind.requirement(),"declineAvailable":true,
            "answers":{"standing":STANDING},"composedAt":capture_time()});
        offer["offerDigest"] = json!({"method":OFFER_DIGEST_METHOD,"value":offer_digest(&offer)?});
        crate::schema_validation::validate_offer(&offer)?;
        self.file_offers.insert(
            id.clone(),
            FileActSlot {
                root: self.workspace.clone(),
                path: path.to_path_buf(),
                bytes,
                kind,
                offer,
                state: FileActState::Composed,
                actor: None,
                context: None,
                capture_id: None,
                uncertain_capture: None,
            },
        );
        Ok(FileActOfferRef { id })
    }
    /// Immutable original bytes for the consuming file preview; never reread an
    /// unrelated current file and label it the offered content.
    pub(crate) fn file_act_preview(
        &self,
        reference: &FileActOfferRef,
    ) -> Result<(&Value, &[u8]), String> {
        let slot = self
            .file_offers
            .get(&reference.id)
            .ok_or("File act offer absent")?;
        Ok((&slot.offer, &slot.bytes))
    }
    fn freeze_file_native(
        &mut self,
        reference: &FileActOfferRef,
        actor: &Value,
        context: &Value,
    ) -> Result<(String, Value, FileActKind), String> {
        let slot = self
            .file_offers
            .get_mut(&reference.id)
            .ok_or("File act offer absent")?;
        if slot.state != FileActState::Composed || slot.root != self.workspace {
            return Err("File act is not a current unpresented offer".into());
        }
        if actor["identityVerified"] != false
            || actor["osAccount"].as_str().is_none_or(|s| s.is_empty())
        {
            return Err("Observed OS actor with identity not verified required".into());
        }
        if read_subject(&slot.root, &slot.path)? != slot.bytes {
            slot.state = FileActState::Stale;
            return Err("File content changed; review again".into());
        }
        let statement=match slot.kind {
            FileActKind::Check=>"Choosing mark checked records that act only.",
            FileActKind::Approve=>"Choosing approve is your statement that you are the accountable person. It records engineering approval only.",
            FileActKind::Rely=>"Choosing rely is your own statement that you are the accountable professional. Professional standing is not verified; no certification is inferred.",
        };
        let text=format!("{}\n\nApp file: {}\nContent identity: {}\nScope: {}\nPurpose: {}\nActor requirement: {}\nActor (identity not verified): {}\n{}\n\n{}\nDecline records only a decline of this kind; Cancel records nothing.",slot.kind.wording(),slot.offer["subject"]["ref"],slot.offer["subject"]["contentIdentity"],slot.offer["scope"],slot.offer["purpose"],slot.kind.requirement(),actor,STANDING,statement);
        // Bound native text; do not silently truncate a confirmation surface.
        if text.len() > 24_000 {
            return Err(
                "File act confirmation exceeds native display budget; nothing presented".into(),
            );
        }
        slot.actor = Some(actor.clone());
        slot.context = Some(context.clone());
        slot.state = FileActState::Presented;
        Ok((text, slot.offer["offerDigest"].clone(), slot.kind))
    }
    pub(crate) fn dismiss_file_act(&mut self, reference: &FileActOfferRef) {
        if let Some(slot) = self.file_offers.get_mut(&reference.id) {
            if matches!(slot.state, FileActState::Composed | FileActState::Presented) {
                slot.state = FileActState::Dismissed;
            }
        }
    }
    fn consume_file_event(
        &mut self,
        reference: &FileActOfferRef,
        event: native::ConfirmedFileEvent,
    ) -> Result<Value, String> {
        let slot = self
            .file_offers
            .get_mut(&reference.id)
            .ok_or("File act offer absent")?;
        if slot.state != FileActState::Presented || slot.root != self.workspace {
            return Err("File act not presented, stale owner or already captured".into());
        }
        if event.id() != reference.id
            || event.digest() != &slot.offer["offerDigest"]
            || slot.actor.as_ref() != Some(event.actor())
            || slot.context.as_ref() != Some(event.context())
            || offer_digest(&slot.offer)? != event.digest()["value"].as_str().unwrap_or("")
        {
            return Err("Native event differs from original offer/actor/context".into());
        }
        match read_subject(&slot.root, &slot.path) {
            Ok(bytes) if bytes == slot.bytes => {}
            _ => {
                slot.state = FileActState::Stale;
                return Err(
                    "File subject changed/unavailable after confirmation; nothing captured".into(),
                );
            }
        }
        let id = crate::util::opaque_id("cap:")?;
        let mut limits = vec!["identity not verified"];
        if slot.kind == FileActKind::Rely && event.choice() == "act" {
            limits.push("professional standing is the person's own statement; not verified");
        }
        let capture = json!({"format":"chirality.aac.capture-evidence","formatVersion":"0.3","captureId":id,"offerId":reference.id,
            "offerDigest":slot.offer["offerDigest"],"choice":event.choice(),"actKind":slot.kind.code(),"actor":event.actor(),
            "boundSubject":[slot.offer["subject"]["ref"]],"boundContent":[slot.offer["subject"]["contentIdentity"]],
            "scope":slot.offer["scope"],"purpose":slot.offer["purpose"],"capturedAt":capture_time(),"surface":"App interface","inputSource":"host-native-confirmation",
            "answers":slot.offer["answers"],"evidenceLimits":limits});
        crate::schema_validation::validate_capture(&capture)?;
        // The native event is not itself an admitted capture. Definite failure
        // before publication means nothing captured (AAC 4.1 step 6).
        let root = slot.root.clone();
        slot.state = FileActState::Dismissed; // consume this confirmation even on failure
        let _lock =
            storage::lock(&root.join(CAPTURE_STORE).join(".capture.lock")).map_err(|e| {
                format!("capture failed; nothing captured; review and confirm again: {e}")
            })?;
        match storage::create_capture_json(&storage::capture_path(&root, &id), &capture) {
            Ok(()) => {}
            Err(storage::CapturePublicationFailure::DefinitelyNotPublished(error)) => {
                return Err(format!(
                    "capture failed; nothing captured; review and confirm again: {error}"
                ));
            }
            Err(storage::CapturePublicationFailure::PublicationUncertain(error)) => {
                // Keep the actual native facts but do not admit them to the writer
                // or recreate absent bytes. Reconciliation requires stored bytes.
                slot.state = FileActState::CaptureUncertain;
                slot.uncertain_capture = Some(capture);
                return Ok(
                    json!({"state":"capture publication uncertain","captureId":id,"captureDurability":"not established","recorded":false,"writeFailure":error}),
                );
            }
        }
        self.admit_file_capture(reference, capture);
        let results = self.flush_native_locked();
        results
            .into_iter()
            .find(|v| v["capture"]["captureId"] == id)
            .ok_or("Original file capture result absent".into())
    }
    fn admit_file_capture(&mut self, reference: &FileActOfferRef, capture: Value) {
        let id = capture["captureId"]
            .as_str()
            .expect("validated capture")
            .to_owned();
        let slot = self.file_offers.get_mut(&reference.id).unwrap();
        slot.state = FileActState::Captured;
        slot.capture_id = Some(id.clone());
        slot.uncertain_capture = None;
        self.file_capture_roots
            .insert(id.clone(), slot.root.clone());
        self.native_captures.insert(
            id,
            NativeCapture {
                ordinal: self.native_captures.len(),
                target_log: LOG.into(),
                a15: None,
                written: false,
                delay_pending: false,
                capture,
                pending: None,
                failure: None,
            },
        );
    }
    /// Retry only the original in-process native facts. Never admits cold claims.
    pub(crate) fn continue_file_act(
        &mut self,
        reference: &FileActOfferRef,
    ) -> Result<Value, String> {
        let slot = self
            .file_offers
            .get(&reference.id)
            .ok_or("File act offer absent")?;
        if slot.root != self.workspace {
            return Err("File act original owning root changed; no relocation".into());
        }
        let root = slot.root.clone();
        let uncertain = slot.uncertain_capture.clone();
        let admitted_id = slot.capture_id.clone();
        if uncertain.is_none() && admitted_id.is_none() {
            return Err("File act has no admitted capture; review and confirm again".into());
        }
        let _lock = storage::lock(&root.join(CAPTURE_STORE).join(".capture.lock"))?;
        let id = if let Some(original) = uncertain {
            let id = original["captureId"].as_str().unwrap().to_owned();
            let path = storage::capture_path(&root, &id);
            // No create/replace call here: uncertain absence never authorizes a
            // new publication. Compare the actual stored bytes before admission.
            let reconcile = (|| -> Result<(), String> {
                let bytes = read_subject(&root, &path)?;
                let stored: Value = serde_json::from_slice(&bytes).map_err(|e| e.to_string())?;
                if stored != original {
                    return Err("Stored capture differs from original native facts".into());
                }
                storage::sync_publication(&path)
            })();
            if let Err(error) = reconcile {
                return Ok(
                    json!({"state":"capture publication uncertain","captureId":id,"captureDurability":"not established","recorded":false,"writeFailure":error}),
                );
            }
            self.admit_file_capture(reference, original);
            id
        } else {
            admitted_id.unwrap()
        };
        let results = self.flush_native_locked();
        results
            .into_iter()
            .find(|v| v["capture"]["captureId"] == id)
            .ok_or("Original file capture result absent".into())
    }
}
pub(super) fn body(capture: &Value) -> Value {
    let evidence = json!([{"kind":"capture evidence","ref":capture["captureId"],"resolutionAtWrite":"resolved"}]);
    if capture["choice"] == "decline" {
        return json!({"actor":capture["actor"],"declinedKind":capture["actKind"],"subject":capture["boundSubject"],"time":capture["capturedAt"],"captureEvidence":evidence});
    }
    json!({"actKind":capture["actKind"],"actClass":{"value":"reserved to the person"},"decisionActor":capture["actor"],"recordingMode":"direct capture",
        "boundSubject":capture["boundSubject"],"boundContent":capture["boundContent"],"scope":capture["scope"],"purpose":capture["purpose"],
        "captureEvidence":evidence,"captureTime":capture["capturedAt"],"evidenceLimits":capture["evidenceLimits"]})
}
#[cfg(test)]
#[path = "file_act_tests.rs"]
mod tests;
