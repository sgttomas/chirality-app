# Decision Log — EST_DEL-005-06_2026-02-27_0546

## DEC-001 — Pricing Method Selection

- **Decision:** Use PARAMETRIC method (estimated hours x hourly rates) as the primary pricing approach.
- **Basis:** `BASIS_OF_ESTIMATE = PARAMETRIC` was specified in the run brief. Level_of_Effort.csv provides deliverable-specific hour allocations for DEL-005-06 with 4 roles. Professional_Staff_Rates.csv provides CAD hourly rates for all 4 roles. Both sources have PARAMETRIC basis and MEDIUM confidence.
- **Alternatives considered:** Professional_Design_Fees.csv (DF-05) provides a fee-percentage alternative (civil design at 1.0% of construction value). This could not be computed because no construction value estimate is available for the civil works in isolation.

## DEC-002 — Scope Traceability Items (Zero-Cost Lines)

- **Decision:** Include 17 scope traceability items (ITM-005 through ITM-021) in Items.csv as LUMP_SUM with Qty=1, but do not create corresponding Detail.csv lines with standalone costs.
- **Basis:** These items represent specific calculation topics and design activities identified in the Datasheet (Construction table), Specification (requirements), and Procedure (steps). Their labour effort is fully embedded in the four role-based labour lines (ITM-001 through ITM-004). Including them ensures scope completeness is verifiable even though they carry no incremental cost.
- **Rationale:** The Level_of_Effort.csv provides aggregate role-level hours for the deliverable, not activity-level hours. Splitting the aggregate into per-activity costs would require assumptions not supported by the source data.

## DEC-003 — CBS Category Assignment

- **Decision:** Assign CBS categories as follows:
  - LABOUR-MGMT: Project Manager (R-01), Cost Estimator (R-08)
  - LABOUR-DESIGN: BIM Technician (R-13), Civil Engineer (R-17)
- **Basis:** Consistent with the role category designations in Professional_Staff_Rates.csv (R-01 = Management, R-08 = Management, R-13 = Design, R-17 = Design). This matches the convention used in prior snapshots (e.g., EST_DEL-005-01).

## DEC-004 — Confidence Level

- **Decision:** All Detail.csv lines assigned Confidence = MED.
- **Basis:** Both source files (Level_of_Effort.csv and Professional_Staff_Rates.csv) report MEDIUM confidence. The combined confidence cannot exceed the lower of the two input confidences.

## DEC-005 — No Fallback Required

- **Decision:** FALLBACK_POLICY (ALLOW_PARAMETRIC) was not invoked because all items were priced using the primary PARAMETRIC basis.
- **Basis:** Complete hour and rate data were available for all 4 roles assigned to DEL-005-06 in the price sources.
