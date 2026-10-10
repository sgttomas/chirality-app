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
            resume: None,
            resume_revision: None,
            errors: BTreeMap::new(),
            error_history: Vec::new(),
            resolutions: BTreeMap::new(),
        }
    }
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
fn validate(target: &str, value: &Value) -> Result<(), String> {
    validators()?
        .get(target)
        .ok_or("native schema unavailable")?
        .validate(value)
        .map_err(|e| format!("native history schema refused {target}: {e}"))
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
        self.pending.insert(
            query.id(),
            Pending {
                query: query.clone(),
                kind,
                selection_epoch: self.selection_epoch,
                stream,
                revision,
                waiting_ended: false,
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
        let s = self.selected()?;
        check_cursor(&s.turn_cursors, cursor, direction)?;
        let id = s.thread.clone();
        let mut params =
            json!({"threadId":id,"sortDirection":direction.native(),"itemsView":"summary"});
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
        if !self.selected()?.known_children.contains_key(child) {
            return Err("child not identified by received native items".into());
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
            json!({"threadId":id}),
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
                            let reference = json!({"threadId":id,"sourceThreadId":thread,"sourceTurnId":turn,"sourceItemId":item["id"],"standing":"native activity reference; no completed-spawn parent edge established"});
                            s.receiver_references.insert(id.into(), reference.clone());
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
                self.selection
                    .as_mut()
                    .unwrap()
                    .child_reads
                    .insert(id, json!({"native":result,"appRole":role_unknown(),"standing":"child metadata read; no return/review/integration inferred"}));
            }
            Kind::Resume(_) => {
                let s = self.selection.as_mut().unwrap();
                s.resume = Some(result.clone());
                s.resume_revision = Some(revision);
                s.metadata = Some(json!({"thread":result["thread"]}));
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
