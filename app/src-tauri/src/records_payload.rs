//! Live payload census shared by routing, export and package preparation.
//! Final names establish retained evidence even when their bytes are corrupt.
//! Only physically validated empty owning controls are omitted preparation;
//! an unresolved publication is preserved and refused with its path.
use super::{record_key, record_uuid, WriteFolder};
use crate::records_index::Stamp;
use std::collections::BTreeMap;
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};

/// Runtime refusal cause, never a stored record or connector format.
#[derive(Debug)]
pub(crate) enum CensusError {
    UnsafeMember { path: PathBuf, detail: String },
    Uncertain { path: PathBuf, detail: String },
}
impl CensusError {
    fn unsafe_member(path: &Path, detail: impl Into<String>) -> Self {
        Self::UnsafeMember {
            path: path.into(),
            detail: detail.into(),
        }
    }
    fn uncertain(path: &Path, detail: impl Into<String>) -> Self {
        Self::Uncertain {
            path: path.into(),
            detail: detail.into(),
        }
    }
    pub(crate) fn unsafe_path(&self) -> Option<&Path> {
        match self {
            Self::UnsafeMember { path, .. } => Some(path),
            Self::Uncertain { .. } => None,
        }
    }
}
impl std::fmt::Display for CensusError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnsafeMember { path, detail } | Self::Uncertain { path, detail } => {
                write!(f, "{}: {detail}", path.display())
            }
        }
    }
}

#[derive(Default)]
pub(crate) struct Census {
    pub(crate) members: BTreeMap<String, Stamp>,
    holds_records: bool,
}

#[derive(Default)]
struct Scan {
    census: Census,
    unknown: Option<CensusError>,
}

#[derive(Clone, Copy)]
enum Folder {
    Root,
    Records(WriteFolder),
    ConnectorEvidence,
    Auxiliary(&'static str),
    RoleContent,
    Opaque,
}

#[derive(Clone, Copy, PartialEq)]
enum Purpose {
    Routing,
    Inventory,
}

fn child(folder: Folder, name: &str) -> Option<Folder> {
    match folder {
        Folder::Root => Some(match name {
            "runs" => Folder::Records(WriteFolder::Runs),
            "acts" => Folder::Records(WriteFolder::Logs),
            "workflow" => Folder::Records(WriteFolder::Workflow),
            "legacy" => Folder::Records(WriteFolder::Legacy),
            "captures" => Folder::Records(WriteFolder::Captures),
            "connectors" => Folder::ConnectorEvidence,
            "fleet" => Folder::Auxiliary("coordination.fleet.jsonl"),
            "role-supply" => Folder::Auxiliary("observations.jsonl"),
            "reads" => Folder::Auxiliary("records-reads.jsonl"),
            "package-imports" => Folder::Auxiliary("package-imports"),
            _ => return None,
        }),
        Folder::Records(kind) => kind.child(name).map(Folder::Records).or_else(|| {
            // RS readers and legacy imports walk log ancestry recursively.
            matches!(kind, WriteFolder::Runs | WriteFolder::Logs).then_some(Folder::Records(kind))
        }),
        Folder::ConnectorEvidence => Some(Folder::ConnectorEvidence),
        Folder::Auxiliary("observations.jsonl") if name == "content" => Some(Folder::RoleContent),
        Folder::Auxiliary(_) | Folder::RoleContent | Folder::Opaque => None,
    }
}

pub(crate) const CONTROLS: &[&str] = &[
    ".writer.lock",
    ".after-run-end.lock",
    "captures/.capture.lock",
    "role-supply/.writer.lock",
];

pub(crate) fn control(rel: &str) -> bool {
    CONTROLS.contains(&rel)
}

fn role_content(name: &str) -> bool {
    name.strip_suffix(".utf8").is_some_and(record_key)
}

// The exact spelling shared by storage::create_json/create_bytes and package
// controls: a leading dot, the complete final basename, UUID v4, and .tmp.
pub(super) fn publication_name(name: &str) -> Option<&str> {
    let (final_name, nonce) = name
        .strip_prefix('.')?
        .strip_suffix(".tmp")?
        .rsplit_once('.')?;
    record_uuid(nonce).then_some(final_name)
}

fn final_record(kind: WriteFolder, name: &str) -> bool {
    // New publications use the write gate's names. Imported legacy logs and
    // captures can have earlier non-key basenames; they remain final evidence.
    kind.record_name(name)
        || !name.starts_with('.')
            && match kind {
                WriteFolder::Runs | WriteFolder::Logs => name.ends_with(".jsonl"),
                WriteFolder::Workflow | WriteFolder::Captures | WriteFolder::Pending => {
                    name.ends_with(".json")
                }
                _ => false,
            }
}

fn final_account(path: &Path, name: &str) -> bool {
    path.parent()
        .and_then(Path::file_name)
        .is_some_and(|n| n == "route-accounts")
        && WriteFolder::Accounts.record_name(name)
}
fn expects_directory(folder: Folder, name: &str) -> bool {
    match folder {
        Folder::Root => child(folder, name).is_some(),
        Folder::Records(kind) => kind.child(name).is_some(),
        Folder::ConnectorEvidence => name == "route-accounts",
        Folder::Auxiliary("observations.jsonl") => name == "content",
        Folder::Auxiliary(_) => false,
        Folder::RoleContent | Folder::Opaque => false,
    }
}
fn expects_file(folder: Folder, path: &Path, name: &str, rel: &str) -> bool {
    control(rel)
        || match folder {
            Folder::Records(kind) => final_record(kind, name),
            Folder::ConnectorEvidence => final_account(path, name),
            Folder::Root => matches!(name, "project.json" | "imports.jsonl"),
            Folder::Auxiliary("package-imports") => {
                name.strip_suffix(".json").is_some_and(record_key)
            }
            Folder::Auxiliary(expected) => name == expected,
            Folder::RoleContent => role_content(name),
            Folder::Opaque => false,
        }
}

/// Classify a bound plain member. Both package custody and this census call
/// this; a temporary name by itself never establishes discardable bytes.
fn member(
    root: &Path,
    path: &Path,
    folder: Folder,
    name: &str,
    rel: &str,
    meta: &std::fs::Metadata,
    purpose: Purpose,
) -> Result<(bool, bool), CensusError> {
    let fail = |why: &str| CensusError::uncertain(path, why);
    if !meta.is_file() {
        return Err(CensusError::unsafe_member(
            path,
            "not a plain member (symlink or unsupported file)",
        ));
    }
    if meta.nlink() != 1 {
        return Err(CensusError::unsafe_member(
            path,
            "hard linked member; publication or identity not known",
        ));
    }
    if purpose == Purpose::Routing && expects_directory(folder, name) {
        return Err(CensusError::unsafe_member(
            path,
            "not a directory at a payload folder",
        ));
    }
    let final_control = control(rel);
    let temporary_control = publication_name(name).is_some_and(|final_name| {
        let parent = path.parent().unwrap().strip_prefix(root).unwrap();
        // Only the package publisher stages owning controls with this name.
        // The role-observation writer opens its final lock directly.
        matches!(
            parent.join(final_name).to_str(),
            Some(".writer.lock" | "captures/.capture.lock")
        )
    });
    if final_control || temporary_control {
        let bytes = crate::records_retention::read_plain(path)
            .map_err(|e| CensusError::uncertain(path, e))?;
        if !bytes.is_empty() {
            return Err(fail("owning control has unexpected bytes; not known"));
        }
        if Stamp::of(&std::fs::symlink_metadata(path).map_err(|e| fail(&e.to_string()))?)
            != Stamp::of(meta)
        {
            return Err(fail("owning control changed during validation"));
        }
        return Ok((false, false));
    }
    // Connector publication attempts are deliberately retained evidence. The
    // connector's inventory also preserves imported opaque members verbatim.
    if publication_name(name).is_some()
        || matches!(folder, Folder::Records(WriteFolder::Workflow))
            && name.strip_prefix(".pending-").is_some_and(record_uuid)
    {
        return Err(fail(
            "unresolved record publication; bytes retained, completion not known",
        ));
    }
    if matches!(folder, Folder::ConnectorEvidence) {
        return Ok((true, final_account(path, name)));
    }
    let record = match folder {
        Folder::Records(kind) => final_record(kind, name),
        _ => false,
    };
    let auxiliary = match folder {
        Folder::Root => matches!(name, "project.json" | "imports.jsonl"),
        Folder::Auxiliary("package-imports") => name.strip_suffix(".json").is_some_and(record_key),
        Folder::Auxiliary(expected) => name == expected,
        Folder::RoleContent => role_content(name),
        _ => false,
    };
    if record || auxiliary || purpose == Purpose::Inventory {
        Ok((true, record))
    } else {
        Err(fail("unrecognised payload member; not known"))
    }
}

fn scan(root: &Path, purpose: Purpose) -> Scan {
    fn walk(
        root: &Path,
        dir: &Path,
        folder: Folder,
        out: &mut Scan,
        depth: usize,
        purpose: Purpose,
    ) -> Result<(), CensusError> {
        if depth > 256 {
            return Err(CensusError::uncertain(dir, "census depth exceeded"));
        }
        if let Some(meta) = crate::records_inspect::presence(dir)
            .map_err(|e| CensusError::uncertain(dir, e.to_string()))?
        {
            if !meta.is_dir() {
                return Err(CensusError::unsafe_member(
                    dir,
                    "not a plain payload directory",
                ));
            }
        }
        crate::storage::check_path(dir).map_err(|e| CensusError::uncertain(dir, e))?;
        let entries = crate::records_inspect::listing(dir)
            .map_err(|e| CensusError::uncertain(dir, format!("inventory incomplete: {e}")))?
            .unwrap_or_default();
        for entry in entries {
            // An uncertain earlier member must not hide a final later in this
            // folder, or prevent the parent from visiting its other folders.
            let result = (|| {
                let path: PathBuf = entry.path;
                let meta = entry.metadata.map_err(|e| {
                    CensusError::uncertain(&path, format!("inventory incomplete: {e}"))
                })?;
                let name = path
                    .file_name()
                    .and_then(|n| n.to_str())
                    .ok_or_else(|| CensusError::uncertain(&path, "unrecognised name"))?;
                let rel =
                    path.strip_prefix(root).unwrap().to_str().ok_or_else(|| {
                        CensusError::uncertain(&path, "payload path is not UTF-8")
                    })?;
                if meta.is_dir() {
                    if control(rel)
                        || purpose == Purpose::Routing && expects_file(folder, &path, name, rel)
                    {
                        return Err(CensusError::unsafe_member(
                            &path,
                            "directory where a final member belongs",
                        ));
                    }
                    let next = child(folder, name)
                        .or_else(|| (purpose == Purpose::Inventory).then_some(Folder::Opaque))
                        .ok_or_else(|| {
                            CensusError::uncertain(&path, "unrecognised payload folder; not known")
                        })?;
                    walk(root, &path, next, out, depth + 1, purpose)?;
                } else {
                    let (retained, record) =
                        member(root, &path, folder, name, rel, &meta, purpose)?;
                    if retained {
                        out.census.members.insert(rel.into(), Stamp::of(&meta));
                    }
                    out.census.holds_records |= record;
                }
                Ok::<(), CensusError>(())
            })();
            if let Err(error) = result {
                out.unknown.get_or_insert(error);
            }
        }
        Ok(())
    }
    let mut out = Scan::default();
    if let Err(error) = walk(root, root, Folder::Root, &mut out, 0, purpose) {
        out.unknown.get_or_insert(error);
    }
    out
}

/// Routing needs one final to establish that records are held. Uncertainty
/// decides the answer only when no final establishes it; readers keep their
/// own per-member limits after this home decision.
pub(crate) fn holds_records(root: &Path) -> Result<bool, CensusError> {
    let observed = scan(root, Purpose::Routing);
    if observed.census.holds_records {
        return Ok(true);
    }
    match observed.unknown {
        Some(error) => Err(error),
        None => Ok(false),
    }
}

/// Inventories carry ordinary unknown payload byte for byte, as earlier builds
/// did. Unresolved publications and physically unsafe/unexaminable members
/// still refuse; their names alone never authorize omitting their bytes.
pub(crate) fn census(root: &Path) -> Result<Census, String> {
    let observed = scan(root, Purpose::Inventory);
    match observed.unknown {
        Some(error) => Err(error.to_string()),
        None => Ok(observed.census),
    }
}
