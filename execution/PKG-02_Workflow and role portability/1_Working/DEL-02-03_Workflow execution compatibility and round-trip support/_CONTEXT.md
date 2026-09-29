# Context: DEL-02-03 Workflow execution compatibility and round-trip support

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-02
- **Package Name:** Workflow and role portability
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-02-03
- **PackageID:** PKG-02
- **Name:** Workflow execution compatibility and round-trip support
- **Description:** Make selected workflow requirements actionable and preserve identity and actual human checkpoints while carrying workflows between App and hosts. Interfaces: PKG-03 catalog describes available tools; PKG-04 records real content-bound acts; PKG-05 supplies host receiving boundary; DEL-09-06 owns the joined host round-trip witness and external contribution record. Verification: Missing capabilities are explicit; checkpoint acts are requested and recorded only when performed, regardless of direct autonomy (holds are governance phase); source revisions survive transfer/adaptation and no human act is fabricated.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App/shared workflow-execution owner; external host owner supplies host execution
- **AnticipatedArtifacts:** CODE: required-tool and checkpoint receiving behavior;DOC: App/host workflow transfer and adaptation contract;TEST: missing-tool, checkpoint recording (governance-phase hold retained) and source-preserving round-trip fixtures
- **CoversScopeItems:** SOW-051;SOW-052;SOW-053;SOW-054;SOW-055
- **SupportsObjectives:** OBJ-003;OBJ-005
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: portable contracts and App workflow behavior can proceed while host receiving inputs are coordinated.

## Package boundary

- **ScopeDescription:** The complete workflow-making workspace and portable workflow/role/checkpoint contracts across App and receiving hosts.
- **InclusionCriteria:** Create, review, register, select, reuse and refine workflows; source identity; additive role supply; accountable allocation of shared contract parts.
- **Exclusions:** Host catalog semantics are PKG-03; attributable act records are PKG-04; host-specific construction is external; shared meaning does not require a common service.
