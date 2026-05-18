# QA CHECKS - dbm-concordance-verify

## Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - `Publication_Concordance_Verification.md`
   - `Publication_Concordance_Verification_Findings.csv`
2. All writes stayed inside the package snapshot directory named in the brief.
3. Every register key receives a verdict in the markdown report.
4. Every blocking verdict appears in the findings CSV.
5. No section outputs, planning artifacts, KTY files, or register files were modified.

## Required verification findings schema

`Publication_Concordance_Verification_Findings.csv` must contain at least:
- `AssertionKey`
- `Verdict`
- `Blocking`
- `ImpactedSections`
- `DeterministicFindingRefs`
- `SourceSupersessionRefs`
- `EvidenceRefs`
- `Explanation`
- `RecommendedAction`

Allowed `Verdict` values:
- `CONFIRMED`
- `NORMALIZATION_ARTIFACT`
- `SEMANTIC_MISMATCH`
- `IMPLICIT_CONFLICT`
- `OMITTED_REQUIRED_ASSERTION`
- `REGISTER_GAP`
- `NEEDS_HUMAN_RULING`

## Required report structure

`Publication_Concordance_Verification.md` must contain these H2 headings in order:

1. `## Verification Summary`
2. `## Per-Key Verdicts`
3. `## Deterministic Finding Interpretation`
4. `## Implicit Conflicts`
5. `## Register Gaps`
6. `## Human Rulings Required`

## Verdict requirements

- `SEMANTIC_MISMATCH`, `IMPLICIT_CONFLICT`, and `REGISTER_GAP` verdicts require explanation with section references.
- `OMITTED_REQUIRED_ASSERTION` verdicts must identify the section, assertion key, and whether the section emitted `OMITTED_WITH_RATIONALE`, `OMITTED_BLOCKING`, or no row.
- `NORMALIZATION_ARTIFACT` verdicts must state why the underlying engineering values agree.
- `NEEDS_HUMAN_RULING` verdicts must explain what information is missing or ambiguous.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- the section root, register, or deterministic findings file is missing,
- output paths fall outside the package snapshot directory.

Use `FAILED` when:
- required outputs cannot be written despite valid inputs,
- the run cannot complete semantic verification for internal reasons.
