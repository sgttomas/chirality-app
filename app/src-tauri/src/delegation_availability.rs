//! Delegation availability (DEL-01-03 NPTD §7.1, R18-1 C-04, reading order by
//! R21-1; read at run time, R19-5) for one conversation, in the Rust host
//! under the owner's OI-008 ruling ("The Rust host owns everything that ...
//! talks to Codex"). The host reads three supplier signals per conversation's
//! model and provider, per Codex home (each home's `Host` keeps its own
//! readings); the web view presents the reading and its reason.
//!
//! Signals at the 0.160.0 pin (generated types under
//! `resources/supplier/0.160.0/`):
//! - `model/list` → `Model.multiAgentVersion` (`disabled` · `v1` · `v2`, or
//!   null) of the entry whose `model` or `id` is the conversation's reported
//!   model;
//! - `config/read` (with the conversation's `cwd`) → `config.features.multi_agent`.
//!   `Config` has no typed `features` field at the pin; it is read as an
//!   additional property, and a configuration that was read and sets nothing
//!   is read, not unread;
//! - `modelProvider/capabilities/read` → `namespaceTools`. Its params are empty
//!   at the pin: it reads the home's configured provider, so the reading counts
//!   for the conversation only when the effective configuration's
//!   `model_provider` is the conversation's reported `modelProvider`; otherwise
//!   `namespaceTools` is not read for that conversation.
use serde_json::{json, Value};

/// The reading's identity: a reading answers for one conversation's model,
/// provider and working folder in one Codex generation of one home.
pub(crate) fn key(conversation: &Value) -> Value {
    json!({"generation":conversation["generation"],"model":conversation["model"],"modelProvider":conversation["modelProvider"],"cwd":conversation["cwd"]})
}

/// The signals from the three reads, for `conversation` (a host thread row:
/// `model`, `modelProvider`, `cwd`). `model` is the `model/list` entry of the
/// conversation's model (`Ok(Value::Null)` when it was not listed); `config`
/// the `config/read` result; `capabilities` the
/// `modelProvider/capabilities/read` result. Only what §7.1 needs is kept.
pub(crate) fn signals(conversation: &Value, model: Result<Value, String>, config: Result<Value, String>, capabilities: Result<Value, String>) -> Value {
    let mut limits = vec![];
    let version = match &model {
        Ok(entry) if entry.is_null() => {
            limits.push(format!("multiAgentVersion not read: model/list lists no model {}", conversation["model"]));
            Value::Null
        }
        Ok(entry) => match entry.get("multiAgentVersion") {
            Some(v) if v == "disabled" || v == "v1" || v == "v2" => v.clone(),
            _ => {
                limits.push(format!("multiAgentVersion not read: model/list reports none for {}", conversation["model"]));
                Value::Null
            }
        },
        Err(cause) => {
            limits.push(format!("multiAgentVersion not read: {cause}"));
            Value::Null
        }
    };
    let (effective, configured_provider) = match &config {
        Ok(result) => {
            let features = result["config"].get("features").and_then(|f| f.get("multi_agent")).cloned();
            let effective = match features {
                Some(v) => json!({"features":{"multi_agent":v}}),
                None => json!({}),
            };
            (effective, Some(result["config"]["model_provider"].clone()))
        }
        Err(cause) => {
            limits.push(format!("effective configuration not read: {cause}"));
            (Value::Null, None)
        }
    };
    let capabilities = match (&capabilities, &configured_provider) {
        (Err(cause), _) => {
            limits.push(format!("namespaceTools not read: {cause}"));
            Value::Null
        }
        (Ok(_), None) => {
            limits.push("namespaceTools not read for this conversation: the configuration was not read, so the provider modelProvider/capabilities/read answered for is not known".into());
            Value::Null
        }
        (Ok(result), Some(provider)) => {
            let conversation_provider = &conversation["modelProvider"];
            if provider.is_string() && provider == conversation_provider {
                json!({"namespaceTools":result["namespaceTools"]})
            } else {
                limits.push(format!(
                    "namespaceTools not read for this conversation: modelProvider/capabilities/read takes no provider at Codex 0.160.0 and answers for the home's configured provider ({}), not the conversation's ({})",
                    provider.as_str().unwrap_or("none named in the effective configuration"),
                    conversation_provider.as_str().unwrap_or("not reported")
                ));
                Value::Null
            }
        }
    };
    json!({"model_multi_agent_version":version,"effective_config":effective,"provider_capabilities":capabilities,"limits":limits,
        "conversation":{"model":conversation["model"],"modelProvider":conversation["modelProvider"],"cwd":conversation["cwd"]}})
}

/// NPTD §7.1 in R21-1's order: (1) `multiAgentVersion` `disabled` → missing;
/// (2) effective `features.multi_agent = false` → missing; (3) `namespaceTools`
/// false → missing; (4) any of the three not read → not established; (5)
/// otherwise present. Missing names the first reason in that order.
pub(crate) fn evaluate(signals: Option<&Value>) -> Value {
    let Some(s) = signals else {
        return json!({"reading":"not established","reason":"the delegation signals were not read for this conversation yet (NPTD §7.1 (4)); the agent may be unable to start a sub-agent"});
    };
    let version = &s["model_multi_agent_version"];
    let config = &s["effective_config"];
    let caps = &s["provider_capabilities"];
    let at = |reading: Value| {
        let mut reading = reading;
        reading["readAt"] = s["readAt"].clone();
        reading
    };
    if version == "disabled" {
        return at(json!({"reading":"missing","reason":"the conversation's model reports multiAgentVersion disabled (NPTD §7.1 (1))"}));
    }
    if config["features"]["multi_agent"] == false {
        return at(json!({"reading":"missing","reason":"the effective configuration sets features.multi_agent = false (NPTD §7.1 (2))"}));
    }
    if caps["namespaceTools"] == false {
        return at(json!({"reading":"missing","reason":"the provider reports namespaceTools false, so Codex sends no delegation tools (NPTD §7.1 (3))"}));
    }
    let version_read = version == "v1" || version == "v2";
    if !version_read || !config.is_object() || caps["namespaceTools"] != true {
        let limits: Vec<String> = s["limits"].as_array().into_iter().flatten().filter_map(|l| l.as_str().map(str::to_owned)).collect();
        let detail = if limits.is_empty() { "one of multiAgentVersion, the effective configuration or namespaceTools was not read".to_owned() } else { limits.join("; ") };
        return at(json!({"reading":"not established","reason":format!("{detail} (NPTD §7.1 (4)); the agent may be unable to start a sub-agent")}));
    }
    at(json!({"reading":"present","reason":null}))
}

/// `host_status`'s thread rows each gain `delegation`: the reading for that
/// conversation from the home's readings (`readings`, as the Host keeps them),
/// or *not established* when none answers for its model, provider and folder.
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
    fn conversation() -> Value {
        json!({"generation":{"home":"h"},"threadId":"t","model":"m","modelProvider":"p","cwd":"/w"})
    }
    fn entry(version: Option<&str>) -> Value {
        match version {
            Some(v) => json!({"id":"m","model":"m","multiAgentVersion":v}),
            None => json!({"id":"m","model":"m","multiAgentVersion":null}),
        }
    }
    fn config(multi_agent: Option<bool>, provider: Option<&str>) -> Value {
        let mut c = json!({"config":{"model_provider":provider},"origins":{}});
        if let Some(v) = multi_agent {
            c["config"]["features"] = json!({"multi_agent":v});
        }
        c
    }
    fn caps(namespace: bool) -> Value {
        json!({"imageGeneration":false,"namespaceTools":namespace,"webSearch":false})
    }
    fn read(model: Result<Value, String>, config: Result<Value, String>, capabilities: Result<Value, String>) -> Value {
        evaluate(Some(&signals(&conversation(), model, config, capabilities)))
    }
    fn reading(v: &Value) -> &str {
        v["reading"].as_str().unwrap()
    }
    const UNREAD: fn() -> Result<Value, String> = || Err("no response".into());

    #[test]
    fn each_reading_in_r21_1_order_and_missing_names_the_first_reason() {
        let ok = || Ok(entry(Some("v2")));
        let present = read(ok(), Ok(config(None, Some("p"))), Ok(caps(true)));
        assert_eq!(present["reading"], "present");
        assert_eq!(reading(&read(Ok(entry(Some("v1"))), Ok(config(Some(true), Some("p"))), Ok(caps(true)))), "present", "v1 and multi_agent true");
        // (1) disabled decides first, even with every other missing reading.
        let first = read(Ok(entry(Some("disabled"))), Ok(config(Some(false), Some("p"))), Ok(caps(false)));
        assert_eq!(first["reading"], "missing");
        assert!(first["reason"].as_str().unwrap().contains("(1)"), "{first}");
        // (2) multi_agent false before namespaceTools false.
        let second = read(ok(), Ok(config(Some(false), Some("p"))), Ok(caps(false)));
        assert!(second["reason"].as_str().unwrap().contains("features.multi_agent = false"), "{second}");
        // (3) namespaceTools false.
        let third = read(ok(), Ok(config(None, Some("p"))), Ok(caps(false)));
        assert_eq!(third["reading"], "missing");
        assert!(third["reason"].as_str().unwrap().contains("(3)"));
        // Missing wins over a signal not read.
        assert_eq!(reading(&read(UNREAD(), Ok(config(Some(false), Some("p"))), UNREAD())), "missing");
        assert_eq!(reading(&read(UNREAD(), Ok(config(None, Some("p"))), Ok(caps(false)))), "missing");
        assert_eq!(reading(&read(Ok(entry(Some("disabled"))), UNREAD(), UNREAD())), "missing");
    }

    #[test]
    fn each_signal_not_read_is_not_established_with_its_cause() {
        let cases = [
            (read(UNREAD(), Ok(config(None, Some("p"))), Ok(caps(true))), "multiAgentVersion not read: no response"),
            (read(Ok(Value::Null), Ok(config(None, Some("p"))), Ok(caps(true))), "lists no model"),
            (read(Ok(entry(None)), Ok(config(None, Some("p"))), Ok(caps(true))), "reports none"),
            (read(Ok(entry(Some("v2"))), UNREAD(), Ok(caps(true))), "effective configuration not read"),
            (read(Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), UNREAD()), "namespaceTools not read: no response"),
        ];
        for (reading, cause) in cases {
            assert_eq!(reading["reading"], "not established", "{reading}");
            assert!(reading["reason"].as_str().unwrap().contains(cause), "{reading} should name {cause}");
        }
        // The capability read answers for the home's configured provider only.
        let other = read(Ok(entry(Some("v2"))), Ok(config(None, Some("other"))), Ok(caps(true)));
        assert_eq!(other["reading"], "not established");
        assert!(other["reason"].as_str().unwrap().contains("home's configured provider (other), not the conversation's (p)"), "{other}");
        let unnamed = read(Ok(entry(Some("v2"))), Ok(config(None, None)), Ok(caps(false)));
        assert_eq!(unnamed["reading"], "not established", "namespaceTools false for another provider is not this conversation's: {unnamed}");
        // No reading at all.
        assert_eq!(evaluate(None)["reading"], "not established");
    }

    #[test]
    fn a_configuration_read_that_sets_nothing_is_read() {
        let s = signals(&conversation(), Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), Ok(caps(true)));
        assert_eq!(s["effective_config"], json!({}));
        assert_eq!(evaluate(Some(&s))["reading"], "present");
        let unread = signals(&conversation(), Ok(entry(Some("v2"))), UNREAD(), Ok(caps(true)));
        assert!(unread["effective_config"].is_null());
        // Nothing of the configuration but features.multi_agent is kept.
        let mut full = config(Some(true), Some("p"));
        full["config"]["developer_instructions"] = json!("private text");
        let kept = signals(&conversation(), Ok(entry(Some("v2"))), Ok(full), Ok(caps(true)));
        assert!(!kept.to_string().contains("private text"));
    }

    #[test]
    fn all_combinations_agree_with_the_r21_1_order() {
        let versions: [Result<Value, String>; 5] = [Ok(entry(Some("disabled"))), Ok(entry(Some("v1"))), Ok(entry(Some("v2"))), Ok(entry(None)), Err("x".into())];
        let configs: [Result<Value, String>; 4] = [Ok(config(Some(false), Some("p"))), Ok(config(Some(true), Some("p"))), Ok(config(None, Some("p"))), Err("x".into())];
        let capabilities: [Result<Value, String>; 3] = [Ok(caps(true)), Ok(caps(false)), Err("x".into())];
        for v in &versions {
            for c in &configs {
                for k in &capabilities {
                    let got = read(v.clone(), c.clone(), k.clone());
                    let version = v.as_ref().ok().and_then(|e| e["multiAgentVersion"].as_str());
                    let multi = c.as_ref().ok().map(|c| c["config"]["features"]["multi_agent"].clone());
                    let namespace = if c.is_ok() { k.as_ref().ok().map(|k| k["namespaceTools"].clone()) } else { None };
                    let expected = if version == Some("disabled") || multi == Some(json!(false)) || namespace == Some(json!(false)) {
                        "missing"
                    } else if matches!(version, Some("v1" | "v2")) && multi.is_some() && namespace == Some(json!(true)) {
                        "present"
                    } else {
                        "not established"
                    };
                    assert_eq!(got["reading"], expected, "{v:?} {c:?} {k:?}");
                }
            }
        }
    }

    #[test]
    fn thread_rows_take_the_reading_of_their_own_model_provider_and_folder() {
        let present = signals(&conversation(), Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), Ok(caps(true)));
        let readings = vec![json!({"key":key(&conversation()),"signals":present})];
        let mut other_model = conversation();
        other_model["model"] = json!("n");
        other_model["threadId"] = json!("u");
        let mut threads = json!([conversation(), other_model]);
        annotate_threads(&mut threads, &readings);
        assert_eq!(threads[0]["delegation"]["reading"], "present");
        assert_eq!(threads[1]["delegation"]["reading"], "not established", "another model has no reading yet");
    }
}
