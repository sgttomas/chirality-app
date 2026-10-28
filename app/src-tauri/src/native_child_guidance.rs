//! Memory-only association of live native child identities with an original
//! App parent carrier. A quoted record or native role name alone grants none.
use crate::{
    hosting::{Host, NativeChildStart, SourceRequest},
    role_lifecycle::RoleBindings,
    role_supply::Composition,
};
use serde_json::{json, Value};
use std::collections::BTreeSet;
struct Pending {
    event: NativeChildStart,
    source: Option<SourceRequest>,
    parent_supply: Option<String>,
    id: String,
    reading: Value,
    composition: Option<Composition>,
    recorded: bool,
    root: Value,
}
#[derive(Default)]
pub(crate) struct ChildGuidance {
    pending: Vec<Pending>,
    seen: BTreeSet<String>,
    limit_events: Vec<Value>,
    limit_seen: BTreeSet<String>,
}
impl ChildGuidance {
    pub(crate) fn reconcile(
        &mut self,
        host: &Host,
        roles: &RoleBindings,
        log: Option<&Result<std::sync::Arc<crate::role_observations::RoleLog>, String>>,
    ) {
        let events = host.observed_child_starts();
        for event in events.iter().cloned() {
            if self.seen.contains(&event.key()) {
                continue;
            }
            let duplicate = self.pending.iter().any(|p| {
                p.event.generation() == event.generation() && p.event.child() == event.child()
            });
            let home = event.generation()["home"].as_str().unwrap_or("");
            let parent = roles.get(home, event.parent());
            let allowed = !duplicate
                && event.child() != event.parent()
                && roles.get(home, event.child()).is_none()
                && parent.is_some_and(|p| {
                    host.parent_child_carrier_current(&event, p)
                        && !p.supplied_children().is_empty()
                });
            let parent_supply = parent.map(|p| p.supply_ref().to_owned());
            let id = match crate::util::opaque_id("sup:child:") {
                Ok(id) => id,
                Err(_) => continue,
            };
            self.seen.insert(event.key());
            let (source, reading) = if allowed {
                match host.child_metadata_dispatch(&event) {
                    Ok(source) => (
                        Some(source),
                        json!({"standing":"unknown","reason":"native child metadata pending"}),
                    ),
                    Err(_) => (
                        None,
                        json!({"standing":"unknown","reason":"native child metadata dispatch unavailable"}),
                    ),
                }
            } else {
                (
                    None,
                    json!({"standing":"unknown","reason":"no supported original App parent carrier; self/ancestor/duplicate/fork/resume references grant no supply"}),
                )
            };
            let root = event.evidence();
            self.pending.push(Pending {
                event,
                source,
                parent_supply,
                id,
                reading,
                composition: None,
                recorded: false,
                root,
            });
        }
        host.acknowledge_child_starts(
            &events
                .into_iter()
                .filter(|event| self.seen.contains(&event.key()))
                .collect::<Vec<_>>(),
        );
        for pending in &mut self.pending {
            if pending.reading["standing"] != "unknown" || pending.reading["terminal"] == true {
                continue;
            }
            let Some(source) = &pending.source else {
                pending.reading["terminal"] = json!(true);
                continue;
            };
            let result = host
                .child_metadata_finish(&pending.event, source)
                .and_then(|thread| {
                    let Some(thread) = thread else {
                        return Ok(None);
                    };
                    let home = pending.event.generation()["home"].as_str().unwrap_or("");
                    let parent = roles
                        .get(home, pending.event.parent())
                        .ok_or("original parent unavailable")?;
                    if !host.parent_child_carrier_current(&pending.event, parent)
                        || pending.parent_supply.as_deref() != Some(parent.supply_ref())
                    {
                        return Err("original parent carrier no longer available".into());
                    }
                    let child = parent
                        .supplied_children()
                        .iter()
                        .find(|c| thread["agentRole"] == c.role.name())
                        .ok_or("native role was not supplied by this parent")?;
                    child.recheck()?;
                    if !host.parent_child_carrier_current(&pending.event, parent) {
                        return Err("original parent carrier ended during inspection".into());
                    }
                    Ok(Some((thread, child.clone())))
                });
            match result {
                Ok(None) => {}
                Ok(Some((thread, child))) => {
                    let account =
                        crate::conversation_roles::frozen_limit_account(&child.composition).ok();
                    pending.reading = json!({"standing":"app-observed-child-supply","role":child.role,"parentSupplyRef":pending.parent_supply,"composition":crate::role_supply::content(child.composition.text.as_bytes()),"file":crate::role_supply::content(&child.envelope),"native":pending.event.evidence(),"metadataRequestRef":source.request_ref(),"agentRole":thread["agentRole"],"parentThreadId":thread["parentThreadId"],"limitAccount":account,"providerAdoption":"unknown","currentRoleAuthorityRestored":false,"basis":"original live parent carrier + completed native child event + correlated child metadata; no provider-uptake or enforcement claim"});
                    pending.composition = Some(*child.composition);
                }
                Err(_) => {
                    pending.reading = json!({"standing":"unknown","terminal":true,"reason":"native child/source/role/carrier identity not established"});
                }
            }
        }
        // Descendant events may precede the first child's metadata reply.
        // Re-evaluate retained original events after association, once per item.
        let limits = self
            .pending
            .iter()
            .filter_map(|pending| {
                let event = &pending.event;
                let key = json!([
                    event.generation(),
                    event.parent(),
                    event.evidence()["turnId"],
                    event.evidence()["itemId"]
                ])
                .to_string();
                if self.limit_seen.contains(&key) {
                    return None;
                }
                let task = self.pending.iter().find(|p| {
                    p.event.child() == event.parent()
                        && p.event.generation()["home"] == event.generation()["home"]
                        && p.event.generation()["appSession"] == event.generation()["appSession"]
                        && p.reading["standing"] == "app-observed-child-supply"
                        && p.reading["role"] == "TASK"
                })?;
                Some((
                    key,
                    event.clone(),
                    task.root.clone(),
                    task.reading.clone(),
                    task.parent_supply.clone(),
                    task.id.clone(),
                ))
            })
            .collect::<Vec<_>>();
        for (key, event, root, task_reading, task_parent_supply, task_id) in limits {
            if !self.limit_seen.insert(key) {
                continue;
            }
            let mut limit = event.evidence();
            limit["observedAt"] = json!(crate::util::now_rfc3339());
            limit["basis"] = json!("comparison-with-original-child-guidance");
            limit["limit"] = json!("L-TASK-1");
            limit["originalRole"] = json!("TASK");
            limit["actionGeneration"] = event.generation().clone();
            limit["originalAssociation"] = json!({"associationId":task_id,"generation":task_reading["native"]["generation"],"parentSupplyRef":task_parent_supply,"role":"TASK"});
            limit["comparisonStanding"]=json!("Original App guidance compared with a later native action; no renewed supply, provider uptake, RoleBinding, CCE or current-source authority");
            limit["root"] = root;
            let account = task_reading["limitAccount"]["limits"]
                .as_array()
                .into_iter()
                .flatten()
                .find(|l| l["limitId"] == "L-TASK-1");
            limit["standing"] = account
                .map(|a| a["standing"].clone())
                .unwrap_or(json!("unknown"));
            limit["parentSupplyRef"] = task_reading["parentSupplyRef"].clone();
            limit["presentedAs"] = json!(if limit["standing"] == "unknown" {
                "TASK made a native delegation; whether its supplied guidance stated a prohibition is unknown"
            } else {
                "TASK made a native delegation; its prohibition is stated, not enforced"
            });
            let request = json!({"home":event.generation()["home"],"generation":event.generation(),"requestIdentity":null,"requestRef":null,"method":null,"writeResult":"not-attempted","outcome":"native-notification-observed","sourceCurrent":null});
            let row=crate::util::opaque_id("sup:limit:").and_then(|id|crate::role_observations::row(&id,"native-task-delegation",Some(event.parent()),request,json!({"role":"unknown","preselected":null,"roleSet":null}),"task-delegation-observed",None,json!({"instructionSources":null,"agentRole":null,"forkedFromId":null}),json!({"originalParentSupplyRef":task_parent_supply,"nativeChildEvent":event.evidence(),"originalTaskAssociation":limit["originalAssociation"],"standing":limit["standing"],"basis":"comparison-with-original-child-guidance"}),None));
            limit["roleSupplyRecord"]=row.and_then(|r|match log{Some(Ok(log))=>log.append(r,None),_=>Err("App role history unavailable".into())}).unwrap_or_else(|_|json!({"state":"not-confirmed","limit":"TASK delegation history unavailable; live native event remains observed"}));
            self.limit_events.push(limit);
        }
        for pending in &mut self.pending {
            if pending.recorded || pending.reading["standing"] != "app-observed-child-supply" {
                continue;
            }
            pending.recorded = true;
            let Some(source) = &pending.source else {
                continue;
            };
            let Ok(status) = host.source_request_status(source) else {
                continue;
            };
            let row = crate::role_observations::row(
                &pending.id,
                "native-child-association",
                Some(pending.event.child()),
                crate::role_observations::request(&status),
                json!({"role":pending.reading["role"],"preselected":null,"roleSet":pending.composition.as_ref().map(Composition::role_set_identity)}),
                "native-child-associated",
                pending.composition.as_ref().map(|c| c.carried.clone()),
                crate::role_observations::reported(&status),
                json!({"parentSupplyRef":pending.parent_supply,"nativeChildEvent":pending.event.evidence(),"supplyCarrier":"parent's original native role configuration; metadata read carries no instructions"}),
                None,
            );
            let recorded = row.and_then(|row| match log {
                Some(Ok(log)) => log.append(row, pending.composition.as_ref()),
                _ => Err("App role history unavailable".into()),
            });
            pending.reading["roleSupplyRecord"]=recorded.unwrap_or_else(|_|json!({"state":"not-confirmed","limit":"Child association history unavailable; native observation retained in memory"}));
        }
    }
    pub(crate) fn for_thread(&self, home: &str, thread: &str) -> Value {
        self.pending
            .iter()
            .find(|p| {
                p.event.generation()["home"] == home
                    && p.event.child() == thread
                    && p.reading["standing"] == "app-observed-child-supply"
            })
            .map(|p| p.reading.clone())
            .unwrap_or(Value::Null)
    }
    pub(crate) fn snapshot(&self) -> Value {
        json!(self
            .pending
            .iter()
            .map(|p| json!({"native":p.event.evidence(),"guidance":p.reading}))
            .collect::<Vec<_>>())
    }
    pub(crate) fn limits(&self) -> Value {
        json!(self.limit_events)
    }
}

/// Existing RS role_limit_observation bodies, admitted only where both the
/// original child-creation item and TASK delegation belong to this live run.
pub(crate) fn run_limit_bodies(
    view: &Value,
    home: &str,
    conversation: &str,
    start: crate::run_offers::RunStart,
    seen: &mut BTreeSet<String>,
) -> Vec<Value> {
    if view["home"] != home {
        return vec![];
    }
    let items = view["items"].as_array().map(Vec::as_slice).unwrap_or(&[]);
    let mut out = vec![];
    for limit in view["roleLimitObservations"]
        .as_array()
        .into_iter()
        .flatten()
    {
        if limit["generation"] != view["generation"]
            || limit["root"]["parentThreadId"] != conversation
            || limit["root"]["generation"] != view["generation"]
        {
            continue;
        }
        let matches = |item: &&Value, event: &Value| {
            item["standing"] == "live-observed"
                && item["displayState"] == "completed"
                && item["threadId"] == event["parentThreadId"]
                && item["turnId"] == event["turnId"]
                && item["native"]["id"] == event["itemId"]
                && item["native"]["type"] == "subAgentActivity"
                && item["native"]["kind"] == "started"
                && item["native"]["agentThreadId"] == event["threadId"]
        };
        let Some(root) = items.iter().find(|i| matches(i, &limit["root"])) else {
            continue;
        };
        if !root["observedOrder"]
            .as_u64()
            .is_some_and(|n| start.includes(n))
            || !items.iter().any(|i| {
                matches(&i, limit)
                    && i["observedOrder"]
                        .as_u64()
                        .is_some_and(|n| start.includes(n))
            })
        {
            continue;
        }
        let key = json!([
            limit["generation"],
            limit["parentThreadId"],
            limit["turnId"],
            limit["itemId"]
        ])
        .to_string();
        if !seen.insert(key.clone()) {
            continue;
        }
        out.push(json!({"limit":"L-TASK-1","roleInForce":"TASK","basis":"native-child-role-reported","standing":limit["standing"],"item":{"kind":"conversation item","ref":format!("native-item:{key}"),"resolutionAtWrite":"resolved"},"thread":limit["parentThreadId"],"observedAt":limit["observedAt"]}));
    }
    out
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn native_child_guidance_run_limit_body_requires_original_live_run_attribution() {
        let g = json!({"appSession":"s","home":"h","spawnCounter":1});
        let event = |parent: &str, child: &str, item: &str| json!({"generation":g,"parentThreadId":parent,"threadId":child,"turnId":format!("turn-{parent}"),"itemId":item});
        let root = event("parent", "task", "spawn-task");
        let mut limit = event("task", "grandchild", "spawn-grandchild");
        limit["root"] = root.clone();
        limit["standing"] = json!("stated-not-enforced");
        limit["observedAt"] = json!("original-time");
        let item = |event: &Value, order: u64| json!({"standing":"live-observed","displayState":"completed","threadId":event["parentThreadId"],"turnId":event["turnId"],"observedOrder":order,"native":{"id":event["itemId"],"type":"subAgentActivity","kind":"started","agentThreadId":event["threadId"]}});
        let mut view = json!({"home":"h","generation":g,"roleLimitObservations":[limit],"items":[item(&root,4),item(&event("task","grandchild","spawn-grandchild"),6)]});
        let mut seen = BTreeSet::new();
        let bodies = run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(3),
            &mut seen,
        );
        assert_eq!(bodies.len(), 1);
        assert_eq!(bodies[0]["observedAt"], "original-time");
        assert!(run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(3),
            &mut seen
        )
        .is_empty());
        assert!(run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(5),
            &mut BTreeSet::new()
        )
        .is_empty());
        view["items"][1]["observedOrder"] = json!(2);
        assert!(run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(3),
            &mut BTreeSet::new()
        )
        .is_empty());
        view["items"][1]
            .as_object_mut()
            .unwrap()
            .remove("observedOrder");
        assert!(run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(3),
            &mut BTreeSet::new()
        )
        .is_empty());
        view["items"][1]["observedOrder"] = json!(6);
        view["items"][1]["standing"] = json!("recovered-from-supplier");
        assert!(run_limit_bodies(
            &view,
            "h",
            "parent",
            crate::run_offers::RunStart::At(3),
            &mut BTreeSet::new()
        )
        .is_empty());
    }
}
