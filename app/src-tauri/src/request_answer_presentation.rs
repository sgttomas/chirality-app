//! The original-source context and frozen reading companion for a request answer.
//! No record, authority, or claim that the person read the companion is created here.
use crate::act_control::native_statement as ns;
use serde_json::{json, Value};
use std::sync::Mutex;

pub(crate) const COMMAND: &str = "item/commandExecution/requestApproval";
pub(crate) const FILE: &str = "item/fileChange/requestApproval";
pub(crate) const QUESTION: &str = "item/tool/requestUserInput";
pub(crate) const LEGACY_COMMAND: &str = "execCommandApproval";
pub(crate) const LEGACY_FILE: &str = "applyPatchApproval";

pub(crate) fn supported(method: &Value) -> bool {
    matches!(
        method.as_str(),
        Some(COMMAND | FILE | QUESTION | LEGACY_COMMAND | LEGACY_FILE)
    )
}

/// Lossless, fully typed JSON. Numeric spelling is text: the existing integer-only
/// digest contract stays unchanged, including for numbers nested in supplier data.
pub(crate) fn typed(value: &Value) -> Value {
    match value {
        Value::Null => json!({"type":"null"}),
        Value::Bool(v) => json!({"type":"boolean","value":v}),
        Value::Number(v) => json!({"type":"number","value":v.to_string()}),
        Value::String(v) => json!({"type":"string","value":v}),
        Value::Array(v) => json!({"type":"array","value":v.iter().map(typed).collect::<Vec<_>>()}),
        Value::Object(v) => {
            json!({"type":"object","value":v.iter().map(|(k,v)|json!([k,typed(v)])).collect::<Vec<_>>()})
        }
    }
}

/// Called only after answer_preview validated the original request and answer.
/// The observer supplies the native view and project observation from the same
/// owning HomeSession; no selected-page state or caller-provided prose is used.
pub(crate) fn context(snapshot: &Value, generation: &Value, id: &Value) -> Result<Value, String> {
    let request = snapshot["serverRequests"]
        .as_array()
        .into_iter()
        .flatten()
        .find(|r| r["generation"] == *generation && r["requestIdentity"] == *id)
        .ok_or("The original request is no longer available; review and confirm again")?;
    let p = &request["nativeParameters"];
    let thread = p
        .get("threadId")
        .or_else(|| p.get("conversationId"))
        .unwrap_or(&Value::Null);
    let row = snapshot["threads"]
        .as_array()
        .into_iter()
        .flatten()
        .rev()
        .find(|r| r["generation"] == *generation && r["threadId"] == *thread);
    let view = &snapshot["nativeView"];
    let matching_view = view["generation"] == *generation && view["home"] == generation["home"];
    let item = matching_view
        .then(|| {
            view["items"]
                .as_array()
                .into_iter()
                .flatten()
                .find(|i| {
                    !p["itemId"].is_null()
                        && i["threadId"] == *thread
                        && i["turnId"] == p["turnId"]
                        && i["native"]["id"] == p["itemId"]
                })
                .cloned()
        })
        .flatten();
    let child = matching_view
        .then(|| {
            view["descendants"]
                .as_array()
                .into_iter()
                .flatten()
                .find(|c| c["threadId"] == *thread)
        })
        .flatten();
    let asker = if thread.is_null() {
        json!({"kind":"no-conversation"})
    } else if !matching_view {
        json!({"kind":"not-established"})
    } else if let Some(c) = child {
        json!({"kind":"delegated","role":c["nativeThread"]["agentRole"],"nickname":c["nativeThread"]["agentNickname"]})
    } else {
        json!({"kind":"conversation"})
    };
    Ok(json!({
        "request":{"method":request["method"],"generation":generation,"requestIdentity":id,"nativeParameters":p},
        "item":item,
        "thread":row.map(|r|json!({"threadId":r["threadId"],"generation":r["generation"],"name":r["name"],"cwd":r["cwd"],"permissionProfile":r["activePermissionProfile"]["id"]})),
        "project":snapshot.get("answerProject").cloned().unwrap_or_else(||json!({"kind":"unknown"})),
        "asker":asker
    }))
}

/// Each block's label and notes are App-owned; value belongs to its stated
/// source. The page draws values through AgentText, never as App sentences.
pub(crate) fn detail(
    label: &'static str,
    source: &'static str,
    value: Value,
    notes: Vec<String>,
) -> Value {
    json!({"label":label,"source":source,"value":value,"notes":notes})
}

#[derive(Clone)]
struct Companion {
    generation: Value,
    request: Value,
    digest: String,
    content: Value,
    pending: bool,
}
static COMPANIONS: Mutex<Vec<Companion>> = Mutex::new(Vec::new());

/// Return whether the new envelope differs from the preceding frozen snapshot
/// for this exact typed request identity. This means available, never viewed.
pub(crate) fn changed(generation: &Value, request: &Value, content: &Value) -> bool {
    COMPANIONS
        .lock()
        .unwrap_or_else(|e| e.into_inner())
        .iter()
        .rev()
        .find(|c| c.generation == *generation && c.request == *request)
        .is_some_and(|c| c.content != *content)
}

pub(crate) fn publish(generation: &Value, request: &Value, digest: &str, content: &Value) {
    let mut rows = COMPANIONS.lock().unwrap_or_else(|e| e.into_inner());
    // The preceding snapshot remains available under its own digest after a
    // cancel/reopen. Reusing an unchanged envelope never manufactures a change.
    if let Some(index) = rows
        .iter()
        .position(|c| c.generation == *generation && c.request == *request && c.digest == digest)
    {
        // Reopening an older envelope makes it the latest presentation again.
        // Keeping first-insertion order would compare a later reopen with the
        // wrong snapshot after a change and then a change back.
        let mut c = rows.remove(index);
        c.pending = true;
        rows.push(c);
    } else {
        rows.push(Companion {
            generation: generation.clone(),
            request: request.clone(),
            digest: digest.into(),
            content: content.clone(),
            pending: true,
        });
    }
}
pub(crate) fn closed(generation: &Value, request: &Value) {
    for c in COMPANIONS
        .lock()
        .unwrap_or_else(|e| e.into_inner())
        .iter_mut()
        .filter(|c| c.generation == *generation && c.request == *request)
    {
        c.pending = false;
    }
}
pub(crate) fn companions(generation: &Value, request: &Value) -> Value {
    json!(COMPANIONS.lock().unwrap_or_else(|e|e.into_inner()).iter()
        .filter(|c|c.generation == *generation && c.request == *request)
        .map(|c|json!({"generation":c.generation,"requestIdentity":c.request,"digest":c.digest,"content":c.content,"pending":c.pending}))
        .collect::<Vec<_>>())
}

pub(crate) fn envelope(
    context: &Value,
    masked_answer: &Value,
    presentation: &Value,
) -> Result<(Value, String), String> {
    let content = typed(
        &json!({"schema":"request-answer/1","context":context,"answer":masked_answer,"presentation":presentation}),
    );
    let digest = ns::content_digest("Request answer", &content)?;
    Ok((content, digest))
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn typed_envelope_preserves_number_string_and_marker_object() {
        let values = [json!(0.5), json!("0.5"), json!({"number":"0.5"})];
        let encodings: Vec<_> = values.iter().map(typed).collect();
        for i in 0..3 {
            for j in 0..3 {
                if i != j {
                    assert_ne!(encodings[i], encodings[j]);
                }
            }
        }
        for v in &encodings {
            ns::content_digest("fixture", v).unwrap();
        }
    }
    #[test]
    fn frozen_snapshot_survives_cancel_without_a_read_claim() {
        let g = json!({"appSession":"companion-fixture","home":"invented","spawnCounter":1});
        let id = json!(17);
        let (a, d) = envelope(
            &json!({"value":0.5}),
            &json!({"answers":{}}),
            &json!({"details":[]}),
        )
        .unwrap();
        assert!(!changed(&g, &id, &a));
        publish(&g, &id, &d, &a);
        closed(&g, &id);
        let rows = companions(&g, &id);
        assert_eq!(rows[0]["content"], a);
        assert_eq!(
            ns::content_digest("fixture", &rows[0]["content"]).unwrap(),
            d
        );
        assert_eq!(rows[0]["pending"], false);
        assert!(rows[0].get("viewed").is_none());
        assert!(!changed(&g, &id, &a));
        let (b, db) = envelope(
            &json!({"value":"0.5"}),
            &json!({"answers":{}}),
            &json!({"details":[]}),
        )
        .unwrap();
        assert!(changed(&g, &id, &b));
        publish(&g, &id, &db, &b);
        closed(&g, &id);
        assert!(changed(&g, &id, &a));
        publish(&g, &id, &d, &a);
        closed(&g, &id);
        assert!(
            !changed(&g, &id, &a),
            "compare the most recently presented snapshot"
        );
        assert_eq!(companions(&g, &json!("17")), json!([]));
    }
}
