# Context: DEL-03-02 Proposal, validation and outcome contract

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-03
- **Package Name:** Host capability and operation contracts
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-03-02
- **PackageID:** PKG-03
- **Name:** Proposal, validation and outcome contract
- **Description:** Specify the same host validation/application path and truthful proposal lifecycle for all actors while domain truth and accepted results remain host-owned. Interfaces: Consumes DEL-03-01 basis/catalog and PKG-04 autonomy/act distinctions; DEL-03-03 external receiving uses this path; host views show old/new values and receipts. Verification: Stale proposals refuse with a reason, later selection cannot retarget, duplicate submission has one effect and unknown outcomes remain unknown; success or queued status never substitutes for actual human acceptance.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared operation-contract owner; host owner owns validation/application/receipts/UI
- **AnticipatedArtifacts:** CONFIG: proposal/basis/origin/outcome schemas;DOC: proposal lifecycle and shared validation route;TEST: stale, retarget, duplicate and unknown-outcome contract fixtures
- **CoversScopeItems:** SOW-070;SOW-090;SOW-091;SOW-170;SOW-171;SOW-172;SOW-173;SOW-174;SOW-175;SOW-176;SOW-177;SOW-178
- **SupportsObjectives:** OBJ-004;OBJ-005
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: agree the affected operation/receiving contract before its dependent implementation and joined witness.

## Package boundary

- **ScopeDescription:** Catalog, basis, validation, proposal and external-access semantics used by human, embedded and App external-agent consumers.
- **InclusionCriteria:** App/shared contract definitions, receiving adapters, contract fixtures and host integration guidance.
- **Exclusions:** SWB domain objects, validation, application, receipts, catalog implementation and UI remain with SWB; automatic extension remains unresolved.
