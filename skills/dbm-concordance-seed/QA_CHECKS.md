# QA CHECKS — dbm-concordance-seed

## Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - one scope-local typed candidate CSV,
   - one scope-local concordance seed QA markdown file.
2. All writes stayed inside the approved `_Publication/DBM/_Planning/` paths named in the brief.
3. The candidate CSV contains the required typed columns, including:
   - `AssertionDomain`
   - `DiscoverySource`
   - `SourceKTYIDs`
   - `SourceSectionIDs`
   - `NormalizationHint`
   - `NormalizationContract`
   - `Criticality`
   - `ComparisonParameter`
   - `SourceFidelityCritical`
   - `SourceExpectedValue`
4. Every emitted row is tied to at least one approved section in `SECTION_IDS` through `AuthoritySectionID`, `RequiredSectionIDs`, or `SourceSectionIDs`, unless `ResolutionStatus=OUT_OF_SCOPE`.
5. `AssertionKey` values are stable uppercase snake case and do not encode ad hoc section-local prose.
6. Unsupported or ambiguous candidates remain explicit as `NEEDS_REVIEW`, `DUPLICATE_CANDIDATE`, or `OUT_OF_SCOPE` rather than being silently normalized into false certainty.
7. New candidate additions are grounded in mapped source content and do not rely on non-authoritative roots such as `_MEMORY.md` or `_SEMANTIC.md`.
8. The QA artifact uses the required stable block structure in the required order.
9. Every emitted candidate with `ResolutionStatus=READY_FOR_FREEZE` has a non-empty `NormalizationContract`.
10. Every evidence atom with `SOURCE_AUTHORITY` that the skill deems concordance-relevant has `SourceFidelityCritical=YES` and a populated `SourceExpectedValue` in the emitted candidate.

## Required QA artifact structure

`*_CONCORDANCE_SEED_QA.md` must contain these H2 headings in this order:

1. `## Scope Summary`
2. `## Inputs Consumed`
3. `## Candidate Refinements`
4. `## New Candidate Additions`
5. `## Ambiguities Requiring Review`
6. `## Duplicate / Merge Notes`
7. `## Normalization Guidance`

Content expectations by block:
- `Inputs Consumed` records candidate input path, planning artifacts consulted, sections covered, and mapped source inputs materially used.
- `Candidate Refinements` records existing candidate rows that were materially completed or corrected.
- `New Candidate Additions` records genuinely added candidates and their engineering rationale.
- `Ambiguities Requiring Review` records unresolved authority ownership, semantic duplication, or normalization uncertainty.
- `Duplicate / Merge Notes` records rows that look semantically related but were not safely merged.
- `Normalization Guidance` records how later section workers should normalize comparison values consistently.

## Required candidate CSV schema

`{CANDIDATE_OUTPUT_PATH}` must contain at least these columns:
- `AssertionKey`
- `AssertionLabel`
- `AssertionDomain`
- `AssertionType`
- `CanonicalTerm`
- `Unit`
- `ComparisonRule`
- `ComparisonParameter`
- `AuthoritySectionID`
- `RequiredSectionIDs`
- `FacilityScope`
- `CurrentStateBasis`
- `DecisionRefs`
- `DiscoverySource`
- `SourceKTYIDs`
- `SourceSectionIDs`
- `NormalizationHint`
- `NormalizationContract`
- `Criticality`
- `CandidateValueExample`
- `SourceArtifact`
- `SourceRef`
- `SourceFidelityCritical`
- `SourceExpectedValue`
- `Notes`
- `ResolutionStatus`

Allowed `ResolutionStatus` values:
- `READY_FOR_FREEZE`
- `NEEDS_REVIEW`
- `DUPLICATE_CANDIDATE`
- `OUT_OF_SCOPE`

Additional checks:
- `Criticality` must be one of `HIGH`, `NORMAL`, or `LOW`.
- `DiscoverySource` must record whether the row came from structured data, prose extraction, open issues, decision log, scope change, or another approved source class.
- `ComparisonParameter` must be populated when `ComparisonRule` requires extra rule detail such as rounding precision.
- `SourceKTYIDs` and `SourceSectionIDs` must identify the mapped source/support footprint for the row.
- `NormalizationHint` must be present whenever a later section worker could normalize the same value in multiple valid ways.
- `NormalizationContract` must be present for `READY_FOR_FREEZE` rows.
- `SourceFidelityCritical=YES` rows must include `SourceExpectedValue` or remain `NEEDS_REVIEW`.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- output paths fall outside `_Publication/DBM/_Planning/`,
- `SECTION_IDS` do not match the approved section map,
- the mapped input set exceeds `MAX_KA_FILES_TOTAL`,
- required planning artifacts or candidate input files are missing.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on successful runs, QA must surface:
- unresolved authority-section ownership,
- unresolved duplicate candidates,
- ambiguous normalization behavior,
- material open-issue / decision-log / SCA dependencies,
- any candidates deliberately left `OUT_OF_SCOPE`.
