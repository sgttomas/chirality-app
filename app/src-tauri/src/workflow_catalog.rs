//! The development catalog: one explicitly selected Root package, embedded
//! unchanged. The production catalog: every workflow of the selected Library
//! release, named by a compiled manifest and read from installed resources.
//! Neither is published release qualification nor historical shipping proof.
//! This child module alone constructs Selection from these closed sets.
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
                registration_basis: None,
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
        // A holding copy is the one package a person picks by its own path, so the reader's refusal
        // of a link above it is said here in words they can act on.
        let held = Snapshot::capture(package).map_err(|e| {
            if e.contains(super::LINK_IN_PACKAGE_PATH) {
                format!("{e}. Choose the holding copy by the real location of its folder, not through a linked folder (on a Mac, /tmp and /var are links to /private/tmp and /private/var)")
            } else {
                e
            }
        })?;
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

/// Every workflow of the selected Library release, as the generated manifest
/// names them (`python3 -m tools.library_workflows`). Candidate admission is
/// distinct from historical release recognition: the manifest claims no
/// shipped past.
pub const PRODUCTION_STANDING: &str = "production bundle candidate; not a published release";
/// The bundled library's source root: the selected Library edition.
pub const RELEASE_SUBJECT: &str = "chirality-library:library-v3.4.0";
const MANIFEST: &[u8] = include_bytes!("../resources/production_workflows/MANIFEST.json");

/// WR LS-5 closed bundled-run subject (DEL-02-02 BUNDLED-RUN-01; widened to the
/// selected Library's whole workflow set, DEL-02-02 AC-014). The compiled
/// manifest names every bundled package, its files and its revision, and this
/// digest pins that manifest: changing any shipped byte changes the generated
/// manifest and so requires a reviewed change here. Only a package this
/// manifest names, resolved from this App's own installed resources with bytes
/// that hash to the manifest's revision, runs without A15. The constant claims
/// no published release, shipped history or qualification.
pub const SELECTED_BUNDLED_MANIFEST_SHA256: &str =
    "20a015b810abececdbf1fe3767ef443476a5aec1c768343c3db8f68daf062f63";
/// Standing of the admitted LS-5 selection. The candidate build itself is still
/// not a published release; that standing stays with the manifest.
pub const BUNDLED_STANDING: &str =
    "bundled with this App build (WR LS-5); runs without A15; this build is a release candidate, not a published release";

/// BUNDLED-RUN-01: this App's own installed workflow resources
/// (`resource_dir()/workflows`), recorded once per process by native startup.
/// It is the only bundle root an LS-5 run may come from, checked by
/// `bundled_run_admission` at selection, prepare, publication and send. Never a
/// caller, renderer or record path.
#[cfg(not(test))]
static INSTALLED_ROOT: std::sync::OnceLock<PathBuf> = std::sync::OnceLock::new();
#[cfg(test)]
thread_local! {
    static TEST_INSTALLED_ROOT: std::cell::RefCell<Option<PathBuf>> = const { std::cell::RefCell::new(None) };
}
/// Native startup only. A second, different root is refused (no rebinding).
/// Test builds record per test thread instead of process-wide.
pub(crate) fn record_installed_root(root: PathBuf) -> Result<(), String> {
    #[cfg(test)]
    return TEST_INSTALLED_ROOT.with(|held| {
        let mut held = held.borrow_mut();
        match held.as_ref() {
            Some(existing) if *existing != root => Err("installed workflow resources already recorded; no rebinding".into()),
            _ => {
                *held = Some(root);
                Ok(())
            }
        }
    });
    #[cfg(not(test))]
    {
        let held = INSTALLED_ROOT.get_or_init(|| root.clone());
        if *held != root {
            return Err("installed workflow resources already recorded; no rebinding".into());
        }
        Ok(())
    }
}
pub(crate) fn installed_root() -> Option<PathBuf> {
    #[cfg(test)]
    return TEST_INSTALLED_ROOT.with(|held| held.borrow().clone());
    #[cfg(not(test))]
    INSTALLED_ROOT.get().cloned()
}

/// One bundled workflow as the compiled manifest names it. Package bytes are
/// not compiled in: they are read from the App's installed resources (or a
/// library holding copy) and admitted only when they hash to `identity.revision`.
pub struct ProductionEntry {
    identity: WorkflowIdentity,
    files: serde_json::Value,
    listing: serde_json::Value,
}
impl ProductionEntry {
    pub fn identity(&self) -> &WorkflowIdentity {
        &self.identity
    }
    /// What the Library says of the workflow, for selection: description,
    /// central, compatibility, roles, navigation, its execution companion as
    /// the index states it, and the release paths its files name.
    pub fn listing(&self) -> &serde_json::Value {
        &self.listing
    }
}
pub struct ProductionCatalog {
    entries: BTreeMap<String, ProductionEntry>,
    source: serde_json::Value,
}
impl ProductionCatalog {
    /// The build closes the manifest; caller manifests cannot confer bundle
    /// admission. Parsed once per process: the compiled bytes never change.
    pub fn load() -> Result<&'static Self, String> {
        static CATALOG: std::sync::OnceLock<Result<ProductionCatalog, String>> =
            std::sync::OnceLock::new();
        CATALOG
            .get_or_init(|| {
                Self::parse(MANIFEST)
                    .map_err(|e| format!("production bundle manifest is not admitted: {e}"))
            })
            .as_ref()
            .map_err(Clone::clone)
    }
    pub(super) fn parse(manifest: &[u8]) -> Result<Self, String> {
        let manifest = crate::workflow_declaration::parse_unique(
            std::str::from_utf8(manifest).map_err(|e| e.to_string())?,
        )?;
        if manifest["schema_version"] != 2
            || manifest["release_subject"] != RELEASE_SUBJECT
            || manifest["standing"] != PRODUCTION_STANDING
            || manifest["historical_shipped_revisions"] != serde_json::json!([])
            || manifest["recognize_v3"] != false
            || !manifest["source"].is_object()
        {
            return Err("manifest header differs from the admitted release subject".into());
        }
        let mut entries = BTreeMap::new();
        for package in manifest["packages"].as_array().ok_or("no package list")? {
            let name = package["name"].as_str().ok_or("package without a name")?;
            let revision = package["revision"].as_str().ok_or("package without a revision")?;
            let files = package["files"].as_array().ok_or("package without a file list")?;
            if package["revision_method"] != SNAPSHOT_METHOD
                || revision.len() != 64
                || !revision.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
                || package["source_path"] != format!("workflows/{name}")
                || !files.iter().any(|file| file["path"] == "WORKFLOW.md")
            {
                return Err(format!("package {name} is not bound by the manifest"));
            }
            let identity = WorkflowIdentity {
                kind: "workflow".into(),
                origin: "bundled".into(),
                source_root: RELEASE_SUBJECT.into(),
                name: name.into(),
                revision: revision.into(),
                revision_method: SNAPSHOT_METHOD.into(),
                derived_from: None,
            };
            identity.validate()?;
            let listing = serde_json::json!({
                "description": package["description"],
                "central": package["central"],
                "compatibility": package["compatibility"],
                "roles": package["roles"],
                "navigation": package["navigation"],
                // What the Library's index states for the method (null without
                // an execution companion), and the release paths the package's
                // files name that the App does not include. Neither is the
                // declared part: nothing here feeds the requirement check.
                "libraryExecution": package["library_execution"],
                "libraryPathsNamed": package["library_paths_named"],
            });
            let entry = ProductionEntry { identity, files: package["files"].clone(), listing };
            if entries.insert(name.to_owned(), entry).is_some() {
                return Err(format!("package {name} is named twice"));
            }
        }
        if entries.is_empty() {
            return Err("manifest names no package".into());
        }
        Ok(Self { entries, source: manifest["source"].clone() })
    }
    /// Every bundled workflow, ordered by name.
    pub fn entries(&self) -> impl Iterator<Item = &ProductionEntry> {
        self.entries.values()
    }
    fn entry(&self, name: &str) -> Result<&ProductionEntry, String> {
        self.entries.get(name).ok_or_else(|| "name not in production catalog".into())
    }
    pub fn identity(&self, name: &str) -> Result<&WorkflowIdentity, String> {
        self.entry(name).map(ProductionEntry::identity)
    }
    /// The Library release the bundle was generated from: repository, tag,
    /// commit and archive, as the manifest records them.
    pub fn source(&self) -> &serde_json::Value {
        &self.source
    }
    pub fn manifest(&self) -> &'static [u8] {
        MANIFEST
    }
    /// The bytes at `package` as the named bundled workflow, or a refusal.
    /// Every file participates: the captured files must be the manifest's
    /// files and hash to the manifest's revision.
    fn admit(&self, name: &str, package: &Path) -> Result<Selection, String> {
        let entry = self.entry(name)?;
        let snapshot = Snapshot::capture(package)
            .map_err(|e| format!("selected revision not resolvable: {e}"))?;
        let files: Vec<_> = snapshot.files().iter().map(|(path, bytes)|
            serde_json::json!({"path":path,"bytes":bytes.len(),"sha256":crate::util::sha256_hex(bytes)})
        ).collect();
        if snapshot.revision() != entry.identity.revision
            || entry.files != serde_json::json!(files)
            || !snapshot.hygiene_findings().is_empty()
        {
            return Err("revision not verified".into());
        }
        Ok(Selection {
            registration_basis: None,
            snapshot,
            identity: entry.identity.clone(),
            admission: SelectionAdmission::ProductionBundle {
                manifest_sha256: crate::util::sha256_hex(MANIFEST),
                release_subject: RELEASE_SUBJECT.into(),
                holding_library: None,
                bundle_root: None,
            },
        })
    }
    /// Test fixtures only: a bundled package read from the source tree the
    /// build bundles, as an unresolved candidate (no bundle root, not runnable).
    #[cfg(test)]
    pub fn select_source(&self, name: &str) -> Selection {
        let source = Path::new(env!("CARGO_MANIFEST_DIR")).join("resources/production_workflows");
        self.admit(name, &source.join(name)).unwrap()
    }

    /// The run guide's reading of one entry of the bundle at `root`: whether
    /// `select_bundle_package` resolves it now. The listing is read on every
    /// host tick, so a package's verification is kept while its files' sizes
    /// and modification times are unchanged. This is a listing aid only:
    /// selection, preparation and sending always read and hash the bytes.
    pub fn listed_admission(&self, root: &Path, name: &str) -> Result<(), String> {
        self.listed_requirement_declaration(root, name).map(|_| ())
    }
    /// The same listing aid, with what the entry's own verified bytes declare
    /// of its required tools (`workflow_declaration::requirement_declaration`,
    /// read as a selection of those bytes reads it). An entry that does not
    /// resolve has no reading: the refusal is returned instead.
    ///
    /// A kept verification answers only while the package folder itself and
    /// everything beneath it are what was verified, by [`FileFacts`]: kind,
    /// size, modification time and, where the platform gives them, identity
    /// and status-change time. A result is kept only when those facts were
    /// the same before and after its verification, and it answers only once
    /// every modification and status-change time among them is at least
    /// [`SETTLED`] older than the moment that verification began, so a later
    /// write always carries a newer status-change time than the kept one,
    /// also where the filesystem keeps times to the second. Until then every
    /// listing verifies again. Not covered: a writer who sets the clock back,
    /// or who can put a status-change time back. Selection, preparation and
    /// sending read and hash the bytes whatever this says.
    pub fn listed_requirement_declaration(&self, root: &Path, name: &str) -> Result<serde_json::Value, String> {
        let package = root.join(name);
        let verify = || self.select_bundle_package(root, name).map(|package| {
            crate::workflow_declaration::requirement_declaration(&package.selection.snapshot().declaration())
        });
        listed_or_verified(&package, SETTLED, verify).0
    }

    /// WR LS-5 / TT-1 / TX-1: the closed bundled-run admission. Admits only a
    /// package the compiled manifest names, resolved by `select_bundle_package`
    /// from exactly this App's recorded installed root (never a library holding
    /// copy, a copy at another root, a development or registered selection).
    /// Bytes and location are rechecked at use by `verify_store`; this check
    /// alone grants no file authority.
    pub fn bundled_run_admission(selection: &Selection) -> Result<&Path, String> {
        let SelectionAdmission::ProductionBundle {
            manifest_sha256,
            release_subject,
            holding_library: None,
            bundle_root: Some(root),
        } = &selection.admission
        else {
            return Err("not a selection resolved from this App's installed bundle".into());
        };
        let catalog = Self::load()?;
        if crate::util::sha256_hex(MANIFEST) != SELECTED_BUNDLED_MANIFEST_SHA256
            || manifest_sha256 != SELECTED_BUNDLED_MANIFEST_SHA256
            || release_subject != RELEASE_SUBJECT
            || catalog.identity(&selection.identity.name).ok() != Some(&selection.identity)
            || selection.snapshot.revision != selection.identity.revision
        {
            return Err("bundled subject is not a workflow of this App's bundled manifest".into());
        }
        match installed_root() {
            Some(installed) if installed.as_path() == root.as_path() => Ok(root),
            Some(_) => Err("This bundled workflow was not resolved from this App's installed resources (WR LS-5)".into()),
            None => Err("This App's installed workflow resources are not known in this process (WR LS-5)".into()),
        }
    }

    /// Native wiring supplies App resource_dir/workflows, never a person-minted manifest.
    pub fn select_bundle_package(
        &self,
        root: &Path,
        name: &str,
    ) -> Result<ProductionBundlePackage, String> {
        self.entry(name)?;
        verify_bundle_manifest(root)?;
        let package = root.join(name);
        crate::storage::check_path(&package)?;
        let mut selection = self.admit(name, &package)?;
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
        self.entry(name)?;
        verify_unregistered_slot(library_root, name)?;
        let package = library_root.join(".chirality/workflows").join(name);
        let mut selection = self.admit(name, &package)?;
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
/// How much older than the start of its verification every time among a
/// package's facts must be before a kept verification answers for it.
pub(super) const SETTLED: std::time::Duration = std::time::Duration::from_secs(2);
type Listed = std::collections::HashMap<PathBuf, (Vec<FileFacts>, std::time::SystemTime, Result<serde_json::Value, String>)>;
/// The package folder's own facts and those of everything beneath it, in
/// order; `None` where the folder is anything but a real folder or cannot be
/// walked, which is never answered from a kept verification.
fn package_facts(package: &Path) -> Option<Vec<FileFacts>> {
    let mut facts = Vec::new();
    match std::fs::symlink_metadata(package) {
        Ok(meta) if meta.is_dir() => facts.push(facts_of(package.to_owned(), &meta)),
        _ => return None,
    }
    file_facts(package, &mut facts).ok()?;
    facts.sort();
    Some(facts)
}
/// Whether every modification and status-change time among `facts` is at
/// least `margin` older than `began`. A path with no modification time, or a
/// time the platform gives that cannot be placed, is never settled.
pub(super) fn settled(facts: &[FileFacts], began: std::time::SystemTime, margin: std::time::Duration) -> bool {
    let Some(limit) = began.checked_sub(margin) else { return false };
    facts.iter().all(|(_, _, _, modified, identity)| {
        let changed = match identity {
            Some((_, _, seconds, nanoseconds)) => match (u64::try_from(*seconds), u32::try_from(*nanoseconds)) {
                (Ok(seconds), Ok(nanoseconds)) => std::time::UNIX_EPOCH.checked_add(std::time::Duration::new(seconds, nanoseconds)),
                _ => None,
            },
            // No status-change time on this platform: the modification time alone.
            None => *modified,
        };
        matches!((modified, changed), (Some(modified), Some(changed)) if *modified <= limit && changed <= limit)
    })
}
static LISTED: std::sync::OnceLock<std::sync::Mutex<Listed>> = std::sync::OnceLock::new();
/// Tests only: whether a verification is kept for `package` at all.
#[cfg(test)]
pub(super) fn listing_keeps(package: &Path) -> bool {
    LISTED.get_or_init(Default::default).lock().unwrap_or_else(|e| e.into_inner()).contains_key(package)
}
/// The listing aid's one decision: the kept result for `package` where its
/// facts are those verified and settled by `margin`, and otherwise `verify`'s
/// result, kept only if the facts are the same after verifying as before.
/// The second value says whether the answer came from a kept verification.
pub(super) fn listed_or_verified(package: &Path, margin: std::time::Duration, verify: impl FnOnce() -> Result<serde_json::Value, String>) -> (Result<serde_json::Value, String>, bool) {
    let Some(facts) = package_facts(package) else { return (verify(), false) };
    let mut listed = LISTED.get_or_init(Default::default).lock().unwrap_or_else(|e| e.into_inner());
    if let Some((seen, began, result)) = listed.get(package) {
        if *seen == facts && settled(seen, *began, margin) {
            return (result.clone(), true);
        }
    }
    let began = std::time::SystemTime::now();
    let result = verify();
    if package_facts(package).as_ref() == Some(&facts) {
        listed.insert(package.to_owned(), (facts, began, result.clone()));
    } else {
        listed.remove(package);
    }
    (result, false)
}
/// Path, kind, size and modification time of one entry beneath a package.
/// What the listing aid compares to take a package as unchanged since it was
/// verified: a path's kind (file, folder, link or other), size, modification
/// time and, on Unix, its device and inode and its status-change time, which a
/// write or a change of its times moves and no caller can set.
pub(super) type FileFacts = (PathBuf, u8, u64, Option<std::time::SystemTime>, Option<(u64, u64, i64, i64)>);
fn facts_of(path: PathBuf, meta: &std::fs::Metadata) -> FileFacts {
    let kind = if meta.file_type().is_symlink() { 2 } else if meta.is_dir() { 1 } else if meta.is_file() { 0 } else { 3 };
    #[cfg(unix)]
    let identity = {
        use std::os::unix::fs::MetadataExt;
        Some((meta.dev(), meta.ino(), meta.ctime(), meta.ctime_nsec()))
    };
    #[cfg(not(unix))]
    let identity = None;
    (path, kind, meta.len(), meta.modified().ok(), identity)
}
fn file_facts(folder: &Path, out: &mut Vec<FileFacts>) -> std::io::Result<()> {
    for entry in std::fs::read_dir(folder)? {
        let path = entry?.path();
        let meta = std::fs::symlink_metadata(&path)?;
        out.push(facts_of(path.clone(), &meta));
        if meta.is_dir() {
            file_facts(&path, out)?;
        }
    }
    Ok(())
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
pub(crate) fn verify_bundle_manifest(root: &Path) -> Result<(), String> {
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
