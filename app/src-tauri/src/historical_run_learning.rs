//! Read-only historical run evidence for WR TT-10/TT-11. Neither a resolved
//! record nor this value is a native receipt, a live run, or a supply writer.
use crate::workflow_workspace::publication::{
    ProjectRecords, ProjectSourceBinding, ResolvedRecord,
};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::ffi::CString;
use std::fs::File;
use std::io::Read;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::fs::MetadataExt;
use std::path::{Component, Path, PathBuf};

const STANDING: &str = "historical record correspondence only; no live run, native receipt, new supply, registration or model adoption is restored";

#[derive(Clone, Debug, PartialEq)]
pub(crate) struct Boundary {
    pub turn: String,
    pub client_message: String,
    pub text_identity: Value,
    pub run_text: Value,
    pub run_text_ref: String,
    pub checks: Vec<Value>,
    pub recovery_pointers: Vec<Value>,
    pub kind: String,
}

pub(crate) struct HistoricalRun {
    pub run: String,
    pub conversation: String,
    pub workflow: Value,
    pub holding_library: String,
    pub start: Boundary,
    pub end: Option<Boundary>,
    /// An acknowledged notice and a later following-run chain can both be
    /// genuine. Only native turn order can select the earliest exact stop.
    pub end_candidates: Vec<Boundary>,
    pub recorded_ended: bool,
    pub limits: Vec<String>,
    proof: Snapshot,
}

/// Strict recorded version identity for Compare when native activity cannot
/// be located. It conveys no turn range, native home or selection authority.
pub(crate) struct HistoricalVersion {
    pub run: String,
    pub conversation: String,
    pub workflow: Value,
    pub holding_library: String,
    pub recorded_ended: bool,
    pub limits: Vec<String>,
    proof: Snapshot,
}
impl HistoricalVersion {
    pub(crate) fn read(project: &ProjectRecords, run: &str) -> Result<Self, String> {
        if run.is_empty() {
            return Err("historical run reference required".into());
        }
        let proof = Snapshot::read(project)?;
        let (start, recorded_ended) = metadata(&proof, run)?;
        let body = start.body();
        let result = Self {
            run:run.into(), conversation:text(body,"conversation")?.into(),
            workflow:body["workflow"].clone(), holding_library:text(body,"holding_library")?.into(),
            recorded_ended, limits:vec![STANDING.into(),"recorded workflow version only; no native start/end boundary or current activity is established".into()], proof,
        };
        result.recheck(project)?;
        Ok(result)
    }
    pub(crate) fn recheck(&self, project: &ProjectRecords) -> Result<(), String> {
        self.proof.recheck(project)
    }
}

#[derive(Clone, Debug)]
pub(crate) struct SourceHome {
    pub home_class: String,
    /// Original recorded generations are provenance, never current authority.
    pub recorded_generations: Vec<Value>,
    pub evidence: Vec<Value>,
}

fn text<'a>(value: &'a Value, field: &str) -> Result<&'a str, String> {
    value[field]
        .as_str()
        .filter(|s| !s.is_empty())
        .ok_or_else(|| format!("historical run: {field} is absent or empty"))
}

fn one<'a>(items: impl Iterator<Item = &'a Value>, label: &str) -> Result<&'a Value, String> {
    let rows: Vec<_> = items.collect();
    match rows.as_slice() {
        [row] => Ok(row),
        [] => Err(format!("historical run: original {label} is unavailable")),
        _ => Err(format!("historical run: duplicate or conflicting {label}")),
    }
}

fn check_opening(opened: &Value, start: &Value, run: &str) -> Result<(), String> {
    if opened["runId"] != run
        || opened["body"]["runId"] != run
        || opened["body"]["surface"] != "App run"
        || opened["body"]["conversationRef"] != start["conversation"]
    {
        return Err("historical run: run_opened scope disagrees with the original WR start".into());
    }
    for (rs, wr) in [
        ("kind", "kind"),
        ("origin", "origin"),
        ("sourceRoot", "source_root"),
        ("name", "name"),
        ("revision", "revision"),
    ] {
        if text(&opened["body"]["workflow"], rs)? != text(&start["workflow"], wr)? {
            return Err(format!(
                "historical run: run_opened workflow {rs} disagrees with original WR tuple"
            ));
        }
    }
    if opened["body"]["workflow"]["revisionVerification"] != "verified" {
        return Err(
            "historical run: opening does not record the registered revision's verification".into(),
        );
    }
    Ok(())
}

fn original_start<'a>(
    records: &'a BTreeMap<String, ResolvedRecord>,
    run: &str,
) -> Result<&'a ResolvedRecord, String> {
    let starts: Vec<_> = records
        .values()
        .filter(|r| {
            r.body()["record_kind"] == "run_text"
                && r.body()["purpose"] == "run start"
                && r.body()["run"] == run
        })
        .collect();
    let start = match starts.as_slice() {
        [start] => *start,
        [] => return Err("historical run: original run-start text is unavailable".into()),
        _ => return Err("historical run: duplicate or conflicting WR run starts".into()),
    };
    let body = start.body();
    for field in [
        "kind",
        "origin",
        "source_root",
        "name",
        "revision",
        "revision_method",
    ] {
        text(&body["workflow"], field)?;
    }
    text(body, "holding_library")?;
    text(body, "conversation")?;
    let refs = start.envelope()["basis_records"]
        .as_array()
        .ok_or("historical run: start basis is unavailable")?;
    if refs.len() != 1 {
        return Err("historical run: run start must name its one original selection".into());
    }
    let selection_ref = refs[0]
        .as_str()
        .ok_or("historical run: selection reference is malformed")?;
    let selection = records
        .get(selection_ref)
        .ok_or("historical run: original selection is unavailable")?;
    let s = selection.body();
    if !start.same_project(selection)
        || s["record_kind"] != "selection_record"
        || s["standing"] != "registered"
        || s["selection_id"] != body["selection"]
        || s["identity"] != body["workflow"]
        || s["holding_library"] != body["holding_library"]
        || s["conversation"] != body["conversation"]
    {
        return Err("historical run: selection and run-start full tuple, holding library or conversation disagree".into());
    }
    let conflict = records
        .values()
        .filter(|r| {
            r.body()["record_kind"] == "selection_record"
                && r.body()["selection_id"] == s["selection_id"]
        })
        .any(|other| {
            ["identity", "holding_library", "conversation", "standing"]
                .iter()
                .any(|field| other.body()[*field] != s[*field])
        });
    // One selected choice can be used for several actual runs. The publisher
    // writes a distinct immutable envelope per run, retaining selection_id and
    // adding that run's prior_run context. The exact cited basis governs;
    // reusing its ID cannot silently change its slot or conversation.
    if conflict {
        return Err("historical run: conflicting original selection identity".into());
    }
    Ok(start)
}

fn boundary(
    project: &ProjectRecords,
    records: &BTreeMap<String, ResolvedRecord>,
    source: &ResolvedRecord,
    kind: &str,
    recovery_rows: &[Value],
) -> Result<Boundary, String> {
    let body = source.body();
    let mut coordinates = BTreeSet::new();
    let mut checks = Vec::new();
    let mut ids = BTreeSet::new();
    let mut acknowledged = false;
    for check in records.values().filter(|r| {
        r.body()["record_kind"] == "supply_check"
            && r.body()["run"] == body["run"]
            && r.body()["purpose"] == body["purpose"]
    }) {
        // A check with the same scope but another source is an ambiguity, not
        // an observation the reader may silently discard.
        let basis = check.envelope()["basis_records"]
            .as_array()
            .ok_or("historical run: check basis unavailable")?;
        if basis.len() != 1 || basis[0] != source.reference() {
            return Err("historical run: supply check names a different original text".into());
        }
        crate::records::supply::correspond(project, source, check)
            .map_err(|e| format!("historical run: supply-check correspondence: {e}"))?;
        if !ids.insert(text(check.body(), "check")?.to_owned()) {
            return Err("historical run: duplicate supply-check identity".into());
        }
        // A failed early history lookup remains evidence, but does not poison
        // a later observation of the same original turn and client message.
        acknowledged |= check.body()["state"] != "not found";
        coordinates.insert((
            text(check.body(), "turn")?.to_owned(),
            text(check.body(), "client_user_message_id")?.to_owned(),
        ));
        checks.push(check.envelope().clone());
    }
    let mut pointers: BTreeMap<String, (Value, bool)> = BTreeMap::new();
    for row in recovery_rows
        .iter()
        .filter(|r| r["kind"] == "conversation_index")
    {
        for tag in row["tags"]
            .as_array()
            .into_iter()
            .flatten()
            .filter(|t| t["owner"] == crate::workflow_learning_pointers::OWNER)
        {
            let raw = text(tag, "value")?;
            let pointer = match crate::workflow_learning_pointers::decode(raw) {
                Ok(pointer) => pointer,
                Err(e) if row["threadId"] == body["conversation"] => {
                    return Err(format!(
                        "historical run: malformed original native boundary pointer: {e}"
                    ))
                }
                Err(_) => continue,
            };
            let relevant = pointer["run_text_ref"] == source.reference()
                || (pointer["run"] == body["run"] && pointer["purpose"] == body["purpose"]);
            if !relevant {
                continue;
            }
            if pointer["run_text_ref"] != source.reference()
                || pointer["run"] != body["run"]
                || pointer["conversation"] != body["conversation"]
                || pointer["purpose"] != body["purpose"]
                || row["threadId"] != body["conversation"]
            {
                return Err(
                    "historical run: native boundary pointer disagrees with the original WR source"
                        .into(),
                );
            }
            crate::recovery::generation_ref(&pointer["generation"])?;
            // REC deliberately retains the execution index's historical
            // lastLoadedGeneration when a new tag is appended. The new
            // positive ACK owns its generation; the append's session locates
            // the original occurrence among later inherited tag copies.
            let original_row = row["session"] == pointer["generation"]["appSession"];
            let item = pointers.entry(raw.to_owned()).or_insert((pointer, false));
            item.1 |= original_row;
        }
    }
    let mut pointer_generations = BTreeSet::new();
    for (pointer, original_row) in pointers.values() {
        if !original_row {
            return Err(
                "historical run: original native pointer app-session occurrence is not retained by REC".into(),
            );
        }
        coordinates.insert((
            text(pointer, "turn")?.into(),
            text(pointer, "client_user_message_id")?.into(),
        ));
        pointer_generations.insert(crate::recovery::generation_ref(&pointer["generation"])?);
        acknowledged = true;
    }
    if pointer_generations.len() > 1 {
        return Err("historical run: conflicting original native pointer generations".into());
    }
    let (turn, client_message) = match coordinates.into_iter().collect::<Vec<_>>().as_slice() {
        [coordinate] => coordinate.clone(),
        [] => {
            return Err(
                "historical run: original acknowledged turn/check boundary is unavailable".into(),
            )
        }
        _ => return Err("historical run: conflicting original turn/client boundaries".into()),
    };
    if !acknowledged {
        return Err("historical run: only not-found checks survived; original acknowledged native boundary unavailable".into());
    }
    Ok(Boundary {
        turn,
        client_message,
        text_identity: body["text_identity"].clone(),
        run_text: body.clone(),
        run_text_ref: source.reference().to_owned(),
        checks,
        recovery_pointers: pointers.into_values().map(|(value, _)| value).collect(),
        kind: kind.into(),
    })
}

fn metadata<'a>(proof: &'a Snapshot, run: &str) -> Result<(&'a ResolvedRecord, bool), String> {
    let records = &proof.records;
    let start_record = original_start(records, run)?;
    let start_body = start_record.body();
    let opened = one(
        proof
            .entries
            .iter()
            .filter(|e| e["runId"] == run && e["kind"] == "run_opened"),
        "RS run_opened",
    )?;
    check_opening(opened, start_body, run)?;
    let own_path = proof.binding.records_root().join(crate::storage::log_rel(
        Some(run),
        crate::records::supply::LIVE_WRITER,
    ));
    let own = proof
        .log_entries
        .get(&own_path)
        .ok_or("historical run: original owning run log is unavailable")?;
    if own
        .iter()
        .filter(|e| e["recordId"] == opened["recordId"] && *e == opened)
        .count()
        != 1
    {
        return Err("historical run: run_opened is outside its original App workflow log".into());
    }
    let ended: Vec<_> = proof
        .entries
        .iter()
        .filter(|e| e["runId"] == run && e["kind"] == "run_ended")
        .collect();
    if ended.len() > 1 {
        return Err("historical run: duplicate or conflicting RS run_ended".into());
    }
    if let Some(end) = ended.first() {
        if own
            .iter()
            .filter(|e| e["recordId"] == end["recordId"] && e == end)
            .count()
            != 1
            || end["seq"].as_u64() <= opened["seq"].as_u64()
        {
            return Err("historical run: run_ended has a different owner, run or ordering".into());
        }
    }
    Ok((start_record, !ended.is_empty()))
}

impl HistoricalRun {
    pub(crate) fn read(project: &ProjectRecords, run: &str) -> Result<Self, String> {
        Self::read_with_recovery(project, run, &[])
    }
    pub(crate) fn read_with_recovery(
        project: &ProjectRecords,
        run: &str,
        recovery_rows: &[Value],
    ) -> Result<Self, String> {
        if run.is_empty() {
            return Err("historical run reference required".into());
        }
        let proof = Snapshot::read(project)?;
        let records = &proof.records;
        let (start_record, recorded_ended) = metadata(&proof, run)?;
        let start_body = start_record.body();
        for entry in proof.entries.iter().filter(|entry| {
            entry["runId"] == run
                && entry["kind"] == "supplied_guidance"
                && matches!(
                    entry["body"]["supplyForm"].as_str(),
                    Some("workflow run start (turn text)" | "workflow run end notice (turn text)")
                )
        }) {
            let reading = crate::records::supply::read_correspondence(project, entry);
            if reading.standing != crate::records::supply::ReadStanding::HistoricalCorrespondence {
                return Err(format!("historical run: recorded RS workflow supply disagrees with its original WR evidence: {}",reading.limits.join("; ")));
            }
        }
        let start = boundary(project, records, start_record, "run start", recovery_rows)?;
        let mut ends = Vec::new();
        for notice in records.values().filter(|r| {
            r.body()["record_kind"] == "run_text"
                && r.body()["purpose"] == "run end notice"
                && r.body()["run"] == run
        }) {
            if notice.body()["conversation"] != start_body["conversation"]
                || notice.envelope()["basis_records"] != json!([start_record.reference()])
            {
                return Err("historical run: end notice disagrees with its original start".into());
            }
            ends.push(boundary(
                project,
                records,
                notice,
                "run end notice",
                recovery_rows,
            )?);
        }
        for next in records.values().filter(|r| {
            r.body()["record_kind"] == "run_text"
                && r.body()["purpose"] == "run start"
                && r.body()["chain"]["prior_run"] == run
        }) {
            let next_run = text(next.body(), "run")?;
            if next_run == run {
                return Err("historical run: self-referential run chain".into());
            }
            let next = original_start(records, next_run)?;
            let next_open = one(
                proof
                    .entries
                    .iter()
                    .filter(|e| e["runId"] == next_run && e["kind"] == "run_opened"),
                "following RS run_opened",
            )?;
            check_opening(next_open, next.body(), next_run)?;
            let next_own_path = proof.binding.records_root().join(crate::storage::log_rel(
                Some(next_run),
                crate::records::supply::LIVE_WRITER,
            ));
            if !proof
                .log_entries
                .get(&next_own_path)
                .is_some_and(|entries| {
                    entries
                        .iter()
                        .filter(|e| e["recordId"] == next_open["recordId"] && *e == next_open)
                        .count()
                        == 1
                })
            {
                return Err(
                    "historical run: following opening is outside its original App workflow log"
                        .into(),
                );
            }
            if next.body()["conversation"] != start_body["conversation"]
                || next_open["body"]["follows"] != run
                || next.body()["chain"]["prior_workflow"] != start_body["workflow"]
            {
                return Err("historical run: following-run chain disagrees with the prior run's full tuple or conversation".into());
            }
            let selection = records
                .get(next.envelope()["basis_records"][0].as_str().unwrap())
                .unwrap();
            if selection.body()["prior_run"]["run"] != run
                || selection.body()["prior_run"]["workflow"] != start_body["workflow"]
            {
                return Err(
                    "historical run: following selection disagrees with the original chain".into(),
                );
            }
            ends.push(boundary(
                project,
                records,
                next,
                "following run start",
                recovery_rows,
            )?);
        }
        if !recorded_ended && !ends.is_empty() {
            return Err(
                "historical run: native end preparation without an actual recorded run end".into(),
            );
        }
        if ends
            .iter()
            .map(|end| &end.kind)
            .collect::<BTreeSet<_>>()
            .len()
            != ends.len()
        {
            return Err(
                "historical run: multiple or conflicting end-notice/following-run boundaries"
                    .into(),
            );
        }
        let end = if ends.len() == 1 {
            ends.first().cloned()
        } else {
            None
        };
        if recorded_ended && ends.is_empty() {
            return Err("historical run: recorded end has no exact acknowledged native end boundary; later conversation turns cannot be attributed to this run".into());
        }
        if ends
            .iter()
            .any(|e| e.turn == start.turn || e.client_message == start.client_message)
        {
            return Err("historical run: start and end have the same native boundary".into());
        }
        let mut limits = vec![STANDING.into(),"REC project paths remain quoted provenance; they do not independently prove a stable-project-UUID equivalence after a folder move or package import".into()];
        for boundary in std::iter::once(&start).chain(ends.iter()) {
            for check in &boundary.checks {
                let body = &check["body"];
                if let Some(state) = body["state"].as_str().filter(|state| *state != "verified") {
                    let at = body["read_at"]
                        .as_str()
                        .map(|time| format!(" at {time}"))
                        .unwrap_or_default();
                    let causes: Vec<_> = body["evidence_limits"]
                        .as_array()
                        .into_iter()
                        .flatten()
                        .filter_map(Value::as_str)
                        .collect();
                    let cause = if causes.is_empty() {
                        String::new()
                    } else {
                        format!("; original evidence limits: {}", causes.join("; "))
                    };
                    limits.push(format!("historical {} check {} ({}) recorded {state}{at}{cause}; this original observation remains separate from fresh native content correlation, which supplies no new workflow-supply or model-adoption claim", boundary.kind, body["check"].as_str().unwrap_or_default(), check["record_id"].as_str().unwrap_or_default()));
                }
            }
        }
        let result = Self {
            run: run.into(),
            conversation: text(start_body, "conversation")?.into(),
            workflow: start_body["workflow"].clone(),
            holding_library: text(start_body, "holding_library")?.into(),
            start,
            end,
            end_candidates: ends,
            recorded_ended,
            limits,
            proof,
        };
        result.recheck(project)?;
        Ok(result)
    }

    /// Preserve the original bytes and source across blocking native reads.
    /// A changed record set is retried from a fresh inspection, never rebound.
    pub(crate) fn recheck(&self, project: &ProjectRecords) -> Result<(), String> {
        self.proof.recheck(project)
    }

    /// Recheck the REC coordinates against their actual current owner as well
    /// as the records source after a blocking native read.
    pub(crate) fn recheck_with_recovery(
        &self,
        project: &ProjectRecords,
        rows: &[Value],
    ) -> Result<(), String> {
        self.recheck(project)?;
        let current = Self::read_with_recovery(project, &self.run, rows)?;
        if current.start != self.start || current.end_candidates != self.end_candidates {
            return Err(
                "historical run: original native boundary evidence changed during the read".into(),
            );
        }
        current.source_home(rows, &[])?;
        Ok(())
    }

    pub(crate) fn source_home(
        &self,
        rows: &[Value],
        restart_events: &[Value],
    ) -> Result<SourceHome, String> {
        source_home_for_run(&self.run, &self.conversation, rows, restart_events)
    }
}

/// Cheap REC provenance query for an explicit read-on-request UI offer. It
/// does not admit records or read native history; those remain press-time work.
pub(crate) fn source_home_for_run(
    run: &str,
    thread: &str,
    rows: &[Value],
    restart_events: &[Value],
) -> Result<SourceHome, String> {
    let mut homes = BTreeSet::new();
    let mut evidence = Vec::new();
    let mut generations = BTreeMap::new();
    let mut tagged_generation = false;
    for row in rows.iter().filter(|r| r["kind"] == "conversation_index") {
        let carries = row["tags"]
            .as_array()
            .into_iter()
            .flatten()
            .any(|t| t["owner"] == crate::run_restart::RUN_TAG_OWNER && t["value"] == run);
        if carries && row["threadId"] != thread {
            return Err("historical run: REC run tag names a different conversation".into());
        }
        if row["threadId"] != thread {
            continue;
        }
        let home = text(row, "home")?;
        if !matches!(home, "H-acct" | "H-key") {
            return Err("historical run: REC native home class is unsupported".into());
        }
        homes.insert(home.to_owned());
        if let Some(reference) = row["lastLoadedGeneration"].as_str() {
            let generation = crate::recovery::generation_from_ref(reference)
                .map_err(|e| format!("historical run: REC generation is unavailable: {e}"))?;
            if carries {
                tagged_generation = true;
            }
            generations.insert(reference.to_owned(), generation);
        } else if carries {
            return Err(
                "historical run: original REC run tag has no full recorded generation".into(),
            );
        }
        evidence.push(row.clone());
    }
    if !tagged_generation {
        return Err("historical run: no positive REC run tag with its original full generation; thread-only indexes and restart facts do not establish a run's native home".into());
    }
    for event in restart_events
        .iter()
        .filter(|e| e["kind"] == "app_restart_interruption" && e["threadId"] == thread)
    {
        let home = text(event, "home")?;
        if !matches!(home, "H-acct" | "H-key") {
            return Err("historical run: restart native home class is unsupported".into());
        }
        homes.insert(home.to_owned());
        evidence.push(event.clone());
    }
    let home_class = match homes.into_iter().collect::<Vec<_>>().as_slice() {
        [home] => home.clone(),
        [] => return Err("historical run: REC does not establish this conversation's native home; no active-home fallback".into()),
        _ => return Err("historical run: REC names this conversation in conflicting native homes".into()),
    };
    Ok(SourceHome {
        home_class,
        recorded_generations: generations.into_values().collect(),
        evidence,
    })
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Stamp {
    device: u64,
    inode: u64,
    mode: u32,
    links: u64,
    size: u64,
    modified: (i64, i64),
    changed: (i64, i64),
}
impl Stamp {
    fn of(m: &std::fs::Metadata) -> Self {
        // Ancestors anchor containment by physical identity. Their unrelated
        // child activity (especially /tmp) is not a change to this source.
        let directory = m.is_dir();
        Self {
            device: m.dev(),
            inode: m.ino(),
            mode: m.mode(),
            links: if directory { 0 } else { m.nlink() },
            size: if directory { 0 } else { m.len() },
            modified: if directory {
                (0, 0)
            } else {
                (m.mtime(), m.mtime_nsec())
            },
            changed: if directory {
                (0, 0)
            } else {
                (m.ctime(), m.ctime_nsec())
            },
        }
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
struct FileProof {
    bytes: Vec<u8>,
    stamps: Vec<Stamp>,
}
impl FileProof {
    fn read(path: &Path) -> Result<Self, String> {
        if !path.is_absolute() {
            return Err("historical run: absolute source required".into());
        }
        let parts: Vec<_> = path
            .components()
            .filter(|p| !matches!(p, Component::RootDir))
            .collect();
        let mut directory = File::open("/").map_err(|e| e.to_string())?;
        let mut stamps = vec![];
        for (n, part) in parts.iter().enumerate() {
            let Component::Normal(name) = part else {
                return Err("historical run: non-normal source component".into());
            };
            let name = CString::new(name.as_encoded_bytes()).map_err(|e| e.to_string())?;
            let is_last = n + 1 == parts.len();
            let flags = libc::O_RDONLY
                | libc::O_NOFOLLOW
                | libc::O_NONBLOCK
                | libc::O_CLOEXEC
                | if is_last { 0 } else { libc::O_DIRECTORY };
            // SAFETY: a retained directory and a NUL-terminated component;
            // no symlink is followed and no control file is created.
            let fd = unsafe { libc::openat(directory.as_raw_fd(), name.as_ptr(), flags) };
            if fd < 0 {
                return Err(format!(
                    "historical run source: {}",
                    std::io::Error::last_os_error()
                ));
            }
            let mut file = unsafe { File::from_raw_fd(fd) };
            let before = file.metadata().map_err(|e| e.to_string())?;
            if is_last && (!before.is_file() || before.nlink() != 1) {
                return Err("historical run: source is not a plain regular file".into());
            }
            stamps.push(Stamp::of(&before));
            if is_last {
                let mut bytes = Vec::new();
                file.read_to_end(&mut bytes).map_err(|e| e.to_string())?;
                if Stamp::of(&file.metadata().map_err(|e| e.to_string())?)
                    != *stamps.last().unwrap()
                {
                    return Err("historical run: file changed while read".into());
                }
                return Ok(Self { bytes, stamps });
            }
            directory = file;
        }
        Err("historical run: source has no file component".into())
    }
}

struct Snapshot {
    binding: ProjectSourceBinding,
    records: BTreeMap<String, ResolvedRecord>,
    entries: Vec<Value>,
    log_entries: BTreeMap<PathBuf, Vec<Value>>,
    files: BTreeMap<PathBuf, FileProof>,
}
impl Snapshot {
    fn recheck(&self, project: &ProjectRecords) -> Result<(), String> {
        let current = Self::read(project)?;
        if !self.binding.same_source(&current.binding) || self.files != current.files {
            return Err(
                "historical run: original project/store or record evidence changed during the read"
                    .into(),
            );
        }
        Ok(())
    }
    fn read(project: &ProjectRecords) -> Result<Self, String> {
        let binding = project.source_binding()?;
        let references = project.list_references()?;
        let paths = crate::storage::discover(project.root())?;
        let mut records = BTreeMap::new();
        let mut files = BTreeMap::new();
        for reference in &references {
            let record = project
                .resolve(reference)
                .map_err(|e| format!("historical run: WR {reference}: {e:?}"))?;
            let key = reference
                .strip_prefix("wr-record:v1:")
                .ok_or("historical run: unsupported WR reference")?;
            let path = binding
                .records_root()
                .join("workflow")
                .join(format!("{key}.json"));
            let proof = FileProof::read(&path)?;
            if proof.bytes != record.bytes() {
                return Err("historical run: WR source changed while resolved".into());
            }
            files.insert(path, proof);
            if records.insert(reference.clone(), record).is_some() {
                return Err("historical run: duplicate WR reference".into());
            }
        }
        let mut entries = Vec::new();
        let mut log_entries = BTreeMap::new();
        let mut ids = BTreeSet::new();
        for path in &paths {
            let proof = FileProof::read(path)?;
            let name = path
                .file_name()
                .and_then(|n| n.to_str())
                .ok_or("historical run: non-UTF8 log name")?;
            let parsed =
                crate::record_lines::parse(&proof.bytes, name, 0, 0, 1, Default::default());
            let mut limits: Vec<String> =
                crate::record_lines::links_removed(path, name, &parsed.chain)
                    .into_iter()
                    .collect();
            if let Some(partial) = parsed.partial_tail {
                limits.push(partial);
            }
            let mut own = Vec::new();
            for line in parsed.lines {
                limits.extend(line.limits);
                own.extend(line.entries);
            }
            if !limits.is_empty() {
                return Err(format!(
                    "historical run: RS record set is incomplete: {}",
                    limits.join("; ")
                ));
            }
            for entry in &own {
                if !ids.insert(text(entry, "recordId")?.to_owned()) {
                    return Err("historical run: duplicate RS record identity".into());
                }
            }
            entries.extend(own.clone());
            log_entries.insert(path.clone(), own);
            files.insert(path.clone(), proof);
        }
        if project.list_references()? != references
            || crate::storage::discover(project.root())? != paths
            || !binding.same_source(&project.source_binding()?)
        {
            return Err("historical run: original record source changed during its census".into());
        }
        for (path, proof) in &files {
            if &FileProof::read(path)? != proof {
                return Err(
                    "historical run: original record evidence changed during its census".into(),
                );
            }
        }
        Ok(Self {
            binding,
            records,
            entries,
            log_entries,
            files,
        })
    }
}

#[cfg(test)]
#[path = "historical_run_learning_tests.rs"]
mod tests;
