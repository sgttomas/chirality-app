//! NIR AT-1/2/3/9 producer only: native-selected source -> prepared text input.
//! No persistence, dispatch, supplier receipt, provider adoption or workflow run.
use crate::schema_validation::compile_targets;
use crate::util::{opaque_id, sha256_hex, FILE_IDENTITY_METHOD};
use jsonschema::Validator;
use serde_json::{json, Value};
use std::collections::HashSet;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

pub const TEXT_FILE_BOUND: usize = 262_144;
pub const SUPPLY_SCHEMA_ID: &str =
    "urn:chirality:app-v4:del-01-04:nir:attachment-supply-record:0.2";
pub const SUPPLY_SCHEMA: &str =
    include_str!("../resources/attachments/nir.attachment-supply-record.schema.json");
const DRAFT_STANDING: &str =
    "draft — not a registered workflow; this conversation is not a workflow run";

pub struct SupplyValidator(Validator);
impl SupplyValidator {
    pub fn from_schema(schema: &str) -> Result<Self, String> {
        let mut validators = compile_targets(
            &[("nir.attachment-supply-record.schema.json", schema)],
            &[SUPPLY_SCHEMA_ID],
            &[SUPPLY_SCHEMA_ID],
        )?;
        Ok(Self(validators.remove(0)))
    }
    pub fn validate(&self, record: &Value) -> Result<(), String> {
        self.0
            .validate(record)
            .map_err(|e| format!("attachment supply schema refused: {e}"))
    }
}
pub fn validate_supply(record: &Value) -> Result<(), String> {
    static VALIDATOR: OnceLock<Result<SupplyValidator, String>> = OnceLock::new();
    VALIDATOR
        .get_or_init(|| SupplyValidator::from_schema(SUPPLY_SCHEMA))
        .as_ref()
        .map_err(Clone::clone)?
        .validate(record)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum HoldReason {
    Unreadable,
    SourceMismatch,
    ContentChanged,
    TextCarrierUnavailable,
    SupplierPathUnavailable,
    InvalidSubmission,
    NonconformantRecord,
}
#[derive(Clone, Debug)]
pub struct AttachmentHold {
    pub reason: HoldReason,
    pub message: String,
    pub native_path: Value,
    pub display_path: String,
}
impl AttachmentHold {
    fn at(path: &Path, reason: HoldReason, message: impl Into<String>) -> Self {
        Self {
            reason,
            message: message.into(),
            native_path: native_path_identity(path),
            display_path: path.to_string_lossy().into_owned(),
        }
    }
}

/// A lossless tagged identity. Display text is never accepted as a dispatch path.
pub fn native_path_identity(path: &Path) -> Value {
    #[cfg(unix)]
    {
        use std::os::unix::ffi::OsStrExt;
        json!({"encoding":"unix_bytes", "bytes":path.as_os_str().as_bytes()})
    }
    #[cfg(windows)]
    {
        use std::os::windows::ffi::OsStrExt;
        let units: Vec<u16> = path.as_os_str().encode_wide().collect();
        json!({"encoding":"windows_utf16", "codeUnits":units})
    }
    #[cfg(not(any(unix, windows)))]
    {
        json!({"encoding":"native_encoded_bytes", "platform":std::env::consts::OS,
            "bytes":path.as_os_str().as_encoded_bytes()})
    }
}
fn identity(bytes: &[u8]) -> Value {
    json!({"method":FILE_IDENTITY_METHOD,"value":sha256_hex(bytes)})
}
struct TextSnapshot {
    text: String,
    identity: Value,
    byte_length: usize,
}
fn read_snapshot(path: &Path) -> Result<TextSnapshot, AttachmentHold> {
    // Read at most bound+1: over-limit content is held, never hashed as a full file.
    // Descriptor-based regular-source check, after a nonblocking Unix open.
    // Pre-open pathname metadata alone would race replacement by a FIFO.
    let mut options = std::fs::OpenOptions::new();
    options.read(true);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        options.custom_flags(libc::O_NONBLOCK | libc::O_NOCTTY);
    }
    let file = options.open(path).map_err(|e| {
        AttachmentHold::at(
            path,
            HoldReason::Unreadable,
            format!("file unreadable; confirm current source or remove: {e}"),
        )
    })?;
    let metadata = file.metadata().map_err(|e| {
        AttachmentHold::at(
            path,
            HoldReason::Unreadable,
            format!("opened source metadata unavailable; confirm source or remove: {e}"),
        )
    })?;
    if !metadata.file_type().is_file() {
        return Err(AttachmentHold::at(
            path,
            HoldReason::Unreadable,
            "opened source is not a regular file; confirm a regular source or remove; nothing sent",
        ));
    }
    let mut bytes = Vec::new();
    file.take((TEXT_FILE_BOUND + 1) as u64)
        .read_to_end(&mut bytes)
        .map_err(|e| {
            AttachmentHold::at(
                path,
                HoldReason::Unreadable,
                format!("file read failed; confirm current source or remove: {e}"),
            )
        })?;
    if bytes.len() > TEXT_FILE_BOUND {
        return Err(AttachmentHold::at(path, HoldReason::TextCarrierUnavailable,
            "text carrier exceeds 262144 original file bytes; confirm another carrier or remove; nothing sent"));
    }
    if bytes.contains(&0) {
        return Err(AttachmentHold::at(path, HoldReason::TextCarrierUnavailable,
            "text carrier unavailable: NUL-bearing file; confirm another carrier or remove; nothing sent"));
    }
    // Both identity and decoded text come from this exact bounded buffer.
    let content = identity(&bytes);
    let byte_length = bytes.len();
    let text = String::from_utf8(bytes).map_err(|_| AttachmentHold::at(path,
        HoldReason::TextCarrierUnavailable,
        "text carrier unavailable: file is not UTF-8; confirm another carrier or remove; nothing sent"))?;
    Ok(TextSnapshot {
        text,
        identity: content,
        byte_length,
    })
}

/// WR owns the supplied draft reference; this producer does not register/trial it.
#[derive(Clone, Debug)]
pub struct DraftTrialReference {
    location: String,
    name: String,
    content: Value,
    /// WR draft key's `draft_root`, set by the WR source owner (TT-4 pointer
    /// key only). Never emitted in the NIR supply record, whose `draft`
    /// element has exactly {location, name, content, standing}.
    root: Option<String>,
}
impl DraftTrialReference {
    pub fn new(location: &str, name: &str, content: Value) -> Result<Self, String> {
        if !matches!(location, "project" | "user")
            || name.is_empty()
            || content.as_object().map(|o| o.len()) != Some(2)
            || content["method"].as_str().is_none_or(str::is_empty)
            || content["value"].as_str().is_none_or(str::is_empty)
        {
            return Err("invalid owning WR draft reference; no trial/registration inferred".into());
        }
        Ok(Self {
            location: location.into(),
            name: name.into(),
            content,
            root: None,
        })
    }
    /// The WR source owner names the drafts folder the draft was read from.
    pub fn with_root(mut self, root: &str) -> Self {
        self.root = Some(root.into());
        self
    }
    /// WR `draft_key` and draft content identity for a TT-4 trial pointer;
    /// `None` when the WR source owner did not name the drafts folder.
    pub fn trial_key(&self) -> Option<(Value, Value)> {
        let root = self.root.as_ref()?;
        Some((
            json!({"draft_location":self.location,"draft_root":root,"name":self.name}),
            self.content.clone(),
        ))
    }
    fn record(&self) -> Value {
        json!({"location":self.location,"name":self.name,"content":self.content,"standing":DRAFT_STANDING})
    }
}

/// Opaque host-owned selection; no deserialization or display-path reconstruction.
#[derive(Clone, Debug)]
pub struct SelectedTextAttachment {
    path: PathBuf,
    selection_ref: String,
    display_name: String,
    selected_identity: Value,
    draft: Option<DraftTrialReference>,
}
impl SelectedTextAttachment {
    /// Caller must be the integrating native picker/WR source owner, not an IPC path.
    pub fn from_native_selection(
        path: PathBuf,
        draft: Option<DraftTrialReference>,
    ) -> Result<Self, AttachmentHold> {
        if !path.is_absolute() || path.to_str().is_none() {
            return Err(AttachmentHold::at(&path, HoldReason::SupplierPathUnavailable,
                "selected native path is not an absolute supplier-representable string; remove or choose a representable source"));
        }
        let name = path
            .file_name()
            .and_then(|n| n.to_str())
            .filter(|n| !n.is_empty())
            .ok_or_else(|| {
                AttachmentHold::at(
                    &path,
                    HoldReason::SupplierPathUnavailable,
                    "selected native file name unavailable; no lossy alternate source",
                )
            })?
            .to_owned();
        let lower = name.to_ascii_lowercase();
        if [".png", ".jpg", ".jpeg", ".gif", ".webp"]
            .iter()
            .any(|suffix| lower.ends_with(suffix))
        {
            return Err(AttachmentHold::at(&path, HoldReason::TextCarrierUnavailable,
                "selected file uses the image carrier; text producer does not silently substitute it"));
        }
        let snapshot = read_snapshot(&path)?;
        let selection_ref = opaque_id("selected-attachment:")
            .map_err(|e| AttachmentHold::at(&path, HoldReason::InvalidSubmission, e))?;
        let display_name = match &draft {
            Some(d) => format!("{name} (draft {})", d.name),
            None => name,
        };
        Ok(Self {
            path,
            selection_ref,
            display_name,
            selected_identity: snapshot.identity,
            draft,
        })
    }
    pub fn selection_ref(&self) -> &str {
        &self.selection_ref
    }
    /// The WR draft this selection belongs to (AT-8), if any.
    pub fn draft(&self) -> Option<&DraftTrialReference> {
        self.draft.as_ref()
    }
    /// The private source path, for the host-side list that retains it.
    pub(crate) fn source_path(&self) -> &Path {
        &self.path
    }
    pub fn native_path(&self) -> Value {
        native_path_identity(&self.path)
    }
    pub fn snapshot(&self) -> Value {
        json!({"selectionRef":self.selection_ref,"nativePath":self.native_path(),
            "displayPath":self.path.to_string_lossy(),"displayName":self.display_name,
            "identityAtSelection":self.selected_identity,"carrier":"text-element",
            "standing":"selected; not sent","draft":self.draft.as_ref().map(DraftTrialReference::record)})
    }
    /// Require the exact selected native identity, never an echoed lossy display.
    pub fn prepare_for_source(
        &self,
        claimed_native_path: &Value,
        submission_ref: &str,
        recorded_at: &str,
    ) -> Result<PreparedTextAttachment, AttachmentHold> {
        if *claimed_native_path != self.native_path() {
            return Err(AttachmentHold::at(&self.path, HoldReason::SourceMismatch,
                "source differs from native selection; confirm current source or remove; nothing prepared"));
        }
        valid_submission(submission_ref)
            .map_err(|e| AttachmentHold::at(&self.path, HoldReason::InvalidSubmission, e))?;
        let observed = read_snapshot(&self.path)?;
        if observed.identity != self.selected_identity {
            return Err(AttachmentHold::at(
                &self.path,
                HoldReason::ContentChanged,
                "content changed since selected; confirm current content or remove; nothing sent",
            ));
        }
        let path = self
            .path
            .to_str()
            .expect("selection retained an exact Unicode path");
        // JSON quoting protects framing from path/name controls; it never rewrites bytes.
        let quoted_name = serde_json::to_string(&self.display_name).unwrap();
        let quoted_path = serde_json::to_string(path).unwrap();
        let digest = observed.identity["value"].as_str().unwrap();
        let element = format!("[Chirality] Attached file {quoted_name} ({quoted_path}; content {}). Its bytes follow this line.\n{}",
            &digest[..12], observed.text);
        let attachment_id = opaque_id("att:")
            .map_err(|e| AttachmentHold::at(&self.path, HoldReason::InvalidSubmission, e))?;
        let mut record = json!({"format":"chirality.nir.attachment-supply","formatVersion":"0.2",
            "attachmentId":attachment_id,"displayName":self.display_name,"suppliedAs":"text-element",
            "supplyStanding":"supplied","localPath":path,"identityAtSelection":self.selected_identity,
            "identityAtSubmission":observed.identity,"byteLength":observed.byte_length,
            "elementIdentity":{"method":"sha256 over UTF-8 text","value":sha256_hex(element.as_bytes())},
            "turnRef":submission_ref,"recordedAt":recorded_at,
            "supplierRead":"not applicable: the bytes are in the turn's own text element",
            "providerAdoption":"not observed"});
        if let Some(draft) = &self.draft {
            record["draft"] = draft.record();
        }
        validate_supply(&record)
            .map_err(|e| AttachmentHold::at(&self.path, HoldReason::NonconformantRecord, e))?;
        Ok(PreparedTextAttachment {
            native_input: json!({"type":"text","text":element,"text_elements":[]}),
            supply_record: record,
            source_identity: self.native_path(),
            selection_ref: self.selection_ref.clone(),
        })
    }
}
fn valid_submission(reference: &str) -> Result<(), String> {
    let token = reference
        .strip_prefix("submission:")
        .ok_or("App submission reference required; never a native turn ID")?;
    uuid::Uuid::parse_str(token)
        .map_err(|_| "submission reference needs an opaque UUID".to_string())?;
    Ok(())
}
pub fn new_submission_ref() -> Result<String, String> {
    opaque_id("submission:")
}

#[derive(Clone, Debug)]
pub struct PreparedTextAttachment {
    native_input: Value,
    supply_record: Value,
    source_identity: Value,
    selection_ref: String,
}
impl PreparedTextAttachment {
    pub fn native_input(&self) -> &Value {
        &self.native_input
    }
    pub fn supply_record(&self) -> &Value {
        &self.supply_record
    }
    pub fn supply_ref(&self) -> String {
        format!(
            "attachment:{}",
            self.supply_record["attachmentId"].as_str().unwrap()
        )
    }
    pub fn source_identity(&self) -> &Value {
        &self.source_identity
    }
    pub fn selection_ref(&self) -> &str {
        &self.selection_ref
    }
}
#[derive(Clone, Debug)]
pub struct PreparedAttachmentList {
    submission_ref: String,
    entries: Vec<PreparedTextAttachment>,
}
impl PreparedAttachmentList {
    pub fn submission_ref(&self) -> &str {
        &self.submission_ref
    }
    pub fn entries(&self) -> &[PreparedTextAttachment] {
        &self.entries
    }
    pub fn supply_refs(&self) -> Vec<String> {
        self.entries
            .iter()
            .map(PreparedTextAttachment::supply_ref)
            .collect()
    }
    pub fn native_inputs(&self) -> Vec<Value> {
        self.entries
            .iter()
            .map(|a| a.native_input.clone())
            .collect()
    }
    pub fn supply_records(&self) -> Vec<Value> {
        self.entries
            .iter()
            .map(|a| a.supply_record.clone())
            .collect()
    }
    pub fn preparation_standing(&self) -> &'static str {
        "prepared; not persisted or sent"
    }
}
/// All-or-nothing preparation. The integrating owner must durably record every
/// member and the ordered HOSTING association before its actual pipe write.
pub fn prepare_ordered(
    selections: &[SelectedTextAttachment],
    submission_ref: &str,
    recorded_at: &str,
) -> Result<PreparedAttachmentList, AttachmentHold> {
    if selections.is_empty() {
        return Err(AttachmentHold::at(
            Path::new(""),
            HoldReason::InvalidSubmission,
            "attachment selection list is empty",
        ));
    }
    let mut seen = HashSet::new();
    let mut entries = Vec::new();
    for selection in selections {
        if !seen.insert(selection.selection_ref()) {
            return Err(AttachmentHold::at(
                &selection.path,
                HoldReason::InvalidSubmission,
                "selected attachment repeats in list; confirm list or remove",
            ));
        }
        entries.push(selection.prepare_for_source(
            &selection.native_path(),
            submission_ref,
            recorded_at,
        )?);
    }
    Ok(PreparedAttachmentList {
        submission_ref: submission_ref.into(),
        entries,
    })
}
