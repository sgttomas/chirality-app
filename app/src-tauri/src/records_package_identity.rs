//! Native package-first association. The fixed active directory contains the
//! original intent once; project/root journal files are only hash-bound locators.
//! Reading one known active location fences both identities without a census.
use super::*;

const REFERENCE: &str = "chirality.records-package-association-reference";
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub(super) struct Association {
    pub prior: Option<Unused>,
}
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub(super) struct Unused {
    pub project: String,
    pub payload: BTreeMap<String, bag::Member>,
    pub physical: Value,
}
#[derive(Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct Reference {
    format: String,
    version: String,
    id: String,
    sha256: String,
}
fn base(store: &Path) -> PathBuf {
    store.join("package-associations")
}
fn active(store: &Path) -> PathBuf {
    base(store).join("active")
}
fn history(store: &Path, id: &str) -> PathBuf {
    base(store).join("history").join(id)
}
fn root_locators(store: &Path, root: &Path) -> Result<PathBuf, String> {
    Ok(base(store).join("roots").join(storage::key(
        root.to_str().ok_or("project root is not UTF-8")?,
    )))
}
fn decoded(bytes: &[u8]) -> Result<Intent, String> {
    serde_json::from_value(bag::parse_json_unique(bytes)?)
        .map_err(|e| format!("association original intent unreadable: {e}"))
}
fn active_original(store: &Path) -> Result<Option<(Intent, Vec<u8>)>, String> {
    let folder = active(store);
    let bytes = match optional(&folder.join("intent.json"))? {
        Some(bytes) => bytes,
        None if !folder.exists() => return Ok(None),
        None => {
            return Err(
                "active association lost its original native intent; no identity inferred".into(),
            )
        }
    };
    let mut intent = decoded(&bytes)?;
    intent.bind_store(store)?;
    intent.valid(&intent.dir(), &intent.id)?;
    let (current, id) = opened()?;
    if current != store
        || intent.store_path() != current
        || intent.store_id != id
        || intent.association.is_none()
        || physical(store)? != intent.physical_store
    {
        return Err("active association does not match this physical records store".into());
    }
    let names = std::fs::read_dir(&folder)
        .map_err(|e| e.to_string())?
        .map(|e| e.map(|e| e.file_name()).map_err(|e| e.to_string()))
        .collect::<Result<Vec<_>, _>>()?;
    if names.len() != 1 || names[0] != "intent.json" {
        return Err("active association contains unknown evidence".into());
    }
    Ok(Some((intent, bytes)))
}
fn completed(intent: &Intent, bytes: &[u8]) -> Result<bool, String> {
    match optional(&intent.completion_path()?)? {
        None => Ok(false),
        Some(done) => {
            if bag::parse_json_unique(&done)? != completion(intent, bytes) {
                return Err(
                    "association completion does not bind its original native intent".into(),
                );
            }
            Ok(true)
        }
    }
}
fn original(store: &Path, id: &str) -> Result<(Intent, Vec<u8>), String> {
    if let Some((intent, bytes)) = active_original(store)? {
        if intent.id == id {
            return Ok((intent, bytes));
        }
    }
    let bytes = plain(&history(store,id).join("intent.json"))
        .map_err(|e|format!("original native association intent is missing or unreadable; no act reconstructed: {e}"))?;
    let mut intent = decoded(&bytes)?;
    intent.bind_store(store)?;
    if intent.id != id || intent.store_path() != store || intent.association.is_none() {
        return Err("association locator identity mismatch".into());
    }
    intent.valid(&intent.dir(), id)?;
    Ok((intent, bytes))
}
pub(super) fn read_intent_entry(
    dir: &Path,
    id: &str,
    bytes: &[u8],
) -> Result<(Intent, Vec<u8>), String> {
    let value = bag::parse_json_unique(bytes)?;
    if value["format"] == REFERENCE {
        let reference: Reference = serde_json::from_value(value).map_err(|e| e.to_string())?;
        if reference.version != "0.1" || reference.id != id {
            return Err("association reference identity/profile invalid".into());
        }
        let store = dir
            .parent()
            .and_then(Path::parent)
            .ok_or("project store absent")?;
        let (intent, raw) = original(store, id)?;
        intent.valid(dir, id)?;
        if sha256_hex(&raw) != reference.sha256 {
            return Err("association reference differs from original native intent".into());
        }
        Ok((intent, raw))
    } else {
        let mut intent: Intent =
            serde_json::from_value(value).map_err(|e| format!("package intent unreadable: {e}"))?;
        intent.bind_store(
            dir.parent()
                .and_then(Path::parent)
                .ok_or("project store absent")?,
        )?;
        intent.valid(dir, id)?;
        if intent.association.is_some() {
            return Err(
                "association native intent must remain at its original authority location".into(),
            );
        }
        Ok((intent, bytes.to_vec()))
    }
}
pub(super) fn read_original_entry(dir: &Path, id: &str) -> Result<(Intent, Vec<u8>), String> {
    let store = dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project store absent")?;
    let (intent, raw) = original(store, id)?;
    intent.valid(dir, id)?;
    Ok((intent, raw))
}
pub(super) fn entry_bytes(intent: &Intent, original_raw: &[u8]) -> Result<Vec<u8>, String> {
    if intent.association.is_some() {
        json_bytes(&Reference {
            format: REFERENCE.into(),
            version: "0.1".into(),
            id: intent.id.clone(),
            sha256: sha256_hex(original_raw),
        })
    } else {
        Ok(original_raw.to_vec())
    }
}
fn referenced_intents(store: &Path, root: &Path) -> Result<Vec<Intent>, String> {
    let folder = root_locators(store, root)?;
    let before = bag::payload_inventory(&folder)?;
    let before_stamp = stamp(&folder)?;
    let mut result = Vec::new();
    for name in before.keys() {
        let id = name
            .strip_suffix(".json")
            .filter(|id| id.len() == 64 && id.bytes().all(|b| b.is_ascii_hexdigit()))
            .ok_or("unknown root association locator")?;
        let value = bag::parse_json_unique(&plain(&folder.join(name))?)?;
        let reference: Reference = serde_json::from_value(value).map_err(|e| e.to_string())?;
        let (intent, raw) = original(store, id)?;
        if reference.format != REFERENCE
            || reference.version != "0.1"
            || reference.id != id
            || reference.sha256 != sha256_hex(&raw)
            || intent.root != root
        {
            return Err("root association locator does not bind its original native intent".into());
        }
        result.push(intent);
    }
    if bag::payload_inventory(&folder)? != before || stamp(&folder)? != before_stamp {
        return Err("root association locators changed during lookup".into());
    }
    Ok(result)
}
fn imports_in_roots(store: &Path, dir: &Path, rows: &[Value]) -> Result<BTreeSet<String>, String> {
    let mut ids = BTreeSet::new();
    for row in rows {
        let Some(project) = row["projectId"].as_str() else {
            continue;
        };
        // A release of unused Q names the P import which released it. Only
        // the adopted project's row identifies an original for this subtree.
        if project_dir(store, project) != dir || row["how"] != "adopted" {
            continue;
        }
        let Some(value) = row.get("packageImport") else {
            continue;
        };
        let id = value
            .as_str()
            .filter(|id| id.len() == 64 && id.bytes().all(|b| b.is_ascii_hexdigit()))
            .ok_or("roots import cue has an invalid original native identity")?;
        if row["format"] != ROOT_FORMAT || row["formatVersion"] != VERSION {
            return Err("roots import cue has an unknown profile".into());
        }
        ids.insert(id.to_owned());
    }
    Ok(ids)
}
pub(super) fn required_intents(dir: &Path) -> Result<BTreeSet<String>, String> {
    let store = dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project store absent")?;
    let mut ids = BTreeSet::new();
    let mut known = BTreeSet::new();
    let active = active_original(store)?;
    let active_cue = active
        .as_ref()
        .is_some_and(|(intent, _)| intent.dir() == dir);
    if let Some((intent, _)) = active {
        if intent.dir() == dir {
            // Frozen native prefixes survive simultaneous loss of secondary
            // project/completion/root locators. They discover originals only;
            // entries must still resolve each actual native act or refuse.
            for bytes in [&intent.roots_original, &intent.roots_final] {
                ids.extend(imports_in_roots(
                    store,
                    dir,
                    &parse_lines(bytes, &store.join("roots.jsonl"))?,
                )?);
            }
            ids.insert(intent.id);
            known.insert(intent.root);
        }
    }
    if let Some(root) = root_for_dir(dir) {
        known.insert(root);
    }
    // The fixed active original supplies its own root. Do not parse an
    // interrupted frozen roots append to rediscover that same authority.
    if !active_cue {
        let rows = roots(store)?;
        ids.extend(imports_in_roots(store, dir, &rows)?);
        for row in rows {
            if let (Some(project), Some(root)) = (row["projectId"].as_str(), row["root"].as_str()) {
                if project_dir(store, project) == dir {
                    known.insert(PathBuf::from(root));
                }
            }
        }
    }
    for root in known {
        for intent in referenced_intents(store, &root)? {
            if intent.dir() == dir {
                ids.insert(intent.id);
            }
        }
    }
    Ok(ids)
}
pub(super) fn original_context(intent: &Intent, original_raw: &[u8]) -> Result<Value, String> {
    let path = if intent.association.is_some() {
        match active_original(intent.store_path())? {
            Some((current, _)) if current.id == intent.id => {
                active(intent.store_path()).join("intent.json")
            }
            _ => history(intent.store_path(), &intent.id).join("intent.json"),
        }
    } else {
        intent.path()?
    };
    let parent = path
        .parent()
        .ok_or("original native intent has no parent")?;
    let first = stamp(&path)?;
    let directory = stamp(parent)?;
    if plain(&path)? != original_raw {
        return Err("original native intent bytes changed during custody observation".into());
    }
    if stamp(&path)? != first || stamp(parent)? != directory {
        return Err("original native intent custody changed during observation".into());
    }
    Ok(
        json!({"path":path,"file":first,"directory":directory,"sha256":sha256_hex(original_raw),"bytes":original_raw.len()}),
    )
}

fn completed_root_released(intent: &Intent) -> Result<bool, String> {
    let path = intent.store_path().join("roots.jsonl");
    let bytes = optional(&path)?.unwrap_or_default();
    let Some(tail) = bytes.strip_prefix(intent.roots_final.as_slice()) else {
        return Ok(false);
    };
    if !bytes.ends_with(b"\n") {
        return Ok(false);
    }
    let root = intent.root.to_str().ok_or("project root is not UTF-8")?;
    let here = listed(&parse_lines(&bytes, &path)?, root);
    let superseded = here.is_empty() || (here.len() == 1 && here[0] != intent.project);
    Ok(superseded
        && parse_lines(tail, &path)?.iter().any(|row| {
            row["format"] == ROOT_FORMAT
                && row["formatVersion"] == VERSION
                && row["projectId"] == intent.project
                && row["root"] == root
                && row["how"] == "released"
        }))
}

pub(super) fn require_root(store: &Path, root: &Path) -> Result<(), String> {
    if let Some((intent, bytes)) = active_original(store)? {
        if intent.root == root && !owns(&intent.dir()) {
            let done = completed(&intent, &bytes)?;
            if done && completed_root_released(&intent)? {
                return Ok(());
            }
            if physical(root)? != intent.physical_root {
                return Err("association belongs to a replaced project folder".into());
            }
            if !done {
                return Err("project identity restoration is incomplete; recover the original package operation before opening or recording".into());
            }
            if !matches!(read_link(root),Link::Present{project,..} if project==intent.project) {
                return Err("restored project identity link is missing or changed; recover the original association".into());
            }
        }
    }
    Ok(())
}
pub(super) fn require_project(dir: &Path) -> Result<(), String> {
    if owns(dir) {
        return Ok(());
    }
    let store = dir
        .parent()
        .and_then(Path::parent)
        .ok_or("project store absent")?;
    if let Some((intent, bytes)) = active_original(store)? {
        let prior = intent
            .association
            .as_ref()
            .and_then(|a| a.prior.as_ref())
            .map(|p| project_dir(store, &p.project));
        if (intent.dir() == dir || prior.as_deref() == Some(dir)) && !completed(&intent, &bytes)? {
            return Err("project identity restoration is incomplete; both original and restored identities remain fenced".into());
        }
    }
    Ok(())
}
pub(super) fn resolve_root(root: &Path) -> Result<Option<Intent>, String> {
    let (store, _) = opened()?;
    if let Some((intent, bytes)) = active_original(&store)? {
        if intent.root == root {
            let superseded = if completed(&intent, &bytes)? {
                completed_root_released(&intent)?
            } else {
                false
            };
            if !superseded {
                if physical(root)? != intent.physical_root {
                    return Err("association belongs to a replaced project folder".into());
                }
                return Ok(Some(intent));
            }
        }
    }
    let mut candidates = referenced_intents(&store, root)?
        .into_iter()
        .filter(|intent| physical(root).ok().as_ref() == Some(&intent.physical_root))
        .collect::<Vec<_>>();
    let current = listed(
        &roots(&store)?,
        root.to_str().ok_or("project root is not UTF-8")?,
    );
    if current.len() == 1 {
        candidates.retain(|i| i.project == current[0]);
    }
    if candidates.len() > 1 {
        let project = &candidates[0].project;
        if candidates.iter().any(|i| &i.project != project) {
            return Err("root has ambiguous historical identity restorations".into());
        }
        candidates.sort_by(|a, b| (&a.at, &a.id).cmp(&(&b.at, &b.id)));
    }
    Ok(candidates.pop())
}
pub(super) fn context(root: &Path) -> Value {
    let link = match read_link(root) {
        Link::Absent => json!({"state":"missing"}),
        Link::Unreadable(e) => json!({"state":"unreadable","limit":e}),
        Link::Present { project, store } => {
            json!({"state":"present","projectId":project,"storeId":store})
        }
    };
    json!({"link":link,"restoration":"The native package review may restore a missing project link or release only a provably unused startup identity. Its original ledger is retained. Used, held, closed, disposed or ambiguous identities are refused."})
}
pub(super) fn prior(root: &Path, project: &str, store: &Path) -> Result<Association, String> {
    let at = root.to_str().ok_or("project root is not UTF-8")?;
    let here = listed(&roots(store)?, at);
    if here.len() > 1 {
        return Err("selected folder has ambiguous project identities".into());
    }
    let linked=match read_link(root){Link::Present{project,..}=>Some(project),Link::Absent=>None,Link::Unreadable(_)=>return Err("unreadable project link is retained; identity restoration cannot replace unknown bytes".into())};
    if let (Some(link), Some(recorded)) = (&linked, here.first()) {
        if link != recorded && link != project {
            return Err(
                "project link and store disagree on a different identity; restoration refused"
                    .into(),
            );
        }
    }
    let prior = here
        .first()
        .filter(|p| p.as_str() != project)
        .cloned()
        .or_else(|| linked.filter(|p| p != project));
    let prior = match prior {
        None => None,
        Some(prior) => {
            if here != vec![prior.clone()] {
                return Err(
                    "different project identity is not a registered unused startup identity".into(),
                );
            }
            Some(unused(root, store, &prior, true)?)
        }
    };
    Ok(Association { prior })
}
fn unused(root: &Path, store: &Path, project: &str, initial: bool) -> Result<Unused, String> {
    let dir = project_dir(store, project);
    let payload = bag::payload_inventory(&dir)?;
    if payload.len() != 1 || !payload.contains_key("project.json") {
        return Err(
            "prior identity already has records or unknown members; nothing reassociated".into(),
        );
    }
    let directory_stamp = stamp(&dir)?;
    for entry in std::fs::read_dir(&dir).map_err(|e| e.to_string())? {
        let path = entry.map_err(|e| e.to_string())?.path();
        match path.file_name().and_then(|name| name.to_str()) {
            Some("project.json" | ".writer.lock") => {}
            Some("captures") => {
                let captured = stamp(&path)?;
                for item in std::fs::read_dir(&path).map_err(|e| e.to_string())? {
                    let member = item.map_err(|e| e.to_string())?.path();
                    if member.file_name().and_then(|name| name.to_str()) != Some(".capture.lock") {
                        return Err(
                            "prior identity contains unknown capture directories or evidence"
                                .into(),
                        );
                    }
                    plain(&member)?;
                }
                if stamp(&path)? != captured {
                    return Err("prior identity capture controls changed during review".into());
                }
            }
            _ => {
                return Err(
                    "prior identity contains unknown directories or evidence; nothing reassociated"
                        .into(),
                )
            }
        }
    }
    if stamp(&dir)? != directory_stamp {
        return Err("prior identity inventory changed during review".into());
    }
    let record = bag::parse_json_unique(&plain(&dir.join("project.json"))?)?;
    if record["format"] != PROJECT_FORMAT
        || record["formatVersion"] != VERSION
        || record["projectId"] != project
        || record["how"] != "minted"
    {
        return Err("prior identity is not an unused startup-minted identity".into());
    }
    let state = retention::view(&dir);
    if state["disposition"] != "kept"
        || state["closed"] != false
        || state["legalHold"] != false
        || state["sequence"] != 0
    {
        return Err(
            "prior identity is held, closed, disposed or has uncertain administrative history"
                .into(),
        );
    }
    let control = controls(&dir)?;
    if control.exists() {
        for entry in std::fs::read_dir(&control).map_err(|e| e.to_string())? {
            let path = entry.map_err(|e| e.to_string())?.path();
            if !matches!(
                path.file_name().and_then(|n| n.to_str()),
                Some(".admission.lock" | ".activity.lock")
            ) {
                return Err(
                    "prior identity has administrative or import history; nothing reassociated"
                        .into(),
                );
            }
            plain(&path)?;
        }
    }
    let registry = roots(store)?;
    if initial {
        let rows: Vec<_> = registry
            .iter()
            .filter(|row| row["projectId"] == project)
            .collect();
        if rows.len() != 1
            || rows[0]["how"] != "minted"
            || rows[0]["root"] != root.to_str().ok_or("project root is not UTF-8")?
        {
            return Err(
                "prior identity has earlier association history; not an unused startup identity"
                    .into(),
            );
        }
    }
    let known = roots_of(&registry, project);
    let same = known == vec![root.to_str().ok_or("project root is not UTF-8")?.to_owned()];
    if !same && (initial || !known.is_empty()) {
        return Err("prior identity has ambiguous root history".into());
    }
    Ok(Unused {
        project: project.into(),
        payload,
        physical: physical(&dir)?,
    })
}
pub(super) fn validate_prior(intent: &Intent) -> Result<(), String> {
    if let Some(prior) = intent.association.as_ref().and_then(|a| a.prior.as_ref()) {
        let now = unused(&intent.root, intent.store_path(), &prior.project, false)?;
        if now.payload != prior.payload || now.physical != prior.physical {
            return Err("unused prior identity changed during restoration".into());
        }
    }
    Ok(())
}
pub(super) fn move_directory(from: &Path, to: &Path) -> Result<(), String> {
    let parent = to.parent().ok_or("association publication has no parent")?;
    bag::create_or_match(&parent.join(".directory.lock"), b"")?;
    let from_parent = from.parent().unwrap();
    let from_binding = physical(from_parent)?;
    let to_binding = physical(parent)?;
    let moved = physical(from)?;
    let input = crate::records_index::open_directory(from_parent).map_err(|e| e.to_string())?;
    let output = crate::records_index::open_directory(parent).map_err(|e| e.to_string())?;
    let source = std::ffi::CString::new(from.file_name().unwrap().as_encoded_bytes())
        .map_err(|e| e.to_string())?;
    let target = std::ffi::CString::new(to.file_name().unwrap().as_encoded_bytes())
        .map_err(|e| e.to_string())?;
    if physical(from_parent)? != from_binding
        || physical(parent)? != to_binding
        || physical(from)? != moved
    {
        return Err("association folders changed before directory publication".into());
    }
    #[cfg(target_os = "macos")]
    let result = unsafe {
        libc::renameatx_np(
            input.as_raw_fd(),
            source.as_ptr(),
            output.as_raw_fd(),
            target.as_ptr(),
            libc::RENAME_EXCL,
        )
    };
    #[cfg(target_os = "linux")]
    let result = unsafe {
        libc::renameat2(
            input.as_raw_fd(),
            source.as_ptr(),
            output.as_raw_fd(),
            target.as_ptr(),
            libc::RENAME_NOREPLACE,
        )
    };
    if result != 0 {
        return Err(format!(
            "association publication uncertain: {}",
            std::io::Error::last_os_error()
        ));
    }
    output.sync_all().map_err(|e| e.to_string())?;
    input.sync_all().map_err(|e| e.to_string())?;
    if physical(from_parent)? != from_binding
        || physical(parent)? != to_binding
        || physical(to)? != moved
    {
        return Err("association directory publication custody uncertain".into());
    }
    Ok(())
}
pub(super) fn publish_intent(intent: &Intent) -> Result<(), String> {
    if intent.association.is_none() {
        return intent.publish(&intent.path()?, &json_bytes(intent)?);
    }
    let raw = json_bytes(intent)?;
    if let Some((old, bytes)) = active_original(intent.store_path())? {
        if old.id != intent.id {
            if !completed(&old, &bytes)? {
                return Err("finish the active project identity restoration first".into());
            }
            move_directory(
                &active(intent.store_path()),
                &history(intent.store_path(), &old.id),
            )?;
        } else if raw != bytes {
            return Err("original association intent changed".into());
        }
    }
    if !active(intent.store_path()).exists() {
        let stage = intent
            .stage_path()
            .parent()
            .unwrap()
            .join("association-intent");
        intent.publish(&stage.join("intent.json"), &raw)?;
        move_directory(&stage, &active(intent.store_path()))?;
    }
    let reference = json_bytes(&Reference {
        format: REFERENCE.into(),
        version: "0.1".into(),
        id: intent.id.clone(),
        sha256: sha256_hex(&raw),
    })?;
    intent.publish(&intent.path()?, &reference)?;
    intent.publish(
        &root_locators(intent.store_path(), &intent.root)?.join(format!("{}.json", intent.id)),
        &reference,
    )?;
    checkpoint("association")
}
pub(super) fn intent_bytes(intent: &Intent) -> Result<Vec<u8>, String> {
    if intent.association.is_some() {
        original(intent.store_path(), &intent.id).map(|(_, bytes)| bytes)
    } else {
        plain(&intent.path()?)
    }
}

#[cfg(test)]
#[path = "records_package_identity_tests.rs"]
mod tests;
