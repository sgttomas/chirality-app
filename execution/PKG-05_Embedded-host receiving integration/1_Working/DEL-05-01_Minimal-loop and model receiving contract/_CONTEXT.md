# Context: DEL-05-01 Minimal-loop and model receiving contract

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. Read it as amended by the active scope-change snapshot named in `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-05
- **Package Name:** Embedded-host receiving integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-05-01
- **PackageID:** PKG-05
- **Name:** Minimal-loop and model receiving contract
- **Description:** Establish App/shared receiving and conformance requirements for the minimal Chat Completions loop on a local or cloud model the person chooses while coordinating host placement, parsing, persistence and panel assembly. Interfaces: PKG-03 provides catalog schemas; PKG-02 checkpoints/roles and PKG-04 records define shared meaning; host owner selects internals and enforces destination and key/credential boundaries; common-loop construction requires a separately agreed repeated responsibility. Verification: Contract cases reject malformed/truncated calls, preserve schema-before-domain validation, limit traffic to the selected model service and allowed destinations and avoid UI blocking; actual host evidence is received, never claimed from this contract alone.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared embedded-integration owner; external host owner implements loop/native layer
- **AnticipatedArtifacts:** DOC: loop messages/tools/events/checkpoints and native-network receiving contract;CONFIG: tool-call/model interface fixtures;TEST: malformed-call, destination and responsiveness conformance cases;DOC: owner allocation and open implementation choices
- **CoversScopeItems:** SOW-015;SOW-016;SOW-017;SOW-136;SOW-137;SOW-138;SOW-139;SOW-140;SOW-141;SOW-142;SOW-144
- **SupportsObjectives:** OBJ-004
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: prepare receiving requirements independently; join host conformance when identified external inputs arrive.

## Package boundary

- **ScopeDescription:** App/shared receiving and conformance responsibilities for the minimal host loop, on a local or cloud model the person chooses, and panel.
- **InclusionCriteria:** Network/model/tool/loop boundary requirements; panel interaction interfaces and owner-coordinated common-component decisions.
- **Exclusions:** No SWB loop or panel construction; no selected common loop implementation or service; no Pi dependency or host team coordination.
