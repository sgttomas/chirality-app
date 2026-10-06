//! EXEC current-phase required-tool compatibility. Checkpoints are guidance, never holds.
use crate::workflow_declaration::{Declaration, Reading};
use serde::Serialize;
use serde_json::Value;
use std::collections::BTreeMap;
#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    Present,
    PresentCurrentlyUnavailable,
    Missing,
    VersionMismatch,
    NotExposedOnThisSurface,
    ChannelNotEnabled,
    NotEstablished,
}
#[derive(Debug, Clone)]
pub struct Operation {
    pub version: String,
    pub exposure: Option<bool>,
    pub availability: Option<bool>,
}
#[derive(Debug, Clone, Default)]
pub struct Environment {
    pub catalog: Option<BTreeMap<String, Operation>>,
    pub channel_enabled: bool,
    pub harness_signals: Option<Value>,
    pub harness_pin: Option<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct ToolResult {
    pub name: String,
    pub necessity: String,
    pub outcome: Outcome,
    pub reason: String,
}
#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Check {
    Compatible,
    Unsupported,
    NotEstablished,
}
#[derive(Debug, Clone, Serialize)]
pub struct Compatibility {
    pub result: Check,
    pub tools: Vec<ToolResult>,
    pub checkpoints_are_guidance: bool,
    pub findings: Vec<String>,
}
impl Compatibility {
    pub fn check_for_role(
        declaration: &Declaration,
        env: &Environment,
        role: Option<&str>,
    ) -> Self {
        let mut result = Self::check(declaration, env);
        if let Some(roles) = declaration
            .raw
            .as_ref()
            .and_then(|v| v.get("compatible_roles"))
        {
            if let Some(list) = roles.as_array() {
                if list.is_empty()
                    || list.iter().any(|v| {
                        v.as_str().is_none_or(|s| {
                            !["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"].contains(&s)
                        })
                    })
                {
                    result.result = Check::NotEstablished;
                    result
                        .findings
                        .push("compatible roles not established".into());
                } else if !list.iter().any(|v| v.as_str() == role) {
                    result.result = Check::Unsupported;
                    result.findings.push(format!(
                        "workflow is written for {roles}; role in force {}",
                        role.unwrap_or("no role")
                    ));
                }
            } else {
                result.result = Check::NotEstablished;
                result
                    .findings
                    .push("compatible roles not established".into());
            }
        }
        if role == Some("TASK")
            && declaration
                .elements
                .get("required_tools")
                .into_iter()
                .flatten()
                .any(|e| {
                    e.reading == Reading::Recognized
                        && e.value["capability"] == "agent-delegation"
                        && e.value["necessity"] == "required"
                })
        {
            result.result = Check::Unsupported;
            result
                .findings
                .push("TASK does not delegate (stated limit, not enforced)".into());
        }
        result
    }
    pub fn check(declaration: &Declaration, env: &Environment) -> Self {
        let mut tools = vec![];
        let mut unknown = declaration.reading != Reading::Recognized
            || !matches!(
                declaration.categories.get("required_tools"),
                Some(Reading::Recognized | Reading::DeclaredEmpty)
            );
        let mut blocked = false;
        for e in declaration
            .elements
            .get("required_tools")
            .into_iter()
            .flatten()
        {
            let v = &e.value;
            let (outcome, reason) = if e.reading != Reading::Recognized {
                (
                    Outcome::NotEstablished,
                    "required-tool element not established".into(),
                )
            } else if v["class"] == "harness_capability" {
                harness_presence(v["capability"].as_str().unwrap_or(""), env)
            } else {
                host_presence(v, env)
            };
            let necessity = v["necessity"].as_str();
            // Optionality must itself be established. A malformed/missing
            // necessity cannot remove an unknown requirement from the verdict.
            let required = necessity == Some("required");
            if !matches!(necessity, Some("required" | "optional")) {
                unknown = true;
            }

            if required {
                blocked |= matches!(
                    outcome,
                    Outcome::Missing
                        | Outcome::VersionMismatch
                        | Outcome::NotExposedOnThisSurface
                        | Outcome::ChannelNotEnabled
                );
                unknown |= outcome == Outcome::NotEstablished;
            }
            tools.push(ToolResult {
                name: v["name"].as_str().unwrap_or("<unestablished>").into(),
                necessity: v["necessity"].as_str().unwrap_or("unknown").into(),
                outcome,
                reason,
            });
        }
        Self {
            result: if blocked {
                Check::Unsupported
            } else if unknown {
                Check::NotEstablished
            } else {
                Check::Compatible
            },
            tools,
            checkpoints_are_guidance: true,
            findings: declaration.findings.clone(),
        }
    }
}
fn host_presence(v: &Value, e: &Environment) -> (Outcome, String) {
    let Some(cat) = &e.catalog else {
        return (
            Outcome::NotEstablished,
            "catalog unreadable or not read".into(),
        );
    };
    let operation = v["operation"].as_str().unwrap_or("");
    let Some(op) = cat.get(operation) else {
        return (
            Outcome::Missing,
            "operation absent from observed catalog edition".into(),
        );
    };
    if v["versions"]
        .as_array()
        .is_some_and(|a| !a.iter().any(|version| version == &op.version))
    {
        return (
            Outcome::VersionMismatch,
            "version compatibility: exact equality only".into(),
        );
    }
    match op.exposure {
        None => return (Outcome::NotEstablished, "surface exposure unagreed".into()),
        Some(false) => {
            return (
                Outcome::NotExposedOnThisSurface,
                "operation not exposed on selected surface".into(),
            )
        }
        _ => {}
    }
    if !e.channel_enabled {
        return (
            Outcome::ChannelNotEnabled,
            "selected channel not enabled".into(),
        );
    }
    if op.availability == Some(false) {
        (
            Outcome::PresentCurrentlyUnavailable,
            "operation present; evaluated runtime precondition unavailable".into(),
        )
    } else {
        (Outcome::Present, String::new())
    }
}
fn harness_presence(name: &str, e: &Environment) -> (Outcome, String) {
    if e.harness_pin.as_deref() != Some("App Codex 0.158.0") {
        return (
            Outcome::NotEstablished,
            "no adopted supplier availability account at acting pin".into(),
        );
    }
    let Some(s) = &e.harness_signals else {
        return (
            Outcome::NotEstablished,
            "availability signals not read".into(),
        );
    };
    let caps = &s["provider_capabilities"];
    let cfg = &s["effective_config"];
    let start = &s["thread_start"];
    let result: Option<bool> = match name {
        "shell-command" | "file-change" => {
            if start.get("approvalPolicy").is_some() && start.get("sandbox").is_some() {
                Some(true)
            } else {
                None
            }
        }
        "web-search" => caps["webSearch"]
            .as_bool()
            .zip(s["web_search_mode"].as_str())
            .map(|(b, m)| b && m != "disabled"),
        "agent-delegation" => {
            // Missing wins over any unread signal (RV21-B / NPTD §7.1).
            if s["model_multi_agent_version"] == "disabled"
                || cfg["features"]["multi_agent"] == false
                || caps["namespaceTools"] == false
            {
                Some(false)
            } else if cfg.is_object()
                && caps["namespaceTools"] == true
                && ["v1", "v2"]
                    .iter()
                    .any(|v| s["model_multi_agent_version"] == *v)
            {
                Some(true)
            } else {
                None
            }
        }
        "dynamic-tool-call" => start["dynamicTools"].as_array().map(|a| !a.is_empty()),
        "image-generation" => caps["imageGeneration"].as_bool(),
        "mcp-tool-call" => s["mcp_server_status"].as_array().and_then(|a| {
            if a.iter().any(|x| {
                x["runtimeStatus"] == "connected"
                    && x["tools"].as_object().is_some_and(|t| !t.is_empty())
            }) {
                if caps["namespaceTools"] == false {
                    None
                } else {
                    Some(true)
                }
            } else if a.iter().any(|x| {
                x.get("toolsError").is_some()
                    || !matches!(x["runtimeStatus"].as_str(), Some("connected" | "stopped"))
            }) {
                None
            } else {
                Some(false)
            }
        }),
        _ => None,
    };
    match result {
        Some(true) => (Outcome::Present, String::new()),
        Some(false) => (
            Outcome::Missing,
            "supplier availability signal reads unavailable".into(),
        ),
        None => (
            Outcome::NotEstablished,
            "presence rule inactive or availability signal unread".into(),
        ),
    }
}

#[cfg(test)] mod original_negative { use super::*; use serde_json::json; #[test] fn original_negative_known_tool_failure_survives_unknown_role_declaration() { let value=json!({"declaration_contract_version":"WD-v0.8","required_tools":[{"name":"read","class":"host_operation","operation":"example.read","purpose":"Read basis","necessity":"required","stages":["Method"]}],"compatible_roles":"invalid","checkpoints":[],"returned_outputs":[],"returned_evidence":[]}); let d=crate::workflow_declaration::read(&format!("```workflow-declaration\n{value}\n```\n")).unwrap(); let env=Environment{catalog:Some(BTreeMap::new()),channel_enabled:true,..Default::default()}; assert_eq!(Compatibility::check_for_role(&d,&env,None).result,Check::Unsupported); }}
