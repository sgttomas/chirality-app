//! App-observed role lifetime seam. Private immutable bindings are not deserialized.
//! Host supplies authentic correlated observations; native history owns transcript data.
//! Serialization/file validity alone establishes no App supply provenance or adoption.
use crate::role_supply::{content, Composition, Role, CONTENT_METHOD};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::sync::OnceLock;

#[derive(Clone, Debug, Serialize)]
struct SourcePart {
    path: String,
    bytes: String,
    source: Value,
    offset: usize,
    length: usize,
    identity: Value,
}
#[derive(Clone, Debug, Serialize)]
struct FrozenGuidance {
    role: Option<Role>,
    text: String,
    identity: Value,
    parts: Vec<SourcePart>,
}
impl FrozenGuidance {
    fn capture(composition: &Composition) -> Result<Self, String> {
        composition.verify()?;
        let raw = &composition.carried;
        if raw["compositionFormat"] != "chirality.role.compose/0.2"
            || raw["baseInstructions"] != "not-set"
        {
            return Err("role composition carrier not established".into());
        }
        let parts = raw["developerInstructions"]["parts"]
            .as_array()
            .ok_or("role source parts missing")?;
        let count = if composition.role.is_some() { 2 } else { 1 };
        if parts.len() != count {
            return Err("common/active role source parts incomplete".into());
        }
        let mut frozen = vec![];
        for (index, part) in parts.iter().enumerate() {
            let path = part["source"]["path"]
                .as_str()
                .ok_or("source path absent")?;
            let expected = if index == 0 {
                "AGENTS.md".into()
            } else {
                format!("agents/AGENT_{}.md", composition.role.unwrap().name())
            };
            let kind = if index == 0 {
                "product-guidance"
            } else {
                "role-guidance"
            };
            if path != expected
                || part["kind"] != kind
                || (index == 1 && part["role"] != json!(composition.role.unwrap()))
            {
                return Err("role selection/source part mismatch".into());
            }
            if part["source"]["store"] != "seeded-copy"
                || part["source"]["release"].as_str().is_none_or(str::is_empty)
                || !matches!(
                    part["source"]["state"].as_str(),
                    Some("default" | "modified")
                )
            {
                return Err("role source provenance incomplete".into());
            }
            let default = &part["source"]["defaultContent"];
            let default_value = default["value"]
                .as_str()
                .ok_or("default source identity absent")?;
            if default["method"] != CONTENT_METHOD
                || default_value.len() != 64
                || !default_value
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
            {
                return Err("default source identity not established".into());
            }
            let offset = usize::try_from(part["offset"].as_u64().ok_or("source offset absent")?)
                .map_err(|_| "offset out of range")?;
            let length = usize::try_from(part["length"].as_u64().ok_or("source length absent")?)
                .map_err(|_| "length out of range")?;
            let end = offset.checked_add(length).ok_or("source range overflow")?;
            let bytes = composition
                .text
                .as_bytes()
                .get(offset..end)
                .ok_or("source range outside composition")?;
            if length == 0
                || part["content"] != content(bytes)
                || part["content"]["method"] != CONTENT_METHOD
                || (index == 0 && offset != 0)
            {
                return Err("source byte identity/range not verified".into());
            }
            if part["source"]["state"] == "default" && default != &content(bytes) {
                return Err("default state does not match actual source bytes".into());
            }
            frozen.push(SourcePart {
                path: path.into(),
                bytes: std::str::from_utf8(bytes)
                    .map_err(|_| "source range not UTF8")?
                    .into(),
                source: part["source"].clone(),
                offset,
                length,
                identity: content(bytes),
            });
        }
        let mut expected = frozen[0].bytes.clone();
        if let Some(role) = composition.role {
            expected.push_str(&format!("\n\n# Active role: {}\n\n", role.name()));
            if frozen[1].offset != expected.len() {
                return Err("role separator/range mismatch".into());
            }
            expected.push_str(&frozen[1].bytes);
        }
        if expected != composition.text {
            return Err("composition does not equal exact source buffers and role framing".into());
        }
        Ok(Self {
            role: composition.role,
            text: expected.clone(),
            identity: content(expected.as_bytes()),
            parts: frozen,
        })
    }
}

#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
#[serde(tag = "standing", rename_all = "kebab-case")]
pub enum RoleInForce {
    AppObserved {
        role: Option<Role>,
        supply_ref: String,
    },
    Unknown {
        reason: String,
    },
}
// Same immutable embedded supplier root/target-ref/Draft7 approach as NativeHistory.
// No schema rewrite, external retrieval, hand-coded subset or unchecked fallback.
fn native_validate(target: &str, value: &Value) -> Result<(), String> {
    static VALIDATORS: OnceLock<Result<BTreeMap<String, jsonschema::Validator>, String>> =
        OnceLock::new();
    let validators = VALIDATORS
        .get_or_init(|| {
            let root: Value = serde_json::from_str(include_str!(
                "../resources/supplier/0.160.0/codex_app_server_protocol.schemas.json"
            ))
            .map_err(|e| e.to_string())?;
            [
                "ThreadStartParams",
                "ThreadStartResponse",
                "ThreadResumeParams",
                "ThreadResumeResponse",
                "ThreadForkParams",
                "ThreadForkResponse",
            ]
            .iter()
            .map(|name| {
                let mut schema = root.clone();
                schema["$ref"] = json!(format!("#/definitions/v2/{name}"));
                jsonschema::options()
                    .with_draft(jsonschema::Draft::Draft7)
                    .offline()
                    .build(&schema)
                    .map(|v| (name.to_string(), v))
                    .map_err(|e| e.to_string())
            })
            .collect()
        })
        .as_ref()
        .map_err(Clone::clone)?;
    validators
        .get(target)
        .ok_or("native lifecycle schema unavailable")?
        .validate(value)
        .map_err(|e| format!("native lifecycle {target} refused: {e}"))
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct ThreadMetadata {
    id: String,
    #[serde(default)]
    agent_role: Option<String>,
    #[serde(default)]
    forked_from_id: Option<String>,
}
#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
struct NativeSettings {
    model: String,
    model_provider: String,
    cwd: String,
    approval_policy: Value,
    approvals_reviewer: String,
    sandbox: Value,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct NativeResultMetadata {
    thread: ThreadMetadata,
    #[serde(default)]
    instruction_sources: Option<Vec<String>>,
    #[serde(flatten)]
    settings: NativeSettings,
}
#[derive(Clone, Debug, Serialize)]
struct NativeObservation {
    request_id: Value,
    request_ref: String,
    role_carrier_observation: Value,
    generation: Value,
    thread: String,
    instruction_sources: Option<Vec<String>>,
    agent_role: Option<String>,
    forked_from: Option<String>,
    reported_settings: NativeSettings,
}
#[derive(Clone, Debug, Serialize)]
#[serde(tag = "kind", rename_all = "kebab-case")]
enum Origin {
    Start,
    InheritedFork {
        source_thread: String,
        source_supply_ref: String,
    },
}
/// Caller-produced from an actual Host-correlated response, not a file parser.
/// Authentic transport provenance remains Host's responsibility, not this Rust type.
#[derive(Clone, Debug, Serialize)]
pub struct RoleBinding {
    home: String,
    thread: String,
    supply_ref: String,
    original: FrozenGuidance,
    origin: Origin,
    observation: NativeObservation,
    /// ROLE §3.3 CA-3: the "Continue as" relation {source thread, source start
    /// record}; a relation, not a copy. Absent for an ordinary start or a fork.
    #[serde(skip_serializing_if = "Option::is_none")]
    continued_from: Option<Value>,
}
impl RoleBinding {
    pub fn home(&self) -> &str {
        &self.home
    }
    pub fn thread(&self) -> &str {
        &self.thread
    }
    pub fn supply_ref(&self) -> &str {
        &self.supply_ref
    }
    pub fn role_in_force(&self, home: &str, thread: &str) -> RoleInForce {
        if self.home != home || self.thread != thread {
            return RoleInForce::Unknown {
                reason: "foreign home/thread binding".into(),
            };
        }
        RoleInForce::AppObserved {
            role: self.original.role,
            supply_ref: self.supply_ref.clone(),
        }
    }
    /// Original App guidance only. No supplier base or transcript enters this account.
    pub fn evidence(&self) -> Value {
        json!({"format":"chirality.role.binding/0.1","binding":self,"adoption":"unknown","provenance":"in-memory App-observed; serialized/imported copy is not trusted"})
    }
    /// Current store comparison changes the future-conversation notice only
    /// (ROLE §4.4 GC-1, GC-2). `kind` keeps an actual change (`changed`, or the
    /// file `missing`) apart from a comparison that could not be made
    /// (`not-read`); only the first two read "guidance changed since this
    /// conversation started". Equal bytes, including a restore to the original
    /// bytes, give no notice.
    pub fn changes(&self, current: &BTreeMap<String, Result<Vec<u8>, String>>) -> Vec<Value> {
        self.original.parts.iter().filter_map(|part|{
            let found=match current.get(&part.path){None=>Some(("missing","missing".to_owned())),Some(Err(e))=>Some(("not-read",format!("unreadable: {e}"))),Some(Ok(bytes)) if content(bytes)!=part.identity=>Some(("changed","guidance changed since this conversation started".to_owned())),_=>None};
            found.map(|(kind,reason)|json!({"path":part.path,"kind":kind,"reason":reason,"appliesTo":"future-conversations","currentConversationRoleChanged":false}))
        }).collect()
    }
    /// How this conversation's role came to be: its own start, a start that
    /// continues another conversation (CA-3), or a same-role fork (F-1).
    pub fn relation(&self) -> Value {
        match &self.origin {
            Origin::Start => match &self.continued_from {
                Some(from) => json!({"kind":"continued-from","from":from}),
                None => json!({"kind":"start"}),
            },
            Origin::InheritedFork { source_thread, source_supply_ref } => json!({"kind":"inherited-fork",
                "sourceThread":source_thread,"sourceSupplyRef":source_supply_ref,"forkedFromId":self.observation.forked_from}),
        }
    }
    pub fn resume(
        &self,
        home: &str,
        generation: Value,
        id: Value,
        request_ref: &str,
    ) -> Result<MetadataRequest, String> {
        MetadataRequest::new(self, home, generation, id, request_ref, false)
    }
    pub fn fork(
        &self,
        home: &str,
        generation: Value,
        id: Value,
        request_ref: &str,
        new_supply_ref: &str,
    ) -> Result<MetadataRequest, String> {
        let mut r = MetadataRequest::new(self, home, generation, id, request_ref, true)?;
        valid_supply_ref(new_supply_ref)?;
        if new_supply_ref == self.supply_ref {
            return Err("fork requires separate supply reference".into());
        }
        r.fork_supply_ref = Some(new_supply_ref.into());
        Ok(r)
    }
}

fn valid_scope(home: &str, generation: &Value) -> Result<(), String> {
    if home.is_empty()
        || generation.as_object().is_none_or(|o| o.len() != 3)
        || generation["home"] != home
        || generation["appSession"].as_str().is_none_or(str::is_empty)
        || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
    {
        return Err("selected home/full generation not established".into());
    }
    Ok(())
}
fn valid_supply_ref(reference: &str) -> Result<(), String> {
    if !reference.starts_with("sup:") || reference.len() <= 4 {
        return Err("supply identity absent".into());
    }
    Ok(())
}
fn valid_request(id: &Value, request_ref: &str) -> Result<(), String> {
    if !(id.as_u64().is_some_and(|v| v > 0) || id.as_str().is_some_and(|v| !v.is_empty()))
        || request_ref.is_empty()
    {
        return Err("native request identity absent".into());
    }
    Ok(())
}
fn observation(
    id: &Value,
    request_ref: &str,
    generation: &Value,
    observed_generation: &Value,
    frame: &Value,
    response_schema: &str,
) -> Result<NativeObservation, String> {
    if generation != observed_generation
        || frame["id"] != *id
        || frame.get("method").is_some()
        || frame.get("error").is_some()
    {
        return Err("native observation uncorrelated, foreign generation or failed".into());
    }
    native_validate(response_schema, &frame["result"])?;
    let meta: NativeResultMetadata = serde_json::from_value(frame["result"].clone())
        .map_err(|e| format!("native typed metadata refused: {e}"))?;
    if meta.thread.id.is_empty() {
        return Err("native thread not observed".into());
    }
    Ok(NativeObservation {
        request_id: id.clone(),
        request_ref: request_ref.into(),
        role_carrier_observation: Value::Null,
        generation: generation.clone(),
        thread: meta.thread.id,
        instruction_sources: meta.instruction_sources,
        agent_role: meta.thread.agent_role,
        forked_from: meta.thread.forked_from_id,
        reported_settings: meta.settings,
    })
}
/// Frozen before dispatch. Does not claim a native start or provider adoption.
#[derive(Clone, Debug)]
pub struct PreparedStart {
    home: String,
    generation: Value,
    id: Value,
    request_ref: String,
    supply_ref: String,
    guidance: FrozenGuidance,
    continued_from: Option<Value>,
}
impl PreparedStart {
    /// CA-3: this start continues another conversation. The relation names the
    /// source thread and its start record (or that none is established); the
    /// supplied guidance is still this start's own composition.
    pub fn continuing(mut self, relation: Value) -> Result<Self, String> {
        if relation["sourceThread"].as_str().is_none_or(str::is_empty) {
            return Err("continue-as source conversation absent".into());
        }
        self.continued_from = Some(relation);
        Ok(self)
    }
    pub fn new(
        home: &str,
        generation: Value,
        id: Value,
        request_ref: &str,
        supply_ref: &str,
        composition: &Composition,
    ) -> Result<Self, String> {
        valid_scope(home, &generation)?;
        valid_request(&id, request_ref)?;
        valid_supply_ref(supply_ref)?;
        Ok(Self {
            home: home.into(),
            generation,
            id,
            request_ref: request_ref.into(),
            supply_ref: supply_ref.into(),
            guidance: FrozenGuidance::capture(composition)?,
            continued_from: None,
        })
    }
    /// Additive role-owned fragment only; the owner supplies selected destination.
    pub fn guidance_params(&self) -> Value {
        json!({"developerInstructions":self.guidance.text})
    }
    pub fn observe(
        self,
        observed_generation: &Value,
        actual_sent: &Value,
        frame: &Value,
    ) -> Result<RoleBinding, String> {
        if actual_sent["id"] != self.id
            || actual_sent["method"] != "thread/start"
            || actual_sent["params"]["developerInstructions"] != self.guidance.text
        {
            return Err("actual native start request does not carry the frozen guidance".into());
        }
        native_validate("ThreadStartParams", &actual_sent["params"])?;
        let mut observation = observation(
            &self.id,
            &self.request_ref,
            &self.generation,
            observed_generation,
            frame,
            "ThreadStartResponse",
        )?;
        // Preserve only App-owned role bytes and selected destination metadata;
        // never cache supplier base/configuration/authentication/transcript data.
        let keys: Vec<_> = actual_sent["params"]
            .as_object()
            .ok_or("native start params must be object")?
            .keys()
            .filter(|k| k.as_str() != "developerInstructions")
            .cloned()
            .collect();
        observation.role_carrier_observation = json!({"method":"thread/start","developerInstructions":self.guidance.identity,
            "requestedModel":actual_sent["params"]["model"],"requestedProvider":actual_sent["params"]["modelProvider"],"cwd":actual_sent["params"]["cwd"],
            "nonRoleSettingKeys":keys,"baseInstructionsPresent":actual_sent["params"].get("baseInstructions").is_some(),"configPresent":actual_sent["params"].get("config").is_some(),
            "nativeBaseAndConfigurationPreservation":"not-established-by-role-binding","settingsOwner":"native caller/user; not overridden or vetoed by role lifecycle"});

        Ok(RoleBinding {
            home: self.home,
            thread: observation.thread.clone(),
            supply_ref: self.supply_ref,
            original: self.guidance,
            origin: Origin::Start,
            observation,
            continued_from: self.continued_from,
        })
    }
}
#[derive(Clone, Debug)]
pub struct MetadataRequest {
    source: RoleBinding,
    home: String,
    generation: Value,
    id: Value,
    request_ref: String,
    is_fork: bool,
    fork_supply_ref: Option<String>,
}
impl MetadataRequest {
    fn new(
        source: &RoleBinding,
        home: &str,
        generation: Value,
        id: Value,
        request_ref: &str,
        is_fork: bool,
    ) -> Result<Self, String> {
        valid_scope(home, &generation)?;
        valid_request(&id, request_ref)?;
        if home != source.home {
            return Err("foreign selected home".into());
        }
        Ok(Self {
            source: source.clone(),
            home: home.into(),
            generation,
            id,
            request_ref: request_ref.into(),
            is_fork,
            fork_supply_ref: None,
        })
    }
    pub fn method(&self) -> &str {
        if self.is_fork {
            "thread/fork"
        } else {
            "thread/resume"
        }
    }
    pub fn params(&self) -> Value {
        json!({"threadId":self.source.thread})
    }
    pub fn generation(&self) -> &Value {
        &self.generation
    }
    pub fn home(&self) -> &str {
        &self.home
    }
    pub fn request_id(&self) -> &Value {
        &self.id
    }
    pub fn request_ref(&self) -> &str {
        &self.request_ref
    }
    /// Resume/fork correlation never manufactures freshly supplied guidance.
    pub fn observe(
        self,
        observed_generation: &Value,
        actual_sent: &Value,
        frame: &Value,
    ) -> Result<RoleBinding, String> {
        if actual_sent["id"] != self.id
            || actual_sent["method"] != self.method()
            || actual_sent["params"] != self.params()
        {
            return Err("resume/fork actual request is not the bound metadata-only packet".into());
        }
        native_validate(
            if self.is_fork {
                "ThreadForkParams"
            } else {
                "ThreadResumeParams"
            },
            &actual_sent["params"],
        )?;
        let observation = observation(
            &self.id,
            &self.request_ref,
            &self.generation,
            observed_generation,
            frame,
            if self.is_fork {
                "ThreadForkResponse"
            } else {
                "ThreadResumeResponse"
            },
        )?;
        if !self.is_fork {
            if observation.thread != self.source.thread {
                return Err("resume returned another thread".into());
            }
            return Ok(self.source);
        }
        if observation.thread == self.source.thread
            || observation.forked_from.as_deref() != Some(self.source.thread.as_str())
        {
            return Err("fork/source relation not observed".into());
        }
        Ok(RoleBinding {
            home: self.home,
            thread: observation.thread.clone(),
            supply_ref: self.fork_supply_ref.ok_or("fork supply reference absent")?,
            original: self.source.original,
            origin: Origin::InheritedFork {
                source_thread: self.source.thread,
                source_supply_ref: self.source.supply_ref,
            },
            observation,
            continued_from: None,
        })
    }
}
/// In-memory owner only. No imported JSON/file path can insert a trusted binding.
#[derive(Default)]
pub struct RoleBindings {
    bindings: BTreeMap<(String, String), RoleBinding>,
}
// Issued only after successful original manager insertion; not a generic binding.
pub(crate) struct CceInserted { pin: crate::hosting::call_custody::StartPin }
impl CceInserted {pub(crate) fn into_pin(self)->crate::hosting::call_custody::StartPin{self.pin}}
impl RoleBindings {
    pub(crate) fn insert_cce_original(&mut self,binding:RoleBinding,pin:crate::hosting::call_custody::StartPin)->Result<crate::hosting::call_custody::ManagerOwner,String>{
        if !matches!(binding.origin,Origin::Start)||binding.original.parts.len()!=2||!pin.role_matches(&binding.home,&binding.thread,&binding.observation.generation,&binding.observation.request_id,&binding.observation.request_ref,&binding.supply_ref,binding.original.role,&binding.original.text,&binding.original.parts[0].bytes,&binding.original.parts[1].bytes){return Err("original manager insertion/source handoff mismatch".into())}
        self.insert(binding)?;
        Ok(crate::hosting::call_custody::ManagerOwner::from_inserted(CceInserted{pin}))
    }
    pub fn insert(&mut self, binding: RoleBinding) -> Result<(), String> {
        let key = (binding.home.clone(), binding.thread.clone());
        if self.bindings.contains_key(&key) {
            return Err("conversation role binding already exists; cannot reselect".into());
        }
        self.bindings.insert(key, binding);
        Ok(())
    }
    pub fn get(&self, home: &str, thread: &str) -> Option<&RoleBinding> {
        self.bindings.get(&(home.into(), thread.into()))
    }
    pub fn selected_role(&self, home: &str, thread: &str) -> RoleInForce {
        self.get(home, thread)
            .map(|b| b.role_in_force(home, thread))
            .unwrap_or(RoleInForce::Unknown {
                reason: "original App supply binding not established".into(),
            })
    }
    /// View-only import diagnosis. Even byte-perfect/schema-valid exported copies
    /// cannot establish the historical native boundary from writable storage.
    pub fn imported_role(_imported: &Value) -> RoleInForce {
        RoleInForce::Unknown {
            reason: "imported role binding provenance unverified".into(),
        }
    }
}
