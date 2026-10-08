//! ROLE additive composition: supplies common and active-role text only at thread/start.
//! Native policy/settings remain the person's configuration; adoption is always unknown.
use crate::util::sha256_hex;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::collections::BTreeSet;
pub const CONTENT_METHOD: &str = "chirality.app.exact-bytes.sha256/v1";
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[allow(non_camel_case_types)]
pub enum Role {
    HELP_HUMAN,
    HELPS_HUMANS,
    WORKING_ITEMS,
    TASK,
}
impl Role {
    pub const ALL: [Role; 4] = [
        Self::HELP_HUMAN,
        Self::HELPS_HUMANS,
        Self::WORKING_ITEMS,
        Self::TASK,
    ];
    pub fn name(self) -> &'static str {
        match self {
            Self::HELP_HUMAN => "HELP_HUMAN",
            Self::HELPS_HUMANS => "HELPS_HUMANS",
            Self::WORKING_ITEMS => "WORKING_ITEMS",
            Self::TASK => "TASK",
        }
    }
    pub fn primary_entry(self) -> bool {
        self != Self::TASK
    }
    pub fn child_roles(self) -> &'static [Role] {
        match self {
            Self::HELP_HUMAN => &[Self::HELPS_HUMANS, Self::WORKING_ITEMS, Self::TASK],
            Self::HELPS_HUMANS | Self::WORKING_ITEMS => &[Self::TASK],
            Self::TASK => &[],
        }
    }
}
/// Read-only App candidate data. Placement/default release choices remain U-R6/U-R11.
pub const BUNDLED_ROLE_SET: &[u8] = include_bytes!("../resources/instructions/roles.json");
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RoleDefinition {
    pub name: Role,
    pub meaning: String,
    pub guidance_file: String,
    pub delegation: String,
    pub child_roles: Vec<Role>,
    pub default_for_new_chat: bool,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RoleSet {
    pub format: String,
    pub roles: Vec<RoleDefinition>,
}
impl RoleSet {
    pub fn parse(bytes: &[u8]) -> Result<Self, String> {
        let set: Self =
            serde_json::from_slice(bytes).map_err(|e| format!("role-set-invalid: {e}"))?;
        if set.format != "chirality.app.roles/1"
            || set.roles.len() != Role::ALL.len()
            || set.roles.iter().filter(|r| r.default_for_new_chat).count() > 1
        {
            return Err("role-set-invalid: format, role count or defaults".into());
        }
        for (role, meaning) in Role::ALL.into_iter().zip([
            "Alignment with the human",
            "Design",
            "Managed execution",
            "Bounded execution; does not delegate",
        ]) {
            let matching: Vec<_> = set.roles.iter().filter(|r| r.name == role).collect();
            if matching.len() != 1 {
                return Err("role-set-invalid: exact four roles required".into());
            }
            let row = matching[0];
            if row.meaning != meaning
                || row.guidance_file != format!("agents/AGENT_{}.md", role.name())
                || row.delegation
                    != if role == Role::TASK {
                        "does-not-delegate"
                    } else {
                        "may-delegate"
                    }
                || row.child_roles != role.child_roles()
            {
                return Err(
                    "role-set-invalid: role meaning, guidance or delegation differs".into(),
                );
            }
        }
        Ok(set)
    }
    pub fn default_role(&self) -> Option<Role> {
        self.roles
            .iter()
            .find(|r| r.default_for_new_chat)
            .map(|r| r.name)
    }
}
pub fn bundled_role_set() -> Result<RoleSet, String> {
    RoleSet::parse(BUNDLED_ROLE_SET)
}
pub fn content(bytes: &[u8]) -> Value {
    json!({"method":CONTENT_METHOD,"value":sha256_hex(bytes)})
}
#[derive(Debug, Clone)]
pub struct Guidance {
    bytes: Vec<u8>,
    source: Value,
}
impl Guidance {
    pub fn seeded(
        path: &str,
        release: &str,
        bytes: Vec<u8>,
        default: &[u8],
    ) -> Result<Self, String> {
        if path != "AGENTS.md"
            && !Role::ALL
                .iter()
                .any(|r| path == format!("agents/AGENT_{}.md", r.name()))
        {
            return Err("guidance source path not allowed".into());
        }
        if release.is_empty() || bytes.is_empty() {
            return Err("guidance file missing or empty".into());
        }
        std::str::from_utf8(&bytes).map_err(|_| "guidance-not-utf8")?;
        let source = json!({"store":"seeded-copy","path":path,"release":release,"state":if bytes==default{"default"}else{"modified"},"defaultContent":content(default)});
        Ok(Self { bytes, source })
    }
    pub fn read_seeded(
        root: &std::path::Path,
        path: &str,
        release: &str,
        default: &[u8],
    ) -> Result<Self, String> {
        if path != "AGENTS.md"
            && !Role::ALL
                .iter()
                .any(|r| path == format!("agents/AGENT_{}.md", r.name()))
        {
            return Err("guidance source path not allowed".into());
        }
        let p = root.join(path);
        for ancestor in [root.to_path_buf(), root.join("agents"), p.clone()] {
            if ancestor == root.join("agents") && path == "AGENTS.md" {
                continue;
            }
            if std::fs::symlink_metadata(&ancestor)
                .map_err(|e| format!("guidance-file-unreadable: {e}"))?
                .file_type()
                .is_symlink()
            {
                return Err("guidance-file-unreadable: symbolic link".into());
            }
        }
        Self::seeded(
            path,
            release,
            std::fs::read(p).map_err(|e| format!("guidance-file-unreadable: {e}"))?,
            default,
        )
    }
    pub fn modified(&self) -> bool {
        self.source["state"] == "modified"
    }
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}
#[derive(Debug, Clone)]
pub struct Composition {
    role_set_identity: Value,
    pub text: String,
    pub carried: Value,
    pub role: Option<Role>,
}
impl Composition {
    pub fn new(
        common: &Guidance,
        role: Option<(Role, &Guidance)>,
        delegated: bool,
    ) -> Result<Self, String> {
        Self::with_role_set(common, role, delegated, BUNDLED_ROLE_SET)
    }
    pub(crate) fn with_role_set(
        common: &Guidance,
        role: Option<(Role, &Guidance)>,
        delegated: bool,
        role_set_bytes: &[u8],
    ) -> Result<Self, String> {
        RoleSet::parse(role_set_bytes)?;
        if common.source["path"] != "AGENTS.md" {
            return Err("common guidance source mismatch".into());
        }
        if role.is_some_and(|(r, _)| !delegated && !r.primary_entry()) {
            return Err("TASK is a bounded executor, not a primary entry".into());
        }
        let mut bytes = common.bytes.clone();
        let mut parts = vec![
            json!({"kind":"product-guidance","source":common.source,"content":content(&common.bytes),"offset":0,"length":common.bytes.len()}),
        ];
        if let Some((r, g)) = role {
            if g.source["path"] != format!("agents/AGENT_{}.md", r.name()) {
                return Err("active role source mismatch".into());
            }
            bytes.extend_from_slice(format!("\n\n# Active role: {}\n\n", r.name()).as_bytes());
            let offset = bytes.len();
            bytes.extend_from_slice(&g.bytes);
            parts.push(json!({"kind":"role-guidance","role":r,"source":g.source,"content":content(&g.bytes),"offset":offset,"length":g.bytes.len()}));
        }
        let carried = json!({"compositionFormat":"chirality.role.compose/0.2","developerInstructions":{"content":content(&bytes),"byteLength":bytes.len(),"parts":parts},"baseInstructions":"not-set","nativeChildRoles":[]});
        Ok(Self {
            role_set_identity: content(role_set_bytes),
            text: String::from_utf8(bytes).map_err(|e| e.to_string())?,
            carried,
            role: role.map(|(r, _)| r),
        })
    }
    pub fn role_set_identity(&self) -> &Value {
        &self.role_set_identity
    }
    pub fn verify(&self) -> Result<(), String> {
        let b = self.text.as_bytes();
        let d = &self.carried["developerInstructions"];
        if d["content"] != content(b) || d["byteLength"] != b.len() {
            return Err("whole composed identity differs".into());
        }
        for p in d["parts"].as_array().ok_or("parts absent")? {
            let offset = p["offset"].as_u64().ok_or("offset absent")? as usize;
            let len = p["length"].as_u64().ok_or("length absent")? as usize;
            let end = offset.checked_add(len).ok_or("byte range overflow")?;
            let piece = b.get(offset..end).ok_or("byte range outside composition")?;
            if p["content"] != content(piece) {
                return Err("part identity differs".into());
            }
        }
        Ok(())
    }
    pub fn start_params(&self) -> Result<Value, String> {
        self.verify()?;
        let params = json!({"developerInstructions":self.text});
        check_role_inputs("thread/start", &params)?;
        Ok(params)
    }
    /// Unresolved child carrier never implies supplied. Existing user-defined names remain untouched.
    pub fn child_status(
        &self,
        user_names: Option<&BTreeSet<String>>,
        carrier_verified: bool,
    ) -> Vec<Value> {
        Role::ALL
            .into_iter()
            .map(|r| {
                let offered = self
                    .role
                    .is_some_and(|parent| parent.child_roles().contains(&r));
                let reason = if !offered {
                    "not-offered-by-role"
                } else if !carrier_verified {
                    "mechanism-not-supported-at-pin"
                } else if user_names.is_none() {
                    "user-configuration-not-read"
                } else if user_names.unwrap().contains(r.name()) {
                    "user-configuration-defines-role"
                } else {
                    "mechanism-not-supported-at-pin"
                };
                json!({"role":r,"status":"not-supplied","reason":reason})
            })
            .collect()
    }
    pub fn start_record(
        &self,
        supply_id: &str,
        thread: &str,
        request_ref: &str,
        generation: u64,
        response: Option<&Value>,
    ) -> Result<Value, String> {
        self.verify()?;
        if !supply_id.starts_with("sup:")
            || thread.is_empty()
            || request_ref.is_empty()
            || generation == 0
        {
            return Err("supply request identity incomplete".into());
        }
        let mut rec = json!({"format":"chirality.role.supply","formatVersion":"0.2","supplyId":supply_id,"thread":thread,"trigger":"thread-start","request":{"method":"thread/start","requestRef":request_ref,"generation":generation},"selection":{"role":self.role.map(|r|r.name()).unwrap_or("none"),"preselected":false,"roleSet":self.role_set_identity},"carried":self.carried,"adoption":"unknown"});
        match response {
            None => {
                rec["outcome"] = json!("unknown-no-response");
                rec["supplierReported"] = json!({"instructionSources":"not-reported"});
            }
            Some(v) if v.get("error").is_some() => {
                rec["outcome"] = json!("request-failed");
                rec["supplierReported"] = json!({"instructionSources":"not-reported"});
            }
            Some(v) => {
                let result = &v["result"];
                let id = result["thread"]["id"]
                    .as_str()
                    .ok_or("supplier thread identity not reported")?;
                rec["thread"] = json!(id);
                rec["outcome"] = json!("supplied");
                rec["supplierReported"] = json!({"instructionSources":result.get("instructionSources").cloned().unwrap_or(json!("not-reported")),"agentRole":result["thread"]["agentRole"]});
            }
        }
        Ok(rec)
    }
}
/// Checks only the App's role-owned input fragment, not the person's harness configuration.
pub fn check_role_inputs(method: &str, params: &Value) -> Result<(), String> {
    let m = params
        .as_object()
        .ok_or("role input fragment must be object")?;
    for k in [
        "baseInstructions",
        "personality",
        "approvalPolicy",
        "approvalsReviewer",
        "sandbox",
        "multiAgentMode",
    ] {
        if m.contains_key(k) {
            return Err(format!("forbidden-input-in-request: {k}"));
        }
    }
    if method != "thread/start"
        && (m.contains_key("developerInstructions") || m.contains_key("config"))
    {
        return Err(format!(
            "forbidden-input-in-request: instructions on {method}"
        ));
    }
    if let Some(config) = m.get("config") {
        for key in config.as_object().ok_or("config must be object")?.keys() {
            let p: Vec<_> = key.split('.').collect();
            if p.len() != 3
                || p[0] != "agents"
                || !Role::ALL.iter().any(|r| r.name() == p[1])
                || !["description", "config_file"].contains(&p[2])
            {
                return Err(format!("forbidden-input-in-request: config key {key}"));
            }
        }
    }
    Ok(())
}
pub fn limit(role: Role, guidance: &Guidance) -> Value {
    json!({"role":role,"delegation":if role==Role::TASK{"does-not-delegate"}else{"may-delegate"},"standing":if guidance.modified(){"unknown"}else{"stated-not-enforced"},"presentedAs":if guidance.modified(){"Not known whether the supplied guidance states this"}else{"Stated, not enforced"},"notEnforcement":["approval-policy","sandbox","brief-text","worktree","user-configuration","depth-limit"]})
}
