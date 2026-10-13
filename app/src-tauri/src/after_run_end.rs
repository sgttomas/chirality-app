//! EXEC RE-2 / CE-16. Ended arrivals receive observations of later verified
//! App-file acts. This never evaluates native items, counts an act, observes
//! a lapse, resumes a run or changes an arrival's final disposition.
use crate::{checkpoint_recorder::ActRead, records::supply::PendingRunEntry};
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
};

#[derive(Clone, PartialEq, Eq)]
struct Scope {
    root: PathBuf,
    device: u64,
    inode: u64,
    project: String,
    dir: PathBuf,
    dir_device: u64,
    dir_inode: u64,
}
impl Scope {
    fn read(project: &Path) -> Result<Self, String> {
        let root = project.canonicalize().map_err(|e| e.to_string())?;
        crate::storage::check_path(&root)?;
        let meta = std::fs::symlink_metadata(&root).map_err(|e| e.to_string())?;
        let home = crate::records_store::home(&root)?;
        if let Some(reason) = home.attachment.refusal {
            return Err(reason);
        }
        let dir = home
            .attachment
            .dir
            .ok_or("project identity unavailable; after-run-end observation records nothing")?;
        crate::storage::check_path(&dir)?;
        let d = std::fs::symlink_metadata(&dir).map_err(|e| e.to_string())?;
        if !meta.is_dir() || !d.is_dir() {
            return Err("after-run-end source is not a physical folder".into());
        }
        Ok(Self {
            root,
            device: meta.dev(),
            inode: meta.ino(),
            project: home
                .attachment
                .project
                .ok_or("project identity unavailable")?,
            dir,
            dir_device: d.dev(),
            dir_inode: d.ino(),
        })
    }
}
struct Cached {
    revision: u64,
    entries: Vec<Value>,
    ended: bool,
    row: Option<Value>,
    limits: Vec<String>,
    dirty: bool,
}
impl Cached {
    fn new(revision: u64, mut entries: Vec<Value>) -> Self {
        // Check all source entries before retaining the bounded presentation.
        if entries.first().is_some_and(|first| {
            entries.iter().all(|e| {
                e["runId"] == first["runId"]
                    && e["recorder"]["role"] == crate::records::APP_WRITER.role
                    && e["recorder"]["identity"] == crate::records::APP_WRITER.identity
            })
        }) {
            entries.retain(presentation_entry);
        }
        let ended = entries.iter().any(|e| e["kind"] == "run_ended");
        Self {
            revision,
            entries,
            ended,
            row: None,
            limits: vec![],
            dirty: true,
        }
    }
}
/// Positions into the immutable verified observation, not another copy of
/// the act/capture bodies. Built once per changed verified read basis.
struct Candidates {
    read: ActRead,
    by_subject: BTreeMap<PathBuf, Vec<usize>>,
    unresolved_by_subject: BTreeMap<PathBuf, Vec<usize>>,
}
impl Candidates {
    fn new(read: ActRead) -> Self {
        let mut by_subject: BTreeMap<PathBuf, Vec<usize>> = BTreeMap::new();
        for (position, claim) in read.acts.iter().enumerate() {
            if claim["record"]["kind"] != "human_act" {
                continue;
            }
            for subject in claim["record"]["body"]["boundSubject"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(Value::as_str)
            {
                by_subject
                    .entry(PathBuf::from(subject))
                    .or_default()
                    .push(position);
            }
        }
        let mut unresolved_by_subject: BTreeMap<PathBuf, Vec<usize>> = BTreeMap::new();
        for (position, claim) in read.unresolved.iter().enumerate() {
            for subject in claim["record"]["body"]["boundSubject"]
                .as_array()
                .into_iter()
                .flatten()
                .filter_map(Value::as_str)
            {
                unresolved_by_subject
                    .entry(PathBuf::from(subject))
                    .or_default()
                    .push(position);
            }
        }
        Self {
            read,
            by_subject,
            unresolved_by_subject,
        }
    }
}
#[derive(Default)]
pub(crate) struct Observer {
    scope: Option<Scope>,
    cache: BTreeMap<PathBuf, Cached>,
    candidates: Option<Candidates>,
    pending: BTreeMap<(String, String, String), PendingRunEntry>,
    rows: Vec<Value>,
    limits: Vec<String>,
    #[cfg(test)]
    pub(crate) work: Work,
}
#[cfg(test)]
#[derive(Default, Clone, Debug, PartialEq, Eq)]
pub(crate) struct Work {
    pub decoded_logs: usize,
    pub candidate_builds: usize,
    pub projected_runs: usize,
    pub matched_acts: usize,
}
impl Observer {
    pub(crate) fn has_pending(&self) -> bool {
        self.pending.values().any(PendingRunEntry::pending)
    }
    pub(crate) fn observe(&mut self, project: &Path) {
        if let Err(reason) = self.attempt(project) {
            self.rows.clear();
            self.limits = vec![reason.clone()];
            for cached in self.cache.values_mut() {
                cached.dirty = true;
            }
            for pending in self.pending.values_mut().filter(|p| p.pending()) {
                pending.failure = Some(reason.clone());
            }
        }
    }
    fn attempt(&mut self, project: &Path) -> Result<(), String> {
        let scope = Scope::read(project)?;
        if self.scope.as_ref().is_some_and(|old| old != &scope) {
            return Err("after-run-end project/store source identity changed; no reassociation or recording".into());
        }
        self.scope = Some(scope.clone());
        // Resolve the current ordinary record home once, not once per run.
        let home = crate::records_store::home(&scope.root)?;
        let base = if home.store_mode {
            scope.dir.clone()
        } else {
            scope.root.join(".chirality/records")
        };
        let writer = format!(
            "{}.jsonl",
            crate::storage::key(crate::records::supply::LIVE_WRITER)
        );
        let mut changed = false;
        crate::records_index::with_index(&scope.root, |ix| -> Result<(), String> {
            let limits = ix.limits();
            if !limits.is_empty() {
                return Err(format!(
                    "after-run-end record sources incomplete: {limits:?}"
                ));
            }
            let paths: std::collections::BTreeSet<_> = ix
                .paths()
                .into_iter()
                .filter(|p| {
                    p.file_name().is_some_and(|n| n == writer.as_str())
                        && p.parent()
                            .and_then(Path::parent)
                            .and_then(Path::file_name)
                            .is_some_and(|n| n == "runs")
                })
                .collect();
            let old = self.cache.len();
            self.cache.retain(|path, _| paths.contains(path));
            changed |= self.cache.len() != old;
            for path in paths {
                let revision = ix.log_revision(&path).ok_or("run source disappeared")?;
                if self.cache.get(&path).is_none_or(|c| c.revision != revision) {
                    self.cache.insert(
                        path.clone(),
                        Cached::new(revision, ix.entries_in_log(&path)?),
                    );
                    changed = true;
                    #[cfg(test)]
                    {
                        self.work.decoded_logs += 1;
                    }
                }
            }
            Ok(())
        })?;
        let has_ended = self.cache.values().any(|c| c.ended);
        // The shared reader checks source/capture/name/key freshness on warm
        // ticks too. Its unchanged immutable observation retains this index.
        let mut acts_changed = if has_ended {
            let read = crate::checkpoint_recorder::project_act_records(&scope.root)?;
            if self
                .candidates
                .as_ref()
                .is_none_or(|old| !old.read.same_observation(&read))
            {
                self.candidates = Some(Candidates::new(read));
                #[cfg(test)]
                {
                    self.work.candidate_builds += 1;
                }
                true
            } else {
                false
            }
        } else {
            false
        };
        if !changed && !acts_changed && !self.has_pending() && !self.cache.values().any(|c| c.dirty)
        {
            return Ok(());
        }
        // An owning control serializes this observer's publication across App
        // processes; no control is created for an empty/no-ended-source project.
        let _owner = if has_ended {
            Some(
                crate::storage::try_read_lock(&scope.dir.join(".after-run-end.lock"))?
                    .ok_or("after-run-end observation busy; retried by the host")?,
            )
        } else {
            None
        };
        // Another App process may have published while this observer waited
        // for ownership. Refresh changed owning logs before reserving any new
        // identity, so its durable relation is deduped under this same control.
        if has_ended {
            crate::records_index::with_index(&scope.root, |ix| -> Result<(), String> {
                let limits = ix.limits();
                if !limits.is_empty() {
                    return Err(format!(
                        "ended sources incomplete after ownership: {limits:?}"
                    ));
                }
                for (path, cached) in &mut self.cache {
                    let revision = ix
                        .log_revision(path)
                        .ok_or("owning run source disappeared after ownership")?;
                    if cached.revision != revision {
                        *cached = Cached::new(revision, ix.entries_in_log(path)?);
                        #[cfg(test)]
                        {
                            self.work.decoded_logs += 1;
                        }
                    }
                }
                Ok(())
            })?;
            let read = crate::checkpoint_recorder::project_act_records(&scope.root)?;
            if self
                .candidates
                .as_ref()
                .is_none_or(|old| !old.read.same_observation(&read))
            {
                self.candidates = Some(Candidates::new(read));
                acts_changed = true;
                #[cfg(test)]
                {
                    self.work.candidate_builds += 1;
                }
            }
        }
        self.limits.clear();
        let mut fresh: Option<Candidates> = None;
        for (path, cached) in &mut self.cache {
            let pending_here = self.pending.iter().any(|(k, p)| {
                p.pending() && cached.entries.first().is_some_and(|e| e["runId"] == k.0)
            });
            if !cached.dirty && !acts_changed && !pending_here {
                continue;
            }
            cached.dirty = false;
            cached.limits.clear();
            cached.row = None;
            if !cached.ended {
                continue;
            }
            #[cfg(test)]
            {
                self.work.projected_runs += 1;
            }
            let Some(run) = cached
                .entries
                .first()
                .and_then(|e| e["runId"].as_str())
                .map(str::to_owned)
            else {
                continue;
            };
            let expected = base
                .join("runs")
                .join(crate::storage::key(&run))
                .join(&writer);
            if path != &expected
                || cached.entries.iter().any(|e| {
                    e["runId"] != run
                        || e["recorder"]["role"] != crate::records::APP_WRITER.role
                        || e["recorder"]["identity"] != crate::records::APP_WRITER.identity
                })
            {
                cached.limits.push(format!("run {run}: entries outside its exact App owning run source; no post-end relation"));
                continue;
            }
            let candidates = self
                .candidates
                .as_ref()
                .ok_or("verified act observation unavailable")?;
            let binding_limit = eligible(&cached.entries, &candidates.read).err();
            if let Some(reason) = &binding_limit {
                cached
                    .limits
                    .push(format!("run {run}: {reason}; no post-end relation"));
            }
            let outputs = if cached.limits.is_empty() {
                relations(&cached.entries, candidates, &scope.root, &mut cached.limits)
            } else {
                vec![]
            };
            #[cfg(test)]
            {
                self.work.matched_acts += outputs.len();
            }
            let now = crate::util::now_rfc3339();
            for (arrival_id, body) in outputs {
                let key = (
                    run.clone(),
                    arrival_id,
                    body["act"]["recordId"].as_str().unwrap().to_owned(),
                );
                if !self.pending.contains_key(&key) {
                    self.pending.insert(
                        key,
                        PendingRunEntry::new("act_after_run_end", body, now.clone())?,
                    );
                }
            }
            if self.pending.iter().any(|(k, p)| k.0 == run && p.pending()) {
                #[cfg(test)]
                BEFORE_WRITE.with(|h| {
                    if let Some(hook) = h.borrow_mut().take() {
                        hook();
                    }
                });
                if Scope::read(project)? != scope {
                    return Err("after-run-end source changed before recording".into());
                }
                let revalidated = crate::checkpoint_recorder::project_act_records(&scope.root)?;
                if fresh
                    .as_ref()
                    .is_none_or(|old| !old.read.same_observation(&revalidated))
                {
                    fresh = Some(Candidates::new(revalidated));
                }
                let current = crate::records_index::with_index(&scope.root, |ix| {
                    let limits = ix.limits();
                    if !limits.is_empty() {
                        return Err(format!("ended source incomplete before write: {limits:?}"));
                    }
                    ix.entries_in_log(path)
                })?;
                let current_eligible = eligible(&current, &fresh.as_ref().unwrap().read);
                let evidence_same = critical(&current) == critical(&cached.entries);
                let still = if evidence_same && current_eligible.is_ok() {
                    relations(
                        &current,
                        fresh.as_ref().unwrap(),
                        &scope.root,
                        &mut cached.limits,
                    )
                } else {
                    vec![]
                };
                for (_, pending) in self
                    .pending
                    .iter_mut()
                    .filter(|(k, p)| k.0 == run && p.pending())
                {
                    if !evidence_same || current_eligible.is_err() {
                        let reason=format!("{}: original ended-run/arrival evidence changed or unresolved; held, not written",pending.record_id);
                        pending.failure = Some(reason.clone());
                        cached.limits.push(reason);
                        continue;
                    }
                    // Durable semantic dedup after relaunch; uncertain own
                    // receipt retries its reserved identity/time for W-2.
                    if let Some(record) = current.iter().find(|e| {
                        e["kind"] == pending.kind
                            && e["body"] == pending.body
                            && e["recordId"] != pending.record_id
                    }) {
                        cached.limits.push(format!("Original {} observed at {} was not published here: the same relation is recorded as {}",pending.record_id,pending.observed_at,record["recordId"]));
                        if !cached
                            .entries
                            .iter()
                            .any(|e| e["recordId"] == record["recordId"])
                        {
                            cached.entries.push(record.clone());
                        }
                        pending.written = Some(record.clone());
                        continue;
                    }
                    if !still.iter().any(|(_, b)| b == &pending.body)
                        && !current.iter().any(|e| {
                            e["recordId"] == pending.record_id && e["body"] == pending.body
                        })
                    {
                        let reason=format!("{}: original after-run-end act evidence unavailable/changed; held, not written",pending.record_id);
                        pending.failure = Some(reason.clone());
                        cached.limits.push(reason);
                        continue;
                    }
                    match crate::records::supply::append_run_entry(&scope.root, &run, pending) {
                        Ok(record) => {
                            #[cfg(test)]
                            AFTER_WRITE.with(|h| {
                                if let Some(hook) = h.borrow_mut().take() {
                                    hook();
                                }
                            });
                            if !cached
                                .entries
                                .iter()
                                .any(|e| e["recordId"] == record["recordId"])
                            {
                                cached.entries.push(record);
                            }
                        }
                        Err(reason) => cached.limits.push(format!(
                            "{}: after-run-end record pending: {reason}",
                            pending.record_id
                        )),
                    }
                }
            }
            let mut view = cached.entries.clone();
            if let Some(reason) = &binding_limit {
                for entry in view
                    .iter_mut()
                    .filter(|e| e["kind"] == "checkpoint_arrival")
                {
                    entry["afterRunEndRelationLimit"] = json!(reason);
                }
            }
            for (_, p) in self
                .pending
                .iter()
                .filter(|(k, p)| k.0 == run && p.pending())
            {
                if let Some(existing) = view.iter_mut().find(|e| e["recordId"] == p.record_id) {
                    existing["written"] = json!(false);
                    existing["limit"] = json!(p.failure);
                } else {
                    view.push(json!({"kind":p.kind,"body":p.body,"recordId":p.record_id,"observedAt":p.observed_at,"written":false,"limit":p.failure,"runId":run}));
                }
            }
            cached.row = Some(
                json!({"run":run,"source":{"projectId":scope.project,"root":crate::attachments::native_path_identity(&scope.root)},"records":view}),
            );
        }
        self.pending.retain(|_, p| p.pending());
        self.rows = self.cache.values().filter_map(|c| c.row.clone()).collect();
        self.limits
            .extend(self.cache.values().flat_map(|c| c.limits.iter().cloned()));
        self.limits.sort();
        self.limits.dedup();
        Ok(())
    }
    pub(crate) fn view(&self) -> Value {
        let held:Vec<_>=self.pending.iter().filter(|(_,p)|p.pending()).map(|((run,_,_),p)|json!({"run":run,"recordId":p.record_id,"observedAt":p.observed_at,"body":p.body,"limit":p.failure})).collect();
        json!({"held":held,"runs":self.rows,"limits":self.limits,"pending":self.has_pending(),"standing":"After-run-end act observations from this project's recorded ended arrivals; no disposition, lapse or native activity is changed. Pending entries are held only in this App process."})
    }
    pub(crate) fn decorate(&self, run: &str, mut view: Value) -> Value {
        if let Some(row) = self.rows.iter().find(|r| r["run"] == run) {
            if self.scope.as_ref().is_some_and(|s| {
                view["project"] == crate::attachments::native_path_identity(&s.root)
            }) {
                if let Some(records) = view["lifecycle"]["records"].as_array_mut() {
                    for entry in row["records"]
                        .as_array()
                        .into_iter()
                        .flatten()
                        .filter(|e| e["kind"] == "checkpoint_arrival")
                    {
                        if let Some(current) = records
                            .iter_mut()
                            .find(|old| old["recordId"] == entry["recordId"])
                        {
                            if let Some(limit) = entry.get("afterRunEndRelationLimit") {
                                current["afterRunEndRelationLimit"] = limit.clone();
                            }
                        }
                    }
                    for e in row["records"]
                        .as_array()
                        .into_iter()
                        .flatten()
                        .filter(|e| e["kind"] == "act_after_run_end")
                    {
                        if !records.iter().any(|old| old["recordId"] == e["recordId"]) {
                            records.push(e.clone());
                        }
                    }
                }
            }
        }
        view
    }
}
fn presentation_entry(e: &Value) -> bool {
    matches!(
        e["kind"].as_str(),
        Some(
            "run_opened"
                | "run_ended"
                | "checkpoint_listed"
                | "checkpoint_arrival"
                | "disposition_change"
                | "act_counted"
                | "act_not_counted"
                | "act_request"
                | "arrival_declined"
                | "act_lapsed"
                | "run_resumed"
                | "continued_past"
                | "act_after_run_end"
                | "evidence_limit"
        )
    )
}
fn critical(entries: &[Value]) -> Vec<&Value> {
    entries
        .iter()
        .filter(|e| {
            matches!(
                e["kind"].as_str(),
                Some("run_opened" | "run_ended" | "checkpoint_arrival")
            )
        })
        .collect()
}
fn eligible(entries: &[Value], read: &ActRead) -> Result<(), String> {
    let opens: Vec<_> = entries
        .iter()
        .filter(|e| e["kind"] == "run_opened")
        .collect();
    let ends: Vec<_> = entries
        .iter()
        .filter(|e| e["kind"] == "run_ended")
        .collect();
    if opens.len() != 1
        || ends.len() != 1
        || opens[0]["body"]["surface"] != "App run"
        || opens[0]["body"]["runId"] != opens[0]["runId"]
    {
        return Err("no unique App opened/ended source".into());
    }
    let mut arrivals = std::collections::BTreeSet::new();
    for entry in critical(entries) {
        if let Some(reason) = read.record_limit(entry["recordId"].as_str().unwrap_or_default()) {
            return Err(format!("{}: {reason}", entry["recordId"]));
        }
        if entry["kind"] == "checkpoint_arrival"
            && !arrivals.insert((
                entry["body"]["checkpoint"].to_string(),
                entry["body"]["arrivalOrdinal"].to_string(),
            ))
        {
            return Err("nonunique checkpoint arrival reference".into());
        }
    }
    Ok(())
}
/// Historical subject binding, without canonicalizing/following today's file.
fn subjects(root: &Path, arrival: &Value) -> Vec<PathBuf> {
    arrival["body"]["referents"]
        .as_array()
        .into_iter()
        .flatten()
        .filter_map(|r| r["subject"].as_str())
        .filter_map(|s| s.strip_prefix("output "))
        .filter(|s| s.match_indices(": file ").count() == 1)
        .filter_map(|s| s.split_once(": file ").map(|(_, p)| p))
        .filter(|p| !p.starts_with('/') && !p.split('/').any(|part| part == ".."))
        .map(|p| {
            root.join(
                p.split('/')
                    .filter(|p| !p.is_empty() && *p != ".")
                    .collect::<PathBuf>(),
            )
        })
        .collect()
}
fn relations(
    entries: &[Value],
    candidates: &Candidates,
    root: &Path,
    limits: &mut Vec<String>,
) -> Vec<(String, Value)> {
    let Some(end) = entries.iter().find(|e| e["kind"] == "run_ended") else {
        return vec![];
    };
    let Some(end_time) = end["observedAt"]
        .as_str()
        .or_else(|| end["writtenAt"].as_str())
        .and_then(instant)
    else {
        limits.push("Run-end time not comparable; no after-run-end relation".into());
        return vec![];
    };
    let recorded: std::collections::BTreeSet<_> = entries
        .iter()
        .filter(|e| e["kind"] == "act_after_run_end")
        .map(|e| e["body"].to_string())
        .collect();
    let mut outputs = Vec::new();
    for arrival in entries.iter().filter(|e| e["kind"] == "checkpoint_arrival") {
        let files = subjects(root, arrival);
        if files.is_empty()
            && arrival["body"]["referents"]
                .as_array()
                .into_iter()
                .flatten()
                .any(|r| r["subject"].as_str().is_some_and(|s| s.contains(": file ")))
        {
            limits.push(format!(
                "{}: historical file subject not unambiguously bound; no after-run-end relation",
                arrival["recordId"]
            ));
        }
        let reference = json!({"checkpoint":arrival["body"]["checkpoint"],"arrivalOrdinal":arrival["body"]["arrivalOrdinal"]});
        let unresolved: std::collections::BTreeSet<_> = files
            .iter()
            .flat_map(|p| {
                candidates
                    .unresolved_by_subject
                    .get(p)
                    .into_iter()
                    .flatten()
                    .copied()
            })
            .collect();
        for position in unresolved {
            let claim = &candidates.read.unresolved[position];
            limits.push(format!(
                "{}: unresolvable act reference: {}; no after-run-end relation",
                claim["record"]["recordId"], claim["reason"]
            ));
        }
        let positions: std::collections::BTreeSet<_> = files
            .iter()
            .flat_map(|p| candidates.by_subject.get(p).into_iter().flatten().copied())
            .collect();
        for position in positions {
            let record = &candidates.read.acts[position]["record"];
            let b = &record["body"];
            let Some(time) = b["captureTime"].as_str().and_then(instant) else {
                limits.push(format!(
                    "{}: capture time not comparable; no after-run-end relation",
                    record["recordId"]
                ));
                continue;
            };
            if time == end_time {
                limits.push(format!(
                    "{}: capture and run-end times equal; after-run-end order not established",
                    record["recordId"]
                ));
            }
            if time <= end_time {
                continue;
            }
            let body = json!({"arrival":reference,"act":{"recordId":record["recordId"],"actKind":b["actKind"],"capturedAt":b["captureTime"],"capturingSurface":"app_act_control"}});
            if !recorded.contains(&body.to_string()) {
                outputs.push((
                    arrival["recordId"].as_str().unwrap_or_default().to_owned(),
                    body,
                ));
            }
        }
    }
    outputs
}
/// RFC3339 instant ordering only; original text remains in the record. Unknown
/// local offset (-00:00), leap seconds and precision beyond ns are unorderable.
fn instant(s: &str) -> Option<i128> {
    let b = s.as_bytes();
    if b.len() < 20
        || b[4] != b'-'
        || b[7] != b'-'
        || !matches!(b[10], b'T' | b't')
        || b[13] != b':'
        || b[16] != b':'
    {
        return None;
    }
    let n = |a, z| {
        let text = s.get(a..z)?;
        text.bytes()
            .all(|b| b.is_ascii_digit())
            .then(|| text.parse::<i64>().ok())
            .flatten()
    };
    let (y, m, d, h, min, sec) = (
        n(0, 4)?,
        n(5, 7)?,
        n(8, 10)?,
        n(11, 13)?,
        n(14, 16)?,
        n(17, 19)?,
    );
    let leap = y % 4 == 0 && (y % 100 != 0 || y % 400 == 0);
    let max = match m {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 if leap => 29,
        2 => 28,
        _ => return None,
    };
    if y < 1 || d < 1 || d > max || h > 23 || min > 59 || sec > 59 {
        return None;
    }
    let mut at = 19;
    let mut fraction = 0i128;
    if b.get(at) == Some(&b'.') {
        at += 1;
        let start = at;
        while b.get(at).is_some_and(u8::is_ascii_digit) {
            at += 1;
        }
        let len = at - start;
        if len == 0 || len > 9 {
            return None;
        }
        fraction = s.get(start..at)?.parse::<i128>().ok()? * 10i128.pow((9 - len) as u32);
    }
    let zone = s.get(at..)?;
    let offset = if matches!(zone, "Z" | "z") {
        0
    } else {
        let z = zone.as_bytes();
        if z.len() != 6 || !matches!(z[0], b'+' | b'-') || z[3] != b':' || zone == "-00:00" {
            return None;
        }
        if !z[1..3].iter().chain(z[4..6].iter()).all(u8::is_ascii_digit) {
            return None;
        }
        let hh = zone.get(1..3)?.parse::<i64>().ok()?;
        let mm = zone.get(4..6)?.parse::<i64>().ok()?;
        if hh > 23 || mm > 59 {
            return None;
        }
        (hh * 60 + mm) * 60 * if z[0] == b'+' { 1 } else { -1 }
    };
    let y = y - i64::from(m <= 2);
    let era = y.div_euclid(400);
    let yy = y - era * 400;
    let mp = m + if m > 2 { -3 } else { 9 };
    let days = era * 146097 + yy * 365 + yy / 4 - yy / 100 + (153 * mp + 2) / 5 + d - 1 - 719468;
    Some(i128::from(days * 86400 + h * 3600 + min * 60 + sec - offset) * 1_000_000_000 + fraction)
}
#[cfg(test)]
thread_local! {pub(crate) static AFTER_WRITE:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
thread_local! {pub(crate) static BEFORE_WRITE:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
#[path = "after_run_end_tests.rs"]
mod tests;
