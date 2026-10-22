//! ACCESS §2/§11 admission from one genuine private config/read.
use super::*;

/// Private construction, no Serde: a source/cwd observation, not a native config lock.
pub(crate) struct ProviderAdmission {
    source: SourceRequest,
    cwd: String,
    provider: String,
    model: String,
    entry: String,
    config: Value,
    children: Option<ChildStartGuard>,
    config_link: Option<crate::child_roles::ConfigLink>,
}
struct ChildStartGuard { namespace: crate::child_roles::Namespace, config: Value, files: Vec<crate::child_roles::ChildSupply> }
const LIMIT: &str = "Access entry unavailable: current provider configuration could not be established; no thread/start sent";
fn unavailable() -> String {
    LIMIT.into()
}
const PROVIDER_FIELDS: &[&str] = &[
    "name",
    "base_url",
    "model_catalog_url",
    "env_key",
    "env_key_instructions",
    "experimental_bearer_token",
    "auth",
    "gateway_oauth",
    "aws",
    "wire_api",
    "query_params",
    "http_headers",
    "env_http_headers",
    "request_max_retries",
    "stream_max_retries",
    "stream_idle_timeout_ms",
    "websocket_connect_timeout_ms",
    "requires_openai_auth",
    "supports_websockets",
    "supports_standalone_web_search",
];
const OBSERVATION_LIMIT: &str = "Configured provider observation unavailable; private values and diagnostics withheld. Manual explicit choices remain independent and Start requires a fresh private reading.";
struct PrivateConfigReading {
    source: SourceRequest,
    cwd: String,
    config: Value,
}

// Publication is deliberately stricter than private operation eligibility.
fn public_id(id: &str) -> bool {
    (1..=64).contains(&id.len())
        && id.as_bytes()[0].is_ascii_alphabetic()
        && id
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b"._-".contains(&b))
}
fn public_endpoint(value: &Value) -> Option<&str> {
    let text = value.as_str()?;
    if text.len() > 2048
        || !text.bytes().all(|b| (33..=126).contains(&b))
        || text.bytes().any(|b| b"@?#\\%".contains(&b))
    {
        return None;
    }
    let rest = text
        .strip_prefix("http://")
        .or_else(|| text.strip_prefix("https://"))?;
    if let Some((_, path)) = rest.split_once('/') {
        if !path
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b"-._~/".contains(&b))
        {
            return None;
        }
    }
    let parsed = tauri::Url::parse(text).ok()?;
    if !matches!(parsed.scheme(), "http" | "https")
        || parsed.host_str().is_none()
        || !parsed.username().is_empty()
        || parsed.password().is_some()
        || parsed.query().is_some()
        || parsed.fragment().is_some()
    {
        return None;
    }
    // Withhold parser reinterpretations instead of displaying a sanitized URL
    // as the reported endpoint. Only an implicit trailing slash is equivalent.
    if parsed.as_str() != text && parsed.as_str() != format!("{text}/") {
        return None;
    }
    Some(text)
}

/// Ephemeral, bounded source-known reflection exclusion. Never stored on Host,
/// serialized, hashed, or treated as an oracle for hidden/covert credentials.
struct PrivateReflections {
    values: Vec<String>,
    nodes: usize,
    bytes: usize,
}
impl PrivateReflections {
    fn new(response: &Value) -> Result<Self, ()> {
        let mut set = Self {
            values: Vec::new(),
            nodes: 0,
            bytes: 0,
        };
        set.scan(response, false, 0)?;
        Ok(set)
    }
    fn remember(&mut self, value: &str, depth: usize) -> Result<(), ()> {
        if depth > 3 || value.len() > 4096 || self.values.len() >= 256 {
            return Err(());
        }
        let lower = value.to_ascii_lowercase();
        if self.values.contains(&lower) {
            return Ok(());
        }
        self.values.push(lower);
        let trimmed = value.trim();
        if trimmed != value {
            self.remember(trimmed, depth + 1)?;
        }
        if let Some((prefix, tail)) = trimmed.split_once(' ') {
            if prefix.eq_ignore_ascii_case("basic") {
                return Err(());
            } // unestablished encoded auth shape
            if prefix.eq_ignore_ascii_case("bearer") || prefix.eq_ignore_ascii_case("token") {
                self.remember(tail.trim(), depth + 1)?;
            }
        }
        if value.starts_with('"') || value.contains('\\') {
            let decoded = serde_json::from_str::<String>(value)
                .or_else(|_| serde_json::from_str::<String>(&format!("\"{value}\"")))
                .map_err(|_| ())?;
            if decoded != value {
                self.remember(&decoded, depth + 1)?;
            }
        }
        if value.contains('%') {
            let mut decoded = Vec::new();
            let bytes = value.as_bytes();
            let mut at = 0;
            while at < bytes.len() {
                if bytes[at] == b'%' {
                    let hex = bytes.get(at + 1..at + 3).ok_or(())?;
                    let text = std::str::from_utf8(hex).map_err(|_| ())?;
                    decoded.push(u8::from_str_radix(text, 16).map_err(|_| ())?);
                    at += 3;
                } else {
                    decoded.push(bytes[at]);
                    at += 1;
                }
            }
            let decoded = String::from_utf8(decoded).map_err(|_| ())?;
            self.remember(&decoded, depth + 1)?;
        }
        if value.contains("://") {
            let url = tauri::Url::parse(value).map_err(|_| ())?;
            let canonical = url.as_str();
            if canonical != value {
                self.remember(canonical, depth + 1)?;
            }
            for part in [
                Some(url.username()).filter(|v| !v.is_empty()),
                url.password(),
                url.fragment(),
            ] {
                if let Some(part) = part {
                    self.remember(part, depth + 1)?;
                }
            }
            for (_, part) in url.query_pairs() {
                self.remember(&part, depth + 1)?;
            }
            if let Some(parts) = url.path_segments() {
                for part in parts.filter(|part| !part.is_empty()) {
                    self.remember(part, depth + 1)?;
                }
            }
        }
        Ok(())
    }
    fn scan(&mut self, value: &Value, sensitive: bool, depth: usize) -> Result<(), ()> {
        self.nodes += 1;
        if self.nodes > 4096 || depth > 24 || self.bytes > 262_144 {
            return Err(());
        }
        match value {
            Value::Object(fields) => {
                for (key, value) in fields {
                    self.bytes = self.bytes.checked_add(key.len()).ok_or(())?;
                    if self.bytes > 262_144 {
                        return Err(());
                    }
                    let normalized = key.to_ascii_lowercase().replace(['-', '_'], "");
                    let channel = credential_name(key)
                        || matches!(
                            normalized.as_str(),
                            "envkey"
                                | "envkeyinstructions"
                                | "experimentalbearertoken"
                                | "auth"
                                | "gatewayoauth"
                                | "aws"
                                | "httpheaders"
                                | "envhttpheaders"
                                | "queryparams"
                                | "loginid"
                                | "authurl"
                                | "verificationurl"
                                | "usercode"
                                | "accesskeyid"
                                | "secretaccesskey"
                                | "sessiontoken"
                                | "refreshtoken"
                                | "clientsecret"
                                | "bearertoken"
                                | "idtoken"
                                | "credentials"
                                | "oauth"
                                | "headers"
                                | "env"
                                | "environment"
                                | "envvars"
                        );
                    if !value.is_null() && channel {
                        let object = matches!(
                            normalized.as_str(),
                            "auth"
                                | "gatewayoauth"
                                | "aws"
                                | "credentials"
                                | "oauth"
                                | "httpheaders"
                                | "envhttpheaders"
                                | "queryparams"
                                | "headers"
                                | "env"
                                | "environment"
                        );
                        if (object && !value.is_object()) || (!object && !value.is_string()) {
                            return Err(());
                        }
                        if matches!(
                            normalized.as_str(),
                            "httpheaders"
                                | "envhttpheaders"
                                | "queryparams"
                                | "headers"
                                | "env"
                                | "environment"
                        ) && value.as_object().unwrap().values().any(|v| !v.is_string())
                        {
                            return Err(());
                        }
                    }
                    if sensitive {
                        self.remember(key, 0)?;
                    }
                    self.scan(value, sensitive || channel, depth + 1)?;
                }
            }
            Value::Array(values) => {
                if sensitive {
                    return Err(());
                }
                for value in values {
                    self.scan(value, false, depth + 1)?;
                }
            }
            Value::String(text) => {
                self.bytes = self.bytes.checked_add(text.len()).ok_or(())?;
                if self.bytes > 262_144 {
                    return Err(());
                }
                if sensitive {
                    self.remember(text, 0)?;
                } else if let Ok(url) = tauri::Url::parse(text) {
                    // URL credential/query/fragment scalars can also occur in
                    // a filtered provider or another configuration/layer role.
                    for part in [
                        Some(url.username()).filter(|v| !v.is_empty()),
                        url.password(),
                        url.fragment(),
                    ] {
                        if let Some(part) = part {
                            self.remember(part, 0)?;
                        }
                    }
                    for (_, part) in url.query_pairs() {
                        self.remember(&part, 0)?;
                    }
                }
            }
            Value::Null => {}
            scalar => {
                if sensitive {
                    self.remember(&scalar.to_string(), 0)?;
                }
            }
        }
        Ok(())
    }
    fn excludes(&self, text: &str) -> bool {
        let lower = text.to_ascii_lowercase();
        self.values.iter().any(|value| lower.contains(value))
    }
    fn excludes_value(&self, value: &Value) -> bool {
        match value {
            Value::String(text) => self.excludes(text),
            Value::Object(fields) => fields.values().any(|v| self.excludes_value(v)),
            Value::Array(items) => items.iter().any(|v| self.excludes_value(v)),
            Value::Null => false,
            other => self.excludes(&other.to_string()),
        }
    }
}

fn project_configured_providers(
    reading: &PrivateConfigReading,
    project: &Value,
) -> Result<Value, String> {
    let fail = || OBSERVATION_LIMIT.to_owned();
    // Scan the WHOLE response before filtering credentialed/unsupported entries.
    let reflections = PrivateReflections::new(&reading.config).map_err(|_| fail())?;
    let definitions = reading.config["config"]["model_providers"]
        .as_object()
        .ok_or_else(fail)?;
    if definitions.len() > 128 {
        return Err(fail());
    }
    let scope = json!({"generation":reading.source.generation(),"cwd":reading.cwd,"projectContext":project,"modeHomeClass":"account","readRevision":reading.source.request_ref});
    if reflections.excludes_value(&scope) {
        return Err(fail());
    }
    let mut rows = Vec::new();
    let mut withheld = false;
    for (id, definition) in definitions {
        // Unknown provider shapes cannot support response-wide exclusion.
        let def = definition.as_object().ok_or_else(fail)?;
        if def
            .keys()
            .any(|key| !PROVIDER_FIELDS.contains(&key.as_str()))
        {
            return Err(fail());
        }
        let endpoint = definition.get("base_url").and_then(public_endpoint);
        if classify(&reading.config, "local-provider", id).is_err()
            || !public_id(id)
            || endpoint.is_none()
            || reflections.excludes(id)
            || reflections.excludes(endpoint.unwrap())
        {
            withheld = true;
            continue;
        }
        rows.push(json!({"id":id,"label":"Configured local provider","endpoint":endpoint.unwrap(),"wireApi":"responses"}));
    }
    let view = json!({"state":"observed","schema":"ConfigReadResponse","scope":scope,"rows":rows,"limit":if withheld {"Some configured definitions or metadata were withheld; no private names, values or diagnostics are offered"} else {"Configured metadata only; not authentication, reachability, model/capability availability or Start authority"}});
    if reflections.excludes_value(&view) {
        return Err(fail());
    }
    Ok(view)
}

/// Native errors can quote credential values. Public consumers keep outcome only.
pub(super) fn withheld(frame: &Value) -> Value {
    let mut safe = json!({"privateConfigWithheld":true});
    if let Some(id) = frame.get("id") {
        safe["id"] = id.clone();
    }
    if frame.get("method").is_some()
        || frame.get("error").is_some() && frame.get("result").is_some()
    {
        safe["observation"] = json!("private configuration envelope unavailable; body withheld");
    } else if let Some(error) = frame.get("error") {
        if let Some(code) = error["code"].as_i64() {
            safe["error"] = json!({"code":code,"message":"Native configuration read refused; private diagnostic withheld"});
        } else {
            safe["observation"] =
                json!("private configuration error shape unavailable; body withheld");
        }
    } else if frame.get("result").is_some() {
        safe["result"] = json!({});
    }
    safe
}

fn credential_name(key: &str) -> bool {
    let key = key.to_ascii_lowercase().replace(['-', '_'], "");
    matches!(
        key.as_str(),
        "authorization"
            | "proxyauthorization"
            | "apikey"
            | "xapikey"
            | "token"
            | "accesstoken"
            | "secret"
            | "password"
            | "key"
    )
}
fn url_without_credentials(value: &Value) -> Result<(), String> {
    let Some(text) = value.as_str().filter(|s| !s.trim().is_empty()) else {
        return Err(unavailable());
    };
    let url = tauri::Url::parse(text).map_err(|_| unavailable())?;
    if !matches!(url.scheme(), "http" | "https") || url.host_str().is_none() {
        return Err(unavailable());
    }
    if !url.username().is_empty()
        || url.password().is_some()
        || url.query_pairs().any(|(key, _)| credential_name(&key))
    {
        return Err("Access entry not offered: selected provider definition carries a credential element; no thread/start sent".into());
    }
    // Untyped query data has no credential-absence contract. Do not claim one.
    if url.query().is_some() {
        return Err(unavailable());
    }
    Ok(())
}
fn classify(result: &Value, entry: &str, provider: &str) -> Result<(), String> {
    let definitions = result["config"]
        .get("model_providers")
        .and_then(Value::as_object)
        .ok_or_else(unavailable)?;
    match entry {
        "chatgpt-account" | "api-key" => {
            if provider != "openai" || definitions.contains_key("openai") {
                return Err("Access entry unavailable: cloud entry requires the reported built-in OpenAI provider; no thread/start sent".into());
            }
            Ok(())
        }
        "local-provider" => {
            if provider == "openai" {
                return Err(unavailable());
            }
            let def=definitions.get(provider).and_then(Value::as_object).ok_or_else(||"Access entry unavailable: selected local provider is not reported in current configuration; no thread/start sent".to_owned())?;
            // Stock 0.160.0 reports these fields, including explicit nulls. New
            // untyped fields cannot establish credential absence.
            if def.keys().any(|key| !PROVIDER_FIELDS.contains(&key.as_str())) {
                return Err(unavailable());
            }
            // ConfigReadResponse leaves provider definitions untyped. Validate
            // known roles too: a familiar key alone establishes no field shape.
            if !def.get("name").is_some_and(Value::is_string) {
                return Err(unavailable());
            }
            for field in [
                "base_url",
                "model_catalog_url",
                "env_key",
                "env_key_instructions",
                "experimental_bearer_token",
            ] {
                if def
                    .get(field)
                    .is_some_and(|v| !v.is_null() && !v.is_string())
                {
                    return Err(unavailable());
                }
            }
            for field in [
                "request_max_retries",
                "stream_max_retries",
                "stream_idle_timeout_ms",
                "websocket_connect_timeout_ms",
            ] {
                if def
                    .get(field)
                    .is_some_and(|v| !v.is_null() && v.as_u64().is_none())
                {
                    return Err(unavailable());
                }
            }
            for field in [
                "requires_openai_auth",
                "supports_websockets",
                "supports_standalone_web_search",
            ] {
                if def.get(field).is_some_and(|v| !v.is_boolean()) {
                    return Err(unavailable());
                }
            }
            for field in ["auth", "gateway_oauth", "aws"] {
                if def
                    .get(field)
                    .is_some_and(|v| !v.is_null() && !v.is_object())
                {
                    return Err(unavailable());
                }
            }
            for field in ["http_headers", "env_http_headers", "query_params"] {
                if let Some(value) = def.get(field).filter(|v| !v.is_null()) {
                    if value
                        .as_object()
                        .is_none_or(|map| map.values().any(|v| !v.is_string()))
                    {
                        return Err(unavailable());
                    }
                }
            }
            // The identified supplier's effective definition explicitly reports
            // these nullable auth channels. Omission is not an absence oracle.
            const AUTH: &[&str] = &[
                "env_key",
                "experimental_bearer_token",
                "auth",
                "gateway_oauth",
                "aws",
            ];
            if AUTH.iter().any(|key| !def.contains_key(*key))
                || ["http_headers", "env_http_headers", "query_params"]
                    .iter()
                    .any(|key| !def.contains_key(*key))
                || !def.contains_key("requires_openai_auth")
            {
                return Err(unavailable());
            }
            let carries = |key: &str| def.get(key).is_some_and(|v| !v.is_null());
            if AUTH.iter().any(|key| carries(key))
                || def.get("requires_openai_auth") == Some(&json!(true))
            {
                return Err("Access entry not offered: selected provider definition carries a credential element; no thread/start sent".into());
            }
            if def
                .get("requires_openai_auth")
                .is_some_and(|v| !v.is_boolean())
                || def.get("wire_api").and_then(Value::as_str) != Some("responses")
            {
                return Err(unavailable());
            }
            url_without_credentials(def.get("base_url").ok_or_else(unavailable)?)?;
            if let Some(catalog) = def.get("model_catalog_url").filter(|v| !v.is_null()) {
                url_without_credentials(catalog)?;
            }
            for field in ["http_headers", "env_http_headers", "query_params"] {
                if let Some(map) = def.get(field).filter(|v| !v.is_null()) {
                    let map = map.as_object().ok_or_else(unavailable)?;
                    if map.keys().any(|key| credential_name(key)) {
                        return Err("Access entry not offered: selected provider definition carries a credential element; no thread/start sent".into());
                    }
                    // Only these fixed HTTP header roles are known non-auth.
                    // Arbitrary query/env/header maps remain unestablished.
                    if !map.is_empty()
                        && (field != "http_headers"
                            || map.iter().any(|(k, v)| {
                                !matches!(
                                    k.to_ascii_lowercase().as_str(),
                                    "accept" | "content-type" | "user-agent" | "openai-beta"
                                ) || !v.is_string()
                            }))
                    {
                        return Err(unavailable());
                    }
                }
            }
            Ok(())
        }
        _ => Err("Access entry unavailable: unsupported entry kind; no thread/start sent".into()),
    }
}
impl Host {
    pub(crate) fn provider_admission_read(
        &self,
        generation: &Value,
        cwd: &str,
        entry: &str,
        provider: &str,
        model: &str,
    ) -> Result<ProviderAdmission, String> {
        self.provider_admission_read_within(
            generation,
            cwd,
            entry,
            provider,
            model,
            Duration::from_secs(10),
        )
    }
    pub(crate) fn provider_admission_read_within(
        &self,
        generation: &Value,
        cwd: &str,
        entry: &str,
        provider: &str,
        model: &str,
        wait: Duration,
    ) -> Result<ProviderAdmission, String> {
        crate::recovery::generation_ref(generation).map_err(|_| unavailable())?;
        if cwd.is_empty() || provider.trim().is_empty() || model.trim().is_empty() {
            return Err(unavailable());
        }
        let reading = self.private_provider_config_read(generation, cwd, wait, false)?;
        classify(&reading.config, entry, provider)?;
        let proof = ProviderAdmission {
            source: reading.source,
            cwd: cwd.into(),
            provider: provider.into(),
            model: model.into(),
            entry: entry.into(),
            config: reading.config,
            children: None,
            config_link: None,
        };
        let i = self.inner.0.lock().unwrap();
        self.check_provider_admission(
            &i,
            &proof,
            &json!({"cwd":cwd,"modelProvider":provider,"model":model}),
        )?;
        Ok(proof)
    }
    fn private_provider_config_read(
        &self,
        generation: &Value,
        cwd: &str,
        wait: Duration,
        person: bool,
    ) -> Result<PrivateConfigReading, String> {
        crate::recovery::generation_ref(generation).map_err(|_| unavailable())?;
        if cwd.is_empty() {
            return Err(unavailable());
        }
        let source = self
            .request_begin_with_access_offer(
                "config/read",
                json!({"cwd":cwd,"includeLayers":true}),
                if person {
                    json!({"kind":"person-directed","name":"configured-provider-observation"})
                } else {
                    json!({"kind":"app-rule","name":"access-provider-admission"})
                },
                false,
                Some(generation),
                false,
                None,
                None,
                None,
                None,
                true,
                None,
            )
            .map_err(|_| unavailable())?;
        #[cfg(test)]
        if let Some(hook) = self.before_provider_wait.lock().unwrap().as_ref() {
            hook(self, &source);
        }
        let received = source.receiver.lock().unwrap().recv_timeout(wait);
        // End every private wait, including malformed/error/timeout/stale paths.
        // Late replies arrive reduced. Drain only this receipt's receiver.
        self.delegation_wait_ended(&source);
        while source.receiver.lock().unwrap().try_recv().is_ok() {}
        let frame = received.map_err(|_| unavailable())?;
        if frame.get("id") != Some(source.request_id())
            || frame.get("method").is_some()
            || frame.get("error").is_some()
        {
            return Err(unavailable());
        }
        let result = frame.get("result").ok_or_else(unavailable)?;
        Self::validate_native_result("ConfigReadResponse", result).map_err(|_| unavailable())?;
        Ok(PrivateConfigReading {
            source,
            cwd: cwd.into(),
            config: result.clone(),
        })
    }
    pub(crate) fn configured_provider_read(
        &self,
        generation: &Value,
        cwd: &str,
        project: &Value,
    ) -> Result<Value, String> {
        self.configured_provider_read_within(generation, cwd, project, Duration::from_secs(10))
    }
    pub(crate) fn configured_provider_read_within(
        &self,
        generation: &Value,
        cwd: &str,
        project: &Value,
        wait: Duration,
    ) -> Result<Value, String> {
        let read = self
            .private_provider_config_read(generation, cwd, wait, true)
            .map_err(|_| OBSERVATION_LIMIT.to_owned())?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| OBSERVATION_LIMIT.to_owned())?;
        let view = project_configured_providers(&read, project)?;
        self.check_provider_read(&self.inner.0.lock().unwrap(), &read.source, cwd)
            .map_err(|_| OBSERVATION_LIMIT.to_owned())?;
        Ok(view)
    }
    /// Non-authoritative current observation revision for the ordinary chooser.
    /// This is generated source metadata, never a private configuration value.
    pub(crate) fn configured_provider_revision(&self, generation: &Value, cwd: &str) -> Value {
        let i = self.inner.0.lock().unwrap();
        if i.generation != *generation
            || i.state != "ready"
            || i.server_requests.is_closed(generation)
        {
            return Value::Null;
        }
        i.provider_read_revisions
            .get(cwd)
            .filter(|(g, _)| g == generation)
            .map(|(_, revision)| json!(revision))
            .unwrap_or(Value::Null)
    }
    fn check_provider_read(
        &self,
        i: &Inner,
        source: &SourceRequest,
        cwd: &str,
    ) -> Result<(), String> {
        let actual = source.source.upgrade().ok_or_else(unavailable)?;
        let e = i
            .source_requests
            .get(&source.request_id().to_string())
            .ok_or_else(unavailable)?;
        if i.provider_read_revisions.get(cwd)
            != Some(&(source.generation.clone(), source.request_ref.clone()))
            || !Arc::ptr_eq(&actual, &self.inner)
            || i.generation != source.generation
            || i.state != "ready"
            || i.server_requests.is_closed(&source.generation)
            || e.request.request_ref != source.request_ref
            || e.request.frame != source.frame
            || !e.private_config
            || !e.written
            || e.write_attempt_in_progress
            || e.write_error.is_some()
            || e.source_limit.is_some()
            || e.response_position.is_none()
            || e.source_pipe
                .is_none_or(|(epoch, _)| epoch != i.attachment_pipe_epoch)
            || e.response
                .as_ref()
                .is_none_or(|r| r.get("result").is_none() || r["privateConfigWithheld"] != true)
            || source.frame["method"] != "config/read"
            || source.frame["params"]["cwd"] != cwd
        {
            return Err("Access entry unavailable: original provider reading superseded/unavailable or destination/source differs; no thread/start sent".into());
        }
        Ok(())
    }
    pub(super) fn check_provider_admission(
        &self,
        i: &Inner,
        proof: &ProviderAdmission,
        params: &Value,
    ) -> Result<(), String> {
        self.check_provider_read(i, &proof.source, &proof.cwd)?;
        if params["cwd"] != proof.cwd
            || params["modelProvider"] != proof.provider
            || params["model"] != proof.model
        {
            return Err("Access entry unavailable: original provider reading superseded/unavailable or destination/source differs; no thread/start sent".into());
        }
        if let Some(children) = &proof.children {
            if params.get("config") != Some(&children.config) {
                return Err("Native child configuration differs from the prepared observation; no start sent".into());
            }
        }
        Ok(())
    }
    pub(crate) fn role_config_link(
        &self,
        proof: &mut ProviderAdmission,
        link: crate::child_roles::ConfigLink,
    ) {
        proof.config_link = Some(link);
    }
    pub(super) fn recheck_child_sources(&self, proof: &ProviderAdmission) -> Result<(), String> {
        if let Some(children) = &proof.children {
            children.namespace.recheck()?;
            for child in &children.files {
                child.recheck()?;
            }
        }
        Ok(())
    }
    pub(crate) fn prepare_role_children(
        &self,
        proof: &mut ProviderAdmission,
        composition: &mut crate::role_supply::Composition,
        instructions: &std::path::Path,
        data: &std::path::Path,
    ) -> Result<(), String> {
        let reading = (|| {
            {
                let i = self
                    .inner
                    .0
                    .lock()
                    .map_err(|_| "Native source unavailable".to_string())?;
                self.check_provider_admission(
                    &i,
                    proof,
                    &json!({"cwd":proof.cwd,"modelProvider":proof.provider,"model":proof.model}),
                )?;
                let pin = i
                    .version_identity
                    .as_ref()
                    .ok_or("unsupported-native-child-supplier")?;
                if pin["declaredPin"]!="0.160.0"||!pin["distributionContentIdentity"].as_array().is_some_and(|rows|rows.iter().any(|r|r["path"]=="bin/codex"&&r["identity"]["algorithm"]=="sha-256"&&r["identity"]["value"]=="112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b")){return Err("unsupported-native-child-supplier".into())}
            }
            crate::child_roles::Namespace::observe_linked(&proof.config, proof.config_link.clone())
        })();
        let namespace = crate::child_roles::prepare(composition, reading, instructions, data);
        if !composition.children.is_empty() {
            // Config-layer/source coherence is a separate requirement from an
            // equal filesystem rereading. A newer native read always replaces
            // the provider proof; a changed response never promotes absence.
            let refreshed = self.provider_admission_read(
                &proof.source.generation,
                &proof.cwd,
                &proof.entry,
                &proof.provider,
                &proof.model,
            )?;
            let stable = refreshed.config == proof.config
                && namespace.as_ref().is_some_and(|n| n.recheck().is_ok());
            let link = proof.config_link.clone();
            *proof = refreshed;
            proof.config_link = link;
            if stable {
                proof.children = namespace.map(|namespace| ChildStartGuard {
                    namespace,
                    config: composition.native_config(),
                    files: composition.children.clone(),
                });
            } else {
                crate::child_roles::prepare(
                    composition,
                    Err("Native role reading changed".into()),
                    instructions,
                    data,
                );
            }
        }
        Ok(())
    }
    pub(crate) fn thread_start_with_role_dispatch(
        &self,
        proof: &ProviderAdmission,
        composition: &crate::role_supply::Composition,
    ) -> Result<SourceRequest, String> {
        composition.verify()?;
        let (mut params, project) = self.offered_start_params(
            &proof.cwd,
            &proof.model,
            &proof.provider,
            Some(&composition.text),
        )?;
        if !composition.children.is_empty() {
            params["config"] = composition.native_config();
        }
        if proof.children.is_some() != !composition.children.is_empty() {
            return Err("Native child preparation source unavailable; no start sent".into());
        }
        crate::role_supply::check_role_inputs(
            "thread/start",
            &json!({"developerInstructions":composition.text,"config":composition.native_config()}),
        )?;
        self.request_begin_with_access_offer(
            "thread/start",
            params,
            json!({"kind":"person-directed"}),
            false,
            Some(&proof.source.generation),
            false,
            None,
            None,
            None,
            project,
            false,
            Some(proof),
        )
    }
    pub(crate) fn thread_start_with_access_dispatch(
        &self,
        proof: &ProviderAdmission,
        guidance: &str,
    ) -> Result<SourceRequest, String> {
        let (params, project) =
            self.offered_start_params(&proof.cwd, &proof.model, &proof.provider, Some(guidance))?;
        self.request_begin_with_access_offer(
            "thread/start",
            params,
            json!({"kind":"person-directed"}),
            false,
            Some(&proof.source.generation),
            false,
            None,
            None,
            None,
            project,
            false,
            Some(proof),
        )
    }
}

#[cfg(all(test, unix))]
mod tests {
    include!("access_provider_tests.rs");
}
