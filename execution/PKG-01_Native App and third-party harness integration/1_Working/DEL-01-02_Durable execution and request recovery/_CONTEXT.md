# Context: DEL-01-02 Durable execution and request recovery

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-02
- **PackageID:** PKG-01
- **Name:** Durable execution and request recovery
- **Description:** Preserve ongoing work and requests across window loss, explicitly stop work, and recover actual Codex state and prior conversation access after reconnect/relaunch. Interfaces: Consumes DEL-01-01 supplier boundary; serves DEL-01-04 request/outcome UI; compact evidence is handed to PKG-04 without making a transcript copy authoritative. Verification: Close/reload/reconnect, denial, unknown request, interruption, restart and missing-acknowledgment cases preserve actual state and never infer approval from silence.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App execution/recovery owner
- **AnticipatedArtifacts:** CODE: main-process session and outstanding-request ownership;CODE: reconnect/relaunch and explicit stop handling;TEST: request settlement and observation-loss fixtures;DOC: unknown-outcome and reuse decisions
- **CoversScopeItems:** SOW-007;SOW-008;SOW-060;SOW-061;SOW-062;SOW-063;SOW-064;SOW-065;SOW-066;SOW-122;SOW-123;SOW-124;SOW-125
- **SupportsObjectives:** OBJ-001;OBJ-002;OBJ-005
- **ContextEnvelope:** L
- **ContextEnvelopeNotes:** A single execution lifecycle with coupled process/request/recovery state. Split from hosting setup and presentation, but keep its failure transitions together to verify surviving requests.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
