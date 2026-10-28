//! Selected-home, generation-bound engine history. Queries are not dispatched
//! here; native payloads are transient receiving views, never durable transcripts.
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::OnceLock;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize)]
pub enum Direction {
    #[serde(rename = "asc")]
    Asc,
    #[serde(rename = "desc")]
    Desc,
}
impl Direction {
    fn native(self) -> &'static str {
        match self {
            Self::Asc => "asc",
            Self::Desc => "desc",
        }
    }
    fn opposite(self) -> Self {
        match self {
            Self::Asc => Self::Desc,
            Self::Desc => Self::Asc,
        }
    }
}
#[derive(Clone, Debug, PartialEq, Serialize)]
pub struct HistoryQuery {
    factory_id: u64,
    query_id: u64,
    home: String,
    generation: Value,
    method: String,
    params: Value,
}
impl HistoryQuery {
    pub fn id(&self) -> u64 {
        self.query_id
    }
    pub fn home(&self) -> &str {
        &self.home
    }
    pub fn generation(&self) -> &Value {
        &self.generation
    }
    pub fn method(&self) -> &str {
        &self.method
    }
    pub fn params(&self) -> &Value {
        &self.params
    }
}
#[derive(Clone, Debug)]
enum Kind {
    List(Direction),
    Metadata(String),
    Turns(String, Direction),
    Items(String, String, Direction),
    Goal(String),
    Child(String),
    Resume(String),
}
impl Kind {
    fn response_schema(&self) -> &'static str {
        match self {
            Self::List(_) => "ThreadListResponse",
            Self::Metadata(_) | Self::Child(_) => "ThreadReadResponse",
            Self::Turns(_, _) => "ThreadTurnsListResponse",
            Self::Items(_, _, _) => "ThreadItemsListResponse",
            Self::Goal(_) => "ThreadGoalGetResponse",
            Self::Resume(_) => "ThreadResumeResponse",
        }
    }
}
struct Pending {
    query: HistoryQuery,
    kind: Kind,
    selection_epoch: u64,
    stream: String,
    revision: u64,
    waiting_ended: bool,
    child_origin: Option<Value>,
}
// Correlation metadata only. The raw page remains in Selection.items_page.
struct AcceptedItems {
    query: HistoryQuery,
    selection_epoch: u64,
    revision: u64,
}

/// A borrowed latest read-only acceptance observation. Public `receive` alone
/// cannot establish supplier authenticity, operational admission or an act.
/// The owning Host must separately verify its private written/correlated source.
pub(crate) struct AcceptedItemsObservation<'a> {
    accepted: &'a AcceptedItems,
    page: &'a Value,
}
impl AcceptedItemsObservation<'_> {
    pub(crate) fn query(&self) -> &HistoryQuery {
        &self.accepted.query
    }
    pub(crate) fn owner_instance(&self) -> u64 {
        self.accepted.query.factory_id
    }
    pub(crate) fn selection_epoch(&self) -> u64 {
        self.accepted.selection_epoch
    }
    pub(crate) fn stream_revision(&self) -> u64 {
        self.accepted.revision
    }
    pub(crate) fn stream(&self) -> &str {
        "item-pages"
    }
    pub(crate) fn page(&self) -> &Value {
        self.page
    }
}

struct Selection {
    thread: String,
    metadata: Option<Value>,
    turns_page: Option<Value>,
    items_page: Option<Value>,
    accepted_items: Option<AcceptedItems>,
    goal: Option<Value>,
    turn_ids: HashSet<String>,
    turn_cursors: HashSet<(String, Direction)>,
    item_cursors: HashMap<String, HashSet<(String, Direction)>>,
    known_children: BTreeMap<String, Value>,
    receiver_references: BTreeMap<String, Value>,
    child_reads: BTreeMap<String, Value>,
    known_ancestors: HashSet<String>,
    started_paths: HashMap<String, String>,
    resume: Option<Value>,
    resume_revision: Option<u64>,
    errors: BTreeMap<String, Value>,
    error_history: Vec<Value>,
    resolutions: BTreeMap<String, Value>,
}
impl Selection {
    fn new(thread: String) -> Self {
        Self {
            thread,
            metadata: None,
            turns_page: None,
            items_page: None,
            accepted_items: None,
            goal: None,
            turn_ids: HashSet::new(),
            turn_cursors: HashSet::new(),
            item_cursors: HashMap::new(),
            known_children: BTreeMap::new(),
            receiver_references: BTreeMap::new(),
            child_reads: BTreeMap::new(),
            known_ancestors: HashSet::new(),
            started_paths: HashMap::new(),
            resume: None,
            resume_revision: None,
            errors: BTreeMap::new(),
            error_history: Vec::new(),
            resolutions: BTreeMap::new(),
        }
    }
}

fn parent_ids(native: &Value) -> Vec<&str> {
    [
        native["parentThreadId"].as_str(),
        native["source"]["subAgent"]["thread_spawn"]["parent_thread_id"].as_str(),
    ]
    .into_iter()
    .flatten()
    .filter(|id| !id.is_empty())
    .collect()
}
fn observed_threads<'a>(
    s: &'a Selection,
    threads: &'a BTreeMap<String, Value>,
    id: &str,
) -> Vec<&'a Value> {
    let mut observations = Vec::new();
    if id == s.thread {
        if let Some(metadata) = &s.metadata {
            observations.push(&metadata["thread"]);
        }
    }
    if let Some(read) = s.child_reads.get(id) {
        observations.push(&read["native"]["thread"]);
    }
    if let Some(native) = threads.get(id) {
        observations.push(native);
    }
    observations
}
// As in native_items: root/self and known ancestor references can be copied
// into a child's forked history. They never establish a new child edge.
fn started_reference_limit(
    s: &Selection,
    threads: &BTreeMap<String, Value>,
    id: &str,
    path: &str,
) -> Option<&'static str> {
    if id.is_empty() || id == s.thread || path == "/root" {
        return Some("root, self or empty native reference");
    }
    if s.known_ancestors.contains(id) {
        return Some("native reference names a previously observed ancestor");
    }
    for own in observed_threads(s, threads, &s.thread) {
        if let Some(own_path) = own["source"]["subAgent"]["thread_spawn"]["agent_path"].as_str() {
            if !path.is_empty() && (own_path == path || own_path.starts_with(&format!("{path}/"))) {
                return Some("native path names the selected agent or an ancestor");
            }
        }
    }
    if ancestor_ids(s, threads).contains(id) {
        return Some("native reference names a known ancestor");
    }
    None
}
fn ancestor_ids(s: &Selection, threads: &BTreeMap<String, Value>) -> HashSet<String> {
    let mut ancestors = s.known_ancestors.clone();
    let mut next = vec![s.thread.clone()];
    let mut seen = HashSet::new();
    while let Some(at) = next.pop() {
        if !seen.insert(at.clone()) {
            continue;
        }
        for native in observed_threads(s, threads, &at) {
            for parent in parent_ids(native) {
                ancestors.insert(parent.to_owned());
                if !seen.contains(parent) {
                    next.push(parent.to_owned());
                }
            }
        }
    }
    ancestors
}
fn refresh_ancestor_limits(s: &mut Selection, threads: &BTreeMap<String, Value>) {
    s.known_ancestors = ancestor_ids(s, threads);
    let limits: Vec<_> = s
        .known_children
        .iter()
        .filter(|(_, child)| child["discoveryKind"] == "subAgentActivity")
        .filter_map(|(id, child)| {
            started_reference_limit(
                s,
                threads,
                id,
                s.started_paths
                    .get(id)
                    .map(String::as_str)
                    .unwrap_or_else(|| child["agentPath"].as_str().unwrap_or("")),
            )
            .map(|reason| (id.clone(), reason))
        })
        .collect();
    for (id, reason) in limits {
        let child = s.known_children.get_mut(&id).unwrap();
        child["discoveryLimit"] = json!(reason);
        unconfirm_started(child, reason);
        if let Some(read) = s.child_reads.get_mut(&id) {
            read["parentRelationship"] = json!({"standing":"unknown","reason":reason});
        }
    }
}
fn child_origin(child: &Value) -> Value {
    json!({"sourceThreadId":child["sourceThreadId"],"sourceTurnId":child["sourceTurnId"],"sourceItemId":child["sourceItemId"],"sourceQuery":child["sourceQuery"],"sourceRevision":child["sourceRevision"],"agentPath":child["agentPath"],"discoveryKind":child["discoveryKind"]})
}
fn unconfirm_started(child: &mut Value, reason: &str) {
    child.as_object_mut().unwrap().remove("parentThreadId");
    child["parentSource"] = json!("not-confirmed");
    child["edgeEvidence"] = json!("native started reference; parent relationship unknown");
    child["parentLimit"] = json!(reason);
}
fn generation_valid(g: &Value) -> bool {
    g.as_object().map(|o| o.len() == 3).unwrap_or(false)
        && g["appSession"]
            .as_str()
            .map(|s| !s.is_empty())
            .unwrap_or(false)
        && g["home"].as_str().map(|s| !s.is_empty()).unwrap_or(false)
        && g["spawnCounter"].as_u64().unwrap_or(0) > 0
}
const TARGETS: &[&str] = &[
    "JSONRPCErrorError",
    "ThreadListParams",
    "ThreadListResponse",
    "ThreadReadParams",
    "ThreadReadResponse",
    "ThreadTurnsListParams",
    "ThreadTurnsListResponse",
    "ThreadItemsListParams",
    "ThreadItemsListResponse",
    "ThreadGoalGetParams",
    "ThreadGoalGetResponse",
    "ThreadResumeParams",
    "ThreadResumeResponse",
];
fn validators() -> Result<&'static HashMap<String, jsonschema::Validator>, String> {
    static VALIDATORS: OnceLock<Result<HashMap<String, jsonschema::Validator>, String>> =
        OnceLock::new();
    VALIDATORS
        .get_or_init(|| {
            let root: Value = serde_json::from_str(include_str!(
                "../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json"
            ))
            .map_err(|e| e.to_string())?;
            TARGETS
                .iter()
                .map(|target| {
                    let mut schema = root.clone();
                    schema["$ref"] = json!(if *target == "JSONRPCErrorError" {
                        format!("#/definitions/{target}")
                    } else {
                        format!("#/definitions/v2/{target}")
                    });
                    jsonschema::options()
                        .with_draft(jsonschema::Draft::Draft7)
                        .offline()
                        .build(&schema)
                        .map(|v| (target.to_string(), v))
                        .map_err(|e| e.to_string())
                })
                .collect()
        })
        .as_ref()
        .map_err(Clone::clone)
}
/// WR TT-9 and TT-10: a history read the workflow workspace makes for a trial
/// (a sub-agent's or a clean trial conversation's first turn, the pages of a
/// bring-back transcript or a comparison). Read methods only. The query is
/// owned by no `NativeHistory` (factory 0 is never issued to one), so its
/// page is neither added to the person's history view nor accepted as a
/// supply-check page; the caller reads the response itself and records only
/// what WR's trial records say.
pub(crate) fn workspace_read(home: &str, generation: &Value, method: &str, params: Value) -> Result<HistoryQuery, String> {
    let target = match method {
        "thread/read" => "ThreadReadParams",
        "thread/turns/list" => "ThreadTurnsListParams",
        "thread/items/list" => "ThreadItemsListParams",
        _ => return Err(format!("{method} is not a read the workflow workspace makes")),
    };
    if home.is_empty() || !generation_valid(generation) || generation["home"] != home {
        return Err("explicit home/full generation required".into());
    }
    validate(target, &params)?;
    static NEXT_READ: AtomicU64 = AtomicU64::new(1);
    let query_id = NEXT_READ
        .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |id| id.checked_add(1))
        .map_err(|_| "workspace read identity exhausted")?;
    Ok(HistoryQuery { factory_id: 0, query_id, home: home.into(), generation: generation.clone(), method: method.into(), params })
}
/// The reviewed native response shape of a workspace read's result (the
/// recovery reads, RECOVERY §5 R-4): a result Codex returns in another shape
/// is not read.
pub(crate) fn validate_read_response(method: &str, result: &Value) -> Result<(), String> {
    let target = match method {
        "thread/read" => "ThreadReadResponse",
        "thread/turns/list" => "ThreadTurnsListResponse",
        "thread/items/list" => "ThreadItemsListResponse",
        _ => return Err(format!("{method} is not a read the workflow workspace makes")),
    };
    validate(target, result)
}
fn validate(target: &str, value: &Value) -> Result<(), String> {
    validators()?
        .get(target)
        .ok_or("native schema unavailable")?
        .validate(value)
        // A validator's Display can quote the rejected conversation payload.
        // Trial fidelity and recovery readers may retain this diagnostic; keep
        // the contract name and refusal without copying native content there.
        .map_err(|_| format!("native history schema refused {target}: invalid response shape"))
}
fn cursor_view(page: Option<&Value>) -> Value {
    match page.and_then(|p| p.get("nextCursor")) {
        None => json!({"state":"not-reported"}),
        Some(Value::Null) => json!({"state":"exhausted"}),
        Some(v) => json!({"state":"available","value":v}),
    }
}
fn capture_cursors(set: &mut HashSet<(String, Direction)>, page: &Value, direction: Direction) {
    if let Some(cursor) = page["nextCursor"].as_str() {
        set.insert((cursor.into(), direction));
    }
    if let Some(cursor) = page["backwardsCursor"].as_str() {
        set.insert((cursor.into(), direction.opposite()));
    }
}
fn check_cursor(
    set: &HashSet<(String, Direction)>,
    cursor: Option<&str>,
    direction: Direction,
) -> Result<(), String> {
    if cursor
        .map(|c| !set.contains(&(c.into(), direction)))
        .unwrap_or(false)
    {
        return Err("cursor not received for this history stream/direction".into());
    }
    Ok(())
}
fn role_unknown() -> Value {
    json!({"standing":"unknown","reason":"original request-bound App role/source metadata not supplied; native agentRole, config, runtime record or fork relation does not establish it"})
}

pub struct NativeHistory {
    factory_id: u64,
    home: String,
    generation: Value,
    closed: bool,
    selection_epoch: u64,
    next_query: u64,
    pending: BTreeMap<u64, Pending>,
    streams: HashMap<String, u64>,
    threads: BTreeMap<String, Value>,
    list_page: Option<Value>,
    list_cursors: HashSet<(String, Direction)>,
    selection: Option<Selection>,
    list_error: Option<Value>,
}
impl NativeHistory {
    pub fn home(&self) -> &str {
        &self.home
    }
    pub fn generation(&self) -> &Value {
        &self.generation
    }
    pub fn selection_epoch(&self) -> u64 {
        self.selection_epoch
    }
    pub fn selected_thread(&self) -> Option<&str> {
        self.selection.as_ref().map(|s| s.thread.as_str())
    }
    pub fn new(home: &str, generation: Value) -> Result<Self, String> {
        if home.is_empty() || !generation_valid(&generation) || generation["home"] != home {
            return Err("explicit selected home/full generation required".into());
        }
        static NEXT_FACTORY: AtomicU64 = AtomicU64::new(1);
        let factory_id = NEXT_FACTORY
            .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |id| id.checked_add(1))
            .map_err(|_| "history factory identity exhausted")?;
        Ok(Self {
            factory_id,
            home: home.into(),
            generation,
            closed: false,
            selection_epoch: 0,
            next_query: 0,
            pending: BTreeMap::new(),
            streams: HashMap::new(),
            threads: BTreeMap::new(),
            list_page: None,
            list_cursors: HashSet::new(),
            selection: None,
            list_error: None,
        })
    }
    fn issue(
        &mut self,
        method: &str,
        target: &str,
        params: Value,
        kind: Kind,
    ) -> Result<HistoryQuery, String> {
        if self.closed {
            return Err("history generation closed".into());
        }
        validate(target, &params)?;
        self.next_query = self
            .next_query
            .checked_add(1)
            .ok_or("query identity exhausted")?;
        let query = HistoryQuery {
            factory_id: self.factory_id,
            query_id: self.next_query,
            home: self.home.clone(),
            generation: self.generation.clone(),
            method: method.into(),
            params,
        };
        let stream = match &kind {
            Kind::List(_) => "catalog".into(),
            Kind::Metadata(_) | Kind::Resume(_) => "thread-state".into(),
            Kind::Turns(_, _) => "turn-pages".into(),
            Kind::Items(_, _, _) => "item-pages".into(),
            Kind::Goal(_) => "goal".into(),
            Kind::Child(id) => format!("child:{id}"),
        };
        let revision = self
            .streams
            .get(&stream)
            .copied()
            .unwrap_or(0)
            .checked_add(1)
            .ok_or("history stream revision exhausted")?;
        self.streams.insert(stream.clone(), revision);
        if !matches!(kind, Kind::List(_)) {
            self.selection.as_mut().unwrap().resolutions.insert(
                stream.clone(),
                json!({"query":query,"revision":revision,"outcome":"pending"}),
            );
        }
        let child_origin = match &kind {
            Kind::Child(id) => self
                .selection
                .as_ref()
                .and_then(|s| s.known_children.get(id))
                .map(child_origin),
            _ => None,
        };
        self.pending.insert(
            query.id(),
            Pending {
                query: query.clone(),
                kind,
                selection_epoch: self.selection_epoch,
                stream,
                revision,
                waiting_ended: false,
                child_origin,
            },
        );
        Ok(query)
    }
    pub fn list_threads(
        &mut self,
        cursor: Option<&str>,
        direction: Direction,
    ) -> Result<HistoryQuery, String> {
        check_cursor(&self.list_cursors, cursor, direction)?;
        let mut params = json!({"sortDirection":direction.native()});
        if let Some(c) = cursor {
            params["cursor"] = json!(c);
        }
        self.issue(
            "thread/list",
            "ThreadListParams",
            params,
            Kind::List(direction),
        )
    }
    pub fn select(&mut self, thread: &str) -> Result<(), String> {
        if self.closed {
            return Err("history generation closed".into());
        }
        if !self.threads.contains_key(thread) {
            return Err("thread not received in selected home list".into());
        }
        self.selection_epoch = self
            .selection_epoch
            .checked_add(1)
            .ok_or("selection epoch exhausted")?;
        self.selection = Some(Selection::new(thread.into()));
        Ok(())
    }
    /// A separate read-only owner established by the Host's private matched
    /// Continue admission. This does not admit execution or fabricate a list
    /// response; the caller retains the actual admission receipt separately.
    pub(crate) fn for_admitted_thread(home: &str, generation: Value, thread: &str) -> Result<Self, String> {
        if thread.is_empty() { return Err("admitted conversation identity absent".into()); }
        let mut history = Self::new(home, generation)?;
        history.selection_epoch = 1;
        history.selection = Some(Selection::new(thread.into()));
        Ok(history)
    }
    fn selected(&self) -> Result<&Selection, String> {
        self.selection
            .as_ref()
            .ok_or("no selected history thread".into())
    }
    pub fn read_metadata(&mut self) -> Result<HistoryQuery, String> {
        let id = self.selected()?.thread.clone();
        self.issue(
            "thread/read",
            "ThreadReadParams",
            json!({"threadId":id,"includeTurns":false}),
            Kind::Metadata(id),
        )
    }
    pub fn turns_page(
        &mut self,
        cursor: Option<&str>,
        direction: Direction,
    ) -> Result<HistoryQuery, String> {
        self.turns_page_limit(cursor, direction, None)
    }
    pub(crate) fn turns_page_limit(&mut self, cursor: Option<&str>, direction: Direction, limit: Option<u32>) -> Result<HistoryQuery, String> {
        let s = self.selected()?;
        check_cursor(&s.turn_cursors, cursor, direction)?;
        let id = s.thread.clone();
        let mut params =
            json!({"threadId":id,"sortDirection":direction.native(),"itemsView":"summary"});
        if let Some(limit) = limit { params["limit"] = json!(limit); }
        if let Some(c) = cursor {
            params["cursor"] = json!(c);
        }
        self.issue(
            "thread/turns/list",
            "ThreadTurnsListParams",
            params,
            Kind::Turns(id, direction),
        )
    }
    pub fn items_page(
        &mut self,
        turn: &str,
        cursor: Option<&str>,
        direction: Direction,
    ) -> Result<HistoryQuery, String> {
        self.items_page_limit(turn, cursor, direction, None)
    }
    pub(crate) fn items_page_limit(&mut self, turn: &str, cursor: Option<&str>, direction: Direction, limit: Option<u32>) -> Result<HistoryQuery, String> {
        let s = self.selected()?;
        if !s.turn_ids.contains(turn) {
            return Err("turn not received in this selected history".into());
        }
        if let Some(c) = cursor {
            let set = s.item_cursors.get(turn).ok_or("item cursor not received")?;
            check_cursor(set, Some(c), direction)?;
        }
        let id = s.thread.clone();
        let mut params = json!({"threadId":id,"turnId":turn,"sortDirection":direction.native()});
        if let Some(limit) = limit { params["limit"] = json!(limit); }
        if let Some(c) = cursor {
            params["cursor"] = json!(c);
        }
        self.issue(
            "thread/items/list",
            "ThreadItemsListParams",
            params,
            Kind::Items(id, turn.into(), direction),
        )
    }
    /// Current accepted item-page observation only; a refusal withholds this
    /// witness, not the prior raw read-only page or supplier history itself.
    pub(crate) fn accepted_items_observation<'a>(
        &'a self,
        query: &HistoryQuery,
    ) -> Result<AcceptedItemsObservation<'a>, String> {
        if self.closed
            || query.factory_id != self.factory_id
            || query.home != self.home
            || query.generation != self.generation
            || query.method != "thread/items/list"
        {
            return Err("foreign/stale/closed accepted history observation".into());
        }
        let selected = self.selected()?;
        let accepted = selected
            .accepted_items
            .as_ref()
            .ok_or("accepted item-page observation unavailable")?;
        if accepted.query != *query
            || accepted.selection_epoch != self.selection_epoch
            || query.params["threadId"] != selected.thread
            || self.streams.get("item-pages") != Some(&accepted.revision)
        {
            return Err("accepted item-page query/selection/stream superseded".into());
        }
        if selected.errors.contains_key("item-pages")
            || self.pending.values().any(|p| {
                p.stream == "item-pages"
                    && p.revision == accepted.revision
                    && p.selection_epoch == self.selection_epoch
            })
        {
            return Err("accepted item-page current observation pending or unavailable".into());
        }
        let page = selected
            .items_page
            .as_ref()
            .ok_or("accepted item-page raw result unavailable")?;
        Ok(AcceptedItemsObservation { accepted, page })
    }

    pub fn read_goal(&mut self) -> Result<HistoryQuery, String> {
        let id = self.selected()?.thread.clone();
        self.issue(
            "thread/goal/get",
            "ThreadGoalGetParams",
            json!({"threadId":id}),
            Kind::Goal(id),
        )
    }
    pub fn read_child(&mut self, child: &str) -> Result<HistoryQuery, String> {
        let selected = self.selected()?;
        let found = selected
            .known_children
            .get(child)
            .ok_or("child not identified by received native items")?;
        if found["discoveryKind"] == "subAgentActivity" {
            if let Some(reason) = found["discoveryLimit"].as_str() {
                return Err(format!("child reference unavailable: {reason}"));
            }
            if let Some(reason) = started_reference_limit(
                selected,
                &self.threads,
                child,
                selected
                    .started_paths
                    .get(child)
                    .map(String::as_str)
                    .unwrap_or_else(|| found["agentPath"].as_str().unwrap_or("")),
            ) {
                return Err(format!("child reference unavailable: {reason}"));
            }
        }
        self.issue(
            "thread/read",
            "ThreadReadParams",
            json!({"threadId":child,"includeTurns":false}),
            Kind::Child(child.into()),
        )
    }
    /// Factory called only by the main-process owner of the explicit Continue
    /// action. It neither dispatches nor proves a person's reserved act.
    pub fn continue_query(&mut self) -> Result<HistoryQuery, String> {
        let id = self.selected()?.thread.clone();
        self.issue(
            "thread/resume",
            "ThreadResumeParams",
            json!({"threadId":id,"excludeTurns":true}),
            Kind::Resume(id),
        )
    }
    fn check_reply(
        &self,
        query: &HistoryQuery,
        source_home: &str,
        source_generation: &Value,
    ) -> Result<&Pending, String> {
        if self.closed
            || source_home != self.home
            || source_generation != &self.generation
            || query.home != self.home
            || query.generation != self.generation
        {
            return Err("foreign/stale/closed history result".into());
        }
        let pending = self
            .pending
            .get(&query.id())
            .ok_or("history query no longer pending")?;
        if pending.query != *query {
            return Err("history query binding differs".into());
        }
        if self.streams.get(&pending.stream) != Some(&pending.revision) {
            return Err("newer query superseded this history result".into());
        }
        if !matches!(pending.kind, Kind::List(_)) && pending.selection_epoch != self.selection_epoch
        {
            return Err("history selection changed since query".into());
        }
        Ok(pending)
    }
    pub fn waiting_ended(&mut self, query: &HistoryQuery) -> Result<(), String> {
        self.check_reply(query, &self.home, &self.generation)?;
        self.pending.get_mut(&query.id()).unwrap().waiting_ended = true;
        Ok(())
    }
    /// A failed local read/validation is not a supplier JSON-RPC error. Keep
    /// that distinction while withholding prior-page/current cursor authority.
    pub(crate) fn read_unavailable(&mut self, query: &HistoryQuery, reason: &str) -> Result<(), String> {
        let pending = self.check_reply(query, &self.home, &self.generation)?;
        let stream = pending.stream.clone();
        let revision = pending.revision;
        let evidence = json!({"standing":"local read unavailable; no native result accepted","query":query,"stream":stream,"revision":revision,"reason":reason});
        let selected = self.selection.as_mut().ok_or("selected read owner absent")?;
        selected.errors.insert(stream.clone(), evidence.clone());
        selected.error_history.push(evidence);
        selected.resolutions.insert(stream, json!({"query":query,"revision":revision,"outcome":"read-unavailable"}));
        self.pending.remove(&query.id());
        Ok(())
    }
    pub(crate) fn supersede_read(&mut self, query: &HistoryQuery) {
        if self.read_unavailable(query, "superseded by a newer context selection").is_err()
            && self.pending.get(&query.id()).is_some_and(|pending| pending.query == *query) {
            self.pending.remove(&query.id());
        }
    }
    pub fn receive_error(
        &mut self,
        query: &HistoryQuery,
        source_home: &str,
        source_generation: &Value,
        error: &Value,
    ) -> Result<(), String> {
        let pending = self.check_reply(query, source_home, source_generation)?;
        validate("JSONRPCErrorError", error)?;
        let list = matches!(pending.kind, Kind::List(_));
        let stream = pending.stream.clone();
        let revision = pending.revision;
        let evidence = json!({"standing":"native error observed; no successful read/resume inferred","query":query,"stream":stream,"revision":revision,"error":error});
        if list {
            self.list_error = Some(evidence);
        } else {
            let selected = self.selection.as_mut().unwrap();
            selected.errors.insert(stream.clone(), evidence.clone());
            selected.error_history.push(evidence);
            selected.resolutions.insert(
                stream,
                json!({"query":query,"revision":revision,"outcome":"native-error-observed"}),
            );
        }
        self.pending.remove(&query.id());
        Ok(())
    }
    pub fn receive(
        &mut self,
        query: &HistoryQuery,
        source_home: &str,
        source_generation: &Value,
        result: &Value,
    ) -> Result<(), String> {
        let pending = self.check_reply(query, source_home, source_generation)?;
        let kind = pending.kind.clone();
        let stream = pending.stream.clone();
        let revision = pending.revision;
        let pinned_child_origin = pending.child_origin.clone();
        let refresh_ancestors =
            matches!(&kind, Kind::List(_) | Kind::Metadata(_) | Kind::Resume(_));
        validate(kind.response_schema(), result)?;
        // Check relational identities before any view mutation.
        if matches!(kind, Kind::List(_))
            && result["data"]
                .as_array()
                .unwrap()
                .iter()
                .any(|t| t["id"].as_str().map(str::is_empty).unwrap_or(true))
        {
            return Err("native thread identity absent/empty".into());
        }
        if matches!(kind, Kind::Turns(_, _))
            && result["data"]
                .as_array()
                .unwrap()
                .iter()
                .any(|t| t["id"].as_str().map(str::is_empty).unwrap_or(true))
        {
            return Err("native turn identity absent/empty".into());
        }
        match &kind {
            Kind::Turns(thread, _) | Kind::Items(thread, _, _)
                if self.selected()?.thread != *thread =>
            {
                return Err("selected history thread binding differs".into())
            }
            _ => {}
        }
        match &kind {
            Kind::Metadata(id) | Kind::Child(id) | Kind::Resume(id)
                if result["thread"]["id"] != *id =>
            {
                return Err("native history thread identity differs".into())
            }
            Kind::Items(_, turn, _)
                if result["data"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .any(|e| e["turnId"] != *turn) =>
            {
                return Err("native item turn identity differs".into())
            }
            Kind::Goal(id)
                if result
                    .get("goal")
                    .filter(|g| !g.is_null())
                    .map(|g| g["threadId"] != *id)
                    .unwrap_or(false) =>
            {
                return Err("native goal thread identity differs".into())
            }
            _ => {}
        }
        match kind {
            Kind::List(direction) => {
                for thread in result["data"].as_array().unwrap() {
                    let id = thread["id"].as_str().ok_or("native thread id absent")?;
                    if id.is_empty() {
                        return Err("native thread id empty".into());
                    }
                    self.threads.insert(id.into(), thread.clone());
                }
                capture_cursors(&mut self.list_cursors, result, direction);
                self.list_page = Some(result.clone());
                self.list_error = None;
            }
            Kind::Metadata(_) => {
                let s = self.selection.as_mut().unwrap();
                s.metadata = Some(result.clone());
            }
            Kind::Turns(_, direction) => {
                let s = self.selection.as_mut().unwrap();
                for turn in result["data"].as_array().unwrap() {
                    s.turn_ids.insert(turn["id"].as_str().unwrap().into());
                }
                capture_cursors(&mut s.turn_cursors, result, direction);
                s.turns_page = Some(result.clone());
            }
            Kind::Items(thread, turn, direction) => {
                let s = self.selection.as_mut().unwrap();
                for entry in result["data"].as_array().unwrap() {
                    let item = &entry["item"];
                    if item["type"] == "collabAgentToolCall" {
                        let completed_spawn = item["tool"] == "spawnAgent"
                            && item["status"] == "completed"
                            && item["senderThreadId"]
                                .as_str()
                                .map(|id| !id.is_empty())
                                .unwrap_or(false);
                        for id in item["receiverThreadIds"].as_array().into_iter().flatten() {
                            if let Some(id) = id.as_str().filter(|id| !id.is_empty()) {
                                let reference = json!({"threadId":id,"sourceThreadId":thread,"sourceTurnId":turn,"sourceItemId":item["id"],"tool":item["tool"],"status":item["status"],"reportedSenderThreadId":item["senderThreadId"],"standing":"native receiver reference; not by itself a parent-child edge or App role"});
                                s.receiver_references.insert(id.into(), reference.clone());
                                if completed_spawn {
                                    s.known_children.entry(id.into()).or_insert_with(|| json!({"threadId":id,"sourceThreadId":thread,"sourceTurnId":turn,"sourceItemId":item["id"],"parentThreadId":item["senderThreadId"],"parentSource":"collabAgentToolCall.senderThreadId","edgeEvidence":"completed spawnAgent"}));
                                }
                                if let Some(child) = s.known_children.get_mut(id) {
                                    child["lastObservedReference"] = reference;
                                }
                            }
                        }
                    } else if item["type"] == "subAgentActivity" {
                        if let Some(id) = item["agentThreadId"].as_str().filter(|id| !id.is_empty())
                        {
                            let reference = json!({"threadId":id,"sourceThreadId":thread,"sourceTurnId":turn,"sourceItemId":item["id"],"kind":item["kind"],"agentPath":item["agentPath"],"sourceQuery":query,"sourceRevision":revision,"standing":"native activity reference; not by itself a parent-child edge or App role"});
                            s.receiver_references.insert(id.into(), reference.clone());
                            let path = item["agentPath"].as_str().unwrap_or("");
                            if item["kind"] == "started" {
                                if let Some(reason) =
                                    started_reference_limit(s, &self.threads, id, path)
                                {
                                    // Preserve positive exclusions even when this
                                    // reference was never admitted as a candidate.
                                    s.known_ancestors.insert(id.to_owned());
                                    if let Some(child) =
                                        s.known_children.get_mut(id).filter(|child| {
                                            child["discoveryKind"] == "subAgentActivity"
                                        })
                                    {
                                        child["discoveryLimit"] = json!(reason);
                                        unconfirm_started(child, reason);
                                        if let Some(read) = s.child_reads.get_mut(id) {
                                            read["parentRelationship"] =
                                                json!({"standing":"unknown","reason":reason});
                                        }
                                    }
                                }
                            }
                            if item["kind"] == "started"
                                && item["id"].as_str().is_some_and(|id| !id.is_empty())
                                && started_reference_limit(s, &self.threads, id, path).is_none()
                            {
                                // Keep the original source fixed; learn the first
                                // nonempty started path as a separate guard basis.
                                let path_conflict = !path.is_empty()
                                    && s.started_paths.get(id).is_some_and(|known| known != path);
                                if !path.is_empty() {
                                    s.started_paths
                                        .entry(id.to_owned())
                                        .or_insert_with(|| path.to_owned());
                                }
                                let child = s.known_children.entry(id.into()).or_insert_with(||json!({"threadId":id,"sourceThreadId":thread,"sourceTurnId":turn,"sourceItemId":item["id"],"sourceQuery":query,"sourceRevision":revision,"discoveryKind":"subAgentActivity","agentPath":path,"parentSource":"not-confirmed","edgeEvidence":"native started reference; parent metadata not read"}));
                                if child["discoveryKind"] == "subAgentActivity" && path_conflict {
                                    let reason =
                                        "conflicting native started paths for the same thread";
                                    child["discoveryLimit"] = json!(reason);
                                    unconfirm_started(child, reason);
                                    if let Some(read) = s.child_reads.get_mut(id) {
                                        read["parentRelationship"] =
                                            json!({"standing":"unknown","reason":reason});
                                    }
                                }
                            }
                            if let Some(child) = s.known_children.get_mut(id) {
                                child["lastObservedReference"] = reference;
                            }
                        }
                    }
                }
                capture_cursors(s.item_cursors.entry(turn).or_default(), result, direction);
                s.items_page = Some(result.clone());
                s.accepted_items = Some(AcceptedItems {
                    query: query.clone(),
                    selection_epoch: self.selection_epoch,
                    revision,
                });
            }
            Kind::Goal(_) => {
                self.selection.as_mut().unwrap().goal = Some(result.clone());
            }
            Kind::Child(id) => {
                let s = self.selection.as_mut().unwrap();
                let child = s.known_children.get(&id).unwrap();
                let started = child["discoveryKind"] == "subAgentActivity";
                let expected = if started {
                    child["sourceThreadId"].as_str()
                } else {
                    child["parentThreadId"].as_str()
                };
                let parents = parent_ids(&result["thread"]);
                let limit = if pinned_child_origin.as_ref() != Some(&child_origin(child)) {
                    Some("native child discovery changed while metadata was pending")
                } else if let Some(reason) = child["discoveryLimit"].as_str() {
                    Some(reason)
                } else if started
                    && started_reference_limit(
                        s,
                        &self.threads,
                        &id,
                        s.started_paths
                            .get(&id)
                            .map(String::as_str)
                            .unwrap_or_else(|| child["agentPath"].as_str().unwrap_or("")),
                    )
                    .is_some()
                {
                    Some("native child discovery now names root, self or an ancestor")
                } else if parents.is_empty() {
                    Some("native child parent was not reported")
                } else if expected.is_none()
                    || parents.iter().any(|parent| Some(*parent) != expected)
                {
                    Some("native child parent differs from the owning discovery thread or is ambiguous")
                } else {
                    None
                };
                let relationship = match limit {
                    Some(reason) => json!({"standing":"unknown","reason":reason}),
                    None => json!({"standing":"native-parent-confirmed","parentThreadId":expected}),
                };
                let limit = limit.map(str::to_owned);
                let expected = expected.map(str::to_owned);
                if started {
                    let child = s.known_children.get_mut(&id).unwrap();
                    if let Some(reason) = limit.as_ref() {
                        unconfirm_started(child, reason);
                    } else {
                        child["parentThreadId"] = json!(expected);
                        child["parentSource"] = json!("thread/read parent metadata");
                        child["edgeEvidence"] =
                            json!("native started reference and matching native parent metadata");
                        child.as_object_mut().unwrap().remove("parentLimit");
                    }
                }
                s.child_reads.insert(id, json!({"native":result,"parentRelationship":relationship,"appRole":role_unknown(),"standing":"child metadata read; no App guidance supply, return/review/integration inferred"}));
            }
            Kind::Resume(_) => {
                let s = self.selection.as_mut().unwrap();
                s.resume = Some(result.clone());
                s.resume_revision = Some(revision);
                s.metadata = Some(json!({"thread":result["thread"]}));
            }
        }
        if refresh_ancestors {
            if let Some(selected) = self.selection.as_mut() {
                refresh_ancestor_limits(selected, &self.threads);
            }
        }
        if !matches!(self.pending.get(&query.id()).unwrap().kind, Kind::List(_)) {
            let selected = self.selection.as_mut().unwrap();
            selected.errors.remove(&stream);
            selected.resolutions.insert(
                stream,
                json!({"query":query,"revision":revision,"outcome":"native-result-observed"}),
            );
        }
        self.pending.remove(&query.id());
        Ok(())
    }
    pub fn close_generation(&mut self, generation: &Value) -> Result<(), String> {
        if generation != &self.generation {
            return Err("foreign generation closure".into());
        }
        self.closed = true;
        self.pending.clear();
        self.selection = None;
        self.threads.clear();
        self.list_page = None;
        self.list_cursors.clear();
        Ok(())
    }
    /// Candidate metadata for a later active owner, never registration performed
    /// by this read/query seam. Caller must recheck actual current Host scope.
    pub fn resumed_thread(&self) -> Option<Value> {
        if self.closed {
            return None;
        }
        let s = self.selection.as_ref()?;
        let resume_revision = s.resume_revision?;
        if self.streams.get("thread-state") != Some(&resume_revision)
            || s.errors.contains_key("thread-state")
            || self.pending.values().any(|p| {
                p.selection_epoch == self.selection_epoch
                    && p.stream == "thread-state"
                    && p.revision == resume_revision
            })
        {
            return None;
        }
        let response = s.resume.as_ref()?;
        let status = response["thread"]["status"]["type"].as_str()?;
        if !matches!(status, "idle" | "active")
            || response["thread"]["canAcceptDirectInput"] == false
        {
            return None;
        }
        Some(
            json!({"home":self.home,"generation":self.generation,"threadId":s.thread,"native":response["thread"],"standing":"explicit Continue query and matching native resume response observed; active owner must recheck and bind","directInput":response["thread"].get("canAcceptDirectInput"),"appRole":role_unknown()}),
        )
    }
    pub fn snapshot(&self) -> Value {
        let resume_eligible = self.resumed_thread().is_some();
        let selected=self.selection.as_ref().map(|s|{let goal=if s.errors.contains_key("goal") {"unavailable"} else if s.resolutions.get("goal").map(|r|r["outcome"]=="pending").unwrap_or(false) {"pending; prior value is only last observed"} else {match s.goal.as_ref().and_then(|g|g.get("goal")){None=>"not-reported",Some(Value::Null)=>"no-goal-reported",Some(_)=>"reported"}};json!({"threadId":s.thread,"state":if !s.errors.is_empty(){"unavailable"}else if resume_eligible{"resume-response-observed"}else{"indexed-read-only"},"metadata":s.metadata,"turnsPage":s.turns_page,"turnCursor":cursor_view(s.turns_page.as_ref()),"itemsPage":s.items_page,"itemCursor":cursor_view(s.items_page.as_ref()),"goal":s.goal,"goalAvailability":goal,"knownChildren":s.known_children.values().collect::<Vec<_>>(),"receiverReferences":s.receiver_references.values().collect::<Vec<_>>(),"childReads":s.child_reads,"resume":s.resume,"resumeEligibilityCurrent":resume_eligible,"error":s.errors.values().next(),"errorsByStream":s.errors,"errorHistory":s.error_history,"streamResolutions":s.resolutions,"appRole":role_unknown(),"checklists":"not kept in supplier history; prior checklist updates cannot be reconstructed after restart/relaunch"})});
        json!({"home":self.home,"generation":self.generation,"state":if self.closed{"observation-ended"}else{"history-receiving"},"threads":self.threads.values().map(|t|json!({"native":t,"appRole":role_unknown()})).collect::<Vec<_>>(),"listPage":self.list_page,"listCursor":cursor_view(self.list_page.as_ref()),"listError":self.list_error,"selected":selected,"pending":self.pending.values().map(|p|json!({"query":p.query,"waitingEnded":p.waiting_ended,"outcome":"pending; query factory/dispatch is not observed success"})).collect::<Vec<_>>(),"activeBindingPerformed":false,"durableNativeData":false,"limits":["Native history is read from the engine; these are disposable page views.","notLoaded/summary/empty/null/unreported are distinct native facts, not absent events.","Parent/child status is not return, review or integration.","ForkedFromId is relation only; original App role stays unknown without bound supply evidence."]})
    }
}
