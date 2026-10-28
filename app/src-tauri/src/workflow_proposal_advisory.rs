//! Read-only CK-1 for an actual selected workflow or verified native offer.
//! Reading a closed subject never creates or changes the person's choice.
use super::*;
use crate::execution_compatibility::report;
use crate::role_lifecycle::RoleInForce;
use serde::{Deserialize, Serialize};
use std::path::Path;

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct ProposalMessage {
    thread_id: String,
    turn_id: String,
    item_id: String,
}
impl From<&crate::run_offers::ItemRef> for ProposalMessage {
    fn from(item: &crate::run_offers::ItemRef) -> Self {
        Self {
            thread_id: item.thread.clone(),
            turn_id: item.turn.clone(),
            item_id: item.item.clone(),
        }
    }
}
/// Expected display correspondence only. The owning host independently
/// resolves the proposal, source and revision again at the ordinary press.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub(crate) struct ProposalContext {
    source_ref: String,
    home: String,
    generation: Value,
    message: ProposalMessage,
    proposed: String,
    run_ref: Option<String>,
    library_ref: String,
    workflow: crate::workflow_workspace::WorkflowIdentity,
    holding_library: String,
    role_supply_ref: Option<String>,
}

fn role_in_conversation(home: &HomeSession, native_home: &str, thread: &str) -> RoleInForce {
    match home.history.try_lock() {
        Ok(history) => history
            .binding(native_home, thread)
            .map(|binding| binding.role_in_force(native_home, thread))
            .unwrap_or(RoleInForce::Unknown {
                reason: "original App supply binding not established".into(),
            }),
        Err(_) => RoleInForce::Unknown {
            reason: "role binding owner busy; not read".into(),
        },
    }
}
fn role_supply(role: &RoleInForce) -> Option<String> {
    match role {
        RoleInForce::AppObserved { supply_ref, .. } => Some(supply_ref.clone()),
        _ => None,
    }
}
// Same evaluator and honest unobserved environment for both CK-1 receiving
// surfaces. The closed subject is read only; no selection or report is stored.
fn compatibility_for_subject(
    selection: &crate::workflow_workspace::Selection,
    holding_library: &str,
    role: RoleInForce,
    generation: &Value,
    thread: &str,
    label: &str,
) -> Value {
    let basis = report::Basis {
        home: generation["home"].as_str().unwrap_or("").into(),
        generation: generation.clone(),
        conversation: thread.into(),
        acting_pin: "App Codex 0.160.0".into(),
        surface: "X".into(),
        environment_observation: None,
        catalog_edition: None,
    };
    let compatibility = match report::evaluate(report::Request {
        selection,
        holding_library: Some(holding_library.into()),
        role,
        basis: basis.clone(),
        occasion: report::Occasion::Selection,
        evaluated_at: crate::util::now_rfc3339(),
        inventory: report::Inventory {
            origin: report::InventoryOrigin::CallerSupplied {
                source: "App Root: no environment collector; nothing observed".into(),
            },
            host_id: None,
            observations: report::Observations::default(),
        },
        model_destination: None,
    }) {
        Ok(evaluation) => evaluation.view(&basis),
        Err(limit) => unavailable_compatibility(limit),
    };
    label_compatibility(compatibility, label)
}
fn unavailable_compatibility(limit: impl Into<String>) -> Value {
    json!({"preparation":null,"state":"no evaluation","limit":limit.into(),"advisory":true})
}
fn label_compatibility(mut compatibility: Value, label: &str) -> Value {
    compatibility["occasionLabel"] = json!(label);
    compatibility["gate"] = json!("informs only; never gates a start (CC-3)");
    compatibility["r14"] = json!("no report stored; no R14 written");
    compatibility
}
fn context_for(
    home: &HomeSession,
    generation: &Value,
    message: &crate::run_offers::ItemRef,
    named: &crate::run_offers::Named,
    run_ref: Option<&str>,
    found: &ProposedRevision,
    store: &Path,
    role: &RoleInForce,
) -> Result<ProposalContext, String> {
    Ok(ProposalContext {
        source_ref: home.workflow_source_ref.clone(),
        home: generation["home"]
            .as_str()
            .ok_or("Original proposal home not established")?
            .into(),
        generation: generation.clone(),
        message: message.into(),
        proposed: named.text(),
        run_ref: run_ref.map(str::to_owned),
        library_ref: found.library.reference.clone(),
        workflow: found.identity.clone(),
        holding_library: store
            .parent()
            .and_then(Path::to_str)
            .ok_or("Original proposal holding library unavailable")?
            .into(),
        role_supply_ref: role_supply(role),
    })
}

impl WorkflowRootSession {
    /// Display only: no selection, prepared run, lifecycle event, native
    /// dispatch, report storage or R14 publication is made by an offer read.
    pub(crate) fn offers_for_home(&self, view: &Value, home: &HomeSession) -> Value {
        let host = home.host.snapshot();
        let generation = &host["generation"];
        if view["generation"] != *generation || view["home"] != generation["home"] {
            return json!([]);
        }
        let mut offers = self.offers(view);
        for offer in offers.as_array_mut().into_iter().flatten() {
            if !offer["proposal"]["resolution"]["workflow"].is_object() {
                continue;
            }
            let subject = (|| {
                let message = crate::run_offers::ItemRef::from_value(&offer["message"])?;
                current_conversation(&host, generation, &message.thread)?;
                let native_home = generation["home"]
                    .as_str()
                    .ok_or("Original proposal home absent")?;
                let (_, named) = crate::run_offers::verify_proposal(
                    view,
                    &message.thread,
                    &self.supersessions(view, native_home, &message.thread),
                    &message,
                )?;
                let found = self.resolve_proposal(&named)?;
                let store = found
                    .library
                    .owner
                    .try_lock()
                    .map_err(|_| "Original proposal library busy; refresh the offer")?
                    .store_copy(&found.identity);
                let selection = found.revision.select();
                crate::storage::check_path(&store)?;
                selection.verify_store(&store)?;
                let run = self.run_in_force(native_home, &message.thread)?;
                let role = role_in_conversation(home, native_home, &message.thread);
                let context = context_for(
                    home,
                    generation,
                    &message,
                    &named,
                    run.as_ref().map(|(id, _)| id.as_str()),
                    &found,
                    &store,
                    &role,
                )?;
                Ok::<_, String>((context, selection, role))
            })();
            let (context, selection, role) = match subject {
                Ok(subject) => subject,
                Err(cause) => {
                    offer["proposal"]["resolution"] = json!({"workflow":null,"notice":cause});
                    continue;
                }
            };
            // Context is established independently of the advisory read. A
            // malformed declaration cannot erase a valid ordinary choice.
            offer["proposal"]["resolution"]["workflow"] = json!(context.workflow);
            offer["proposal"]["context"] = json!(context);
            offer["proposal"]["compatibility"] = compatibility_for_subject(
                &selection,
                &context.holding_library,
                role,
                &context.generation,
                &context.message.thread_id,
                "CK-1 offered candidate",
            );
        }
        offers
    }

    /// Display the existing per-chat closed choice in its owning Home only.
    /// Inspection is not a chat choice; another Home's same thread ID cannot
    /// supply the role or comparison basis. Existing mutation guards are intact.
    pub(crate) fn decorate_selected_compatibility(
        &self,
        status: &mut Value,
        view: &Value,
        home: &HomeSession,
    ) {
        let host = home.host.snapshot();
        let generation = &host["generation"];
        for row in status["selections"].as_array_mut().into_iter().flatten() {
            if row["sourceRef"] != home.workflow_source_ref {
                continue;
            }
            let Some(thread) = row["threadId"].as_str() else {
                continue;
            };
            let chat = crate::workflow_selection::Chat::in_home(home, thread);
            let Some(selected) = self.selected.get(&chat) else {
                continue;
            };
            let holding = selected.package.parent().and_then(Path::to_str);
            let subject = (|| {
                if view["generation"] != *generation || view["home"] != generation["home"] {
                    return Err(
                        "Selected workflow's original Home generation view is unavailable".into(),
                    );
                }
                current_conversation(&host, generation, thread)?;
                selected.selection.verify_store(&selected.package)?;
                let holding = holding.ok_or("Selected workflow holding library unavailable")?;
                Ok::<_, String>(compatibility_for_subject(
                    &selected.selection,
                    holding,
                    role_in_conversation(home, generation["home"].as_str().unwrap_or(""), thread),
                    generation,
                    thread,
                    "CK-1 selected candidate",
                ))
            })();
            let mut compatibility = subject.unwrap_or_else(|limit| {
                label_compatibility(unavailable_compatibility(limit), "CK-1 selected candidate")
            });
            compatibility["holdingLibrary"] = json!(holding);
            row["selection"]["compatibility"] = compatibility;
        }
    }

    /// Only the original displayed proposal/candidate is accepted here. The
    /// existing selection and lifecycle path remains the person's one choice.
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn start_proposed_disclosed(
        &mut self,
        view: &Value,
        home: std::sync::Arc<HomeSession>,
        generation: &Value,
        message: &Value,
        live: Option<&str>,
        person_text: String,
        project: Option<&Path>,
        context: &ProposalContext,
    ) -> Result<String, String> {
        self.start_proposed_with_context(
            view,
            home,
            generation,
            message,
            live,
            person_text,
            project,
            Some(context),
        )
    }

    #[allow(clippy::too_many_arguments)]
    pub(super) fn verify_disclosed_context(
        &self,
        view: &Value,
        home: &HomeSession,
        generation: &Value,
        message: &crate::run_offers::ItemRef,
        live: Option<&str>,
        named: &crate::run_offers::Named,
        found: &ProposedRevision,
        store: &Path,
        expected: &ProposalContext,
    ) -> Result<(), String> {
        if home.host.snapshot()["generation"] != *generation || view["generation"] != *generation {
            return Err("Original proposal generation changed; refresh the offer; nothing selected or started".into());
        }
        let role = role_in_conversation(
            home,
            generation["home"].as_str().unwrap_or(""),
            &message.thread,
        );
        let mut observed =
            context_for(home, generation, message, named, live, found, store, &role)?;
        if let (Some(original), Some(current)) =
            (&expected.role_supply_ref, &observed.role_supply_ref)
        {
            if original != current {
                return Err("Original proposal role source changed; refresh the offer; nothing selected or started".into());
            }
        }
        // Busy/missing role observation is Unknown, not evidence of a new
        // role or deliberate no-role. It must not become a compatibility gate.
        observed.role_supply_ref = expected.role_supply_ref.clone();
        if &observed != expected {
            return Err("Original displayed proposal source, run or workflow changed; refresh the offer; nothing selected or started".into());
        }
        Ok(())
    }
}
