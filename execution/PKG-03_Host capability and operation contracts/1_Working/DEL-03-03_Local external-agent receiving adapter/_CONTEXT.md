# Context: DEL-03-03 Local external-agent receiving adapter

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-03
- **Package Name:** Host capability and operation contracts
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-03-03
- **PackageID:** PKG-03
- **Name:** Local external-agent receiving adapter
- **Description:** Enable App Codex to inspect and submit through a host catalog-derived local MCP or CLI boundary only when the person enables host access. Interfaces: Uses native Codex tools and DEL-03-01/02 contracts with PKG-04 policy; host endpoint/server construction remains external; DEL-09-09 joins the actual inspect-to-receipt witness. Verification: Disabled and unavailable access is explicit; enabled external requests preserve basis, validation, autonomy and reserved-act behavior without a second host mutation route.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App external-host integration owner; external host owner supplies MCP/CLI endpoint
- **AnticipatedArtifacts:** CODE: App-side native MCP/CLI configuration and receiving adapter as needed;DOC: machine-local enablement and operation-policy interface;TEST: external consumer contract fixtures
- **CoversScopeItems:** SOW-148;SOW-183;SOW-184
- **SupportsObjectives:** OBJ-004
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: agree the affected operation/receiving contract before its dependent implementation and joined witness.

## Package boundary

- **ScopeDescription:** Catalog, basis, validation, proposal and external-access semantics used by human, embedded and App external-agent consumers.
- **InclusionCriteria:** App/shared contract definitions, receiving adapters, contract fixtures and host integration guidance.
- **Exclusions:** SWB domain objects, validation, application, receipts, catalog implementation and UI remain with SWB; automatic extension remains unresolved.
