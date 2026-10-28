//! CRR-v0.1: checked record bytes and attributed claims, never verified truth or acts.
use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::{HashMap, HashSet};
fn text<'a>(v: &'a Value, k: &str) -> Result<&'a str, String> {
    v[k].as_str().ok_or_else(|| format!("Missing text {k}"))
}
fn list<'a>(v: &'a Value, k: &str) -> Result<&'a Vec<Value>, String> {
    v[k].as_array().ok_or_else(|| format!("Missing array {k}"))
}
fn require(ok: bool, why: &str) -> Result<(), String> {
    if ok {
        Ok(())
    } else {
        Err(why.into())
    }
}
fn supported(v: &Value) -> Value {
    let mut out: Vec<Value> = v["facts"]
        .as_array()
        .unwrap()
        .iter()
        .map(|f| json!({"statement":f["statement"],"basis":"source_route","refs":[f["fact_id"]]}))
        .collect();
    out.extend(v["comparisons"].as_array().unwrap().iter().map(|c|json!({"statement":format!("Selected excerpts {} and {}: {}; no whole-record or substantive-change conclusion.",c["since_fact_id"].as_str().unwrap(),c["at_fact_id"].as_str().unwrap(),c["relation"].as_str().unwrap()),"basis":"source_route","refs":[c["comparison_id"]]})));
    json!(out)
}
fn fact_statement(s: &Value, e: &Value) -> String {
    format!(
        "Observed excerpt {} at {}; content SHA-256 {}.",
        e["excerpt_id"].as_str().unwrap(),
        s["revision"].as_str().unwrap(),
        e["sha256"].as_str().unwrap()
    )
}
fn role(d: &str) -> Result<&'static str, String> {
    match d {
        "locate_compare" => Ok("agent"),
        "review_integrate" => Ok("manager"),
        "cross_undertaking_coordination" => Ok("person"),
        _ => Err("Unknown contribution duty".into()),
    }
}
/// Called after shape validation. Internal consistency cannot establish original custody.
pub fn validate_cold(v: &Value) -> Result<(), String> {
    let mut common = v.clone();
    common["interpretations"] = json!([]);
    require(
        serde_json::to_vec(v).map_err(|e| e.to_string())?.len()
            <= crate::connector_materialization::BYTE_LIMIT,
        "Format0.4 exceeds1MiB serialized bytes",
    )?;
    crate::connector_materialization::validate_common(&common)?;
    let req = &v["evidence"]["git_request"];
    let path = text(&v["evidence"], "selected_path")?;
    require(
        !path.is_empty()
            && !path.starts_with('/')
            && !path.contains('\0')
            && path
                .split('/')
                .all(|p| !p.is_empty() && p != "." && p != ".."),
        "Invalid selected path",
    )?;
    require(
        text(req, "at")?.len() == text(req, "since")?.len(),
        "Mixed repository object formats",
    )?;
    let mut ids = HashSet::new();
    let mut excerpts = HashMap::new();
    let mut sides = HashSet::new();
    for s in list(v, "sources")? {
        require(ids.insert(text(s, "source_id")?), "Duplicate identifier")?;
        require(s["path"] == path, "Selected path mismatch")?;
        sides.insert(text(&s["provenance"], "side")?);
        for e in list(s, "excerpts")? {
            require(!text(e, "text")?.contains('\0'), "NUL excerpt")?;
            let id = text(e, "excerpt_id")?;
            require(ids.insert(id), "Duplicate identifier")?;
            excerpts.insert(id, (s, e));
            let anchor = text(e, "anchor")?;
            let first = anchor
                .trim_start_matches('L')
                .split('-')
                .next()
                .unwrap()
                .parse::<u64>()
                .map_err(|_| "Bad anchor")?;
            require(
                e["byte_start"].as_u64().unwrap() >= first - 1,
                "Impossible preceding line offset",
            )?;
        }
    }
    let mut facts = HashMap::new();
    let mut seen = HashSet::new();
    for f in list(v, "facts")? {
        let id = text(f, "fact_id")?;
        require(ids.insert(id), "Duplicate identifier")?;
        let eid = text(f, "excerpt_id")?;
        let (s, e) = excerpts.get(eid).ok_or("Dangling fact excerpt")?;
        require(
            seen.insert(eid)
                && f["source_id"] == s["source_id"]
                && f["anchor"] == e["anchor"]
                && f["statement"] == fact_statement(s, e),
            "Fact binding/statement mismatch",
        )?;
        facts.insert(id, f);
    }
    require(
        seen.len() == excerpts.len(),
        "Every excerpt needs exactly one fact",
    )?;
    let mut pairs = HashSet::new();
    let mut comparisons = HashMap::new();
    for c in list(v, "comparisons")? {
        let id = text(c, "comparison_id")?;
        require(ids.insert(id), "Duplicate identifier")?;
        let sf = facts
            .get(text(c, "since_fact_id")?)
            .ok_or("Missing since fact")?;
        let af = facts.get(text(c, "at_fact_id")?).ok_or("Missing at fact")?;
        let (ss, se) = excerpts[text(sf, "excerpt_id")?];
        let (ats, ae) = excerpts[text(af, "excerpt_id")?];
        require(
            ss["provenance"]["side"] == "since" && ats["provenance"]["side"] == "at",
            "Reversed comparison",
        )?;
        require(
            pairs.insert((text(c, "since_fact_id")?, text(c, "at_fact_id")?)),
            "Duplicate comparison pair",
        )?;
        let relation = if se["text"] == ae["text"] {
            "same_excerpt_bytes"
        } else {
            "different_excerpt_bytes"
        };
        require(c["relation"] == relation, "False byte relation")?;
        comparisons.insert(id, c);
    }
    let mut claims = HashMap::new();
    for c in list(v, "claims")? {
        let id = text(c, "claim_id")?;
        require(ids.insert(id), "Duplicate identifier")?;
        for f in list(c, "fact_ids")? {
            require(
                facts.contains_key(f.as_str().ok_or("Bad fact ref")?),
                "Dangling claim fact",
            )?;
        }
        for p in list(c, "comparison_ids")? {
            require(
                comparisons.contains_key(p.as_str().ok_or("Bad pair ref")?),
                "Dangling claim pair",
            )?;
        }
        require(
            c["scope"] != "record_change" || !list(c, "comparison_ids")?.is_empty(),
            "Change claim requires pair",
        )?;
        claims.insert(id, c);
    }
    for c in list(v, "contradictions")? {
        let id = text(c, "contradiction_id")?;
        require(ids.insert(id), "Duplicate identifier")?;
        for cr in list(c, "claim_ids")? {
            require(
                claims.contains_key(cr.as_str().ok_or("Bad claim ref")?),
                "Dangling contradiction claim",
            )?;
        }
        let gap = json!({"origin":"caller_reported","gap":c["description"],"effect":c["effect"],"responsible":c["responsible"],"context":{"side":"general","requested_commit":null,"path":null}});
        require(list(v, "gaps")?.contains(&gap), "Missing contradiction gap")?;
        require(
            list(&v["conclusions"], "unsupported")?.contains(
                &json!({"conclusion":format!("Contradiction {id} resolved"),"why":c["effect"]}),
            ),
            "Missing contradiction unsupported effect",
        )?;
    }
    for r in list(v, "contribution_reports")? {
        require(ids.insert(text(r, "report_id")?), "Duplicate identifier")?;
        for f in list(r, "fact_ids")? {
            require(
                facts.contains_key(f.as_str().ok_or("Bad report fact")?),
                "Dangling report fact",
            )?;
        }
    }
    require(
        v["conclusions"]["supported"] == supported(v),
        "Mechanical support mismatch",
    )?;
    require(
        list(v, "gaps")?
            .iter()
            .any(|g| g["origin"] == "producer_limit"),
        "Missing producer limitation",
    )?;
    let mut failed = HashSet::new();
    for g in list(v, "gaps")? {
        if g["origin"] == "observed_git_failure" {
            let c = &g["context"];
            let side = text(c, "side")?;
            require(
                matches!(side, "at" | "since")
                    && !sides.contains(side)
                    && failed.insert(side)
                    && c["path"] == path
                    && c["requested_commit"] == req[side],
                "Invalid/duplicate failed-side context",
            )?;
        }
    }
    require(
        ["at", "since"]
            .iter()
            .all(|s| sides.contains(s) || failed.contains(s)),
        "Missing failed side",
    )?;
    Ok(())
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct PairInput {
    pub key: String,
    pub since_anchor: String,
    pub at_anchor: String,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ClaimInput {
    pub key: String,
    pub statement: String,
    pub asserted_by: String,
    pub asserted_role: String,
    pub scope: String,
    pub anchors: Vec<String>,
    pub pairs: Vec<String>,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ContradictionInput {
    pub claims: Vec<String>,
    pub description: String,
    pub effect: String,
    pub responsible: crate::connector_materialization::Responsibility,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ReportInput {
    pub duty: String,
    pub reported_by: String,
    pub reported_actor: Option<String>,
    pub reported_status: String,
    pub reason: String,
    pub anchors: Vec<String>,
}
#[derive(Clone, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Input {
    pub draft: crate::connector_materialization::PrepareInput,
    pub pairs: Vec<PairInput>,
    pub claims: Vec<ClaimInput>,
    pub contradictions: Vec<ContradictionInput>,
    pub reports: Vec<ReportInput>,
}
#[cfg(unix)]
pub(crate) fn compose(
    e: &crate::connector_source::MaterializationEvidence,
    input: &Input,
    recorder: &str,
) -> Result<Value, String> {
    use crate::util::opaque_id;
    require(
        e.request["since"].is_string(),
        "Record comparison requires an explicit since pin",
    )?;
    require(
        input.draft.interpretations.is_empty(),
        "Use attributed record claims for format0.4",
    )?;
    require(
        input.pairs.len() <= 16
            && input.claims.len() <= 32
            && input.contradictions.len() <= 32
            && input.reports.len() <= 32,
        "Reconstruction input count limit",
    )?;
    let success =
        usize::from(e.at.is_ok()) + usize::from(e.since.as_ref().is_some_and(|s| s.is_ok()));
    require(
        input.draft.sources.len() == success,
        "Retain every successful requested side",
    )?;
    let mut v = crate::connector_materialization::compose_base(e, &input.draft, recorder)?;
    v["formatVersion"] = json!("0.4");
    v["standing"] = json!("bounded_record_comparison");
    v.as_object_mut().unwrap().remove("interpretations");
    v["evidence"]["selected_path"] = json!(e.relative.to_str().ok_or("Non UTF8 selected path")?);
    let mut facts = vec![];
    let mut anchor_facts = HashMap::new();
    let mut fact_text = HashMap::new();
    for (s, choice) in list(&v, "sources")?.iter().zip(&input.draft.sources) {
        for (excerpt, reference) in list(s, "excerpts")?.iter().zip(&choice.anchors) {
            let id = opaque_id("fact-")?;
            facts.push(json!({"fact_id":id,"source_id":s["source_id"],"excerpt_id":excerpt["excerpt_id"],"anchor":excerpt["anchor"],"statement":fact_statement(s,excerpt),"standing":"observed_record_excerpt_only"}));
            anchor_facts.insert(reference.clone(), id.clone());
            fact_text.insert(id, text(excerpt, "text")?.to_string());
        }
    }
    let resolve =
        |refs: &Vec<String>, map: &HashMap<String, String>| -> Result<Vec<String>, String> {
            refs.iter()
                .map(|r| {
                    map.get(r)
                        .cloned()
                        .ok_or_else(|| "Unknown/unselected reconstruction reference".into())
                })
                .collect()
        };
    let mut pairs = vec![];
    let mut pair_ids = HashMap::new();
    for p in &input.pairs {
        require(
            !p.key.is_empty() && !pair_ids.contains_key(&p.key),
            "Duplicate/empty pair key",
        )?;
        let sf = anchor_facts
            .get(&p.since_anchor)
            .ok_or("Unknown since anchor")?;
        let af = anchor_facts.get(&p.at_anchor).ok_or("Unknown at anchor")?;
        let id = opaque_id("comparison-")?;
        pairs.push(json!({"comparison_id":id,"since_fact_id":sf,"at_fact_id":af,"relation":if fact_text[sf]==fact_text[af]{"same_excerpt_bytes"}else{"different_excerpt_bytes"},"standing":"checked_excerpt_relation_only"}));
        pair_ids.insert(p.key.clone(), id);
    }
    let mut claims = vec![];
    let mut claim_ids = HashMap::new();
    for c in &input.claims {
        require(
            !c.key.is_empty() && !claim_ids.contains_key(&c.key),
            "Duplicate/empty claim key",
        )?;
        let id = opaque_id("claim-")?;
        claims.push(json!({"claim_id":id,"statement":c.statement,"asserted_by":c.asserted_by,"asserted_role":c.asserted_role,"attribution_standing":"caller_asserted_identity","scope":c.scope,"standing":"attributed_record_claim_not_verified_truth","fact_ids":resolve(&c.anchors,&anchor_facts)?,"comparison_ids":resolve(&c.pairs,&pair_ids)?}));
        claim_ids.insert(c.key.clone(), id);
    }
    let mut contradictions = vec![];
    for c in &input.contradictions {
        let id = opaque_id("contradiction-")?;
        let responsibility =
            json!({"standing":c.responsible.standing,"identity":c.responsible.identity});
        contradictions.push(json!({"contradiction_id":id,"claim_ids":resolve(&c.claims,&claim_ids)?,"description":c.description,"effect":c.effect,"responsible":responsibility,"standing":"caller_reported_unresolved"}));
        v["gaps"].as_array_mut().unwrap().push(json!({"origin":"caller_reported","gap":c.description,"effect":c.effect,"responsible":responsibility,"context":{"side":"general","requested_commit":null,"path":null}}));
        v["conclusions"]["unsupported"]
            .as_array_mut()
            .unwrap()
            .push(json!({"conclusion":format!("Contradiction {id} resolved"),"why":c.effect}));
    }
    let mut reports = vec![];
    for r in &input.reports {
        reports.push(json!({"report_id":opaque_id("report-")?,"duty":r.duty,"actor_role":role(&r.duty)?,"reported_by":r.reported_by,"reported_actor":r.reported_actor,"reported_status":r.reported_status,"reason":r.reason,"fact_ids":resolve(&r.anchors,&anchor_facts)?,"standing":"unverified_contribution_report","performance_verification":"not_established"}));
    }
    for g in v["gaps"].as_array_mut().unwrap() {
        if g["origin"] == "producer_limit" {
            g["gap"]=json!("Selected record excerpts only; completeness, truth, actual duties and authority unestablished");
            g["effect"]=json!("No whole-record or substantive-change conclusion from byte comparison; no verified performance");
        }
    }
    v["conclusions"]["unsupported"][0] = json!({"conclusion":"Whole-record meaning, completeness, truth, actual duties and authority","why":"Selected excerpts and attributed claims/reports do not establish these"});
    v["facts"] = json!(facts);
    v["comparisons"] = json!(pairs);
    v["claims"] = json!(claims);
    v["contradictions"] = json!(contradictions);
    v["contribution_reports"] = json!(reports);
    v["conclusions"]["supported"] = supported(&v);
    crate::connector_route_store::validate_account(&v).map_err(|e| e.to_string())?;
    Ok(v)
}
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub fn prepare(
    registry: &std::sync::Mutex<crate::connector_materialization::Registry>,
    source: &std::sync::Mutex<crate::connector_source::Session>,
    input: Input,
    project: &std::path::Path,
) -> Result<Value, String> {
    crate::connector_materialization::prepare_composed(
        registry,
        source,
        input.draft.clone(),
        project,
        || {},
        |e, _, recorder| compose(e, &input, recorder),
    )
}
