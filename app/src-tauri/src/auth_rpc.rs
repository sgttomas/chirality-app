//! Unit A method-aware account RPC observation. No credential store/home/UI.
use serde_json::{json, Value};
pub const REDACTED: &str = "[account RPC: sensitive value withheld; not original bytes]";
pub const ERROR_REDACTED: &str =
    "[account RPC: native auth diagnostic withheld; original text unavailable]";
/// No Clone/Debug/Deserialize or public real-entry/renderer constructor.
pub(crate) struct TransientApiKey {
    value: String,
}
impl TransientApiKey {
    #[cfg(test)]
    pub(super) fn synthetic(value: &str) -> Self {
        Self {
            value: value.into(),
        }
    }
    pub(crate) fn into_params(self) -> Value {
        json!({"type":"apiKey","apiKey":self.value})
    }
}
pub fn account_method(method: &str) -> bool {
    method.starts_with("account/")
        || matches!(
            method,
            "configRequirements/read"
                | "modelProvider/authRecoveryStarted"
                | "modelProvider/authRecoveryCompleted"
        )
}
fn credential_key(key: &str) -> bool {
    matches!(
        key,
        "apiKey" | "accessToken" | "secretAccessKey" | "sessionToken" | "accessKeyId"
    )
}
fn presentation_key(key: &str) -> bool {
    matches!(key, "authUrl" | "verificationUrl" | "userCode")
}
fn has_credentials(value: &Value) -> bool {
    match value {
        Value::Object(fields) => fields
            .iter()
            .any(|(key, value)| credential_key(key) || has_credentials(value)),
        Value::Array(items) => items.iter().any(has_credentials),
        _ => false,
    }
}
pub fn generic_guard(method: &str, params: &Value) -> Result<(), String> {
    if account_method(method) && has_credentials(params)
        || method == "account/login/start"
            && matches!(
                params["type"].as_str(),
                Some("apiKey" | "chatgptAuthTokens" | "amazonBedrock" | "amazonBedrockAccessKeys")
            )
    {
        return Err("credential-bearing account RPC requires private transient source; generic route refused without send".into());
    }
    if method == "account/login/start"
        && !matches!(
            params["type"].as_str(),
            Some("chatgpt" | "chatgptDeviceCode")
        )
    {
        return Err(
            "unsupported/malformed generic account login mode; no credential frame sent".into(),
        );
    }
    if method == "getAuthStatus" && params["includeToken"] == true {
        return Err("token-inclusive status is not supported by this App boundary".into());
    }
    if method == "account/read" && params["refreshToken"] == true {
        return Err("App account read does not force token refresh".into());
    }
    Ok(())
}
/// Build a fresh projection without cloning a raw sensitive field first.
fn fields(value: &Value, auth: bool) -> Value {
    match value {
        Value::Object(object) => Value::Object(
            object
                .iter()
                .map(|(key, value)| {
                    let projected = if credential_key(key)
                        || presentation_key(key)
                        || key == "loginId"
                    {
                        json!(REDACTED)
                    } else if auth && matches!(key.as_str(), "success" | "requiresOpenaiAuth") {
                        if value.is_boolean() {
                            value.clone()
                        } else {
                            json!(REDACTED)
                        }
                    } else if auth && key == "type" {
                        match value.as_str() {
                            Some("apiKey") => json!("apiKey"),
                            Some("chatgpt") => json!("chatgpt"),
                            Some("chatgptDeviceCode") => json!("chatgptDeviceCode"),
                            Some("chatgptAuthTokens") => json!("chatgptAuthTokens"),
                            Some("amazonBedrock") => json!("amazonBedrock"),
                            _ => json!(REDACTED),
                        }
                    } else if auth
                        && matches!(key.as_str(), "error" | "message" | "diagnostic" | "details")
                    {
                        if key == "error" && value.is_object() {
                            let mut error = serde_json::Map::new();
                            if let Some(code) =
                                value.get("code").filter(|code| code.as_i64().is_some())
                            {
                                error.insert("code".into(), code.clone());
                            }
                            error.insert("message".into(), json!(ERROR_REDACTED));
                            if value.get("data").is_some() {
                                error.insert("data".into(), json!(REDACTED));
                            }
                            Value::Object(error)
                        } else {
                            json!(ERROR_REDACTED)
                        }
                    } else if auth && key == "data" {
                        json!(REDACTED)
                    } else {
                        fields(value, auth)
                    };
                    (key.clone(), projected)
                })
                .collect(),
        ),
        Value::Array(items) => Value::Array(items.iter().map(|item| fields(item, auth)).collect()),
        _ => value.clone(),
    }
}
/// Structural framing only, not published method validation or success proof.
/// Unknown but framed native notifications retain the ordinary receiving path.
pub fn protocol_envelope(frame: &Value) -> bool {
    let Some(object) = frame.as_object() else {
        return false;
    };
    let id = object.get("id");
    let valid_id =
        id.is_some_and(|v| v.is_string() || v.as_i64().is_some() || v.as_u64().is_some());
    if object.get("method").is_some_and(Value::is_string) {
        return id.is_none() || valid_id;
    }
    valid_id
        && object.get("method").is_none()
        && (object.contains_key("result") || object.contains_key("error"))
}
pub fn project_frame(frame: &Value, correlated_method: Option<&str>) -> (Value, bool) {
    let method = frame
        .get("method")
        .and_then(Value::as_str)
        .or(correlated_method);
    let auth = method.is_some_and(account_method);
    if !auth {
        return (frame.clone(), false);
    }
    let mut projected = fields(frame, true);
    if let Some(result) = frame.get("result") {
        projected["result"] = match correlated_method {
            Some("account/login/start") => {
                let kind = match result["type"].as_str() {
                    Some("apiKey") => json!("apiKey"),
                    Some("chatgpt") => json!("chatgpt"),
                    Some("chatgptDeviceCode") => json!("chatgptDeviceCode"),
                    Some("chatgptAuthTokens") => json!("chatgptAuthTokens"),
                    Some("amazonBedrock") => json!("amazonBedrock"),
                    _ => json!(REDACTED),
                };
                let mut safe = json!({"type":kind});
                // Unit A offers no OAuth/device control. Login IDs are unavailable,
                // including extra fields on API-key responses, never arbitrary strings.
                if matches!(
                    result["type"].as_str(),
                    Some("chatgpt" | "chatgptDeviceCode")
                ) {
                    for key in ["loginId", "authUrl", "verificationUrl", "userCode"] {
                        if result.get(key).is_some() {
                            safe[key] = json!(REDACTED);
                        }
                    }
                }
                safe
            }
            Some("account/read") => {
                let mut safe = json!({});
                if let Some(value) = result.get("requiresOpenaiAuth") {
                    safe["requiresOpenaiAuth"] = if value.is_boolean() {
                        value.clone()
                    } else {
                        json!(REDACTED)
                    };
                }
                if let Some(account) = result.get("account") {
                    safe["account"] = if account.is_null() {
                        Value::Null
                    } else {
                        match account["type"].as_str() {
                            Some("apiKey") => json!({"type":"apiKey"}),
                            Some("chatgpt") => json!({"type":"chatgpt","detailsUnavailable":true}),
                            _ => json!(REDACTED),
                        }
                    };
                }
                safe
            }
            Some("account/logout") => {
                if result.is_object() {
                    json!({})
                } else {
                    json!(REDACTED)
                }
            }
            Some("configRequirements/read") => {
                let mut safe = json!({});
                if let Some(req) = result.get("requirements") {
                    safe["requirements"] = if req.is_null() {
                        Value::Null
                    } else if req.is_object() {
                        let mut r = json!({});
                        if let Some(allowed) = req.get("allowedLoginMethods") {
                            r["allowedLoginMethods"] = if allowed.is_null() {
                                Value::Null
                            } else if let Some(items) = allowed.as_array() {
                                Value::Array(
                                    items
                                        .iter()
                                        .map(|v| match v.as_str() {
                                            Some("api") => json!("api"),
                                            Some("chatgpt") => json!("chatgpt"),
                                            _ => json!(REDACTED),
                                        })
                                        .collect(),
                                )
                            } else {
                                json!(REDACTED)
                            };
                        }
                        r
                    } else {
                        json!(REDACTED)
                    };
                }
                safe
            }
            _ => projected["result"].clone(),
        };
    }
    (projected, true)
}
pub fn login_policy(response: Option<&Value>) -> Result<&'static str, String> {
    let Some(response) = response else {
        return Ok("policy unavailable/unknown; not permission evidence");
    };
    if response.get("error").is_some() {
        return Ok("native policy read failed/unknown; not permission evidence");
    }
    if !response.get("result").is_some_and(Value::is_object) {
        return Ok("native policy shape unavailable/unknown; not permission evidence");
    }
    let allowed = response["result"]["requirements"].get("allowedLoginMethods");
    match allowed {
        Some(Value::Array(methods)) => {
            if methods
                .iter()
                .any(|m| !matches!(m.as_str(), Some("api" | "chatgpt")))
            {
                return Err("native login restriction malformed; no key frame written".into());
            }
            if !methods.iter().any(|m| m == "api") {
                return Err("native login policy excludes API-key entry; no key frame written or config changed".into());
            }
            Ok("native api method listed; native login still decides")
        }
        None | Some(Value::Null) => Ok("restriction absent/null; policy permission unknown"),
        _ => Err("native login restriction malformed; no key frame written".into()),
    }
}
pub fn typed_observation(
    method: &str,
    frame: &Value,
    native_shape_valid: bool,
    requested_mode: Option<&str>,
) -> Value {
    if !native_shape_valid {
        return json!({"state":"native shape/envelope invalid or unavailable; typed account standing unknown","credentialValidity":"unknown","identityVerified":false});
    }
    if frame.get("error").is_some() {
        return json!({"state":"native error observed; diagnostic redacted","code":frame["error"].get("code"),"credentialValidity":"unknown","identityVerified":false});
    }
    let result = &frame["result"];
    match method {
        "account/login/start" => {
            json!({"state":if result["type"]=="apiKey" && requested_mode==Some("apiKey"){"native API-key presence reported; validity unknown until actual use"}else{"unexpected native login result; presence unknown"},"nativeType":result["type"],"credentialValidity":"unknown","identityVerified":false})
        }
        "account/read" => {
            json!({"state":if result.get("account").is_none(){"account omitted; unknown/unavailable"}else if result["account"].is_null(){"native account null observed"}else{"native account type observed"},"account":result.get("account"),"requiresOpenaiAuth":result.get("requiresOpenaiAuth"),"identityVerified":false})
        }
        "account/logout" => {
            json!({"state":"native acknowledgment only; no filesystem removal/history deletion or turn end inferred","identityVerified":false})
        }
        _ => json!({"state":"source observation only; no policy/auth/actor qualification"}),
    }
}
