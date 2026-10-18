//! Pointer-only REC metadata produced from an actual positive native start.
//! A pointer is quoted provenance, never a receipt or permission to resume.
use serde_json::{json, Value};
use std::sync::{Arc, Mutex};

pub(crate) const OWNER: &str = "DEL-02-02/native-text-boundary";
pub(crate) type Held = Arc<Mutex<Vec<Pointer>>>;

pub(crate) fn decode(raw: &str) -> Result<Value, String> {
    let value: Value =
        serde_json::from_str(raw).map_err(|_| "historical native boundary: malformed pointer")?;
    let fields = [
        "version",
        "run",
        "conversation",
        "run_text_ref",
        "purpose",
        "generation",
        "turn",
        "client_user_message_id",
    ];
    if value
        .as_object()
        .is_none_or(|o| o.len() != fields.len() || fields.iter().any(|f| !o.contains_key(*f)))
        || value["version"] != 1
    {
        return Err("historical native boundary: unsupported version or fields".into());
    }
    for field in [
        "run",
        "conversation",
        "run_text_ref",
        "turn",
        "client_user_message_id",
    ] {
        if value[field].as_str().is_none_or(str::is_empty) {
            return Err(format!("historical native boundary: missing {field}"));
        }
    }
    if !value["run_text_ref"]
        .as_str()
        .unwrap()
        .starts_with("wr-record:v1:")
        || !matches!(
            value["purpose"].as_str(),
            Some("run start" | "run end notice")
        )
    {
        return Err("historical native boundary: unsupported original text".into());
    }
    crate::recovery::generation_ref(&value["generation"])?;
    Ok(value)
}

/// No constructor from JSON: only the actual Host-issued positive result can
/// produce a pointer retained for a later idempotent metadata-only retry.
pub(crate) struct Pointer {
    value: Value,
    class: String,
    status: Value,
}
impl Pointer {
    fn observed(
        native: &crate::hosting::PreparedNativeTurnStart<'_>,
        text: &crate::workflow_workspace::PreparedRunText,
        original: &str,
        client: &str,
        class: &str,
    ) -> Result<Self, String> {
        Self::observed_source(native.source(), native.turn_id(), text, original, client, class)
    }
    fn observed_source(
        source: &crate::hosting::SourceRequest,
        turn: &str,
        text: &crate::workflow_workspace::PreparedRunText,
        original: &str,
        client: &str,
        class: &str,
    ) -> Result<Self, String> {
        let frame = source.attempted_frame();
        if source.generation() != &text.scope().generation
            || client.is_empty()
            || !matches!(class, "H-acct" | "H-key")
            || frame["method"] != "turn/start"
            || frame["params"]["threadId"] != text.scope().conversation
            || frame["params"]["clientUserMessageId"] != client
            || frame["params"]["input"][0]["text"] != text.text()
        {
            return Err("native boundary does not match its original source".into());
        }
        let value = json!({"version":1,"run":text.scope().run,"conversation":text.scope().conversation,"run_text_ref":original,"purpose":text.record()["purpose"],"generation":text.scope().generation,"turn":turn,"client_user_message_id":client});
        decode(&value.to_string())?;
        Ok(Self {
            value,
            class: class.into(),
            status: Value::Null,
        })
    }
    fn persist(&mut self, host: &crate::hosting::Host) -> Value {
        // A retained typed observation may be saved after this same Host has
        // restarted its native child. Only metadata uses the current context;
        // the pointer keeps its original acknowledged generation verbatim.
        let current = host.snapshot()["generation"].clone();
        let generation = if current["home"] == self.value["generation"]["home"]
            && current["appSession"] == self.value["generation"]["appSession"]
        {
            &current
        } else {
            &self.value["generation"]
        };
        self.status = host.tag_conversation(
            generation,
            self.value["conversation"].as_str().unwrap(),
            Some(&self.class),
            OWNER,
            &self.value.to_string(),
        );
        self.status.clone()
    }
}

pub(crate) fn retain(
    held: &Held,
    host: &crate::hosting::Host,
    class: Option<&str>,
    native: &crate::hosting::PreparedNativeTurnStart<'_>,
    text: &crate::workflow_workspace::PreparedRunText,
    original: &str,
    client: &str,
) -> Value {
    let pointer = match class
        .ok_or("native source class unavailable")
        .and_then(|class| {
            Pointer::observed(native, text, original, client, class)
                .map_err(|_| "native boundary does not match its original source")
        }) {
        Ok(pointer) => pointer,
        Err(limit) => {
            return json!({"persistence":"memory-only","limit":limit,"standing":"no historical boundary retained; the native send outcome is unchanged"})
        }
    };
    save(held, host, pointer)
}

/// The attachment path admits only the Host's private positive full-packet
/// observation. A resolved submission DTO or cold metadata cannot supply it.
pub(crate) fn retain_attachment(
    held: &Held,
    host: &crate::hosting::Host,
    class: Option<&str>,
    native: &crate::hosting::AttachmentNativeTurnStart<'_>,
    text: &crate::workflow_workspace::PreparedRunText,
    original: &str,
    client: &str,
) -> Value {
    let pointer = match class.ok_or("native source class unavailable").and_then(|class| {
        if text.record()["purpose"] != "run end notice" {
            return Err("attachment boundary is not an original end notice");
        }
        Pointer::observed_source(native.source(), native.turn_id(), text, original, client, class)
            .map_err(|_| "native boundary does not match its original source")
    }) {
        Ok(pointer) => pointer,
        Err(limit) => return json!({"persistence":"memory-only","limit":limit,"standing":"no historical boundary retained; the native send outcome is unchanged"}),
    };
    save(held, host, pointer)
}

fn save(held: &Held, host: &crate::hosting::Host, mut pointer: Pointer) -> Value {
    let result = pointer.persist(host);
    let mut held = held.lock().unwrap();
    if !held.iter().any(|p| p.value == pointer.value) {
        held.push(pointer);
    }
    result
}

pub(crate) fn retry(held: &Held, host: &crate::hosting::Host) -> Value {
    json!(held
        .lock()
        .unwrap()
        .iter_mut()
        .map(|p| p.persist(host))
        .collect::<Vec<_>>())
}

pub(crate) fn view(held: &Held) -> Value {
    json!(held.lock().unwrap().iter().map(|p| json!({"originalText":p.value["run_text_ref"],"purpose":p.value["purpose"],"persistence":p.status["persistence"],"limit":p.status["limit"],"standing":"acknowledgment pointer only; native history is read separately"})).collect::<Vec<_>>())
}
