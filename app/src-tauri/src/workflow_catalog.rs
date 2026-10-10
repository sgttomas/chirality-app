//! One explicitly selected Root package, embedded unchanged for development.
//! This is neither published release qualification nor historical shipping proof.
//! The child module alone constructs Selection from this closed resource set.
use super::{Selection, SelectionAdmission, Snapshot, WorkflowIdentity, SNAPSHOT_METHOD};
use std::{
    collections::BTreeMap,
    path::{Path, PathBuf},
};

pub const NAME: &str = "coordinated-knowledge-work";
pub const STANDING: &str = "App-v4 development build candidate; not a published release";
const REVISION: &str = "1b1733864cd89fd6d8ca74bf3e2084ff1105c1fc7d76537eefb42e2ae9a41e83";
const WORKFLOW: &[u8] =
    include_bytes!("../resources/development_workflows/coordinated-knowledge-work/WORKFLOW.md");
const NOTES: &[u8] =
    include_bytes!("../resources/development_workflows/coordinated-knowledge-work/REVIEW-NOTES.md");

/// No caller-supplied catalog, tuple, manifest, file or proof constructor.
/// Loading this value admits only the manager-selected embedded package set.
pub struct DevelopmentCatalog {
    selection: Selection,
}

impl DevelopmentCatalog {
    pub fn load() -> Result<Self, String> {
        let snapshot = Snapshot::from_files(BTreeMap::from([
            ("WORKFLOW.md".into(), WORKFLOW.to_vec()),
            ("REVIEW-NOTES.md".into(), NOTES.to_vec()),
        ]))?;
        if snapshot.revision() != REVISION || !snapshot.hygiene_findings().is_empty() {
            return Err("development package differs from its admitted source revision".into());
        }
        let identity = snapshot.identity("bundled", "chirality-root", NAME, None)?;
        if identity.revision_method != SNAPSHOT_METHOD {
            return Err("development package method differs from its admitted method".into());
        }
        Ok(Self {
            selection: Selection {
                snapshot,
                identity,
                admission: SelectionAdmission::DevelopmentCatalog {
                    source_map_sha256: crate::util::sha256_hex(include_bytes!(
                        "../resources/development_workflows/SOURCE_MAP.json"
                    )),
                    tranche: "APP-V4-GROUP-A-DEVELOPMENT-WORKFLOW-20261005".into(),
                },
            },
        })
    }

    pub fn identity(&self) -> &WorkflowIdentity {
        self.selection.identity()
    }

    pub fn standing(&self) -> &'static str {
        STANDING
    }

    /// Caller choice can select this embedded tuple, never relabel caller bytes.
    pub fn select_embedded(&self) -> Selection {
        self.selection.clone()
    }

    /// LS-8-style equality restricted to this development candidate, not release
    /// history. All files, including notes and additional files, participate.
    pub fn recognize_holding_copy(&self, package: &Path) -> Result<HoldingCopySelection, String> {
        if !package.is_absolute() {
            return Err("holding copy requires a fixed absolute package path".into());
        }
        if package.file_name().and_then(|n| n.to_str()) != Some(NAME) {
            return Err("holding copy name differs from the admitted package".into());
        }
        let held = Snapshot::capture(package)?;
        if held.files() != self.selection.snapshot().files()
            || held.revision() != self.identity().revision
        {
            return Err(
                "holding copy differs from the admitted development package; review to register"
                    .into(),
            );
        }
        Ok(HoldingCopySelection {
            selection: self.selection.clone(),
            package: package.to_path_buf(),
        })
    }
}

/// Exact holding location remains distinct from the immutable bundled identity.
pub struct HoldingCopySelection {
    selection: Selection,
    package: PathBuf,
}
impl HoldingCopySelection {
    pub fn selection(&self) -> &Selection {
        &self.selection
    }
    pub fn package_path(&self) -> &Path {
        &self.package
    }
    pub fn standing(&self) -> &'static str {
        STANDING
    }
    /// Recheck at the point of use; later mutation never changes the pinned tuple.
    pub fn verify_current(&self) -> Result<(), String> {
        self.selection.verify_store(&self.package)
    }
}

/// Integrator-selected production inputs. Candidate admission is distinct from
/// historical release recognition: this first manifest claims no shipped past.
pub const PRODUCTION_STANDING: &str = "production bundle candidate; not a published release";
pub const RELEASE_SUBJECT: &str = "chirality-app-v4:APP-V4-BUNDLE-INPUTS-20261008";
const MANIFEST: &[u8] = include_bytes!("../resources/production_workflows/MANIFEST.json");
const PRODUCTION_WORKFLOW: &[u8] =
    include_bytes!("../resources/production_workflows/coordinated-knowledge-work/WORKFLOW.md");
const PRODUCTION_NOTES: &[u8] =
    include_bytes!("../resources/production_workflows/coordinated-knowledge-work/REVIEW-NOTES.md");

pub struct ProductionCatalog {
    selection: Selection,
}
impl ProductionCatalog {
    /// The build closes both manifest and byte inputs; caller manifests cannot
    /// confer bundle admission. Every included file participates in identity.
    pub fn load() -> Result<Self, String> {
        let snapshot = Snapshot::from_files(BTreeMap::from([
            ("WORKFLOW.md".into(), PRODUCTION_WORKFLOW.to_vec()),
            ("REVIEW-NOTES.md".into(), PRODUCTION_NOTES.to_vec()),
        ]))?;
        let manifest = crate::workflow_declaration::parse_unique(
            std::str::from_utf8(MANIFEST).map_err(|e| e.to_string())?,
        )?;
        let package = &manifest["packages"][0];
        let expected_files: Vec<_> = snapshot.files().iter().map(|(path, bytes)|
            serde_json::json!({"path":path,"bytes":bytes.len(),"sha256":crate::util::sha256_hex(bytes)})
        ).collect();
        if manifest["schema_version"] != 1
            || manifest["release_subject"] != RELEASE_SUBJECT
            || manifest["standing"] != PRODUCTION_STANDING
            || manifest["historical_shipped_revisions"] != serde_json::json!([])
            || manifest["recognize_v3"] != false
            || manifest["source_revision"] != "6d3fa1e0d4de75cdfc2c76c4e08117901b20b29d"
            || manifest["packages"].as_array().map(Vec::len) != Some(1)
            || package["name"] != NAME
            || package["source_root"] != "chirality-root"
            || package["source_path"] != "workflows/coordinated-knowledge-work"
            || package["revision_method"] != SNAPSHOT_METHOD
            || package["revision"] != snapshot.revision()
            || package["files"] != serde_json::json!(expected_files)
            || !snapshot.hygiene_findings().is_empty()
        {
            return Err("production bundle manifest does not bind admitted source bytes".into());
        }
        let identity = snapshot.identity("bundled", RELEASE_SUBJECT, NAME, None)?;
        Ok(Self {
            selection: Selection {
                snapshot,
                identity,
                admission: SelectionAdmission::ProductionBundle {
                    manifest_sha256: crate::util::sha256_hex(MANIFEST),
                    release_subject: RELEASE_SUBJECT.into(),
                    holding_library: None,
                    bundle_root: None,
                },
            },
        })
    }
    pub fn identity(&self) -> &WorkflowIdentity {
        self.selection.identity()
    }
    pub fn select_embedded(&self) -> Selection {
        self.selection.clone()
    }
    pub fn manifest(&self) -> &'static [u8] {
        MANIFEST
    }

    /// Native wiring supplies App resource_dir/workflows, never a person-minted manifest.
    pub fn select_bundle_package(
        &self,
        root: &Path,
        name: &str,
    ) -> Result<ProductionBundlePackage, String> {
        if name != self.identity().name {
            return Err("name not in production catalog".into());
        }
        verify_bundle_manifest(root)?;
        let package = root.join(name);
        crate::storage::check_path(&package)?;
        self.selection.verify_store(&package)?;
        let mut selection = self.selection.clone();
        if let SelectionAdmission::ProductionBundle { bundle_root, .. } = &mut selection.admission {
            *bundle_root = Some(root.into());
        }
        Ok(ProductionBundlePackage { selection, package })
    }

    /// LS-8 candidate counterpart: a same-name, byte-equal copy in an actual
    /// unregistered library slot. Never treats a draft, arbitrary path or an
    /// occupied/corrupt registry slot as a release-registered workflow.
    pub fn recognize_holding_copy(
        &self,
        library_root: &Path,
        name: &str,
    ) -> Result<ProductionHoldingCopy, String> {
        if name != self.identity().name {
            return Err("name not in production catalog".into());
        }
        verify_unregistered_slot(library_root, name)?;
        let package = library_root.join(".chirality/workflows").join(name);
        self.selection.verify_store(&package)?;
        let mut selection = self.selection.clone();
        if let SelectionAdmission::ProductionBundle {
            holding_library, ..
        } = &mut selection.admission
        {
            *holding_library = Some(library_root.into());
        }
        Ok(ProductionHoldingCopy {
            selection,
            library_root: library_root.into(),
            package,
        })
    }
}
pub(super) fn verify_unregistered_slot(library_root: &Path, name: &str) -> Result<(), String> {
    if !library_root.is_absolute() || !library_root.is_dir() {
        return Err("fixed existing physical library root required".into());
    }
    crate::storage::check_path(library_root)?;
    crate::storage::check_path(&library_root.join(".chirality/workflows").join(name))?;
    let rows = super::registration::read_ledger(library_root)?;
    if rows
        .iter()
        .any(|row| row["identity"]["name"] == name && row["outcome"] == "registered")
    {
        return Err("registered slot: use its registered revision; no bundled substitution".into());
    }
    // An orphaned revision store is ambiguous, not an unregistered slot.
    let store = library_root
        .join(".chirality/workflow-revisions")
        .join(name);
    crate::storage::check_path(&store)?;
    match std::fs::symlink_metadata(&store) {
        Ok(_) => return Err("revision store present: library slot needs reconciliation".into()),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(format!("revision store unreadable: {e}")),
    }
    Ok(())
}
pub struct ProductionHoldingCopy {
    selection: Selection,
    library_root: PathBuf,
    package: PathBuf,
}
impl ProductionHoldingCopy {
    pub fn selection(&self) -> &Selection {
        &self.selection
    }
    pub fn package_path(&self) -> &Path {
        &self.package
    }
    pub fn verify_current(&self) -> Result<(), String> {
        verify_unregistered_slot(&self.library_root, &self.selection.identity().name)?;
        self.selection.verify_store(&self.package)
    }
}

/// Concrete installed bundle resolution; retained Selection rechecks this manifest
/// and path through the existing prepare/send verify_store consumer.
pub struct ProductionBundlePackage {
    selection: Selection,
    package: PathBuf,
}
impl ProductionBundlePackage {
    pub fn selection(&self) -> &Selection {
        &self.selection
    }
    pub fn package_path(&self) -> &Path {
        &self.package
    }
    pub fn verify_current(&self) -> Result<(), String> {
        self.selection.verify_store(&self.package)
    }
}
pub(super) fn verify_bundle_manifest(root: &Path) -> Result<(), String> {
    if !root.is_absolute() || !root.is_dir() {
        return Err("fixed existing bundle root required".into());
    }
    let manifest = root.join("MANIFEST.json");
    crate::storage::check_path(&manifest)?;
    if super::read_regular_file(&manifest)
        .map_err(|e| format!("bundle manifest not resolvable: {e}"))?
        != MANIFEST
    {
        return Err("bundle manifest differs from admitted release candidate".into());
    }
    Ok(())
}
