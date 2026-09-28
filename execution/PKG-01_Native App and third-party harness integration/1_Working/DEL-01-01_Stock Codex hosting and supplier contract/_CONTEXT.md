# Context: DEL-01-01 Stock Codex hosting and supplier contract

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-01
- **PackageID:** PKG-01
- **Name:** Stock Codex hosting and supplier contract
- **Description:** Provide the pinned stock Codex App Server host under the chosen App stack and define its process and protocol ownership; qualify the selected embedding protocol and identify provider-protocol requirements. Interfaces: Native views and recovery consume generated protocol types; PKG-02 supplies guidance/workflow inputs; provider access consumes the chosen protocol. SOW-128 plan behavior is jointly delivered with DEL-01-03. Verification: Stock binary identity, generated fields, unknown-request path and selected-version checks pass on the candidate; any reuse is assessed against this receiving contract.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App supplier-integration owner
- **AnticipatedArtifacts:** CODE: App-owned child/protocol boundary;CONFIG: selected supplier pin and generated protocol types;DOC: Rust/TypeScript responsibility and optional-reuse decision;TEST: recorded protocol and upgrade qualification fixtures
- **CoversScopeItems:** SOW-097;SOW-099;SOW-100;SOW-101;SOW-118;SOW-119;SOW-121;SOW-128;SOW-131;SOW-135;SOW-149
- **SupportsObjectives:** OBJ-001;OBJ-002;OBJ-004
- **ContextEnvelope:** L
- **ContextEnvelopeNotes:** One supplier-hosting context with process, schema and pin qualification. Kept together because generated types and process ownership determine the seam; UI, durable recovery, account flows and packaging are split into separate deliverables.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
