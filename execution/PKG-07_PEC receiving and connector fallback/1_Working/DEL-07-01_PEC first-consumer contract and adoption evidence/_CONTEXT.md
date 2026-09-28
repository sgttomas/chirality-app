# Context: DEL-07-01 PEC first-consumer contract and adoption evidence

Accepted basis: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; see `ACCEPTED_MANIFEST.csv` and `DECISION.md`. No production completion or external contribution is inferred.

## Identity and accepted fields

- **PackageID:** PKG-07
- **Package Name:** PEC receiving and connector fallback
- **Discipline:** SOFTWARE (accepted decomposition variant; no separate discipline column supplied)
- **DeliverableID:** DEL-07-01
- **PackageID:** PKG-07
- **Name:** PEC first-consumer contract and adoption evidence
- **Description:** Provide product PEC consumption within the qualified, released coverage deliberately adopted by the receiving application, with examined-through identity and claim limits visible. Contract preparation and development/fixture work can proceed before that product receiving envelope is available; neither establishes operational consumption or reliance. Interfaces: PKG-06 owns execution and source coordination files; provider owns extraction/response; DEL-07-02 supplies fallback; later Piping adoption is separately owned. Verification: Pin, source, coverage, freshness and limitations remain inspectable; presence never proves correctness or owns execution; OI-022 details are resolved before operational reliance.
- **Type:** API_CONTRACT
- **ResponsibleParty:** App PEC receiving owner; PEC provider owner supplies released qualification evidence
- **AnticipatedArtifacts:** DOC: first-consumer questions and receiving contract;CODE: App receiving adapter within adopted envelope;TEST: source-pin/claim/coverage/freshness fixtures;DOC: qualification/release/consumer-adoption evidence
- **CoversScopeItems:** SOW-028;SOW-029;SOW-030;SOW-031;SOW-244;SOW-248
- **SupportsObjectives:** OBJ-007
- **ContextEnvelope:** M
- **ContextEnvelopeNotes:** One bounded behavior or contract slice; named interfaces and focused checks constrain required context. File counts remain production-definition estimates, not model limits.
- **PhaseHint:** Nonbinding: define fallback now; adopt only the actual qualified and released PEC envelope when available.

## Package boundary

- **ScopeDescription:** Optional PEC consumption and the accountable receiving policy for connector limitations and source-file recovery.
- **InclusionCriteria:** App first-consumer contract, claim standing and qualified/adopted envelope; independently applicable fallback for optional feeds.
- **Exclusions:** No PEC provider construction or execution authority; Domains query/research semantics belong to PKG-08 and have no PEC prerequisite.
