# Context: DEL-07-02 Connector limitation and source-file recovery paths

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-07
- **Package Name:** PEC receiving and connector fallback
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-07-02
- **PackageID:** PKG-07
- **Name:** Connector limitation and source-file recovery paths
- **Description:** Make optional connector limits visible and keep supported work moving through explicit source-file recovery without inferring readiness, permission or empty work from missing feeds. Interfaces: PEC and Domains use this receiving policy independently; PKG-08 owns Domains-specific query/admission behavior. PEC availability is never a prerequisite to Domains or App development. Verification: Absent/stale/partial/failing states produce the actual fallback route and responsible manager/human work; qualified PEC can be adopted later without forcing a new start gate.
- **Type:** BACKEND_FEATURE_SLICE
- **ResponsibleParty:** App connector-receiving owner; managers and human retain fallback coordination
- **AnticipatedArtifacts:** CODE: App limited/absent/failing connector receiving states;DOC: source-file reconstruction and responsibility route;TEST: independent connector availability/fallback fixtures
- **CoversScopeItems:** SOW-032;SOW-033;SOW-034;SOW-035;SOW-036;SOW-245;SOW-246
- **SupportsObjectives:** OBJ-007
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define fallback now; adopt only the actual qualified and released PEC envelope when available.

## Package boundary

- **ScopeDescription:** Optional PEC consumption and the accountable receiving policy for connector limitations and source-file recovery.
- **InclusionCriteria:** App first-consumer contract, claim standing and qualified/adopted envelope; independently applicable fallback for optional feeds.
- **Exclusions:** No PEC provider construction or execution authority; Domains query/research semantics belong to PKG-08 and have no PEC prerequisite.
