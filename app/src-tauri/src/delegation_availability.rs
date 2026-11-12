//! Delegation availability (DEL-01-03 NPTD §7.1, R18-1 C-04 as revised by the
//! owner on 2026-11-09, reading order by R21-1; read at run time, R19-5) for
//! one conversation, in the Rust host under the owner's OI-008 ruling ("The
//! Rust host owns everything that ... talks to Codex"). The host reads the
//! supplier signals per conversation's model and provider, per Codex home
//! (each home's `Host` keeps its own readings); the web view presents the
//! reading and its reason.
//!
//! Signals at the declared pin (generated types under
//! `resources/supplier/<pin>/`):
//! - `model/list` → `Model.multiAgentVersion` (`disabled` · `v1` · `v2`, or
//!   null) of the entry whose `model` or `id` is the conversation's reported
//!   model;
//! - `config/read` (with the conversation's `cwd`) → `config.features.multi_agent`.
//!   `Config` has no typed `features` field at the pin; it is read as an
//!   additional property, and a configuration that was read and sets nothing
//!   is read, not unread.
//!
//! `modelProvider/capabilities/read` no longer publishes `namespaceTools`:
//! openai/codex PR 50447 removed the provider gate on tool namespaces, so
//! Codex offers its sub-agent tools whatever the provider's capabilities. The
//! read stays only to note its failure; it never changes the reading, and a
//! legacy `namespaceTools` echo in its result is ignored.
//!
//! `model/list` takes no provider at the pin: it answers for the provider the
//! app-server resolves for itself, not for a conversation whose folder
//! (project `.codex/` layers) or start chose another. The host reads that
//! server provider as `config/read`'s `model_provider` without a folder and
//! at the server's own working folder (both must agree). `multiAgentVersion`
//! counts for a conversation only when that server provider is the
//! conversation's reported `modelProvider`; otherwise it is not read for it.
use serde_json::{json, Value};

/// The reading's identity: a reading answers for one conversation's model,
/// provider and working folder in one Codex generation of one home.
pub(crate) fn key(conversation: &Value) -> Value {
    json!({"generation":conversation["generation"],"model":conversation["model"],"modelProvider":conversation["modelProvider"],"cwd":conversation["cwd"]})
}

/// The signals from the reads, for `conversation` (a host thread row:
/// `model`, `modelProvider`, `cwd`). `model` is the `model/list` entry of the
/// conversation's model (`Ok(Value::Null)` when it was not listed); `config`
/// the `config/read` result at the conversation's folder; `server` the
/// provider the app-server resolves for itself (`config/read`'s
/// `model_provider`, a string or null); `capabilities` the
/// `modelProvider/capabilities/read` result, of which only a failure is kept,
/// as a note. Only what §7.1 needs is kept.
pub(crate) fn signals(conversation: &Value, model: Result<Value, String>, config: Result<Value, String>, server: Result<Value, String>, capabilities: Result<Value, String>) -> Value {
    let mut limits = vec![];
    let mut notes = vec![];
    let conversation_provider = &conversation["modelProvider"];
    // Why model/list does not answer for this conversation, if it does not.
    let other_provider = match &server {
        Ok(provider) if provider.is_string() && provider == conversation_provider => None,
        Ok(provider) => Some(format!(
            "it takes no provider at Codex {} and answers for the app-server's provider ({}), not the conversation's ({})",
            crate::hosting::DECLARED_PIN,
            provider.as_str().unwrap_or("none named in the app-server's configuration"),
            conversation_provider.as_str().unwrap_or("not reported")
        )),
        Err(cause) => Some(format!("it takes no provider at Codex {} and the app-server's provider was not read ({cause})", crate::hosting::DECLARED_PIN)),
    };
    let version = match (&model, &other_provider) {
        (Err(cause), _) => {
            limits.push(format!("multiAgentVersion not read: {cause}"));
            Value::Null
        }
        (Ok(_), Some(why)) => {
            limits.push(format!("multiAgentVersion not read for this conversation: model/list {why}"));
            Value::Null
        }
        (Ok(entry), None) if entry.is_null() => {
            limits.push(format!("multiAgentVersion not read: model/list lists no model {}", conversation["model"]));
            Value::Null
        }
        (Ok(entry), None) => match entry.get("multiAgentVersion") {
            Some(v) if v == "disabled" || v == "v1" || v == "v2" => v.clone(),
            _ => {
                limits.push(format!("multiAgentVersion not read: model/list reports none for {}", conversation["model"]));
                Value::Null
            }
        },
    };
    let effective = match &config {
        Ok(result) => match result["config"].get("features").and_then(|f| f.get("multi_agent")) {
            Some(v) => json!({"features":{"multi_agent":v}}),
            None => json!({}),
        },
        Err(cause) => {
            limits.push(format!("effective configuration not read: {cause}"));
            Value::Null
        }
    };
    // No provider capability gates delegation at the declared pin (openai/codex PR
    // 50447): nothing of the result is kept, and a failure is only noted.
    if let Err(cause) = &capabilities {
        notes.push(format!("modelProvider/capabilities/read failed ({cause}); no provider capability gates delegation at Codex {}, so the reading does not rest on it", crate::hosting::DECLARED_PIN));
    }
    json!({"model_multi_agent_version":version,"effective_config":effective,"limits":limits,"notes":notes,
        "conversation":{"model":conversation["model"],"modelProvider":conversation["modelProvider"],"cwd":conversation["cwd"]}})
}

/// NPTD §7.1's readings in R21-1's order: (1) `multiAgentVersion` disabled
/// and (2) an effective `features.multi_agent = false` are *missing*; (3) a
/// version or configuration not read (or not counting for the conversation)
/// is *not established*; (4) otherwise *present*. Provider capabilities take
/// no part: a capabilities-read failure is carried as `note` only, and a
/// legacy `namespaceTools` echo is ignored.
pub(crate) fn evaluate(signals: Option<&Value>) -> Value {
    let Some(s) = signals else {
        return json!({"reading":"not established","reason":"the delegation signals were not read for this conversation yet (NPTD §7.1 (3)); the agent may be unable to start a sub-agent"});
    };
    let version = &s["model_multi_agent_version"];
    let config = &s["effective_config"];
    let notes: Vec<&str> = s["notes"].as_array().into_iter().flatten().filter_map(Value::as_str).collect();
    let at = |reading: Value| {
        let mut reading = reading;
        reading["readAt"] = s["readAt"].clone();
        if !notes.is_empty() { reading["note"] = json!(notes.join("; ")); }
        reading
    };
    if version == "disabled" {
        return at(json!({"reading":"missing","reason":"the conversation's model reports multiAgentVersion disabled (NPTD §7.1 (1))"}));
    }
    if config["features"]["multi_agent"] == false {
        return at(json!({"reading":"missing","reason":"the effective configuration sets features.multi_agent = false (NPTD §7.1 (2))"}));
    }
    let limits: Vec<&str> = s["limits"].as_array().into_iter().flatten().filter_map(Value::as_str).collect();
    if limits.is_empty() && (version == "v1" || version == "v2") && config.is_object() {
        return at(json!({"reading":"present","reason":null}));
    }
    let detail = if limits.is_empty() { "the model's multiAgentVersion or the effective configuration was not read".to_owned() } else { limits.join("; ") };
    at(json!({"reading":"not established","reason":format!("{detail} (NPTD §7.1 (3)); the agent may be unable to start a sub-agent")}))
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
    /// A 0.167.0 capabilities result, optionally with a legacy (pre-0.167)
    /// `namespaceTools` echo as an untyped additional property.
    fn caps(legacy_namespace: Option<bool>) -> Value {
        let mut c = json!({"imageGeneration":false,"webSearch":false});
        if let Some(n) = legacy_namespace {
            c["namespaceTools"] = json!(n);
        }
        c
    }
    fn read(model: Result<Value, String>, config: Result<Value, String>, capabilities: Result<Value, String>) -> Value {
        evaluate(Some(&signals(&conversation(), model, config, Ok(json!("p")), capabilities)))
    }
    fn reading(v: &Value) -> &str {
        v["reading"].as_str().unwrap()
    }
    const UNREAD: fn() -> Result<Value, String> = || Err("no response".into());

    #[test]
    fn a_legacy_namespace_tools_echo_does_not_change_the_reading() {
        // Codex 0.167.0 removed namespaceTools and its gate (openai/codex PR
        // 50447); an echo of it, true or false, neither hides nor shows delegation.
        for (version, multi_agent, expected) in [("v2", None, "present"), ("v1", Some(true), "present"), ("disabled", None, "missing"), ("v2", Some(false), "missing")] {
            let without = read(Ok(entry(Some(version))), Ok(config(multi_agent, Some("p"))), Ok(caps(None)));
            assert_eq!(without["reading"], expected, "{version} {multi_agent:?}: {without}");
            for legacy in [true, false] {
                let with = read(Ok(entry(Some(version))), Ok(config(multi_agent, Some("p"))), Ok(caps(Some(legacy))));
                assert_eq!(with, without, "namespaceTools {legacy} changes nothing");
            }
        }
        // Nor does a signals value carrying a pre-0.167 provider_capabilities field.
        for legacy in [true, false] {
            let s = json!({"model_multi_agent_version":"v2","effective_config":{},"provider_capabilities":{"namespaceTools":legacy},"limits":[]});
            assert_eq!(evaluate(Some(&s))["reading"], "present", "namespaceTools {legacy}");
        }
        // And nothing of the capabilities result is kept.
        let s = signals(&conversation(), Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), Ok(json!("p")), Ok(caps(Some(false))));
        assert!(!s.to_string().contains("namespaceTools") && !s.to_string().contains("imageGeneration"), "{s}");
    }

    #[test]
    fn each_reading_in_r21_1_order_and_missing_names_the_first_reason() {
        let ok = || Ok(entry(Some("v2")));
        let present = read(ok(), Ok(config(None, Some("p"))), Ok(caps(None)));
        assert_eq!(present["reading"], "present", "{present}");
        assert!(present["reason"].is_null() && present.get("note").is_none(), "{present}");
        assert_eq!(reading(&read(Ok(entry(Some("v1"))), Ok(config(Some(true), Some("p"))), Ok(caps(None)))), "present");
        // (1) disabled decides first, even with (2) also missing.
        let first = read(Ok(entry(Some("disabled"))), Ok(config(Some(false), Some("p"))), Ok(caps(None)));
        assert_eq!(first["reading"], "missing");
        assert!(first["reason"].as_str().unwrap().contains("(1)"), "{first}");
        // (2) multi_agent false.
        let second = read(ok(), Ok(config(Some(false), Some("p"))), Ok(caps(None)));
        assert_eq!(second["reading"], "missing");
        assert!(second["reason"].as_str().unwrap().contains("features.multi_agent = false"), "{second}");
        // Missing wins over a signal not read.
        assert_eq!(reading(&read(UNREAD(), Ok(config(Some(false), Some("p"))), UNREAD())), "missing");
        assert_eq!(reading(&read(Ok(entry(Some("disabled"))), UNREAD(), UNREAD())), "missing");
        assert_eq!(reading(&read(UNREAD(), Ok(config(None, Some("p"))), Ok(caps(None)))), "not established");
    }

    #[test]
    fn a_capabilities_read_failure_is_a_note_only() {
        let failed = read(Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), UNREAD());
        assert_eq!(failed["reading"], "present", "{failed}");
        assert!(failed["note"].as_str().unwrap().contains("modelProvider/capabilities/read failed (no response)"), "{failed}");
        let missing = read(Ok(entry(Some("v2"))), Ok(config(Some(false), Some("p"))), UNREAD());
        assert_eq!(missing["reading"], "missing");
        assert!(missing["note"].is_string());
        let unread = read(UNREAD(), Ok(config(None, Some("p"))), UNREAD());
        assert_eq!(unread["reading"], "not established");
        assert!(!unread["reason"].as_str().unwrap().contains("capabilities"), "the note is not a reason: {unread}");
    }

    #[test]
    fn each_signal_not_read_is_not_established_with_its_cause() {
        let cases = [
            (read(UNREAD(), Ok(config(None, Some("p"))), Ok(caps(None))), "multiAgentVersion not read: no response"),
            (read(Ok(Value::Null), Ok(config(None, Some("p"))), Ok(caps(None))), "lists no model"),
            (read(Ok(entry(None)), Ok(config(None, Some("p"))), Ok(caps(None))), "reports none"),
            (read(Ok(entry(Some("v2"))), UNREAD(), Ok(caps(None))), "effective configuration not read"),
        ];
        for (reading, cause) in cases {
            assert_eq!(reading["reading"], "not established", "{reading}");
            assert!(reading["reason"].as_str().unwrap().contains(cause), "{reading} should name {cause}");
        }
        // B-1: model/list answers for the app-server's provider, never for a
        // conversation whose provider differs, whatever the conversation's
        // folder configuration names.
        let on = |server: Result<Value, String>, version: &str| {
            evaluate(Some(&signals(&conversation(), Ok(entry(Some(version))), Ok(config(None, Some("p"))), server, Ok(caps(None)))))
        };
        for server in [Ok(json!("other")), Ok(Value::Null), Err("config/read not sent".to_owned())] {
            // The server's catalog says present: not this conversation's.
            let up = on(server.clone(), "v2");
            assert_eq!(up["reading"], "not established", "{server:?}: {up}");
            assert!(up["reason"].as_str().unwrap().contains("model/list it takes no provider"), "{up}");
            // It says missing: not this conversation's either, so nothing is hidden.
            assert_eq!(on(server.clone(), "disabled")["reading"], "not established", "{server:?}: a same-named model's disabled from another catalog");
        }
        assert!(on(Ok(json!("other")), "v2")["reason"].as_str().unwrap().contains("app-server's provider (other), not the conversation's (p)"));
        assert_eq!(on(Ok(json!("p")), "disabled")["reading"], "missing");
        assert_eq!(on(Ok(json!("p")), "v2")["reading"], "present");
        // No reading at all.
        assert_eq!(evaluate(None)["reading"], "not established");
        // RV21 (R21-1): a configuration never read is not "nothing set", even
        // with the version read.
        let unread_config = json!({"model_multi_agent_version":"v2","effective_config":null,"limits":[]});
        assert_eq!(evaluate(Some(&unread_config))["reading"], "not established");
        let unread_version = json!({"model_multi_agent_version":null,"effective_config":{},"limits":[]});
        assert_eq!(evaluate(Some(&unread_version))["reading"], "not established");
    }

    #[test]
    fn a_configuration_read_that_sets_nothing_is_read() {
        let s = signals(&conversation(), Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), Ok(json!("p")), Ok(caps(None)));
        assert_eq!(s["effective_config"], json!({}));
        assert_eq!(evaluate(Some(&s))["reading"], "present");
        let unread = signals(&conversation(), Ok(entry(Some("v2"))), UNREAD(), Ok(json!("p")), Ok(caps(None)));
        assert!(unread["effective_config"].is_null());
        // Nothing of the configuration but features.multi_agent is kept.
        let mut full = config(Some(true), Some("p"));
        full["config"]["developer_instructions"] = json!("private text");
        let kept = signals(&conversation(), Ok(entry(Some("v2"))), Ok(full), Ok(json!("p")), Ok(caps(None)));
        assert!(!kept.to_string().contains("private text"));
    }

    #[test]
    fn all_combinations_agree_with_the_r21_1_order() {
        let versions: [Result<Value, String>; 5] = [Ok(entry(Some("disabled"))), Ok(entry(Some("v1"))), Ok(entry(Some("v2"))), Ok(entry(None)), Err("x".into())];
        let configs: [Result<Value, String>; 4] = [Ok(config(Some(false), Some("p"))), Ok(config(Some(true), Some("p"))), Ok(config(None, Some("p"))), Err("x".into())];
        let capabilities: [Result<Value, String>; 4] = [Ok(caps(None)), Ok(caps(Some(true))), Ok(caps(Some(false))), Err("x".into())];
        for v in &versions {
            for c in &configs {
                for k in &capabilities {
                    let got = read(v.clone(), c.clone(), k.clone());
                    let version = v.as_ref().ok().and_then(|e| e["multiAgentVersion"].as_str());
                    let multi = c.as_ref().ok().map(|c| c["config"]["features"]["multi_agent"].clone());
                    let expected = if version == Some("disabled") || multi == Some(json!(false)) {
                        "missing"
                    } else if matches!(version, Some("v1" | "v2")) && c.is_ok() {
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
        let present = signals(&conversation(), Ok(entry(Some("v2"))), Ok(config(None, Some("p"))), Ok(json!("p")), Ok(caps(None)));
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
