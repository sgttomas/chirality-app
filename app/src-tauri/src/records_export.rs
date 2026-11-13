//! RS §13.8 / U-STORE-5: byte-preserving, verified BagIt exports.
//! The package is unsigned until App signing. No import or disposal is implied.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};
use std::fs::OpenOptions;
use std::io::{Read, Write};
use std::os::unix::fs::{DirBuilderExt, OpenOptionsExt};
use std::path::{Component, Path, PathBuf};

const DECLARATION: &[u8] = b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n";
const HEADS: &str = "records-chain-heads.json";
const ADMIN: &str = "records-administration.json";
const TAGS: &[&str] = &["bagit.txt", "bag-info.txt", "manifest-sha256.txt", HEADS, "verify.py", ADMIN];
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
    let mut f = OpenOptions::new().write(true).create_new(true).mode(0o600).open(path).map_err(io)?;
    f.write_all(bytes).map_err(io)?;
    f.sync_all().map_err(io)
}
fn manifest(folder: &Path, paths: impl Iterator<Item = String>) -> Result<Vec<u8>, String> {
    let mut out = String::new();
    for path in paths { out.push_str(&format!("{}  {}\n", digest(&folder.join(&path))?, encode(&path))); }
    Ok(out.into_bytes())
}
/// The chain-head tag's profiles. 0.1 recorded a head for each record log;
/// 0.2 added the role supply log's; 0.3 (written by this build) adds to each
/// log's head the reader's account of its lines, `setAside` and `torn`
/// (`record_lines::chain_account`), and to a role supply log the reader could
/// not take, the `line` and `kind` of its fault. Earlier profiles are read.
#[derive(Clone, Copy, PartialEq)]
enum Profile { V01, V02, V03 }
impl Profile {
    fn version(self) -> &'static str { match self { Profile::V01 => "0.1", Profile::V02 => "0.2", Profile::V03 => "0.3" } }
    fn of(version: Option<&str>) -> Result<Self, String> {
        match version { Some("0.1") => Ok(Profile::V01), Some("0.2") => Ok(Profile::V02), Some("0.3") => Ok(Profile::V03), _ => Err("unsupported chain-head tag profile".into()) }
    }
    fn describes(self) -> &'static str {
        match self {
            Profile::V01 => "0.1: legacy RS-only heads; role supply log heads unestablished",
            Profile::V02 => "0.2: RS and role supply log heads",
            Profile::V03 => "0.3: RS and role supply log heads, with the reader's account of each log's lines",
        }
    }
}
fn heads_profile(folder: &Path, paths: impl Iterator<Item = String>, profile: Profile) -> Value {
    let (roles, account) = (profile != Profile::V01, profile == Profile::V03);
    let logs: Vec<Value> = paths.filter(|p| p.ends_with(".jsonl") && (p.starts_with("runs/") || p.starts_with("acts/") || p == crate::records_store::REGISTERED_COPY || (roles && p == crate::role_observations::RELATIVE_LOG)))
        .map(|path| {
            let file = folder.join(&path);
            let chain = match (path == crate::role_observations::RELATIVE_LOG, account) {
                (true, true) => crate::role_observations::copied_chain_account(&file),
                (true, false) => crate::role_observations::copied_chain_head(&file),
                (false, true) => crate::record_lines::chain_account(&file),
                (false, false) => crate::record_lines::chain_head(&file),
            };
            json!({"log":path,"chain":chain})
        }).collect();
    json!({"format":"chirality.records-export-chain-heads","formatVersion":profile.version(),"method":crate::record_lines::LINE_METHOD,"logs":logs})
}
fn heads(folder: &Path, paths: impl Iterator<Item = String>) -> Value { heads_profile(folder,paths,Profile::V03) }
/// Puts `from` in place at `to` by an exclusive rename: never replaces a file
/// already at `to` (also used for a new records store line file).
pub(crate) fn publish(from: &Path, to: &Path) -> Result<(), String> {
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
    let home = crate::records_store::readable_home(project)?;
    let source = home.attachment.dir.clone().ok_or("project has no attached records in the store; nothing exported")?;
    crate::records_store::export_permitted(&source,&home.attachment.root)?;
    let project_id = home.attachment.project.ok_or("project identity unavailable")?;
    crate::storage::check_path(destination)?;
    let parent = std::fs::canonicalize(destination.parent().ok_or("export has no parent folder")?).map_err(io)?;
    let destination = parent.join(destination.file_name().ok_or("export has no folder name")?);
    let store = crate::records_store::store_root().ok_or("records store unavailable")?;
    if parent.starts_with(&store) || parent.starts_with(&home.attachment.root) { return Err("export destination must be outside the records store and project".into()); }
    if std::fs::symlink_metadata(&destination).is_ok() { return Err("export destination already exists; nothing overwritten".into()); }
    // Capture writers acquire capture ownership before record ownership; keep
    // that same order here. Other changes are caught by the final census.
    let _captures = crate::storage::read_lock(&source.join("captures/.capture.lock"))?;
    let _writers = crate::storage::read_lock(&source.join(".writer.lock"))?;
    // A waiting importer may have completed or stopped after eligibility was
    // first checked. Fleet payload never bypasses the ordinary import state.
    crate::records_store::export_permitted(&source,&home.attachment.root)?;
    let before = files(&source, true)?;
    let administration=crate::records_retention::export_snapshot(&source,&project_id,None)?;
    let stage = parent.join(crate::util::opaque_id(".records-export-")?);
    std::fs::DirBuilder::new().mode(0o700).create(&stage).map_err(io)?;
    let result = (|| {
        std::fs::DirBuilder::new().mode(0o700).create(stage.join("data")).map_err(io)?;
        for (rel, stamp) in &before {
            let input = source.join(rel);
            crate::storage::check_path(&input)?;
            let mut f = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK).open(&input).map_err(io)?;
            if crate::records_index::Stamp::of(&f.metadata().map_err(io)?) != *stamp { return Err("records changed while preparing export; try again".into()); }
            let output = stage.join("data").join(rel);
            std::fs::DirBuilder::new().recursive(true).mode(0o700).create(output.parent().ok_or("export member has no parent")?).map_err(io)?;
            let mut copy = OpenOptions::new().write(true).create_new(true).mode(0o600).open(&output).map_err(io)?;
            std::io::copy(&mut f, &mut copy).map_err(io)?;
            copy.sync_all().map_err(io)?;
            if crate::records_index::Stamp::of(&f.metadata().map_err(io)?) != *stamp || digest(&input)? != digest(&output)? { return Err("records changed during export; try again".into()); }
        }
        if files(&source, true)? != before { return Err("records changed during export; try again".into()); }
        write(&stage.join("bagit.txt"), DECLARATION)?;
        write(&stage.join("bag-info.txt"), format!("External-Identifier: {project_id}\nChirality-Signing: unsigned; waits for App signing (OI-011)\n").as_bytes())?;
        write(&stage.join("manifest-sha256.txt"), &manifest(&stage, before.keys().map(|p| format!("data/{p}")))?)?;
        write(&stage.join(HEADS), &serde_json::to_vec_pretty(&heads(&stage.join("data"), before.keys().cloned())).map_err(|e| e.to_string())?)?;
        if administration!=crate::records_retention::export_snapshot(&source,&project_id,None)? {return Err("administration changed during export; try again".into());}
        write(&stage.join(ADMIN),&serde_json::to_vec_pretty(&administration).map_err(|e|e.to_string())?)?;
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
        let limited = verified["logIntegrity"]["state"] == LIMITED;
        Ok(json!({"state":if limited {"export created: package bytes verified; log integrity limited"} else {"verified export created"},"logIntegrity":verified["logIntegrity"],"folder":destination,"files":before.len(),"projectId":project_id,"verification":verified,"signing":"unsigned; waits for App signing (OI-011)"}))
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
    let current_profile: BTreeSet<String>=TAGS.iter().map(|p|p.to_string()).collect();
    let legacy_profile: BTreeSet<String>=TAGS.iter().filter(|p|**p!=ADMIN).map(|p|p.to_string()).collect();
    if tags!=current_profile && tags!=legacy_profile {return Err("tag inventory differs from export profile".into());}
    let administration=if tags.contains(ADMIN){
        let v:Value=serde_json::from_slice(&read_tag(&folder.join(ADMIN))?).map_err(|e|e.to_string())?;
        let project:Value=serde_json::from_slice(&read_tag(&folder.join("data/project.json"))?).map_err(|e|e.to_string())?;
        if v["format"]!="chirality.records-administration-snapshot" || v["formatVersion"]!="0.1" || v["projectId"]!=project["projectId"] || v["projectKey"]!=crate::storage::key(project["projectId"].as_str().ok_or("payload project identity absent")?) || !v["events"].is_object() || v["sequence"].as_u64().is_none(){return Err("administration snapshot identity/profile invalid".into());}
        "protected prior administrative bytes; unsigned"
    }else{"unknown: legacy package has no administrative history snapshot"};
    let mut inventory = payload.clone();
    inventory.extend(tags);
    inventory.insert("tagmanifest-sha256.txt".into());
    if file_inventory.into_keys().collect::<BTreeSet<_>>() != inventory { return Err("package inventory differs from manifests".into()); }
    let expected: Value = serde_json::from_slice(&read_tag(&folder.join(HEADS))?).map_err(|e| e.to_string())?;
    let profile=Profile::of(expected["formatVersion"].as_str())?;
    let role_heads=profile!=Profile::V01;
    let names=||actual.iter().map(|p| p.strip_prefix("data/").unwrap().to_owned());
    let observed = heads_profile(&folder.join("data"), names(), profile);
    if observed != expected { return Err("copied log chain heads differ from export manifest".into()); }
    // What the reader finds in the payload now, with its account of each
    // log's lines, whatever profile the package was written in: a line set
    // aside is an integrity limit for a package of any profile.
    let found = if profile==Profile::V03 { observed } else { heads_profile(&folder.join("data"), names(), Profile::V03) };
    // Two statements, never one: the bytes agree with the manifests and the
    // recorded heads; and, separately, whether a log's own integrity is
    // limited. A chain already broken in the store at export is carried as
    // it stood: the package is not refused, and its log is not whole.
    let integrity = log_integrity(&found, !role_heads && actual.contains(&format!("data/{}", crate::role_observations::RELATIVE_LOG)));
    let limited = integrity["state"] == LIMITED;
    Ok(json!({"state":if limited {"package bytes consistent; log integrity limited"} else {"package bytes consistent; no chain recorded broken"},
        "packageBytes":"consistent with the manifests and the recorded chain heads",
        // Its own statement: equal bytes say each log is the log that was
        // exported, and nothing about whether its records are intact.
        "exportedLogs":if profile==Profile::V03 {"each chained log is byte for byte the log the chain-head tag records; this says it is the log that was exported, not that its records are intact"} else {"not pinned: this package's chain-head profile does not record each log's bytes in its tag"},
        "logIntegrity":integrity,
        "files":payload.len(),"administration":administration,"chainHeadProfile":profile.describes(),"signing":"unsigned; no origin or human act authenticated"}))
}
/// The two states a build that states log integrity writes.
pub(crate) const LIMITED: &str = "limited";
/// What is said of a line the reader set aside, after its log and line.
const SET_ASIDE: &str = " was set aside by the App as invalid: it is not read as a record, and its own link is not examined";
/// What is said of an unclosed final part, after its log and its length.
const UNCLOSED: &str = " bytes after the last complete line";
pub(crate) const WHOLE: &str = "no chain recorded broken";
/// What a package's chain-head tag records about its logs' own integrity,
/// apart from whether the package's bytes are consistent: each chain the
/// store's reader reported broken at export, as `<log>: chain broken at line
/// N: ...`, and each log whose chain it could not read.
pub(crate) fn log_integrity(heads: &Value, role_log_without_head: bool) -> Value {
    // Anything not stated, not readable or not checked is a limit: only a
    // head that states an empty list of breaks counts as not recorded broken.
    let mut limits: Vec<String> = Vec::new();
    match heads["logs"].as_array() {
        None => limits.push("NOT CHECKED: the chain-head tag lists no logs".into()),
        Some(items) => for item in items {
            let log = item["log"].as_str().unwrap_or("a log the tag does not name");
            let chain = &item["chain"];
            if let Some(state) = chain["state"].as_str() {
                limits.push(format!("{log}: the App's reader could not read this log's chain ({state}: {}){}", chain["error"].as_str().unwrap_or("no cause recorded"),
                    match (chain["line"].as_u64(), chain["kind"].as_str()) { (Some(line), Some(kind)) => format!("; the fault is at line {line}: {kind}"), _ => String::new() }));
            } else if let Some(broken) = chain["broken"].as_array() {
                // The reader names a log by its file name; what follows that
                // name is the break. Taken by position, never by its words.
                let name = format!("{}: ", if log == crate::role_observations::RELATIVE_LOG { "role supply observations" } else { log.rsplit('/').next().unwrap_or(log) });
                limits.extend(broken.iter().map(|limit| match limit.as_str() {
                    Some(limit) => format!("{log}: {}", limit.strip_prefix(name.as_str()).unwrap_or(limit)),
                    None => format!("{log}: a recorded break that is not text"),
                }));
            } else {
                limits.push(format!("{log}: NOT CHECKED: the package records no list of breaks for this chain"));
            }
            // A line the reader set aside is a limit, never part of a clean result.
            limits.extend(chain["setAside"].as_array().into_iter().flatten().map(|line| format!("{log}: line {line}{SET_ASIDE}")));
            // A partly present unit at the log's end is a limit too (AC-009).
            if let Some(bytes) = chain["unclosedEnd"].as_u64() { limits.push(format!("{log}: partial entry at end (not read): {bytes}{UNCLOSED}")); }
        },
    }
    if role_log_without_head {
        limits.push(format!("{}: NOT CHECKED: this package's chain-head profile (0.1) records no head for this log to compare with", crate::role_observations::RELATIVE_LOG));
    }
    if limits.is_empty() { json!({"state":WHOLE}) } else { json!({"state":LIMITED,"limits":limits}) }
}
/// A stored `logIntegrity` member as a reader takes it. A record written
/// before the member existed does not state it: that reads as "not stated",
/// never as no chain recorded broken.
pub(crate) fn stored_log_integrity(export: &Value) -> Value {
    // Only the two forms this build writes are read, whole: the clean state
    // with nothing else, or the limited state with at least one limit, each
    // a text. Anything else, malformed or self-contradictory, is not stated.
    let Some(members) = export.get("logIntegrity").and_then(Value::as_object) else { return json!({"state":"not stated"}) };
    let whole = members.len() == 1 && members.get("state").is_some_and(|s| s == WHOLE);
    let limited = members.len() == 2 && members.get("state").is_some_and(|s| s == LIMITED)
        && members.get("limits").and_then(Value::as_array).is_some_and(|limits| !limits.is_empty() && limits.iter().all(|l| l.as_str().is_some_and(|t| !t.is_empty())));
    if whole || limited { Value::Object(members.clone()) } else { json!({"state":"not stated"}) }
}
/// What a person is shown where a package they are verifying, importing or
/// relying on carries limits on log integrity; `None` when there is none.
/// Each limit is what the App's reader found in the package's logs, unless
/// the limit itself is marked NOT CHECKED. Nothing is said of when or why.
pub(crate) fn integrity_statement(integrity: &Value) -> Option<String> {
    if integrity["state"] == "not stated" {
        return Some("Log integrity: NOT STATED. Package bytes consistent. No statement of log integrity is recorded here.".into());
    }
    let limits: Vec<&str> = integrity["limits"].as_array()?.iter().filter_map(Value::as_str).collect();
    (integrity["state"] == LIMITED).then(|| format!("Log integrity: LIMITED. Package bytes consistent. {} limit(s), found by the App's reader unless marked NOT CHECKED: {}.",
        limits.len(), limits.join("; ")))
}
/// The same in a bounded form for a native confirmation's summary: the
/// number of limits, and where each is named. No limit is quoted or read
/// here, so nothing in a limit's own text can be taken for a log or a line.
pub(crate) fn integrity_summary(integrity: &Value) -> Option<String> {
    if integrity["state"] == "not stated" {
        return integrity_statement(integrity);
    }
    if integrity["state"] != LIMITED { return None; }
    let count = integrity["limits"].as_array()?.len();
    Some(format!("Log integrity: LIMITED. Package bytes consistent. {count} limit(s); each is named in full in the App under this confirmation."))
}
/// The log integrity recorded by the chain-head tag of a package this module
/// has verified (`verify`).
pub(crate) fn package_log_integrity(folder: &Path) -> Result<Value, String> {
    let heads: Value = serde_json::from_slice(&read_tag(&folder.join(HEADS))?).map_err(|e| e.to_string())?;
    let profile = Profile::of(heads["formatVersion"].as_str())?;
    let data = folder.join("data");
    let names: Vec<String> = files(&data, false)?.into_keys().collect();
    let role_log = names.iter().any(|name| name == crate::role_observations::RELATIVE_LOG);
    // Read from the payload, with the reader's account, for any profile.
    Ok(log_integrity(&heads_profile(&data, names.into_iter(), Profile::V03), role_log && profile == Profile::V01))
}
#[cfg(test)]
thread_local! {
    /// Makes `matches_current` write its result as a build before the
    /// `logIntegrity` member did (a stored disposal entry of that age).
    pub(crate) static BEFORE_LOG_INTEGRITY: std::cell::Cell<bool> = const { std::cell::Cell::new(false) };
}

/// A verified bag must match every current retained payload byte, not just RS
/// heads. Recovery accepts only an unchanged subset of the original complete bag.
pub(crate) fn matches_current(source:&Path,folder:&Path,remaining:bool)->Result<Value,String>{
    crate::storage::check_path(folder)?;
    let folder=std::fs::canonicalize(folder).map_err(io)?;
    let store=source.parent().and_then(Path::parent).ok_or("project source has no store")?;
    if folder.starts_with(store) {return Err("the export must survive outside the records store".into());}
    let verified=verify(&folder)?;
    let admin:Value=serde_json::from_slice(&read_tag(&folder.join(ADMIN)).map_err(|_|"legacy export has unknown administrative history; create a current export before disposal".to_owned())?).map_err(|e|e.to_string())?;
    let project_id=admin["projectId"].as_str().ok_or("export project identity missing")?;
    let prior=if remaining {crate::records_retention::view(source)["disposal"]["sequence"].as_u64().and_then(|seq|seq.checked_sub(1))}else{None};
    if remaining && prior.is_none(){return Err("original disposal context absent".into());}
    if admin!=crate::records_retention::export_snapshot(source,project_id,prior)? {return Err("export administrative history is stale or unrelated; create a current export".into());}
    let exported=files(&folder.join("data"),false)?;
    // Only a payload that is not there is an empty remainder; one that cannot
    // be examined is never verified as empty (`present`).
    let before=if present(source)?{files(source,true)?}else if remaining{BTreeMap::new()}else{return Err("current project payload unavailable".into());};
    if (!remaining && before.keys().collect::<Vec<_>>()!=exported.keys().collect::<Vec<_>>()) || before.keys().any(|k|!exported.contains_key(k)) {return Err("verified export does not cover the current complete project payload".into());}
    let mut payload=BTreeMap::new();
    for (rel,stamp) in &before {
        let input=source.join(rel);
        let hash=digest(&input)?;
        if hash!=digest(&folder.join("data").join(rel))? {return Err(format!("verified export is stale or unrelated: {rel}"));}
        if crate::records_index::Stamp::of(&std::fs::metadata(&input).map_err(io)?)!=*stamp {return Err("payload changed during verification".into());}
        payload.insert(rel.clone(),json!({"sha256":hash,"bytes":std::fs::metadata(input).map_err(io)?.len()}));
    }
    if present(source)? && files(source,true)?!=before {return Err("payload inventory changed during verification".into());}
    // tagmanifest hashes the payload manifest, chain-head tag and other tags.
    let identity=digest(&folder.join("tagmanifest-sha256.txt"))?;
    verify(&folder)?;
    if identity!=digest(&folder.join("tagmanifest-sha256.txt"))? {return Err("export changed during verification".into());}
    let bytes=serde_json::to_vec(&payload).map_err(|e|e.to_string())?;
    // Recorded with a disposal act (decided by App Agent 0, 2026-11-12): what
    // the export relied on states about its logs' integrity, apart from its
    // bytes matching. Always written; a reader takes its absence as not stated.
    let integrity=package_log_integrity(&folder)?;
    let mut out=json!({"folder":folder,"folderIdentity":{ "device":std::os::unix::fs::MetadataExt::dev(&std::fs::metadata(&folder).map_err(io)?),"inode":std::os::unix::fs::MetadataExt::ino(&std::fs::metadata(&folder).map_err(io)?)},"identity":identity,"identityMethod":"sha256 exact tagmanifest bytes","payload":{"files":payload.len(),"identity":crate::util::sha256_hex(&bytes),"identityMethod":"sha256 sorted relative file names, exact byte hashes and lengths"},"administrationIdentity":digest(&folder.join(ADMIN))?,"chainHeadProfile":verified["chainHeadProfile"],"verification":"complete package bytes, prior administration and declared chain-head profile verified; matches current store payload"});
    #[cfg(test)]
    if BEFORE_LOG_INTEGRITY.with(|b|b.get()) {return Ok(out);}
    // Read alone, this sentence speaks of bytes and says what it does not cover.
    out["verification"]=json!(format!("package bytes, prior administration and recorded chain heads agree with the manifests and match the current store payload; separately, log integrity: {}",
        match integrity["limits"].as_array() { Some(limits) => format!("limited ({}, each named in logIntegrity)", limits.len()), None => WHOLE.to_owned() }));
    out["logIntegrity"]=integrity;
    Ok(out)
}

#[cfg(test)]
pub(crate) fn payload_paths_for_test(dir:&Path)->Vec<PathBuf>{files(dir,true).unwrap().into_keys().map(|p|dir.join(p)).collect()}
#[cfg(test)]
pub(crate) fn legacy_for_test(dir:&Path){std::fs::remove_file(dir.join(ADMIN)).unwrap();std::fs::write(dir.join("tagmanifest-sha256.txt"),manifest(dir,TAGS.iter().filter(|p|**p!=ADMIN).map(|p|p.to_string())).unwrap()).unwrap();}

#[cfg(test)]
#[path = "records_export_tests.rs"]
mod tests;

/// Whether `path` is there, for disposal and its staging: only NotFound is
/// absence. A path that cannot be examined is an error, never absent, so
/// nothing that could not be seen is passed over as gone.
pub(crate) fn present(path: &Path) -> Result<bool, String> {
    match std::fs::symlink_metadata(path) {
        Ok(_) => Ok(true),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(false),
        Err(e) => Err(format!("{} could not be examined: {e}; whether it is there is not known", path.display())),
    }
}
/// Recovery's private staging folder contains exact original member names.
/// A raced pathname is first moved exclusively, then checked in its private
/// location. Unverified bytes survive there rather than being unlinked.
pub(crate) fn staged_payload(folder: &Path, bag: &Path) -> Result<Value, String> {
    let exported = files(&bag.join("data"), false)?;
    let inventory = if present(folder)? {
        files(folder, false)?
    } else {
        BTreeMap::new()
    };
    let mut payload = BTreeMap::new();
    for rel in inventory.keys() {
        let member = folder.join(rel);
        if excluded(Path::new(rel)) {
            let meta = std::fs::symlink_metadata(&member).map_err(io)?;
            if !meta.is_file() || meta.len() != 0 {
                return Err(format!(
                    "unexpected owning control bytes preserved: {}",
                    member.display()
                ));
            }
        } else if !exported.contains_key(rel)
            || digest(&member)? != digest(&bag.join("data").join(rel))?
        {
            return Err(format!(
                "unverified staged member preserved: {}",
                member.display()
            ));
        }
        payload.insert(rel,json!({"bytes":std::fs::metadata(&member).map_err(io)?.len(),"sha256":digest(&member)?}));
    }
    if present(folder)? && files(folder, false)? != inventory {
        return Err("staged payload changed during verification".into());
    }
    Ok(
        json!({"files":payload.len(),"identity":crate::util::sha256_hex(&serde_json::to_vec(&payload).map_err(|e|e.to_string())?)}),
    )
}
fn remove_empty_tree(folder: &Path) -> Result<(), String> {
    if !present(folder)? {
        return Ok(());
    }
    crate::storage::check_path(folder)?;
    for entry in std::fs::read_dir(folder).map_err(io)? {
        let path = entry.map_err(io)?.path();
        let meta = std::fs::symlink_metadata(&path).map_err(io)?;
        if !meta.is_dir() {
            return Err(format!(
                "unexpected remaining member preserved: {}",
                path.display()
            ));
        }
        remove_empty_tree(&path)?;
    }
    // remove_dir, rather than remove_dir_all: a new entry prevents completion.
    std::fs::remove_dir(folder).map_err(|e| {
        format!(
            "nonempty/changed folder retained: {}: {e}",
            folder.display()
        )
    })
}
#[cfg(test)]
thread_local! {pub(crate) static AFTER_MEMBER_STAGE:std::cell::RefCell<Option<Box<dyn FnOnce()>>> = const {std::cell::RefCell::new(None)};}

fn manifest_hashes(bytes: &[u8]) -> Result<BTreeMap<String, String>, String> {
    let mut out = BTreeMap::new();
    for line in std::str::from_utf8(bytes)
        .map_err(|e| e.to_string())?
        .lines()
    {
        let (hash, path) = line.split_once("  ").ok_or("invalid frozen manifest")?;
        if hash.len() != 64 || !hash.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err("invalid frozen checksum".into());
        }
        if out
            .insert(decode(path)?, hash.to_ascii_lowercase())
            .is_some()
        {
            return Err("duplicate frozen member".into());
        }
    }
    Ok(out)
}
pub(crate) fn dispose_members(
    source: &Path,
    bag: &Path,
    stage: &Path,
    identity: &str,
) -> Result<(), String> {
    let tags = read_tag(&bag.join("tagmanifest-sha256.txt"))?;
    if crate::util::sha256_hex(&tags) != identity {
        return Err("original export changed; nothing more disposed".into());
    }
    let tag_hashes = manifest_hashes(&tags)?;
    let payload_bytes = read_tag(&bag.join("manifest-sha256.txt"))?;
    if tag_hashes.get("manifest-sha256.txt") != Some(&crate::util::sha256_hex(&payload_bytes)) {
        return Err("original payload manifest changed; nothing more disposed".into());
    }
    let frozen = manifest_hashes(&payload_bytes)?;
    let exported: BTreeMap<String, String> = frozen
        .into_iter()
        .map(|(name, hash)| {
            Ok((
                name.strip_prefix("data/")
                    .ok_or("unexpected frozen payload member")?
                    .to_string(),
                hash,
            ))
        })
        .collect::<Result<_, String>>()?;
    staged_payload(stage, bag)?;
    crate::storage::ensure_directory(stage)?;
    let mut expected: Vec<String> = exported.keys().cloned().collect();
    expected.extend([".writer.lock".into(), "captures/.capture.lock".into()]);
    for rel in expected {
        let input = source.join(&rel);
        let staged = stage.join(&rel);
        if !present(&staged)? && present(&input)? {
            crate::storage::check_path(&input)?;
            let meta = std::fs::symlink_metadata(&input).map_err(io)?;
            if !meta.is_file() {
                return Err(format!("unexpected member retained: {}", input.display()));
            }
            crate::storage::ensure_directory(
                staged.parent().ok_or("staged member has no parent")?,
            )?;
            publish(&input, &staged).map_err(|e| format!("disposal member staging: {e}"))?;
            crate::storage::sync_dir(input.parent().unwrap())?;
            crate::storage::sync_dir(staged.parent().unwrap())?;
            #[cfg(test)]
            if let Some(hook) = AFTER_MEMBER_STAGE.with(|h| h.borrow_mut().take()) {
                hook();
            }
        }
        if present(&staged)? {
            crate::storage::check_path(&staged)?;
            let before = std::fs::symlink_metadata(&staged).map_err(io)?;
            if !before.is_file() {
                return Err(format!(
                    "nonregular staged bytes preserved: {}",
                    staged.display()
                ));
            }
            let stamp = crate::records_index::Stamp::of(&before);
            let expected = if excluded(Path::new(&rel)) {
                if before.len() != 0 {
                    return Err(format!(
                        "unexpected owning control bytes preserved: {}",
                        staged.display()
                    ));
                }
                digest(&staged)?
            } else {
                let hash = exported.get(&rel).ok_or("frozen member absent")?.clone();
                if digest(&bag.join("tagmanifest-sha256.txt"))? != identity
                    || digest(&bag.join("data").join(&rel))? != hash
                {
                    return Err(format!(
                        "original export member changed; staged bytes retained: {}",
                        staged.display()
                    ));
                }
                hash
            };
            if digest(&staged)? != expected
                || crate::records_index::Stamp::of(&std::fs::symlink_metadata(&staged).map_err(io)?)
                    != stamp
            {
                return Err(format!(
                    "changed/unverified staged bytes preserved: {}",
                    staged.display()
                ));
            }
            std::fs::remove_file(&staged).map_err(io)?;
            crate::storage::sync_dir(staged.parent().unwrap())?;
        }
        if present(&input)? {
            return Err(format!(
                "member reappeared after staging; bytes retained: {}",
                input.display()
            ));
        }
    }
    // Unknown files are never swept, in the original tree or private staging.
    remove_empty_tree(source)?;
    remove_empty_tree(stage)?;
    crate::storage::sync_dir(source.parent().ok_or("project source has no parent")?)?;
    crate::storage::sync_dir(stage.parent().ok_or("staging has no parent")?)
}
/// Rewrites a package's chain-head tag in an earlier profile, as a build of
/// that profile exported it, and its tag manifest with it.
#[cfg(test)]
pub(crate) fn reprofile_as_for_test(folder:&Path,version:&str){
    let paths=files(&folder.join("data"),false).unwrap().into_keys().collect::<Vec<_>>();
    std::fs::write(folder.join(HEADS),serde_json::to_vec_pretty(&heads_profile(&folder.join("data"),paths.into_iter(),Profile::of(Some(version)).unwrap())).unwrap()).unwrap();
    let tags:Vec<String>=TAGS.iter().filter(|p|folder.join(p).exists()).map(|p|p.to_string()).collect();
    std::fs::write(folder.join("tagmanifest-sha256.txt"),manifest(folder,tags.into_iter()).unwrap()).unwrap();
}
#[cfg(test)]
pub(crate) fn reprofile_for_test(folder:&Path){
    let paths=files(&folder.join("data"),false).unwrap().into_keys().collect::<Vec<_>>();
    std::fs::write(folder.join("manifest-sha256.txt"),manifest(folder,paths.iter().map(|p|format!("data/{p}"))).unwrap()).unwrap();
    std::fs::write(folder.join(HEADS),serde_json::to_vec_pretty(&heads(&folder.join("data"),paths.into_iter())).unwrap()).unwrap();
    std::fs::write(folder.join("tagmanifest-sha256.txt"),manifest(folder,TAGS.iter().map(|p|p.to_string())).unwrap()).unwrap();
}
