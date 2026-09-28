# Context: DEL-02-01 Portable workflow contract and shared allocation

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-02
- **Package Name:** Workflow and role portability
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-02-01
- **PackageID:** PKG-02
- **Name:** Portable workflow contract and shared allocation
- **Description:** Define the portable workflow declaration and four-role receiving semantics, and allocate compatible shared types/components only where repeated consumer responsibilities justify them. Interfaces: PKG-03 owns catalog semantics and supplies required-tool capability descriptors; PKG-04 owns human-act/run record fields; PKG-05 receives host workflow/panel needs. Shared placement is decided per consumer with no presumed service. Verification: Declared inputs/tools/checkpoints/outputs/evidence remain readable, source-compatible and usable by App/host consumers; all shared responsibilities name their consuming owners and unresolved placement.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared workflow-contract owner; affected consumer owners confirm their receiving responsibilities
- **AnticipatedArtifacts:** DOC: portable workflow/role/checkpoint contract;CONFIG: open declared-part schemas and examples;DOC: shared contract/component responsibility map;TEST: parser and consumer contract fixtures
- **CoversScopeItems:** SOW-021;SOW-022;SOW-037;SOW-038;SOW-039;SOW-042;SOW-043;SOW-044;SOW-045;SOW-145;SOW-146;SOW-147
- **SupportsObjectives:** OBJ-003;OBJ-004;OBJ-005
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: portable contracts and App workflow behavior can proceed while host receiving inputs are coordinated.

## Package boundary

- **ScopeDescription:** The complete workflow-making workspace and portable workflow/role/checkpoint contracts across App and receiving hosts.
- **InclusionCriteria:** Create, review, register, select, reuse and refine workflows; source identity; additive role supply; accountable allocation of shared contract parts.
- **Exclusions:** Host catalog semantics are PKG-03; attributable act records are PKG-04; host-specific construction is external; shared meaning does not require a common service.
