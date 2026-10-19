//! Continue-as observations use the original Host-issued source, never a
//! renderer status, a last-request search or an error string as send evidence.
use super::*;

#[derive(Clone)]
pub(crate) enum HandoffSendObservation {
    NotAttempted(String),
    Sent(Value),
    NativeFailed(Value),
    Unknown(String),
}

impl Host {
    /// Every Err exits the existing factory before actual dispatch. Once a
    /// source was reserved, that factory returns it even after write failure.
    pub(crate) fn handoff_text_begin(
        &self,
        generation: &Value,
        thread: &str,
        text: &str,
    ) -> Result<SourceRequest, String> {
        crate::recovery::generation_ref(generation)?;
        let params = Self::text_turn_params(thread, text)?;
        self.request_begin_scoped(
            "turn/start",
            params,
            json!({"kind":"person-directed"}),
            false,
            Some(generation),
        )
    }

    pub(crate) fn handoff_text_wait(&self, source: &SourceRequest, wait: Duration) {
        // The caller already retained this exact source. A wait error is not
        // evidence that no attempt happened; read the original source below.
        let _ = self.wait_source_response(source, wait);
    }

    /// Current physical attachment is separate from a historical response.
    /// Reporting an old acknowledgment never re-admits its old pipe/generation.
    pub(crate) fn handoff_source_current(&self, source: &SourceRequest) -> bool {
        if self.check_source(source).is_err() {
            return false;
        }
        let i = self.inner.0.lock().unwrap();
        let Some(e) = i.source_requests.get(&source.request_id().to_string()) else {
            return false;
        };
        if e.request.generation != source.generation
            || e.request.frame != source.frame
            || e.request.request_ref != source.request_ref
            || i.generation != source.generation
            || i.state != "ready"
            || i.server_requests.is_closed(&source.generation)
        {
            return false;
        }
        let pipe = self.stdin.lock().unwrap();
        e.source_pipe.is_some_and(|(epoch, identity)| {
            epoch == i.attachment_pipe_epoch
                && pipe
                    .as_ref()
                    .and_then(|pipe| Self::pipe_identity(pipe).ok())
                    == Some(identity)
        })
    }

    /// Read-only, including after the original generation ended. A historical
    /// acknowledgment confers no current operation, role or admission authority.
    pub(crate) fn handoff_send_observation(
        &self,
        source: &SourceRequest,
        generation: &Value,
        thread: &str,
        text: &str,
    ) -> HandoffSendObservation {
        use HandoffSendObservation::*;
        if let Err(reason) = self.check_source(source) {
            return Unknown(reason);
        }
        let params = &source.frame["params"];
        if source.generation != *generation
            || source.frame["method"] != "turn/start"
            || params["threadId"] != thread
            || params["input"]
                .as_array()
                .and_then(|input| input.last())
                .and_then(|input| input["text"].as_str())
                != Some(text)
        {
            return Unknown(
                "The retained original handoff sender/target/text differs; no replacement lookup"
                    .into(),
            );
        }
        let i = self.inner.0.lock().unwrap();
        let Some(e) = i.source_requests.get(&source.request_id().to_string()) else {
            return Unknown("Original source receipt unavailable".into());
        };
        if e.request.generation != source.generation
            || e.request.frame != source.frame
            || e.request.request_ref != source.request_ref
        {
            return Unknown(
                "Original source receipt changed during observation; no replacement lookup".into(),
            );
        }
        if e.write_attempt_in_progress {
            return Unknown("The original physical write has not settled".into());
        }
        if e.attempt_position.is_none() {
            return if let Some(reason) = &e.source_limit {
                NotAttempted(reason.clone())
            } else {
                Unknown("The original writer has no settled attempt observation".into())
            };
        }
        if !e.written || e.write_error.is_some() || e.source_pipe.is_none() {
            return Unknown("The original write did not establish a complete frame; partial submission remains unknown".into());
        }
        let Some(response) = &e.response else {
            return Unknown("No native response to the original request is observed; submission remains unknown".into());
        };
        if response.get("id") != Some(source.request_id())
            || response.get("method").is_some()
            || e.response_position.is_none()
            || response.get("error").is_some() && response.get("result").is_some()
        {
            return Unknown("Original native response is malformed or contradictory".into());
        }
        if let Some(error) = response.get("error") {
            return if error["code"].as_i64().is_some() && error["message"].is_string() {
                NativeFailed(response.clone())
            } else {
                Unknown("Original native error has no valid code/message".into())
            };
        }
        if response
            .get("result")
            .and_then(|result| result.get("turn"))
            .is_some_and(Self::native_turn_shape)
        {
            Sent(response.clone())
        } else {
            Unknown("Original response establishes no valid native turn result".into())
        }
    }
}

#[cfg(test)]
impl Host {
    pub(crate) fn handoff_test_block_writer<T>(&self, operation: impl FnOnce() -> T) -> T {
        let _writer = self.frame_write.lock().unwrap();
        operation()
    }
}
