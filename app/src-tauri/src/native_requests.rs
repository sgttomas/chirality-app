//! Main-process request custody. Native parameters live only in the current
//! process; durable recovery exports summaries, never the conversation payload.
use serde_json::{json, Value};
use std::collections::HashMap;
use std::sync::OnceLock;

const ANSWERS: &[(&str, &str)] = &[
    (
        "item/commandExecution/requestApproval",
        "CommandExecutionRequestApprovalResponse",
    ),
    (
        "item/fileChange/requestApproval",
        "FileChangeRequestApprovalResponse",
    ),
    (
        "item/permissions/requestApproval",
        "PermissionsRequestApprovalResponse",
    ),
    ("execCommandApproval", "ExecCommandApprovalResponse"),
    ("applyPatchApproval", "ApplyPatchApprovalResponse"),
    ("item/tool/requestUserInput", "ToolRequestUserInputResponse"),
    (
        "mcpServer/elicitation/request",
        "McpServerElicitationRequestResponse",
    ),
    ("currentTime/read", "CurrentTimeReadResponse"),
];
fn validators() -> Result<&'static HashMap<String, jsonschema::Validator>, String> {
    static VALIDATORS: OnceLock<Result<HashMap<String, jsonschema::Validator>, String>> =
        OnceLock::new();
    VALIDATORS
        .get_or_init(|| {
            let source: Value = serde_json::from_str(include_str!(
                "../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json"
            ))
            .map_err(|e| e.to_string())?;
            ANSWERS
                .iter()
                .map(|(method, target)| {
                    // Select a target in the unchanged generated definition tree. All
                    // local refs keep their native root; retrieval stays disabled.
                    let mut schema = source.clone();
                    schema["$ref"] = json!(format!("#/definitions/{target}"));
                    jsonschema::options()
                        .with_draft(jsonschema::Draft::Draft7)
                        .offline()
                        .build(&schema)
                        .map(|v| (method.to_string(), v))
                        .map_err(|e| e.to_string())
                })
                .collect()
        })
        .as_ref()
        .map_err(Clone::clone)
}
pub fn negative(method: &str, answer: &Value) -> bool {
    let decision = answer.get("decision").unwrap_or(answer);
    matches!(
        decision.as_str(),
        Some("decline" | "cancel" | "denied" | "abort")
    ) || decision.get("denied").is_some()
        || matches!(
            answer.get("action").and_then(Value::as_str),
            Some("decline" | "cancel")
        )
        || (method == "item/tool/requestUserInput" && answer.get("answers") == Some(&json!({})))
        || (method == "item/permissions/requestApproval"
            && answer.get("permissions") == Some(&json!({})))
}
pub fn decline(method: &str, params: &Value) -> Option<Value> {
    match method {
        "item/commandExecution/requestApproval" | "item/fileChange/requestApproval" => {
            let offered = params.get("availableDecisions").and_then(Value::as_array);
            ["decline", "cancel"]
                .into_iter()
                .find(|d| offered.map(|a| a.contains(&json!(d))).unwrap_or(true))
                .map(|d| json!({"decision":d}))
        }
        "execCommandApproval" | "applyPatchApproval" => {
            Some(json!({"decision":{"denied":{"rejection":""}}}))
        }
        "item/permissions/requestApproval" => Some(json!({"permissions":{},"scope":"turn"})),
        "item/tool/requestUserInput" => Some(json!({"answers":{}})),
        "mcpServer/elicitation/request" => {
            Some(json!({"action":"decline","content":null,"_meta":null}))
        }
        _ => None,
    }
}
/// A grant may remove requested entries, never add broader permissions.
fn subset(grant: &Value, requested: &Value) -> bool {
    if grant.is_null() {
        return true;
    }
    match grant {
        Value::Object(fields) => fields.iter().all(|(key, value)| {
            requested
                .get(key)
                .map(|r| subset(value, r))
                .unwrap_or(value.is_null())
        }),
        Value::Array(items) => requested
            .as_array()
            .map(|r| items.iter().all(|v| r.contains(v)))
            .unwrap_or(false),
        Value::Bool(false) => requested.is_boolean(),
        _ => grant == requested,
    }
}
fn validate_answer(method: &str, params: &Value, answer: &Value) -> Result<(), String> {
    let validator = validators()?.get(method).ok_or("invalid-answer")?;
    validator
        .validate(answer)
        .map_err(|_| "invalid-answer".to_string())?;
    if let Some(decision) = answer.get("decision") {
        if decision == "timed_out" {
            return Err("invalid-answer".into());
        }
        if let Some(offered) = params.get("availableDecisions").and_then(Value::as_array) {
            if !offered.contains(decision) {
                return Err("invalid-answer".into());
            }
        } else if method == "item/commandExecution/requestApproval" {
            if let Some(amendment) = decision.get("acceptWithExecpolicyAmendment") {
                if amendment.get("execpolicy_amendment")
                    != params.get("proposedExecpolicyAmendment")
                    || params.get("proposedExecpolicyAmendment").is_none()
                {
                    return Err("invalid-answer".into());
                }
            }
            if let Some(amendment) = decision.get("applyNetworkPolicyAmendment") {
                let offered = params
                    .get("proposedNetworkPolicyAmendments")
                    .and_then(Value::as_array);
                if !offered
                    .map(|a| {
                        amendment
                            .get("network_policy_amendment")
                            .map(|v| a.contains(v))
                            .unwrap_or(false)
                    })
                    .unwrap_or(false)
                {
                    return Err("invalid-answer".into());
                }
            }
        }
    }
    if method == "item/permissions/requestApproval"
        && !subset(&answer["permissions"], &params["permissions"])
    {
        return Err("invalid-answer".into());
    }
    if method == "mcpServer/elicitation/request"
        && answer["action"] == "accept"
        && matches!(
            params["mode"].as_str(),
            Some("form" | "openai/form" | "openaiForm")
        )
    {
        let schema = params.get("requestedSchema").ok_or("invalid-answer")?;
        let validator = jsonschema::options()
            .offline()
            .build(schema)
            .map_err(|_| "invalid-answer".to_string())?;
        validator
            .validate(&answer["content"])
            .map_err(|_| "invalid-answer".to_string())?;
    }
    if method == "item/tool/requestUserInput" {
        let questions = params
            .get("questions")
            .and_then(Value::as_array)
            .ok_or("invalid-answer")?;
        for (id, value) in answer["answers"].as_object().ok_or("invalid-answer")? {
            let q = questions
                .iter()
                .find(|q| q["id"] == id.as_str())
                .ok_or("invalid-answer")?;
            if q["isOther"] != true {
                for a in value["answers"].as_array().ok_or("invalid-answer")? {
                    if !q["options"]
                        .as_array()
                        .map(|opts| opts.iter().any(|o| o["label"] == *a))
                        .unwrap_or(false)
                    {
                        return Err("invalid-answer".into());
                    }
                }
            }
        }
    }
    Ok(())
}

#[derive(Default)]
pub struct RequestRegister {
    entries: Vec<Value>,
    closed: Vec<Value>,
}
impl RequestRegister {
    pub fn entries(&self) -> Vec<Value> {
        self.entries.clone()
    }
    /// Export the adopted HOSTING record interface; reducer-private fields stay private.
    pub fn records(&self) -> Vec<Value> {
        self.entries.iter().map(|e| {
            let method=e["method"].as_str().unwrap_or("");
            let class=if e["classification"]!="known-answerable" {"none"}else if method=="currentTime/read" {"named-service"}else if matches!(method,"item/tool/requestUserInput"|"mcpServer/elicitation/request") {"person-input"}else{"a14"};
            let mut record=json!({"recordKind":"server-request-entry","requestIdentity":e["requestId"],"generation":e["generation"],"method":method,
                "classification":e["classification"],"originClass":class,"nativeParameters":e["nativeParameters"],"receiptPosition":e["receiptPosition"],
                "state":if class=="none"&&e["state"]=="settling" {json!("received")}else{e["state"].clone()},"replyWriteResult":e["replyWriteResult"],
                "acknowledgmentObservation":if e["acknowledgment"].is_object(){json!({"status":"observed","what":e["acknowledgment"]["observed"]})}else{json!({"status":"not-observed"})}});
            let mut subject=serde_json::Map::new();
            for (native,key) in [("threadId","thread"),("turnId","turn"),("itemId","item"),("callId","call")] {if let Some(value)=e["nativeParameters"].get(native){subject.insert(key.into(),value.clone());}}
            if !subject.is_empty(){record["subjectReferences"]=Value::Object(subject);}
            if e["state"]=="ended-unanswered" {record["endCause"]=json!("process-exit");}
            if e.get("resolution").is_some() {record["supplierResolution"]=json!({"source":"serverRequest/resolved"});if let Some(cause)=e["resolution"].get("cause"){record["supplierResolution"]["cause"]=cause.clone();}}
            if let Some(settlement)=e.get("settlement") {
                let origin=settlement["origin"].as_str().unwrap_or("");
                let origin=if let Some(rule)=origin.strip_prefix("app-rule:"){json!({"class":"app-rule","ruleName":rule})}
                    else if origin=="person-via-interaction" {json!({"class":origin,"actorRef":settlement["actor"]})}else{json!({"class":origin})};
                let kind=if settlement.get("error").is_some(){"error"}else if e["negative"]==true{"decline"}else{"answer"};
                let mut result=json!({"kind":kind,"origin":origin});
                if let Some(redaction)=settlement.get("contentRedacted") {result["secretValuesPresent"]=json!(true);result["redaction"]=json!({"marker":"secret-answer-values-removed","questionIds":redaction["questionIds"]});}
                else {result["nativeContent"]=settlement.get("error").or_else(||settlement.get("content")).cloned().unwrap_or(Value::Null);}
                record["settlement"]=result;
            }
            record
        }).collect()
    }

    pub fn receive(
        &mut self,
        generation: &Value,
        position: u64,
        frame: &Value,
        capabilities: &Value,
    ) -> Result<Option<Value>, String> {
        if generation.as_object().map(|o| o.len() != 3).unwrap_or(true)
            || generation["appSession"]
                .as_str()
                .map(str::is_empty)
                .unwrap_or(true)
            || generation["home"]
                .as_str()
                .map(str::is_empty)
                .unwrap_or(true)
            || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
            || !(frame["id"].is_string()
                || frame["id"].as_i64().is_some()
                || frame["id"].as_u64().is_some())
        {
            return Err("malformed-request-identity".into());
        }
        if self.closed.contains(generation) {
            return Err("generation-closed".into());
        }
        if self
            .entries
            .iter()
            .any(|e| e["generation"] == *generation && e["requestId"] == frame["id"])
        {
            return Err("duplicate-request-identity".into());
        }
        let method = frame["method"].as_str().ok_or("malformed-request")?;
        let (class, origin, error) = match method {
            "item/tool/call" => (
                "known-app-unsupported",
                "app-rule:no-dynamic-tools",
                Some("App has no registered dynamic tools"),
            ),
            "account/chatgptAuthTokens/refresh" => (
                "known-app-unsupported",
                "app-rule:external-token-login-not-adopted",
                Some("External-token login is not adopted"),
            ),
            "currentTime/read" if capabilities["experimentalApi"] == true => {
                ("known-answerable", "named-service", None)
            }
            m if ANSWERS.iter().any(|(known, _)| *known == m) && m != "currentTime/read" => {
                ("known-answerable", "person-input", None)
            }
            _ => (
                "unfamiliar",
                "app-explicit-error",
                Some("Unrecognized supplier request"),
            ),
        };
        let mut entry = json!({"generation":generation,"requestId":frame["id"],"method":method,"classification":class,
            "nativeParameters":frame.get("params").cloned().unwrap_or(Value::Null),"receiptPosition":position,
            "state":if error.is_some(){"received"}else{"outstanding"},"replyWriteResult":"not-attempted","acknowledgment":"not-observed"});
        let reply = error.map(|message| {
            let content = json!({"code":-32601,"message":message});
            entry["settlement"] = json!({"origin":origin,"error":content});
            entry["state"] = json!("settling");
            json!({"id":frame["id"],"error":content})
        });
        self.entries.push(entry);
        Ok(reply)
    }
    fn index(&self, generation: &Value, id: &Value) -> Result<usize, String> {
        self.entries
            .iter()
            .position(|e| e["generation"] == *generation && e["requestId"] == *id)
            .ok_or("no-such-request".into())
    }
    pub fn prepare(
        &mut self,
        generation: &Value,
        id: &Value,
        answer: &Value,
        origin: &str,
        actor: Option<&str>,
    ) -> Result<Value, String> {
        let idx = self.index(generation, id)?;
        if self.closed.contains(generation) {
            return Err("generation-closed".into());
        }
        let e = &mut self.entries[idx];
        if e["state"] == "resolved-by-supplier" {
            return Err("already-resolved".into());
        }
        if e["state"] != "outstanding" {
            return Err("already-settled".into());
        }
        let method = e["method"].as_str().unwrap();
        let person = origin == "person-via-interaction"
            && actor
                .map(|a| a.starts_with("person:") && a.ends_with(" (identity not verified)"))
                .unwrap_or(false);
        let service = method == "currentTime/read" && origin == "app-rule:current-time";
        let app_negative = origin
            .strip_prefix("app-rule:")
            .map(|rule| !rule.is_empty())
            .unwrap_or(false)
            && negative(method, answer);
        if !person && !service && !app_negative {
            return Err("origin-not-permitted".into());
        }
        validate_answer(method, &e["nativeParameters"], answer)?;
        let mut secret_ids = Vec::new();
        if method == "item/tool/requestUserInput" {
            if let Some(qs) = e["nativeParameters"]["questions"].as_array() {
                for q in qs {
                    if q["isSecret"] == true
                        && answer["answers"]
                            .get(q["id"].as_str().unwrap_or(""))
                            .is_some()
                    {
                        secret_ids.push(q["id"].clone());
                    }
                }
            }
        }
        let is_negative = negative(method, answer);
        // Never retain secret answer bytes even during settling/write failure.
        e["settlement"] = if secret_ids.is_empty() {
            json!({"origin":origin,"actor":actor,"content":answer})
        } else {
            json!({"origin":origin,"actor":actor,"contentRedacted":{"questionIds":secret_ids}})
        };
        e["negative"] = json!(is_negative);
        e["state"] = json!("settling");
        Ok(json!({"id":id,"result":answer}))
    }
    /// Explicit protocol errors belong only to the boundary or a named App rule.
    pub fn prepare_error(
        &mut self,
        generation: &Value,
        id: &Value,
        error: &Value,
        origin: &str,
    ) -> Result<Value, String> {
        let idx = self.index(generation, id)?;
        if self.closed.contains(generation) {
            return Err("generation-closed".into());
        }
        let e = &mut self.entries[idx];
        if e["state"] == "resolved-by-supplier" {
            return Err("already-resolved".into());
        }
        if e["state"] != "outstanding" {
            return Err("already-settled".into());
        }
        if origin != "app-explicit-error"
            && !origin
                .strip_prefix("app-rule:")
                .map(|rule| !rule.is_empty())
                .unwrap_or(false)
        {
            return Err("origin-not-permitted".into());
        }
        if error["code"].as_i64().is_none() || error["message"].as_str().is_none() {
            return Err("invalid-answer".into());
        }
        e["settlement"] = json!({"origin":origin,"error":error});
        // Private source marker: only this successfully admitted later R9
        // operation sets it. Receipt RT02/03 errors never acquire RT14/15.
        e["laterProtocolError"] = json!(true);
        e["state"] = json!("settling");
        Ok(json!({"id":id,"error":error}))
    }
    pub fn written(&mut self, generation: &Value, id: &Value, success: bool) {
        if let Ok(idx) = self.index(generation, id) {
            let e = &mut self.entries[idx];
            if e["state"] != "settling" {
                return;
            }
            e["replyWriteResult"] = json!(if success { "written" } else { "write-failed" });
            e["state"] = json!(if e["settlement"].get("error").is_some()
                && e["laterProtocolError"] != true
            {
                "errored"
            } else if !success {
                "settle-write-failed"
            } else if e["settlement"].get("error").is_some() {
                "errored"
            } else if e["negative"] == true {
                "declined"
            } else {
                "answered"
            });
        }
    }
    pub fn is_closed(&self, generation: &Value) -> bool {
        self.closed.contains(generation)
    }
    pub fn resolved(&mut self, generation: &Value, params: &Value) {
        if self.closed.contains(generation) {
            return;
        }
        if let Ok(idx) = self.index(generation, &params["requestId"]) {
            let e = &mut self.entries[idx];
            if e["nativeParameters"]["threadId"] != params["threadId"] {
                return;
            }
            if e["state"] == "outstanding" {
                e["state"] = json!("resolved-by-supplier");
                e["resolution"] = params.clone();
            } else if (matches!(e["state"].as_str(), Some("answered" | "declined"))
                || (e["state"] == "errored" && e["laterProtocolError"] == true))
                && e["replyWriteResult"] == "written"
            {
                e["acknowledgment"] = json!({"observed":"serverRequest/resolved after written reply","generation":generation,"native":params});
            } else if matches!(e["state"].as_str(), Some("errored" | "settle-write-failed")) {
                // A supplier resolution is real, but does not acknowledge a
                // reply whose write failed, or silently manufacture its success.
                e["resolution"] = params.clone();
            }
        }
    }
    pub fn close(&mut self, generation: &Value) -> usize {
        if !self.closed.contains(generation) {
            self.closed.push(generation.clone());
        }
        let mut ended = 0;
        for e in &mut self.entries {
            if e["generation"] == *generation {
                e["closedGeneration"] = json!(true);
            }
            if e["generation"] == *generation && e["state"] == "outstanding" {
                e["state"] = json!("ended-unanswered");
                e["endCause"] = json!("process-exit");
                ended += 1;
            }
        }
        ended
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn gen() -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":1})
    }
    const ACTOR: &str = "person:Invented/test/unknown (identity not verified)";
    fn receive(r: &mut RequestRegister, method: &str, params: Value) -> Option<Value> {
        r.receive(
            &gen(),
            1,
            &json!({"id":"opaque","method":method,"params":params}),
            &json!({"experimentalApi":false}),
        )
        .unwrap()
    }
    #[test]
    fn unfamiliar_and_unsupported_explicit_error_keeps_unknown_ack() {
        for method in [
            "future/request",
            "attestation/generate",
            "currentTime/read",
            "item/tool/call",
            "account/chatgptAuthTokens/refresh",
        ] {
            let mut r = RequestRegister::default();
            let reply = receive(&mut r, method, json!({"threadId":"t","extra":42})).unwrap();
            assert_eq!(reply["error"]["code"], -32601);
            r.written(&gen(), &json!("opaque"), true);
            assert_eq!(r.entries()[0]["state"], "errored");
            assert_eq!(r.entries()[0]["acknowledgment"], "not-observed");
            assert_eq!(r.entries()[0]["nativeParameters"]["extra"], 42);
        }
    }
    #[test]
    fn refusal_order_offer_and_supplier_resolution() {
        let mut r = RequestRegister::default();
        receive(
            &mut r,
            "item/commandExecution/requestApproval",
            json!({"threadId":"t","availableDecisions":["accept","cancel"]}),
        );
        assert_eq!(
            r.prepare(&gen(), &json!("absent"), &json!({}), "agent", None)
                .unwrap_err(),
            "no-such-request"
        );
        assert_eq!(
            r.prepare(
                &gen(),
                &json!("opaque"),
                &json!({"decision":"accept"}),
                "app-rule:auto",
                None
            )
            .unwrap_err(),
            "origin-not-permitted"
        );
        assert_eq!(
            r.prepare(
                &gen(),
                &json!("opaque"),
                &json!({"decision":"decline"}),
                "person-via-interaction",
                Some(ACTOR)
            )
            .unwrap_err(),
            "invalid-answer"
        );
        assert_eq!(
            decline(
                "item/commandExecution/requestApproval",
                &r.entries()[0]["nativeParameters"]
            ),
            Some(json!({"decision":"cancel"}))
        );
        r.resolved(&gen(), &json!({"threadId":"foreign","requestId":"opaque"}));
        assert_eq!(r.entries()[0]["state"], "outstanding");
        r.resolved(
            &gen(),
            &json!({"threadId":"t","requestId":"opaque","extra":"retained"}),
        );
        assert_eq!(
            r.prepare(&gen(), &json!("opaque"), &json!({}), "agent", None)
                .unwrap_err(),
            "already-resolved"
        );
        r.close(&gen());
        assert_eq!(
            r.prepare(&gen(), &json!("opaque"), &json!({}), "agent", None)
                .unwrap_err(),
            "generation-closed"
        );
    }
    #[test]
    fn written_reply_and_ack_are_separate_and_foreign_generation_cannot_settle() {
        let mut r = RequestRegister::default();
        receive(
            &mut r,
            "item/fileChange/requestApproval",
            json!({"threadId":"t"}),
        );
        let reply = r
            .prepare(
                &gen(),
                &json!("opaque"),
                &json!({"decision":"decline"}),
                "person-via-interaction",
                Some(ACTOR),
            )
            .unwrap();
        assert_eq!(
            reply,
            json!({"id":"opaque","result":{"decision":"decline"}})
        );
        r.written(&gen(), &json!("opaque"), true);
        assert_eq!(r.entries()[0]["state"], "declined");
        assert_eq!(r.entries()[0]["acknowledgment"], "not-observed");
        r.resolved(
            &json!({"appSession":"s","home":"other","spawnCounter":1}),
            &json!({"threadId":"t","requestId":"opaque"}),
        );
        assert_eq!(r.entries()[0]["acknowledgment"], "not-observed");
        r.resolved(&gen(), &json!({"threadId":"t","requestId":"opaque"}));
        assert!(r.entries()[0]["acknowledgment"].is_object());
    }
    #[test]
    fn every_person_answer_kind_has_native_decline_and_schema_refusals() {
        for method in ANSWERS
            .iter()
            .map(|(m, _)| *m)
            .filter(|m| *m != "currentTime/read")
        {
            let mut r = RequestRegister::default();
            receive(&mut r, method, json!({"threadId":"t","questions":[]}));
            let answer = decline(method, &json!({})).unwrap();
            assert_eq!(
                r.prepare(
                    &gen(),
                    &json!("opaque"),
                    &json!({"invented":true}),
                    "person-via-interaction",
                    Some(ACTOR)
                )
                .unwrap_err(),
                "invalid-answer"
            );
            r.prepare(
                &gen(),
                &json!("opaque"),
                &answer,
                "person-via-interaction",
                Some(ACTOR),
            )
            .unwrap();
            r.written(&gen(), &json!("opaque"), true);
            assert_eq!(r.entries()[0]["state"], "declined", "{method}");
        }
    }
    #[test]
    fn secret_values_never_remain_even_when_write_fails() {
        let mut r = RequestRegister::default();
        receive(
            &mut r,
            "item/tool/requestUserInput",
            json!({"threadId":"t","questions":[{"id":"secret","isSecret":true,"isOther":true}]}),
        );
        let reply = r
            .prepare(
                &gen(),
                &json!("opaque"),
                &json!({"answers":{"secret":{"answers":["invented-secret"]}}}),
                "person-via-interaction",
                Some(ACTOR),
            )
            .unwrap();
        assert_eq!(
            reply["result"]["answers"]["secret"]["answers"][0],
            "invented-secret"
        );
        assert!(!serde_json::to_string(&r.entries())
            .unwrap()
            .contains("invented-secret"));
        r.written(&gen(), &json!("opaque"), false);
        assert_eq!(r.entries()[0]["state"], "settle-write-failed");
        assert!(!serde_json::to_string(&r.entries())
            .unwrap()
            .contains("invented-secret"));
    }
    #[test]
    fn no_observer_no_timeout_no_generation_rebinding() {
        let mut r = RequestRegister::default();
        receive(
            &mut r,
            "item/fileChange/requestApproval",
            json!({"threadId":"t"}),
        );
        assert_eq!(r.entries()[0]["state"], "outstanding");
        assert_eq!(r.close(&gen()), 1);
        let new = json!({"appSession":"new","home":"h","spawnCounter":1});
        r.receive(&new,1,&json!({"id":"opaque","method":"item/fileChange/requestApproval","params":{"threadId":"t"}}),&json!({})).unwrap();
        r.resolved(&gen(), &json!({"threadId":"t","requestId":"opaque"}));
        assert_eq!(r.entries()[1]["state"], "outstanding");
    }
}

#[cfg(test)]
mod contract_tests {
    use super::*;
    #[test]
    fn exported_entries_match_adopted_hosting_schema_for_errors_answers_secret_and_resolution() {
        let schema: Value = serde_json::from_str(include_str!(
            "../resources/runtime_core/hosting.server-request-entry.schema.json"
        ))
        .unwrap();
        let validator = jsonschema::options().offline().build(&schema).unwrap();
        let g = json!({"appSession":"s","home":"h","spawnCounter":1});
        for method in [
            "future/request",
            "item/tool/call",
            "item/fileChange/requestApproval",
            "item/tool/requestUserInput",
        ] {
            let mut r = RequestRegister::default();
            r.receive(&g,1,&json!({"id":1,"method":method,"params":{"threadId":"t","turnId":"u","itemId":"i","questions":[{"id":"q","isSecret":true,"isOther":true}]}}),&json!({})).unwrap();
            if method == "item/fileChange/requestApproval" {
                r.prepare(
                    &g,
                    &json!(1),
                    &json!({"decision":"cancel"}),
                    "person-via-interaction",
                    Some("person:Invented/test/unknown (identity not verified)"),
                )
                .unwrap();
            } else if method == "item/tool/requestUserInput" {
                r.prepare(
                    &g,
                    &json!(1),
                    &json!({"answers":{"q":{"answers":["invented-secret"]}}}),
                    "person-via-interaction",
                    Some("person:Invented/test/unknown (identity not verified)"),
                )
                .unwrap();
            }
            r.written(&g, &json!(1), false);
            for record in r.records() {
                validator.validate(&record).unwrap();
                assert!(!serde_json::to_string(&record)
                    .unwrap()
                    .contains("invented-secret"));
            }
        }
        let mut r = RequestRegister::default();
        r.receive(
            &g,
            1,
            &json!({"id":1,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}),
            &json!({}),
        )
        .unwrap();
        r.resolved(&g, &json!({"threadId":"t","requestId":1}));
        validator.validate(&r.records()[0]).unwrap();
    }
}

#[cfg(test)]
mod review_repair_tests {
    use super::*;
    fn g() -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":1})
    }
    fn receive(r: &mut RequestRegister, method: &str) {
        r.receive(
            &g(),
            1,
            &json!({"id":1,"method":method,"params":{"threadId":"t","questions":[]}}),
            &json!({}),
        )
        .unwrap();
    }
    #[test]
    fn closed_generation_refuses_a_new_id_and_keeps_original_entries() {
        let mut r = RequestRegister::default();
        receive(&mut r, "item/fileChange/requestApproval");
        r.close(&g());
        let before = r.records();
        assert_eq!(r.receive(&g(),2,&json!({"id":2,"method":"item/fileChange/requestApproval","params":{"threadId":"t"}}),&json!({})).unwrap_err(),"generation-closed");
        assert_eq!(r.records(), before);
    }
    #[test]
    fn failed_reply_resolution_is_not_a_written_reply_acknowledgment() {
        for method in ["future/request", "item/fileChange/requestApproval"] {
            let mut r = RequestRegister::default();
            receive(&mut r, method);
            if method == "item/fileChange/requestApproval" {
                r.prepare(
                    &g(),
                    &json!(1),
                    &json!({"decision":"decline"}),
                    "app-rule:invented-negative",
                    None,
                )
                .unwrap();
            }
            r.written(&g(), &json!(1), false);
            let before = r.entries()[0]["state"].clone();
            r.resolved(
                &g(),
                &json!({"threadId":"t","requestId":1,"cause":"supplier-native"}),
            );
            let record = &r.records()[0];
            assert_eq!(record["state"], before);
            assert_eq!(record["replyWriteResult"], "write-failed");
            assert_eq!(
                record["acknowledgmentObservation"]["status"],
                "not-observed"
            );
            assert_eq!(
                record["supplierResolution"]["source"],
                "serverRequest/resolved"
            );
            assert_eq!(record["supplierResolution"]["cause"], "supplier-native");
        }
    }
    #[test]
    fn named_app_rules_may_decline_or_error_person_input_but_cannot_supply_content() {
        let schema: Value = serde_json::from_str(include_str!(
            "../resources/runtime_core/hosting.server-request-entry.schema.json"
        ))
        .unwrap();
        let validator = jsonschema::options().offline().build(&schema).unwrap();
        for method in [
            "item/tool/requestUserInput",
            "mcpServer/elicitation/request",
        ] {
            let mut r = RequestRegister::default();
            receive(&mut r, method);
            let content = if method == "item/tool/requestUserInput" {
                json!({"answers":{"unknown":{"answers":["invented"]}}})
            } else {
                json!({"action":"accept","content":{}})
            };
            assert_eq!(
                r.prepare(&g(), &json!(1), &content, "app-rule:invented", None)
                    .unwrap_err(),
                "origin-not-permitted"
            );
            r.prepare(
                &g(),
                &json!(1),
                &decline(method, &json!({})).unwrap(),
                "app-rule:invented-negative",
                None,
            )
            .unwrap();
            r.written(&g(), &json!(1), true);
            assert_eq!(r.records()[0]["state"], "declined");
            validator.validate(&r.records()[0]).unwrap();
            let mut r = RequestRegister::default();
            receive(&mut r, method);
            let error = json!({"code":-32603,"message":"invented rule error"});
            assert_eq!(
                r.prepare_error(&g(), &json!(1), &error, "person-via-interaction")
                    .unwrap_err(),
                "origin-not-permitted"
            );
            assert_eq!(
                r.prepare_error(&g(), &json!(1), &error, "app-rule:invented-error")
                    .unwrap(),
                json!({"id":1,"error":error})
            );
            r.written(&g(), &json!(1), true);
            validator.validate(&r.records()[0]).unwrap();
            assert_eq!(r.records()[0]["settlement"]["kind"], "error");
        }
    }
}

#[cfg(test)]
mod form_alias_validation_tests {
    use super::*;
    const ACTOR: &str = "person:synthetic alias tester (identity not verified)";
    const METHOD: &str = "mcpServer/elicitation/request";
    const MODES: &[&str] = &["form", "openai/form", "openaiForm"];
    fn generation() -> Value {
        json!({"appSession":"synthetic","home":"synthetic-home","spawnCounter":1})
    }
    fn register(params: Value) -> RequestRegister {
        let mut register = RequestRegister::default();
        assert!(register
            .receive(
                &generation(),
                1,
                &json!({"id":"alias","method":METHOD,"params":params}),
                &json!({})
            )
            .unwrap()
            .is_none());
        register
    }
    fn parameters(mode: &str) -> Value {
        json!({"mode":mode,"serverName":"synthetic-server","threadId":"thread","message":"synthetic form","requestedSchema":{"type":"object","properties":{"answer":{"type":"string","minLength":2}},"required":["answer"],"additionalProperties":false},"nativeUnknown":"retained"})
    }
    #[test]
    fn each_supported_form_alias_validates_direct_content_before_reply_and_retains_native_parameters(
    ) {
        for mode in MODES {
            let params = parameters(mode);
            let mut register = register(params.clone());
            let before = register.entries();
            for invalid in [
                json!({"answer":7}),
                json!({}),
                json!({"answer":""}),
                json!({"answer":"valid","notRequested":true}),
                json!(null),
            ] {
                let answer = json!({"action":"accept","content":invalid,"_meta":null});
                assert_eq!(
                    register
                        .prepare(
                            &generation(),
                            &json!("alias"),
                            &answer,
                            "person-via-interaction",
                            Some(ACTOR)
                        )
                        .unwrap_err(),
                    "invalid-answer",
                    "mode {mode}"
                );
                assert_eq!(
                    register.entries(),
                    before,
                    "invalid reply must leave custody unchanged for {mode}"
                );
            }
            let valid = json!({"action":"accept","content":{"answer":"valid"},"_meta":null});
            assert_eq!(
                register
                    .prepare(
                        &generation(),
                        &json!("alias"),
                        &valid,
                        "person-via-interaction",
                        Some(ACTOR)
                    )
                    .unwrap(),
                json!({"id":"alias","result":valid})
            );
            assert_eq!(register.entries()[0]["nativeParameters"], params);
            assert_eq!(register.entries()[0]["nativeParameters"]["mode"], *mode);
            assert_eq!(
                register.entries()[0]["settlement"]["origin"],
                "person-via-interaction"
            );
        }
    }
    #[test]
    fn each_alias_requires_requested_schema_and_refuses_unretrievable_references_offline() {
        for mode in MODES {
            for schema in [
                None,
                Some(json!(false)),
                Some(json!({"$ref":"https://example.invalid/schema-that-must-not-be-retrieved"})),
            ] {
                let mut params = parameters(mode);
                match schema {
                    Some(schema) => params["requestedSchema"] = schema,
                    None => {
                        params.as_object_mut().unwrap().remove("requestedSchema");
                    }
                }
                let mut register = register(params);
                let before = register.entries();
                assert_eq!(
                    register
                        .prepare(
                            &generation(),
                            &json!("alias"),
                            &json!({"action":"accept","content":{"answer":"valid"}}),
                            "person-via-interaction",
                            Some(ACTOR)
                        )
                        .unwrap_err(),
                    "invalid-answer",
                    "mode {mode}"
                );
                assert_eq!(register.entries(), before);
            }
        }
    }
    #[test]
    fn aliases_and_nonform_modes_keep_exact_negative_shapes_and_origin_guards() {
        for mode in
            MODES
                .iter()
                .copied()
                .chain(["url", "openai/userVerification", "future/unrecognized"])
        {
            for action in ["decline", "cancel"] {
                let mut params = parameters(mode);
                params["requestedSchema"] = json!(false);
                let mut register = register(params.clone());
                let negative = json!({"action":action,"content":null,"_meta":null});
                assert_eq!(
                    register
                        .prepare(
                            &generation(),
                            &json!("alias"),
                            &negative,
                            "person-via-interaction",
                            Some(ACTOR)
                        )
                        .unwrap(),
                    json!({"id":"alias","result":negative})
                );
                assert_eq!(register.entries()[0]["nativeParameters"], params);
            }
        }
        for mode in MODES {
            let mut register = register(parameters(mode));
            assert_eq!(
                register
                    .prepare(
                        &generation(),
                        &json!("alias"),
                        &json!({"action":"accept","content":{"answer":"valid"}}),
                        "app-rule:synthetic-affirmative",
                        None
                    )
                    .unwrap_err(),
                "origin-not-permitted"
            );
        }
    }
}
