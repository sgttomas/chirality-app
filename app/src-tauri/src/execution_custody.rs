//! Pointer-only execution custody owned by Host's admitted source path.
//! No native payload, external-operation inference or live capability is retained.
//!
//! Recovery after a restart (RECOVERY §3.2 CV-11…CV-15, CV-19, CV-22): a
//! conversation whose generation closed, or that an earlier App session left
//! unsettled, is read again from Codex history once its own home's next
//! generation is ready. The Host sends the reads; this keeps the states, the
//! `observation_recovered` / `turn_outcome` events and the ledger rows.
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use crate::recovery::{generation_from_ref, generation_ref};

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
    /// The ready generation of the last recovery attempt, their count, the
    /// person's retry (CV-15) and why the last read failed (CV-14).
    attempt: Option<String>,
    attempts: u64,
    retry: bool,
    reason: Option<String>,
    /// A recovery state not yet queued as a ledger row.
    dirty: bool,
}
#[derive(Default)]
pub(super) struct ExecutionCustody {
    conversations: BTreeMap<(String, String), Conversation>,
    closed: BTreeSet<String>,
    events: Vec<Value>,
    limits: Vec<String>,
    /// The ready generation earlier sessions' rows were last adopted for.
    adopted_for: Option<String>,
}
/// One conversation to read in a ready generation: its custody key (the
/// generation it was last loaded in, and the thread) and the turn last seen
/// live there.
pub(super) struct RecoveryTarget { pub(super) key: (String, String), pub(super) turn: Option<String> }
/// A lost turn's stop request, for `turn_outcome` (cause and identity).
pub(super) struct RecoveredStop { pub(super) cause: String, pub(super) id: String }
/// CV-19's unsettled states.
const UNSETTLED: [&str; 6] = ["turn-live", "interrupt-pending", "observation-lost", "recovery-pending", "recovering", "unavailable"];
fn loss_cause(cause: &str) -> Option<&'static str> {
    ["supplier-exit", "supplier-stop", "app-quit", "system-termination", "app-ended-without-record"].into_iter().find(|c| *c == cause)
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
    pub(super) fn rows(&mut self,generation:&Value,history:crate::recovery::History<'_>)->Vec<Value> {
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
        // CV-22: the supplier ended during recovery; the reads resume at the next ready.
        for row in self.conversations.values_mut().filter(|r|r.state=="recovering"&&r.attempt.as_deref()==Some(g.as_str())) {
            row.state="recovery-pending";row.at=at.into();row.dirty=true;
        }
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
        // RECOVERY §3.5 RQ-04 and RQ-05 at this generation's close: each entry
        // still outstanding ended unanswered, and each written reply whose
        // acknowledgment was never observed (§8.2 `request_ended_unanswered`,
        // `acknowledgment_not_observed`). The entry is cited by reference only.
        for r in requests.iter().filter(|r| r["generation"] == *generation) {
            let (Some(method), Ok(identity)) = (r["method"].as_str(), serde_json::to_string(&r["requestId"])) else { continue };
            let mut entry = json!({"generation":g,"requestIdentity":identity,"method":method});
            if let Some(thread) = r["nativeParameters"]["threadId"].as_str().filter(|s| !s.is_empty()) {
                let mut subject = json!({"threadId":thread});
                for k in ["turnId", "itemId"] {
                    if let Some(v) = r["nativeParameters"][k].as_str().filter(|s| !s.is_empty()) { subject[k] = json!(v); }
                }
                entry["subject"] = subject;
            }
            let origin = r["settlement"]["origin"].as_str().unwrap_or_default();
            let written = matches!(r["state"].as_str(), Some("answered" | "declined")) || (r["state"] == "errored" && r["laterProtocolError"] == true);
            if r["state"] == "outstanding" {
                self.events.push(json!({"kind":"request_ended_unanswered","eventId":format!("cev:rq04:{g}:{identity}"),"appSession":generation["appSession"],"at":at,"standing":"App-observed","entry":entry,"context":cause}));
            } else if written && r["replyWriteResult"] == "written" && !r["acknowledgment"].is_object()
                && !self.events.iter().any(|e| e["eventId"] == format!("cev:rq05:{g}:{identity}"))
                && (origin == "person-via-interaction" || origin == "app-explicit-error" || origin.strip_prefix("app-rule:").is_some_and(|rule| !rule.is_empty())) {
                self.events.push(json!({"kind":"acknowledgment_not_observed","eventId":format!("cev:rq05:{g}:{identity}"),"appSession":generation["appSession"],"at":at,"standing":"App-observed","entry":entry,"settlementOrigin":origin,"context":cause}));
            }
        }
    }
    /// CV-19: conversations an earlier App session left unsettled in this
    /// physical home, from their latest ledger rows, held recovery-pending
    /// until this home's process is ready. Each is adopted once.
    pub(super) fn adopt(&mut self,session:&str,generation:&Value,rows:crate::recovery::History<'_>) {
        let Ok(current)=generation_ref(generation) else{return;};
        if self.adopted_for.as_deref()==Some(current.as_str()) {return;}
        self.adopted_for=Some(current);
        for row in crate::recovery::latest_execution_rows(rows) {
            let (Some(reference),Some(thread))=(row["lastLoadedGeneration"].as_str(),row["threadId"].as_str()) else{continue;};
            let Ok(source)=generation_from_ref(reference) else{continue;};
            if source["appSession"]==session||source["home"]!=generation["home"]||self.conversations.contains_key(&(reference.into(),thread.into())) {continue;}
            let execution=&row["lastObservedExecution"];
            if !execution["state"].as_str().is_some_and(|s|UNSETTLED.contains(&s)) {continue;}
            let turn=execution["liveTurn"].as_str().filter(|s|!s.is_empty()).map(str::to_owned);
            // Items with no persisted turn stay unknown (§7.2); they settle nothing.
            let open=execution["openItems"].as_array().into_iter().flatten().filter_map(|i|Some(((i["turnId"].as_str()?.to_owned(),i["itemId"].as_str()?.to_owned()),i["itemType"].as_str()?.to_owned()))).collect();
            self.closed.insert(reference.into());
            self.conversations.insert((reference.into(),thread.into()),Conversation{binding:Some(row.clone()),turn,open,state:"recovery-pending",at:execution["at"].as_str().unwrap_or_default().into(),cause:execution["lostCause"].as_str().and_then(loss_cause),..Default::default()});
        }
    }
    /// CV-11, CV-12, CV-15: the conversations of this physical home to read in
    /// its ready generation `generation`, each moved to recovering. A lost
    /// conversation is read at the next ready; an unavailable one at the next
    /// ready after the one that failed, or at once when the person retries.
    /// Only conversations with an App index (and so a home) are read.
    pub(super) fn begin_recovery(&mut self,generation:&Value,at:&str)->Vec<RecoveryTarget> {
        let Ok(current)=generation_ref(generation) else{return Vec::new();};
        let mut due=Vec::new();
        for ((key,thread),row) in self.conversations.iter_mut() {
            if !Self::due(&self.closed,key,row,&current,generation) {continue;}
            row.state="recovering";row.attempt=Some(current.clone());row.attempts+=1;row.retry=false;row.at=at.into();row.dirty=true;
            due.push(RecoveryTarget{key:(key.clone(),thread.clone()),turn:row.turn.clone()});
        }
        due
    }
    fn due(closed:&BTreeSet<String>,key:&str,row:&Conversation,current:&str,generation:&Value)->bool {
        if key==current||row.binding.is_none()||!closed.contains(key) {return false;}
        if generation_from_ref(key).map_or(true,|source|source["home"]!=generation["home"]) {return false;}
        match row.state {"observation-lost"|"recovery-pending"=>true,"unavailable"=>row.retry||row.attempt.as_deref()!=Some(current),_=>false}
    }
    /// Whether a recovery pass in the ready `generation` has anything to do:
    /// earlier sessions' rows not yet adopted for it, or a conversation due.
    /// Checked first, so an idle tick takes no App writer.
    pub(super) fn recovery_due(&self,generation:&Value)->bool {
        let Ok(current)=generation_ref(generation) else{return false;};
        self.adopted_for.as_deref()!=Some(current.as_str())||self.conversations.iter().any(|((key,_),row)|Self::due(&self.closed,key,row,&current,generation))
    }
    /// Whether this conversation's reads in `generation` are still its current
    /// attempt (CV-22 moves it back to recovery-pending).
    pub(super) fn recovering_in(&self,key:&(String,String),generation:&Value)->bool {
        let current=generation_ref(generation).ok();
        self.conversations.get(key).is_some_and(|r|r.state=="recovering"&&r.attempt==current)
    }
    /// CV-15 by the person: the unavailable conversations of `thread` are read
    /// again at the next recovery pass. Returns how many.
    pub(super) fn request_retry(&mut self,thread:&str)->usize {
        let mut n=0;
        for ((_,t),row) in self.conversations.iter_mut() {if t==thread&&row.state=="unavailable"{row.retry=true;n+=1;}}
        n
    }
    fn recovered_event(&self,key:&(String,String),generation:&Value,at:&str)->Option<Value> {
        let row=self.conversations.get(key)?;let home=row.binding.as_ref()?["home"].clone();let current=generation_ref(generation).ok()?;
        Some(json!({"kind":"observation_recovered","eventId":format!("cev:recovered:{current}:{}:{}:{}",key.0,key.1,row.attempts),"appSession":generation["appSession"],"at":at,"standing":"App-observed","threadId":key.1,"home":home,"generation":current,"via":"thread/read","turns":[]}))
    }
    /// CV-22 before the generation's close is observed: the process left
    /// `ready` during the reads; they resume at the next ready.
    pub(super) fn recovery_pending_again(&mut self,key:&(String,String),at:&str) {
        if let Some(row)=self.conversations.get_mut(key) {row.state="recovery-pending";row.at=at.into();row.dirty=true;}
    }
    /// CV-14: the reads failed or returned no result.
    pub(super) fn recovery_failed(&mut self,key:&(String,String),generation:&Value,reason:&str,at:&str) {
        let Some(mut event)=self.recovered_event(key,generation,at) else{return;};
        event["priorEvents"]=json!("unavailable");event["unavailableReason"]=json!(reason);
        let Some(row)=self.conversations.get_mut(key) else{return;};
        row.state="unavailable";row.reason=Some(reason.into());row.at=at.into();row.dirty=true;
        self.events.push(event);
    }
    /// CV-13: the reads completed. `status` is the turn last seen live as
    /// Codex history reports it (None: not in history). Emits
    /// `observation_recovered` *accessible* and, for that turn, `turn_outcome`:
    /// *recovered-from-supplier* for a final status, otherwise *unknown*.
    /// Its items seen open settle "not completed (turn ended)" only when
    /// history reports the turn ended (G-4).
    pub(super) fn recovered(&mut self,key:&(String,String),generation:&Value,status:Option<&str>,stop:Option<RecoveredStop>,at:&str) {
        let Some(mut event)=self.recovered_event(key,generation,at) else{return;};
        event["priorEvents"]=json!("accessible");
        let Some(row)=self.conversations.get_mut(key) else{return;};
        let mut outcome_event=None;
        if let Some(turn)=row.turn.clone() {
            let outcome=status.filter(|s|matches!(*s,"interrupted"|"completed"|"failed"));
            let reported=status.unwrap_or("no such turn");
            let reading=match (&stop,outcome) {
                (Some(stop),_)=>format!("{}; Codex reports: {reported}",crate::stop_records::label(&stop.cause,outcome.unwrap_or("unknown")).unwrap_or("stop requested")),
                (None,Some(s))=>match row.cause {
                    Some("app-quit")=>format!("observation lost at App quit; Codex reports: {s}"),
                    Some("supplier-stop")=>format!("observation lost when Codex was stopped; Codex reports: {s}"),
                    _=>format!("recovered from Codex: {s}"),
                },
                (None,None) if status==Some("inProgress")=>"outcome unknown (Codex history reports inProgress for a turn whose process ended)".into(),
                (None,None)=>"outcome unknown (turn not in Codex history)".into(),
            };
            let mut recovered=json!({"turnId":turn,"supplierStatus":status.unwrap_or("absent"),"appReading":reading});
            // G-5: the turn was live when the App stopped the process (closing its input).
            if matches!(row.cause,Some("supplier-stop"|"app-quit")) {recovered["historyNote"]=json!("graceful-stop abort note (Codex 0.158.0, observed OBS-2)");}
            event["turns"]=json!([recovered]);
            let mut outcome_json=json!({"kind":"turn_outcome","eventId":format!("cev:outcome:{}:{}:{turn}",key.0,key.1),"appSession":generation["appSession"],"at":at,"standing":"App-observed","threadId":key.1,"turnId":turn,"outcome":outcome.unwrap_or("unknown"),"source":if outcome.is_some(){"recovered-from-supplier"}else{"not-observed"}});
            if let Some(stop)=&stop {outcome_json["cause"]=json!(stop.cause);outcome_json["stopRequest"]=json!(stop.id);}
            let items:Vec<Value>=row.open.iter().filter(|((t,_),_)|*t==turn).map(|((_,id),kind)|json!({"itemId":id,"itemType":kind,"settled":"not completed (turn ended)"})).collect();
            if outcome.is_some()&&!items.is_empty() {outcome_json["itemsNotCompleted"]=json!(items);}
            outcome_event=Some(outcome_json);
        }
        // Settled: nothing of this generation remains to recover.
        row.state="indexed";row.turn=None;row.open.clear();row.cause=None;row.reason=None;row.at=at.into();row.dirty=true;
        self.events.push(event);
        if let Some(outcome)=outcome_event {self.events.push(outcome);}
    }
    /// Ledger rows for recovery states not yet queued. A conversation keeps
    /// its last loaded generation; recovering, unavailable and
    /// recovery-pending keep the lost turn and its items for a relaunch; an
    /// indexed row has nothing left to recover.
    pub(super) fn recovery_rows(&mut self,session:&str,history:crate::recovery::History<'_>)->Vec<Value> {
        let mut result=Vec::new();
        for ((key,thread),row) in self.conversations.iter_mut().filter(|(_,r)|r.dirty) {
            row.dirty=false;
            let Some(binding)=&row.binding else{continue;};
            let Some(base)=history.iter().rev().find(|e|e["kind"]=="conversation_index"&&e["threadId"]==*thread&&e["home"]==binding["home"]) else{continue;};
            let mut execution=json!({"state":row.state,"at":row.at});
            if row.state!="indexed" {
                if let Some(turn)=&row.turn {execution["liveTurn"]=json!(turn);}
                execution["openItems"]=json!(row.open.iter().map(|((turn,id),kind)|json!({"turnId":turn,"itemId":id,"itemType":kind})).collect::<Vec<_>>());
                if let Some(cause)=row.cause {execution["lostCause"]=json!(cause);}
            }
            let mut entry=base.clone();entry["session"]=json!(session);entry["at"]=json!(row.at);
            entry["lastLoadedGeneration"]=json!(key);entry["lastObservedExecution"]=execution;
            result.push(entry);
        }
        result
    }
    /// The custody events held in this App process, in the order they arose.
    pub(super) fn events(&self)->&[Value] {&self.events}
    pub(super) fn snapshot(&self)->Value {
        json!({"events":self.events,"limits":self.limits,"observations":self.conversations.iter().map(|((generation,thread),row)|json!({"generation":generation,"threadId":thread,"state":row.state,"liveTurn":row.turn,"openItems":row.open.iter().map(|((turn,id),kind)|json!({"turnId":turn,"itemId":id,"itemType":kind})).collect::<Vec<_>>(),"indexKnown":row.binding.is_some(),"recoveryAttempts":row.attempts,"unavailableReason":row.reason,"standing":"App-observed pointer state; persistence is reported separately"})).collect::<Vec<_>>()})
    }
}
