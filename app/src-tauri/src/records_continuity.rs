//! DEL-04-03-owned REC receiver values. Unverified operational metadata only.
//! These small pointers establish no role, act, run or supplier authentication.
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Clone)]
pub(super) struct Project {
    pub reference: Option<String>,
    pub directory: Value,
}

pub(super) const OWNER: &str = "DEL-04-03";
#[derive(Clone, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub(super) struct Source {
    pub generation: String,
    pub request: String,
    pub rpc: u64,
    pub method: String,
    pub thread: String,
}
#[derive(Clone, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub(super) struct Receipt {
    format: String,
    version: String,
    pub home: String,
    pub home_class: String,
    pub thread: String,
    pub project: String,
    pub directory: Value,
    definition: String,
    offered: Source,
    pub admitted: Source,
    pub from: Option<String>,
}
pub(super) fn definition_identity() -> String {
    crate::util::sha256_hex(
        &serde_json::to_vec(&crate::records_access::definition())
            .expect("supported definition serializes"),
    )
}
impl Source {
    pub fn new(
        generation: &Value,
        request: &str,
        rpc: &Value,
        method: &str,
        thread: &str,
    ) -> Result<Self, String> {
        Ok(Self {
            generation: crate::recovery::generation_ref(generation)?,
            request: request.into(),
            rpc: rpc.as_u64().ok_or("original App request ID unavailable")?,
            method: method.into(),
            thread: thread.into(),
        })
    }
}
impl Receipt {
    pub fn start(
        home: &str,
        thread: &str,
        project: &str,
        directory: Value,
        source: Source,
    ) -> Self {
        Self {
            format: "chirality.records-capability.receipt".into(),
            version: "0.1".into(),
            home: home.into(),
            home_class: String::new(),
            thread: thread.into(),
            project: project.into(),
            directory,
            definition: definition_identity(),
            offered: source.clone(),
            admitted: source,
            from: None,
        }
    }
    pub fn fork(&self, thread: &str, source: Source) -> Self {
        Self {
            thread: thread.into(),
            admitted: source,
            from: Some(self.thread.clone()),
            ..self.clone()
        }
    }
    pub fn encode(&self) -> Result<String, String> {
        serde_json::to_string(self).map_err(|_| "records receipt encoding unavailable".into())
    }
    pub fn decode(value: &str) -> Result<Self, String> {
        if value.len() > 8192 {
            return Err("records receipt exceeds its compact bound".into());
        }
        let receipt: Self = serde_json::from_str(value)
            .map_err(|_| "records receipt malformed or unsupported".to_string())?;
        if receipt.format != "chirality.records-capability.receipt"
            || receipt.version != "0.1"
            || receipt.definition != definition_identity()
        {
            return Err("records receipt definition or format unsupported".into());
        }
        if !matches!(receipt.home_class.as_str(), "H-acct" | "H-key")
            || receipt.home.is_empty()
            || receipt.thread.is_empty()
            || receipt.project.is_empty()
        {
            return Err("records receipt owning context unknown".into());
        }
        for source in [&receipt.offered, &receipt.admitted] {
            let generation = crate::recovery::generation_from_ref(&source.generation)?;
            if generation["home"] != receipt.home
                || source.request.is_empty()
                || source.thread.is_empty()
            {
                return Err("records receipt source association differs".into());
            }
        }
        if receipt.offered.method != "thread/start" || receipt.admitted.thread != receipt.thread {
            return Err("records receipt admission association differs".into());
        }
        match receipt.from.as_deref() {
            None if receipt.offered == receipt.admitted
                && receipt.admitted.method == "thread/start" =>
            {
                ()
            }
            Some(from)
                if !from.is_empty()
                    && from != receipt.thread
                    && receipt.admitted.method == "thread/fork" =>
            {
                ()
            }
            _ => {
                return Err("records receipt original offering or fork association differs".into())
            }
        }
        Ok(receipt)
    }
}

impl super::Host {
    pub(super) fn records_offer_is_current(
        inner: &super::Inner,
        generation: &Value,
        thread: &Value,
    ) -> bool {
        inner
            .records_offers
            .iter()
            .any(|(g, t)| g == generation && t == thread)
            && inner
                .records_capability
                .as_ref()
                .and_then(|capability| capability.project_identity().ok())
                .is_some_and(|project| {
                    inner.records_offer_projects.iter().any(|(g, t, expected)| {
                        g == generation && t == thread && *expected == project
                    })
                })
            && inner
                .records_receipts
                .iter()
                .find(|(g, t, _)| g == generation && Some(t.as_str()) == thread.as_str())
                .is_none_or(|(_, _, receipt)| {
                    inner
                        .records_project_context
                        .as_ref()
                        .and_then(|context| context.reference())
                        == Some(receipt.project.as_str())
                })
    }
    fn records_binding_view(&self, generation: &Value, thread: &str, view: Value) {
        let mut inner = self.inner.0.lock().unwrap();
        if let Some(row) = inner
            .threads
            .iter_mut()
            .rev()
            .find(|row| row["generation"] == *generation && row["threadId"] == thread)
        {
            row["recordsCapabilityBinding"] = view;
        }
    }
    pub(super) fn persist_records_receipt(
        &self,
        generation: &Value,
        thread: &str,
        home: Option<&str>,
    ) {
        let receipt = {
            let inner = self.inner.0.lock().unwrap();
            if Self::context_scope(&inner, generation, thread, home).is_err() {
                return;
            }
            inner
                .records_receipts
                .iter()
                .find(|(g, t, _)| g == generation && t == thread)
                .map(|(_, _, receipt)| receipt.clone())
        };
        let Some(mut receipt) = receipt else {
            let current = {
                let inner = self.inner.0.lock().unwrap();
                Self::records_offer_is_current(&inner, generation, &serde_json::json!(thread))
            };
            self.records_binding_view(generation,thread,serde_json::json!({"state":if current{"bound in current generation"}else{"unknown/unsupported"},"persistence":"memory-only","limit":"original exact offered start or explicit project receipt unavailable; cold binding unknown, no older offering backfilled"}));
            return;
        };
        receipt.home_class = home.unwrap_or_default().into();
        let value = receipt.encode().and_then(|value| {
            Self::validate_receipt(&value, &receipt.home, thread, &receipt.project)?;
            Ok(value)
        });
        let persistence = match value {
            Ok(value) => self.tag_conversation(generation, thread, home, OWNER, &value),
            Err(limit) => serde_json::json!({"persistence":"memory-only","limit":limit}),
        };
        let mut inner = self.inner.0.lock().unwrap();
        if Self::context_scope(&inner, generation, thread, home).is_err() {
            return;
        }
        if let Some((_, _, held)) = inner
            .records_receipts
            .iter_mut()
            .find(|(g, t, _)| g == generation && t == thread)
        {
            *held = receipt;
        }
        let current =
            Self::records_offer_is_current(&inner, generation, &serde_json::json!(thread));
        drop(inner);
        self.records_binding_view(generation,thread,serde_json::json!({"state":if current{"bound in current generation"}else{"unknown/unsupported"},"persistence":persistence["persistence"],"limit":if current{persistence.get("limit").cloned().unwrap_or(Value::Null)}else{serde_json::json!("current capability project differs from the original offering")},"standing":"unverified App operational metadata; cold use requires a healthy durable receipt observation"}));
    }
    fn validate_receipt(
        value: &str,
        home: &str,
        thread: &str,
        project: &str,
    ) -> Result<Receipt, String> {
        let receipt = Receipt::decode(value)?;
        if receipt.home != home || receipt.thread != thread || receipt.project != project {
            return Err(
                "records receipt native home/thread or explicit App project differs".into(),
            );
        }
        Ok(receipt)
    }
    fn records_tag_basis(rows: &[Value], thread: &str) -> Vec<String> {
        let mut basis = rows
            .iter()
            .filter(|row| row["kind"] == "conversation_index" && row["threadId"] == thread)
            .flat_map(|row| {
                row["tags"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .filter(|tag| tag["owner"] == OWNER)
                    .map(|tag| serde_json::json!([row["home"], tag]).to_string())
            })
            .collect::<Vec<_>>();
        basis.sort();
        basis.dedup();
        basis
    }
    pub(super) fn restore_records_receipt(&self, generation: &Value, thread: &str) {
        let restored = (|| -> Result<(Receipt, Vec<String>), String> {
            let project = {
                let inner = self.inner.0.lock().unwrap();
                Self::context_scope(&inner, generation, thread, None)?;
                if inner.records_capability.is_none() {
                    return Err("records capability unavailable".into());
                }
                inner
                    .records_project_context
                    .as_ref()
                    .and_then(|context| context.reference())
                    .map(str::to_owned)
                    .ok_or("explicit capability App project unknown")?
            };
            let rows = {
                let _writer = self.recovery_writer.lock().unwrap();
                self.drain_recovery_owned();
                self.refresh_recovery_observation();
                let inner = self.inner.0.lock().unwrap();
                Self::context_scope(&inner, generation, thread, None)?;
                if inner.recovery_initialization_error.is_some() || inner.recovery_error.is_some() {
                    return Err("records receipt REC source unavailable or incomplete".into());
                }
                let observation = inner
                    .recovery_snapshot
                    .as_ref()
                    .ok_or("records receipt durable REC source unavailable")?;
                if observation.summary["historyLimits"]
                    .as_array()
                    .is_some_and(|limits| !limits.is_empty())
                {
                    return Err("records receipt durable REC history incomplete".into());
                }
                std::sync::Arc::clone(&observation.rows)
            };
            let mut receipt = None;
            for row in rows
                .iter()
                .filter(|row| row["kind"] == "conversation_index" && row["threadId"] == thread)
            {
                for tag in row["tags"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .filter(|tag| tag["owner"] == OWNER)
                {
                    let value = tag["value"]
                        .as_str()
                        .ok_or("records receipt tag malformed")?;
                    let candidate = Self::validate_receipt(
                        value,
                        generation["home"].as_str().unwrap_or_default(),
                        thread,
                        &project,
                    )?;
                    let capability = self
                        .records_capability()
                        .ok_or("records capability unavailable during lookup")?;
                    if candidate.directory != capability.project_identity()? {
                        return Err("records receipt physical capability project differs".into());
                    }
                    if row["home"] != candidate.home_class {
                        return Err("records receipt owning REC home class differs".into());
                    }
                    if receipt
                        .as_ref()
                        .is_some_and(|existing| existing != &candidate)
                    {
                        return Err("records receipt claims conflict; binding unknown".into());
                    }
                    receipt = Some(candidate);
                }
            }
            let receipt = receipt
                .ok_or("original durable records offering receipt absent; binding unknown")?;
            Ok((receipt, Self::records_tag_basis(&rows, thread)))
        })();
        #[cfg(test)]
        if let Some(hook) = self.before_records_receipt_bind.lock().unwrap().take() {
            hook();
        }
        // Reacquire the shared REC writer after staging/hook and compare only
        // this receiver's source basis. Read-only observation changes do not
        // invalidate it; a newly conflicting tag does. Hold through binding.
        let _writer = self.recovery_writer.lock().unwrap();
        self.drain_recovery_owned();
        self.refresh_recovery_observation();
        let mut inner = self.inner.0.lock().unwrap();
        if Self::context_scope(&inner, generation, thread, None).is_err() {
            return;
        }
        let restored = restored.and_then(|(receipt, basis)| {
            let observation = inner
                .recovery_snapshot
                .as_ref()
                .ok_or("records receipt REC source unavailable during binding")?;
            if inner.recovery_initialization_error.is_some()
                || inner.recovery_error.is_some()
                || observation.summary["historyLimits"]
                    .as_array()
                    .is_some_and(|limits| !limits.is_empty())
                || Self::records_tag_basis(&observation.rows, thread) != basis
            {
                return Err(
                    "records receipt REC source changed or became incomplete during lookup".into(),
                );
            }
            let capability = inner
                .records_capability
                .as_ref()
                .ok_or("records capability unavailable during binding")?;
            if receipt.directory != capability.project_identity()? {
                return Err(
                    "records receipt physical capability project changed during lookup".into(),
                );
            }
            if inner
                .records_project_context
                .as_ref()
                .and_then(|context| context.reference())
                != Some(receipt.project.as_str())
            {
                return Err("explicit capability App project changed during receipt lookup".into());
            }
            Ok(receipt)
        });
        let view = match restored {
            Ok(receipt) => {
                if !inner
                    .records_offers
                    .iter()
                    .any(|(g, t)| g == generation && t == thread)
                {
                    inner
                        .records_offers
                        .push((generation.clone(), serde_json::json!(thread)));
                }
                inner.records_offer_projects.push((
                    generation.clone(),
                    serde_json::json!(thread),
                    receipt.directory.clone(),
                ));
                inner
                    .records_receipts
                    .push((generation.clone(), thread.into(), receipt));
                serde_json::json!({"state":"bound in current generation","persistence":"durable App metadata","source":"one matching records receipt after genuine explicit resume","standing":"unverified operational metadata; no role, act or run authority restored"})
            }
            Err(limit) => {
                serde_json::json!({"state":"unknown/unsupported","limit":limit,"standing":"no original offering backfilled; other tools remain unsupported"})
            }
        };
        drop(inner);
        self.records_binding_view(generation, thread, view);
    }
}
