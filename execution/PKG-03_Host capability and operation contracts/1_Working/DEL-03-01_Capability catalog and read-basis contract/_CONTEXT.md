# Context: DEL-03-01 Capability catalog and read-basis contract

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-03
- **Package Name:** Host capability and operation contracts
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-03-01
- **PackageID:** PKG-03
- **Name:** Capability catalog and read-basis contract
- **Description:** Define one catalog of meaningful reads/operations and their fields, availability and basis so App, human and embedded consumers share operation meaning. Interfaces: PKG-02 tool requirements consume this contract; DEL-03-02 consumes basis and operation identities; PKG-04 supplies adopted operation-policy classes; host owner supplies actual tables/diagnostics. Verification: Representative reads and unavailable operations agree in result, standing, reason and basis across contracts; generated versus hand-built surfaces are explicit. Automatic extension is not inferred.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared capability-contract owner; host owner owns catalog implementation
- **AnticipatedArtifacts:** CONFIG: catalog and read-basis schemas;DOC: generated-surface and adapter-responsibility map;TEST: availability/read-standing/basis contract fixtures
- **CoversScopeItems:** SOW-018;SOW-067;SOW-068;SOW-069;SOW-072;SOW-157;SOW-158;SOW-159;SOW-160;SOW-161;SOW-162;SOW-163;SOW-164;SOW-165;SOW-166;SOW-167;SOW-168;SOW-169
- **SupportsObjectives:** OBJ-004;OBJ-005
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** A schema and semantic fixture context, not implementation of every host operation. Its many atomic rows are fields/invariants of one coherent catalog result.
- **PhaseHint:** Nonbinding: agree the affected operation/receiving contract before its dependent implementation and joined witness.

## Package boundary

- **ScopeDescription:** Catalog, basis, validation, proposal and external-access semantics used by human, embedded and App external-agent consumers.
- **InclusionCriteria:** App/shared contract definitions, receiving adapters, contract fixtures and host integration guidance.
- **Exclusions:** SWB domain objects, validation, application, receipts, catalog implementation and UI remain with SWB; automatic extension remains unresolved.
