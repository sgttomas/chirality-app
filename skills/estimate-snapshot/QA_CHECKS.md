# estimate-snapshot — QA Checks

Minimum checks for a valid run.

## Step 0 fail-fast

1. `BASIS_OF_ESTIMATE` is present in `RuntimeOverrides` and passes `python3 tools/validation/validate_enum.py BASIS_OF_ESTIMATE {value}`. Any failure → `RUN_STATUS=FAILED_INPUTS` and halt before writing any snapshot artifacts.
2. `CURRENCY` is present.
3. `ESTIMATES_ROOT` resolves to an existing directory.

## S1 — Write quarantine respected

- No files outside `{ESTIMATES_ROOT}` were modified.
- Deliverable content, `_STATUS.md`, decomposition outputs, and dependency registers are untouched.

## S2 — Snapshot created

- A new snapshot folder `EST_{OUTPUT_LABEL}_{YYYY-MM-DD}_{HHMM}/` exists under `{ESTIMATES_ROOT}`, even if the run ended `FAILED_INPUTS` or blocked.
- No existing snapshot folder was overwritten.

## S3 — BASIS_OF_ESTIMATE validated

- `BASIS_OF_ESTIMATE` is one of: `QUOTE`, `RATE_TABLE`, `HISTORICAL`, `PARAMETRIC`, `ALLOWANCE`.
- Invalid or missing → `RUN_STATUS=FAILED_INPUTS`.

## S4 — Required artifacts exist

All of the following must exist in the snapshot folder:

- `Run_Context.md`
- `Summary.md`
- `QA_Report.md`
- `Source_Index.md`
- `Decision_Log.md`
- `Assumptions_Log.md`
- `WBS_CBS_Matrix.csv`

## S5 — Detail.csv schema integrity (when Detail.csv exists)

`Detail.csv` is parseable and contains all mandatory columns:

`LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes`

Enum checks:

- `Method` ∈ `{QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC}`
- `Confidence` ∈ `{LOW, MEDIUM, HIGH}` (canonical per `tools/validation/validate_enum.py`)
- `Currency` matches the brief's `CURRENCY`

Allowance/parametric convention:

- When `Method ∈ {ALLOWANCE, PARAMETRIC}`: `Qty=1`, `Unit=LS`, `UnitRate=Amount`.

## S6 — Provenance discipline

- Every priced row has a best-effort `SourceRef` (file + section/row ID, OR reference to a row in `Decision_Log.md`/`Assumptions_Log.md`) OR explicitly `location TBD`.
- `QA_Report.md` reports provenance completeness as a percentage and lists top missing-source offenders.
- No row carries an invented source or a source that is not actually in `PRICE_SOURCES`.

## Confidence rules (invariant)

| Confidence | When to assign |
|---|---|
| `HIGH` | Human-confirmed values; vendor-quoted values (`Method=QUOTE`) |
| `MEDIUM` | Published rate-table derivations with stable references; normalized historical data; approved parametric model outputs |
| `LOW` | Allowance-table values; sparse historical analogs; parametric outputs with weak parameter grounding |

- Never assign `HIGH` to allowance or parametric-derived amounts.
- `HIGH` on a `QUOTE`-method row requires an attached `SourceRef` to the vendor quote.
- Confidence assignments must be consistent with the row's `Method` value.

## S7 — Status reporting

`QA_Report.md` MUST declare one `RUN_STATUS`:

| Status | When |
|---|---|
| `OK` | Totals are meaningful; no critical input gaps |
| `WARNINGS` | Some totals exist but material `TBD`s or assumptions remain |
| `FAILED_INPUTS` | Basis inputs or pricing sources insufficient for meaningful totals |

## S8 — Operator acceptance (lightweight)

A snapshot is "good enough to publish" when:

- `RUN_STATUS ∈ {OK, WARNINGS}` with clearly bounded gaps.
- Basis-consistency checks pass, or deviations are explicitly approved and logged in `Decision_Log.md`.
- Provenance completeness is reported and top gaps are actionable.
- Scope coverage is explicit (included / excluded / blocked counts and reasons).
- No writes occurred outside `{ESTIMATES_ROOT}`.

## Basis-consistency check

- If `ALLOW_MIXED_METHODS=FALSE`: every Detail.csv row's `Method` should equal `BASIS_OF_ESTIMATE`, except where `FALLBACK_POLICY` explicitly permits a deviation and the deviation is logged in `Decision_Log.md`.
- If `ALLOW_MIXED_METHODS=TRUE`: mixed methods are allowed, but `QA_Report.md` must include the method mix histogram.

## Blocker reporting

When dependency evidence is loaded:

- Deliverables whose estimates are blocked by missing input information are listed in `Blockers.md` or `blocker_report.csv`.
- Each blocker cites the dependency row that raised it (from the deliverable's `Dependencies.csv` or an explicit dependency source).
- `EstimateImpactClass` (when present in dependency rows) is passed through as a hint; never invented.

## Failure reporting

- Missing `PRICE_SOURCES` or empty basis evidence → produce `TBD` amounts and declare `RUN_STATUS=WARNINGS` or `FAILED_INPUTS` per SPEC.
- Missing decomposition → `[WARNING] MISSING_DECOMPOSITION` logged in `QA_Report.md` and `Run_Context.md`; run proceeds with degraded ID/path validation.
- Invalid `BASIS_OF_ESTIMATE` → `RUN_STATUS=FAILED_INPUTS`; no pricing attempted.
- Attempt to overwrite an existing snapshot folder → halt; report as a tooling failure.

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Snapshot folder path
- Counts: in-scope deliverables, priced rows, blocked deliverables
- Provenance completeness percentage
- Method mix histogram (even when single-method)
- List of `PRICE_SOURCES` that were actually consumed
- No writes outside `{ESTIMATES_ROOT}`
