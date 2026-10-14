//! EXEC RE-2 / CE-16 and RC-8 / CE-10. Ended arrivals receive later verified
//! App-file act observations. A performed single-file A4/A6/A7 can lapse on
//! current content. This never evaluates native items, counts a new act or
//! resumes a run.
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
    lapse: Option<LapseState>,
    end_binding_limit: Option<String>,
    lapse_limit: Option<String>,
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
            lapse: None,
            end_binding_limit: None,
            lapse_limit: None,
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
#[derive(Clone)]
struct LapsePlan {
    paths: Vec<PathBuf>,
    arrivals: Vec<Value>,
}
struct LapseState {
    revision: u64,
    read: ActRead,
    plan: LapsePlan,
    files: Vec<(PathBuf, crate::checkpoint_recorder::Current)>,
}
struct LapsePending {
    path: PathBuf,
    run: String,
    members: Vec<PendingRunEntry>,
    binding: Vec<Value>,
    acts: Vec<Value>,
}
#[derive(Default)]
pub(crate) struct Observer {
    scope: Option<Scope>,
    cache: BTreeMap<PathBuf, Cached>,
    candidates: Option<Candidates>,
    pending: BTreeMap<(String, String, String), PendingRunEntry>,
    rows: Vec<Value>,
    limits: Vec<String>,
    recording_limit: Option<String>,
    pending_activity: Option<crate::storage::Ownership>,
    lapse_pending: Vec<LapsePending>,
    files: BTreeMap<PathBuf, FileIdentity>,
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
    pub lapse_projections: usize,
    pub lapse_row_materializations: usize,
}
impl Observer {
    pub(crate) fn has_pending(&self) -> bool {
        self.pending.values().any(PendingRunEntry::pending)
            || self
                .lapse_pending
                .iter()
                .any(|p| p.members.iter().any(PendingRunEntry::pending))
    }
    pub(crate) fn observe(&mut self, project: &Path) {
        if let Err(reason) = self.attempt(project).and_then(|_| {
            #[cfg(test)]
            BETWEEN_PHASES.with(|hook| {
                if let Some(h) = hook.borrow_mut().take() {
                    h()
                }
            });
            self.observe_lapses(project)
        }) {
            self.rows.clear();
            self.limits = vec![reason.clone()];
            for cached in self.cache.values_mut() {
                cached.dirty = true;
            }
            for pending in self.pending.values_mut().filter(|p| p.pending()) {
                pending.failure = Some(reason.clone());
            }
            for pending in self
                .lapse_pending
                .iter_mut()
                .flat_map(|p| p.members.iter_mut())
                .filter(|p| p.pending())
            {
                pending.failure = Some(reason.clone());
            }
        }
        if !self.has_pending() {
            self.pending_activity = None;
        }
    }
    fn attempt(&mut self, project: &Path) -> Result<(), String> {
        let scope = Scope::read(project)?;
        if self.scope.as_ref().is_some_and(|old| old != &scope) {
            return Err("after-run-end project/store source identity changed; no reassociation or recording".into());
        }
        self.scope = Some(scope.clone());
        // Closed payload remains readable history. Admission is held through
        // this phase before any new identity/body is reserved or published.
        let admission = crate::records_retention::write_path(&scope.dir);
        let was_refused = self.recording_limit.is_some();
        self.recording_limit = admission.as_ref().err().cloned();
        if was_refused && admission.is_ok() {
            // Reopen can admit observations already discoverable in retained
            // history; no native/record revision need have changed meanwhile.
            for cached in self.cache.values_mut() {
                cached.dirty = true;
                cached.lapse = None;
            }
        }
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
            cached.end_binding_limit = binding_limit.clone();
            if let Some(reason) = &binding_limit {
                cached
                    .limits
                    .push(format!("run {run}: {reason}; no post-end relation"));
            }
            let outputs = if admission.is_ok() && cached.limits.is_empty() {
                relations(&cached.entries, candidates, &scope.root, &mut cached.limits)
            } else {
                vec![]
            };
            #[cfg(test)]
            {
                self.work.matched_acts += outputs.len();
            }
            if !outputs.is_empty() {
                retain_pending_activity(&mut self.pending_activity, &scope)?;
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
            if let Err(reason) = &admission {
                for (_, p) in self
                    .pending
                    .iter_mut()
                    .filter(|(k, p)| k.0 == run && p.pending())
                {
                    p.failure.get_or_insert(reason.clone());
                }
            }
            if admission.is_ok() && self.pending.iter().any(|(k, p)| k.0 == run && p.pending()) {
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
    fn observe_lapses(&mut self, project: &Path) -> Result<(), String> {
        let Some(scope) = self.scope.clone() else {
            return Ok(());
        };
        if !self.cache.values().any(|c| c.ended) {
            return Ok(());
        }
        let _owner = crate::storage::try_read_lock(&scope.dir.join(".after-run-end.lock"))?
            .ok_or("ended lapse observation busy; retried")?;
        if Scope::read(project)? != scope {
            return Err("ended lapse project/store source identity changed".into());
        }
        let admission = crate::records_retention::write_path(&scope.dir);
        self.recording_limit = admission.as_ref().err().cloned();
        let read = crate::checkpoint_recorder::project_act_records(&scope.root)?;
        let mut changed_rows = std::collections::BTreeSet::new();
        crate::records_index::with_index(&scope.root, |ix| -> Result<(), String> {
            if !ix.limits().is_empty() {
                return Err("ended lapse sources incomplete after ownership".into());
            }
            for (path, cached) in &mut self.cache {
                let revision = ix
                    .log_revision(path)
                    .ok_or("ended source disappeared after ownership")?;
                if revision != cached.revision {
                    // Apply the same full-source validation and bounded entry
                    // projection as discovery, including a concurrent append.
                    let mut refreshed = Cached::new(revision, ix.entries_in_log(path)?);
                    refreshed.row = cached.row.take();
                    *cached = refreshed;
                    changed_rows.insert(path.clone());
                    #[cfg(test)]
                    {
                        self.work.decoded_logs += 1;
                    }
                }
            }
            Ok(())
        })?;
        let home = crate::records_store::home(&scope.root)?;
        let base = if home.store_mode {
            scope.dir.clone()
        } else {
            scope.root.join(".chirality/records")
        };
        let mut observations = BTreeMap::new();
        for (path, cached) in &mut self.cache {
            if !cached.ended || admission.is_err() {
                continue;
            }
            let run = match owning_run(&base, path, &cached.entries) {
                Ok(run) => run,
                Err(reason) => {
                    if cached.row.is_some() {
                        changed_rows.insert(path.clone());
                    }
                    cached.row = None;
                    cached.limits.push(reason);
                    continue;
                }
            };
            if self
                .lapse_pending
                .iter()
                .any(|p| p.path == *path && p.members.iter().any(PendingRunEntry::pending))
            {
                continue;
            }
            let changed = cached.lapse.as_ref().is_none_or(|old| {
                old.revision != cached.revision || !old.read.same_observation(&read)
            });
            let plan = if changed {
                match lapse_paths(&cached.entries, &read, &scope.root) {
                    Ok(paths) => {
                        if cached.lapse_limit.take().is_some() {
                            changed_rows.insert(path.clone());
                        }
                        paths
                    }
                    Err(reason) => {
                        cached
                            .limits
                            .push(format!("run {run}: {reason}; no post-end lapse"));
                        if cached.lapse_limit.as_deref() != Some(reason.as_str()) {
                            changed_rows.insert(path.clone());
                        }
                        mark_lapse_limit(cached, &reason);
                        continue;
                    }
                }
            } else {
                cached.lapse.as_ref().unwrap().plan.clone()
            };
            let current = plan
                .paths
                .iter()
                .map(|path| {
                    let value = observations.entry(path.clone()).or_insert_with(|| {
                        current_file(
                            &scope.root,
                            (scope.device, scope.inode),
                            path,
                            &mut self.files,
                        )
                    });
                    (path.clone(), value.clone())
                })
                .collect::<Vec<_>>();
            if !changed
                && cached
                    .lapse
                    .as_ref()
                    .is_some_and(|old| old.files == current)
            {
                continue;
            }
            #[cfg(test)]
            {
                self.work.lapse_projections += 1;
            }
            let now = crate::util::now_rfc3339();
            let outputs = crate::checkpoint_recorder::observe_ended_lapses(
                &cached.entries,
                &read,
                &now,
                &plan.arrivals,
                &mut |subject| {
                    current
                        .iter()
                        .find(|(path, _)| path == subject)
                        .map(|(_, value)| value.clone())
                        .unwrap_or_else(|| {
                            crate::checkpoint_recorder::Current::Unavailable(
                                "original counted file binding unavailable".into(),
                            )
                        })
                },
            );
            let binding = lapse_binding(&cached.entries);
            if !outputs.is_empty() {
                retain_pending_activity(&mut self.pending_activity, &scope)?;
                changed_rows.insert(path.clone());
            }
            for unit in crate::checkpoint_recorder::units(&outputs) {
                let mut members = outputs[unit]
                    .iter()
                    .map(|(kind, body)| PendingRunEntry::new(kind, body.clone(), now.clone()))
                    .collect::<Result<Vec<_>, _>>()?;
                if members.len() > 1 {
                    let group = members[0].record_id.clone();
                    for member in &mut members {
                        member.group = Some(group.clone());
                    }
                }
                let mut ids = std::collections::BTreeSet::new();
                for member in &members {
                    if let Some(id) = member.body["act"]["recordId"].as_str() {
                        ids.insert(id);
                    }
                    for annotation in member.body["annotations"].as_array().into_iter().flatten() {
                        for id in annotation["actRefs"]
                            .as_array()
                            .into_iter()
                            .flatten()
                            .filter_map(Value::as_str)
                        {
                            ids.insert(id);
                        }
                    }
                }
                let acts = ids
                    .into_iter()
                    .filter_map(|id| {
                        read.acts
                            .iter()
                            .find(|a| a["record"]["recordId"] == id)
                            .map(|a| a["record"].clone())
                    })
                    .collect();
                self.lapse_pending.push(LapsePending {
                    path: path.clone(),
                    run: run.clone(),
                    members,
                    binding: binding.clone(),
                    acts,
                });
            }
            cached.lapse = Some(LapseState {
                revision: cached.revision,
                read: read.clone(),
                plan,
                files: current,
            });
        }
        for pending in &mut self.lapse_pending {
            if !pending.members.iter().any(PendingRunEntry::pending) {
                continue;
            }
            #[cfg(test)]
            BEFORE_WRITE.with(|hook| {
                if let Some(h) = hook.borrow_mut().take() {
                    h()
                }
            });
            let result = (|| {
                if let Err(reason) = &admission {
                    return Err(reason.clone());
                }
                if Scope::read(project)? != scope {
                    return Err("original ended lapse source identity changed".into());
                }
                let fresh = crate::checkpoint_recorder::project_act_records(&scope.root)?;
                let current = crate::records_index::with_index(&scope.root, |ix| {
                    if !ix.limits().is_empty() {
                        return Err(
                            "ended lapse record sources incomplete before publication".into()
                        );
                    }
                    ix.entries_in_log(&pending.path)
                })?;
                if owning_run(&base, &pending.path, &current)? != pending.run {
                    return Err("original owning run changed".into());
                }
                lapse_paths(&current, &fresh, &scope.root)?;
                for original in &pending.binding {
                    if current
                        .iter()
                        .find(|e| e["recordId"] == original["recordId"])
                        != Some(original)
                        || fresh
                            .record_limit(original["recordId"].as_str().unwrap_or_default())
                            .is_some()
                    {
                        return Err("original counted/arrival/lapse source changed or unresolved; no reassociation".into());
                    }
                }
                for original in &pending.acts {
                    if !fresh.acts.iter().any(|a| a["record"] == *original) {
                        return Err(
                            "original counted act unavailable or changed; lapse held".into()
                        );
                    }
                }
                // c1 was coherently observed before reservation. Later ordinary
                // file edits do not rewrite or discard this historical interval.
                crate::records::supply::append_run_group_in(
                    &scope.root,
                    &pending.run,
                    &mut pending.members,
                    crate::records::RecordSet::Complete,
                )
            })();
            let Some(cached) = self.cache.get_mut(&pending.path) else {
                continue;
            };
            changed_rows.insert(pending.path.clone());
            match result {
                Ok(records) => {
                    for record in records {
                        if !cached
                            .entries
                            .iter()
                            .any(|e| e["recordId"] == record["recordId"])
                        {
                            cached.entries.push(record);
                        }
                    }
                    #[cfg(test)]
                    AFTER_WRITE.with(|hook| {
                        if let Some(h) = hook.borrow_mut().take() {
                            h()
                        }
                    });
                    cached.lapse = None;
                }
                Err(reason) => {
                    for member in &mut pending.members {
                        member.failure.get_or_insert(reason.clone());
                    }
                    cached.limits.push(format!("ended lapse pending: {reason}"));
                }
            }
        }
        for (path, cached) in &mut self.cache {
            if !changed_rows.contains(path) {
                continue;
            }
            if let Some(row) = cached.row.as_mut() {
                #[cfg(test)]
                {
                    self.work.lapse_row_materializations += 1;
                }
                let mut records = cached.entries.clone();
                if let Some(reason) = cached
                    .lapse_limit
                    .as_ref()
                    .or(cached.end_binding_limit.as_ref())
                {
                    for entry in records
                        .iter_mut()
                        .filter(|e| e["kind"] == "checkpoint_arrival")
                    {
                        entry["afterRunEndRelationLimit"] = json!(reason);
                    }
                }
                for (_, member) in self.pending.iter().filter(|(key, member)| {
                    key.0
                        == cached
                            .entries
                            .first()
                            .and_then(|e| e["runId"].as_str())
                            .unwrap_or_default()
                        && member.pending()
                }) {
                    if let Some(existing) = records
                        .iter_mut()
                        .find(|e| e["recordId"] == member.record_id)
                    {
                        existing["written"] = json!(false);
                        existing["limit"] = json!(member.failure);
                    } else {
                        records.push(json!({"kind":member.kind,"body":member.body,"recordId":member.record_id,"observedAt":member.observed_at,"written":false,"limit":member.failure}));
                    }
                }
                for p in self.lapse_pending.iter().filter(|p| p.path == *path) {
                    for member in p.members.iter().filter(|m| m.pending()) {
                        if let Some(existing) = records
                            .iter_mut()
                            .find(|e| e["recordId"] == member.record_id)
                        {
                            existing["written"] = json!(false);
                            existing["limit"] = json!(member.failure);
                        } else {
                            records.push(json!({"kind":member.kind,"body":member.body,"recordId":member.record_id,"observedAt":member.observed_at,"written":false,"limit":member.failure,"runId":p.run}));
                        }
                    }
                }
                row["records"] = json!(records);
            }
        }
        self.lapse_pending
            .retain(|p| p.members.iter().any(PendingRunEntry::pending));
        if !changed_rows.is_empty() {
            self.rows = self.cache.values().filter_map(|c| c.row.clone()).collect();
        }
        self.limits
            .extend(self.cache.values().flat_map(|c| c.limits.iter().cloned()));
        self.limits.sort();
        self.limits.dedup();
        Ok(())
    }
    pub(crate) fn view(&self) -> Value {
        let mut held:Vec<_>=self.pending.iter().filter(|(_,p)|p.pending()).map(|((run,_,_),p)|json!({"run":run,"recordId":p.record_id,"observedAt":p.observed_at,"body":p.body,"limit":p.failure})).collect();
        held.extend(self.lapse_pending.iter().flat_map(|unit|unit.members.iter().filter(|p|p.pending()).map(|p|json!({"run":unit.run,"recordId":p.record_id,"observedAt":p.observed_at,"kind":p.kind,"body":p.body,"limit":p.failure}))));
        let mut limits = self.limits.clone();
        if let Some(reason) = &self.recording_limit {
            limits.push(format!("no new post-end observations: {reason}"));
        }
        limits.sort();
        limits.dedup();
        json!({"held":held,"runs":self.rows,"limits":limits,"pending":self.has_pending(),"standing":"After-run-end observations from this project's recorded ended arrivals. Later acts change no disposition; a counted file act can lapse on changed content. No native activity or new performance is inferred. Pending entries are held only in this App process."})
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
                    for e in row["records"].as_array().into_iter().flatten().filter(|e| {
                        matches!(
                            e["kind"].as_str(),
                            Some("act_after_run_end" | "act_lapsed" | "disposition_change")
                        )
                    }) {
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
/// Reservation and the lifetime lease are admitted under the same project
/// fence. Another controller must not close/dispose while private W2 is owed.
fn retain_pending_activity(
    activity: &mut Option<crate::storage::Ownership>,
    scope: &Scope,
) -> Result<(), String> {
    if activity.is_none() {
        let held = crate::records_retention::activity(&scope.root)?;
        if Scope::read(&scope.root)? != *scope {
            return Err(
                "pending observation activity source changed; no reservation or reassociation"
                    .into(),
            );
        }
        *activity = held;
    }
    Ok(())
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
fn owning_run(base: &Path, path: &Path, entries: &[Value]) -> Result<String, String> {
    let run = entries
        .first()
        .and_then(|e| e["runId"].as_str())
        .ok_or("owning run absent")?;
    let expected = base
        .join("runs")
        .join(crate::storage::key(run))
        .join(format!(
            "{}.jsonl",
            crate::storage::key(crate::records::supply::LIVE_WRITER)
        ));
    if path != expected
        || entries.iter().any(|e| {
            e["runId"] != run
                || e["recorder"]["role"] != crate::records::APP_WRITER.role
                || e["recorder"]["identity"] != crate::records::APP_WRITER.identity
        })
    {
        return Err("entries outside the exact App owning run source; no post-end lapse".into());
    }
    Ok(run.to_owned())
}
fn lapse_binding(entries: &[Value]) -> Vec<Value> {
    entries
        .iter()
        .filter(|e| {
            matches!(
                e["kind"].as_str(),
                Some(
                    "run_opened"
                        | "run_ended"
                        | "checkpoint_arrival"
                        | "act_counted"
                        | "disposition_change"
                        | "act_lapsed"
                )
            )
        })
        .cloned()
        .collect()
}
fn mark_lapse_limit(cached: &mut Cached, reason: &str) {
    cached.lapse_limit = Some(reason.to_owned());
    if let Some(records) = cached
        .row
        .as_mut()
        .and_then(|r| r["records"].as_array_mut())
    {
        for entry in records
            .iter_mut()
            .filter(|e| e["kind"] == "checkpoint_arrival")
        {
            entry["afterRunEndRelationLimit"] = json!(reason);
        }
    }
    cached.lapse = None;
}
fn lapse_paths(entries: &[Value], read: &ActRead, root: &Path) -> Result<LapsePlan, String> {
    eligible(entries, read)?;
    for entry in lapse_binding(entries) {
        if let Some(reason) = read.record_limit(entry["recordId"].as_str().unwrap_or_default()) {
            return Err(format!("{}: {reason}", entry["recordId"]));
        }
    }
    let mut paths = std::collections::BTreeSet::new();
    let mut arrivals = Vec::new();
    for (arrival, performance, content) in crate::checkpoint_recorder::ended_lapse_basis(entries) {
        if !matches!(arrival["requiredAct"].as_str(), Some("A4" | "A6" | "A7")) {
            continue;
        }
        let files = subjects(root, &json!({"body":arrival}));
        if files.len() != 1 || arrival["referents"].as_array().is_none_or(|r| r.len() != 1) {
            continue;
        }
        let end = entries
            .iter()
            .position(|e| e["kind"] == "run_ended")
            .ok_or("ended source absent")?;
        let reference =
            json!({"checkpoint":arrival["checkpoint"],"arrivalOrdinal":arrival["arrivalOrdinal"]});
        if entries[end + 1..].iter().any(|e| {
            e["body"]["arrival"] == reference
                && (e["kind"] == "act_counted"
                    || (e["kind"] == "disposition_change"
                        && matches!(
                            e["body"]["disposition"].as_str(),
                            Some("performed" | "lapsed")
                        )
                        && (e["body"]["performanceOrdinal"] != performance["performanceOrdinal"]
                            || e["body"]["answeredBy"] != performance["answeredBy"])))
        }) {
            return Err(
                "new count or conflicting performance association after the recorded end; no post-end reassociation".into(),
            );
        }
        let ids = performance["answeredBy"]
            .as_array()
            .ok_or("performed source has no counted act references")?;
        if ids.is_empty() {
            return Err("performed source names no counted act".into());
        }
        for id in ids {
            let act = read
                .acts
                .iter()
                .map(|a| &a["record"])
                .find(|r| r["recordId"] == *id && r["kind"] == "human_act")
                .ok_or("counted act reference unavailable/unresolved")?;
            let body = &act["body"];
            if body["actKind"] != arrival["requiredAct"]
                || body["boundSubject"]
                    != json!([files[0]
                        .to_str()
                        .ok_or("original subject path is not representable")?])
                || body["boundContent"].as_array().is_none_or(|v| v.len() != 1)
                || body["boundContent"][0]["method"] != content["method"]
                || body["boundContent"][0]["value"] != content["value"]
            {
                return Err(
                    "counted act does not bind the ended performance's exact file/content/kind"
                        .into(),
                );
            }
            let reference = json!({"checkpoint":arrival["checkpoint"],"arrivalOrdinal":arrival["arrivalOrdinal"]});
            if !entries[..end].iter().any(|e| {
                e["kind"] == "act_counted"
                    && e["body"]["arrival"] == reference
                    && e["body"]["act"]["recordId"] == *id
                    && e["body"]["act"]["actKind"] == body["actKind"]
                    && e["body"]["act"]["capturedAt"] == body["captureTime"]
                    && e["body"]["act"]["capturingSurface"] == "app_act_control"
            }) {
                return Err("ended performance lacks its exact counted-act citation".into());
            }
            paths.insert(files[0].clone());
        }
        arrivals.push(reference);
    }
    Ok(LapsePlan {
        paths: paths.into_iter().collect(),
        arrivals,
    })
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
// Current bytes are mutable; project/store/run identities are not. Each read
// walks opened physical folders without following a link, and checks every
// owning name again. A missing component is absence only within that proved
// physical chain. Leaf-only stamps never authorize a cache hit by themselves.
type FileStamp = (u64, u64, u64, i64, i64, i64, i64);
fn file_stamp(m: &std::fs::Metadata) -> FileStamp {
    (
        m.dev(),
        m.ino(),
        m.len(),
        m.mtime(),
        m.mtime_nsec(),
        m.ctime(),
        m.ctime_nsec(),
    )
}
struct FileIdentity {
    stamp: FileStamp,
    value: String,
    read_at: i64,
}
fn current_file(
    root: &Path,
    owner: (u64, u64),
    subject: &Path,
    cache: &mut BTreeMap<PathBuf, FileIdentity>,
) -> crate::checkpoint_recorder::Current {
    use crate::checkpoint_recorder::Current;
    match read_current_file(root, owner, subject, cache) {
        Ok(value) => value,
        Err(reason) => {
            cache.remove(subject);
            Current::Unavailable(reason)
        }
    }
}
fn read_current_file(
    root: &Path,
    owner: (u64, u64),
    subject: &Path,
    cache: &mut BTreeMap<PathBuf, FileIdentity>,
) -> Result<crate::checkpoint_recorder::Current, String> {
    use crate::checkpoint_recorder::Current;
    use sha2::Digest;
    use std::{
        fs::File,
        io::Read,
        os::{
            fd::{AsRawFd, FromRawFd},
            unix::{ffi::OsStrExt, fs::OpenOptionsExt},
        },
    };
    let rel = subject
        .strip_prefix(root)
        .map_err(|_| "bound file is outside its original project")?;
    let parts = rel
        .components()
        .map(|part| match part {
            std::path::Component::Normal(s) => Ok(s),
            _ => Err("bound file is not a plain original project path"),
        })
        .collect::<Result<Vec<_>, _>>()?;
    if parts.is_empty() {
        return Err("bound file is the project folder".into());
    }
    if !root.is_absolute() {
        return Err("owning project is not an absolute physical path".into());
    }
    let folder = std::fs::OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open("/")
        .map_err(|e| e.to_string())?;
    let mut owners = vec![(PathBuf::from("/"), folder)];
    fn names(owners: &[(PathBuf, File)]) -> Result<(), String> {
        for (path, file) in owners {
            let opened = file.metadata().map_err(|e| e.to_string())?;
            let named = std::fs::symlink_metadata(path).map_err(|e| e.to_string())?;
            if !opened.is_dir()
                || !named.is_dir()
                || (opened.dev(), opened.ino()) != (named.dev(), named.ino())
            {
                return Err("original owning folder name changed or is aliased".into());
            }
        }
        Ok(())
    }
    for component in root.components().skip(1) {
        let std::path::Component::Normal(part) = component else {
            return Err("owning project name is not plain".into());
        };
        let name = std::ffi::CString::new(part.as_bytes())
            .map_err(|_| "owning folder name contains NUL")?;
        let fd = unsafe {
            libc::openat(
                owners.last().unwrap().1.as_raw_fd(),
                name.as_ptr(),
                libc::O_RDONLY
                    | libc::O_DIRECTORY
                    | libc::O_NOFOLLOW
                    | libc::O_CLOEXEC
                    | libc::O_NONBLOCK,
            )
        };
        if fd < 0 {
            return Err(format!(
                "physical owning project unavailable: {}",
                std::io::Error::last_os_error()
            ));
        }
        let file = unsafe { File::from_raw_fd(fd) };
        let path = owners.last().unwrap().0.join(part);
        owners.push((path, file));
    }
    names(&owners)?;
    let opened_root = owners
        .last()
        .unwrap()
        .1
        .metadata()
        .map_err(|e| e.to_string())?;
    if (opened_root.dev(), opened_root.ino()) != owner {
        return Err("original physical project identity changed".into());
    }
    for (at, part) in parts.iter().enumerate() {
        let parent = &owners.last().unwrap().1;
        let before_parent = parent.metadata().map_err(|e| e.to_string())?;
        let name =
            std::ffi::CString::new(part.as_bytes()).map_err(|_| "bound file name contains NUL")?;
        let last = at + 1 == parts.len();
        let flags = libc::O_RDONLY
            | libc::O_NOFOLLOW
            | libc::O_CLOEXEC
            | libc::O_NONBLOCK
            | if last { 0 } else { libc::O_DIRECTORY };
        let fd = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) };
        if fd < 0 {
            let error = std::io::Error::last_os_error();
            names(&owners)?;
            let after_parent = owners
                .last()
                .unwrap()
                .1
                .metadata()
                .map_err(|e| e.to_string())?;
            if error.kind() == std::io::ErrorKind::NotFound
                && file_stamp(&before_parent) == file_stamp(&after_parent)
            {
                names(&owners)?;
                cache.remove(subject);
                return Ok(Current::Absent);
            }
            return Err(format!("original bound file unavailable: {error}"));
        }
        let mut file = unsafe { File::from_raw_fd(fd) };
        if !last {
            let path = owners.last().unwrap().0.join(part);
            owners.push((path, file));
            names(&owners)?;
            continue;
        }
        let before = file.metadata().map_err(|e| e.to_string())?;
        if !before.is_file() {
            return Err("bound subject is not a regular file".into());
        }
        const CAP: u64 = 256 * 1024 * 1024;
        if before.len() > CAP {
            return Err(format!("bound file is larger than {CAP} bytes; not read"));
        }
        let read_at = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map_err(|e| e.to_string())?
            .as_secs() as i64;
        let kept = cache
            .get(subject)
            .filter(|old| old.stamp == file_stamp(&before) && old.read_at > before.ctime() + 1)
            .map(|old| old.value.clone());
        let value = match kept {
            Some(value) => value,
            None => {
                let mut hash = sha2::Sha256::new();
                let mut buf = [0u8; 64 * 1024];
                let mut total = 0u64;
                loop {
                    let n = file.read(&mut buf).map_err(|e| e.to_string())?;
                    if n == 0 {
                        break;
                    }
                    total += n as u64;
                    if total > CAP {
                        return Err("bound file grew beyond the read limit".into());
                    }
                    hash.update(&buf[..n]);
                }
                format!("{:x}", hash.finalize())
            }
        };
        #[cfg(test)]
        DURING_FILE_READ.with(|hook| {
            if let Some(h) = hook.borrow_mut().take() {
                h(subject)
            }
        });
        let after = file.metadata().map_err(|e| e.to_string())?;
        names(&owners)?;
        let named = std::fs::symlink_metadata(subject).map_err(|e| e.to_string())?;
        if !named.is_file()
            || file_stamp(&before) != file_stamp(&after)
            || file_stamp(&after) != file_stamp(&named)
        {
            return Err("bound file changed while observed".into());
        }
        names(&owners)?;
        cache.insert(
            subject.to_owned(),
            FileIdentity {
                stamp: file_stamp(&after),
                value: value.clone(),
                read_at,
            },
        );
        return Ok(Current::Present(value));
    }
    Err("bound file source is absent".into())
}
#[cfg(test)]
thread_local! {static DURING_FILE_READ:std::cell::RefCell<Option<Box<dyn FnOnce(&Path)>>>=const{std::cell::RefCell::new(None)};}

#[cfg(test)]
thread_local! {pub(crate) static BETWEEN_PHASES:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
thread_local! {pub(crate) static AFTER_WRITE:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
thread_local! {pub(crate) static BEFORE_WRITE:std::cell::RefCell<Option<Box<dyn FnOnce()>>>=const{std::cell::RefCell::new(None)};}
#[cfg(test)]
#[path = "after_run_end_tests.rs"]
mod tests;
