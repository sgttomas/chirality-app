# Context: DEL-01-03 Native plans, tools and delegation views

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-03
- **PackageID:** PKG-01
- **Name:** Native plans, tools and delegation views
- **Description:** Expose native planning, substantial tools and subagent activity while keeping the person directing professional-application work. Interfaces: Consumes DEL-01-01 native types and DEL-01-02 execution state; DEL-02-02 owns workflow-making integration; PKG-06 consumes native delegation identities. Verification: Representative native plan revisions, tool outcomes and descendants remain visible without a translated Chirality event vocabulary; selected-version identity is visible through the supplier boundary.
- **Type:** UX_UI_SLICE
- **ResponsibleParty:** App native-interaction owner
- **AnticipatedArtifacts:** CODE: native plan/revision and tool/delegation views;TEST: pinned-native-item presentation fixtures;DOC: native feature and optional-UI-reuse map
- **CoversScopeItems:** SOW-001;SOW-003;SOW-004;SOW-006;SOW-014;SOW-128;SOW-129
- **SupportsObjectives:** OBJ-001;OBJ-002
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
