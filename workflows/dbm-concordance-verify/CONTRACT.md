# dbm-concordance-verify contract

## Brief

This file defines the INIT-TASK dispatch contract for `TASK + dbm-concordance-verify`.

### Purpose

Use this workflow after deterministic package concordance and source-supersession checks have produced findings, but before dbm-publisher accepts package readiness.

### Scope model

- `ScopePath` should be the immutable package snapshot directory.
- `AllowedWriteTargets` must name exactly:
  - `Publication_Concordance_Verification.md`
  - `Publication_Concordance_Verification_Findings.csv`

The brief must not grant write access to section folders, planning artifacts, KTY folders, or source authority files.

### Required brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `PURPOSE` | string | Why verification is being run | `Verify semantic concordance before package readiness.` |
| `ScopePath` | path | Package snapshot directory | `/abs/root/_Publication/DBM/package/RUN-20260421-120000/` |
| `Workflow` | string | Must equal this workflow name | `dbm-concordance-verify` |
| `AllowedWriteTargets` | list[path] | Exact verification outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |
| `RuntimeOverrides.SECTIONS_ROOT` | path | Current section outputs root | `/.../_Publication/DBM/sections/` |
| `RuntimeOverrides.CONCORDANCE_REGISTER_PATH` | path | Frozen register | `/.../_Planning/Publication_Concordance_Register.csv` |
| `RuntimeOverrides.CONCORDANCE_FINDINGS_PATH` | path | Deterministic concordance findings | `/.../Publication_Concordance_Findings.csv` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_PATH` | path | Markdown verification output | `/.../Publication_Concordance_Verification.md` |
| `RuntimeOverrides.OUTPUT_VERIFICATION_FINDINGS_PATH` | path | CSV verification findings output | `/.../Publication_Concordance_Verification_Findings.csv` |
| `ExpectedOutputs` | list[path] | Same two verification outputs | `[/.../Publication_Concordance_Verification.md, /.../Publication_Concordance_Verification_Findings.csv]` |

### Optional brief fields

| Field | Type | Meaning | Example |
|---|---|---|---|
| `RuntimeOverrides.SOURCE_SUPERSESSION_FINDINGS_PATH` | path | Source-supersession findings when validation ran | `/.../Source_Supersession_Findings.csv` |
| `RuntimeOverrides.PUBLICATION_RULES_PATH` | path | Approved publication rules | `/.../_Planning/Publication_Rules.md` |
| `RuntimeOverrides.PUBLICATION_INPUT_MANIFEST` | path | Frozen manifest | `/.../_Planning/Publication_Input_Manifest.md` |
| `RuntimeOverrides.PACKAGE_SNAPSHOT_PATH` | path | Package snapshot root | `/.../_Publication/DBM/package/RUN-20260421-120000/` |
| `CustomInstructions` | string | Run-specific emphasis only | `Pay special attention to shared utility values.` |

### Runtime-override guidance

- `SECTIONS_ROOT` must contain complete current section bundles.
- The workflow reads synthesized section outputs only. It must not be asked to inspect raw KTY-local source files.
- `SOURCE_SUPERSESSION_FINDINGS_PATH` should be provided whenever `validate_source_supersession.py` ran.

### Example INIT-TASK brief

```md
PURPOSE: Verify semantic concordance before final DBM readiness.
ScopePath: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/
Workflow: dbm-concordance-verify
AllowedWriteTargets:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
RuntimeOverrides:
  SECTIONS_ROOT: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/sections/
  CONCORDANCE_REGISTER_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/_Planning/Publication_Concordance_Register.csv
  CONCORDANCE_FINDINGS_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Findings.csv
  OUTPUT_VERIFICATION_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  OUTPUT_VERIFICATION_FINDINGS_PATH: /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
ExpectedOutputs:
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification.md
  - /repo/domains/West_Doe_Deepcut_DBM/_Publication/DBM/package/RUN-20260421-120000/Publication_Concordance_Verification_Findings.csv
```

## Acceptance

### Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - `Publication_Concordance_Verification.md`
   - `Publication_Concordance_Verification_Findings.csv`
2. All writes stayed inside the package snapshot directory named in the brief.
3. Every register key receives a verdict in the markdown report.
4. Every blocking verdict appears in the findings CSV.
5. No section outputs, planning artifacts, KTY files, or register files were modified.

### Required verification findings schema

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

### Required report structure

`Publication_Concordance_Verification.md` must contain these H2 headings in order:

1. `## Verification Summary`
2. `## Per-Key Verdicts`
3. `## Deterministic Finding Interpretation`
4. `## Implicit Conflicts`
5. `## Register Gaps`
6. `## Human Rulings Required`

### Verdict requirements

- `SEMANTIC_MISMATCH`, `IMPLICIT_CONFLICT`, and `REGISTER_GAP` verdicts require explanation with section references.
- `OMITTED_REQUIRED_ASSERTION` verdicts must identify the section, assertion key, and whether the section emitted `OMITTED_WITH_RATIONALE`, `OMITTED_BLOCKING`, or no row.
- `NORMALIZATION_ARTIFACT` verdicts must state why the underlying engineering values agree.
- `NEEDS_HUMAN_RULING` verdicts must explain what information is missing or ambiguous.

### Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- the section root, register, or deterministic findings file is missing,
- output paths fall outside the package snapshot directory.

Use `FAILED` when:
- required outputs cannot be written despite valid inputs,
- the run cannot complete semantic verification for internal reasons.

## Tool use

### Preferred tool order

No deterministic tools are required. The verifier reads already-produced package and section artifacts and performs semantic reasoning.

### Allowed deterministic tools

#### Operationally invoked

None.

### Expected use of reasoning

Use semantic reasoning to compare section prose, assertion rows, deterministic findings, and source-supersession findings across the full package context.

### Disallowed use

- Do not invoke publication tools.
- Do not dispatch other agents or workflows.
- Do not read raw KTY-local source files.
- Do not rewrite section bodies, section QA, planning artifacts, or the concordance register.

### Write boundary

Writes are limited to:
- `Publication_Concordance_Verification.md`
- `Publication_Concordance_Verification_Findings.csv`

Both outputs must resolve under the current immutable package snapshot directory named in the brief.
