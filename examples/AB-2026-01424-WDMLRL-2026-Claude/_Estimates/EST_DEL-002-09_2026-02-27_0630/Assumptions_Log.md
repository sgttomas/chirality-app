# Assumptions Log — EST_DEL-002-09_2026-02-27_0630

## Explicit Assumptions

### ASM-001 — Currency

**Assumption:** All amounts are in Canadian Dollars (CAD).

**Basis:** INIT-TASK brief specifies CURRENCY = CAD. Assumed_Project_Parameters.csv (PP-17) confirms CAD as project currency with MEDIUM confidence.

**Impact if wrong:** All amounts would need currency conversion. Low risk given Alberta project context.

### ASM-002 — Hourly Rate Validity

**Assumption:** The parametric hourly rates in Professional_Staff_Rates.csv are representative of 2026 Alberta market rates for the design-build delivery model.

**Basis:** Rates are marked PARAMETRIC with MEDIUM confidence in the source file. No firm quotes or salary surveys are referenced.

**Impact if wrong:** Total estimate could vary. Rate sensitivity: a +/-10% change in the Structural Engineer rate (dominant cost driver at 74.3% of total) would shift the total by approximately +/-$1,428.

### ASM-003 — Level of Effort Validity

**Assumption:** The estimated hours in Level_of_Effort.csv are representative of the effort required to produce the DEL-002-09 Stair Details drawing set for this project's scope and complexity.

**Basis:** Hours are marked PARAMETRIC in the source file. The 84-hour Structural Engineer allocation (approximately 2 weeks full-time equivalent) is consistent with producing a multi-sheet structural detail drawing set including stair plan, elevation, sections, base connection details, top connection details, handrail/guardrail details, material schedule, and general notes for a 35 ft rise industrial stair with multiple connection types.

**Impact if wrong:** Total estimate would scale proportionally. Effort is the primary cost driver (hours x rate). Factors that could increase effort: complex stair geometry (switchback), unusual geotechnical conditions requiring special anchoring, extensive guardrail scope, or multiple design iterations from County review.

### ASM-004 — No Overhead or Disbursements Included

**Assumption:** The estimate represents direct labour cost only. No overhead (office, insurance, IT), profit margin, or disbursements (printing, travel to Ferintosh site, software) are included.

**Basis:** No overhead or disbursement rates were provided in PRICE_SOURCES. The hourly rates may or may not include overhead depending on how they were derived (not specified in source).

**Impact if wrong:** If rates are bare labour cost, the true fully-loaded cost could be 1.5x to 2.5x higher (typical overhead multiples for professional engineering services in Alberta).

### ASM-005 — Single Design Iteration

**Assumption:** The LOE hours assume a single design iteration through the procedure steps (design, draft, review, issue). No rework cycles beyond the Step 5 County review process are assumed.

**Basis:** Implicit in the LOE model structure (one set of hours per deliverable). Procedure describes one internal QA cycle (Step 4) and one County review (Step 5).

**Impact if wrong:** Significant rework (e.g., material change from steel to concrete mid-design, major County comments, coordination conflicts with DEL-002-05) could increase effort by 25-50%.

### ASM-006 — Design Scope Limited to Drawing Set

**Assumption:** This estimate covers the drawing set production scope only, as defined in the Specification. Structural calculations (DEL-002-10), structural specification (DEL-002-12), mezzanine framing (DEL-002-05), and construction (PKG-011) are separately estimated.

**Basis:** Specification "Out of Scope" section explicitly excludes calculations, mezzanine framing, foundation design, and construction. Each is a separate deliverable with its own LOE allocation.

**Impact if wrong:** If scope boundaries shift (e.g., stair calculations folded into DEL-002-09), the effort and cost would increase.
