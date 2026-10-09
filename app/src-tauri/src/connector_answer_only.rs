//! C3-AO-COLD-01: recorded-content consistency only. No Host capability or writer admission.
use serde::{
    de::{self, MapAccess, SeqAccess, Visitor},
    Deserialize, Deserializer,
};
use serde_json::{json, Map, Value};
use std::{
    collections::{HashMap, HashSet},
    fmt,
    io::Read,
    sync::OnceLock,
};
pub const LIMIT: usize = 1048576;
struct Strict(Value);
impl<'de> Deserialize<'de> for Strict {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct V;
        impl<'de> Visitor<'de> for V {
            type Value = Strict;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
                f.write_str("JSON without duplicate keys")
            }
            fn visit_bool<E: de::Error>(self, v: bool) -> Result<Strict, E> {
                Ok(Strict(json!(v)))
            }
            fn visit_i64<E: de::Error>(self, v: i64) -> Result<Strict, E> {
                Ok(Strict(json!(v)))
            }
            fn visit_u64<E: de::Error>(self, v: u64) -> Result<Strict, E> {
                Ok(Strict(json!(v)))
            }
            fn visit_f64<E: de::Error>(self, v: f64) -> Result<Strict, E> {
                serde_json::Number::from_f64(v)
                    .map(|n| Strict(Value::Number(n)))
                    .ok_or_else(|| E::custom("nonfinite JSON"))
            }
            fn visit_str<E: de::Error>(self, v: &str) -> Result<Strict, E> {
                Ok(Strict(json!(v)))
            }
            fn visit_string<E: de::Error>(self, v: String) -> Result<Strict, E> {
                Ok(Strict(Value::String(v)))
            }
            fn visit_unit<E: de::Error>(self) -> Result<Strict, E> {
                Ok(Strict(Value::Null))
            }
            fn visit_seq<A: SeqAccess<'de>>(self, mut a: A) -> Result<Strict, A::Error> {
                let mut v = vec![];
                while let Some(x) = a.next_element::<Strict>()? {
                    v.push(x.0);
                }
                Ok(Strict(Value::Array(v)))
            }
            fn visit_map<A: MapAccess<'de>>(self, mut a: A) -> Result<Strict, A::Error> {
                let mut m = Map::new();
                while let Some(k) = a.next_key::<String>()? {
                    if m.contains_key(&k) {
                        return Err(de::Error::custom("duplicate JSON key"));
                    }
                    m.insert(k, a.next_value::<Strict>()?.0);
                }
                Ok(Strict(Value::Object(m)))
            }
        }
        d.deserialize_any(V)
    }
}
pub fn parse(bytes: &[u8]) -> Result<Value, String> {
    let mut d = serde_json::Deserializer::from_slice(bytes);
    let v = Strict::deserialize(&mut d).map_err(|e| e.to_string())?;
    d.end().map_err(|e| e.to_string())?;
    Ok(v.0)
}
pub fn bounded_read(reader: impl Read) -> Result<Vec<u8>, String> {
    let mut bytes = vec![];
    reader
        .take((LIMIT + 1) as u64)
        .read_to_end(&mut bytes)
        .map_err(|e| e.to_string())?;
    if bytes.len() > LIMIT {
        return Err(
            "known-version read exceeds1MiB; stopped at sentinel, no wider fallback".into(),
        );
    }
    Ok(bytes)
}
fn require(ok: bool, why: &str) -> Result<(), String> {
    if ok {
        Ok(())
    } else {
        Err(why.into())
    }
}
fn validators() -> Result<&'static Vec<jsonschema::Validator>, String> {
    static V: OnceLock<Result<Vec<jsonschema::Validator>, String>> = OnceLock::new();
    V.get_or_init(|| {
        let account: Value = serde_json::from_str(include_str!(
            "../resources/connector_route/connector.route-account.v0.5.schema.json"
        ))
        .map_err(|e| e.to_string())?;
        let message: Value = serde_json::from_str(include_str!(
            "../resources/connector_route/connector.contribution-message.v0.1.schema.json"
        ))
        .map_err(|e| e.to_string())?;
        [account, message["$defs"]["answer"].clone()]
            .iter()
            .map(|v| jsonschema::validator_for(v).map_err(|e| e.to_string()))
            .collect()
    })
    .as_ref()
    .map_err(Clone::clone)
}
pub fn shape(v: &Value) -> Result<(), String> {
    validators()?[0].validate(v).map_err(|e| e.to_string())
}
pub fn selected(v: &Value) -> bool {
    ["review", "plan", "integration", "integration_attempt"]
        .iter()
        .all(|k| v[*k].is_null())
}
fn strings(v: &Value) -> Result<HashSet<&str>, String> {
    let list = v.as_array().ok_or("Expected reference list")?;
    let s = list
        .iter()
        .map(|x| x.as_str().ok_or("Expected reference string".to_owned()))
        .collect::<Result<HashSet<_>, _>>()?;
    require(s.len() == list.len(), "Duplicate reference")?;
    Ok(s)
}
fn greater(a: &str, b: &str) -> bool {
    let a = a.trim_start_matches('0');
    let b = b.trim_start_matches('0');
    a.len() > b.len() || a.len() == b.len() && a > b
}
/// The base must have been independently resolved from original bytes by the caller.
pub fn validate(v: &Value, base: &Value) -> Result<Value, String> {
    shape(v)?;
    require(selected(v), "Recognized0.5 subset not adopted")?;
    require(
        !v["gaps"].as_array().unwrap().is_empty(),
        "Missing explicit outstanding integration gap",
    )?;
    require(
        v["base_account"]["account_id"] == base["account_id"]
            && v["question_id"] == base["question"]["id"],
        "Base identity/question mismatch",
    )?;
    let artifact = &v["answer"]["artifact"];
    let text = artifact["text"].as_str().unwrap();
    require(
        artifact["byte_length"].as_f64() == Some(text.len() as f64)
            && artifact["sha256"] == crate::util::sha256_hex(text.as_bytes()),
        "Exact answer bytes/hash/length mismatch",
    )?;
    let answer = parse(text.as_bytes())?;
    validators()?[1]
        .validate(&answer)
        .map_err(|e| e.to_string())?;
    require(
        answer["account_sha256"] == v["base_account"]["sha256"]
            && answer["question_id"] == v["question_id"],
        "Answer subject mismatch",
    )?;
    let gaps: HashSet<String> = (0..base["gaps"].as_array().ok_or("Base gaps missing")?.len())
        .map(|i| format!("/gaps/{i}"))
        .collect();
    let carried = strings(&answer["retained_gap_pointers"])?;
    require(
        carried
            .iter()
            .map(|s| s.to_string())
            .collect::<HashSet<_>>()
            == gaps,
        "Omitted or unknown base gap",
    )?;
    let contradictions: HashSet<&str> = base["contradictions"]
        .as_array()
        .unwrap()
        .iter()
        .map(|c| c["contradiction_id"].as_str().unwrap())
        .collect();
    require(
        strings(&answer["retained_contradiction_ids"])? == contradictions,
        "Omitted or unknown base contradiction",
    )?;
    let mut ids = HashSet::new();
    for claim in answer["claims"].as_array().unwrap() {
        require(
            ids.insert(claim["claim_id"].as_str().unwrap()),
            "Duplicate answer claim ID",
        )?;
        let mut count = 0;
        for (refs, items, key) in [
            ("base_claim_ids", "claims", "claim_id"),
            ("fact_ids", "facts", "fact_id"),
            ("comparison_ids", "comparisons", "comparison_id"),
        ] {
            let known: HashSet<_> = base[items]
                .as_array()
                .unwrap()
                .iter()
                .map(|x| x[key].as_str().unwrap())
                .collect();
            let found = strings(&claim[refs])?;
            count += found.len();
            require(found.is_subset(&known), "Unknown support reference")?;
        }
        require(count > 0, "Uncited answer claim")?;
    }
    let receipt = &v["answer"]["receipt"];
    require(
        receipt["kind"] == "answer_emission"
            && receipt["supplied_role"] == "TASK"
            && receipt["item_type"] == "agentMessage"
            && receipt["phase"] == "final_answer",
        "Wrong recorded answer kind/role/item/phase",
    )?;
    require(
        receipt["home_reference"] == receipt["generation"]["home"]
            && receipt["content_sha256"] == artifact["sha256"],
        "Recorded generation/content mismatch",
    )?;
    let pos = |key: &str| receipt[key].as_str().unwrap();
    require(
        greater(
            pos("response_receipt_position"),
            pos("dispatch_receipt_floor"),
        ) && greater(pos("item_receipt_position"), pos("dispatch_receipt_floor"))
            && !greater(
                pos("item_receipt_position"),
                pos("terminal_receipt_position"),
            ),
        "Recorded receipt ordering mismatch",
    )?;
    let mut kinds = HashSet::new();
    let mut identities = HashMap::new();
    let mut positions = HashMap::new();
    for source in receipt["sources"].as_array().unwrap() {
        let kind = source["kind"].as_str().unwrap();
        require(kinds.insert(kind), "Duplicate source kind")?;
        require(
            source["method"]
                == if kind == "role_supply" {
                    "sha256:role_guidance_utf8"
                } else {
                    "sha256:host_parsed_frame_json_utf8"
                },
            "Wrong recorded source method",
        )?;
        if kind == "request" {
            require(
                source["identity"] == receipt["request_reference"],
                "Recorded request reference mismatch",
            )?;
        }
        if kind == "role_supply" {
            require(
                source["identity"] == receipt["role_supply_reference"],
                "Recorded role reference mismatch",
            )?;
        }
        let id = source["identity"].as_str().unwrap();
        let content = (
            kind,
            source["method"].as_str().unwrap(),
            source["sha256"].as_str().unwrap(),
        );
        if let Some(old) = identities.insert(id, content) {
            require(old == content, "Conflicting source identity")?;
        }
        let field = match kind {
            "result" => Some("response_receipt_position"),
            "item_event" => Some("item_receipt_position"),
            "terminal_event" => Some("terminal_receipt_position"),
            _ => None,
        };
        if let Some(f) = field {
            let value = (id, source["sha256"].as_str().unwrap());
            if let Some(old) = positions.insert(pos(f), value) {
                require(old == value, "Conflicting recorded stream position")?;
            }
        }
    }
    require(
        kinds
            == HashSet::from([
                "request",
                "result",
                "item_event",
                "terminal_event",
                "role_supply",
            ]),
        "Incomplete source reference inventory",
    )?;
    Ok(answer)
}
