//! WD carriage and element reading. Retains failures instead of rejecting prose-only packages.
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

pub const SCHEMA: &str =
    include_str!("../resources/workflow_role/workflow-declaration.schema.json");
pub const CATEGORIES: [(&str, &str); 5] = [
    ("expected_inputs", "expected_input"),
    ("required_tools", "required_tool"),
    ("checkpoints", "checkpoint"),
    ("returned_outputs", "returned_output"),
    ("returned_evidence", "returned_evidence"),
];

/// Duplicate keys refuse parsing at every depth; serde_json::Value alone overwrites them.
struct UniqueJson(Value);
impl<'de> Deserialize<'de> for UniqueJson {
    fn deserialize<D: serde::Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        struct Visitor;
        impl<'de> serde::de::Visitor<'de> for Visitor {
            type Value = UniqueJson;
            fn expecting(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
                f.write_str("JSON without duplicate keys")
            }
            fn visit_bool<E: serde::de::Error>(self, v: bool) -> Result<Self::Value, E> {
                Ok(UniqueJson(v.into()))
            }
            fn visit_i64<E: serde::de::Error>(self, v: i64) -> Result<Self::Value, E> {
                Ok(UniqueJson(v.into()))
            }
            fn visit_u64<E: serde::de::Error>(self, v: u64) -> Result<Self::Value, E> {
                Ok(UniqueJson(v.into()))
            }
            fn visit_f64<E: serde::de::Error>(self, v: f64) -> Result<Self::Value, E> {
                serde_json::Number::from_f64(v)
                    .map(|n| UniqueJson(Value::Number(n)))
                    .ok_or_else(|| E::custom("non-finite number"))
            }
            fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> {
                Ok(UniqueJson(v.into()))
            }
            fn visit_string<E: serde::de::Error>(self, v: String) -> Result<Self::Value, E> {
                Ok(UniqueJson(v.into()))
            }
            fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
                Ok(UniqueJson(Value::Null))
            }
            fn visit_none<E: serde::de::Error>(self) -> Result<Self::Value, E> {
                Ok(UniqueJson(Value::Null))
            }
            fn visit_seq<A: serde::de::SeqAccess<'de>>(
                self,
                mut a: A,
            ) -> Result<Self::Value, A::Error> {
                let mut v = vec![];
                while let Some(x) = a.next_element::<UniqueJson>()? {
                    v.push(x.0)
                }
                Ok(UniqueJson(Value::Array(v)))
            }
            fn visit_map<A: serde::de::MapAccess<'de>>(
                self,
                mut a: A,
            ) -> Result<Self::Value, A::Error> {
                let mut m = serde_json::Map::new();
                while let Some(k) = a.next_key::<String>()? {
                    if m.contains_key(&k) {
                        return Err(serde::de::Error::custom(format!("duplicate JSON key {k}")));
                    }
                    m.insert(k, a.next_value::<UniqueJson>()?.0);
                }
                Ok(UniqueJson(Value::Object(m)))
            }
        }
        d.deserialize_any(Visitor)
    }
}
pub fn parse_unique(text: &str) -> Result<Value, String> {
    serde_json::from_str::<UniqueJson>(text)
        .map(|v| v.0)
        .map_err(|e| e.to_string())
}

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Reading {
    Undeclared,
    DeclaredEmpty,
    Recognized,
    Invalid,
    NotEstablished,
}
#[derive(Debug, Clone, Serialize)]
pub struct Element {
    pub value: Value,
    pub reading: Reading,
    pub findings: Vec<String>,
}
#[derive(Debug, Clone, Serialize)]
pub struct Declaration {
    pub raw: Option<Value>,
    pub reading: Reading,
    pub categories: BTreeMap<String, Reading>,
    pub elements: BTreeMap<String, Vec<Element>>,
    pub findings: Vec<String>,
}

/// Complete CommonMark root block location. Ranges name original UTF-8 bytes,
/// including original CRLF; parsed code text is a reading view only.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocatedDeclaration {
    pub json_text: String,
    pub block_bytes: std::ops::Range<usize>,
    pub text_bytes: Vec<std::ops::Range<usize>>,
}
/// WD CR3's first closed front-matter span, without rewriting source bytes.
fn body_start(text: &str) -> usize {
    let bytes = text.as_bytes();
    let mut start = 0;
    let mut lines = vec![];
    while start < bytes.len() {
        let mut end = start;
        while end < bytes.len() && !matches!(bytes[end], b'\n' | b'\r') {
            end += 1;
        }
        let mut next = end;
        if next < bytes.len() {
            next += 1;
            if bytes[end] == b'\r' && bytes.get(next) == Some(&b'\n') {
                next += 1;
            }
        }
        lines.push((start, end, next));
        start = next;
    }
    if lines
        .first()
        .is_some_and(|(a, b, _)| &text[*a..*b] == "---")
    {
        if let Some((_, _, next)) = lines
            .iter()
            .skip(1)
            .find(|(a, b, _)| &text[*a..*b] == "---")
        {
            return *next;
        }
    }
    0
}
/// CR1 selects the reserved literal opening-line token. CommonMark may decode
/// an info-string alias, but those decoded aliases do not declare this package.
fn literal_declaration_opener(text: &str, start: usize) -> bool {
    let Some(remainder) = text.get(start..) else {
        return false;
    };
    let line = remainder.split(['\r', '\n']).next().unwrap_or("");
    let spaces = line.bytes().take_while(|b| *b == b' ').count();
    if spaces > 3 {
        return false;
    }
    let opening = &line[spaces..];
    let Some(marker) = opening.as_bytes().first().copied() else {
        return false;
    };
    if !matches!(marker, b'`' | b'~') {
        return false;
    }
    let count = opening.bytes().take_while(|b| *b == marker).count();
    count >= 3 && opening[count..].trim() == "workflow-declaration"
}
pub fn locate(text: &str) -> Result<Option<LocatedDeclaration>, String> {
    use pulldown_cmark::{CodeBlockKind, Event, Options, Parser, Tag, TagEnd};
    let offset = body_start(text);
    let mut depth = 0usize;
    let mut active: Option<LocatedDeclaration> = None;
    let mut found = vec![];
    for (event, range) in Parser::new_ext(&text[offset..], Options::empty()).into_offset_iter() {
        match event {
            Event::Start(tag) => {
                if depth == 0 {
                    if let Tag::CodeBlock(CodeBlockKind::Fenced(info)) = &tag {
                        if info.trim() == "workflow-declaration"
                            && literal_declaration_opener(text, range.start + offset)
                        {
                            active = Some(LocatedDeclaration {
                                json_text: String::new(),
                                block_bytes: (range.start + offset)..(range.end + offset),
                                text_bytes: vec![],
                            });
                        }
                    }
                }
                depth += 1;
            }
            Event::Text(value) => {
                if let Some(block) = &mut active {
                    block.json_text.push_str(&value);
                    block
                        .text_bytes
                        .push((range.start + offset)..(range.end + offset));
                }
            }
            Event::End(tag) => {
                depth = depth
                    .checked_sub(1)
                    .ok_or("CommonMark event stack invalid")?;
                if tag == TagEnd::CodeBlock && depth == 0 {
                    if let Some(mut block) = active.take() {
                        block.block_bytes.end = range.end + offset;
                        found.push(block);
                    }
                }
            }
            _ => {}
        }
    }
    match found.len() {
        0 => Ok(None),
        1 => Ok(found.pop()),
        _ => Err("FB-02: more than one workflow-declaration block".into()),
    }
}
/// Legacy reading API delegates all Markdown structure to the pinned parser.
pub fn extract(text: &str) -> Result<Option<String>, String> {
    Ok(locate(text)?.map(|b| {
        b.json_text
            .strip_suffix('\n')
            .unwrap_or(&b.json_text)
            .to_owned()
    }))
}

fn validator(def: Option<&str>) -> Result<jsonschema::Validator, String> {
    let schema: Value = serde_json::from_str(SCHEMA).map_err(|e| e.to_string())?;
    let mut target = schema.clone();
    if let Some(name) = def {
        target = serde_json::json!({"$defs":schema["$defs"],"$ref":format!("#/$defs/{name}")});
    }
    jsonschema::options()
        .with_draft(jsonschema::Draft::Draft202012)
        .offline()
        .build(&target)
        .map_err(|e| format!("WD schema setup: {e}"))
}

pub fn read(text: &str) -> Result<Declaration, String> {
    let mut r = Declaration {
        raw: None,
        reading: Reading::Undeclared,
        categories: BTreeMap::new(),
        elements: BTreeMap::new(),
        findings: vec![],
    };
    let block = match extract(text) {
        Ok(x) => x,
        Err(e) => {
            r.reading = Reading::NotEstablished;
            r.findings.push(e);
            return Ok(r);
        }
    };
    let Some(block) = block else {
        for (c, _) in CATEGORIES {
            r.categories.insert(c.into(), Reading::Undeclared);
        }
        return Ok(r);
    };
    let doc = match parse_unique(&block) {
        Ok(v) => v,
        Err(e) => {
            r.reading = Reading::NotEstablished;
            r.findings.push(format!("FB-02: {e}"));
            return Ok(r);
        }
    };
    r.raw = Some(doc.clone());
    if doc["declaration_contract_version"] != "WD-v0.8" {
        r.reading = Reading::NotEstablished;
        r.findings
            .push("contract version not established; preserved".into());
        return Ok(r);
    }
    r.reading = Reading::Recognized;
    let root: Value = serde_json::from_str(SCHEMA).map_err(|e| e.to_string())?;
    for k in doc.as_object().ok_or("WD envelope must be object")?.keys() {
        if root["properties"].get(k).is_none() {
            r.findings
                .push(format!("unrecognized top-level element {k}; preserved"));
        }
    }
    for (cat, def) in CATEGORIES {
        let state = match doc.get(cat) {
            None => Reading::Undeclared,
            Some(Value::Array(a)) if a.is_empty() => Reading::DeclaredEmpty,
            Some(Value::Array(_)) => Reading::Recognized,
            _ => Reading::NotEstablished,
        };
        r.categories.insert(cat.into(), state);
        let Some(a) = doc[cat].as_array() else {
            continue;
        };
        let v = validator(Some(def))?;
        let mut elements = vec![];
        for el in a {
            let errors: Vec<_> = v.iter_errors(el).map(|e| e.to_string()).collect();
            let mut e = Element {
                value: el.clone(),
                reading: if errors.is_empty() {
                    Reading::Recognized
                } else {
                    Reading::NotEstablished
                },
                findings: errors,
            };
            if cat == "checkpoints" {
                if let Some(act) = el["required_act"].as_str() {
                    if let Some(n) = act.strip_prefix('A').and_then(|s| s.parse::<u32>().ok()) {
                        if (1..=16).contains(&n) && ![4, 5, 6, 7, 12].contains(&n) {
                            e.reading = Reading::Invalid;
                            e.findings
                                .push("FB-03: recognized act not permitted as checkpoint".into());
                        }
                    }
                }
            }
            elements.push(e);
        }
        let mut names = BTreeMap::<String, usize>::new();
        for e in &elements {
            if let Some(n) = e.value["name"].as_str() {
                *names.entry(n.into()).or_default() += 1;
            }
        }
        for e in &mut elements {
            if e.value["name"].as_str().is_some_and(|n| names[n] > 1) {
                e.reading = if cat == "checkpoints" {
                    Reading::Invalid
                } else {
                    Reading::NotEstablished
                };
                e.findings.push("FB-20: duplicate category name".into());
            }
        }
        r.elements.insert(cat.into(), elements);
    }
    domain_checks(&mut r);
    // Validate role/restriction independently; malformed metadata is never a hidden default.
    for field in ["compatible_roles", "tool_restriction"] {
        if let Some(value) = doc.get(field) {
            let mut s = root["properties"][field].clone();
            s.as_object_mut()
                .ok_or("WD property schema")?
                .insert("$defs".into(), root["$defs"].clone());
            let v = jsonschema::options()
                .offline()
                .build(&s)
                .map_err(|e| e.to_string())?;
            if let Err(e) = v.validate(value) {
                r.findings.push(format!("{field} not established: {e}"));
            }
        }
    }
    Ok(r)
}

fn domain_checks(r: &mut Declaration) {
    let usable: BTreeMap<String, BTreeSet<String>> = r
        .elements
        .iter()
        .map(|(c, a)| {
            (
                c.clone(),
                a.iter()
                    .filter(|e| e.reading == Reading::Recognized)
                    .filter_map(|e| e.value["name"].as_str().map(String::from))
                    .collect(),
            )
        })
        .collect();
    let host_tools: BTreeSet<String> = r
        .elements
        .get("required_tools")
        .into_iter()
        .flatten()
        .filter(|e| e.reading == Reading::Recognized && e.value["class"] == "host_operation")
        .filter_map(|e| e.value["name"].as_str().map(String::from))
        .collect();
    let exists = |cat: &str, v: &Value| {
        v.as_str()
            .is_some_and(|n| usable.get(cat).is_some_and(|s| s.contains(n)))
    };
    let outputs: BTreeMap<String, Value> = r
        .elements
        .get("returned_outputs")
        .into_iter()
        .flatten()
        .filter_map(|e| {
            e.value["name"]
                .as_str()
                .map(|n| (n.into(), e.value.clone()))
        })
        .collect();
    for (cat, a) in &mut r.elements {
        for e in a {
            if e.reading != Reading::Recognized {
                continue;
            }
            let v = &e.value;
            let mut failures = vec![];
            if cat == "expected_inputs"
                && v["kind"] == "host_read"
                && !v["read_through"]
                    .as_str()
                    .is_some_and(|s| host_tools.contains(s))
            {
                failures.push("FB-21: read_through must name usable host operation");
            }
            if cat == "returned_outputs" {
                for label in v["promised_standing"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .filter_map(Value::as_str)
                {
                    let l = label.to_lowercase();
                    if l.trim() == "checked"
                        || l.split(|c: char| !c.is_alphanumeric() && c != '-')
                            .any(|w| {
                                ["approved", "certified", "sealed", "code-compliant"].contains(&w)
                            })
                    {
                        failures.push("FB-10: promised human standing cannot follow execution");
                    }
                }
                if v.get("gating_checkpoint").is_some()
                    && !exists("checkpoints", &v["gating_checkpoint"])
                {
                    failures.push("FB-21: gating checkpoint not usable");
                }
                for t in v["relies_on"]
                    .as_array()
                    .into_iter()
                    .flatten()
                    .chain(v["produced_by"]["tools"].as_array().into_iter().flatten())
                {
                    if !exists("required_tools", t) {
                        failures.push("FB-21: output tool not usable");
                    }
                }
            }
            if cat == "returned_evidence" {
                for t in v["supports"].as_array().into_iter().flatten() {
                    if exists("returned_outputs", t) == exists("checkpoints", t) {
                        failures.push("FB-21: support absent or ambiguous");
                    }
                }
            }
            if cat == "checkpoints" {
                let rw = &v["reached_when"];
                let sb = &v["subject"];
                if rw["kind"] == "before_dispatch" && !exists("required_tools", &rw["tool"]) {
                    failures.push("FB-13: dispatch tool not usable");
                }
                if rw["kind"] == "output_produced" && !exists("returned_outputs", &rw["output"]) {
                    failures.push("FB-13: produced output not usable");
                }
                if ["named_output", "objects_named_output_concerns"]
                    .iter()
                    .any(|c| sb["class"] == *c)
                    && !exists("returned_outputs", &sb["output"])
                {
                    failures.push("FB-13: subject output not usable");
                }
                for obj in [rw, sb] {
                    for t in obj["tools"].as_array().into_iter().flatten() {
                        if !t.as_str().is_some_and(|s| host_tools.contains(s)) {
                            failures.push("FB-13: outcome needs usable host operations");
                        }
                    }
                }
                if rw["kind"] == "output_produced" {
                    if let Some(o) = rw["output"].as_str().and_then(|n| outputs.get(n)) {
                        if o["form"] == "workflow_input"
                            || o["form"] == "human_act_standing"
                            || (o["form"] == "host_change" && o.get("produced_by").is_none())
                        {
                            failures.push("FB-13: output production unobservable");
                        }
                    }
                }
                if sb["class"] == "objects_named_output_concerns" {
                    if let Some(o) = sb["output"].as_str().and_then(|n| outputs.get(n)) {
                        if o["relies_on"].as_array().is_none_or(|a| a.is_empty()) {
                            failures.push("FB-13: output concerns no named read");
                        }
                    }
                }
                if v["required_act"] == "A5"
                    && !(rw["kind"] == "host_outcome"
                        && rw["outcome"] == "queued"
                        && sb["class"] == "change_items_of_named_proposal")
                {
                    failures.push("FB-16: A5 combination invalid");
                }
                if sb["class"] == "targets_of_held_call" && rw["kind"] != "before_dispatch" {
                    failures.push("FB-16: held-call target needs before_dispatch");
                }
                if (v["required_act"] == "A12")
                    != (sb["class"] == "grant_setting" && sb.get("setting").is_some())
                {
                    failures.push("FB-17: grant act and setting must correspond");
                }
            }
            if !failures.is_empty() {
                e.reading =
                    if cat == "checkpoints" || failures.iter().any(|f| f.starts_with("FB-10")) {
                        Reading::Invalid
                    } else {
                        Reading::NotEstablished
                    };
                e.findings.extend(failures.into_iter().map(String::from));
            }
        }
    }
}
