//! Pointer-only execution custody owned by Host's admitted source path.
//! No native payload, external-operation inference or live capability is retained.
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use crate::recovery::generation_ref;

#[derive(Default)]
struct Conversation {
    binding: Option<Value>,
    turn: Option<String>,
    terminal: BTreeSet<String>,
    open: BTreeMap<(String, String), String>,
    completed: BTreeSet<(String, String)>,
    state: &'static str,
    at: String,
    cause: Option<&'static str>,
}
#[derive(Default)]
pub(super) struct ExecutionCustody {
    conversations: BTreeMap<(String, String), Conversation>,
    closed: BTreeSet<String>,
    events: Vec<Value>,
    limits: Vec<String>,
}
impl ExecutionCustody {
    fn conversation(&mut self, generation: &Value, thread: &str) -> Option<&mut Conversation> {
        let key = generation_ref(generation).ok()?;
        if thread.is_empty() || self.closed.contains(&key) { return None; }
        Some(self.conversations.entry((key,thread.into())).or_insert_with(|| Conversation {state:"loaded-idle", ..Default::default()}))
    }
    /// Called only after the owning Host has admitted the actual context/index.
    pub(super) fn bind(&mut self, generation:&Value, thread:&str, index:&Value) {
        if let Some(row)=self.conversation(generation,thread) {row.binding=Some(index.clone());}
    }
    pub(super) fn turn(&mut self, generation:&Value, thread:&str, native:&Value, terminal_event:bool, at:&str) {
        let Some(id)=native["id"].as_str().filter(|s|!s.is_empty()) else{return;};
        let Some(status)=native["status"].as_str() else{return;};
        if !matches!(status,"inProgress"|"completed"|"interrupted"|"failed") {return;}
        if terminal_event&&status=="inProgress" {self.limits.push(format!("{} thread {thread} turn {id}: terminal event reports active status; terminal event governs custody, original source remains contradictory",generation_ref(generation).unwrap_or_default()));}
        let Some(row)=self.conversation(generation,thread) else{return;};
        if row.terminal.contains(id) {return;}
        if status=="inProgress"&&!terminal_event {
            // Native turn lifecycle, not a model/renderer-selected target.
            row.turn=Some(id.into());row.state="turn-live";
        } else {
            row.terminal.insert(id.into());
            row.open.retain(|(turn,_),_|turn!=id);
            if row.turn.as_deref()==Some(id) {row.turn=None;row.state="loaded-idle";}
        }
        row.at=at.into();
    }
    pub(super) fn item(&mut self,generation:&Value,params:&Value,completed:bool,at:&str) {
        let (Some(thread),Some(turn),Some(id),Some(kind))=(params["threadId"].as_str(),params["turnId"].as_str(),params["item"]["id"].as_str(),params["item"]["type"].as_str()) else{return;};
        if [thread,turn,id,kind].iter().any(|s|s.is_empty()) {return;}
        let Some(row)=self.conversation(generation,thread) else{return;};
        if row.terminal.contains(turn) {return;}
        let key=(turn.to_string(),id.to_string());
        if completed {row.open.remove(&key);row.completed.insert(key);}
        else if !row.completed.contains(&key) {row.open.insert(key,kind.into());}
        row.at=at.into();
    }
    /// Reconcile with the current owning index so concurrent tag additions survive.
    pub(super) fn rows(&mut self,generation:&Value,history:&[Value])->Vec<Value> {
        let Ok(g)=generation_ref(generation) else{return Vec::new();};
        let mut result=Vec::new();
        for ((key,thread),row) in self.conversations.iter_mut().filter(|((key,_),_)|key==&g) {
            let Some(binding)=&row.binding else{continue;};
            let Some(base)=history.iter().rev().find(|e|e["kind"]=="conversation_index"&&e["threadId"]==*thread&&e["home"]==binding["home"]) else{continue;};
            if row.at.is_empty(){continue;}
            let mut execution=json!({"state":row.state,"at":row.at});
            if let Some(turn)=&row.turn {
                execution["liveTurn"]=json!(turn);
            }
            // Ledger0.3 retains the actual known native association, independently
            // of lifecycle evidence. Item-only evidence never creates liveTurn.
            execution["openItems"]=json!(row.open.iter().map(|((turn,id),kind)|json!({"turnId":turn,"itemId":id,"itemType":kind})).collect::<Vec<_>>());
            if let Some(cause)=row.cause {execution["lostCause"]=json!(cause);}
            // Timestamp alone never creates another durable observation.
            let mut old=base["lastObservedExecution"].clone();let mut new=execution.clone();
            old.as_object_mut().map(|o|o.remove("at"));new.as_object_mut().map(|o|o.remove("at"));
            if old==new&&base["lastLoadedGeneration"]==*key {continue;}
            let mut entry=base.clone();entry["session"]=generation["appSession"].clone();entry["at"]=json!(row.at);
            entry["lastLoadedGeneration"]=json!(key);entry["lastObservedExecution"]=execution;
            result.push(entry);
        }
        result
    }
    pub(super) fn close(&mut self,generation:&Value,cause:&'static str,requests:&[Value],at:&str) {
        let Ok(g)=generation_ref(generation) else{return;};
        if !self.closed.insert(g.clone()){return;}
        let mut homes:BTreeMap<String,Vec<String>>=BTreeMap::new();
        for ((key,thread),row) in self.conversations.iter_mut().filter(|((key,_),_)|key==&g) {
            let _=key;
            row.state="observation-lost";row.cause=Some(cause);row.at=at.into();
            if let Some(home)=row.binding.as_ref().and_then(|b|b["home"].as_str()) {homes.entry(home.into()).or_default().push(thread.clone());}
            else {self.limits.push(format!("{g} thread {thread}: owning App index/home absent; loss references are memory-only, cold lookup unavailable"));}
        }
        for (home,threads) in homes {
            let mut turns=Vec::new();let mut items=Vec::new();
            for thread in &threads {
                let row=&self.conversations[&(g.clone(),thread.clone())];
                if let Some(turn)=&row.turn {turns.push(json!({"threadId":thread,"turnId":turn}));}
                for ((turn,id),kind) in &row.open {
                    items.push(json!({"threadId":thread,"turnId":turn,"itemId":id,"itemType":kind,"lastObservedStatus":"inProgress"}));
                }
            }
            let outstanding=requests.iter().filter(|r|r["generation"]==*generation&&r["state"]=="outstanding"&&r["nativeParameters"]["threadId"].as_str().is_some_and(|t|threads.iter().any(|s|s==t))).filter_map(|r|{
                let method=r["method"].as_str()?;let id=r.get("requestId")?;
                let mut subject=json!({"threadId":r["nativeParameters"]["threadId"]});
                for k in ["turnId","itemId"] {if let Some(v)=r["nativeParameters"][k].as_str().filter(|s|!s.is_empty()){subject[k]=json!(v);}}
                Some(json!({"generation":g,"requestIdentity":id.to_string(),"method":method,"subject":subject}))
            }).collect::<Vec<_>>();
            self.events.push(json!({"kind":"observation_lost","eventId":format!("cev:{}:{}",g,home),"appSession":generation["appSession"],"at":at,"standing":"App-observed","home":home,"generation":g,"cause":cause,"conversations":threads,"liveTurns":turns,"inFlightItems":items,"outstandingEntries":outstanding}));
        }
    }
    pub(super) fn snapshot(&self)->Value {
        json!({"events":self.events,"limits":self.limits,"observations":self.conversations.iter().map(|((generation,thread),row)|json!({"generation":generation,"threadId":thread,"state":row.state,"liveTurn":row.turn,"openItems":row.open.iter().map(|((turn,id),kind)|json!({"turnId":turn,"itemId":id,"itemType":kind})).collect::<Vec<_>>(),"indexKnown":row.binding.is_some(),"standing":"App-observed pointer state; persistence is reported separately"})).collect::<Vec<_>>()})
    }
}
