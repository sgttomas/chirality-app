//! ACCESS §2/§11 admission from one genuine private config/read.
use super::*;

/// Private construction, no Serde: a source/cwd observation, not a native config lock.
pub(crate) struct ProviderAdmission {
    source: SourceRequest,
    cwd: String,
    provider: String,
    model: String,
}
const LIMIT: &str = "Access entry unavailable: current provider configuration could not be established; no thread/start sent";
fn unavailable() -> String {
    LIMIT.into()
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
            const KNOWN: &[&str] = &[
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
            if def.keys().any(|key| !KNOWN.contains(&key.as_str())) {
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
        let source = self
            .request_begin_with_access_offer(
                "config/read",
                json!({"cwd":cwd,"includeLayers":true}),
                json!({"kind":"app-rule","name":"access-provider-admission"}),
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
        classify(result, entry, provider)?;
        let proof = ProviderAdmission {
            source,
            cwd: cwd.into(),
            provider: provider.into(),
            model: model.into(),
        };
        let i = self.inner.0.lock().unwrap();
        self.check_provider_admission(
            &i,
            &proof,
            &json!({"cwd":cwd,"modelProvider":provider,"model":model}),
        )?;
        Ok(proof)
    }
    pub(super) fn check_provider_admission(
        &self,
        i: &Inner,
        proof: &ProviderAdmission,
        params: &Value,
    ) -> Result<(), String> {
        let actual = proof.source.source.upgrade().ok_or_else(unavailable)?;
        let e = i
            .source_requests
            .get(&proof.source.request_id().to_string())
            .ok_or_else(unavailable)?;
        if i.provider_read_revisions.get(&proof.cwd)
            != Some(&(
                proof.source.generation.clone(),
                proof.source.request_ref.clone(),
            ))
            || !Arc::ptr_eq(&actual, &self.inner)
            || i.generation != proof.source.generation
            || i.state != "ready"
            || i.server_requests.is_closed(&proof.source.generation)
            || e.request.request_ref != proof.source.request_ref
            || e.request.frame != proof.source.frame
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
            || params["cwd"] != proof.cwd
            || params["modelProvider"] != proof.provider
            || params["model"] != proof.model
        {
            return Err("Access entry unavailable: original provider reading superseded/unavailable or destination/source differs; no thread/start sent".into());
        }
        Ok(())
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
