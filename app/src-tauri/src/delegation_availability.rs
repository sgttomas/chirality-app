//! Conservative delegation reading for Codex 0.169.0 (DEL-01-03).
//! App Agent 0's 2026-11-15 rule recognizes only the observed baseline and
//! disabled configurations. It does not reproduce supplier feature precedence.
//! A positive reading says tools are offered, never that a child will run.
use serde_json::{json, Value};

/// Bind the reading to this conversation, including its reported native source.
/// A root reading must never be reused for a descendant with the same model.
pub(crate) fn key(conversation: &Value) -> Value {
    json!({"generation":conversation["generation"],"threadId":conversation["threadId"],
        "model":conversation["model"],"modelProvider":conversation["modelProvider"],
        "cwd":conversation["cwd"],"threadSource":conversation["threadSource"]})
}

pub(crate) fn signals(conversation: &Value, model: Result<Value, String>, config: Result<Value, String>,
    requirements: Result<Value, String>, server: Result<Value, String>, capabilities: Result<Value, String>) -> Value {
    let mut limits = Vec::<String>::new();
    let mut notes = Vec::<String>::new();
    let root = matches!(conversation["threadSource"].as_str(), Some("appServer" | "cli" | "vscode" | "exec"));
    if !root {
        limits.push("the conversation is a descendant or its root source was not established; descendant depth is not read".into());
    }
    // The App deliberately omits 0.169.0's optional modelProvider parameter.
    // Its catalog therefore counts only for the matching server provider.
    match server {
        Ok(ref provider) if provider.is_string() && *provider == conversation["modelProvider"] => {},
        Ok(_) => limits.push("model/list uses the app-server default provider, which does not establish this conversation's catalogue".into()),
        Err(cause) => limits.push(format!("app-server provider not read: {cause}")),
    }
    let mut catalog_read = false;
    let version = match model {
        Ok(ref entry) if entry.is_object() => match entry.get("multiAgentVersion") {
            None | Some(Value::Null) => { catalog_read = true; Value::Null },
            Some(v) if v == "disabled" || v == "v1" || v == "v2" => { catalog_read = true; v.clone() },
            _ => { limits.push("model catalogue multiAgentVersion is unfamiliar".into()); Value::Null },
        },
        Ok(_) => { limits.push("the conversation's model was not in the catalogue".into()); Value::Null },
        Err(cause) => { limits.push(format!("model catalogue not read: {cause}")); Value::Null },
    };
    let (mut legacy_set, mut v2_set, mut agents_set) = (false, false, false);
    let mut effective_agents = Value::Null;
    let mut config_read = false;
    match config {
        Ok(ref result) if result["config"].is_object() && result["layers"].is_array() => {
            config_read = true;
            for layer in result["layers"].as_array().unwrap() {
                let Some(table) = layer["config"].as_object() else {
                    limits.push("a configuration layer is incomplete".into()); continue;
                };
                for name in ["features", "agents"] {
                    if table.get(name).is_some_and(|v| !v.is_object()) {
                        limits.push(format!("{name} in a configuration layer could not be read"));
                    }
                }
                legacy_set |= layer["config"]["features"].get("multi_agent").is_some();
                v2_set |= layer["config"]["features"].get("multi_agent_v2").is_some();
                agents_set |= layer["config"]["agents"].get("enabled").is_some();
            }
            let effective = &result["config"];
            // Typed effective config may serialize unset optional fields as null.
            legacy_set |= !effective["features"]["multi_agent"].is_null();
            v2_set |= !effective["features"]["multi_agent_v2"].is_null();
            agents_set |= !effective["agents"]["enabled"].is_null();
            effective_agents = effective["agents"]["enabled"].as_bool().map(Value::Bool).unwrap_or(Value::Null);
            for name in ["features", "agents"] {
                if !effective[name].is_null() && !effective[name].is_object() {
                    limits.push(format!("effective {name} could not be read"));
                }
            }
            if agents_set && !effective_agents.is_boolean() {
                limits.push("agents.enabled is set in a layer but its effective value is not established".into());
            }
        },
        Ok(_) => limits.push("config/read did not supply complete effective configuration and layers".into()),
        Err(cause) => limits.push(format!("config/read failed: {cause}")),
    }
    let mut requirements_read = false;
    match requirements {
        Ok(ref result) => match result.get("requirements") {
            Some(Value::Null) => requirements_read = true,
            Some(value) if value.is_object() => {
                requirements_read = true;
                match value.get("featureRequirements") {
                    None | Some(Value::Null) => {},
                    Some(features) if features.is_object() => {
                        for name in ["multi_agent", "multi_agent_v2", "collab", "agents.enabled"] {
                            if features.get(name).is_some() {
                                limits.push(format!("managed requirement {name} constrains delegation"));
                            }
                        }
                    },
                    _ => limits.push("managed feature requirements could not be read".into()),
                }
            },
            _ => limits.push("configRequirements/read did not supply its requirements reading".into()),
        },
        Err(cause) => limits.push(format!("configRequirements/read failed: {cause}")),
    }
    if v2_set { limits.push("features.multi_agent_v2 is set; native tool exposure is not established".into()); }
    if legacy_set { limits.push("features.multi_agent is set; the legacy setting alone does not establish delegation".into()); }
    if let Err(cause) = capabilities {
        notes.push(format!("modelProvider/capabilities/read failed ({cause}); provider capabilities do not decide delegation"));
    }
    // Retain only the named signals, not arbitrary config, catalogue or requirement content.
    json!({"rule":"codex-0.169.0-conservative", "root":root,"catalog_read":catalog_read,
        "model_multi_agent_version":version,"config_read":config_read,"requirements_read":requirements_read,
        "agents_set":agents_set,"effective_agents_enabled":effective_agents,
        "legacy_set":legacy_set,"v2_set":v2_set,"limits":limits,"notes":notes})
}

pub(crate) fn evaluate(signals: Option<&Value>) -> Value {
    let unknown = |reason: String| json!({"reading":"not established","reason":reason});
    let Some(s) = signals else { return unknown("delegation signals not read for this conversation".into()); };
    let mut result = if s["rule"] != "codex-0.169.0-conservative" || s["root"] != true
        || s["catalog_read"] != true || s["config_read"] != true || s["requirements_read"] != true {
        unknown("the root conversation, catalogue, configuration layers or requirements reading is not established".into())
    } else if s["limits"].as_array().is_none_or(|v| !v.is_empty()) {
        unknown(s["limits"].as_array().map(|v| v.iter().filter_map(Value::as_str).collect::<Vec<_>>().join("; "))
            .unwrap_or_else(|| "delegation reading is incomplete".into()))
    } else if s["legacy_set"] != false || s["v2_set"] != false {
        unknown("features.multi_agent or features.multi_agent_v2 is set or unread".into())
    } else if s["effective_agents_enabled"] == false {
        json!({"reading":"missing","reason":"agents.enabled is false with neither delegation feature set"})
    } else if s["model_multi_agent_version"] == "disabled" {
        json!({"reading":"missing","reason":"the model catalogue reports multiAgentVersion disabled with neither delegation feature set"})
    } else if s["agents_set"] == false && (s["model_multi_agent_version"].is_null()
        || s["model_multi_agent_version"] == "v1" || s["model_multi_agent_version"] == "v2") {
        json!({"reading":"present","reason":"Native tools are offered to this root conversation; this does not establish that a child will run or that capacity remains."})
    } else {
        unknown("agents.enabled is set; delegation is not established for that configuration".into())
    };
    if result["reading"] == "not established" {
        if let Some(limits) = s["limits"].as_array().filter(|v| !v.is_empty()) {
            result["reason"] = json!(limits.iter().filter_map(Value::as_str).collect::<Vec<_>>().join("; "));
        }
    }
    result["readAt"] = s["readAt"].clone();
    if let Some(notes) = s["notes"].as_array().filter(|v| !v.is_empty()) {
        result["note"] = json!(notes.iter().filter_map(Value::as_str).collect::<Vec<_>>().join("; "));
    }
    result
}

pub(crate) fn annotate_threads(threads: &mut Value, readings: &[Value]) {
    for thread in threads.as_array_mut().into_iter().flatten() {
        let wanted = key(thread);
        let found = readings.iter().rev().find(|r| r["key"] == wanted);
        thread["delegation"] = evaluate(found.map(|r| &r["signals"]));
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn conversation() -> Value { json!({"generation":{"home":"h"},"threadId":"t","threadSource":"appServer","model":"m","modelProvider":"p","cwd":"/w"}) }
    fn config(table: Value) -> Value { json!({"config":table,"layers":[{"config":table}],"origins":{}}) }
    fn read(version: Value, table: Value) -> Value {
        evaluate(Some(&signals(&conversation(), Ok(json!({"model":"m","multiAgentVersion":version})),
            Ok(config(table)), Ok(json!({"requirements":null})), Ok(json!("p")), Ok(json!({})))))
    }
    #[test]
    fn baseline_and_disabled_cases_and_their_limits() {
        for version in [Value::Null,json!("v1"),json!("v2")] {
            let result=read(version.clone(),json!({})); assert_eq!(result["reading"],"present");
            assert!(result["reason"].as_str().unwrap().contains("capacity"));
            assert_eq!(read(version,json!({"agents":{"enabled":false}}))["reading"],"missing");
        }
        assert_eq!(read(json!("disabled"),json!({}))["reading"],"missing");
        assert_eq!(read(json!("v1"),json!({"agents":{"enabled":true}}))["reading"],"not established");
    }
    #[test]
    fn every_explicit_feature_and_descendant_precedes_missing() {
        for version in [Value::Null,json!("disabled"),json!("v1"),json!("v2")] {
            for (name,values) in [("multi_agent",vec![json!(false),json!(true)]),
                ("multi_agent_v2",vec![json!(false),json!(true),json!({"enabled":false}),json!({"disable_native_tools":true})])] {
                for value in values {
                    let mut c=json!({"agents":{"enabled":false},"features":{}});c["features"][name]=value;
                    let result=read(version.clone(),c);assert_eq!(result["reading"],"not established");
                    assert!(result["reason"].as_str().unwrap().contains(name));
                }
            }
        }
        let mut child=conversation();child["threadSource"]=json!({"subAgent":{"thread_spawn":{"parent_thread_id":"t","depth":1}}});
        let result=evaluate(Some(&signals(&child,Ok(json!({"multiAgentVersion":"disabled"})),
            Ok(config(json!({"agents":{"enabled":false}}))),Ok(json!({"requirements":null})),Ok(json!("p")),Ok(json!({})))));
        assert_eq!(result["reading"],"not established"); assert!(result["reason"].as_str().unwrap().contains("descendant"));
    }
    #[test]
    fn partial_reads_managed_constraints_and_other_provider_are_not_missing() {
        let mk=|c,r,p|evaluate(Some(&signals(&conversation(),Ok(json!({"multiAgentVersion":"disabled"})),c,r,p,Ok(json!({})))));
        let complete=Ok(config(json!({})));let none=Ok(json!({"requirements":null}));
        for result in [mk(Err("silent".into()),none.clone(),Ok(json!("p"))),
            mk(Ok(json!({"config":{}})),none.clone(),Ok(json!("p"))),
            mk(complete.clone(),Err("silent".into()),Ok(json!("p"))),
            mk(complete.clone(),Ok(json!({})),Ok(json!("p"))),
            mk(complete.clone(),none.clone(),Ok(json!("other"))),
            mk(complete,Ok(json!({"requirements":{"featureRequirements":{"multi_agent":true}}})),Ok(json!("p")))] {
            assert_eq!(result["reading"],"not established","{result}");
        }
    }
    #[test]
    fn lower_layers_are_not_erased_and_arbitrary_text_is_not_kept() {
        let mut c=config(json!({"developer_instructions":"private text"}));
        c["layers"]=json!([{"config":{"features":{"multi_agent":false}}},{"config":{}}]);
        let s=signals(&conversation(),Ok(json!({"multiAgentVersion":"v1"})),Ok(c),Ok(json!({"requirements":null})),Ok(json!("p")),Err("unavailable".into()));
        assert!(!s.to_string().contains("private text"));
        assert_eq!(evaluate(Some(&s))["reading"],"not established");
    }
    #[test]
    fn reading_is_not_shared_with_another_thread_or_source() {
        let c=conversation();let s=signals(&c,Ok(json!({"multiAgentVersion":"v1"})),Ok(config(json!({}))),Ok(json!({"requirements":null})),Ok(json!("p")),Ok(json!({})));
        let mut other=c.clone();other["threadId"]=json!("u");
        let mut child=c.clone();child["threadSource"]=json!({"subAgent":"review"});
        let mut rows=json!([c,other,child]);
        annotate_threads(&mut rows,&[json!({"key":key(&conversation()),"signals":s})]);
        assert_eq!(rows[0]["delegation"]["reading"],"present");
        assert_eq!(rows[1]["delegation"]["reading"],"not established");
        assert_eq!(rows[2]["delegation"]["reading"],"not established");
    }
}
