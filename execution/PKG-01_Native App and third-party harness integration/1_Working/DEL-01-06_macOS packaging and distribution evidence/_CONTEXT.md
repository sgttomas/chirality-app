# Context: DEL-01-06 macOS packaging and distribution evidence

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-01
- **Package Name:** Native App and third-party harness integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-01-06
- **PackageID:** PKG-01
- **Name:** macOS packaging and distribution evidence
- **Description:** Provide the scoped macOS package and its signing/entitlement evidence, with the written sign-in distribution response obtained at the public-release point of need. Interfaces: Packages the identified DEL-01-01 binary and App; PKG-09 uses the packaged candidate; external SWB packaging knowledge may be received but does not qualify this package. Verification: Packaged target starts with identified binaries and required entitlements; unresolved terms block public distribution only, not owner use or independent development.
- **Type:** CI_CD_CHANGE
- **ResponsibleParty:** App packaging owner; owner obtains supplier terms
- **AnticipatedArtifacts:** CONFIG: macOS Apple Silicon packaging/signing/notarisation;DOC: entitlement and binary identity record;TEST: package install/launch witness;DOC: written distribution-terms response before public release
- **CoversScopeItems:** SOW-098;SOW-117;SOW-134
- **SupportsObjectives:** OBJ-002
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define and build the App against its selected supplier inputs; external host/provider completion is not a start gate.

## Package boundary

- **ScopeDescription:** Native App shell and initial integration of the stock third-party Codex harness, including native interaction, recovery, OAuth/sign-in, API-key/local-provider access and macOS packaging. Chirality owns the receiving integration and maintenance; Codex owns its agent engine and credentials.
- **InclusionCriteria:** Behavior implemented through stock pinned Codex and the selected Tauri/React/Vite App; candidate-specific supplier and package qualification.
- **Exclusions:** Portable workflow semantics and registration are PKG-02; host construction is external; no second harness or generic event translation.
