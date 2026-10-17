//! Exact-byte package administration admission. These helpers acquire no
//! admission lock: the package importer owns the exclusive gate and durable
//! pending fence across planning, restoration and final publication.
use super::*;
use std::collections::BTreeMap;
use std::io::Write;
use std::os::unix::fs::DirBuilderExt;

#[derive(Clone, Debug)]
pub(crate) struct PackageAdministration {
    pub(crate) project_id: String,
    pub(crate) project_key: String,
    pub(crate) events: BTreeMap<String, Vec<u8>>,
    pub(crate) sequence: u64,
    pub(crate) head: Option<String>,
    pub(crate) closed: bool,
    pub(crate) legal_hold: bool,
    pub(crate) disposition: &'static str,
}
impl PackageAdministration {
    pub(crate) fn summary(&self) -> Value {
        json!({"projectId":self.project_id,"projectKey":self.project_key,
            "sequence":self.sequence,"head":self.head,"closed":self.closed,
            "legalHold":self.legal_hold,"disposition":self.disposition,
            "standing":"Exact administrative bytes; unsigned, no actor or installation authenticated"})
    }
}

fn from_events(
    project_id: &str,
    events: BTreeMap<String, Vec<u8>>,
) -> Result<PackageAdministration, String> {
    if project_id.is_empty() {
        return Err("package project identity is empty".into());
    }
    let key = storage::key(project_id);
    let mut state = State::default();
    for (name, bytes) in &events {
        advance_event(&key, Some(project_id), name, bytes, &mut state)?;
    }
    Ok(PackageAdministration {
        project_id: project_id.into(),
        project_key: key,
        events,
        sequence: state.sequence,
        head: state.head,
        closed: state.closed,
        legal_hold: state.hold,
        disposition: if state.completed {
            "disposed"
        } else if state.disposition.is_some() {
            "disposal incomplete"
        } else {
            "kept"
        },
    })
}

/// Validation only: neither serialization nor native attribution is changed.
pub(crate) fn validate_package_snapshot(
    project_id: &str,
    snapshot: &Value,
) -> Result<PackageAdministration, String> {
    let object = snapshot
        .as_object()
        .ok_or("administration snapshot is not an object")?;
    let fields = [
        "format",
        "formatVersion",
        "projectId",
        "projectKey",
        "events",
        "standing",
        "sequence",
    ];
    if object.len() != fields.len()
        || fields.iter().any(|name| !object.contains_key(*name))
        || snapshot["format"] != "chirality.records-administration-snapshot"
        || snapshot["formatVersion"] != "0.1"
        || snapshot["projectId"] != project_id
        || snapshot["projectKey"] != storage::key(project_id)
        || !snapshot["standing"].is_string()
    {
        return Err(
            "administration snapshot identity/profile invalid; operational import refused".into(),
        );
    }
    let declared = snapshot["sequence"]
        .as_u64()
        .ok_or("administration snapshot sequence invalid")?;
    let events = snapshot["events"]
        .as_object()
        .ok_or("administration snapshot events are not an object")?;
    let events = events
        .iter()
        .map(|(name, value)| {
            let text = value
                .as_str()
                .ok_or("administrative event is not exact UTF-8 text")?;
            Ok((name.clone(), text.as_bytes().to_vec()))
        })
        .collect::<Result<BTreeMap<_, _>, String>>()?;
    let parsed = from_events(project_id, events)?;
    if declared != parsed.sequence {
        return Err("administration snapshot sequence does not cover every event".into());
    }
    Ok(parsed)
}

#[derive(Clone, Debug)]
pub(crate) struct AdministrationRestore {
    pub(crate) missing_events: BTreeMap<String, Vec<u8>>,
    pub(crate) marker_needed: bool,
    pub(crate) source_context: Value,
    incoming: PackageAdministration,
    resulting: PackageAdministration,
    original_events: BTreeMap<String, Vec<u8>>,
    original_marker: Option<Vec<u8>>,
}
impl AdministrationRestore {
    /// The package's recorded history and the retained local result are distinct.
    pub(crate) fn summary(&self) -> Value {
        json!({"sourceHistory":self.incoming.summary(),"resultingRetention":self.resulting.summary(),
            "localSource":self.source_context,"missingEvents":self.missing_events.keys().collect::<Vec<_>>(),
            "restoreFirstEventMarker":self.marker_needed})
    }
}

fn directory_context(path: &Path) -> Result<Value, String> {
    storage::check_path(path)?;
    match std::fs::symlink_metadata(path) {
        Ok(_) => physical(path),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(Value::Null),
        Err(e) => Err(format!("administrative folder unavailable: {e}")),
    }
}
fn plain_context(path: &Path) -> Result<(Vec<u8>, Value), String> {
    let before = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    let bytes = read_plain(path)?;
    let m = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if crate::records_index::Stamp::of(&before) != crate::records_index::Stamp::of(&m) {
        return Err("administrative member changed while freezing import context".into());
    }
    Ok((
        bytes.clone(),
        json!({"sha256":util::sha256_hex(&bytes),"bytes":m.len(),
        "device":m.dev(),"inode":m.ino(),"mtime":m.mtime(),"mtimeNanos":m.mtime_nsec(),
        "ctime":m.ctime(),"ctimeNanos":m.ctime_nsec()}),
    ))
}
fn event_names(folder: &Path) -> Result<Vec<String>, String> {
    let mut names = match std::fs::read_dir(folder) {
        Ok(entries) => entries
            .map(|entry| {
                entry
                    .map_err(|e| e.to_string())?
                    .file_name()
                    .into_string()
                    .map_err(|_| "administrative event name is not UTF-8".into())
            })
            .collect::<Result<Vec<_>, String>>()?,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Vec::new(),
        Err(e) => return Err(format!("administrative history unavailable: {e}")),
    };
    names.sort();
    for name in &names {
        let seq = name
            .strip_suffix(".json")
            .and_then(|n| n.parse::<u64>().ok())
            .filter(|n| *n > 0)
            .ok_or("unknown administrative event member")?;
        if *name != format!("{seq:020}.json") {
            return Err("unsafe or noncanonical administrative event name".into());
        }
    }
    Ok(names)
}
struct LocalHistory {
    events: BTreeMap<String, Vec<u8>>,
    marker: Option<Vec<u8>>,
    first_head: Option<String>,
    context: Value,
}
fn local_history(dir: &Path) -> Result<LocalHistory, String> {
    let control = control(dir)?;
    let folder = control.join("events");
    let controls = directory_context(&control)?;
    let folder_identity = directory_context(&folder)?;
    match std::fs::symlink_metadata(control.join("removal")) {
        Ok(_) => {
            return Err(
                "disposal staging exists; package restoration cannot revive a disposed identity"
                    .into(),
            )
        }
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {}
        Err(e) => return Err(format!("disposal staging state unavailable: {e}")),
    }
    let names = event_names(&folder)?;
    let mut events = BTreeMap::new();
    let mut contexts = BTreeMap::new();
    for name in &names {
        let (bytes, context) = plain_context(&folder.join(name))?;
        events.insert(name.clone(), bytes);
        contexts.insert(name.clone(), context);
    }
    let first_head = marker_head(dir)?;
    let (marker, marker_context) = if first_head.is_some() {
        let (bytes, context) = plain_context(&history_marker(dir)?)?;
        (Some(bytes), context)
    } else {
        (None, Value::Null)
    };
    if event_names(&folder)? != names
        || directory_context(&control)? != controls
        || directory_context(&folder)? != folder_identity
        || marker_head(dir)? != first_head
    {
        return Err("administrative history changed while planning package restoration".into());
    }
    let remembered = ACCEPTED_HEADS
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .cloned();
    Ok(LocalHistory {
        events,
        marker,
        first_head,
        context: json!({"controlFolder":controls,"eventsFolder":folder_identity,
            "events":contexts,"marker":marker_context,"rememberedPrefix":remembered}),
    })
}

/// Computes an exact compatible union without changing local custody or state.
/// A newer local tail survives; a package cannot roll it back or clear its hold.
pub(crate) fn plan_package_restore(
    dir: &Path,
    incoming: &PackageAdministration,
) -> Result<AdministrationRestore, String> {
    plan_restore(dir, incoming, None)
}

/// Only the importer's durable, frozen original local context may supply this
/// baseline. Its own partially restored source rows are not new local acts.
pub(crate) fn resume_package_restore(
    dir: &Path,
    incoming: &PackageAdministration,
    original_source_context: &Value,
) -> Result<AdministrationRestore, String> {
    plan_restore(dir, incoming, Some(original_source_context))
}

fn plan_restore(
    dir: &Path,
    incoming: &PackageAdministration,
    baseline: Option<&Value>,
) -> Result<AdministrationRestore, String> {
    if dir.file_name().and_then(|n| n.to_str()) != Some(incoming.project_key.as_str()) {
        return Err("package administration targets a different project key".into());
    }
    let local = local_history(dir)?;
    let mut source_context = baseline.unwrap_or(&local.context).clone();
    if let Some(baseline) = baseline {
        let fields = [
            "controlFolder",
            "eventsFolder",
            "events",
            "marker",
            "rememberedPrefix",
            "retention",
        ];
        let object = baseline
            .as_object()
            .ok_or("original import administration context is invalid")?;
        if object.len() != fields.len() || fields.iter().any(|field| !object.contains_key(*field)) {
            return Err("original import administration context profile is invalid".into());
        }
    }
    let context_events = source_context["events"]
        .as_object()
        .ok_or("original import administration context is invalid")?;
    let mut original_events = BTreeMap::new();
    for (name, context) in context_events {
        let bytes = local
            .events
            .get(name)
            .ok_or("original local administrative evidence disappeared during import")?;
        if local.context["events"][name] != *context {
            return Err("original local administrative evidence changed during import".into());
        }
        original_events.insert(name.clone(), bytes.clone());
    }
    let original_retention = match from_events(&incoming.project_id, original_events.clone()) {
        Ok(history) => history.summary(),
        Err(error) => json!({"disposition":"unavailable","limit":error}),
    };
    if baseline.is_some() && source_context["retention"] != original_retention {
        return Err(
            "original local retention context disagrees with its exact event evidence".into(),
        );
    }
    source_context["retention"] = original_retention;
    let original_marker = if source_context["marker"].is_null() {
        None
    } else {
        if source_context["marker"] != local.context["marker"] {
            return Err("original local administrative marker changed during import".into());
        }
        Some(
            local
                .marker
                .clone()
                .ok_or("original local administrative marker disappeared")?,
        )
    };
    for field in ["controlFolder", "eventsFolder"] {
        if !source_context[field].is_null() && source_context[field] != local.context[field] {
            return Err("original administrative folder changed during import".into());
        }
    }
    let mut combined = incoming.events.clone();
    let mut missing_events = incoming.events.clone();
    for (name, bytes) in &local.events {
        if baseline.is_some()
            && !original_events.contains_key(name)
            && incoming.events.get(name) != Some(bytes)
        {
            return Err("administrative event is outside the frozen package-import intent".into());
        }
        if combined.get(name).is_some_and(|other| other != bytes) {
            return Err(format!(
                "conflicting local administrative event {name}; nothing replaced"
            ));
        }
        combined.insert(name.clone(), bytes.clone());
        missing_events.remove(name);
    }
    let resulting = from_events(&incoming.project_id, combined)?;
    let first = resulting
        .events
        .first_key_value()
        .map(|(_, bytes)| util::sha256_hex(bytes));
    if local
        .first_head
        .as_ref()
        .is_some_and(|expected| Some(expected) != first.as_ref())
    {
        return Err("package history conflicts with surviving first-event marker".into());
    }
    let remembered = ACCEPTED_HEADS
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .cloned();
    if let Some((sequence, head)) = &remembered {
        if resulting
            .events
            .get(&format!("{sequence:020}.json"))
            .is_none_or(|bytes| util::sha256_hex(bytes) != *head)
        {
            return Err(
                "package history cannot restore the previously observed administrative prefix"
                    .into(),
            );
        }
    }
    // Import is not a local release-hold or reopen act. Even an otherwise
    // compatible source extension cannot clear the latest surviving/witnessed
    // local restriction. A valid newer local release remains part of the union.
    let original_remembered = if source_context["rememberedPrefix"].is_null() {
        None
    } else {
        let pair = source_context["rememberedPrefix"]
            .as_array()
            .filter(|pair| pair.len() == 2)
            .ok_or("original remembered prefix is invalid")?;
        let sequence = pair[0]
            .as_u64()
            .filter(|n| *n > 0)
            .ok_or("original remembered sequence is invalid")?;
        let head = pair[1]
            .as_str()
            .ok_or("original remembered head is invalid")?;
        if resulting
            .events
            .get(&format!("{sequence:020}.json"))
            .is_none_or(|bytes| util::sha256_hex(bytes) != head)
        {
            return Err(
                "package history conflicts with the frozen original remembered prefix".into(),
            );
        }
        Some(sequence)
    };
    let original_tail = original_events
        .last_key_value()
        .and_then(|(name, _)| name.strip_suffix(".json"))
        .and_then(|sequence| sequence.parse::<u64>().ok())
        .unwrap_or(0)
        .max(original_remembered.unwrap_or(0));
    if let Some(bytes) = resulting.events.get(&format!("{original_tail:020}.json")) {
        let event: Value = serde_json::from_slice(bytes).map_err(|e| e.to_string())?;
        if (event["stateAfter"]["closed"] == true && !resulting.closed)
            || (event["stateAfter"]["legalHold"] == true && !resulting.legal_hold)
        {
            return Err(
                "package import cannot reopen the local project or release its legal hold".into(),
            );
        }
    }
    if resulting.disposition != "kept" {
        return Err(
            "project records are disposed or disposal is incomplete; package restoration refused"
                .into(),
        );
    }
    Ok(AdministrationRestore {
        marker_needed: local.marker.is_none() && !resulting.events.is_empty(),
        missing_events,
        source_context,
        incoming: incoming.clone(),
        resulting,
        original_events,
        original_marker,
    })
}

fn original_context_survives(
    plan: &AdministrationRestore,
    now: &LocalHistory,
) -> Result<(), String> {
    for field in ["controlFolder", "eventsFolder"] {
        if !plan.source_context[field].is_null() && plan.source_context[field] != now.context[field]
        {
            return Err("original administrative folder changed; restoration refused".into());
        }
    }
    for (name, bytes) in &plan.original_events {
        if now.events.get(name) != Some(bytes)
            || plan.source_context["events"][name] != now.context["events"][name]
        {
            return Err(
                "original local administrative evidence changed; restoration refused".into(),
            );
        }
    }
    if let Some(marker) = &plan.original_marker {
        if now.marker.as_ref() != Some(marker)
            || plan.source_context["marker"] != now.context["marker"]
        {
            return Err("original administrative marker changed; restoration refused".into());
        }
    }
    for (name, bytes) in &now.events {
        if plan.resulting.events.get(name) != Some(bytes) {
            return Err("administrative history changed outside the restoration plan".into());
        }
    }
    if now.first_head.as_ref().is_some_and(|head| {
        plan.resulting
            .events
            .first_key_value()
            .is_none_or(|(_, bytes)| util::sha256_hex(bytes) != *head)
    }) {
        return Err("administrative marker disagrees with restoration plan".into());
    }
    Ok(())
}

// New imported evidence is private from creation. Existing evidence and its
// permissions are never rewritten; exclusive rename cannot replace a member.
fn publish_restored(path: &Path, bytes: &[u8]) -> Result<(), String> {
    storage::check_path(path)?;
    let parent = path.parent().ok_or("restored event has no parent")?;
    std::fs::DirBuilder::new()
        .recursive(true)
        .mode(0o700)
        .create(parent)
        .map_err(|e| e.to_string())?;
    storage::check_path(parent)?;
    // An interrupted staging write stays outside the strict events inventory.
    // Exclusive rename publishes a complete single-link file in one operation.
    let staging = if parent.file_name().is_some_and(|name| name == "events") {
        parent
            .parent()
            .ok_or("administration staging folder absent")?
    } else {
        parent
    };
    let temporary = staging.join(util::opaque_id(".package-restore-")?);
    let result = (|| {
        let mut file = std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .mode(0o600)
            .open(&temporary)
            .map_err(|e| format!("restored evidence staging: {e}"))?;
        file.write_all(bytes)
            .map_err(|e| format!("restored evidence write: {e}"))?;
        file.sync_all()
            .map_err(|e| format!("restored evidence sync: {e}"))?;
        publish_without_replace(&temporary, path)?;
        storage::sync_publication(path)
    })();
    if temporary.exists() {
        let _ = std::fs::remove_file(&temporary);
        let _ = storage::sync_dir(staging);
    }
    result
}
fn publish_without_replace(from: &Path, to: &Path) -> Result<(), String> {
    use std::os::unix::ffi::OsStrExt;
    let from = std::ffi::CString::new(from.as_os_str().as_bytes()).map_err(|e| e.to_string())?;
    let to = std::ffi::CString::new(to.as_os_str().as_bytes()).map_err(|e| e.to_string())?;
    #[cfg(target_os = "macos")]
    let result = unsafe { libc::renamex_np(from.as_ptr(), to.as_ptr(), libc::RENAME_EXCL) };
    #[cfg(target_os = "linux")]
    let result = unsafe {
        libc::renameat2(
            libc::AT_FDCWD,
            from.as_ptr(),
            libc::AT_FDCWD,
            to.as_ptr(),
            libc::RENAME_NOREPLACE,
        )
    };
    #[cfg(not(any(target_os = "macos", target_os = "linux")))]
    return Err("exclusive administrative restoration unavailable on this platform".into());
    #[cfg(any(target_os = "macos", target_os = "linux"))]
    if result != 0 {
        return Err(format!(
            "create-once restored evidence: {}",
            std::io::Error::last_os_error()
        ));
    }
    Ok(())
}

/// Idempotent create-once recovery of original bytes. Caller retains exclusive
/// import admission and its durable pending fence until all publications settle.
pub(crate) fn restore_package_history(
    dir: &Path,
    plan: &AdministrationRestore,
) -> Result<(), String> {
    let current = local_history(dir)?;
    original_context_survives(plan, &current)?;
    let fresh = resume_package_restore(dir, &plan.incoming, &plan.source_context)?;
    if fresh.resulting.events != plan.resulting.events
        || fresh.resulting.summary() != plan.resulting.summary()
    {
        return Err("administrative restoration result changed; review again".into());
    }
    let folder = control(dir)?.join("events");
    for (name, bytes) in &plan.missing_events {
        let path = folder.join(name);
        match std::fs::symlink_metadata(&path) {
            Ok(_) if read_plain(&path)? == *bytes => {}
            Ok(_) => {
                return Err(
                    "administrative restoration found conflicting bytes; nothing overwritten"
                        .into(),
                )
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => publish_restored(&path, bytes)?,
            Err(e) => {
                return Err(format!(
                    "administrative restoration member unavailable: {e}"
                ))
            }
        }
    }
    if !plan.resulting.events.is_empty() {
        // This control pins exact existing first-event evidence; it is no act.
        if marker_head(dir)?.is_none() {
            let first = plan.resulting.events.first_key_value().unwrap().1;
            let marker = json!({"format":"chirality.records-administration-started","formatVersion":"0.1",
                "projectKey":plan.resulting.project_key,"firstHead":util::sha256_hex(first)});
            publish_restored(
                &history_marker(dir)?,
                &serde_json::to_vec_pretty(&marker).map_err(|e| e.to_string())?,
            )?;
        }
        durable_history(dir)?;
    }
    let after = local_history(dir)?;
    original_context_survives(plan, &after)?;
    if after.events != plan.resulting.events {
        return Err("restored administrative inventory differs from its plan".into());
    }
    let observed = state(dir)?;
    if observed.view()["closed"] != plan.resulting.closed
        || observed.view()["legalHold"] != plan.resulting.legal_hold
        || observed.view()["disposition"] != plan.resulting.disposition
        || observed.sequence != plan.resulting.sequence
        || observed.head != plan.resulting.head
    {
        return Err("restored administrative state differs from its plan".into());
    }
    Ok(())
}

#[cfg(test)]
#[path = "records_administration_tests.rs"]
mod tests;
