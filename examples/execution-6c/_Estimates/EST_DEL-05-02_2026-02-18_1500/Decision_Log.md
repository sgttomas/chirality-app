# Decision Log: EST_DEL-05-02_2026-02-18_1500

## Decisions Applied During This Run

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| D-001 | Use dual cost structure (production + construction content) | Required by BOE Section 3.2; DEL-05-02 has both production hours and embedded construction pricing | Two line groups in Detail.csv |
| D-002 | Schedule B construction content must reconcile exactly to Schedule A | Per Specification.md R-005 and decomposition acceptance criteria | All CBS totals forced to match DEL-05-01 summary |
| D-003 | CBS granularity: split Schedule A CIVIL into CIVIL + UG sub-codes in Schedule B | Schedule B provides more detail than Schedule A; underground utilities separated for cost tracking | CIVIL + UG combined = $1,580,000 matching Schedule A CIVIL total |
| D-004 | CBS granularity: separate COLDSTG from STRUCT | Cold storage building is a distinct scope element (PEMB vs institutional construction) | $290,000 tracked separately; still reconciles to Schedule A STRUCT + COLDSTG |
| D-005 | GR breakdown into 8 sub-lines | Schedule B provides cost structure transparency for the 15% GR allocation | $1,305,000 allocated across project management, supervision, temp facilities, mob/demob, misc, H&S, QC, cleanup |
| D-006 | Builder's risk + CGL insurance placed in FEES CBS (not GR) | Reconciles to Schedule A which carries all bonds/insurance in FEES | L-116 = $82k in FEES; GR L-014 reallocated to misc GR items |
| D-007 | Design fee markup adjustment line (L-108 = $405k) | Sum of discipline-specific fee percentages ($375k) is less than Schedule A design fee allocation ($780k = 9% of base). Adjustment represents DB firm overhead/profit/coordination premium. | Transparent reconciliation of fee calculation methods |
| D-008 | Underground utility contingency ($64.5k in L-078) | Sum of bottom-up utility line items ($276k) is less than Schedule A allocation ($350k). Difference allocated as contingency for unforeseen conditions. | Reconciliation allocation with documented rationale |
| D-009 | Equipment line items exclude GR overlap lines from totals | L-095 (temp facilities) and L-096 (temp power) are shown for transparency but flagged as non-additive (already in GR) | Prevents double-counting; documented in Notes column |
| D-010 | Production hours from Level_of_Effort.csv (44 hrs vs Schedule A 72 hrs) | Different production scope: Schedule B detail work (44 hrs) vs Schedule A compilation + pricing strategy (72 hrs) | Production costs differ between DEL-05-01 and DEL-05-02 as expected |
| D-011 | OI-004 FF&E resolved as $20,000 cash allowance (Additional Option 6) | Per BOE Section 4 recommendation and OPT-18 in Optional_Items_Pricing.csv | $20k carried at HIGH confidence |
| D-012 | Cold storage electrical sub-allocation in L-059 | Cold storage electrical ($36k per ES-12) allocated to ELEC CBS in L-059 for CBS traceability rather than buried in L-080 cold storage turnkey | Provides discipline-level cost visibility; L-080 captures remaining turnkey cost |
