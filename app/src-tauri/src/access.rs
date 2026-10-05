//! Explicit per-conversation selection and home-scoped account observations.
//! Credential custody and sign-in remain Codex's; this module stores no token/key.
use crate::util::now_rfc3339;
use serde_json::{json, Value};

pub struct AccountObservation {
    home: String,
    generation: Value,
    account: Value,
    observed: bool,
}
impl AccountObservation {
    pub fn new(home: String, generation: Value) -> Result<Self, String> {
        if home.is_empty()
            || generation["home"] != home
            || generation["appSession"]
                .as_str()
                .map(str::is_empty)
                .unwrap_or(true)
            || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
        {
            return Err("account home/generation required".into());
        }
        Ok(Self {
            home,
            generation,
            account: Value::Null,
            observed: false,
        })
    }
    pub fn read(&mut self, generation: &Value, result: &Value) -> Result<(), String> {
        if generation != &self.generation {
            return Err("foreign account generation".into());
        }
        let account = result
            .get("account")
            .ok_or("account/read has no account field")?;
        if !account.is_null()
            && !matches!(
                account["type"].as_str(),
                Some("chatgpt" | "apiKey" | "chatgptAuthTokens")
            )
        {
            return Err("unknown native account kind".into());
        }
        self.account = account.clone();
        self.observed = true;
        Ok(())
    }
    pub fn lost(&mut self) {
        self.account = Value::Null;
        self.observed = false;
    }
    pub fn codex_account(&self) -> Option<String> {
        if !self.observed || self.account["type"] != "chatgpt" {
            return None;
        }
        Some(
            self.account["email"]
                .as_str()
                .filter(|s| !s.is_empty())
                .unwrap_or("ChatGPT account (no email reported)")
                .into(),
        )
    }
    pub fn snapshot(&self) -> Value {
        json!({"home":self.home,"generation":self.generation,"state":if self.observed{"observed"}else{"unknown"},"nativeAccount":self.account,"codexAccount":self.codex_account(),"identityVerified":false})
    }
}

pub struct ConversationSelection {
    project: Option<String>,
    record: Value,
    offered_provider: Option<String>,
    home: Option<String>,
    generation: Option<Value>,
}
impl ConversationSelection {
    pub fn new(conversation: &str, project: &str) -> Result<Self, String> {
        if conversation.is_empty() || project.is_empty() {
            return Err("conversation/project required".into());
        }
        Self::new_explicit(conversation, Some(project))
    }
    /// The native Root/shared owner supplies a frozen explicit reference or
    /// explicit absence. Neither native cwd/home nor renderer text is a source.
    pub fn new_explicit(conversation: &str, project: Option<&str>) -> Result<Self, String> {
        if conversation.is_empty() || project.is_some_and(str::is_empty) {
            return Err("conversation/nonempty explicit project required".into());
        }
        let record = match project {
            Some(project) => {
                json!({"schema":"chirality.access-selection/v0.2","conversation":conversation,"project":project,"state":"no-selection","selection":null})
            }
            None => json!({"conversation":conversation,"state":"no-selection","selection":null}),
        };
        Ok(Self {
            project: project.map(str::to_owned),
            record,
            offered_provider: None,
            home: None,
            generation: None,
        })
    }
    pub fn project(&self) -> Option<&str> {
        self.project.as_deref()
    }
    pub fn canonical_record(&self) -> Option<Value> {
        self.project.as_ref().map(|_| self.record.clone())
    }
    /// Derived live source view, never a new durable selection schema.
    pub fn view(&self) -> Value {
        let mut view = self.record.clone();
        view.as_object_mut().unwrap().remove("schema");
        view.as_object_mut().unwrap().remove("project");
        view["projectContext"] = json!({"reference":self.project,"standing":if self.project.is_some(){"explicit App reference frozen for this selection"}else{"App project not established"}});
        view["canonicalSelectionRecord"] = json!(self.canonical_record());
        view["projectSensitiveChoiceAvailable"] = json!(self.project.is_some());
        view["viewStanding"] =
            json!("derived live selection; no native/history/cold authority from this view");
        view
    }
    pub fn offer_last(&mut self, entry: &str, provider: &str, model: &str) -> Result<(), String> {
        if self.project.is_none() {
            return Err(
                "project last-choice offer unavailable: App project not established".into(),
            );
        }
        if self.record["state"] != "no-selection"
            || [entry, provider, model].iter().any(|s| s.is_empty())
        {
            return Err("last-choice offer not available".into());
        }
        self.record["state"] = json!("offer-shown");
        self.record["offer"] = json!({"entryId":entry,"model":model,"label":"your last choice for this project","applied":false});
        self.offered_provider = Some(provider.into());
        Ok(())
    }
    pub fn choose(
        &mut self,
        entry: &str,
        provider: &str,
        model: &str,
        accept_offer: bool,
    ) -> Result<(), String> {
        if self.record.get("thread").is_some() {
            return Err("start a new conversation for another access mode".into());
        }
        if self.record["state"] == "starting" {
            return Err("thread start in progress".into());
        }
        if [entry, provider, model].iter().any(|s| s.is_empty()) {
            return Err("explicit entry, provider and model required".into());
        }
        if accept_offer
            && (self.record["state"] != "offer-shown"
                || self.record["offer"]["entryId"] != entry
                || self.record["offer"]["model"] != model
                || self.offered_provider.as_deref() != Some(provider))
        {
            return Err("offered choice differs".into());
        }
        self.record["state"] = json!("selected");
        self.record["selection"] = json!({"entryId":entry,"providerId":provider,"model":model,"source":if accept_offer{"offered-last-choice-accepted"}else{"person"},"chosenAt":now_rfc3339()});
        self.record.as_object_mut().unwrap().remove("offer");
        self.record.as_object_mut().unwrap().remove("refusal");
        Ok(())
    }
    pub fn start_params(
        &mut self,
        generation: &Value,
        home_kind: &str,
        run_requested: bool,
    ) -> Result<Value, String> {
        if self.record["selection"].is_null() {
            let message = if run_requested {
                "run not started — no model selected"
            } else {
                "not started — no model selected"
            };
            self.record["refusal"] =
                json!({"reason":"no-model-selected","text":message,"runRequested":run_requested});
            return Err(message.into());
        }
        if !matches!(
            self.record["state"].as_str(),
            Some("selected" | "start-failed")
        ) {
            return Err("selection is not ready to start".into());
        }
        if !matches!(home_kind, "account" | "api-key")
            || generation["home"]
                .as_str()
                .map(str::is_empty)
                .unwrap_or(true)
            || generation["appSession"]
                .as_str()
                .map(str::is_empty)
                .unwrap_or(true)
            || generation["spawnCounter"].as_u64().unwrap_or(0) == 0
        {
            return Err("full owning home generation required".into());
        }
        if self.record["selection"]["entryId"] == "api-key" && home_kind != "api-key" {
            return Err("API-key entry requires its own home".into());
        }
        if self.record["selection"]["entryId"] == "chatgpt-account" && home_kind != "account" {
            return Err("ChatGPT entry requires account home".into());
        }
        self.home = Some(home_kind.into());
        self.generation = Some(generation.clone());
        self.record["state"] = json!("starting");
        Ok(
            json!({"model":self.record["selection"]["model"],"modelProvider":self.record["selection"]["providerId"]}),
        )
    }
    pub fn started(&mut self, generation: &Value, result: &Value) -> Result<(), String> {
        if self.record["state"] != "starting" || self.generation.as_ref() != Some(generation) {
            return Err("foreign or unexpected start response".into());
        }
        let thread = result["thread"]["id"]
            .as_str()
            .filter(|s| !s.is_empty())
            .ok_or("thread/start has no thread identity")?;
        let reported = match (result["modelProvider"].as_str(), result["model"].as_str()) {
            (Some(provider), Some(model)) => json!({"provider":provider,"model":model}),
            _ => Value::Null,
        };
        self.record["thread"] = json!({"threadId":thread,"home":self.home,"requested":{"provider":self.record["selection"]["providerId"],"model":self.record["selection"]["model"]},"reported":reported});
        self.record["state"] = json!("started");
        Ok(())
    }
    pub fn start_failed(&mut self, reason: &str) -> Result<(), String> {
        if self.record["state"] != "starting" {
            return Err("no pending start".into());
        }
        self.record["state"] = json!("start-failed");
        self.record["refusal"] = json!({"reason":"start-failed","text":reason});
        Ok(())
    }
    pub fn unavailable(&mut self, reason: &str) -> Result<(), String> {
        if self.record["selection"].is_null() {
            return Err("no selected entry".into());
        }
        self.record["state"] = json!("entry-unavailable");
        self.record["refusal"] = json!({"reason":"entry-unavailable","text":reason});
        Ok(())
    }
    pub fn snapshot(&self) -> Value {
        self.canonical_record().unwrap_or_else(|| self.view())
    }
    pub fn recovery_home(&self) -> Option<&'static str> {
        match self.home.as_deref() {
            Some("account") => Some("H-acct"),
            Some("api-key") => Some("H-key"),
            _ => None,
        }
    }
    pub fn owning_generation(&self) -> Option<&Value> {
        self.generation.as_ref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn g() -> Value {
        json!({"appSession":"s","home":"h","spawnCounter":1})
    }
    fn valid(selection: &ConversationSelection) {
        let schema: Value = serde_json::from_str(include_str!(
            "../resources/runtime_core/access.conversation-selection.schema.json"
        ))
        .unwrap();
        jsonschema::options()
            .offline()
            .build(&schema)
            .unwrap()
            .validate(&selection.snapshot())
            .unwrap();
    }
    #[test]
    fn last_choice_is_only_an_offer_and_never_a_configuration_default() {
        let mut choice = ConversationSelection::new("c", "p").unwrap();
        valid(&choice);
        choice
            .offer_last("chatgpt-account", "openai", "model")
            .unwrap();
        valid(&choice);
        assert_eq!(
            choice.start_params(&g(), "account", true).unwrap_err(),
            "run not started — no model selected"
        );
        assert_eq!(choice.snapshot()["selection"], Value::Null);
        valid(&choice);
        choice
            .choose("chatgpt-account", "openai", "model", true)
            .unwrap();
        valid(&choice);
        assert_eq!(
            choice.start_params(&g(), "account", false).unwrap(),
            json!({"model":"model","modelProvider":"openai"})
        );
        valid(&choice);
        choice.started(&g(),&json!({"thread":{"id":"t"},"model":"reported-model","modelProvider":"reported-provider"})).unwrap();
        valid(&choice);
        assert_eq!(choice.snapshot()["thread"]["requested"]["model"], "model");
        assert_eq!(
            choice.snapshot()["thread"]["reported"]["model"],
            "reported-model"
        );
        assert!(choice
            .choose("api-key", "openai", "different", false)
            .is_err());
    }
    #[test]
    fn closed_generation_and_unavailable_entry_never_choose_fallback() {
        let mut choice = ConversationSelection::new("c", "p").unwrap();
        choice.choose("api-key", "openai", "m", false).unwrap();
        assert!(choice.start_params(&g(), "account", false).is_err());
        choice.start_params(&g(), "api-key", false).unwrap();
        let foreign = json!({"appSession":"other","home":"h","spawnCounter":1});
        assert!(choice
            .started(&foreign, &json!({"thread":{"id":"t"}}))
            .is_err());
        choice
            .start_failed("unknown: generation closed without response")
            .unwrap();
        valid(&choice);
        assert_eq!(choice.snapshot()["selection"]["entryId"], "api-key");
        choice.unavailable("key removed").unwrap();
        assert!(choice.start_params(&g(), "api-key", false).is_err());
        valid(&choice);
    }
    #[test]
    fn account_identity_requires_reported_home_scoped_account_not_plan_guessing() {
        let mut account = AccountObservation::new("h".into(), g()).unwrap();
        assert_eq!(account.codex_account(), None);
        account
            .read(
                &g(),
                &json!({"account":{"type":"chatgpt","email":null,"planType":"plus"}}),
            )
            .unwrap();
        assert_eq!(
            account.codex_account().unwrap(),
            "ChatGPT account (no email reported)"
        );
        account.read(&g(),&json!({"account":{"type":"chatgpt","email":"invented@example.invalid","planType":"pro"}})).unwrap();
        assert_eq!(account.codex_account().unwrap(), "invented@example.invalid");
        account.lost();
        assert_eq!(account.codex_account(), None);
        assert!(account.read(&json!(1), &json!({"account":null})).is_err());
        account
            .read(&g(), &json!({"account":{"type":"apiKey"}}))
            .unwrap();
        assert_eq!(account.codex_account(), None);
    }

    #[test]
    fn explicit_unknown_project_has_no_row_offer_or_default_but_person_choice_starts() {
        let mut choice = ConversationSelection::new_explicit("unknown", None).unwrap();
        assert_eq!(choice.project(), None);
        assert!(choice.canonical_record().is_none());
        assert!(choice.snapshot().get("schema").is_none());
        assert!(choice.snapshot().get("project").is_none());
        assert_eq!(choice.snapshot()["projectSensitiveChoiceAvailable"], false);
        assert!(choice.offer_last("chatgpt-account", "openai", "m").is_err());
        assert!(choice
            .start_params(&g(), "account", false)
            .unwrap_err()
            .contains("no model selected"));
        assert!(choice
            .choose("chatgpt-account", "openai", "m", true)
            .is_err());
        choice
            .choose("chatgpt-account", "openai", "m", false)
            .unwrap();
        assert_eq!(
            choice.start_params(&g(), "account", false).unwrap(),
            json!({"model":"m","modelProvider":"openai"})
        );
        choice.started(&g(),&json!({"thread":{"id":"t"},"cwd":"/native/Q","projectId":"native-id","model":"m","modelProvider":"openai"})).unwrap();
        assert_eq!(choice.snapshot()["state"], "started");
        assert!(choice.canonical_record().is_none());
        assert_eq!(choice.project(), None);
    }
    #[test]
    fn explicit_known_context_is_frozen_and_canonical_shape_unchanged() {
        let choice = ConversationSelection::new_explicit("c", Some("App P / 家")).unwrap();
        valid(&choice);
        assert_eq!(choice.canonical_record().unwrap(), choice.snapshot());
        let mut view = choice.view();
        view["projectContext"]["reference"] = json!("current Q");
        assert_eq!(choice.project(), Some("App P / 家"));
        assert_eq!(choice.snapshot()["project"], "App P / 家");
        assert!(ConversationSelection::new_explicit("c", Some("")).is_err());
        assert!(ConversationSelection::new("c", "").is_err());
    }
}
