# Context: DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-05
- **PackageID:** PKG-01
- **Name:** Native OAuth/sign-in, API-key and local-provider access
- **Description:** Connect the App to Codex-native ChatGPT sign-in/OAuth, API-key and local-server access, keep the modes configured together, and choose per conversation through Codex-owned credentials and supported provider methods. Interfaces: Consumes selected protocol/pin from DEL-01-01; App UI exposes per-conversation choice; PKG-05 receives applicable local-server capability requirements without an extra App harness. Verification: Each mode starts the intended conversation while all remain configured; native sign-in is exercised through the selected Codex account flow; supported compliant servers can substitute; account-home and API-key details are decided before dependent implementation.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App account/provider integration owner
- **AnticipatedArtifacts:** CODE: Codex-native OAuth/sign-in receiving and account/provider selection;CONFIG: supported local provider settings;DOC: account-home/API-key protocol decisions;TEST: native sign-in, concurrent-mode and compliant-server substitution checks
- **CoversScopeItems:** SOW-009;SOW-010;SOW-011;SOW-012;SOW-132;SOW-133;SOW-149;SOW-150
- **SupportsObjectives:** OBJ-002;OBJ-004
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
