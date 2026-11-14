//! The state of plugins, and of apps connected to the person's ChatGPT account, in this home's
//! Codex: read for display before every conversation start, resume and fork, and returned in the
//! Host status as `extensions`. The reading never refuses a request and never delays one past its
//! own bound; a failure of it is recorded and shown.
//!
//! The state is what Codex itself reports after every layer and requirement
//! (`experimentalFeature/list`, whose `enabled` is the effective value). Each start, resume and fork
//! loads its configuration again in Codex, so a reading made just before it covers an account
//! change and a refetch of requirements. A reading is bound to the generation it was made on: one
//! whose generation is replaced before its request is registered is shown as not read.
//!
//! Where each state comes from is taken only from evidence already read on the same generation,
//! never by a further configuration reading (a configuration reading becomes the generation's
//! newest and would retire the provider reading the request itself is admitted on, `reading_gate`):
//! - the origins in the private `config/read` (layers included) that admitted this very request
//!   (`ProviderAdmission`), when it carries one;
//! - the pins under `featureRequirements` in the latest answered `configRequirements/read` of the
//!   generation.
//!
//! Without that evidence the source is not established.
use super::*;

/// The most pages one reading follows. Codex at the pin lists every feature on one page; a longer
/// sequence is not followed and gives no reading.
pub(crate) const FEATURE_PAGE_LIMIT: usize = 8;
/// The wait for a reading when the Host was not started with one (`HostConfig::wait_limit`).
const DEFAULT_WAIT: Duration = Duration::from_secs(20);
/// The App's own bound on one reading, all its pages together, whatever the Host's wait: a reading
/// that only informs the display holds a conversation request back no longer than this.
const READ_BOUND: Duration = Duration::from_secs(5);
const STAGES: [&str; 5] = ["beta", "underDevelopment", "stable", "deprecated", "removed"];

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
    /// Its key's origin is the user layer: this home's own `config.toml`.
    ThisHome,
    /// Its key's origin is a project layer.
    Project,
    /// No origin for its key and no pin, both read: Codex's own default.
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
/// the reply gives no usable answer.
pub(super) fn requirement_pins(reply: &Value) -> Option<Value> {
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
        // The App's own `-c` settings (none for these features), Codex's packaged defaults, or a
        // layer this version does not name: not established.
        _ => Source::NotEstablished,
    }
}

/// Where a feature's state comes from. `origins`: the origins object of the reading that admitted
/// the request, when there is one. `pins`: the pins of the generation's latest answered
/// requirements reading, when there is one (`{}`: read, nothing pinned).
pub(super) fn source(feature: Feature, origins: Option<&Value>, pins: Option<&Value>) -> Source {
    if pins.is_some_and(|p| feature.requirement_names().iter().any(|n| p.get(*n).is_some())) { return Source::OutsideApp; }
    let Some(origins) = origins.filter(|o| o.is_object()) else { return Source::NotEstablished; };
    match feature.origin_keys().iter().find_map(|key| origins.get(*key)) {
        Some(origin) => layer_source(origin),
        None if pins.is_some() => Source::Default,
        None => Source::NotEstablished,
    }
}

fn feature_record(observed: &Observed, source: Source, read_at: &str) -> Value {
    json!({"state": observed.state.key(), "source": source.key(), "readAt": read_at, "notReadBecause": observed.not_read_because})
}

impl Host {
    /// Reads plugins and apps on `method`'s generation and records the result as the Host status's
    /// `extensions`. Never refuses: every failure is recorded as not read. Holds no lock across the
    /// reading's requests. Returns the generation read on, which registration compares
    /// (`extensions_registered`); None when nothing was read (the local home, or a generation that
    /// is not current and ready, whose request registration refuses as before).
    pub(super) fn extensions_read(&self, method: &str, expected_generation: Option<&Value>, admission: Option<&ProviderAdmission>) -> Option<Value> {
        let (generation, wait, local, current) = {
            let i = self.inner.0.lock().unwrap();
            let generation = expected_generation.cloned().unwrap_or_else(|| i.generation.clone());
            let current = i.generation == generation && i.state == "ready" && !i.server_requests.is_closed(&generation);
            (generation, i.feature_read_wait.unwrap_or(DEFAULT_WAIT).min(READ_BOUND), i.local_provider.is_some(), current)
        };
        // The dedicated local home reaches only the local model server and has no ChatGPT account.
        if local || !current { return None; }
        let read_at = crate::util::now_rfc3339();
        let (plugins, apps) = match self.feature_list_read(&generation, wait) {
            Ok(entries) => (evaluate(&entries, Feature::Plugins), evaluate(&entries, Feature::Apps)),
            Err(because) => (Observed::not_read(because), Observed::not_read(because)),
        };
        let origins = admission.and_then(|p| p.reading_origins(&generation));
        let mut i = self.inner.0.lock().unwrap();
        let pins = Self::latest_requirement_pins(&i, &generation);
        i.extensions = Some(json!({
            "generation": generation,
            "request": method,
            "readAt": read_at,
            "plugins": feature_record(&plugins, source(Feature::Plugins, origins.as_ref(), pins.as_ref()), &read_at),
            "apps": feature_record(&apps, source(Feature::Apps, origins.as_ref(), pins.as_ref()), &read_at),
            "evidence": {
                "origins": if origins.is_some() { "admitting-reading" } else { "none" },
                "requirements": if pins.is_some() { "latest-reading" } else { "none" },
            },
        }));
        Some(generation)
    }

    /// At registration, under the host's state lock: a reading made on another generation than the
    /// one the request is registered on is shown as not read.
    pub(super) fn extensions_registered(i: &mut Inner, read_on: Option<&Value>) {
        let Some(read_on) = read_on else { return };
        if *read_on == i.generation { return; }
        if let Some(record) = i.extensions.as_mut().filter(|r| &r["generation"] == read_on) {
            for feature in ["plugins", "apps"] {
                record[feature]["state"] = json!(State::NotRead.key());
                record[feature]["notReadBecause"] = json!("generation-changed");
            }
        }
    }

    /// The pins of the latest answered `configRequirements/read` of `generation`, if any.
    fn latest_requirement_pins(i: &Inner, generation: &Value) -> Option<Value> {
        i.source_requests.values()
            .filter(|e| e.request.generation == *generation && e.request.frame["method"] == "configRequirements/read")
            .filter_map(|e| Some((e.response_position?, e.response.as_ref()?)))
            .max_by_key(|(position, _)| *position)
            .and_then(|(_, reply)| requirement_pins(reply))
    }

    /// Every entry of every page, following `nextCursor` up to `FEATURE_PAGE_LIMIT` pages within
    /// one wait, or why there is no reading.
    fn feature_list_read(&self, generation: &Value, wait: Duration) -> Result<Vec<Value>, &'static str> {
        let deadline = std::time::Instant::now() + wait;
        let mut entries = Vec::new();
        let mut cursor: Option<String> = None;
        for _ in 0..FEATURE_PAGE_LIMIT {
            let params = match &cursor { None => json!({}), Some(c) => json!({"cursor": c}) };
            let remaining = deadline.saturating_duration_since(std::time::Instant::now());
            if remaining.is_zero() { return Err("not-answered"); }
            // The frame writer too is waited for only within this reading's bound: a reading that
            // cannot be written in time is not sent, and holds nothing back.
            let bound = WriteBound { deadline, phase: Arc::new(Mutex::new(SendPhase::Pending)), gave_up: Mutex::new(None) };
            let request = self.request_begin_with_access_offer_guarded("experimentalFeature/list", params, json!({"kind":"app-rule","name":"feature-state-read"}), false, Some(generation), false, None, None, None, None, false, None, None, None, None, Some(&bound))
                .map_err(|_| "not-sent")?;
            // A request withdrawn before its write (the writer not taken within the bound) was not sent.
            let reply = self.feature_reply(&request, remaining).map_err(|e| if e.starts_with("refused-not-sent") { "not-sent" } else { "not-answered" })?;
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

    /// Codex's reply to one page, within `wait`.
    fn feature_reply(&self, request: &SourceRequest, wait: Duration) -> Result<Value, String> {
        #[cfg(test)]
        if let Some(hook) = self.feature_read_reply.lock().unwrap().as_ref() { hook(self, request); }
        self.wait_source_response(request, wait)
    }

    /// A stand-in's reply to the reading: plugins and apps off.
    #[cfg(test)]
    pub(crate) fn answer_features_off_for_test(&self) {
        *self.feature_read_reply.lock().unwrap() = Some(Box::new(|host, source| {
            host.on_line(&serde_json::to_vec(&json!({"id": source.request_id(), "result": features_off_page()})).unwrap(), source.generation());
        }));
    }
}

/// One page as Codex at the pin answers `experimentalFeature/list` with both features off.
#[cfg(test)]
pub(crate) fn features_off_page() -> Value {
    json!({"data": [
        {"name": "plugins", "enabled": false, "defaultEnabled": true, "stage": "stable"},
        {"name": "apps", "enabled": false, "defaultEnabled": true, "stage": "stable"},
    ], "nextCursor": null})
}
