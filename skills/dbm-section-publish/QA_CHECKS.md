# QA CHECKS — dbm-section-publish

## Minimum output validity checks

The run is valid only when all of the following are true:

1. All three required outputs exist:
   - section body markdown,
   - section QA markdown,
   - section assertions CSV.
2. The section body reads as coherent engineering prose under `Publication_Rules.md` rather than as a concatenated artifact dump.
3. The section body reflects current post-SCA state when mapped sources require a state choice.
4. Unsupported claims are surfaced as `TBD`, assumptions, or conflicts rather than silently guessed.
5. The section body does not use detailed inline source citations; detailed provenance belongs in QA and the package trace appendix.
6. The section QA artifact uses the required stable block structure in the required order.
7. The section assertions CSV contains the required columns and valid `AssertionStatus` values.
8. All writes stayed inside the approved section-local publication folder.

## Required QA artifact structure

`SEC-##_QA.md` must contain these H2 headings in this order:

1. `## Section Summary`
2. `## Coverage Table`
3. `## Readiness Observations`
4. `## Conflict Register`
5. `## Terminology Notes`
6. `## Gap / TBD Register`
7. `## Amendment Notes`
8. `## Assertion Emission Notes`

Content expectations by block:
- `Coverage Table` records mapped KTYs/KAs consumed plus mapped inputs skipped and why.
- `Readiness Observations` records KTY readiness issues.
- `Conflict Register` records contradictory values/states and both source positions.
- `Gap / TBD Register` preserves distinctions such as `TBD`, `ASSUMPTION`, and `DEFERRED_CONFIRMATION`.
- `Assertion Emission Notes` records required assertions emitted or explicitly marked non-applicable.

## Required assertions CSV schema

`SEC-##_ASSERTIONS.csv` must contain at least these columns:
- `SectionID`
- `AssertionKey`
- `AssertionStatus`
- `DisplayValue`
- `NormalizedValue`
- `Units`
- `SourceArtifact`
- `SourceRef`
- `SCARefs`
- `DecisionRefs`
- `Notes`

Allowed `AssertionStatus` values:
- `ASSERTED`
- `REFERRED`
- `NOT_APPLICABLE`
- `CONFLICT_UNRESOLVED`

Additional checks:
- Every row must use the current `SECTION_ID`.
- If the section is an authority or required participant for an approved assertion key, the CSV must contain one row for that key.
- `NormalizedValue` should be fit for deterministic comparison under the approved concordance rule.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- mapped `PRIMARY` or `CONFLICTING` inputs are below readiness threshold,
- the section input set exceeds `MAX_KA_FILES` or the approved size limit,
- output paths fall outside the approved section-local publication folder.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on non-blocking runs, QA must surface:
- skipped supporting inputs,
- terminology normalizations,
- remaining conflicts,
- remaining `TBD` / assumption / deferred-confirmation items,
- any reliance on amendment notes or decision-log references.
