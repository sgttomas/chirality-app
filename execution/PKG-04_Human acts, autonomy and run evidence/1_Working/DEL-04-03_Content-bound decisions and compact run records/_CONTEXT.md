# Context: DEL-04-03 Content-bound decisions and compact run records

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-04
- **Package Name:** Human acts, autonomy and run evidence
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-04-03
- **PackageID:** PKG-04
- **Name:** Content-bound decisions and compact run records
- **Description:** Keep workflow/decision/accepted records in project files and compact run records linking actual operations, models, autonomy, human acts and host receipts. Interfaces: PKG-02 definitions/checkpoints, PKG-03 basis/receipts and PKG-06 decisions consume this format; Codex session storage stays operational; host run recording adopts the shared format without copying receipts. Verification: Recorded acts bind content/scope/purpose, changed bound content lapses visibly and unobserved acts/outcomes remain unclaimed; DEL-09-11 tests later reconstruction.
- **Type:** DATA_MODEL_CHANGE
- **ResponsibleParty:** App/shared evidence-record owner; host owner supplies receipts and actual acts
- **AnticipatedArtifacts:** CONFIG: versioned human-act and run-file format;CODE: App record writer/reader and content-change lapse handling;TEST: identity, reference and lapse fixtures;DOC: record authority and host receipt links
- **CoversScopeItems:** SOW-092;SOW-093;SOW-094;SOW-095;SOW-096;SOW-143;SOW-186
- **SupportsObjectives:** OBJ-004;OBJ-005
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One record identity and lifecycle context with App reader/writer and contract fixtures; host receipt production and unrelated domain storage remain outside.
- **PhaseHint:** Nonbinding: settle affected policy/record details before dependent operation implementation or reliance.

## Package boundary

- **ScopeDescription:** Operation-policy distinctions, visible autonomy and content-bound human-act/run records.
- **InclusionCriteria:** App/shared policy and receiving behavior; file record identity and standing; links to host receipts; reserved-policy accounting.
- **Exclusions:** No professional certification; global reserved list and classifier policy remain TBD; host enforcement is externally owned.
