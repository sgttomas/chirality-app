//! The state of plugins, and of apps connected to the person's ChatGPT account, in this home's
//! Codex, read for display. The reading is made after the reply that names a conversation's
//! thread (`thread/start`, `thread/resume`, `thread/fork`), with that thread's id, on a worker of
//! its own: nothing on the conversation request's path waits for it, registers it or is refused
//! by it. It is shown with the conversation, as `threads[].extensions`. Once after the home's
//! Codex is ready, a base reading with no thread is made the same way and shown as
//! `extensionsBase`, marked as the home's state before any project's settings apply; it is never
//! shown as a conversation's state.
//!
//! The state is what Codex itself reports after every layer and requirement
//! (`experimentalFeature/list`, whose `enabled` is the effective value). With the thread's id,
//! Codex includes the project settings of that thread's folder. A reading has one deadline for all
//! its pages, the frame writer and the replies together; one that does not finish by then is not
//! read, and its late completion changes nothing. A reading is bound to its generation: closing
//! or replacing the generation drops every reading of it.
//!
//! A reading never waits on Codex's input while it holds the frame writer. With the writer held, a
//! page whose frame, newline included, is no longer than the pipe's atomic size (`PIPE_BUF`) is
//! written in one write call that does not wait (`write_without_waiting`): the whole frame is
//! written, or nothing is and the reading is not read, not sent, and the writer is released at
//! once, so a conversation request that comes after it goes to its own write. A write that leaves
//! part of a frame, or leaves the input's flags changed, stops Codex with its own words.
//!
//! Where each state comes from is taken only from evidence already read on the same generation,
//! never by a further configuration reading (a configuration or requirements reading becomes the
//! generation's newest and would retire the provider reading the next request is admitted on,
//! `reading_gate`):
//! - the origins in the private `config/read` (layers included) that admitted the conversation
//!   request (`ProviderAdmission`), only when that reading was made for the folder Codex reports
//!   for the thread;
//! - the pins under `featureRequirements` in the latest answered `configRequirements/read` of the
//!   generation, only when that reply settled correctly, correlated, as a result with no error and
//!   in the native shape.
//!
//! Without that evidence the source is not established.
use super::*;

/// The method of the reading.
pub(crate) const FEATURE_LIST: &str = "experimentalFeature/list";
/// The most pages one reading follows. Codex at the pin lists every feature on one page; a longer
/// sequence is not followed and gives no reading.
pub(crate) const FEATURE_PAGE_LIMIT: usize = 8;
/// The wait for a reading when the Host was not started with one (`HostConfig::wait_limit`).
const DEFAULT_WAIT: Duration = Duration::from_secs(20);
/// The App's own bound on one reading, all its pages together, whatever the Host's wait.
const READ_BOUND: Duration = Duration::from_secs(5);
/// How long past the deadline the reading's keeper waits for the reading's own account of why it
/// ended. Nothing read after the deadline is taken as read (`feature_list_read`).
const REPORT_GRACE: Duration = Duration::from_millis(50);
const STAGES: [&str; 5] = ["beta", "underDevelopment", "stable", "deprecated", "removed"];
/// The scope of the base reading: the home's state before any project's settings apply.
pub(crate) const BASE_SCOPE: &str = "home-before-project-settings";

/// What one reading says of one feature. Only a single well-formed entry gives `On` or `Off`;
/// everything else is `NotRead`, which is never shown as off.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum State { On, Off, NotRead }
impl State {
    pub(crate) fn key(self) -> &'static str {
        match self { State::On => "on", State::Off => "off", State::NotRead => "not-read" }
    }
}

/// Where a feature's state comes from, on evidence.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Source {
    /// A managed requirement pins it, or its key's origin is a managed layer (MDM, system, legacy
    /// managed, or the enterprise cloud bundle).
    OutsideApp,
    /// Its key's origin is the user layer (this home's own `config.toml`), and the requirements
    /// were read and pin nothing for it.
    ThisHome,
    /// Its key's origin is a project layer, and the requirements were read and pin nothing for it.
    Project,
    /// No origin for its key, or Codex's packaged defaults, and no pin, both read: Codex's own default.
    Default,
    /// Not established by the evidence available.
    NotEstablished,
}
impl Source {
    pub(crate) fn key(self) -> &'static str {
        match self {
            Source::OutsideApp => "outside-app",
            Source::ThisHome => "this-home",
            Source::Project => "project",
            Source::Default => "default",
            Source::NotEstablished => "not-established",
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Feature { Plugins, Apps }
impl Feature {
    /// The name Codex lists the feature under.
    fn name(self) -> &'static str { match self { Feature::Plugins => "plugins", Feature::Apps => "apps" } }
    /// The names a requirement can pin it under: `connectors` is a second name for apps.
    fn requirement_names(self) -> &'static [&'static str] {
        match self { Feature::Plugins => &["plugins"], Feature::Apps => &["apps", "connectors"] }
    }
    /// Its configuration keys, the one that prevails first: within one features table Codex applies
    /// `connectors` after `apps`, so `connectors`, where present, decides.
    fn origin_keys(self) -> &'static [&'static str] {
        match self { Feature::Plugins => &["features.plugins"], Feature::Apps => &["features.connectors", "features.apps"] }
    }
}

/// One feature's state, and why it was not read when it was not.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct Observed { pub(crate) state: State, pub(crate) not_read_because: Option<&'static str> }
impl Observed {
    fn not_read(because: &'static str) -> Self { Observed { state: State::NotRead, not_read_because: Some(because) } }
}

/// The requests that load a conversation's configuration in Codex.
pub(super) fn loads_conversation(method: &str) -> bool {
    matches!(method, "thread/start" | "thread/resume" | "thread/fork")
}

fn entry_in_shape(entry: &Value) -> bool {
    entry.is_object()
        && entry["name"].is_string()
        && entry["enabled"].is_boolean()
        && entry["defaultEnabled"].is_boolean()
        && entry["stage"].as_str().is_some_and(|s| STAGES.contains(&s))
}

/// One feature's state from the entries of every page: exactly one well-formed entry under its
/// name. An entry without a readable name could be either feature, so it leaves both not read.
pub(super) fn evaluate(entries: &[Value], feature: Feature) -> Observed {
    if entries.iter().any(|e| !e["name"].is_string()) { return Observed::not_read("unnamed-entry"); }
    let named: Vec<&Value> = entries.iter().filter(|e| e["name"] == feature.name()).collect();
    if !named.iter().all(|e| entry_in_shape(e)) { return Observed::not_read("malformed-entry"); }
    match named.as_slice() {
        [one] => Observed { state: if one["enabled"] == true { State::On } else { State::Off }, not_read_because: None },
        [] => Observed::not_read("missing"),
        _ => Observed::not_read("duplicate"),
    }
}

/// The pins a requirements reply names for these features (`{}` when it names none), or None when
/// the reply gives no usable answer. A reply carrying an error, with or without a result, is no
/// answer. Whether the reply settled correctly and has the native shape is the caller's
/// (`requirements_evidence`).
pub(super) fn requirement_pins(reply: &Value) -> Option<Value> {
    if reply.get("error").is_some() { return None; }
    let result = reply.get("result").filter(|r| r.is_object())?;
    let features = match result.get("requirements")? {
        Value::Null => return Some(json!({})),
        Value::Object(requirements) => match requirements.get("featureRequirements") {
            None | Some(Value::Null) => return Some(json!({})),
            Some(Value::Object(features)) => features,
            Some(_) => return None,
        },
        _ => return None,
    };
    let mut pins = serde_json::Map::new();
    for name in ["plugins", "apps", "connectors"] {
        match features.get(name) {
            None => {}
            Some(Value::Bool(value)) => { pins.insert(name.into(), json!(value)); }
            Some(_) => return None,
        }
    }
    Some(Value::Object(pins))
}

fn layer_source(origin: &Value) -> Source {
    match origin["name"]["type"].as_str() {
        Some("user") => Source::ThisHome,
        Some("project") => Source::Project,
        Some("mdm" | "system" | "enterpriseManaged" | "legacyManagedConfigTomlFromFile" | "legacyManagedConfigTomlFromMdm") => Source::OutsideApp,
        // Codex's packaged defaults are its own default.
        Some("packagedDefaults") => Source::Default,
        // The App's own `-c` settings (none for these features), or a layer this version does not
        // name: not established.
        _ => Source::NotEstablished,
    }
}

/// Where a feature's state comes from. `origins`: the origins object of the reading that admitted
/// the conversation, for the thread's own folder, when there is one. `pins`: the pins of the
/// generation's latest successful requirements reading, when there is one (`{}`: read, nothing
/// pinned).
pub(super) fn source(feature: Feature, origins: Option<&Value>, pins: Option<&Value>) -> Source {
    if pins.is_some_and(|p| feature.requirement_names().iter().any(|n| p.get(*n).is_some())) { return Source::OutsideApp; }
    let Some(origins) = origins.filter(|o| o.is_object()) else { return Source::NotEstablished; };
    let from_layer = match feature.origin_keys().iter().find_map(|key| origins.get(*key)) {
        Some(origin) => layer_source(origin),
        None => Source::Default,
    };
    // A managed layer's origin is evidence on its own. Any other source holds only once the
    // requirements were read and pin nothing for this feature: without that reading, a requirement
    // could be what decides the value, so the source is not established.
    match from_layer {
        Source::OutsideApp => Source::OutsideApp,
        _ if pins.is_none() => Source::NotEstablished,
        other => other,
    }
}

/// The private configuration reading that admitted a conversation request: the folder it was
/// made for, and its origins when it was made on the request's generation.
#[derive(Clone, Debug, Default, PartialEq)]
pub(crate) struct Admitted { pub(crate) cwd: Option<String>, pub(crate) origins: Option<Value> }
impl Admitted {
    pub(super) fn of(proof: &ProviderAdmission, generation: &Value) -> Self {
        Admitted { cwd: proof.reading_cwd().map(str::to_owned), origins: proof.reading_origins(generation) }
    }
    /// The origins, only when the reading was made for `cwd`, the folder Codex reports for the
    /// thread; and how they were taken.
    fn origins_for(admitted: Option<&Admitted>, cwd: Option<&str>) -> (Option<Value>, &'static str) {
        match admitted {
            None => (None, "none"),
            Some(a) if a.cwd.is_some() && a.cwd.as_deref() == cwd => match &a.origins {
                Some(origins) => (Some(origins.clone()), "admitting-reading-same-folder"),
                None => (None, "none"),
            },
            Some(_) => (None, "admitting-reading-other-folder"),
        }
    }
}

/// One reading shown: for a conversation (`threads[].extensions`) or the home's base
/// (`extensionsBase`). `seq` is the reading's number: only the latest one begun completes.
#[derive(Clone, Debug)]
pub(crate) struct Record { seq: u64, shown: Value }

/// What one reading is for.
#[derive(Clone, Debug)]
pub(crate) struct Target {
    generation: Value,
    seq: u64,
    /// The conversation's thread; None for the home's base reading.
    thread_id: Option<String>,
    /// The conversation request whose reply named the thread.
    request: Option<String>,
    /// The folder Codex reported for the thread in that reply.
    cwd: Option<String>,
    admitted: Option<Admitted>,
    wait: Duration,
}

fn feature_record(observed: &Observed, source: Source, read_at: Option<&str>, requirements_read_at: Option<&str>) -> Value {
    json!({"state": observed.state.key(), "source": source.key(), "readAt": read_at, "notReadBecause": observed.not_read_because, "requirementsReadAt": requirements_read_at})
}

fn shown(target: &Target, plugins: Value, apps: Value, evidence: Value) -> Value {
    let mut shown = json!({"generation": target.generation, "request": target.request, "plugins": plugins, "apps": apps, "evidence": evidence});
    match &target.thread_id {
        Some(thread) => shown["threadId"] = json!(thread),
        None => shown["scope"] = json!(BASE_SCOPE),
    }
    shown
}

/// A reading begun and not yet finished: not read, because it is being read.
fn in_progress(target: &Target) -> Value {
    let reading = Observed::not_read("reading");
    let feature = feature_record(&reading, Source::NotEstablished, None, None);
    shown(target, feature.clone(), feature, json!({"origins": "none", "requirements": "none"}))
}

impl Host {
    /// When a reply to a request of the current generation is taken in, under the Host's state
    /// lock: keeps when a requirements reply arrived, and, for a reply that names a conversation's
    /// thread, begins that conversation's reading (shown as being read) and returns what it is
    /// for. Nothing is returned for the dedicated local home, a reply that did not settle
    /// correctly, an error reply or one that names no thread.
    pub(super) fn extensions_on_reply(i: &mut Inner, key: &str, generation: &Value, raw: &Value, settled: bool) -> Option<Target> {
        let method = i.source_requests.get(key).filter(|e| e.request.generation == *generation)?.request.frame["method"].as_str()?.to_owned();
        if method == "configRequirements/read" { i.requirements_read_at.insert(key.to_owned(), now_rfc3339()); return None; }
        if !loads_conversation(&method) { return None; }
        let admitted = i.extensions_admitted.remove(key);
        #[cfg(test)]
        if !i.feature_readings_for_test { return None; }
        // The dedicated local home reaches only the local model server and has no ChatGPT account.
        if i.local_provider.is_some() || i.generation != *generation || i.state != "ready" || i.server_requests.is_closed(generation) { return None; }
        if !settled || raw.get("error").is_some() { return None; }
        let thread = raw["result"]["thread"]["id"].as_str().filter(|t| !t.is_empty())?.to_owned();
        i.feature_read_seq += 1;
        let target = Target {
            generation: generation.clone(), seq: i.feature_read_seq, thread_id: Some(thread.clone()), request: Some(method),
            cwd: raw["result"]["cwd"].as_str().map(str::to_owned), admitted, wait: Self::feature_read_wait(i),
        };
        i.extensions_threads.insert(thread, Record { seq: target.seq, shown: in_progress(&target) });
        Some(target)
    }

    /// Once the home's Codex on `generation` is ready: its base reading, off the caller's path.
    pub(super) fn extensions_after_ready(&self, generation: &Value) {
        let target = {
            let mut i = self.inner.0.lock().unwrap();
            #[cfg(test)]
            if !i.feature_readings_for_test { return; }
            if i.local_provider.is_some() || i.generation != *generation || i.state != "ready" || i.server_requests.is_closed(generation) { return; }
            i.feature_read_seq += 1;
            let target = Target { generation: generation.clone(), seq: i.feature_read_seq, thread_id: None, request: None, cwd: None, admitted: None, wait: Self::feature_read_wait(&i) };
            i.extensions_base = Some(Record { seq: target.seq, shown: in_progress(&target) });
            target
        };
        self.extensions_spawn(target);
    }

    fn feature_read_wait(i: &Inner) -> Duration { i.feature_read_wait.unwrap_or(DEFAULT_WAIT).min(READ_BOUND) }

    /// Runs the reading on a worker of its own, with the Host's own handle (`this`). Called with
    /// no lock held. A worker that cannot be started leaves the reading not sent.
    pub(super) fn extensions_spawn(&self, target: Target) {
        let host = self.this.lock().unwrap().upgrade();
        let keep = target.clone();
        let spawned = host.and_then(|host| std::thread::Builder::new().name("feature-reading".into()).spawn(move || host.extensions_keep(keep)).ok());
        if spawned.is_none() { self.extensions_complete(&target, Err("not-sent"), &now_rfc3339()); }
    }

    /// The reading's keeper: the pages are read on a second worker, and the keeper records the
    /// outcome by the one deadline, even when a write of the reading is still blocked on Codex's
    /// input. What that worker finds afterwards changes nothing.
    fn extensions_keep(self: Arc<Self>, target: Target) {
        let deadline = std::time::Instant::now() + target.wait;
        let (tx, rx) = channel();
        let (reader, generation, thread) = (Arc::clone(&self), target.generation.clone(), target.thread_id.clone());
        let spawned = std::thread::Builder::new().name("feature-reading-pages".into()).spawn(move || {
            let outcome = reader.feature_list_read(&generation, thread.as_deref(), deadline);
            let _ = tx.send((outcome, now_rfc3339()));
        });
        let (outcome, read_at) = match spawned {
            Err(_) => (Err("not-sent"), now_rfc3339()),
            Ok(_) => rx.recv_timeout(deadline.saturating_duration_since(std::time::Instant::now()) + REPORT_GRACE)
                .unwrap_or_else(|_| (Err("not-answered"), now_rfc3339())),
        };
        self.extensions_complete(&target, outcome, &read_at);
    }

    /// Records a reading's outcome, only while its generation is current and ready and it is still
    /// the latest reading begun for its conversation or for the base.
    fn extensions_complete(&self, target: &Target, outcome: Result<Vec<Value>, &'static str>, read_at: &str) {
        let mut i = self.inner.0.lock().unwrap();
        if i.generation != target.generation || i.state != "ready" || i.server_requests.is_closed(&target.generation) { return; }
        let latest = match &target.thread_id { Some(thread) => i.extensions_threads.get(thread), None => i.extensions_base.as_ref() };
        if latest.map(|r| r.seq) != Some(target.seq) { return; }
        let (plugins, apps) = match outcome {
            Ok(entries) => (evaluate(&entries, Feature::Plugins), evaluate(&entries, Feature::Apps)),
            Err(because) => (Observed::not_read(because), Observed::not_read(because)),
        };
        let requirements = Self::requirements_evidence(&i, &target.generation);
        let (pins, requirements_at) = match &requirements { Some((pins, at)) => (Some(pins), at.as_deref()), None => (None, None) };
        let (origins, origins_evidence) = Admitted::origins_for(target.admitted.as_ref(), target.cwd.as_deref());
        let record = |observed: &Observed, feature: Feature| feature_record(observed, source(feature, origins.as_ref(), pins), Some(read_at), requirements_at);
        let evidence = json!({"origins": origins_evidence, "requirements": if requirements.is_some() { "read" } else { "none" }});
        let record = Record { seq: target.seq, shown: shown(target, record(&plugins, Feature::Plugins), record(&apps, Feature::Apps), evidence) };
        match &target.thread_id {
            Some(thread) => { i.extensions_threads.insert(thread.clone(), record); }
            None => i.extensions_base = Some(record),
        }
    }

    /// The pins of the latest answered `configRequirements/read` of `generation`, and when it was
    /// received: only from a reply that settled correctly, correlated with its request, as a result
    /// with no error and in the native shape. Otherwise there is no pin evidence.
    pub(super) fn requirements_evidence(i: &Inner, generation: &Value) -> Option<(Value, Option<String>)> {
        let (key, e) = i.source_requests.iter()
            .filter(|(_, e)| e.request.generation == *generation && e.request.frame["method"] == "configRequirements/read" && e.response_position.is_some())
            .max_by_key(|(_, e)| e.response_position)?;
        let reply = e.response.as_ref()?;
        let successful = e.write_error.is_none() && e.source_limit.is_none()
            && matches!(e.native_settlement, Some(Ok(())))
            && e.auth_response_shape == Some(true)
            && reply.get("error").is_none() && reply.get("result").is_some()
            && reply.get("id") == Some(e.request.request_id());
        if !successful { return None; }
        Some((requirement_pins(reply)?, i.requirements_read_at.get(key).cloned()))
    }

    /// Generation closed: every reading of it is dropped, with what was kept for them.
    pub(super) fn extensions_close(i: &mut Inner) {
        i.extensions_threads.clear();
        i.extensions_base = None;
        i.extensions_admitted.clear();
        i.requirements_read_at.clear();
    }

    /// Drops every reading not of the current, open generation, with what was kept for them: the
    /// admissions and requirements times of requests not of that generation.
    pub(super) fn extensions_retire_stale(i: &mut Inner) {
        if i.server_requests.is_closed(&i.generation) { Self::extensions_close(i); return; }
        let current = i.generation.clone();
        i.extensions_threads.retain(|_, r| r.shown["generation"] == current);
        if i.extensions_base.as_ref().is_some_and(|r| r.shown["generation"] != current) { i.extensions_base = None; }
        let Inner { source_requests, extensions_admitted, requirements_read_at, .. } = i;
        let of_current = |key: &String| source_requests.get(key).is_some_and(|e| e.request.generation == current);
        extensions_admitted.retain(|key, _| of_current(key));
        requirements_read_at.retain(|key, _| of_current(key));
    }

    /// Each conversation's reading on its row (`threads[].extensions`), and the home's base reading
    /// as `extensionsBase`.
    pub(super) fn extensions_status(i: &mut Inner, status: &mut Value) {
        Self::extensions_retire_stale(i);
        if let Some(rows) = status["threads"].as_array_mut() {
            for row in rows.iter_mut().filter(|row| row["generation"] == i.generation) {
                if let Some(record) = row["threadId"].as_str().and_then(|thread| i.extensions_threads.get(thread)) { row["extensions"] = record.shown.clone(); }
            }
        }
        status["extensionsBase"] = i.extensions_base.as_ref().map(|r| r.shown.clone()).unwrap_or(Value::Null);
    }

    /// Every entry of every page, following `nextCursor` up to `FEATURE_PAGE_LIMIT` pages, all
    /// within the one `deadline`, or why there is no reading. Each page names the thread, when there
    /// is one. What remains of the deadline is computed again after every wait: for the frame
    /// writer, the write, and each reply. A reply received after the deadline is not taken.
    pub(super) fn feature_list_read(&self, generation: &Value, thread: Option<&str>, deadline: std::time::Instant) -> Result<Vec<Value>, &'static str> {
        let mut entries = Vec::new();
        let mut cursor: Option<String> = None;
        for _ in 0..FEATURE_PAGE_LIMIT {
            let mut params = json!({});
            if let Some(thread) = thread { params["threadId"] = json!(thread); }
            if let Some(cursor) = &cursor { params["cursor"] = json!(cursor); }
            if std::time::Instant::now() >= deadline { return Err(if entries.is_empty() && cursor.is_none() { "not-sent" } else { "not-answered" }); }
            // The frame writer too is waited for only within the deadline, and only while no other
            // request waits for it (`feature_writer_within`): a reading not written in time is not sent.
            let bound = WriteBound { deadline, phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
            let request = self.request_begin_with_access_offer_guarded(FEATURE_LIST, params, json!({"kind":"app-rule","name":"feature-state-read"}), false, Some(generation), false, None, None, None, None, false, None, None, None, None, Some(&bound))
                .map_err(|_| "not-sent")?;
            let reply = self.feature_reply(&request, deadline).map_err(|e| if e.starts_with("refused-not-sent") { "not-sent" } else { "not-answered" })?;
            if std::time::Instant::now() > deadline { return Err("not-answered"); }
            if reply.get("error").is_some() { return Err("error-reply"); }
            let result = reply.get("result").filter(|r| r.is_object()).ok_or("malformed-reply")?;
            let data = result.get("data").and_then(Value::as_array).ok_or("malformed-reply")?;
            entries.extend(data.iter().cloned());
            match result.get("nextCursor") {
                None | Some(Value::Null) => return Ok(entries),
                Some(Value::String(next)) => cursor = Some(next.clone()),
                Some(_) => return Err("malformed-reply"),
            }
        }
        Err("page-limit")
    }

    /// Codex's reply to one page, within what remains of `deadline` now, after the writer wait and
    /// the write.
    fn feature_reply(&self, request: &SourceRequest, deadline: std::time::Instant) -> Result<Value, String> {
        #[cfg(test)]
        if let Some(hook) = self.feature_read_reply.lock().unwrap().as_ref() { hook(self, request); }
        self.wait_source_response(request, deadline.saturating_duration_since(std::time::Instant::now()))
    }

    /// The frame writer for a page of the reading: only when it is free and no other request is
    /// waiting for it or being prepared (`FrameWriter`), and only until the deadline.
    pub(super) fn feature_writer_within(&self, limit: &WriteBound, generation: &Value) -> Result<std::sync::MutexGuard<'_, ()>, String> {
        loop {
            match self.frame_write.try_lock_unqueued() {
                Ok(Some(guard)) => return Ok(guard),
                Err(()) => return Err("the frame writer is unavailable; nothing was written".into()),
                Ok(None) => {}
            }
            if std::time::Instant::now() >= limit.deadline { return Err(NOT_WRITTEN_IN_LIMIT.into()); }
            let ended = { let i = self.inner.0.lock().unwrap(); i.generation != *generation || i.server_requests.is_closed(generation) || i.state != "ready" };
            if ended { return Err(PROCESS_ENDING.into()); }
            std::thread::sleep(Duration::from_millis(1));
        }
    }

    /// Turns on the readings for a test Host held in an `Arc`: off in every other test, so that the
    /// tests of other parts see only their own frames.
    #[cfg(test)]
    pub(crate) fn feature_readings_for_test(self: &Arc<Self>) {
        *self.this.lock().unwrap() = Arc::downgrade(self);
        self.inner.0.lock().unwrap().feature_readings_for_test = true;
    }
}

#[cfg(test)]
impl Host {
    /// The reading kept for a conversation's thread, whether or not it has a row yet.
    pub(crate) fn extensions_record_for_test(&self, thread: &str) -> Option<Value> {
        self.inner.0.lock().unwrap().extensions_threads.get(thread).map(|r| r.shown.clone())
    }
    /// Whether anything is kept for a reading: conversations, base, admissions or requirements times.
    pub(crate) fn extensions_kept_for_test(&self) -> bool {
        let i = self.inner.0.lock().unwrap();
        !i.extensions_threads.is_empty() || i.extensions_base.is_some() || !i.extensions_admitted.is_empty() || !i.requirements_read_at.is_empty()
    }
}

/// `Admitted::origins_for`, for the tests.
#[cfg(test)]
pub(crate) fn extensions_origins_for_test(admitted: Option<&Admitted>, cwd: Option<&str>) -> (Option<Value>, &'static str) {
    Admitted::origins_for(admitted, cwd)
}

/// Why a page of the reading was not written. A frame longer than one atomic write is not attempted;
/// one that Codex's input could not take at once was not written, no byte of it.
pub(crate) const FRAME_TOO_LONG: &str = "the reading's frame is longer than one atomic write to Codex's input; nothing was written";
pub(crate) const INPUT_FULL: &str = "Codex's input could not take the reading's frame without waiting; nothing was written";
pub(crate) const NOT_ATTEMPTED: &str = "Codex's input could not be set not to wait; no write was made";
/// A write of the reading that is neither written nor not sent.
pub(crate) const INTERRUPTED: &str = "the reading's write was interrupted";
pub(crate) const SHORT_WRITE: &str = "only part of the reading's frame reached Codex's input";
pub(crate) const FLAGS_NOT_RESTORED: &str = "Codex's input could not be put back as it was after the reading's write";
/// The words of the stop that follows a reading's write that changed Codex's input.
pub(crate) const STOP_REASON: &str = "The App could not be sure that Codex's input was left as it was after it read the state of plugins and apps, so it stopped Codex. Start Codex again to continue.";

/// Whether the reading's write left nothing on Codex's input: its request was not sent.
pub(crate) fn nothing_attempted(error: &str) -> bool { matches!(error, INPUT_FULL | NOT_ATTEMPTED | FRAME_TOO_LONG) }
/// Whether the reading's write changed Codex's input for the frames after it: part of a frame on
/// it, or its flags not put back. Codex is then stopped.
pub(crate) fn input_changed(error: &str) -> bool { error.starts_with(SHORT_WRITE) || error.starts_with(FLAGS_NOT_RESTORED) }

/// What the one write call of a page did.
#[derive(Debug, PartialEq)]
pub(crate) enum NoWait { Written, WouldBlock, Interrupted, Short(usize), Failed(String) }

/// The one write call's return, `n` with `errno` when it is negative, for a frame of `len` bytes.
/// Only the whole frame is written; only `EAGAIN` with nothing written is would-block.
pub(crate) fn no_wait_outcome(n: isize, errno: i32, len: usize) -> NoWait {
    if n < 0 {
        return match errno {
            libc::EAGAIN => NoWait::WouldBlock,
            libc::EINTR => NoWait::Interrupted,
            errno => NoWait::Failed(std::io::Error::from_raw_os_error(errno).to_string()),
        };
    }
    if n as usize == len { NoWait::Written } else { NoWait::Short(n as usize) }
}

/// Writes one page's frame (`bytes`, its newline included) to Codex's input in one write call that
/// does not wait. Called with the frame writer held, so no other frame is written while the
/// descriptor does not wait: every write to Codex's input is made with that writer held. A frame
/// longer than `PIPE_BUF` is not attempted. On macOS a write of at most `PIPE_BUF` bytes to a pipe
/// that does not wait is made whole, or returns `EAGAIN` with nothing written (XNU `pipe_write`).
/// The descriptor's flags are put back as they were before this returns; nothing between setting
/// and putting them back can unwind. `Ok` only when the whole frame was written.
pub(crate) fn write_without_waiting(file: &std::fs::File, bytes: &[u8], restore_fails: bool) -> Result<(), String> {
    use std::os::fd::AsRawFd;
    if bytes.len() > libc::PIPE_BUF { return Err(FRAME_TOO_LONG.into()); }
    let fd = file.as_raw_fd();
    let flags = unsafe { libc::fcntl(fd, libc::F_GETFL) };
    if flags < 0 || unsafe { libc::fcntl(fd, libc::F_SETFL, flags | libc::O_NONBLOCK) } != 0 { return Err(NOT_ATTEMPTED.into()); }
    let n = unsafe { libc::write(fd, bytes.as_ptr().cast(), bytes.len()) };
    let errno = if n < 0 { std::io::Error::last_os_error().raw_os_error().unwrap_or(0) } else { 0 };
    // Put back, then read back: the descriptor waits again exactly when it did before. (The kernel
    // also reports bits of its own, such as that the descriptor was written, so only this bit is
    // compared.)
    let restored = !restore_fails && unsafe { libc::fcntl(fd, libc::F_SETFL, flags) } == 0
        && unsafe { libc::fcntl(fd, libc::F_GETFL) } & libc::O_NONBLOCK == flags & libc::O_NONBLOCK;
    let outcome = no_wait_outcome(n, errno, bytes.len());
    if !restored { return Err(format!("{FLAGS_NOT_RESTORED} (write: {outcome:?})")); }
    match outcome {
        NoWait::Written => Ok(()),
        NoWait::WouldBlock => Err(INPUT_FULL.into()),
        NoWait::Interrupted => Err(INTERRUPTED.into()),
        NoWait::Short(written) => Err(format!("{SHORT_WRITE}: {written} of {} bytes", bytes.len())),
        NoWait::Failed(error) => Err(error),
    }
}
