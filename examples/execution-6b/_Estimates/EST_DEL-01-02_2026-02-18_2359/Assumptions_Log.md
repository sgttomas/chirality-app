# Assumptions Log -- DEL-01-02

**RunID:** EST_DEL-01-02_2026-02-18_2359

---

| AssumptionID | Assumption | Basis | Impact if Wrong |
|---|---|---|---|
| ASM-0102-01 | Hourly rates from Professional_Staff_Rates.csv reflect achievable market rates for Alberta-based professional services in 2024 | MARKET basis with MEDIUM confidence as stated in source file | If actual rates differ, amounts scale linearly; DEL-01-02 total is small ($2,380) so rate variance has minimal project impact |
| ASM-0102-02 | Level of effort hours (16h R-22, 4h R-02) are sufficient for final PDF assembly of a ~15MB proposal document with ~38 deliverable inputs | PARAMETRIC basis in Level_of_Effort.csv; consistent with industry norms for proposal assembly of this scale | If assembly complexity exceeds estimate, additional hours would be needed; risk is low given the administrative nature of the work |
| ASM-0102-03 | All upstream deliverables will be delivered in a format ready for direct PDF assembly without significant rework | Implied by the production-only scope of DEL-01-02; consistent with Procedure.md prerequisites | If upstream deliverables require reformatting or rework, additional coordination hours may be needed beyond the 20h estimate |
| ASM-0102-04 | One revision cycle is included in the 16-hour Proposal Coordinator estimate | Standard proposal practice; LOE notes reference "submission QA" | Multiple revision cycles could increase hours; risk is bounded by the 6-week proposal preparation timeline |
