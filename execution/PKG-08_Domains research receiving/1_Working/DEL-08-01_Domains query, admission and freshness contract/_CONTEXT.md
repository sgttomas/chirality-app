# Context: DEL-08-01 Domains query, admission and freshness contract

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-08
- **Package Name:** Domains research receiving
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-08-01
- **PackageID:** PKG-08
- **Name:** Domains query, admission and freshness contract
- **Description:** Define a usable Domains receiving contract that treats search as evidence location and establishes admitted source standing, freshness and limitations before research reliance. Interfaces: Provider/query tool identity remains OI-023/OI-026; PKG-05 local data boundary applies; DEL-08-02 consumes the contract; PEC has no dependency role. Verification: Query results preserve references and limitations without becoming source authority; deployment is compatible with local-operation constraints before dependent implementation or reliance.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared Domains receiving owner; provider/tool owner remains unresolved
- **AnticipatedArtifacts:** DOC: source-admission/query/provenance/freshness contract;CONFIG: candidate query/result fixtures after source admission;TEST: unavailable/unsuitable/stale-source cases;DOC: provider/tool/deployment/data-boundary decision account
- **CoversScopeItems:** SOW-023;SOW-024;SOW-025;SOW-247;SOW-249
- **SupportsObjectives:** OBJ-007
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: receiving definition develops in parallel; Domains joins a subsequent connected increment.

## Package boundary

- **ScopeDescription:** Source-admitted Domains query consumption and the later research-context-to-design-candidate receiving activity.
- **InclusionCriteria:** App/shared query/admission contract and coordinated research workflow, provenance, freshness and later host receiving evidence.
- **Exclusions:** Provider construction/ownership is unresolved; SWB candidate implementation remains external; no corpus, database, deployment or new role is selected.
