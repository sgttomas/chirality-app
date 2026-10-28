//! Original live child-event custody, separate from stored/forked transcript pages.
use super::*;
#[derive(Clone, Debug)]
pub(crate) struct NativeChildStart {
    generation: Value,
    parent: String,
    child: String,
    turn: String,
    item: String,
    position: u64,
}
impl NativeChildStart {
    pub(super) fn capture(generation: &Value, frame: &Value) -> Option<Self> {
        if frame.get("id").is_some() || frame["method"] != "item/completed" {
            return None;
        }
        let p = &frame["params"];
        let item = &p["item"];
        if item["type"] != "subAgentActivity"
            || item["kind"] != "started"
            || Host::validate_native_result("ItemCompletedNotification", p).is_err()
        {
            return None;
        }
        let parent = p["threadId"].as_str()?.to_owned();
        let child = item["agentThreadId"].as_str()?.to_owned();
        let turn = p["turnId"].as_str()?.to_owned();
        let id = item["id"].as_str()?.to_owned();
        if parent.is_empty() || child.is_empty() || turn.is_empty() || id.is_empty() {
            return None;
        }
        Some(Self {
            generation: generation.clone(),
            parent,
            child,
            turn,
            item: id,
            position: 0,
        })
    }
    pub(super) fn at_receipt(mut self, position: u64) -> Self {
        self.position = position;
        self
    }

    pub(crate) fn generation(&self) -> &Value {
        &self.generation
    }
    pub(crate) fn parent(&self) -> &str {
        &self.parent
    }
    pub(crate) fn child(&self) -> &str {
        &self.child
    }
    pub(crate) fn key(&self) -> String {
        json!([
            self.generation,
            self.parent,
            self.child,
            self.item,
            self.position
        ])
        .to_string()
    }
    pub(crate) fn evidence(&self) -> Value {
        json!({"generation":self.generation,"parentThreadId":self.parent,"threadId":self.child,"turnId":self.turn,"itemId":self.item,"receiptPosition":self.position,"source":"live item/completed subAgentActivity(kind=started)"})
    }
}
impl Host {
    pub(crate) fn observed_child_starts(&self) -> Vec<NativeChildStart> {
        self.inner.0.lock().unwrap().native_child_events.clone()
    }
    pub(crate) fn acknowledge_child_starts(&self, events: &[NativeChildStart]) {
        let keys = events
            .iter()
            .map(NativeChildStart::key)
            .collect::<std::collections::BTreeSet<_>>();
        self.inner
            .0
            .lock()
            .unwrap()
            .native_child_events
            .retain(|event| !keys.contains(&event.key()));
    }
    pub(crate) fn parent_child_carrier_current(
        &self,
        event: &NativeChildStart,
        original: &crate::role_lifecycle::RoleBinding,
    ) -> bool {
        if !original.original_child_carrier(event.generation())
            || original.thread() != event.parent()
        {
            return false;
        }
        let i = self.inner.0.lock().unwrap();
        if i.generation != event.generation
            || i.state != "ready"
            || i.server_requests.is_closed(&event.generation)
        {
            return false;
        }
        let Some(start) = i
            .source_requests
            .values()
            .find(|s| s.request.request_ref() == original.original_request_ref())
        else {
            return false;
        };
        start.written
            && start.response_position.is_some_and(|p| p < event.position)
            && start.request.generation == event.generation
            && !i.source_requests.values().any(|s| {
                s.request.generation == event.generation
                    && s.request.frame["method"] == "thread/resume"
                    && s.request.frame["params"]["threadId"] == event.parent
                    && s.request.request_id().as_u64() > start.request.request_id().as_u64()
            })
    }
    pub(crate) fn child_metadata_dispatch(
        &self,
        event: &NativeChildStart,
    ) -> Result<SourceRequest, String> {
        // The opaque event was constructed from an actual source notification.
        // No renderer JSON or stored page can create it.
        if event.parent == event.child {
            return Err("Child guidance unknown: native self reference".into());
        }
        self.request_begin_scoped(
            "thread/read",
            json!({"threadId":event.child,"includeTurns":false}),
            json!({"kind":"app-rule","name":"native-child-guidance-association"}),
            false,
            Some(&event.generation),
        )
    }
    pub(crate) fn child_metadata_finish(
        &self,
        event: &NativeChildStart,
        source: &SourceRequest,
    ) -> Result<Option<Value>, String> {
        let status = self.source_request_status(source)?;
        if status["sourceCurrent"] != true || source.generation() != &event.generation {
            return Err("Child guidance unknown: source generation ended".into());
        }
        if status["response"].is_null() {
            return Ok(None);
        }
        let frame = &status["response"];
        if status["writeResult"] != "written"
            || status["outcome"] != "response-observed-result"
            || status["sentFrame"]["method"] != "thread/read"
            || status["sentFrame"]["params"] != json!({"threadId":event.child,"includeTurns":false})
            || frame.get("id") != Some(source.request_id())
            || frame.get("method").is_some()
            || frame.get("error").is_some()
        {
            return Err("Child guidance unknown: metadata request/response mismatch".into());
        }
        Self::validate_native_result("ThreadReadResponse", &frame["result"])
            .map_err(|_| "Child guidance unknown: native metadata shape unavailable")?;
        let thread = &frame["result"]["thread"];
        if thread["id"] != event.child
            || thread["parentThreadId"] != event.parent
            || !thread["forkedFromId"].is_null()
            || thread["source"]["subAgent"]["thread_spawn"]["parent_thread_id"] != event.parent
            || thread["source"]["subAgent"]["thread_spawn"]["agent_role"] != thread["agentRole"]
        {
            return Err(
                "Child guidance unknown: native child/parent/fork identity mismatch".into(),
            );
        }
        while source.receiver.lock().unwrap().try_recv().is_ok() {}
        Ok(Some(thread.clone()))
    }
}
