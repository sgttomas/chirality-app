//! Dormant offered-call custody. No production offer issuer or managed service.
use super::{Inner, SourceRequest};
use crate::role_supply::{Composition, Role};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::io::{self, Write};
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicU8, Ordering};
use std::sync::{Arc, Condvar, Mutex, Weak};

pub(crate) const TOOL: &str = "chirality_c3_request_answer_v1";
pub(crate) const UNAVAILABLE: &str = "managed-service-unavailable: no TASK session was created";
pub(crate) const FRAME_LIMIT: usize = 32768;
pub(crate) const ARGS_LIMIT: usize = 16384;
pub(crate) const ID_LIMIT: usize = 256;
pub(crate) const PATH_LIMIT: usize = 4096;
pub(crate) const CLAIM_LIMIT: usize = 32;
pub(crate) const BYTE_LENGTH_MAX: u64 = 9007199254740991;
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum Refusal {
    Shape,
    Limit,
    Tool,
    Stale,
    Capacity,
    Duplicate,
    Origin,
    AlreadyAttempted,
}
impl Refusal {
    pub(crate) fn message(self) -> &'static str {
        match self {
            Self::Shape | Self::Limit => "Invalid arguments for offered tool",
            Self::Capacity => "Offered call capacity exhausted",
            _ => "Original offered call unavailable",
        }
    }
}
fn bounded_str(v: &Value, max: usize) -> Result<&str, Refusal> {
    v.as_str()
        .filter(|s| !s.is_empty() && s.len() <= max)
        .ok_or(Refusal::Shape)
}
fn boxed(s: &str) -> Result<Box<str>, Refusal> {
    if s.is_empty() || s.len() > ID_LIMIT {
        return Err(Refusal::Limit);
    }
    Ok(s.into())
}
fn walk(v: &Value, depth: usize, nodes: &mut usize, string_limit: usize) -> Result<(), Refusal> {
    *nodes = nodes.checked_add(1).ok_or(Refusal::Limit)?;
    if *nodes > 512 {
        return Err(Refusal::Limit);
    }
    match v {
        Value::String(s) if s.len() > string_limit => Err(Refusal::Limit),
        Value::Array(a) => {
            if depth >= 8 || a.len() > 64 {
                return Err(Refusal::Limit);
            }
            for x in a {
                walk(x, depth + 1, nodes, string_limit)?
            }
            Ok(())
        }
        Value::Object(o) => {
            if depth >= 8 || o.len() > 64 {
                return Err(Refusal::Limit);
            }
            for (k, x) in o {
                if k.len() > 256 {
                    return Err(Refusal::Limit);
                }
                *nodes += 1;
                if *nodes > 512 {
                    return Err(Refusal::Limit);
                }
                walk(x, depth + 1, nodes, string_limit)?
            }
            Ok(())
        }
        _ => Ok(()),
    }
}
struct Count {
    bytes: usize,
    limit: usize,
}
impl Write for Count {
    fn write(&mut self, b: &[u8]) -> io::Result<usize> {
        self.bytes = self
            .bytes
            .checked_add(b.len())
            .filter(|n| *n <= self.limit)
            .ok_or_else(|| io::Error::from(io::ErrorKind::FileTooLarge))?;
        Ok(b.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}
pub(crate) fn count_bytes(v: &Value, limit: usize) -> Result<(), Refusal> {
    serde_json::to_writer(Count { bytes: 0, limit }, v).map_err(|_| Refusal::Limit)
}
pub(crate) fn bounded(v: &Value, limit: usize, string_limit: usize) -> Result<(), Refusal> {
    walk(v, 0, &mut 0, string_limit)?;
    count_bytes(v, limit)
}
pub(crate) fn digest(v: &Value) -> Result<[u8; 32], Refusal> {
    super::request_event_join::pf1(v).map_err(|_| Refusal::Limit)
}
fn hash(s: &str) -> [u8; 32] {
    Sha256::digest(s.as_bytes()).into()
}
pub(crate) fn definition() -> Value {
    json!({"type":"function","name":TOOL,"description":"Request one bounded C3 answer from the App managed-session service; unavailable when that service is absent.","inputSchema":{"type":"object","additionalProperties":false,"required":["base","question","claimIds"],"properties":{"base":{"type":"object","additionalProperties":false,"required":["path","id","byteLength","sha256"],"properties":{"path":{"type":"string","minLength":1},"id":{"type":"string","minLength":1},"byteLength":{"type":"integer","minimum":0},"sha256":{"type":"string","minLength":64,"maxLength":64,"pattern":"^[0-9a-f]{64}$"}}},"question":{"type":"string","minLength":1},"claimIds":{"type":"array","uniqueItems":true,"items":{"type":"string","minLength":1}}}}})
}
pub(crate) fn unavailable() -> Value {
    json!({"success":false,"contentItems":[{"type":"inputText","text":UNAVAILABLE}]})
}
pub(crate) fn arguments(v: &Value) -> Result<(), Refusal> {
    bounded(v, ARGS_LIMIT, 8192)?;
    let o = v.as_object().ok_or(Refusal::Shape)?;
    if o.len() != 3
        || !o.contains_key("base")
        || !o.contains_key("question")
        || !o.contains_key("claimIds")
    {
        return Err(Refusal::Shape);
    }
    let b = o["base"].as_object().ok_or(Refusal::Shape)?;
    if b.len() != 4
        || !["path", "id", "byteLength", "sha256"]
            .iter()
            .all(|k| b.contains_key(*k))
    {
        return Err(Refusal::Shape);
    }
    bounded_str(&b["path"], PATH_LIMIT)?;
    bounded_str(&b["id"], ID_LIMIT)?;
    bounded_str(&o["question"], ID_LIMIT)?;
    let valid_length = b["byteLength"]
        .as_u64()
        .is_some_and(|n| n <= BYTE_LENGTH_MAX)
        || b["byteLength"].as_f64().is_some_and(|n| {
            n.is_finite() && n >= 0.0 && n <= BYTE_LENGTH_MAX as f64 && n.fract() == 0.0
        });
    if !valid_length {
        return Err(Refusal::Shape);
    }
    let sha = bounded_str(&b["sha256"], 64)?;
    if sha.len() != 64
        || !sha
            .bytes()
            .all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c))
    {
        return Err(Refusal::Shape);
    }
    let ids = o["claimIds"].as_array().ok_or(Refusal::Shape)?;
    if ids.len() > CLAIM_LIMIT {
        return Err(Refusal::Limit);
    }
    for (n, id) in ids.iter().enumerate() {
        let s = bounded_str(id, ID_LIMIT)?;
        if ids[..n].iter().any(|x| x.as_str() == Some(s)) {
            return Err(Refusal::Shape);
        }
    }
    Ok(())
}

pub(crate) struct OfferIntent {
    supply_ref: Box<str>,
    role: Role,
    guidance: [u8; 32],
    common: [u8; 32],
    role_text: [u8; 32],
    definition: [u8; 32],
}
impl OfferIntent {
    #[cfg(test)]
    pub(super) fn new(c: &Composition, supply_ref: &str) -> Result<Self, Refusal> {
        c.verify().map_err(|_| Refusal::Origin)?;
        let role = c
            .role
            .filter(|r| matches!(r, Role::HELP_HUMAN | Role::WORKING_ITEMS))
            .ok_or(Refusal::Origin)?;
        if c.text.len() > 65536 {
            return Err(Refusal::Limit);
        }
        let parts = c.carried["developerInstructions"]["parts"]
            .as_array()
            .filter(|p| p.len() == 2)
            .ok_or(Refusal::Origin)?;
        let piece = |n: usize| -> Result<&str, Refusal> {
            let offset = parts[n]["offset"].as_u64().ok_or(Refusal::Origin)? as usize;
            let len = parts[n]["length"].as_u64().ok_or(Refusal::Origin)? as usize;
            c.text
                .get(offset..offset.checked_add(len).ok_or(Refusal::Limit)?)
                .ok_or(Refusal::Origin)
        };
        let d = definition();
        bounded(&d, 4096, 8192)?;
        if !supply_ref.starts_with("sup:") || supply_ref.len() <= 4 {
            return Err(Refusal::Origin);
        }
        Ok(Self {
            supply_ref: boxed(supply_ref)?,
            role,
            guidance: hash(&c.text),
            common: hash(piece(0)?),
            role_text: hash(piece(1)?),
            definition: digest(&d)?,
        })
    }
}
#[derive(Clone, PartialEq, Eq)]
pub(crate) struct SmallId {
    bytes: [u8; ID_LIMIT],
    len: u16,
}
impl SmallId {
    fn new(s: &str) -> Result<Self, Refusal> {
        if s.is_empty() || s.len() > ID_LIMIT {
            return Err(Refusal::Limit);
        }
        let mut id = Self {
            bytes: [0; ID_LIMIT],
            len: s.len() as u16,
        };
        id.bytes[..s.len()].copy_from_slice(s.as_bytes());
        Ok(id)
    }
    fn text(&self) -> &str {
        std::str::from_utf8(&self.bytes[..self.len as usize]).expect("constructed UTF8")
    }
}
#[derive(Clone, PartialEq, Eq)]
pub(crate) struct Scope {
    session: SmallId,
    home: SmallId,
    counter: u64,
}
impl Scope {
    fn new(g: &Value) -> Result<Self, Refusal> {
        if g.as_object().is_none_or(|o| o.len() != 3) {
            return Err(Refusal::Shape);
        }
        Ok(Self {
            session: SmallId::new(g["appSession"].as_str().ok_or(Refusal::Shape)?)?,
            home: SmallId::new(g["home"].as_str().ok_or(Refusal::Shape)?)?,
            counter: g["spawnCounter"]
                .as_u64()
                .filter(|n| *n > 0)
                .ok_or(Refusal::Shape)?,
        })
    }
    pub(super) fn matches(&self, g: &Value) -> bool {
        g.as_object().is_some_and(|o| o.len() == 3)
            && g["appSession"].as_str() == Some(self.session.text())
            && g["home"].as_str() == Some(self.home.text())
            && g["spawnCounter"].as_u64() == Some(self.counter)
    }
    #[cfg(test)]
    fn view(&self) -> Value {
        json!({"appSession":self.session.text(),"home":self.home.text(),"spawnCounter":self.counter})
    }
}
#[derive(Clone, PartialEq, Eq)]
pub(crate) enum Rpc {
    Signed(i64),
    Unsigned(u64),
    Text(SmallId),
}
impl Rpc {
    fn new(v: &Value) -> Result<Self, Refusal> {
        if let Some(n) = v.as_i64() {
            Ok(Self::Signed(n))
        } else if let Some(n) = v.as_u64() {
            Ok(Self::Unsigned(n))
        } else {
            Ok(Self::Text(SmallId::new(v.as_str().ok_or(Refusal::Shape)?)?))
        }
    }
    pub(super) fn matches(&self, v: &Value) -> bool {
        match self {
            Self::Signed(n) => v.as_i64() == Some(*n),
            Self::Unsigned(n) => v.as_u64() == Some(*n),
            Self::Text(s) => v.as_str() == Some(s.text()),
        }
    }
    pub(super) fn view(&self) -> Value {
        match self {
            Self::Signed(n) => json!(n),
            Self::Unsigned(n) => json!(n),
            Self::Text(s) => json!(s.text()),
        }
    }
}
struct Life {
    alive: AtomicBool,
}
pub(crate) struct ManagerOwner {
    pin: StartPin,
    life: Arc<Life>,
}
impl Drop for ManagerOwner {
    fn drop(&mut self) {
        self.life.alive.store(false, Ordering::SeqCst);
    }
}
impl ManagerOwner {
    pub(crate) fn from_inserted(inserted: crate::role_lifecycle::CceInserted) -> Self {
        Self {
            pin: inserted.into_pin(),
            life: Arc::new(Life {
                alive: AtomicBool::new(true),
            }),
        }
    }
}

pub(crate) struct StartPin {
    host: Weak<(Mutex<Inner>, Condvar)>,
    generation: Scope,
    start_ref: Box<str>,
    rpc: Rpc,
    thread: Box<str>,
    supply_ref: Box<str>,
    role: Role,
    guidance: [u8; 32],
    common: [u8; 32],
    role_text: [u8; 32],
    frame: [u8; 32],
}
impl StartPin {
    pub(crate) fn role_matches(
        &self,
        home: &str,
        thread: &str,
        generation: &Value,
        rpc: &Value,
        reference: &str,
        supply_ref: &str,
        role: Option<Role>,
        text: &str,
        common: &str,
        role_text: &str,
    ) -> bool {
        self.generation.matches(generation)
            && self.generation.home.text() == home
            && self.thread.as_ref() == thread
            && self.rpc.matches(rpc)
            && self.start_ref.as_ref() == reference
            && self.supply_ref.as_ref() == supply_ref
            && role == Some(self.role)
            && hash(text) == self.guidance
            && hash(common) == self.common
            && hash(role_text) == self.role_text
    }
}

pub(super) struct Offer {
    host: Weak<(Mutex<Inner>, Condvar)>,
    generation: Scope,
    start_ref: Box<str>,
    rpc: Rpc,
    frame: [u8; 32],
    intent: OfferIntent,
    thread: Option<Box<str>>,
    life: Weak<Life>,
    retired: bool,
    call: Option<Arc<CallFacts>>,
    taken: bool,
}
impl Offer {
    pub(super) fn bind(
        intent: OfferIntent,
        host: &Arc<(Mutex<Inner>, Condvar)>,
        request: &SourceRequest,
    ) -> Result<Self, Refusal> {
        // The sender constructs the fixed RPC wrapper; validate bounded start params
        // (including the static schema) separately from the whole-frame byte cap.
        bounded(&request.frame["params"], 65536, 65536)?;
        count_bytes(&request.frame, 65536)?;
        for k in ["appSession", "home"] {
            bounded_str(&request.generation[k], 256)?;
        }
        let defs = request.frame["params"]["dynamicTools"]
            .as_array()
            .filter(|v| v.len() == 1)
            .ok_or(Refusal::Origin)?;
        if request.frame["method"] != "thread/start"
            || digest(&defs[0])? != intent.definition
            || request.frame["params"]["developerInstructions"]
                .as_str()
                .is_none_or(|s| hash(s) != intent.guidance)
        {
            return Err(Refusal::Origin);
        }
        Ok(Self {
            host: Arc::downgrade(host),
            generation: Scope::new(&request.generation)?,
            start_ref: boxed(request.request_ref())?,
            rpc: Rpc::new(request.request_id())?,
            frame: digest(&request.frame)?,
            intent,
            thread: None,
            life: Weak::new(),
            retired: false,
            call: None,
            taken: false,
        })
    }
    pub(super) fn request_matches(&self, r: &SourceRequest) -> bool {
        self.generation.matches(&r.generation)
            && self.start_ref.as_ref() == r.request_ref()
            && self.rpc.matches(r.request_id())
            && Weak::ptr_eq(&self.host, &r.source)
    }
    pub(super) fn native_admitted(&mut self, r: &SourceRequest, thread: &str) {
        if self.request_matches(r) && !self.retired {
            if let Ok(t) = boxed(thread) {
                self.thread = Some(t)
            }
        }
    }
    pub(super) fn start_pin(&self, r: &SourceRequest) -> Result<StartPin, Refusal> {
        if self.retired || !self.request_matches(r) || digest(&r.frame)? != self.frame {
            return Err(Refusal::Stale);
        }
        Ok(StartPin {
            host: self.host.clone(),
            generation: self.generation.clone(),
            start_ref: self.start_ref.clone(),
            rpc: self.rpc.clone(),
            thread: self.thread.clone().ok_or(Refusal::Origin)?,
            supply_ref: self.intent.supply_ref.clone(),
            role: self.intent.role,
            guidance: self.intent.guidance,
            common: self.intent.common,
            role_text: self.intent.role_text,
            frame: self.frame,
        })
    }
    pub(super) fn adopt(&mut self, owner: &ManagerOwner) -> Result<(), Refusal> {
        let p = &owner.pin;
        if self.retired
            || !Weak::ptr_eq(&self.host, &p.host)
            || self.generation != p.generation
            || self.start_ref != p.start_ref
            || self.thread.as_deref() != Some(p.thread.as_ref())
            || self.frame != p.frame
        {
            return Err(Refusal::Stale);
        }
        self.life = Arc::downgrade(&owner.life);
        Ok(())
    }
    fn alive(&self) -> bool {
        !self.retired
            && self
                .life
                .upgrade()
                .is_some_and(|l| l.alive.load(Ordering::SeqCst))
    }
    pub(super) fn scope_matches(&self, g: &Value) -> bool {
        self.generation.matches(g) && !self.retired
    }
    pub(super) fn retire(&mut self) {
        self.retired = true;
    }
    pub(super) fn classify(&self, g: &Value, frame: &Value) -> Option<Result<Admission, Refusal>> {
        if !self.alive() {
            return None;
        }
        if !(frame["id"].as_i64().is_some()
            || frame["id"].as_u64().is_some()
            || frame["id"]
                .as_str()
                .is_some_and(|s| !s.is_empty() && s.len() <= ID_LIMIT))
        {
            return None;
        }
        if !self.generation.matches(g) {
            return Some(Err(Refusal::Stale));
        }
        let p = &frame["params"];
        if p["threadId"].as_str() != self.thread.as_deref() {
            return Some(Err(Refusal::Stale));
        }
        if p["tool"] != TOOL || !p.get("namespace").is_none_or(Value::is_null) {
            return Some(Err(Refusal::Tool));
        }
        if self.call.is_some() {
            return Some(Err(Refusal::Capacity));
        }
        Some((|| {
            bounded(frame, FRAME_LIMIT, 8192)?;
            for k in ["threadId", "turnId", "callId", "tool"] {
                bounded_str(&p[k], ID_LIMIT)?;
            }
            if !(frame["id"].as_i64().is_some()
                || frame["id"].as_u64().is_some()
                || frame["id"]
                    .as_str()
                    .is_some_and(|s| !s.is_empty() && s.len() <= ID_LIMIT))
            {
                return Err(Refusal::Shape);
            }
            arguments(&p["arguments"])?;
            Ok(Admission {
                frame: digest(frame)?,
                params: digest(p)?,
            })
        })())
    }
    pub(super) fn received(
        &mut self,
        g: &Value,
        position: u64,
        index: usize,
        frame: &Value,
        a: Admission,
    ) {
        if self.call.is_none() {
            self.call = Some(Arc::new(CallFacts {
                generation: Scope::new(g).expect("validated original scope"),
                rpc: Rpc::new(&frame["id"]).expect("validated original RPC"),
                thread: boxed(frame["params"]["threadId"].as_str().unwrap()).unwrap(),
                turn: boxed(frame["params"]["turnId"].as_str().unwrap()).unwrap(),
                call_id: boxed(frame["params"]["callId"].as_str().unwrap()).unwrap(),
                receipt: position,
                index,
                frame: a.frame,
                params: a.params,
                state: AtomicU8::new(0),
                cut: AtomicU64::new(0),
                resolution: AtomicU64::new(0),
                canonical: AtomicBool::new(false),
            }));
        }
    }
    #[cfg(test)]
    pub(super) fn inspect(&self) -> Option<Value> {
        self.call.as_ref().map(|facts| {
            IncomingCall {
                host: self.host.clone(),
                facts: Arc::clone(facts),
            }
            .readout()
        })
    }
    pub(super) fn take(&mut self) -> Option<IncomingCall> {
        if self.taken {
            return None;
        }
        let facts = self.call.clone()?;
        self.taken = true;
        Some(IncomingCall {
            host: self.host.clone(),
            facts,
        })
    }
    pub(super) fn original(&self, h: &IncomingCall) -> bool {
        self.alive()
            && Weak::ptr_eq(&self.host, &h.host)
            && self.call.as_ref().is_some_and(|c| Arc::ptr_eq(c, &h.facts))
    }
    pub(super) fn resolution(&self, g: &Value, pos: u64, p: &Value) {
        if let Some(c) = &self.call {
            if c.generation.matches(g)
                && c.rpc.matches(&p["requestId"])
                && p["threadId"] == c.thread.as_ref()
            {
                let _ = c
                    .resolution
                    .compare_exchange(0, pos, Ordering::SeqCst, Ordering::SeqCst);
            }
        }
    }
}
// Only an active Offer can construct this classification provenance.
pub(crate) struct Admission {
    frame: [u8; 32],
    params: [u8; 32],
}
pub(crate) struct IncomingCall {
    host: Weak<(Mutex<Inner>, Condvar)>,
    pub(super) facts: Arc<CallFacts>,
}
pub(super) struct CallFacts {
    pub generation: Scope,
    pub rpc: Rpc,
    thread: Box<str>,
    turn: Box<str>,
    call_id: Box<str>,
    pub receipt: u64,
    pub index: usize,
    frame: [u8; 32],
    pub params: [u8; 32],
    pub state: AtomicU8,
    pub cut: AtomicU64,
    pub resolution: AtomicU64,
    pub canonical: AtomicBool,
}
impl IncomingCall {
    pub(super) fn belongs(&self, host: &Arc<(Mutex<Inner>, Condvar)>) -> bool {
        Weak::ptr_eq(&self.host, &Arc::downgrade(host))
    }
    #[cfg(test)]
    pub(super) fn readout(&self) -> Value {
        json!({"generation":self.facts.generation.view(),"rpc":self.facts.rpc.view(),"thread":self.facts.thread,"turn":self.facts.turn,"callId":self.facts.call_id,"receipt":self.facts.receipt,"frameDigest":self.facts.frame,"state":self.facts.state.load(Ordering::SeqCst),"cut":self.facts.cut.load(Ordering::SeqCst),"resolution":self.facts.resolution.load(Ordering::SeqCst),"canonicalUpdated":self.facts.canonical.load(Ordering::SeqCst),"delivery":"not-established","lifetime":"same-process original attempt only; not recovery authority"})
    }
}

pub(crate) const RETAINED_LIMIT: usize = 16384;
pub(crate) const SCRATCH_LIMIT: usize = 65536;
pub(crate) const INCREMENTAL_LIMIT: usize = 131072;
// Nine bounded boxed identities; fixed H5/RPC arrays; two Arc allocation headers.
pub(crate) const RETAINED_BOUND: usize = std::mem::size_of::<Offer>()
    + std::mem::size_of::<ManagerOwner>()
    + std::mem::size_of::<CallFacts>()
    + std::mem::size_of::<Life>()
    + 2 * std::mem::size_of::<IncomingCall>()
    + 9 * ID_LIMIT
    + 4 * std::mem::size_of::<usize>();
pub(crate) const fn budget_ok(retained: usize, scratch: usize, total: usize) -> bool {
    retained <= RETAINED_LIMIT && scratch <= SCRATCH_LIMIT && total <= INCREMENTAL_LIMIT
}
const _: () = assert!(budget_ok(
    RETAINED_BOUND,
    super::request_event_join::SORT_SCRATCH + 4096,
    RETAINED_BOUND + super::request_event_join::SORT_SCRATCH + 4096
));

#[cfg(test)]
mod call_custody_tests {
    include!("hosting_call_custody_tests.rs");
}
