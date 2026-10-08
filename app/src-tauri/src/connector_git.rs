//! CGP-v0.1: transient exact object graph reads; no branch, pathspec or source account.
use crate::{
    attachments::native_path_identity,
    connector_git_process::{Control, Engine, Failure, Result},
    util::{now_rfc3339, sha256_hex},
};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, HashSet},
    fs,
    os::unix::{ffi::OsStrExt, fs::MetadataExt},
    path::{Component, Path, PathBuf},
};
#[derive(Clone)]
pub struct Side {
    pub bytes: Vec<u8>,
    pub view: Value,
    pub raw_objects: Vec<(String, Vec<u8>)>,
}
pub struct Completed {
    pub at: std::result::Result<Side, Failure>,
    pub since: Option<std::result::Result<Side, Failure>>,
    pub association: Value,
    pub engine: Value,
    pub request: Value,
}
impl Completed {
    pub fn view(&self) -> Value {
        fn side(s: &std::result::Result<Side, Failure>) -> Value {
            match s {
                Ok(s) => json!({"status":"Git-object-verified","object":s.view}),
                Err(e) => json!({"status":"gap","kind":e.kind,"reason":e.detail}),
            }
        }
        let good = usize::from(self.at.is_ok())
            + usize::from(self.since.as_ref().is_some_and(|s| s.is_ok()));
        let total = 1 + usize::from(self.since.is_some());
        json!({"status":if good==0{"gaps-only"}else if good<total{"partial"}else{"complete"},"at":side(&self.at),"since":self.since.as_ref().map(side),"association":self.association,"engine":self.engine,"request":self.request,"comparison":if good==2{Some(if self.at.as_ref().unwrap().bytes==self.since.as_ref().unwrap().as_ref().unwrap().bytes{"identical blob bytes at distinct requested pins; no semantic conclusion"}else{"different blob bytes; no semantic interpretation"})}else{None},"limits":["Object membership/bytes only; not source truth, authorship, signature or accepted-branch authority","Original local snapshot remains a separate observation","Pathname Git subprocess does not inherit all-descendant no-follow capability; pre/post checks cannot exclude transient same-user substitution","No OS network sandbox or escaped-descendant exclusion claimed; restricted built-ins and sanitized config are the qualified mechanism","No source/account/fact/conclusion/duty/save/send production"]})
    }
}
#[derive(Clone)]
struct Association {
    root: PathBuf,
    admin: PathBuf,
    common: PathBuf,
    objects: PathBuf,
    format: String,
    observations: Value,
}
fn fail(kind: &'static str, s: impl Into<String>) -> Failure {
    Failure::abort(kind, s)
}
fn nofollow(path: &Path) -> Result<PathBuf> {
    let mut walked = PathBuf::from("/");
    if !path.is_absolute() {
        return Err(fail("association", "Absolute host association required"));
    }
    for part in path.components() {
        match part {
            Component::RootDir => {}
            Component::CurDir => {}
            Component::ParentDir => {
                walked.pop();
            }
            Component::Normal(p) => {
                walked.push(p);
                let m = fs::symlink_metadata(&walked)
                    .map_err(|e| fail("association", e.to_string()))?;
                if m.file_type().is_symlink() {
                    return Err(fail(
                        "association",
                        "Symlink indirection in repository association",
                    ));
                }
            }
            _ => return Err(fail("association", "Unsupported path component")),
        }
    }
    Ok(walked)
}
fn bounded_metadata(path: &Path) -> Result<(fs::Metadata, Vec<u8>)> {
    use std::io::Read;
    use std::os::unix::fs::OpenOptionsExt;
    let mut f = fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_NONBLOCK)
        .open(path)
        .map_err(|e| fail("association", e.to_string()))?;
    let m = f
        .metadata()
        .map_err(|e| fail("association", e.to_string()))?;
    if !m.is_file() {
        return Err(fail("association", "Association metadata is not regular"));
    }
    let mut bytes = Vec::new();
    (&mut f)
        .take(1048577)
        .read_to_end(&mut bytes)
        .map_err(|e| fail("association", e.to_string()))?;
    if bytes.len() > 1048576 {
        return Err(fail(
            "association",
            "Association metadata exceeds actual byte cap",
        ));
    }
    let after = f
        .metadata()
        .map_err(|e| fail("association", e.to_string()))?;
    if [
        m.len(),
        m.mtime() as u64,
        m.mtime_nsec() as u64,
        m.ctime() as u64,
        m.ctime_nsec() as u64,
    ] != [
        after.len(),
        after.mtime() as u64,
        after.mtime_nsec() as u64,
        after.ctime() as u64,
        after.ctime_nsec() as u64,
    ] {
        return Err(fail(
            "association_changed",
            "Metadata changed during bounded read",
        ));
    }
    Ok((m, bytes))
}
fn metadata(path: &Path, control: &Control) -> Result<Value> {
    control.check()?;
    let path = nofollow(path)?;
    let initial = fs::symlink_metadata(&path).map_err(|e| fail("association", e.to_string()))?;
    let (m, content) = if initial.is_file() {
        let (m, b) = bounded_metadata(&path)?;
        (m, Some(b))
    } else {
        (initial, None)
    };
    Ok(
        json!({"path":native_path_identity(&path),"device":m.dev().to_string(),"inode":m.ino().to_string(),"size":m.len().to_string(),"mtime":m.mtime().to_string(),"mtimeNs":m.mtime_nsec().to_string(),"bytes":content.as_ref().map(|b|b.iter().map(|x|format!("{x:02x}")).collect::<String>()),"sha256":content.as_ref().map(|b|sha256_hex(b))}),
    )
}
fn text(path: &Path) -> Result<String> {
    nofollow(path)?;
    String::from_utf8(bounded_metadata(path)?.1)
        .map_err(|_| fail("association", "Association metadata is not UTF-8"))
}
fn linked_path(base: &Path, raw: &str) -> Result<PathBuf> {
    let line = raw.strip_suffix('\n').unwrap_or(raw);
    if line.is_empty() || line.contains(['\n', '\r', '\0']) {
        return Err(fail("association", "Malformed linked metadata path"));
    }
    let p = PathBuf::from(line);
    nofollow(&if p.is_absolute() { p } else { base.join(p) })
}
fn scan_objects(path: &Path, control: &Control) -> Result<Value> {
    let mut pending = vec![(path.to_path_buf(), 0usize)];
    let mut rows = Vec::new();
    let mut queued = 1usize;
    let mut captured = path.as_os_str().as_bytes().len();
    while let Some((path, depth)) = pending.pop() {
        control.check()?;
        if depth > 128 {
            return Err(fail("capability", "Object storage scan exceeds depth128"));
        }
        let m = fs::symlink_metadata(&path).map_err(|e| fail("association", e.to_string()))?;
        if m.file_type().is_symlink() || (!m.is_file() && !m.is_dir()) {
            return Err(fail(
                "association",
                "Symlink/nonregular object storage unsupported",
            ));
        }
        let key = path.as_os_str().as_bytes().to_vec();
        let row = json!([
            key.iter().map(|b| format!("{b:02x}")).collect::<String>(),
            m.dev().to_string(),
            m.ino().to_string(),
            m.len().to_string(),
            m.mtime().to_string(),
            m.mtime_nsec().to_string()
        ]);
        captured += row.to_string().len();
        if captured > 8 * 1048576 {
            return Err(fail(
                "capability",
                "Object association scan exceeds8MiB capture budget",
            ));
        }
        rows.push((key, row));
        if m.is_dir() {
            for e in fs::read_dir(&path).map_err(|e| fail("association", e.to_string()))? {
                control.check()?;
                let p = e.map_err(|e| fail("association", e.to_string()))?.path();
                queued += 1;
                captured += p.as_os_str().as_bytes().len();
                if queued > 65536 || captured > 8 * 1048576 {
                    return Err(fail(
                        "capability",
                        "Object association scan entry/byte budget exceeded",
                    ));
                }
                pending.push((p, depth + 1));
            }
        }
    }
    rows.sort_by(|a, b| a.0.cmp(&b.0));
    let values: Vec<_> = rows.into_iter().map(|(_, v)| v).collect();
    Ok(
        json!({"entryCount":values.len(),"observationsSha256":sha256_hex(&serde_json::to_vec(&values).unwrap()),"mechanism":"bounded iterative no-symlink scan; raw native path bytes, not display keys"}),
    )
}
impl Association {
    fn open(root: &Path, relative: &Path, control: &Control) -> Result<Self> {
        control.check()?;
        let root = nofollow(root)?;
        let git = root.join(".git");
        let gm = fs::symlink_metadata(&git).map_err(|_| {
            fail(
                "scope",
                "Explicit project must itself be a Git worktree root; no upward discovery",
            )
        })?;
        if gm.file_type().is_symlink() {
            return Err(fail("association", "Symlink .git unsupported"));
        }
        let mut records = vec![metadata(&root, control)?, metadata(&git, control)?];
        let (admin, common) = if gm.is_dir() {
            (git.clone(), git.clone())
        } else if gm.is_file() {
            let raw = text(&git)?;
            let admin = linked_path(
                &root,
                raw.strip_prefix("gitdir: ")
                    .ok_or_else(|| fail("association", "Malformed .git link"))?,
            )?;
            let common = linked_path(&admin, &text(&admin.join("commondir"))?)?;
            if common == admin {
                return Err(fail("association", "Cyclic linked common directory"));
            }
            let backlink = linked_path(&admin, &text(&admin.join("gitdir"))?)?;
            if backlink != git {
                return Err(fail("association", "Linked worktree backlink mismatch"));
            }
            records.extend([
                metadata(&admin.join("commondir"), control)?,
                metadata(&admin.join("gitdir"), control)?,
            ]);
            (admin, common)
        } else {
            return Err(fail("association", "Unsupported .git entry"));
        };
        let mut prefix = root.clone();
        for c in relative
            .components()
            .take(relative.components().count().saturating_sub(1))
        {
            prefix.push(c);
            if prefix.join(".git").exists() {
                return Err(fail("scope", "Selected path crosses a nested repository"));
            }
        }
        for p in [&admin, &common, &admin.join("HEAD"), &common.join("config")] {
            records.push(metadata(p, control)?);
        }
        let config = text(&common.join("config"))?;
        let mut section = String::new();
        let mut relevant = BTreeMap::new();
        for line in config.lines() {
            let l = line.trim();
            if l.is_empty() || l.starts_with(['#', ';']) {
                continue;
            }
            if l.starts_with('[') {
                let s = l
                    .strip_prefix('[')
                    .and_then(|x| x.strip_suffix(']'))
                    .ok_or_else(|| fail("association", "Malformed config section"))?;
                section = s
                    .split_whitespace()
                    .next()
                    .unwrap_or("")
                    .to_ascii_lowercase();
                continue;
            }
            if section == "core" || section == "extensions" {
                let (k, v) = l.split_once('=').ok_or_else(|| {
                    fail("association", "Unsupported source core/extension syntax")
                })?;
                let key = format!("{section}.{}", k.trim().to_ascii_lowercase());
                if section == "extensions" && key != "extensions.objectformat" {
                    return Err(fail(
                        "capability",
                        format!("Unsupported repository extension: {key}"),
                    ));
                }
                if [
                    "core.repositoryformatversion",
                    "core.bare",
                    "core.worktree",
                    "extensions.objectformat",
                ]
                .contains(&key.as_str())
                {
                    if relevant
                        .insert(key, v.trim().trim_matches('"').to_ascii_lowercase())
                        .is_some()
                    {
                        return Err(fail("association", "Duplicate relevant config declaration"));
                    }
                }
            }
        }
        if relevant.get("core.bare").is_some_and(|v| v != "false")
            || relevant.contains_key("core.worktree")
        {
            return Err(fail("scope", "Bare/separate worktree override unsupported"));
        }
        let version = relevant
            .get("core.repositoryformatversion")
            .map(String::as_str)
            .unwrap_or("0");
        if !matches!(version, "0" | "1") {
            return Err(fail("capability", "Unsupported repository format version"));
        }
        let format = relevant
            .get("extensions.objectformat")
            .cloned()
            .unwrap_or_else(|| "sha1".into());
        if !matches!(format.as_str(), "sha1" | "sha256") || format == "sha256" && version != "1" {
            return Err(fail("capability", "Unsupported object format declaration"));
        }
        let objects = nofollow(&common.join("objects"))?;
        for name in ["alternates", "http-alternates"] {
            if fs::symlink_metadata(objects.join("info").join(name)).is_ok() {
                return Err(fail("capability", "Object alternates unsupported"));
            }
        }
        let storage = scan_objects(&objects, control)?;
        let observations = json!({"project":native_path_identity(&root),"admin":native_path_identity(&admin),"common":native_path_identity(&common),"objects":native_path_identity(&objects),"externalMetadata":!common.starts_with(&root),"objectFormat":format,"metadata":records,"storage":storage,"residual":"Filesystem observations around pathname Git reads; not continuous same-user substitution exclusion"});
        Ok(Self {
            root,
            admin,
            common,
            objects,
            format,
            observations,
        })
    }
    fn verify(&self, relative: &Path, c: &Control) -> Result<()> {
        let now = Self::open(&self.root, relative, c)?;
        if now.observations != self.observations {
            return Err(fail(
                "association_changed",
                "Repository/worktree/object association changed; entire new request discarded",
            ));
        }
        Ok(())
    }
}
pub fn valid_id(id: &str, format: &str) -> bool {
    id.len() == (if format == "sha1" { 40 } else { 64 })
        && id
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
fn object(
    engine: &Engine,
    a: &Association,
    id: &str,
    kind: &str,
    budget: &mut usize,
    c: &Control,
) -> Result<Vec<u8>> {
    let cap = if kind == "blob" { 262144 } else { 1048576 };
    let raw = engine.run(
        &a.objects,
        &["cat-file", "--batch", "--no-use-mailmap"],
        format!("{id}\n").as_bytes(),
        cap + 160,
        c,
    )?;
    let newline = raw
        .iter()
        .position(|b| *b == b'\n')
        .ok_or_else(|| Failure::side("framing", "Missing object header"))?;
    let header = std::str::from_utf8(&raw[..newline])
        .map_err(|_| Failure::side("framing", "Nontext object header"))?;
    if header == format!("{id} missing") {
        return Err(Failure::side(
            "missing",
            "Requested object is unavailable locally; no fetch",
        ));
    }
    let fields: Vec<_> = header.split(' ').collect();
    if fields.len() != 3 || fields[0] != id || fields[1] != kind {
        return Err(Failure::side("type", "Wrong object identity/type"));
    }
    let size = fields[2]
        .parse::<usize>()
        .map_err(|_| Failure::side("framing", "Invalid length"))?;
    if size > cap
        || budget
            .checked_add(size.saturating_mul(2))
            .is_none_or(|x| x > 8 * 1048576)
    {
        return Err(Failure::side(
            "limit",
            "Object or side payload limit exceeded",
        ));
    }
    if raw.len() != newline + 1 + size + 1 || raw.last() != Some(&b'\n') {
        return Err(Failure::side("framing", "Truncated/excess object payload"));
    }
    let bytes = raw[newline + 1..newline + 1 + size].to_vec();
    *budget += size * 2; // Count accepted bytes plus recomputation input against the side budget.
    let oid = engine.run(
        &a.objects,
        &["hash-object", "-t", kind, "--stdin", "--no-filters"],
        &bytes,
        65,
        c,
    )?;
    if oid != format!("{id}\n").as_bytes() {
        return Err(Failure::side(
            "integrity",
            "Returned raw type/bytes do not recompute to requested object ID",
        ));
    }
    Ok(bytes)
}
fn side(engine: &Engine, a: &Association, relative: &Path, id: &str, c: &Control) -> Result<Side> {
    let parts: Vec<_> = relative
        .components()
        .map(|p| match p {
            Component::Normal(n) if !n.as_bytes().contains(&0) => Ok(n.as_bytes().to_vec()),
            _ => Err(Failure::side("path", "Invalid literal path component")),
        })
        .collect::<Result<_>>()?;
    if parts.is_empty() || parts.len() > 128 {
        return Err(Failure::side("limit", "Path component limit exceeded"));
    }
    let mut budget = 0;
    let mut retained = Vec::new();
    let commit = object(engine, a, id, "commit", &mut budget, c)?;
    let first = commit.split(|b| *b == b'\n').next().unwrap_or_default();
    let tree = std::str::from_utf8(first)
        .ok()
        .and_then(|s| s.strip_prefix("tree "))
        .filter(|s| valid_id(s, &a.format))
        .ok_or_else(|| Failure::side("commit", "Malformed commit root tree"))?;
    retained.push((id.to_owned(), commit.clone()));
    let root_tree = tree.to_owned();
    let mut oid = root_tree.clone();
    let mut traversed = Vec::new();
    for (index, component) in parts.iter().enumerate() {
        let raw = object(engine, a, &oid, "tree", &mut budget, c)?;
        retained.push((oid.clone(), raw.clone()));
        let mut position = 0;
        let mut names = HashSet::new();
        let mut found = None;
        let hash_len = if a.format == "sha1" { 20 } else { 32 };
        while position < raw.len() {
            let space = raw[position..]
                .iter()
                .position(|b| *b == b' ')
                .map(|n| n + position)
                .ok_or_else(|| Failure::side("tree", "Malformed tree mode"))?;
            let nul = raw[space + 1..]
                .iter()
                .position(|b| *b == 0)
                .map(|n| n + space + 1)
                .ok_or_else(|| Failure::side("tree", "Malformed tree name"))?;
            let mode = std::str::from_utf8(&raw[position..space])
                .map_err(|_| Failure::side("tree", "Invalid mode"))?;
            let name = &raw[space + 1..nul];
            if name.is_empty()
                || name == b"."
                || name == b".."
                || name.contains(&b'/')
                || !names.insert(name.to_vec())
                || !matches!(mode, "40000" | "100644" | "100755" | "120000" | "160000")
                || nul + 1 + hash_len > raw.len()
            {
                return Err(Failure::side("tree", "Malformed/duplicate raw tree entry"));
            }
            let child = raw[nul + 1..nul + 1 + hash_len]
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            if name == component {
                found = Some((mode.to_owned(), child));
            }
            position = nul + 1 + hash_len;
        }
        let (mode, child) = found.ok_or_else(|| {
            Failure::side(
                "path_missing",
                "Exact selected path absent at requested commit",
            )
        })?;
        traversed.push(json!({"tree":oid,"rawSha256":sha256_hex(&raw),"componentHex":component.iter().map(|b|format!("{b:02x}")).collect::<String>(),"mode":mode,"object":child}));
        if index + 1 == parts.len() {
            if !matches!(mode.as_str(), "100644" | "100755") {
                return Err(Failure::side(
                    "nonregular",
                    "Final path is not a regular blob",
                ));
            }
            let bytes = object(engine, a, &child, "blob", &mut budget, c)?;
            if bytes.contains(&0) || std::str::from_utf8(&bytes).is_err() {
                return Err(Failure::side(
                    "encoding",
                    "Blob outside UTF-8/no-NUL text slice",
                ));
            }
            let view = json!({"reference":crate::util::opaque_id("git-side-").map_err(|e|Failure::abort("supervision",e))?,"requestedCommit":id,"readCommit":id,"rawCommitHex":commit.iter().map(|b|format!("{b:02x}")).collect::<String>(),"rawCommitSha256":sha256_hex(&commit),"rootTree":root_tree,"traversed":traversed,"blob":child,"mode":mode,"pathIdentity":native_path_identity(relative),"sha256":sha256_hex(&bytes),"byteLength":bytes.len(),"text":std::str::from_utf8(&bytes).unwrap(),"observedAt":now_rfc3339(),"timeProvenance":"observed_clock","objectPayloadBytes":budget,"standing":"same-engine raw object ID consistency checked; membership/bytes only"});
            return Ok(Side {
                bytes,
                view,
                raw_objects: retained,
            });
        }
        if mode != "40000" {
            return Err(Failure::side(
                "nonregular",
                "Intermediate path is not a tree",
            ));
        }
        oid = child;
    }
    unreachable!()
}
pub fn read(
    root: &Path,
    relative: &Path,
    at: &str,
    since: Option<&str>,
    c: &Control,
) -> Result<Completed> {
    read_with(root, relative, at, since, c, |_| Ok(()))
}
pub(crate) fn read_with(
    root: &Path,
    relative: &Path,
    at: &str,
    since: Option<&str>,
    c: &Control,
    mut hook: impl FnMut(&str) -> Result<()>,
) -> Result<Completed> {
    let a = Association::open(root, relative, c)?;
    if !valid_id(at, &a.format) || since.is_some_and(|s| !valid_id(s, &a.format)) {
        return Err(fail(
            "input",
            "Only lowercase full commit IDs of the repository format are accepted",
        ));
    }
    let engine = Engine::create(&a.objects, &a.format, c)?;
    let at_result = side(&engine, &a, relative, at, c);
    if at_result.as_ref().is_err_and(|e| e.whole) {
        return Err(at_result.err().unwrap());
    }
    hook("after_at")?;
    c.check()?;
    let since_result = since.map(|id| side(&engine, &a, relative, id, c));
    if let Some(Err(e)) = &since_result {
        if e.whole {
            return Err(e.clone());
        }
    }
    hook("before_publish")?;
    c.check()?;
    a.verify(relative, c)?;
    engine.verify()?;
    Ok(Completed {
        at: at_result,
        since: since_result,
        association: a.observations,
        engine: engine.identity(),
        request: json!({"at":at,"since":since,"path":native_path_identity(relative)}),
    })
}
#[cfg(test)]
#[path = "connector_git_tests.rs"]
pub(crate) mod tests;
