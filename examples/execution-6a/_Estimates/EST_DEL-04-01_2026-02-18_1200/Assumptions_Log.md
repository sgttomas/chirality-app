# Assumptions Log — EST_DEL-04-01_2026-02-18_1200

## Assumptions

| AssumptionID | Category | Assumption | Basis | Confidence | Impact if Wrong |
|---|---|---|---|---|---|
| ASM-001 | Area | Cold storage building area is 6,000 sf (60' x 100'). | DEC-001 (decomposition decision); PP-07 (Assumed_Project_Parameters.csv, CONFIRMED, HIGH confidence); SOW-0301. | HIGH | Direct multiplier on shell cost. If area changes, rerun with updated area. |
| ASM-002 | Rate | PB-01 RecommendedRate of $32/sf is an appropriate parametric rate for a pre-engineered metal building shell in Alberta (2024 pricing basis). | Parametric_Building_Rates.csv PB-01; range $28-35/sf; MEDIUM confidence per source. | MED | At range endpoints: low = $168,000, high = $210,000. Variance band is +/- $24,000 from recommended ($192,000). |
| ASM-003 | Design fee | Design and engineering services for the cold storage shell configuration are estimated at $10,000 (approximately 5% of shell construction cost). | No explicit design fee source in PRICE_SOURCES. Estimated by analogy: PEMB design for a simple clear-span building is a modest engineering effort (selection of manufacturer system, load verification, coordination drawings). 5% is within typical range for simple structures. | LOW | If design fee is higher (e.g., 8-10% for more complex coordination), impact is +$5,000 to +$10,000. |
| ASM-004 | Scope | The PB-01 parametric rate includes all components listed in its description: framing, roof, wall cladding, gutters/downspouts, anchor bolts, and erection. No additional line items are needed for these components. | PB-01 Notes field: "Includes: framing; roof; wall cladding; gutters/downspouts; anchor bolts; erection." | MED | If PB-01 excludes a component that should be in DEL-04-01 scope (e.g., specialized flashing or snow guards), those items would need to be added as separate line items. |
| ASM-005 | Market | Parametric rates from PRICE_SOURCES are representative of current Alberta construction market conditions (2024 basis). | Source files carry "Alberta 2024" in descriptions. | MED | Market escalation or regional supply constraints could shift actual costs. No escalation factor applied. |
