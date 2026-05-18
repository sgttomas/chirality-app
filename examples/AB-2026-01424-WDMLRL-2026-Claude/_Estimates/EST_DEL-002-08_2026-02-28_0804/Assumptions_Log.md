# Assumptions Log — EST_DEL-002-08_2026-02-28_0804

**RunID:** EST_DEL-002-08_2026-02-28_0804
**AsOf:** 2026-02-28T08:04:00-07:00

---

## ASM-001 — Independent Peer Review Scope (8 Hours)

| Field | Value |
|---|---|
| **Assumption ID** | ASM-001 |
| **Date** | 2026-02-28 |
| **Affected Line** | LN-006 (ITM-006) |
| **Category** | Scope / Level of Effort |
| **Assumption** | Independent peer review of the Steel Plate Embedment Plan IFC drawings requires 8 hours of Structural Engineer (R-14) effort. |
| **Basis** | Procedure enrichment D-003 identifies independent peer review as best practice for P.Eng.-stamped deliverables. The 8-hour allocation is a professional judgment estimate for a single-deliverable peer review covering load calculations, anchor design, plate locations, and drawing quality checks. |
| **Impact if Wrong** | If actual peer review requires more than 8 hours (e.g., due to design complexity or review iterations), the estimate would understate the cost. At $170/hr, each additional hour adds $170 CAD. Conversely, if fewer hours are needed, the estimate would overstate. |
| **Linked Decision** | DEC-R01 |
| **Confidence** | LOW |

---

## ASM-002 — Coordination Review Effort Embedded in Engineering Hours

| Field | Value |
|---|---|
| **Assumption ID** | ASM-002 |
| **Date** | 2026-02-28 |
| **Affected Line** | LN-005 (ITM-005) |
| **Category** | Scope / Level of Effort |
| **Assumption** | Inter-discipline coordination review effort (architectural, plumbing, mechanical) is fully captured within the 84 Structural Engineer hours in LN-004 and does not require a separate cost allocation. |
| **Basis** | Procedure Step 7 identifies coordination review as part of the engineering workflow. The Structural Engineer's 84-hour allocation includes time for coordination inputs (Step 1) and issue-for-review cycles (Step 7). LN-005 is carried at $0.00 as a scope marker. |
| **Impact if Wrong** | If coordination review requires effort beyond what is embedded in the Structural Engineer's hours (e.g., extended multi-discipline workshops), additional cost would need to be allocated. |
| **Linked Decision** | N/A |
| **Confidence** | LOW |

---

## ASM-003 — PARAMETRIC Pricing Adequacy

| Field | Value |
|---|---|
| **Assumption ID** | ASM-003 |
| **Date** | 2026-02-28 |
| **Affected Line** | All (LN-001 through LN-006) |
| **Category** | Pricing Method |
| **Assumption** | The PARAMETRIC method using Professional_Staff_Rates.csv (rates) and Level_of_Effort.csv (hours) provides adequate pricing accuracy for all line items in DEL-002-08. |
| **Basis** | All rate and hours sources are classified as MEDIUM confidence. Rates are drawn from a 25-role staff rate table; hours are drawn from a deliverable-specific hours allocation model. Both sources are internally consistent and project-specific. |
| **Impact if Wrong** | If actual staff rates differ from the rate table or if the hours model under/over-estimates effort, the total estimate would deviate. The current total is $20,590.00 CAD. |
| **Linked Decision** | N/A |
| **Confidence** | MED |

---

## Summary

| Assumption ID | Line(s) | Description | Confidence |
|---|---|---|---|
| ASM-001 | LN-006 | 8 hours for independent peer review scope | LOW |
| ASM-002 | LN-005 | Coordination review effort embedded in LN-004 engineering hours | LOW |
| ASM-003 | All | PARAMETRIC pricing method adequate for all line items | MED |
