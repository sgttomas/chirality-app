//! Sealed consuming-build association and complete exact-byte artifact closure.
//! No runtime field or persisted manifest can create a trusted selection.
use super::{artifact, digest, resolve, Artifact, Selection, PRODUCTION_SELECTION};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
};
#[derive(Clone)]
pub(crate) struct Selected {
    source: PathBuf,
    source_id: (u64, u64),
    anchor: Artifact,
    files: BTreeMap<String, Vec<u8>>,
    expected: Artifact,
    attestation: Artifact,
}
fn collect(base: &Path, anchor: &Artifact) -> Result<BTreeMap<String, Vec<u8>>, String> {
    let selection: Selection =
        serde_json::from_slice(&artifact(base, anchor)?).map_err(|e| e.to_string())?;
    let expected: Value =
        serde_json::from_slice(&artifact(base, &selection.expected)?).map_err(|e| e.to_string())?;
    let attestation: Value = serde_json::from_slice(&artifact(base, &selection.attestation)?)
        .map_err(|e| e.to_string())?;
    let mut pending = vec![anchor.clone(), selection.expected, selection.attestation];
    for (value, pointers) in [
        (
            &expected,
            &[
                "/label_evidence",
                "/generation_correspondence",
                "/generated/provenance",
                "/generated/version_advance",
                "/archive/acquisition_authorization",
                "/archive/custody",
                "/archive/extraction_procedure",
            ][..],
        ),
        (
            &attestation,
            &[
                "/review_evidence",
                "/adoption/through_help_human",
                "/adoption/evidence",
            ][..],
        ),
    ] {
        for pointer in pointers {
            pending.push(
                serde_json::from_value(
                    value
                        .pointer(pointer)
                        .ok_or("declared artifact reference absent")?
                        .clone(),
                )
                .map_err(|e| e.to_string())?,
            );
        }
    }
    let mut files = BTreeMap::<String, Vec<u8>>::new();
    let mut total = 0usize;
    while let Some(reference) = pending.pop() {
        if let Some(prior) = files.get(&reference.path) {
            if digest(prior) != reference.sha256 {
                return Err("colliding source reference digest".into());
            }
            continue;
        }
        if files.len() >= 1024 {
            return Err("artifact closure member limit".into());
        }
        let raw = artifact(base, &reference)?;
        total = total
            .checked_add(raw.len())
            .ok_or("closure size overflow")?;
        if total > 32 * 1024 * 1024 {
            return Err("artifact closure byte limit".into());
        }
        // Evidence payload bytes are opaque; incidental JSON path/hash objects
        // do not declare additional dependencies or acquire authority.
        files.insert(reference.path, raw);
    }
    // File/ancestor collisions cannot be represented by a physical closure.
    for path in files.keys() {
        let mut parent = Path::new(path).parent();
        while let Some(p) = parent {
            if files.contains_key(p.to_str().ok_or("invalid closure path")?) {
                return Err("artifact path collides with directory".into());
            }
            parent = p.parent();
        }
    }
    Ok(files)
}
impl Selected {
    fn resolve_source(source: &Path, anchor: Artifact) -> Result<Self, String> {
        resolve(source, &anchor)?;
        let files = collect(source, &anchor)?;
        let selection: Selection = serde_json::from_slice(
            files
                .get(&anchor.path)
                .ok_or("selection absent from closure")?,
        )
        .map_err(|e| e.to_string())?;
        let attestation: Value = serde_json::from_slice(
            files
                .get(&selection.attestation.path)
                .ok_or("attestation absent")?,
        )
        .map_err(|e| e.to_string())?;
        let author = attestation["author"].as_str().ok_or("author absent")?;
        let reviewer = attestation["independent_reviewer"]
            .as_str()
            .ok_or("reviewer absent")?;
        if reviewer_key(author)? == reviewer_key(reviewer)? {
            return Err("review is not independent".into());
        }
        let metadata = super::root(source)?.metadata().map_err(|e| e.to_string())?;
        let selected = Self {
            source: source.into(),
            source_id: (metadata.dev(), metadata.ino()),
            anchor,
            files,
            expected: selection.expected,
            attestation: selection.attestation,
        };
        selected.recheck()?;
        Ok(selected)
    }
    pub(crate) fn production(source: &Path) -> Result<Self, String> {
        let (path, sha256) =
            PRODUCTION_SELECTION.ok_or("S3-qualified compiled selection absent")?;
        Self::resolve_source(
            source,
            Artifact {
                path: path.into(),
                sha256: sha256.into(),
            },
        )
    }
    #[cfg(test)]
    pub(crate) fn fixture(source: &Path, anchor: Artifact) -> Result<Self, String> {
        Self::resolve_source(source, anchor)
    }
    pub(crate) fn recheck(&self) -> Result<(), String> {
        // Association is held by this sealed native capability, never reselected
        // from mirror bytes. Production can construct it only from the constant.
        let metadata = super::root(&self.source)?
            .metadata()
            .map_err(|e| e.to_string())?;
        if (metadata.dev(), metadata.ino()) != self.source_id {
            return Err("selected source root relocated/replaced".into());
        }
        resolve(&self.source, &self.anchor)?;
        if collect(&self.source, &self.anchor)? != self.files {
            return Err("selected source closure changed".into());
        }
        Ok(())
    }
    pub(crate) fn files(&self) -> &BTreeMap<String, Vec<u8>> {
        &self.files
    }
    pub(crate) fn expected_ref(&self) -> &Artifact {
        &self.expected
    }
    pub(crate) fn attestation_ref(&self) -> &Artifact {
        &self.attestation
    }
    pub(crate) fn expected(&self) -> Result<Value, String> {
        serde_json::from_slice(
            self.files
                .get(&self.expected.path)
                .ok_or("missing selected reference")?,
        )
        .map_err(|e| e.to_string())
    }
    pub(crate) fn source(&self) -> &Path {
        &self.source
    }
    pub(crate) fn association(&self) -> Value {
        json!({"method":"selected-s1-contract-closure.s3","originalSource":self.source,"compiledAnchor":self.anchor,"expectedReference":self.expected,"adoptionAttestation":self.attestation})
    }
    pub(crate) fn check_mirror(&self, files: &BTreeMap<String, Vec<u8>>) -> Result<(), String> {
        self.recheck()?;
        for (path, bytes) in &self.files {
            if files.get(path) != Some(bytes) {
                return Err("selected mirror closure differs".into());
            }
        }
        Ok(())
    }
}

/// Invented contract-shaped values only; cannot compile into a production build.
#[cfg(test)]
pub(crate) fn fixture_files(source: &Path, inventory: &Value, expected_path: &str) -> Artifact {
    fn write(source: &Path, path: &str, value: &Value) -> Artifact {
        let raw = serde_json::to_vec(value).unwrap();
        let dest = source.join(path);
        std::fs::create_dir_all(dest.parent().unwrap()).unwrap();
        std::fs::write(dest, &raw).unwrap();
        Artifact {
            path: path.into(),
            sha256: digest(&raw),
        }
    }
    let mut e: Value = serde_json::from_str(include_str!(
        "../resources/distribution-successor/synthetic-expected.json"
    ))
    .unwrap();
    e["inventory"] = inventory.clone();
    e["pin"] = json!(crate::hosting::DECLARED_PIN);
    e["generated"]["pin"] = json!(crate::hosting::DECLARED_PIN);
    let ep = [
        "/label_evidence",
        "/generation_correspondence",
        "/generated/provenance",
        "/generated/version_advance",
        "/archive/acquisition_authorization",
        "/archive/custody",
        "/archive/extraction_procedure",
    ];
    for (n, p) in ep.iter().enumerate() {
        let reference = write(
            source,
            &format!("evidence/expected/{n}.json"),
            &json!({"path":"incidental-absent.json","sha256":"0".repeat(64)}),
        );
        *e.pointer_mut(p).unwrap() = serde_json::to_value(reference).unwrap();
    }
    let expected = write(source, expected_path, &e);
    let mut a: Value = serde_json::from_str(include_str!(
        "../resources/distribution-successor/synthetic-attestation.json"
    ))
    .unwrap();
    a["expected_reference"] = serde_json::to_value(&expected).unwrap();
    for (n, p) in [
        "/review_evidence",
        "/adoption/through_help_human",
        "/adoption/evidence",
    ]
    .iter()
    .enumerate()
    {
        let reference = write(
            source,
            &format!("evidence/adoption/{n}.json"),
            &json!({"synthetic":"opaque evidence; not an issuer"}),
        );
        *a.pointer_mut(p).unwrap() = serde_json::to_value(reference).unwrap();
    }
    let attestation = write(source, "reference/attestation.json", &a);
    write(
        source,
        "selection/build.json",
        &json!({"format":"build-selection.s2","method":"codex-vendor-tree-v1","schema_ids":["expected-reference.s1","adoption-attestation.s1"],"expected":expected,"attestation":attestation}),
    )
}
#[cfg(test)]
mod tests {
    use super::*;
    struct Fixture {
        root: PathBuf,
        anchor: Artifact,
    }
    impl Fixture {
        fn new() -> Self {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("closure-").unwrap());
            std::fs::create_dir(&root).unwrap();
            let e: Value = serde_json::from_str(include_str!(
                "../resources/distribution-successor/synthetic-expected.json"
            ))
            .unwrap();
            let anchor = fixture_files(&root, &e["inventory"], "reference/expected.json");
            Self { root, anchor }
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn exact_known_closure_preserves_opaque_incidental_json() {
        let f = Fixture::new();
        let selected = Selected::fixture(&f.root, f.anchor.clone()).unwrap();
        assert_eq!(selected.files.len(), 13);
        assert!(!selected.files.contains_key("incidental-absent.json"));
        for (path, bytes) in &selected.files {
            assert_eq!(*bytes, std::fs::read(f.root.join(path)).unwrap());
        }
        selected.check_mirror(&selected.files).unwrap();
    }
    #[test]
    fn wrong_anchor_dependency_tamper_and_missing_mirror_refuse() {
        let f = Fixture::new();
        let mut bad = f.anchor.clone();
        bad.sha256 = "0".repeat(64);
        assert!(Selected::fixture(&f.root, bad).is_err());
        let selected = Selected::fixture(&f.root, f.anchor.clone()).unwrap();
        let mut mirror = selected.files.clone();
        mirror.remove("evidence/expected/0.json");
        assert!(selected.check_mirror(&mirror).is_err());
        std::fs::write(f.root.join("evidence/expected/0.json"), b"tamper").unwrap();
        assert!(selected.recheck().is_err());
    }
    #[test]
    fn subject_disagreement_and_source_relocation_refuse() {
        let f = Fixture::new();
        let selected = Selected::fixture(&f.root, f.anchor.clone()).unwrap();
        let moved = f.root.with_extension("moved");
        std::fs::rename(&f.root, &moved).unwrap();
        std::fs::create_dir(&f.root).unwrap();
        for (path, raw) in &selected.files {
            let dest = f.root.join(path);
            std::fs::create_dir_all(dest.parent().unwrap()).unwrap();
            std::fs::write(dest, raw).unwrap();
        }
        assert!(selected.recheck().is_err());
        std::fs::remove_dir_all(moved).unwrap();
        let mut selection: Value =
            serde_json::from_slice(&std::fs::read(f.root.join(&f.anchor.path)).unwrap()).unwrap();
        let ap = f.root.join("reference/attestation.json");
        let mut a: Value = serde_json::from_slice(&std::fs::read(&ap).unwrap()).unwrap();
        a["expected_reference"]["path"] = json!("different.json");
        let raw = serde_json::to_vec(&a).unwrap();
        std::fs::write(ap, &raw).unwrap();
        selection["attestation"]["sha256"] = json!(digest(&raw));
        let raw = serde_json::to_vec(&selection).unwrap();
        std::fs::write(f.root.join(&f.anchor.path), &raw).unwrap();
        assert!(Selected::fixture(
            &f.root,
            Artifact {
                path: f.anchor.path.clone(),
                sha256: digest(&raw)
            }
        )
        .is_err());
    }
}

const PYTHON_TABLE: &str =
    include_str!("../resources/distribution-successor/python-string-identity.s3.json");
const PYTHON_TABLE_SHA256: &str =
    "071c266188836e733a100e01fe4b7a40552ed18d41b04d481fef1b2ea4a29f40";
fn python_table() -> Result<&'static Value, String> {
    static TABLE: std::sync::OnceLock<Result<Value, String>> = std::sync::OnceLock::new();
    TABLE
        .get_or_init(|| checked_python_table(PYTHON_TABLE))
        .as_ref()
        .map_err(Clone::clone)
}
fn checked_python_table(raw: &str) -> Result<Value, String> {
    if digest(raw.as_bytes()) != PYTHON_TABLE_SHA256 {
        return Err("unsupported Python identity table drift".into());
    }
    let value: Value = serde_json::from_str(raw).map_err(|e| e.to_string())?;
    if value["algorithm"] != "python-strip-casefold-scalar-v1"
        || value["unicodeVersion"] != "15.1.0"
    {
        return Err("unsupported string identity algorithm/version".into());
    }
    Ok(value)
}
pub(crate) fn reviewer_key(text: &str) -> Result<String, String> {
    let table = python_table()?;
    let whitespace = table["whitespace"]
        .as_array()
        .ok_or("whitespace table absent")?;
    let stripped = text.trim_matches(|c: char| {
        whitespace
            .iter()
            .any(|w| w.as_str() == Some(c.encode_utf8(&mut [0; 4])))
    });
    let mut folded = String::new();
    for c in stripped.chars() {
        let key = c.to_string();
        match table["casefold"].get(&key) {
            Some(value) => folded.push_str(value.as_str().ok_or("invalid fold mapping")?),
            None => folded.push(c),
        }
    }
    Ok(folded)
}
pub(crate) fn string_identity_basis() -> Value {
    match python_table() {
        Ok(table) => {
            json!({"method":table["algorithm"],"pythonImplementation":table["pythonImplementation"],"pythonVersion":table["pythonVersion"],"unicodeVersion":table["unicodeVersion"],"interpreterSha256":table["interpreterSha256"],"generatorSha256":table["generatorSha256"],"tableSha256":PYTHON_TABLE_SHA256,"domain":table["domain"]})
        }
        Err(error) => json!({"state":"unsupported","reason":error}),
    }
}

#[cfg(test)]
mod identity_tests {
    use super::*;
    use sha2::{Digest, Sha256};
    #[test]
    fn table_mapping_and_version_drift_refuse() {
        let mut changed: Value = serde_json::from_str(PYTHON_TABLE).unwrap();
        changed["casefold"]["A"] = json!("b");
        assert!(checked_python_table(&serde_json::to_string(&changed).unwrap()).is_err());
        let mut changed: Value = serde_json::from_str(PYTHON_TABLE).unwrap();
        changed["unicodeVersion"] = json!("future");
        assert!(checked_python_table(&serde_json::to_string(&changed).unwrap()).is_err());
    }
    #[test]
    fn sealed_selection_uses_unicode_and_control_boundary_identity_without_rewriting() {
        for (author, reviewer, accepted) in [
            ("Straße", "STRASSE", false),
            ("\u{1c}Alice\u{1f}", "\tALICE ", false),
            (" \t", "\u{1c}", false),
            ("Straße", "Distinct reviewer", true),
        ] {
            let root = std::env::temp_dir()
                .canonicalize()
                .unwrap()
                .join(crate::util::opaque_id("identity-selection-").unwrap());
            let sample: Value = serde_json::from_str(include_str!(
                "../resources/distribution-successor/synthetic-expected.json"
            ))
            .unwrap();
            let mut anchor = fixture_files(&root, &sample["inventory"], "reference/expected.json");
            let mut e: Value = serde_json::from_slice(
                &std::fs::read(root.join("reference/expected.json")).unwrap(),
            )
            .unwrap();
            e["author"] = json!(author);
            let raw = serde_json::to_vec(&e).unwrap();
            std::fs::write(root.join("reference/expected.json"), &raw).unwrap();
            let er = Artifact {
                path: "reference/expected.json".into(),
                sha256: digest(&raw),
            };
            let mut a: Value = serde_json::from_slice(
                &std::fs::read(root.join("reference/attestation.json")).unwrap(),
            )
            .unwrap();
            a["author"] = json!(author);
            a["independent_reviewer"] = json!(reviewer);
            a["expected_reference"] = serde_json::to_value(&er).unwrap();
            let raw = serde_json::to_vec(&a).unwrap();
            std::fs::write(root.join("reference/attestation.json"), &raw).unwrap();
            let ar = Artifact {
                path: "reference/attestation.json".into(),
                sha256: digest(&raw),
            };
            let mut selection: Value =
                serde_json::from_slice(&std::fs::read(root.join(&anchor.path)).unwrap()).unwrap();
            selection["expected"] = serde_json::to_value(er).unwrap();
            selection["attestation"] = serde_json::to_value(ar).unwrap();
            let raw = serde_json::to_vec(&selection).unwrap();
            std::fs::write(root.join(&anchor.path), &raw).unwrap();
            anchor.sha256 = digest(&raw);
            let result = Selected::fixture(&root, anchor);
            assert_eq!(result.is_ok(), accepted, "{author:?}/{reviewer:?}");
            if let Ok(selected) = result {
                assert_eq!(selected.expected().unwrap()["author"], author);
            }
            std::fs::remove_dir_all(root).unwrap();
        }
    }
    #[test]
    fn rust_identity_matches_every_pinned_python_scalar_and_mixed_oracle() {
        let table = python_table().unwrap();
        let mut hash = Sha256::new();
        for cp in 0..0x110000u32 {
            if let Some(c) = char::from_u32(cp) {
                let output = reviewer_key(&c.to_string()).unwrap();
                hash.update(cp.to_be_bytes());
                hash.update((output.len() as u32).to_be_bytes());
                hash.update(output.as_bytes());
            }
        }
        assert_eq!(
            format!("{:x}", hash.finalize()),
            table["oracle"]["scalarSha256"]
        );
        for pair in table["oracle"]["mixed"].as_array().unwrap() {
            assert_eq!(reviewer_key(pair[0].as_str().unwrap()).unwrap(), pair[1]);
        }
        assert_eq!(
            reviewer_key("Straße").unwrap(),
            reviewer_key("STRASSE").unwrap()
        );
        assert_eq!(
            reviewer_key("\u{1c}Alice\u{1f}").unwrap(),
            reviewer_key("\tALICE ").unwrap()
        );
        assert_ne!(
            reviewer_key("Author").unwrap(),
            reviewer_key("Reviewer").unwrap()
        );
    }
}
