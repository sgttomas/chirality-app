//! Dormant AA-CAP consistency only. No production reservation issuer.
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::io::{self, Write};
use std::sync::{Arc, Condvar, Mutex, Weak};

pub(super) const FRAME: usize = 262144;
pub(super) const TEXT: usize = 65536;
pub(super) const ID: usize = 256;
pub(super) const NODES: usize = 4096;
pub(super) const WIDTH: usize = 128;
pub(super) const DEPTH: usize = 16;
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum Reason {
    Shape,
    Limit,
    Foreign,
    NoAttempt,
    Write,
    Conflict,
    Closed,
    Exhausted,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum Standing {
    Pending,
    ConsistentThroughReceipt(u64, u64),
    Refused(Reason),
}
#[derive(Clone, PartialEq, Eq)]
struct Identity {
    bytes: [u8; ID],
    len: u16,
}
impl Identity {
    fn new(s: &str) -> Result<Self, Reason> {
        if s.is_empty() || s.len() > ID {
            return Err(Reason::Limit);
        }
        let mut v = Self {
            bytes: [0; ID],
            len: s.len() as u16,
        };
        v.bytes[..s.len()].copy_from_slice(s.as_bytes());
        Ok(v)
    }
    fn matches(&self, s: &str) -> bool {
        self.bytes[..self.len as usize] == *s.as_bytes()
    }
}
#[derive(Clone, PartialEq, Eq)]
struct Generation {
    session: Identity,
    home: Identity,
    counter: u64,
}
impl Generation {
    fn new(v: &Value) -> Result<Self, Reason> {
        Ok(Self {
            session: Identity::new(v["appSession"].as_str().ok_or(Reason::Shape)?)?,
            home: Identity::new(v["home"].as_str().ok_or(Reason::Shape)?)?,
            counter: v["spawnCounter"]
                .as_u64()
                .filter(|n| *n > 0)
                .ok_or(Reason::Shape)?,
        })
    }
    fn matches(&self, v: &Value) -> bool {
        v["appSession"]
            .as_str()
            .is_some_and(|s| self.session.matches(s))
            && v["home"].as_str().is_some_and(|s| self.home.matches(s))
            && v["spawnCounter"].as_u64() == Some(self.counter)
    }
}
pub(super) struct CaptureReservation {
    host: Weak<(Mutex<super::Inner>, Condvar)>,
    epoch: u64,
}
impl CaptureReservation {
    #[cfg(test)]
    pub(super) fn new(host: &Arc<(Mutex<super::Inner>, Condvar)>, epoch: u64) -> Self {
        Self {
            host: Arc::downgrade(host),
            epoch,
        }
    }
    pub(super) fn matches(&self, host: &Arc<(Mutex<super::Inner>, Condvar)>, epoch: u64) -> bool {
        self.epoch == epoch && Weak::ptr_eq(&self.host, &Arc::downgrade(host))
    }
}

fn visit(v: &Value, depth: usize, nodes: &mut usize) -> Result<(), Reason> {
    *nodes = nodes.checked_add(1).ok_or(Reason::Limit)?;
    if *nodes > NODES {
        return Err(Reason::Limit);
    }
    match v {
        Value::String(s) if s.len() > TEXT => Err(Reason::Limit),
        Value::Array(a) => {
            if depth >= DEPTH || a.len() > WIDTH {
                return Err(Reason::Limit);
            }
            for x in a {
                visit(x, depth + 1, nodes)?;
            }
            Ok(())
        }
        Value::Object(o) => {
            if depth >= DEPTH || o.len() > WIDTH {
                return Err(Reason::Limit);
            }
            for (k, x) in o {
                if k.len() > ID {
                    return Err(Reason::Limit);
                }
                *nodes = nodes.checked_add(1).ok_or(Reason::Limit)?;
                if *nodes > NODES {
                    return Err(Reason::Limit);
                }
                visit(x, depth + 1, nodes)?;
            }
            Ok(())
        }
        _ => Ok(()),
    }
}
struct HashSink {
    hash: Sha256,
    bytes: usize,
}
impl Write for HashSink {
    fn write(&mut self, b: &[u8]) -> io::Result<usize> {
        let n = self
            .bytes
            .checked_add(b.len())
            .filter(|n| *n <= FRAME)
            .ok_or_else(|| io::Error::from(io::ErrorKind::FileTooLarge))?;
        self.hash.update(b);
        self.bytes = n;
        Ok(b.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}
fn encode(v: &Value, s: &mut HashSink) -> Result<(), Reason> {
    let put = |s: &mut HashSink, b: &[u8]| s.write_all(b).map_err(|_| Reason::Limit);
    match v {
        Value::Array(a) => {
            put(s, b"[")?;
            for (n, x) in a.iter().enumerate() {
                if n > 0 {
                    put(s, b",")?;
                }
                encode(x, s)?;
            }
            put(s, b"]")
        }
        Value::Object(o) => {
            // Fixed borrowed scratch, never allocated from input length.
            let mut keys: [Option<(&str, &Value)>; WIDTH] = [None; WIDTH];
            for (n, (k, v)) in o.iter().enumerate() {
                keys[n] = Some((k.as_str(), v));
            }
            keys[..o.len()]
                .sort_unstable_by(|a, b| a.unwrap().0.as_bytes().cmp(b.unwrap().0.as_bytes()));
            put(s, b"{")?;
            for (n, e) in keys[..o.len()].iter().enumerate() {
                let (k, v) = e.unwrap();
                if n > 0 {
                    put(s, b",")?;
                }
                serde_json::to_writer(&mut *s, k).map_err(|_| Reason::Limit)?;
                put(s, b":")?;
                encode(v, s)?;
            }
            put(s, b"}")
        }
        _ => serde_json::to_writer(s, v).map_err(|_| Reason::Limit),
    }
}
pub(super) fn pf1(v: &Value) -> Result<[u8; 32], Reason> {
    visit(v, 0, &mut 0)?;
    let mut s = HashSink {
        hash: Sha256::new(),
        bytes: 0,
    };
    s.hash.update(b"chirality-aa-cap-pf1\0");
    encode(v, &mut s)?;
    Ok(s.hash.finalize().into())
}
fn scalar(v: &Value) -> Result<[u8; 32], Reason> {
    match v {
        Value::String(s) if s.len() <= ID => pf1(v),
        Value::String(_) => Err(Reason::Limit),
        Value::Number(_) | Value::Null | Value::Bool(_) => pf1(v),
        _ => Err(Reason::Shape),
    }
}
fn text(v: &Value) -> Result<([u8; 32], usize), Reason> {
    let s = v.as_str().ok_or(Reason::Shape)?;
    if s.len() > TEXT {
        return Err(Reason::Limit);
    }
    Ok((Sha256::digest(s.as_bytes()).into(), s.len()))
}
fn ident(v: &Value) -> Result<Identity, Reason> {
    Identity::new(v.as_str().ok_or(Reason::Shape)?)
}

pub(super) struct Core {
    epoch: u64,
    revision: u64,
    receipt: u64,
    standing: Standing,
    generation: Option<Generation>,
    request_ref: Option<Identity>,
    rpc: Option<[u8; 32]>,
    thread: Option<Identity>,
    request_digest: Option<[u8; 32]>,
    request_text: Option<([u8; 32], usize)>,
    pipe: Option<(u64, (u64, u64))>,
    cut: Option<u64>,
    written: bool,
    turn: Option<Identity>,
    response: Option<[u8; 32]>,
    item: Option<(Identity, [u8; 32], ([u8; 32], usize))>,
    terminal: Option<[u8; 32]>,
}
impl Core {
    pub(super) fn bind(
        reservation: CaptureReservation,
        host: &Arc<(Mutex<super::Inner>, Condvar)>,
        epoch: u64,
        g: &Value,
        reference: &str,
        frame: &Value,
        pipe: Option<(u64, (u64, u64))>,
    ) -> Self {
        let mut c = Self {
            epoch,
            revision: 0,
            receipt: 0,
            standing: Standing::Pending,
            generation: None,
            request_ref: None,
            rpc: None,
            thread: None,
            request_digest: None,
            request_text: None,
            pipe,
            cut: None,
            written: false,
            turn: None,
            response: None,
            item: None,
            terminal: None,
        };
        let result = (|| {
            if !reservation.matches(host, epoch) {
                return Err(Reason::Foreign);
            }
            c.request_digest = Some(pf1(frame)?);
            c.generation = Some(Generation::new(g)?);
            c.request_ref = Some(Identity::new(reference)?);
            c.rpc = Some(scalar(frame.get("id").ok_or(Reason::Shape)?)?);
            if frame["method"] != "turn/start" {
                return Err(Reason::Shape);
            }
            let p = frame["params"].as_object().ok_or(Reason::Shape)?;
            if p.len() != 2 || !p.contains_key("threadId") || !p.contains_key("input") {
                return Err(Reason::Shape);
            }
            c.thread = Some(ident(&p["threadId"])?);
            let a = p["input"]
                .as_array()
                .filter(|a| a.len() == 1)
                .ok_or(Reason::Shape)?;
            let t = a[0].as_object().ok_or(Reason::Shape)?;
            if t.len() != 3
                || t.get("type").and_then(Value::as_str) != Some("text")
                || t.get("text_elements")
                    .and_then(Value::as_array)
                    .is_none_or(|a| !a.is_empty())
            {
                return Err(Reason::Shape);
            }
            c.request_text = Some(text(t.get("text").ok_or(Reason::Shape)?)?);
            Ok(())
        })();
        if let Err(r) = result {
            c.refuse(r)
        }
        c
    }
    fn refuse(&mut self, r: Reason) {
        if !matches!(self.standing, Standing::Refused(_)) {
            self.standing = Standing::Refused(r);
        }
    }
    fn current(&self, g: &Value, epoch: u64) -> bool {
        self.epoch == epoch && self.generation.as_ref().is_some_and(|x| x.matches(g))
    }
    fn selected(&self, reference: &str) -> bool {
        self.request_ref
            .as_ref()
            .is_some_and(|x| x.matches(reference))
    }
    fn refresh(&mut self) {
        if !matches!(self.standing, Standing::Refused(_)) {
            self.standing = if self.written
                && self.cut.is_some()
                && self.response.is_some()
                && self.item.is_some()
                && self.terminal.is_some()
            {
                Standing::ConsistentThroughReceipt(self.receipt, self.revision)
            } else {
                Standing::Pending
            };
        }
    }
    pub(super) fn prewrite(
        &mut self,
        g: &Value,
        epoch: u64,
        reference: &str,
        pipe: (u64, (u64, u64)),
        receipt: u64,
    ) {
        if !self.selected(reference) {
            return;
        }
        if !self.current(g, epoch) || self.pipe != Some(pipe) {
            self.refuse(Reason::Foreign);
            return;
        }
        if self.cut.is_some() {
            self.refuse(Reason::Conflict);
            return;
        }
        self.cut = Some(receipt);
    }
    pub(super) fn settle(
        &mut self,
        g: &Value,
        epoch: u64,
        reference: &str,
        pipe: Option<(u64, (u64, u64))>,
        written: bool,
    ) {
        if !self.selected(reference) {
            return;
        }
        if !self.current(g, epoch) || self.pipe != pipe {
            self.refuse(Reason::Foreign)
        } else if self.cut.is_none() {
            self.refuse(Reason::NoAttempt)
        } else if !written {
            self.refuse(Reason::Write)
        } else {
            self.written = true;
        }
        self.refresh();
    }
    fn candidate(&mut self, turn: Identity) -> Result<(), Reason> {
        if let Some(first) = &self.turn {
            if *first != turn {
                return Err(Reason::Conflict);
            }
        } else {
            self.turn = Some(turn)
        }
        Ok(())
    }
    pub(super) fn observe(
        &mut self,
        g: &Value,
        epoch: u64,
        pipe_epoch: u64,
        position: u64,
        frame: &Value,
    ) {
        if matches!(self.standing, Standing::Refused(_)) || !self.current(g, epoch) {
            return;
        }
        if self.pipe.is_none_or(|(e, _)| e != pipe_epoch) {
            self.refuse(Reason::Foreign);
            return;
        }
        // Match Host's existing protocol-class admission. A projected diagnostic
        // marker is not a response/notification even if lookalike fields exist.
        if !frame.is_object() || frame.get("observation").is_some() {
            return;
        }
        let response = frame.get("method").is_none()
            && (frame.get("result").is_some() || frame.get("error").is_some())
            && frame
                .get("id")
                .and_then(|id| scalar(id).ok())
                .is_some_and(|id| Some(id) == self.rpc);
        let method = frame["method"].as_str();
        let notification = frame.get("id").is_none()
            && matches!(method, Some("item/completed" | "turn/completed"))
            && frame["params"]["threadId"]
                .as_str()
                .is_some_and(|t| self.thread.as_ref().is_some_and(|x| x.matches(t)));
        if !response && !notification {
            return;
        }
        if self.cut.is_none_or(|cut| position <= cut) {
            self.refuse(Reason::NoAttempt);
            return;
        }
        let result = (|| {
            let digest = pf1(frame)?;
            let duplicate = if response {
                self.response == Some(digest)
            } else if method == Some("item/completed") {
                self.item.as_ref().is_some_and(|(_, d, _)| *d == digest)
            } else {
                self.terminal == Some(digest)
            };
            if duplicate {
                return Ok(false);
            }
            if response {
                if frame.get("method").is_some() || frame.get("error").is_some() {
                    return Err(Reason::Conflict);
                }
                let turn = &frame["result"]["turn"];
                if !frame["result"].is_object()
                    || !turn.is_object()
                    || !turn["items"].is_array()
                    || !matches!(
                        turn["status"].as_str(),
                        Some("inProgress" | "completed" | "interrupted" | "failed")
                    )
                {
                    return Err(Reason::Shape);
                }
                self.candidate(ident(&turn["id"])?)?;
                if matches!(turn["status"].as_str(), Some("failed" | "interrupted")) {
                    return Err(Reason::Conflict);
                }
                if self.response.is_some_and(|d| d != digest) {
                    return Err(Reason::Conflict);
                }
                self.response = Some(digest);
            } else if method == Some("item/completed") {
                let p = &frame["params"];
                let item = &p["item"];
                self.candidate(ident(&p["turnId"])?)?;
                if !p["completedAtMs"].is_i64() && !p["completedAtMs"].is_u64() {
                    return Err(Reason::Shape);
                }
                if item["type"] != "agentMessage" || item["phase"] != "final_answer" {
                    return Err(Reason::Shape);
                }
                let id = ident(&item["id"])?;
                let txt = text(&item["text"])?;
                if self
                    .item
                    .as_ref()
                    .is_some_and(|(i, d, _)| *i != id || *d != digest)
                {
                    return Err(Reason::Conflict);
                }
                if self.item.is_none() {
                    self.item = Some((id, digest, txt));
                }
            } else {
                let turn = &frame["params"]["turn"];
                self.candidate(ident(&turn["id"])?)?;
                if turn["status"] != "completed"
                    || !turn["items"].is_array()
                    || !turn.get("error").is_none_or(Value::is_null)
                {
                    return Err(Reason::Shape);
                }
                if self.terminal.is_some_and(|d| d != digest) {
                    return Err(Reason::Conflict);
                }
                self.terminal = Some(digest);
            }
            Ok(true)
        })();
        let changed = match result {
            Ok(changed) => changed,
            Err(r) => {
                self.refuse(r);
                return;
            }
        };
        self.receipt = position;
        if !changed {
            self.refresh();
            return;
        }
        match self.revision.checked_add(1) {
            Some(n) => self.revision = n,
            None => self.refuse(Reason::Exhausted),
        }
        self.refresh();
    }
    pub(super) fn retire(&mut self) {
        self.refuse(Reason::Closed)
    }
    #[cfg(test)]
    pub(super) fn readout(&self) -> (Standing, &'static str, usize) {
        (
            self.standing,
            "nativeSchemaValidation=not-performed-by-core",
            std::mem::size_of::<Self>(),
        )
    }
}

pub(super) const RETAINED: usize = 8192;
pub(super) const SCRATCH: usize = 65536;
pub(super) const INCREMENTAL: usize = 131072;
pub(super) const SORT_SCRATCH: usize =
    (DEPTH + 1) * std::mem::size_of::<[Option<(&str, &Value)>; WIDTH]>();
pub(super) const fn within_budget(retained: usize, scratch: usize, total: usize) -> bool {
    retained <= RETAINED && scratch <= SCRATCH && total <= INCREMENTAL
}
const _: () = assert!(within_budget(
    std::mem::size_of::<Core>(),
    SORT_SCRATCH + 4096,
    RETAINED + SCRATCH + 4096
));
const _: () = assert!(std::mem::size_of::<Core>() <= RETAINED);
const _: () = assert!(SORT_SCRATCH + 4096 <= SCRATCH);
const _: () = assert!(RETAINED + SCRATCH + 4096 <= INCREMENTAL);
