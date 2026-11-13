//! Live payload census shared by routing, export and package preparation.
//! Final names establish retained evidence even when their bytes are corrupt.
//! Only physically validated empty owning controls are omitted preparation;
//! an unresolved publication is preserved and refused with its path.
use super::{record_key, record_uuid, WriteFolder};
use crate::records_index::Stamp;
use std::collections::BTreeMap;
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};

#[derive(Default)]
pub(crate) struct Census {
    pub(crate) members: BTreeMap<String, Stamp>,
    pub(crate) holds_records: bool,
}

#[derive(Clone, Copy)]
enum Folder {
    Root,
    Records(WriteFolder),
    ConnectorEvidence,
    Auxiliary(&'static str),
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
        Folder::Auxiliary(_) => None,
    }
}

fn control(rel: &str) -> bool {
    matches!(rel, ".writer.lock" | "captures/.capture.lock")
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

/// Classify a bound plain member. Both package custody and this census call
/// this; a temporary name by itself never establishes discardable bytes.
fn member(
    root: &Path,
    path: &Path,
    folder: Folder,
    name: &str,
    rel: &str,
    meta: &std::fs::Metadata,
) -> Result<(bool, bool), String> {
    let fail = |why: &str| format!("{}: {why}", path.display());
    if !meta.is_file() {
        return Err(fail("not a plain member (symlink or unsupported file)"));
    }
    if meta.nlink() != 1 {
        return Err(fail(
            "hard linked member; publication or identity not known",
        ));
    }
    let final_control = control(rel);
    let temporary_control = publication_name(name).is_some_and(|final_name| {
        let parent = path.parent().unwrap().strip_prefix(root).unwrap();
        control(&parent.join(final_name).to_string_lossy())
    });
    if final_control || temporary_control {
        let bytes = crate::records_retention::read_plain(path)?;
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
        let final_account = path
            .parent()
            .and_then(Path::file_name)
            .is_some_and(|n| n == "route-accounts")
            && WriteFolder::Accounts.record_name(name);
        return Ok((true, final_account));
    }
    let record = match folder {
        Folder::Records(kind) => final_record(kind, name),
        _ => false,
    };
    let auxiliary = match folder {
        Folder::Root => matches!(name, "project.json" | "imports.jsonl"),
        Folder::Auxiliary("package-imports") => name.strip_suffix(".json").is_some_and(record_key),
        Folder::Auxiliary(expected) => name == expected,
        _ => false,
    };
    if record || auxiliary {
        Ok((true, record))
    } else {
        Err(fail("unrecognised payload member; not known"))
    }
}

pub(crate) fn census(root: &Path) -> Result<Census, String> {
    fn walk(
        root: &Path,
        dir: &Path,
        folder: Folder,
        out: &mut Census,
        depth: usize,
    ) -> Result<(), String> {
        if depth > 256 {
            return Err(format!("{}: census depth exceeded", dir.display()));
        }
        crate::storage::check_path(dir)?;
        let entries = crate::records_inspect::listing(dir)
            .map_err(|e| format!("{}: inventory incomplete: {e}", dir.display()))?
            .unwrap_or_default();
        for entry in entries {
            let path: PathBuf = entry.path;
            let meta = entry
                .metadata
                .map_err(|e| format!("{}: inventory incomplete: {e}", path.display()))?;
            let name = path
                .file_name()
                .and_then(|n| n.to_str())
                .ok_or_else(|| format!("{}: unrecognised name", path.display()))?;
            let rel = path
                .strip_prefix(root)
                .unwrap()
                .to_str()
                .ok_or("payload path is not UTF-8")?;
            if meta.is_dir() {
                let next = child(folder, name).ok_or_else(|| {
                    format!("{}: unrecognised payload folder; not known", path.display())
                })?;
                walk(root, &path, next, out, depth + 1)?;
            } else {
                let (retained, record) = member(root, &path, folder, name, rel, &meta)?;
                if retained {
                    out.members.insert(rel.into(), Stamp::of(&meta));
                }
                out.holds_records |= record;
            }
        }
        Ok(())
    }
    let mut out = Census::default();
    walk(root, root, Folder::Root, &mut out, 0)?;
    Ok(out)
}
