//! New-conversation model discovery (DEL-01-05 access; DEL-01-04 presentation):
//! the models Codex reports, read only at the person's press.
//!
//! At the 0.160.0 pin `model/list` takes no provider (ModelListParams is
//! `{cursor?, includeHidden?, limit?}`): it answers for the provider the
//! app-server resolves for itself, read as `config/read`'s `model_provider`
//! with no folder and at the server's own folder (DEL-01-03 NPTD §7.1, as in
//! `delegation_availability`). This module turns those reads into a narrow
//! view: the server provider (or why it is not established) and each listed
//! model's `id`, `model`, `displayName`, a bounded `description` and
//! `isDefault`. No configuration body, other model field, hidden model,
//! entitlement or account fact is carried. Nothing here reads, writes or
//! starts anything; `Host::model_catalog_read` performs the reads.
use serde_json::{json, Value};

/// Pages followed before stopping with an explicit limit.
pub(crate) const MODEL_PAGES: usize = 20;
/// Entries kept; any beyond are reported as not shown.
pub(crate) const MAX_MODELS: usize = 200;
const DESCRIPTION_LIMIT: usize = 300;
pub(crate) const STANDING: &str = "Models Codex reports for the app-server's own provider in this Codex generation, read now at your press. A listed model is the supplier's reported availability for that provider, not your account's entitlement or access; Start still checks the current configuration.";

fn displayable_provider(value: &str) -> bool {
    let mut chars = value.chars();
    value.len() <= 64 && chars.next().is_some_and(|c| c.is_ascii_alphabetic())
        && chars.all(|c| c.is_ascii_alphanumeric() || matches!(c, '.' | '_' | '-'))
}
fn plain(value: &str) -> bool { !value.is_empty() && !value.chars().any(char::is_control) }

/// The provider the app-server resolves for its parameterless reads. Both
/// `config/read` readings must name the same provider; a null or absent
/// provider is kept as null (never inferred to be a built-in provider) and
/// matches no conversation provider.
pub(crate) fn server_provider(bare: Result<Value, String>, own: Result<Value, String>) -> Result<Option<String>, String> {
    let provider = |read: &Value| -> Result<Option<String>, String> {
        match &read["config"]["model_provider"] {
            Value::Null => Ok(None),
            Value::String(name) if displayable_provider(name) => Ok(Some(name.clone())),
            Value::String(_) => Err("the app-server's provider name is not a displayable provider identifier".into()),
            _ => Err("the app-server's configuration reports a provider that is not a name".into()),
        }
    };
    let (bare, own) = (provider(&bare?)?, provider(&own?)?);
    if bare != own {
        return Err(format!("the app-server's configuration names provider {} without a folder and {} at its own folder; neither is chosen",
            bare.as_deref().unwrap_or("none"), own.as_deref().unwrap_or("none")));
    }
    Ok(bare)
}

/// One listed model as shown, or None for a hidden or unreadable entry.
pub(crate) fn listed(entry: &Value) -> Option<Value> {
    if entry["hidden"] != Value::Bool(false) { return None; }
    let field = |name: &str| entry[name].as_str().filter(|v| plain(v) && v.len() <= 128).map(str::to_owned);
    let (id, model, display) = (field("id")?, field("model")?, field("displayName")?);
    let description: String = entry["description"].as_str().unwrap_or("").chars().filter(|c| !c.is_control()).take(DESCRIPTION_LIMIT).collect();
    Some(json!({"id":id,"model":model,"displayName":display,"description":description,"isDefault":entry["isDefault"] == Value::Bool(true)}))
}

/// The listed models, following `nextCursor` until it is null. A page error,
/// an empty or repeated cursor, or the page cap ends the read: what was read is
/// kept and marked incomplete, never presented as the whole list.
pub(crate) fn collect(mut page: impl FnMut(Option<String>) -> Result<Value, String>) -> (Vec<Value>, Vec<String>) {
    let (mut models, mut limits, mut cursor, mut skipped) = (Vec::new(), Vec::new(), None::<String>, 0usize);
    let mut finished = false;
    for _ in 0..MODEL_PAGES {
        let result = match page(cursor.clone()) { Ok(result) => result, Err(cause) => { limits.push(format!("model list incomplete: {cause}")); finished = true; break; } };
        for entry in result["data"].as_array().into_iter().flatten() {
            match listed(entry) {
                Some(row) if models.len() < MAX_MODELS => models.push(row),
                Some(_) => skipped += 1,
                None => {}
            }
        }
        match result["nextCursor"].as_str() {
            None => { finished = true; break; }
            Some("") => { limits.push("model list incomplete: Codex returned an empty page cursor".into()); finished = true; break; }
            Some(next) if cursor.as_deref() == Some(next) => { limits.push("model list incomplete: Codex repeated a page cursor".into()); finished = true; break; }
            Some(next) => cursor = Some(next.to_owned()),
        }
    }
    if !finished { limits.push(format!("model list incomplete: more models not read after {MODEL_PAGES} pages")); }
    if skipped > 0 { limits.push(format!("{skipped} further listed models not shown (at most {MAX_MODELS})")); }
    (models, limits)
}

/// The view returned to the web view.
pub(crate) fn view(generation: &Value, provider: Result<Option<String>, String>, models: (Vec<Value>, Vec<String>), read_at: &str) -> Value {
    let (models, limits) = models;
    let complete = limits.iter().all(|l| !l.starts_with("model list incomplete"));
    let mut out = json!({"state":if models.is_empty() && !complete {"unavailable"} else {"observed"},"generation":generation,
        "models":models,"complete":complete,"limits":limits,"readAt":read_at,"standing":STANDING});
    match provider {
        Ok(Some(name)) => out["serverProvider"] = json!(name),
        Ok(None) => { out["serverProvider"] = Value::Null; out["providerLimit"] = json!("the app-server's configuration names no provider; the list is not matched to any conversation provider"); }
        Err(cause) => { out["serverProvider"] = Value::Null; out["providerLimit"] = json!(format!("provider not established: {cause}")); }
    }
    out
}

/// A press that read nothing.
pub(crate) fn refused(generation: &Value, cause: &str, read_at: &str) -> Value {
    json!({"state":"unavailable","generation":generation,"models":[],"complete":false,"limits":[cause],"readAt":read_at,
        "serverProvider":Value::Null,"providerLimit":"not read","standing":STANDING})
}

#[cfg(test)]
mod tests {
    use super::*;
    fn entry(id: &str) -> Value { json!({"id":id,"model":id,"displayName":format!("Name {id}"),"description":"d","hidden":false,"isDefault":id=="b","defaultReasoningEffort":"medium","supportedReasoningEfforts":[],"upgrade":"secret-ish"}) }
    fn cfg(p: Value) -> Result<Value, String> { Ok(json!({"config":{"model_provider":p,"developer_instructions":"private text"}})) }

    #[test]
    fn provider_requires_agreement_and_never_infers_a_default() {
        assert_eq!(server_provider(cfg(json!("openai")), cfg(json!("openai"))), Ok(Some("openai".into())));
        assert_eq!(server_provider(cfg(Value::Null), cfg(Value::Null)), Ok(None));
        let e = server_provider(cfg(json!("openai")), cfg(json!("local"))).unwrap_err();
        assert!(e.contains("openai without a folder and local at its own folder; neither is chosen"), "{e}");
        assert!(server_provider(cfg(Value::Null), cfg(json!("openai"))).unwrap_err().contains("none without a folder"));
        assert!(server_provider(Err("config/read answered with an error".into()), cfg(json!("openai"))).unwrap_err().contains("answered with an error"));
        assert!(server_provider(cfg(json!("bad name!")), cfg(json!("bad name!"))).is_err());
        assert!(server_provider(cfg(json!(3)), cfg(json!(3))).is_err());
    }

    #[test]
    fn only_named_fields_of_visible_entries_are_kept() {
        let row = listed(&entry("a")).unwrap();
        assert_eq!(row, json!({"id":"a","model":"a","displayName":"Name a","description":"d","isDefault":false}));
        assert!(listed(&json!({"id":"h","model":"h","displayName":"H","description":"","hidden":true,"isDefault":false})).is_none());
        assert!(listed(&json!({"id":"h","model":"h","displayName":"H","description":""})).is_none(), "hidden not reported is not shown");
        assert!(listed(&json!({"id":"","model":"x","displayName":"X","description":"","hidden":false})).is_none());
        assert!(listed(&json!({"id":"x\n","model":"x","displayName":"X","description":"","hidden":false})).is_none());
        let long = listed(&json!({"id":"x","model":"x","displayName":"X","description":"y".repeat(500),"hidden":false,"isDefault":true})).unwrap();
        assert_eq!(long["description"].as_str().unwrap().len(), 300);
        assert_eq!(long["isDefault"], true);
    }

    #[test]
    fn paging_follows_cursors_and_marks_every_early_end_incomplete() {
        let pages = vec![json!({"data":[entry("a")],"nextCursor":"2"}), json!({"data":[entry("b"),{"hidden":true}],"nextCursor":null})];
        let mut seen = vec![];
        let (models, limits) = collect(|c| { seen.push(c.clone()); Ok(pages[seen.len() - 1].clone()) });
        assert_eq!(seen, vec![None, Some("2".to_string())]);
        assert_eq!(models.len(), 2); assert!(limits.is_empty());
        let v = view(&json!({"g":1}), Ok(Some("openai".into())), (models, limits), "t");
        assert_eq!(v["state"], "observed"); assert_eq!(v["complete"], true); assert_eq!(v["serverProvider"], "openai");
        assert!(!v.to_string().contains("secret-ish") && !v.to_string().contains("private text"));

        let mut n = 0;
        let (models, limits) = collect(|_| { n += 1; if n == 1 { Ok(json!({"data":[entry("a")],"nextCursor":"x"})) } else { Err("model/list answered with an error".into()) } });
        assert_eq!(models.len(), 1); assert!(limits[0].starts_with("model list incomplete: model/list answered"), "{limits:?}");
        assert_eq!(view(&json!(1), Ok(None), (models, limits), "t")["complete"], false);

        let (_, limits) = collect(|_| Ok(json!({"data":[],"nextCursor":"same"})));
        assert!(limits.iter().any(|l| l.contains("repeated a page cursor")), "{limits:?}");
        let (_, limits) = collect(|_| Ok(json!({"data":[],"nextCursor":""})));
        assert!(limits.iter().any(|l| l.contains("empty page cursor")));
        let mut k = 0;
        let (_, limits) = collect(|_| { k += 1; Ok(json!({"data":[],"nextCursor":format!("c{k}")})) });
        assert_eq!(k, MODEL_PAGES); assert!(limits.iter().any(|l| l.contains("more models not read after 20 pages")));
        let many: Vec<Value> = (0..MAX_MODELS + 5).map(|i| entry(&format!("m{i}"))).collect();
        let (models, limits) = collect(|_| Ok(json!({"data":many,"nextCursor":null})));
        assert_eq!(models.len(), MAX_MODELS); assert!(limits.iter().any(|l| l.starts_with("5 further listed models not shown")));
        let (models, limits) = collect(|_| Err("model/list not sent: the reading's time limit was reached".into()));
        let v = view(&json!(1), Err("x".into()), (models, limits), "t");
        assert_eq!(v["state"], "unavailable"); assert_eq!(v["providerLimit"], "provider not established: x");
    }
}
