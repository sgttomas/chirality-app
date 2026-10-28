//! Read-only App intake of person-selected external host documents.
//! C CI-1/CI-3, §5.2/5.5 and RR-1…4; ADAPTER RD-1…3; PANEL H-5/H-6.
//! The caller owns the native file-selection boundary. This module reads each
//! selected path once, retains bytes in memory, and creates no dispatch, native
//! event mapping, durable copy, host identity, act or qualification evidence.
use crate::catalog::{BoundRead, Catalog, ReadObservation};
use crate::receiving::{compare_panel, PanelComparison};
use serde_json::{json, Value};
use std::path::PathBuf;

#[derive(Clone, Debug)]
pub struct SelectedPaths {
    pub catalog: PathBuf,
    pub read: PathBuf,
    pub counterpart: Option<PathBuf>,
}
#[derive(Clone, Debug)]
pub struct DocumentEvidence {
    path: PathBuf,
    bytes: Option<Vec<u8>>,
    document: Option<Value>,
    assessment: &'static str,
    reason: Option<String>,
}
impl DocumentEvidence {
    fn load(path: PathBuf) -> Self {
        match std::fs::read(&path) {
            Err(error) => Self { path, bytes: None, document: None, assessment: "unavailable", reason: Some(error.to_string()) },
            Ok(bytes) => {
                let parsed = serde_json::from_slice(&bytes);
                let (document, assessment, reason) = match parsed {
                    Ok(document) => (Some(document), "not_assessed", None),
                    Err(error) => (None, "malformed", Some(format!("malformed JSON: {error}"))),
                };
                Self { path, bytes: Some(bytes), document, assessment, reason }
            }
        }
    }
    pub fn selected_path(&self) -> &std::path::Path { &self.path }
    pub fn original_bytes(&self) -> Option<&[u8]> { self.bytes.as_deref() }
    pub fn original_document(&self) -> Option<&Value> { self.document.as_ref() }
    pub fn assessment(&self) -> &str { self.assessment }
    pub fn reason(&self) -> Option<&str> { self.reason.as_deref() }
    fn refuse(&mut self, assessment: &'static str, reason: String) {
        self.assessment = assessment; self.reason = Some(reason);
    }
    fn snapshot(&self) -> Value {
        json!({"selectedPath": native_path_identity(&self.path),
            "displayPath": self.path.to_string_lossy(),
            "pathDisplayLimit": if self.path.to_str().is_some() { None } else { Some("native path is not Unicode; display is lossy; use selectedPath for identity") },
            "assessment": self.assessment,
            "reason": self.reason, "originalDocument": self.document,
            "originalBytes": self.bytes})
    }
}
#[derive(Clone, Debug)]
pub struct ExternalObservation {
    catalog_evidence: DocumentEvidence,
    read_evidence: DocumentEvidence,
    counterpart_evidence: Option<DocumentEvidence>,
    catalog: Option<Catalog>,
    read: Option<ReadObservation>,
    counterpart: Option<ReadObservation>,
}
impl ExternalObservation {
    /// Only paths returned by the integrating native selector belong here.
    /// Source claims remain person-supplied/unverified even after conformity.
    pub fn load(selected: SelectedPaths) -> Self {
        let mut catalog_evidence = DocumentEvidence::load(selected.catalog);
        let mut read_evidence = DocumentEvidence::load(selected.read);
        let mut counterpart_evidence = selected.counterpart.map(DocumentEvidence::load);
        let catalog = match catalog_evidence.original_bytes() {
            Some(bytes) => match Catalog::receive(bytes) {
                Ok(catalog) => { catalog_evidence.assessment = "received"; Some(catalog) }
                Err(reason) => {
                    if catalog_evidence.assessment != "malformed" { catalog_evidence.refuse("invalid", reason); }
                    None
                }
            },
            None => None,
        };
        let read = receive_read(catalog.as_ref(), &mut read_evidence);
        let counterpart = counterpart_evidence.as_mut().and_then(|e| receive_read(catalog.as_ref(), e));
        Self { catalog_evidence, read_evidence, counterpart_evidence, catalog, read, counterpart }
    }
    pub fn catalog_evidence(&self) -> &DocumentEvidence { &self.catalog_evidence }
    pub fn read_evidence(&self) -> &DocumentEvidence { &self.read_evidence }
    pub fn counterpart_evidence(&self) -> Option<&DocumentEvidence> { self.counterpart_evidence.as_ref() }
    pub fn bound_read(&self) -> Option<&BoundRead> {
        match &self.read { Some(ReadObservation::Success(read)) => Some(read), _ => None }
    }
    /// All meaningful source content remains in originalDocument. This snapshot
    /// supplies display accounting, never a summary or stronger host standing.
    pub fn snapshot(&self) -> Value {
        let read = self.bound_read();
        let reported_currency = read.map(|r| r.document()["standing"]["currency"].clone());
        let counterpart = match &self.counterpart { Some(ReadObservation::Success(r)) => Some(r), _ => None };
        let comparison = match (read, self.counterpart_evidence.as_ref(), counterpart) {
            (_, None, _) => "host_table_not_supplied",
            (None, _, _) => "comparison_not_established_primary_read",
            (_, Some(_), None) => "comparison_not_established_counterpart",
            (Some(read), _, Some(host)) => match compare_panel(read, Some(host)) {
                PanelComparison::SameMeaningfulContent => "same_meaningful_supplied_content",
                PanelComparison::DifferentMeaningfulContent => "different_meaningful_supplied_content",
                PanelComparison::HostTableNotSupplied => "host_table_not_supplied",
            },
        };
        json!({
            "provenance": "person-supplied document; host origin unverified",
            "hostOrigin": "unverified", "qualification": "not_established",
            "dispatch": "none", "comparisonScope": "supplied_documents_only",
            "reportedCurrency": reported_currency,
            "currencyMeaning": "as reported in this observation",
            "basisCitationAssessment": read.map(|r| if r.citable {"complete_as_supplied"} else {"incomplete"}),
            "evidenceLimits": read.map(|r| r.limits.clone()).unwrap_or_default(),
            "catalog": self.catalog_evidence.snapshot(), "read": self.read_evidence.snapshot(),
            "counterpart": self.counterpart_evidence.as_ref().map(DocumentEvidence::snapshot),
            "comparison": comparison,
            "catalogIdentity": self.catalog.as_ref().map(|c| json!({"host":c.document()["host_identity"],"edition":c.document()["edition"]})),
        })
    }
}
fn receive_read(catalog: Option<&Catalog>, evidence: &mut DocumentEvidence) -> Option<ReadObservation> {
    if evidence.assessment == "malformed" || evidence.bytes.is_none() { return None; }
    let Some(catalog) = catalog else {
        evidence.refuse("prerequisite_unavailable", "catalog not received; read conformity not established".into());
        return None;
    };
    match catalog.receive_read(evidence.original_bytes().unwrap()) {
        Ok(observation) => { evidence.assessment = "received"; Some(observation) }
        Err(reason) => { evidence.refuse("invalid", reason); None }
    }
}

/// Native path identity is distinct from its human-readable display. Never
/// serialize PathBuf through serde (it rejects non-Unicode native paths), and
/// never use the lossy display string as the selected-file identity.
fn native_path_identity(path: &std::path::Path) -> Value {
    #[cfg(unix)] {
        use std::os::unix::ffi::OsStrExt;
        json!({"encoding":"unix_bytes", "bytes":path.as_os_str().as_bytes()})
    }
    #[cfg(windows)] {
        use std::os::windows::ffi::OsStrExt;
        let units: Vec<u16> = path.as_os_str().encode_wide().collect();
        json!({"encoding":"windows_utf16", "codeUnits":units})
    }
    #[cfg(not(any(unix, windows)))] {
        json!({"encoding":"native_encoded_bytes", "platform":std::env::consts::OS,
            "bytes":path.as_os_str().as_encoded_bytes()})
    }
}
