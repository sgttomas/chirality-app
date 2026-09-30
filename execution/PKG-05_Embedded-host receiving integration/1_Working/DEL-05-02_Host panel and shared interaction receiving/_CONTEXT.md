# Context: DEL-05-02 Host panel and shared interaction receiving

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. Read it as amended by the active scope-change snapshot named in `projects/chirality-app-v4/execution/_ScopeChange/_LATEST.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-05
- **Package Name:** Embedded-host receiving integration
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-05-02
- **PackageID:** PKG-05
- **Name:** Host panel and shared interaction receiving
- **Description:** Provide the App/shared receiving contribution and host-panel requirements so agent work remains visible in host-owned tables and views. Interfaces: Uses PKG-02 workflows, PKG-03 proposals, PKG-04 standing and DEL-05-01 loop events; host-specific panel assembly and domain table construction remain external. Verification: Required conversation/workflow/proposal/check interactions point to actual host objects and results; no agent-private result surface or unagreed shared implementation is introduced.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App/shared panel receiving owner; external host owner implements host panel/tables/views
- **AnticipatedArtifacts:** DOC: conversation/workflow/proposal/check panel interface;DOC: justified reusable-component allocation;TEST: panel-to-host-table receiving cases;CODE: selected reusable components only after responsibility agreement
- **CoversScopeItems:** SOW-019;SOW-020
- **SupportsObjectives:** OBJ-004
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: prepare receiving requirements independently; join host conformance when identified external inputs arrive.

## Package boundary

- **ScopeDescription:** App/shared receiving and conformance responsibilities for the minimal host loop, on a local or cloud model the person chooses, and panel.
- **InclusionCriteria:** Network/model/tool/loop boundary requirements; panel interaction interfaces and owner-coordinated common-component decisions.
- **Exclusions:** No SWB loop or panel construction; no selected common loop implementation or service; no Pi dependency or host team coordination.
