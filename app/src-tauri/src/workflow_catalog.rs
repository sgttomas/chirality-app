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
