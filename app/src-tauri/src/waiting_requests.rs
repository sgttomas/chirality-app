//! Local register metadata for WI-1/WI-3. No supplier reads or answer authority.
use crate::{home_resources::HomeClass, runtime_session::HomeRouter};
use serde_json::{json, Value};

fn groups(class: HomeClass, snapshot: &Value) -> Vec<Value> {
    let generation = &snapshot["generation"];
    if snapshot["state"] != "ready" || crate::recovery::generation_ref(generation).is_err() { return vec![]; }
    let mut groups: Vec<Value> = Vec::new();
    for request in snapshot["serverRequests"].as_array().into_iter().flatten() {
        if request["generation"] != *generation || request["closedGeneration"] == true || request["state"] != "outstanding"
            || request["classification"] != "known-answerable" || request["originClass"] == "named-service" { continue; }
        let params = &request["nativeParameters"];
        let thread = params.get("threadId").filter(|v| !v.is_null()).or_else(||params.get("conversationId"))
            .and_then(Value::as_str).filter(|s| !s.is_empty()).map_or(Value::Null, |s|json!(s));
        if let Some(group) = groups.iter_mut().find(|g|g["threadId"] == thread) {
            group["count"] = json!(group["count"].as_u64().unwrap() + 1);
        } else {
            groups.push(json!({"modeHomeClass":class.as_str(),"generation":generation,"threadId":thread,"count":1}));
        }
    }
    groups
}

pub(crate) fn overview(router: &HomeRouter) -> Value {
    let mut waiting = Vec::new(); let mut sources = Vec::new();
    for home in router.entries() {
        let snapshot = home.host.snapshot();
        let groups = groups(home.class(), &snapshot);
        sources.push(json!({"modeHomeClass":home.class().as_str(),"generation":snapshot["generation"],"state":snapshot["state"],
            "count":groups.iter().filter_map(|g|g["count"].as_u64()).sum::<u64>()}));
        waiting.extend(groups);
    }
    json!({"groups":waiting,"sources":sources,"coverage":"Known answerable requests awaiting the person in ready, current local registers of all configured App conversation homes. Sequential snapshots, not an atomic cross-home observation; counts can change before opening. No supplier read."})
}

pub(crate) fn open(router: &mut HomeRouter, mode: &str, generation: &Value, thread: &Value) -> Result<Value, String> {
    crate::recovery::generation_ref(generation)?;
    if !thread.is_null() && !thread.as_str().is_some_and(|s|!s.is_empty()) { return Err("Waiting conversation must be the original named thread or null".into()); }
    let class = match mode { "account"=>HomeClass::Account,"api-key"=>HomeClass::ApiKey,_=>return Err("Unknown waiting-request home class; no fallback".into()) };
    let home = router.entry(class)?;
    let snapshot = home.host.snapshot();
    if snapshot["generation"] != *generation || snapshot["state"] != "ready" {
        return Err("Original waiting-request source is no longer current and ready; refresh the overview".into());
    }
    if !groups(class, &snapshot).iter().any(|g|g["threadId"] == *thread) {
        return Err("Original conversation has no current waiting request group; refresh the overview".into());
    }
    let loaded = thread.is_string() && snapshot["threads"].as_array().into_iter().flatten().any(|t|t["generation"] == *generation && t["threadId"] == *thread);
    router.activate(class)?;
    Ok(json!({"modeHomeClass":mode,"generation":generation,"threadId":thread,"threadLoaded":loaded,
        "standing":"Explicit navigation to the original current waiting-request source only; no answer, resume or send"}))
}
