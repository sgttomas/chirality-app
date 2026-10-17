//! Recovery of derived package controls. Only a surviving original local
//! native intent authorizes publication; receipts and completions never do.
use super::*;
use std::io::Read;

static ORIGINALS: std::sync::LazyLock<Mutex<BTreeMap<PathBuf, BTreeMap<String, String>>>> =
    std::sync::LazyLock::new(|| Mutex::new(BTreeMap::new()));

#[derive(Clone)]
pub(super) struct Entry {
    pub(super) intent: Intent,
    /// Exact original full intent bytes, even when the current journal member
    /// is an association reference. Completion always binds this original act.
    pub(super) bytes: Vec<u8>,
    pub(super) done: Option<Vec<u8>>,
    pub(super) missing_entry: bool,
    pub(super) missing_receipt: bool,
    pub(super) repair_needed: bool,
}

fn names(folder: &Path) -> Result<BTreeSet<String>, String> {
    storage::check_path(folder)?;
    match std::fs::read_dir(folder) {
        Ok(rows) => rows
            .map(|row| {
                row.map_err(|e| e.to_string())?
                    .file_name()
                    .into_string()
                    .map_err(|_| "non-UTF8 package journal member".into())
            })
            .collect(),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(BTreeSet::new()),
        Err(e) => Err(e.to_string()),
    }
}

/// This reader distinguishes absent derived controls from lost native acts.
/// It never publishes, admits incomplete work, follows a foreign receipt, or
/// forgets a previously observed original intent. Parent readers enforce the
/// returned repair flag; the native repair path is its only tolerant consumer.
pub(super) fn entries(dir: &Path) -> Result<Vec<Entry>, String> {
    let folder = journal(dir)?;
    let original_names = names(&folder)?;
    let before = bag::payload_inventory(&folder)?;
    let original_stamp = stamp(&folder)?;
    let receipts = dir.join("package-imports");
    let receipt_names = names(&receipts)?;
    let receipt_before = bag::payload_inventory(&receipts)?;
    let receipt_stamp = stamp(&receipts)?;
    let intent_names: BTreeSet<_> = original_names
        .iter()
        .filter(|name| !name.ends_with(".completed.json"))
        .cloned()
        .collect();
    let mut required = identity::required_intents(dir)?;
    let remembered = ORIGINALS
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .cloned()
        .unwrap_or_default();
    required.extend(remembered.keys().cloned());
    if let Some(seen) = SEEN.lock().unwrap_or_else(|p| p.into_inner()).get(dir) {
        required.extend(
            seen.iter()
                .filter(|name| !name.ends_with(".completed.json"))
                .filter_map(|name| name.strip_suffix(".json"))
                .map(str::to_owned),
        );
    }
    let disposed = if intent_names.is_empty() && required.is_empty() {
        false
    } else {
        retention::disposition_started(dir)?
    };
    let mut result = Vec::new();
    let mut ids = required;
    for name in &original_names {
        if let Some(id) = name.strip_suffix(".completed.json") {
            if !canonical_id(id)
                || (!intent_names.contains(&format!("{id}.json")) && !ids.contains(id))
            {
                return Err("package completion has lost its original local intent".into());
            }
            continue;
        }
        let id = name
            .strip_suffix(".json")
            .filter(|id| canonical_id(id))
            .ok_or("unknown package journal member")?;
        ids.insert(id.to_owned());
    }
    if ids.is_empty() && !names(&dir.join("package-imports"))?.is_empty() {
        return Err("package origin receipts have no surviving original local native intent; quoted derivatives cannot restore its authority".into());
    }
    for id in &ids {
        if !canonical_id(id) {
            return Err("invalid required original import identity".into());
        }
        let local = optional(&folder.join(format!("{id}.json")))?;
        let missing_entry = local.is_none();
        let (intent, bytes) = match local {
            Some(local) => identity::read_intent_entry(dir, id, &local)?,
            None => identity::read_original_entry(dir, id)?,
        };
        intent.valid(dir, id)?;
        if remembered
            .get(id)
            .is_some_and(|hash| *hash != sha256_hex(&bytes))
        {
            return Err("previously observed original native package intent changed".into());
        }
        let done = optional(&intent.completion_path()?)?;
        if let Some(done) = &done {
            let expected = json_bytes(&completion(&intent, &bytes))?;
            if *done != expected {
                return Err("unequal package completion; original intent remains held".into());
            }
        }
        // Legitimate disposal removes this payload receipt along with the
        // payload. Its surviving completed import must not obstruct disposal
        // completion or recreate any removed bytes. An unfinished intent still
        // fences, including after a conflicting externally supplied ledger.
        let missing_receipt = if disposed && done.is_some() {
            false
        } else {
            match optional(&dir.join(intent.receipt_relative()))? {
                Some(receipt) if receipt == json_bytes(&intent.receipt())? => false,
                Some(_) => {
                    return Err("unequal package import origin receipt; nothing replaced".into())
                }
                None => true,
            }
        };
        let repair_needed = missing_entry || done.is_none() || missing_receipt;
        result.push(Entry {
            intent,
            bytes,
            done,
            missing_entry,
            missing_receipt,
            repair_needed,
        });
    }
    // A local import can append no roots row at all. If its original and
    // completion disappear, its surviving receipt must not silently become
    // foreign evidence merely because another local import also survives.
    // Only an actual local native act's copied members can establish a receipt
    // as imported foreign bytes; before/payload membership cannot do that.
    for name in &receipt_names {
        let id = name
            .strip_suffix(".json")
            .filter(|id| canonical_id(id))
            .ok_or("unknown payload package origin receipt member")?;
        let member = receipt_before
            .get(name)
            .ok_or("payload package origin receipt is not a regular file")?;
        let relative = format!("package-imports/{name}");
        if let Some(local) = result.iter().find(|row| row.intent.id == id) {
            let expected = json_bytes(&local.intent.receipt())?;
            if member.sha256 != sha256_hex(&expected) || member.bytes != expected.len() as u64 {
                return Err(
                    "unequal local package origin receipt; original intent remains held".into(),
                );
            }
        } else if !result
            .iter()
            .any(|row| row.intent.copied.get(&relative) == Some(member))
        {
            return Err("package origin receipt has no surviving local native intent or exact local copied-foreign proof; missing native authority remains held".into());
        }
    }
    if names(&folder)? != original_names
        || bag::payload_inventory(&folder)? != before
        || stamp(&folder)? != original_stamp
        || names(&receipts)? != receipt_names
        || bag::payload_inventory(&receipts)? != receipt_before
        || stamp(&receipts)? != receipt_stamp
    {
        return Err("package import journal changed while reading".into());
    }
    SEEN.lock()
        .unwrap_or_else(|p| p.into_inner())
        .entry(dir.to_owned())
        .or_default()
        .extend(ids.into_iter().map(|id| format!("{id}.json")));
    let mut remembered = ORIGINALS.lock().unwrap_or_else(|p| p.into_inner());
    let known = remembered.entry(dir.to_owned()).or_default();
    for row in &result {
        if known
            .get(&row.intent.id)
            .is_some_and(|hash| *hash != sha256_hex(&row.bytes))
        {
            return Err(
                "original native package intent changed between concurrent observations".into(),
            );
        }
    }
    for row in &result {
        known.insert(row.intent.id.clone(), sha256_hex(&row.bytes));
    }
    Ok(result)
}

fn canonical_id(id: &str) -> bool {
    id.len() == 64 && id.bytes().all(|b| b.is_ascii_hexdigit())
}

/// Hash an immutable original byte prefix while retaining the full current
/// file's custody. A later append is neither erased nor attributed by repair.
fn prefix(path: &Path, member: &bag::Member) -> Result<(), String> {
    storage::check_path(path)?;
    let before = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
    if !before.is_file() || before.nlink() != 1 || before.len() < member.bytes {
        return Err("original package member is missing, shortened or unsafe".into());
    }
    let mut file = crate::records_index::open_log(path).map_err(|e| e.to_string())?;
    let expected = crate::records_index::Stamp::of(&before);
    if crate::records_index::Stamp::of(&file.metadata().map_err(|e| e.to_string())?) != expected {
        return Err("package member changed while opening its original prefix".into());
    }
    use sha2::Digest;
    let mut digest = sha2::Sha256::new();
    let mut left = member.bytes;
    let mut buffer = [0u8; 64 * 1024];
    while left > 0 {
        let wanted = left.min(buffer.len() as u64) as usize;
        let count = file
            .read(&mut buffer[..wanted])
            .map_err(|e| e.to_string())?;
        if count == 0 {
            return Err("original package prefix ended before its declared length".into());
        }
        digest.update(&buffer[..count]);
        left -= count as u64;
    }
    if format!("{:x}", digest.finalize()) != member.sha256 {
        return Err("original imported prefix changed; control recovery refused".into());
    }
    if crate::records_index::Stamp::of(&file.metadata().map_err(|e| e.to_string())?) != expected
        || crate::records_index::Stamp::of(
            &std::fs::symlink_metadata(path).map_err(|e| e.to_string())?,
        ) != expected
    {
        return Err("package member changed during original-prefix verification".into());
    }
    Ok(())
}

fn administration(intent: &Intent) -> Result<Value, String> {
    let incoming = retention::validate_package_snapshot(&intent.project, &intent.administration)?;
    let now = retention::plan_package_restore(&intent.dir(), &incoming)?;
    if !now.missing_events.is_empty() || now.marker_needed {
        return Err("original package administration publication is incomplete".into());
    }
    let original = intent.source_context["events"]
        .as_object()
        .ok_or("original native import administrative context is invalid")?;
    for (name, proof) in original {
        if now.source_context["events"][name]["sha256"] != proof["sha256"]
            || now.source_context["events"][name]["bytes"] != proof["bytes"]
        {
            return Err("original local administrative prefix changed or disappeared".into());
        }
    }
    if let Some(pair) = intent.source_context["rememberedPrefix"].as_array() {
        if pair.len() != 2 {
            return Err("original native import remembered history is invalid".into());
        }
        let sequence = pair[0]
            .as_u64()
            .ok_or("original remembered sequence invalid")?;
        if now.source_context["events"][format!("{sequence:020}.json")]["sha256"] != pair[1] {
            return Err("original remembered administrative prefix cannot be proved".into());
        }
    }
    Ok(now.summary())
}

/// Material completion proof permits ordinary subsequent append-only activity.
/// It never shortens a log, changes admin state or manufactures writer custody.
fn completed_roots_witness(intent: &Intent, roots: &[u8], rows: &[Entry]) -> Result<Value, String> {
    if roots.starts_with(&intent.roots_final) && compatible_roots(intent, roots)? {
        return Ok(Value::Null);
    }
    // A later completed LOCAL native import may retain the exact intervening
    // identity round trip. Its original roots prefix is the authority here;
    // a receipt, an unfinished import or an arbitrary related tail is not.
    for row in rows {
        let later = &row.intent;
        let Some(done) = &row.done else { continue };
        if later.id == intent.id
            || later.project != intent.project
            || later.root != intent.root
            || later.store_path() != intent.store_path()
            || later.store_id != intent.store_id
            || later.physical_root != intent.physical_root
            || later.physical_store != intent.physical_store
            || later.physical_payload != intent.physical_payload
            || later.link_after != intent.link_after
            || !later.roots_original.starts_with(&intent.roots_final)
            || !later.roots_final.starts_with(&later.roots_original)
            || !roots.starts_with(&later.roots_final)
            || !compatible_roots(later, roots)?
        {
            continue;
        }
        let mut original = identity::original_context(later, &row.bytes)?;
        // The full original parent-directory custody is frozen and rechecked
        // in control_context before publication. Repairing another reference
        // can legitimately change that same journal directory afterwards.
        // Its physical identity and mode, and the original file's full custody
        // and bytes, must still remain unchanged after those own publications.
        original["directory"] = json!({"device":original["directory"]["device"],
            "inode":original["directory"]["inode"],"mode":original["directory"]["mode"]});
        return Ok(json!({"importId":later.id,"original":original,
            "completion":sha256_hex(done),"completionStamp":stamp(&later.completion_path()?)?}));
    }
    Err("original roots association is incomplete or conflicting".into())
}

fn complete_context(
    intent: &Intent,
    derived: &BTreeMap<String, bag::Member>,
    rows: &[Entry],
) -> Result<Value, String> {
    let (store, id) = opened()?;
    if store != intent.store_path()
        || id != intent.store_id
        || physical(&store)? != intent.physical_store
        || physical(&intent.root)? != intent.physical_root
        || physical(&intent.dir())? != intent.physical_payload
    {
        return Err("original project/store custody changed; controls remain held".into());
    }
    if retention::disposition_started(&intent.dir())? {
        return Err("disposal has started; control repair cannot recreate payload".into());
    }
    let link = plain(&intent.root.join(PROJECT_LINK))?;
    if link != intent.link_after {
        return Err("original import association is not completely published".into());
    }
    let roots = plain(&store.join("roots.jsonl"))?;
    let roots_witness = completed_roots_witness(intent, &roots, rows)?;
    let current = bag::payload_inventory(&intent.dir())?;
    let mut original = intent.before.clone();
    original.extend(intent.payload.clone());
    for (name, member) in &original {
        match current.get(name) {
            Some(now) if now == member => {}
            Some(now) if name.ends_with(".jsonl") && now.bytes >= member.bytes => {
                prefix(&intent.dir().join(name), member)?;
            }
            None if derived.get(name) == Some(member) => {}
            _ => {
                return Err(format!(
                    "original package member is incomplete or unequal: {name}"
                ))
            }
        }
    }
    let administration = administration(intent)?;
    Ok(json!({"payload":current,"administration":administration,
        "root":physical(&intent.root)?,"store":physical(&store)?,"payloadFolder":physical(&intent.dir())?,
        "roots":sha256_hex(&roots),"rootsStamp":stamp(&store.join("roots.jsonl"))?,
        "rootsWitness":roots_witness,"link":sha256_hex(&link),"linkStamp":stamp(&intent.root.join(PROJECT_LINK))?}))
}

struct SourceSnapshot {
    snapshot: bag::Snapshot,
    selection: Option<bag::Snapshot>,
}
enum WorkKind {
    Controls,
    Resume(SourceSnapshot),
}
struct Work {
    entry: Entry,
    kind: WorkKind,
    context: Value,
}
pub(crate) struct ControlPlan {
    root: PathBuf,
    dir: PathBuf,
    work: Vec<Work>,
    controls: Value,
    actor: Value,
    observed: Value,
    deferred: Vec<String>,
}
fn wanted(dir: &Path, rows: Vec<Entry>) -> Result<Vec<Entry>, String> {
    let uncertain = UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .cloned();
    if uncertain
        .as_ref()
        .is_some_and(|id| !rows.iter().any(|row| &row.intent.id == id))
    {
        return Err("uncertain package publication lost its original native intent".into());
    }
    Ok(rows
        .into_iter()
        .filter(|row| row.repair_needed || Some(&row.intent.id) == uncertain.as_ref())
        .collect())
}
fn derivative_members(rows: &[Entry]) -> Result<BTreeMap<String, bag::Member>, String> {
    rows.iter()
        .map(|row| {
            let bytes = json_bytes(&row.intent.receipt())?;
            Ok((
                row.intent.receipt_relative(),
                bag::Member {
                    sha256: sha256_hex(&bytes),
                    bytes: bytes.len() as u64,
                },
            ))
        })
        .collect()
}
fn control_context(dir: &Path, rows: &[Entry]) -> Result<Value, String> {
    let mut stamps = BTreeMap::new();
    for path in [controls(dir)?, journal(dir)?, dir.join("package-imports")] {
        stamps.insert(path.clone(), stamp(&path)?);
    }
    let mut evidence = Vec::new();
    for row in rows {
        for path in [
            row.intent.path()?,
            row.intent.completion_path()?,
            dir.join(row.intent.receipt_relative()),
        ] {
            stamps.insert(path.clone(), stamp(&path)?);
        }
        evidence.push(json!({"id":row.intent.id,"intent":sha256_hex(&row.bytes),
            "originalCustody":identity::original_context(&row.intent,&row.bytes)?,
            "done":row.done.as_ref().map(|bytes|sha256_hex(bytes)),
            "missingEntry":row.missing_entry,"missingReceipt":row.missing_receipt,"repairNeeded":row.repair_needed}));
    }
    let uncertain = UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .get(dir)
        .cloned();
    Ok(json!({"evidence":evidence,"stamps":stamps,"uncertain":uncertain}))
}
fn source_snapshot(intent: &Intent, source: Option<&Path>) -> Result<SourceSnapshot, String> {
    let stage = intent.stage_path();
    let retained = match std::fs::symlink_metadata(&stage) {
        Ok(_) => true,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => false,
        Err(e) => return Err(e.to_string()),
    };
    let (snapshot, selection) = if retained {
        if source.is_some() {
            return Err("the original private package is present; review its retained bytes before selecting another source".into());
        }
        (bag::inspect(&stage)?, None)
    } else {
        let source = source.ok_or("the original private package is missing; select the exact original exported package to finish its existing intent")?;
        storage::check_path(source)?;
        let source = source.canonicalize().map_err(|e| e.to_string())?;
        if source.starts_with(intent.store_path())
            || intent.store_path().starts_with(&source)
            || source.starts_with(&intent.root)
            || intent.root.starts_with(&source)
        {
            return Err("choose the original package outside the project and current store".into());
        }
        let parent = stage.parent().ok_or("original stage parent is absent")?;
        // Reject a different selected package before populating the original
        // missing stage. A mistaken selection must not occupy its recovery slot.
        let review = parent.join(crate::util::opaque_id("reselected-review-")?);
        bag::create_or_match(
            &review.join("selection.json"),
            &json_bytes(&json!({"packageIdentity":intent.package_identity,"source":source}))?,
        )?;
        let selected = bag::snapshot(&source, &review.join("bag"))?;
        if selected.identity() != intent.package_identity
            || selected.project_id() != intent.project
            || selected.payload() != &intent.payload
            || selected.administration() != &intent.administration
        {
            return Err("selected package differs from the original native intent; original stage remains absent".into());
        }
        selected.verify_unchanged()?;
        bag::create_or_match(&parent.join("reselection-staging"), b"")?;
        // A failed copy retains its partial destination. Keep that destination
        // off the fixed original stage name so the same exact package can be
        // selected again after interruption without deleting unknown evidence.
        let candidate = review.join("rebuild");
        {
            let rebuilt = bag::snapshot(selected.root(), &candidate)?;
            if rebuilt.identity() != intent.package_identity
                || rebuilt.project_id() != intent.project
                || rebuilt.payload() != &intent.payload
                || rebuilt.administration() != &intent.administration
            {
                return Err("rebuilt private package differs from the original native intent; original stage remains absent".into());
            }
            rebuilt.verify_unchanged()?;
        }
        selected.verify_unchanged()?;
        selected.source_unchanged()?;
        // Exclusive directory publication cannot replace a stage that arrived
        // during the rebuild. The external selection stays at its own path so
        // its full source custody can still be checked across the question.
        identity::move_directory(&candidate, &stage)?;
        (bag::inspect(&stage)?, Some(selected))
    };
    if snapshot.identity() != intent.package_identity
        || snapshot.project_id() != intent.project
        || snapshot.payload() != &intent.payload
        || snapshot.administration() != &intent.administration
    {
        return Err("selected or retained package differs from the original native intent; nothing imported".into());
    }
    Ok(SourceSnapshot {
        snapshot,
        selection,
    })
}
pub(crate) fn needs_package(root: &Path) -> Result<bool, String> {
    let (_, _, dir) = recovery_project(root)?;
    let rows = entries(&dir)?;
    let derived = derivative_members(&rows)?;
    let selected = wanted(&dir, rows.clone())?;
    if selected.is_empty() {
        return Ok(false);
    }
    if retention::disposition_started(&dir)? {
        return Err(
            "disposal has started; package-control repair is held and cannot recreate payload"
                .into(),
        );
    }
    // Complete independent control repairs first. Their restored derivatives
    // may unblock another original import without requiring its source now.
    if selected
        .iter()
        .any(|row| complete_context(&row.intent, &derived, &rows).is_ok())
    {
        return Ok(false);
    }
    for row in selected {
        match std::fs::symlink_metadata(row.intent.stage_path()) {
            Ok(_) => {}
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(true),
            Err(e) => return Err(e.to_string()),
        }
    }
    Ok(false)
}
pub(crate) fn prepare(
    root: &Path,
    source: Option<&Path>,
    actor: &Value,
    observed: &Value,
) -> Result<ControlPlan, String> {
    require_native_actor(actor)?;
    storage::check_path(root)?;
    if root.canonicalize().map_err(|e| e.to_string())? != root {
        return Err("recover package controls from the original physical project folder".into());
    }
    let (_, _, dir) = recovery_project(root)?;
    // Check before lock_intent: payload ownership controls must never recreate
    // a legitimately removed payload subtree.
    if retention::disposition_started(&dir)? {
        return Err(
            "disposal has started; package-control repair is held and cannot recreate payload"
                .into(),
        );
    }
    let selected = wanted(&dir, entries(&dir)?)?;
    if selected.is_empty() {
        return Err("no original package controls need recovery".into());
    }
    if selected.iter().any(|row| row.intent.root != root) {
        return Err("recover package controls from each intent's original project folder".into());
    }
    let _guards = lock_intent(&selected[0].intent)?;
    let rows = entries(&dir)?;
    let controls = control_context(&dir, &rows)?;
    let derived = derivative_members(&rows)?;
    let selected = wanted(&dir, rows.clone())?;
    let mut work = Vec::new();
    let mut blocked = Vec::new();
    for entry in selected {
        match complete_context(&entry.intent, &derived, &rows) {
            Ok(context) => work.push(Work {
                entry,
                kind: WorkKind::Controls,
                context,
            }),
            Err(material_error) => blocked.push((entry, material_error)),
        }
    }
    let deferred = if work.is_empty() {
        if blocked.len() != 1 {
            return Err("multiple unfinished payload publications require explicit resolution; no new import act performed".into());
        }
        let (entry, error) = blocked.pop().unwrap();
        let snapshot =
            source_snapshot(&entry.intent, source).map_err(|e| format!("{error}; {e}"))?;
        let context = validate_target(&entry.intent, &snapshot.snapshot, true)?;
        work.push(Work {
            entry,
            kind: WorkKind::Resume(snapshot),
            context,
        });
        Vec::new()
    } else {
        blocked
            .into_iter()
            .map(|(entry, _)| entry.intent.id)
            .collect()
    };
    Ok(ControlPlan {
        root: root.into(),
        dir,
        work,
        controls,
        actor: actor.clone(),
        observed: observed.clone(),
        deferred,
    })
}
pub(crate) fn statement(
    plan: &ControlPlan,
) -> Result<crate::act_control::native_statement::NativeStatement, String> {
    let imports: Vec<_> = plan.work.iter().map(|work|json!({"importId":work.entry.intent.id,
        "packageIdentity":work.entry.intent.package_identity,"missingJournalReference":work.entry.missing_entry,
        "missingReceipt":work.entry.missing_receipt,"missingCompletion":work.entry.done.is_none(),
        "finishOriginalPayload":matches!(work.kind,WorkKind::Resume(_)),"originalActor":work.entry.intent.actor,
        "review":work.context})).collect();
    let full = format!("Recover the derived controls of {} original package import(s)?\n\nProject folder: {}\n\nEach surviving original native intent remains unchanged. This repairs its missing derived controls or finishes only its original frozen payload publications. It performs no new import act, restores no actor or native custody, preserves later local append-only records and valid newer retention history, and replaces no unequal file.\n\nDeferred original operations (still fenced; finish separately): {}\n\n{}\n\nActor for this recovery (identity not verified): {}",
        plan.work.len(),plan.root.display(),if plan.deferred.is_empty(){"none".into()}else{plan.deferred.join(", ")},STANDING,crate::act_control::native_statement::actor_line(&plan.actor));
    let detail = json!({"imports":imports,"deferredImports":plan.deferred,"controls":plan.controls,"actor":plan.actor,"observed":plan.observed});
    crate::act_control::native_statement::whole_or_in_app(
        "package control recovery",
        "original package import",
        full,
        &detail,
        |digest| {
            format!("Recover original package controls?\n\nThe complete original intents, exact package identities, missing controls, local histories and recovery actor are shown in the App. sha-256: {digest}\nDeferred original operations (still fenced): {}\nThis performs no new import act and restores no native custody. Changed evidence refuses publication.",if plan.deferred.is_empty(){"none".into()}else{plan.deferred.join(", ")})
        },
    )
}
pub(crate) fn apply(plan: ControlPlan, actor: &Value, observed: &Value) -> Result<Value, String> {
    if actor != &plan.actor || observed != &plan.observed {
        return Err("native recovery actor or home context changed; review again".into());
    }
    if retention::disposition_started(&plan.dir)? {
        return Err(
            "disposal has started; package-control recovery cannot recreate payload".into(),
        );
    }
    let first = plan
        .work
        .first()
        .ok_or("empty package control recovery plan")?;
    let _guards = lock_intent(&first.entry.intent)?;
    let rows = entries(&plan.dir)?;
    if control_context(&plan.dir, &rows)? != plan.controls {
        return Err("package controls changed after the native question; review again".into());
    }
    let derived = derivative_members(&rows)?;
    for work in &plan.work {
        let now = match &work.kind {
            WorkKind::Controls => complete_context(&work.entry.intent, &derived, &rows)?,
            WorkKind::Resume(snapshot) => {
                if let Some(selection) = &snapshot.selection {
                    selection.verify_unchanged()?;
                    selection.source_unchanged()?;
                }
                snapshot.snapshot.source_unchanged()?;
                validate_target(&work.entry.intent, &snapshot.snapshot, true)?
            }
        };
        if now != work.context {
            return Err(
                "package recovery context changed after the native question; review again".into(),
            );
        }
    }
    UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .insert(plan.dir.clone(), first.entry.intent.id.clone());
    let mut repaired = Vec::new();
    // Pure derivatives first; all incomplete material stays behind admission.
    for work in &plan.work {
        let i = &work.entry.intent;
        let bytes = identity::entry_bytes(i, &work.entry.bytes)?;
        i.publish(&i.path()?, &bytes)?;
        if matches!(work.kind, WorkKind::Controls) {
            i.publish(
                &plan.dir.join(i.receipt_relative()),
                &json_bytes(&i.receipt())?,
            )?;
        }
    }
    for work in &plan.work {
        if matches!(work.kind, WorkKind::Controls) {
            let mut expected = work.context.clone();
            for repaired in &plan.work {
                if matches!(repaired.kind, WorkKind::Controls) {
                    let receipt = repaired.entry.intent.receipt_relative();
                    expected["payload"][&receipt] = json!(derived
                        .get(&receipt)
                        .ok_or("derived receipt proof absent")?);
                }
            }
            if complete_context(&work.entry.intent, &derived, &rows)? != expected {
                return Err("package material changed while recovering controls; completion remains unconfirmed".into());
            }
        }
    }
    for work in &plan.work {
        let i = &work.entry.intent;
        if matches!(work.kind, WorkKind::Controls) {
            i.publish(
                &i.completion_path()?,
                &json_bytes(&completion(i, &work.entry.bytes))?,
            )?;
            storage::sync_dir(&i.folder()?)?;
            repaired.push(i.id.clone());
        }
    }
    for work in &plan.work {
        if let WorkKind::Resume(snapshot) = &work.kind {
            finish(&work.entry.intent, &snapshot.snapshot)?;
            repaired.push(work.entry.intent.id.clone());
        }
    }
    let final_rows = entries(&plan.dir)?;
    if !plan.deferred.is_empty() {
        if final_rows
            .iter()
            .any(|row| row.repair_needed && !plan.deferred.contains(&row.intent.id))
        {
            return Err(
                "selected original controls remain incomplete; recovery remains fenced".into(),
            );
        }
        UNCERTAIN
            .lock()
            .unwrap_or_else(|p| p.into_inner())
            .insert(plan.dir.clone(), plan.deferred[0].clone());
        return Ok(
            json!({"state":"package controls partly recovered","recoveredImports":repaired,
            "deferredImports":plan.deferred,"limit":"An original package operation remains fenced; finish that same operation after these independent controls are restored.","standing":STANDING}),
        );
    }
    if final_rows.iter().any(|row| row.repair_needed) {
        return Err(
            "package controls remain incomplete; the same original recovery stays fenced".into(),
        );
    }
    UNCERTAIN
        .lock()
        .unwrap_or_else(|p| p.into_inner())
        .remove(&plan.dir);
    remember(&plan.dir, &plan.root);
    Ok(
        json!({"state":"package controls recovered","recoveredImports":repaired,
        "retention":retention::view(&plan.dir),"standing":STANDING}),
    )
}
pub(crate) fn status(root: &Path) -> Value {
    let result = (|| -> Result<Value, String> {
        let (_, _, dir) = recovery_project(root)?;
        let selected = wanted(&dir, entries(&dir)?)?;
        if selected.is_empty() {
            return Ok(json!({"canRepair":false,"needsPackage":false}));
        }
        if retention::disposition_started(&dir)? {
            return Ok(json!({"canRepair":false,"needsPackage":false,
                "limit":"Disposal has started; package-control repair cannot recreate removed payload. Missing native completion remains held."}));
        }
        Ok(json!({"canRepair":true,"needsPackage":needs_package(root)?,
            "repairImports":selected.iter().map(|row|row.intent.id.clone()).collect::<Vec<_>>(),
            "limit":"Ordinary reads and recording remain fenced until the surviving original intents' derived controls are confirmed."}))
    })();
    result.unwrap_or_else(|limit| json!({"canRepair":false,"needsPackage":false,"limit":limit}))
}

#[cfg(test)]
#[path = "records_package_controls_tests.rs"]
mod tests;
