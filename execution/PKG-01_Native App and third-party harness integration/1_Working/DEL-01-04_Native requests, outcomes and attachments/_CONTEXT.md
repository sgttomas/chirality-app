# Context: DEL-01-04 Native requests, outcomes and attachments

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-04
- **PackageID:** PKG-01
- **Name:** Native requests, outcomes and attachments
- **Description:** Provide the native request, response, turn/outcome and attachment interactions required by the App and expose the workflow workspace receiving interface. Interfaces: DEL-01-02 owns outstanding requests and truthful outcomes; DEL-02-02 owns reviewed drafts/registration; PKG-04 supplies act distinctions. Old UI reuse remains optional. Verification: Grant, deny, answer, explicit decline and unknown outcomes are presented correctly; attachments and workflow-draft transitions preserve actual supplied content identity.
- **Type:** UX_UI_SLICE
- **ResponsibleParty:** App native-interaction owner
- **AnticipatedArtifacts:** CODE: native approval/question cards and response interactions;CODE: turn/outcome and attachment presentation;TEST: request and attachment interaction fixtures;DOC: receiving contract for workflow draft UI
- **CoversScopeItems:** SOW-005;SOW-014;SOW-129
- **SupportsObjectives:** OBJ-001;OBJ-002
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
