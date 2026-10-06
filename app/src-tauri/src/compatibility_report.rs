//! In-memory advisory preparation; not the persisted EXEC report format or a receipt.
use super::*;
use crate::role_lifecycle::RoleInForce;
use crate::workflow_workspace::Selection;

#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
pub enum Occasion {
    Selection,
    BeforeFirstAction,
}
#[derive(Clone, Debug, Serialize, PartialEq, Eq)]
pub struct Basis {
    pub home: String,
    pub generation: Value,
    pub conversation: String,
    pub acting_pin: String,
    pub surface: String,
    pub environment_observation: Option<String>,
    pub catalog_edition: Option<String>,
}
/// Supplied only by the owning environment collector, not deserialized from the UI.
/// Partial means listed entries may be evaluated, but omission proves nothing.
pub enum CatalogCoverage {
    Unobserved,
    Partial(BTreeMap<String, Operation>),
    Complete(BTreeMap<String, Operation>),
}
pub struct Observations {
    pub catalog: CatalogCoverage,
    pub channel_enabled: Option<bool>,
    pub harness_signals: Option<Value>,
}
impl Default for Observations {
    fn default() -> Self {
        Self {
            catalog: CatalogCoverage::Unobserved,
            channel_enabled: None,
            harness_signals: None,
        }
    }
}
#[derive(Clone, Debug, Serialize)]
pub struct RequirementDisplay {
    pub name: String,
    pub purpose: Value,
    pub fallback: Value,
    pub outcome: Outcome,
    pub reason: String,
}
#[derive(Clone, Debug, Serialize)]
pub struct PreparedReport {
    id: String,
    basis: Basis,
    occasion: Occasion,
    evaluated_at: String,
    workflow: Value,
    declaration: Declaration,
    role: RoleInForce,
    check: Compatibility,
    requirements: Vec<RequirementDisplay>,
}
fn is_blocking(outcome: &Outcome) -> bool {
    matches!(
        outcome,
        Outcome::Missing
            | Outcome::VersionMismatch
            | Outcome::NotExposedOnThisSurface
            | Outcome::ChannelNotEnabled
    )
}
fn report_check(
    declaration: &Declaration,
    basis: &Basis,
    observations: &Observations,
    role: &RoleInForce,
) -> Compatibility {
    let catalog = match &observations.catalog {
        CatalogCoverage::Unobserved => None,
        CatalogCoverage::Partial(v) | CatalogCoverage::Complete(v) => Some(v.clone()),
    };
    let environment = Environment {
        catalog,
        channel_enabled: observations.channel_enabled.unwrap_or(true),
        harness_signals: observations.harness_signals.clone(),
        harness_pin: Some(basis.acting_pin.clone()),
    };
    let mut result = Compatibility::check(declaration, &environment);
    for (entry, row) in declaration
        .elements
        .get("required_tools")
        .into_iter()
        .flatten()
        .zip(result.tools.iter_mut())
    {
        if entry.value["class"] != "host_operation" {
            continue;
        }
        if matches!(observations.catalog, CatalogCoverage::Partial(_))
            && row.outcome == Outcome::Missing
        {
            row.outcome = Outcome::NotEstablished;
            row.reason =
                "operation absent from partial observation; absence not established".into();
        }
        if observations.channel_enabled.is_none()
            && matches!(
                row.outcome,
                Outcome::Present | Outcome::PresentCurrentlyUnavailable
            )
        {
            row.outcome = Outcome::NotEstablished;
            row.reason = "acting channel state not observed".into();
        }
    }
    let blocked = result
        .tools
        .iter()
        .any(|r| r.necessity == "required" && is_blocking(&r.outcome));
    let unknown = declaration.reading != Reading::Recognized
        || !matches!(
            declaration.categories.get("required_tools"),
            Some(Reading::Recognized | Reading::DeclaredEmpty)
        )
        || result.tools.iter().any(|r| {
            !matches!(r.necessity.as_str(), "required" | "optional")
                || (r.necessity == "required" && r.outcome == Outcome::NotEstablished)
        });
    result.result = if blocked {
        Check::Unsupported
    } else if unknown {
        Check::NotEstablished
    } else {
        Check::Compatible
    };
    match role {
        RoleInForce::AppObserved { role, .. } => {
            // Reuse role semantics without letting the legacy environment evaluation
            // replace the explicitly partial/unknown inventory result above.
            let mut role_only = declaration.clone();
            role_only.elements.remove("required_tools");
            role_only
                .categories
                .insert("required_tools".into(), Reading::DeclaredEmpty);
            // Preserve delegation requirement for the known TASK special case.
            if role.as_ref().is_some_and(|r| r.name() == "TASK") {
                role_only.elements.insert(
                    "required_tools".into(),
                    declaration
                        .elements
                        .get("required_tools")
                        .into_iter()
                        .flatten()
                        .filter(|e| e.value["capability"] == "agent-delegation")
                        .cloned()
                        .collect(),
                );
            }
            let checked = Compatibility::check_for_role(
                &role_only,
                &Environment::default(),
                role.as_ref().map(|r| r.name()),
            );
            if checked.result == Check::Unsupported {
                result.result = Check::Unsupported;
            } else if checked.result == Check::NotEstablished && result.result != Check::Unsupported
            {
                result.result = Check::NotEstablished;
            }
            result.findings.extend(checked.findings);
        }
        RoleInForce::Unknown { reason } => {
            let constrained = declaration
                .raw
                .as_ref()
                .and_then(|v| v.get("compatible_roles"))
                .is_some()
                || declaration
                    .elements
                    .get("required_tools")
                    .into_iter()
                    .flatten()
                    .any(|e| {
                        e.value["capability"] == "agent-delegation"
                            && e.value["necessity"] == "required"
                    });
            if constrained && result.result != Check::Unsupported {
                result.result = Check::NotEstablished;
            }
            result.findings.push(format!(
                "original role not established: {reason}; not a deliberate no-role selection"
            ));
        }
    }
    result
}
impl PreparedReport {
    pub fn prepare(
        selection: &Selection,
        basis: Basis,
        occasion: Occasion,
        evaluated_at: String,
        observations: &Observations,
        role: RoleInForce,
    ) -> Result<Self, String> {
        if basis.home.is_empty()
            || basis.conversation.is_empty()
            || basis.acting_pin.is_empty()
            || basis.surface.is_empty()
            || evaluated_at.is_empty()
        {
            return Err("report basis/occasion time absent".into());
        }
        let declaration = selection.snapshot().declaration()?;
        let check = report_check(&declaration, &basis, observations, &role);
        let requirements = declaration
            .elements
            .get("required_tools")
            .into_iter()
            .flatten()
            .zip(&check.tools)
            .map(|(e, r)| RequirementDisplay {
                name: r.name.clone(),
                purpose: e.value["purpose"].clone(),
                fallback: e.value["fallback"].clone(),
                outcome: r.outcome.clone(),
                reason: r.reason.clone(),
            })
            .collect();
        Ok(Self {
            id: crate::util::opaque_id("compatibility-preparation:")?,
            basis,
            occasion,
            evaluated_at,
            workflow: serde_json::to_value(selection.identity()).map_err(|e| e.to_string())?,
            declaration,
            role,
            check,
            requirements,
        })
    }
    pub fn result(&self) -> &Check {
        &self.check.result
    }
    /// Currency is a view; the original report and its basis remain immutable.
    pub fn view(&self, current_basis: &Basis) -> Value {
        let statement = match self.check.result {
            Check::Compatible => format!(
                "requirement check passes against {} on {} at {}",
                self.basis.catalog_edition.as_deref().unwrap_or(
                    "catalog not observed; no catalog-dependent requirement established"
                ),
                self.basis.surface,
                self.evaluated_at
            ),
            Check::Unsupported => {
                "requirement check does not pass; the person may still start".into()
            }
            Check::NotEstablished => {
                "requirement check not established; the person may still start".into()
            }
        };
        serde_json::json!({"preparation":self,"occasion":match self.occasion {Occasion::Selection=>"CK-1",Occasion::BeforeFirstAction=>"CK-2"},"notCurrent":&self.basis!=current_basis,"statement":statement,"recording":"not published; no EXEC report or RS R14 receipt","advisory":true,"adoption":"unknown"})
    }
}

#[cfg(test)]
#[path = "compatibility_report_tests.rs"]
mod tests;
