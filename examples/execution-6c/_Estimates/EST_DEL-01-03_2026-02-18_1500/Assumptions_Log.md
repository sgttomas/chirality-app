# Assumptions Log: EST_DEL-01-03_2026-02-18_1500

| AssumptionID | Assumption | Source | Impact if Wrong |
|---|---|---|---|
| A-001 | Bond types required are standard Performance Bond (50% contract) and Labour & Materials Payment Bond (50% contract) per Alberta municipal DB practice | Industry standard; RFP Section 5.3.1 not yet extracted (DEP-01-03-005 PENDING) | If RFP requires different bond types/amounts (e.g., 100% performance bond), premiums could increase by up to 2x |
| A-002 | Contract value basis for bond/insurance percentage calculation is base construction excluding GST ($9,863,000) | EST_DEL-05-01_2026-02-18_1400; standard bonding practice | If bonding basis includes GST or options, premiums increase by 5-10% |
| A-003 | CCIP (Contractor Controlled Insurance Program) is the insurance delivery model, not OPIP (Owner Provided) | BOE Section 8 A-07; Fees_Permits_Insurance.csv FP-03 | If Owner provides insurance (OPIP), CCIP premium ($197,260) would not apply to contractor |
| A-004 | All professional hourly rates are internal DB firm rates (not external consultant fees) except R-25 Legal which is explicitly external | BOE Section 8 A-01; Professional_Staff_Rates.csv | External consultant rates may be higher for PM, admin roles |
| A-005 | Surety broker fee is a separate cost from bond premiums | Fees_Permits_Insurance.csv FP-19 notes "sometimes embedded in bond premium" | If embedded, $3,500 broker fee would be double-counted; remove L-030 if confirmed embedded |
| A-006 | Construction value from DEL-05-01 is PARAMETRIC and will change when actual pricing is completed | EST_DEL-05-01_2026-02-18_1400 Key Observations #6 | All percentage-based premiums ($537,534 total) will scale proportionally with final construction value |
| A-007 | Level of effort for bond/insurance documentation (10 hours total) assumes surety broker and insurance provider are cooperative and responsive | Level_of_Effort.csv DEL-01-03 rows; comparable proposal experience | If extended negotiation required, PM and legal hours could increase 2-3x |
