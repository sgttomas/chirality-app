# Context: DEL-06-02 Return, waiting and human-decision workspace

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-06
- **Package Name:** File-based fleet coordination
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-06-02
- **PackageID:** PKG-06
- **Name:** Return, waiting and human-decision workspace
- **Description:** Let the coordinator examine returns, understand waiting causes and decide from exact-act packages rebuilt from project files. Interfaces: Consumes DEL-06-01 work graph and PKG-04 actual-act records; native running-state observations remain distinct from returned/reviewed/integrated work; DEL-09-05 owns the joined fleet witness. Verification: Rebuilt views preserve ownership, pending review, alternatives/consequences and actual decisions while remaining derived from the files.
- **Type:** UX_UI_SLICE
- **ResponsibleParty:** App fleet-experience owner
- **AnticipatedArtifacts:** CODE: return-review queue and waiting-cause views;CODE: prepared decision-package view;TEST: cross-session rebuild and queue/decision fixtures;DOC: view derivation and ownership boundary
- **CoversScopeItems:** SOW-085;SOW-086;SOW-087;SOW-088;SOW-089
- **SupportsObjectives:** OBJ-006
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: App fleet work proceeds from its file/native contracts without PEC availability.

## Package boundary

- **ScopeDescription:** Bounded delegation and recoverable work-graph, return, waiting and decision views in the App.
- **InclusionCriteria:** Product coordination records and rebuildable views; clear native-delegation and human-decision interfaces.
- **Exclusions:** Project dependency DAG and project practice are PKG-10; PEC observes through PKG-07; further fleet scope remains TBD.
