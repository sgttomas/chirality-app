//! RS §13.8 / U-STORE-5: byte-preserving, verified BagIt exports.
//! The package is unsigned until App signing. No import or disposal is implied.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::fs::OpenOptions;
use std::io::{Read, Write};
use std::os::unix::fs::OpenOptionsExt;
use std::path::{Component, Path, PathBuf};

const DECLARATION: &[u8] = b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n";
const HEADS: &str = "records-chain-heads.json";
const TAGS: &[&str] = &["bagit.txt", "bag-info.txt", "manifest-sha256.txt", HEADS, "verify.py"];
const VERIFIER: &[u8] = include_bytes!("../../tools/verify_records_bag.py");

fn io(e: std::io::Error) -> String { e.to_string() }
fn digest(path: &Path) -> Result<String, String> {
    let mut f = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(path).map_err(io)?;
    if !f.metadata().map_err(io)?.is_file() { return Err("package member is not a regular file".into()); }
    let mut hash = Sha256::new();
    let mut bytes = [0; 65536];
    loop { let n = f.read(&mut bytes).map_err(io)?; if n == 0 { break; } hash.update(&bytes[..n]); }
    Ok(format!("{:x}", hash.finalize()))
}
fn read_tag(path: &Path) -> Result<Vec<u8>, String> {
    crate::storage::check_path(path)?;
    let mut f = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(path).map_err(io)?;
    if !f.metadata().map_err(io)?.is_file() { return Err("package tag is not a regular file".into()); }
    let mut bytes = Vec::new(); f.read_to_end(&mut bytes).map_err(io)?; Ok(bytes)
}
fn relative(path: &Path) -> Result<String, String> {
    if path.components().any(|c| !matches!(c, Component::Normal(_))) { return Err("unsafe package path".into()); }
    path.to_str().map(str::to_owned).ok_or_else(|| "package path is not UTF-8".into())
}
fn encode(path: &str) -> String { path.replace('%', "%25").replace('\r', "%0D").replace('\n', "%0A") }
fn decode(path: &str) -> Result<String, String> {
    let mut out = String::new();
    let mut chars = path.chars();
    while let Some(c) = chars.next() {
        if c != '%' { out.push(c); continue; }
        let code = [chars.next().ok_or("bad manifest escape")?, chars.next().ok_or("bad manifest escape")?].iter().collect::<String>();
        out.push(match code.as_str() { "25" => '%', "0D" => '\r', "0A" => '\n', _ => return Err("bad manifest escape".into()) });
    }
    relative(Path::new(&out))?;
    Ok(out)
}
fn excluded(rel: &Path) -> bool {
    // Omit only actual owning controls. Imported connector publication files
    // (including .tmp/.lock names) are retained evidence, not scratch to drop.
    rel == Path::new(".writer.lock") || rel == Path::new("captures/.capture.lock")
}
fn files(root: &Path, omit_controls: bool) -> Result<BTreeMap<String, crate::records_index::Stamp>, String> {
    fn walk(root: &Path, dir: &Path, omit: bool, out: &mut BTreeMap<String, crate::records_index::Stamp>) -> Result<(), String> {
        crate::storage::check_path(dir)?;
        for item in std::fs::read_dir(dir).map_err(io)? {
            let path = item.map_err(io)?.path();
            let rel = path.strip_prefix(root).map_err(|e| e.to_string())?;
            if omit && excluded(rel) { continue; }
            let meta = std::fs::symlink_metadata(&path).map_err(io)?;
            if meta.is_dir() { walk(root, &path, omit, out)?; }
            else if meta.is_file() { out.insert(relative(rel)?, crate::records_index::Stamp::of(&meta)); }
            else { return Err(format!("unsupported or linked export member: {}", path.display())); }
        }
        Ok(())
    }
    let mut out = BTreeMap::new();
    walk(root, root, omit_controls, &mut out)?;
    Ok(out)
}
fn write(path: &Path, bytes: &[u8]) -> Result<(), String> {
    let mut f = OpenOptions::new().write(true).create_new(true).open(path).map_err(io)?;
    f.write_all(bytes).map_err(io)?;
    f.sync_all().map_err(io)
}
fn manifest(folder: &Path, paths: impl Iterator<Item = String>) -> Result<Vec<u8>, String> {
    let mut out = String::new();
    for path in paths { out.push_str(&format!("{}  {}\n", digest(&folder.join(&path))?, encode(&path))); }
    Ok(out.into_bytes())
}
fn heads(folder: &Path, paths: impl Iterator<Item = String>) -> Value {
    let logs: Vec<Value> = paths.filter(|p| p.ends_with(".jsonl") && (p.starts_with("runs/") || p.starts_with("acts/") || p == crate::records_store::REGISTERED_COPY))
        .map(|path| json!({"log":path,"chain":crate::record_lines::chain_head(&folder.join(&path))})).collect();
    json!({"format":"chirality.records-export-chain-heads","formatVersion":"0.1","method":crate::record_lines::LINE_METHOD,"logs":logs})
}
fn publish(from: &Path, to: &Path) -> Result<(), String> {
    use std::os::unix::ffi::OsStrExt;
    let from = std::ffi::CString::new(from.as_os_str().as_bytes()).map_err(|e| e.to_string())?;
    let to = std::ffi::CString::new(to.as_os_str().as_bytes()).map_err(|e| e.to_string())?;
    #[cfg(target_os = "macos")]
    let rc = unsafe { libc::renamex_np(from.as_ptr(), to.as_ptr(), libc::RENAME_EXCL) };
    #[cfg(target_os = "linux")]
    let rc = unsafe { libc::renameat2(libc::AT_FDCWD, from.as_ptr(), libc::AT_FDCWD, to.as_ptr(), libc::RENAME_NOREPLACE) };
    #[cfg(not(any(target_os = "macos", target_os = "linux")))]
    return Err("exclusive export publication is unavailable on this platform".into());
    #[cfg(any(target_os = "macos", target_os = "linux"))]
    if rc != 0 { return Err(format!("export publication: {}", std::io::Error::last_os_error())); }
    Ok(())
}

/// Exports the already attached project's store to a new folder. No identity
/// is minted by this read; import-needed and identity refusals stay explicit.
pub fn export(project: &Path, destination: &Path) -> Result<Value, String> {
    let home = crate::records_store::home(project)?;
    let source = home.attachment.dir.ok_or("project has no attached records in the store; nothing exported")?;
    if !home.store_mode { return Err("project records need import before export".into()); }
    let project_id = home.attachment.project.ok_or("project identity unavailable")?;
    crate::storage::check_path(destination)?;
    let parent = std::fs::canonicalize(destination.parent().ok_or("export has no parent folder")?).map_err(io)?;
    let destination = parent.join(destination.file_name().ok_or("export has no folder name")?);
    let store = crate::records_store::store_root().ok_or("records store unavailable")?;
    if parent.starts_with(&store) || parent.starts_with(&home.attachment.root) { return Err("export destination must be outside the records store and project".into()); }
    if std::fs::symlink_metadata(&destination).is_ok() { return Err("export destination already exists; nothing overwritten".into()); }
    // Capture writers acquire capture ownership before record ownership; keep
    // that same order here. Other changes are caught by the final census.
    let _captures = crate::storage::lock(&source.join("captures/.capture.lock"))?;
    let _writers = crate::records_store::writer_lock(&source, false)?;
    let before = files(&source, true)?;
    let stage = parent.join(crate::util::opaque_id(".records-export-")?);
    std::fs::create_dir(&stage).map_err(io)?;
    let result = (|| {
        std::fs::create_dir(stage.join("data")).map_err(io)?;
        for (rel, stamp) in &before {
            let input = source.join(rel);
            crate::storage::check_path(&input)?;
            let mut f = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&input).map_err(io)?;
            if crate::records_index::Stamp::of(&f.metadata().map_err(io)?) != *stamp { return Err("records changed while preparing export; try again".into()); }
            let output = stage.join("data").join(rel);
            std::fs::create_dir_all(output.parent().ok_or("export member has no parent")?).map_err(io)?;
            let mut copy = OpenOptions::new().write(true).create_new(true).open(&output).map_err(io)?;
            std::io::copy(&mut f, &mut copy).map_err(io)?;
            copy.sync_all().map_err(io)?;
            if crate::records_index::Stamp::of(&f.metadata().map_err(io)?) != *stamp || digest(&input)? != digest(&output)? { return Err("records changed during export; try again".into()); }
        }
        if files(&source, true)? != before { return Err("records changed during export; try again".into()); }
        write(&stage.join("bagit.txt"), DECLARATION)?;
        write(&stage.join("bag-info.txt"), format!("External-Identifier: {project_id}\nChirality-Signing: unsigned; waits for App signing (OI-011)\n").as_bytes())?;
        write(&stage.join("manifest-sha256.txt"), &manifest(&stage, before.keys().map(|p| format!("data/{p}")))?)?;
        write(&stage.join(HEADS), &serde_json::to_vec_pretty(&heads(&stage.join("data"), before.keys().cloned())).map_err(|e| e.to_string())?)?;
        write(&stage.join("verify.py"), VERIFIER)?;
        write(&stage.join("tagmanifest-sha256.txt"), &manifest(&stage, TAGS.iter().map(|s| s.to_string()))?)?;
        let verified = verify(&stage)?;
        // Flush folders before publication, deepest first.
        fn sync_dirs(path: &Path) -> Result<(), String> {
            for entry in std::fs::read_dir(path).map_err(io)? { let p = entry.map_err(io)?.path(); if p.is_dir() { sync_dirs(&p)?; } }
            crate::storage::sync_dir(path)
        }
        sync_dirs(&stage)?;
        publish(&stage, &destination)?;
        crate::storage::sync_dir(&parent).map_err(|e| format!("export published at {}; folder durability not established: {e}", destination.display()))?;
        Ok(json!({"state":"verified export created","folder":destination,"files":before.len(),"projectId":project_id,"verification":verified,"signing":"unsigned; waits for App signing (OI-011)"}))
    })();
    if stage.exists() { let _ = std::fs::remove_dir_all(stage); }
    result
}

fn check_manifest(folder: &Path, name: &str, payload: bool) -> Result<BTreeSet<String>, String> {
    let text = String::from_utf8(read_tag(&folder.join(name))?).map_err(|e| e.to_string())?;
    let mut seen = BTreeSet::new();
    for line in text.lines() {
        let (hash, encoded) = line.split_once("  ").ok_or("malformed SHA-256 manifest")?;
        let path = decode(encoded)?;
        if hash.len() != 64 || !hash.bytes().all(|b| b.is_ascii_hexdigit()) || path.starts_with("data/") != payload || (!payload && path.starts_with("tagmanifest-")) { return Err("invalid manifest member".into()); }
        if !seen.insert(path.clone()) { return Err("duplicate manifest member".into()); }
        crate::storage::check_path(&folder.join(&path))?;
        if digest(&folder.join(&path))? != hash.to_ascii_lowercase() { return Err(format!("checksum mismatch: {path}")); }
    }
    Ok(seen)
}
/// Verifies this App's complete export profile, including payload inventory,
/// tags and copied RS chain heads. Valid bytes do not confer act authenticity.
pub fn verify(folder: &Path) -> Result<Value, String> {
    crate::storage::check_path(folder)?;
    let file_inventory = files(folder, false)?;
    if read_tag(&folder.join("bagit.txt"))? != DECLARATION { return Err("unsupported BagIt declaration".into()); }
    let payload = check_manifest(folder, "manifest-sha256.txt", true)?;
    let actual: BTreeSet<String> = files(&folder.join("data"), false)?.keys().map(|p| format!("data/{p}")).collect();
    if actual != payload { return Err("payload inventory differs from manifest".into()); }
    let tags = check_manifest(folder, "tagmanifest-sha256.txt", false)?;
    if tags != TAGS.iter().map(|p| p.to_string()).collect() { return Err("tag inventory differs from export profile".into()); }
    let mut inventory = payload.clone();
    inventory.extend(tags);
    inventory.insert("tagmanifest-sha256.txt".into());
    if file_inventory.into_keys().collect::<BTreeSet<_>>() != inventory { return Err("package inventory differs from manifests".into()); }
    let expected: Value = serde_json::from_slice(&read_tag(&folder.join(HEADS))?).map_err(|e| e.to_string())?;
    let observed = heads(&folder.join("data"), actual.iter().map(|p| p.strip_prefix("data/").unwrap().to_owned()));
    if observed != expected { return Err("copied log chain heads differ from export manifest".into()); }
    Ok(json!({"state":"verified package bytes and chain heads","files":payload.len(),"signing":"unsigned; no origin or human act authenticated"}))
}

#[cfg(test)]
#[path = "records_export_tests.rs"]
mod tests;
