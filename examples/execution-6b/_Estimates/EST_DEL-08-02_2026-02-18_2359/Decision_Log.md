# Decision Log -- EST_DEL-08-02_2026-02-18_2359

| DecisionID | Decision | Rationale |
|---|---|---|
| EST-DEC-001 | CBS code CX assigned to Commissioning Lead (R-21) hours | R-21 is categorized as "Construction" in Professional_Staff_Rates.csv. For PKG-008 (Commissioning, Closeout & Warranty), the CBS code CX (Commissioning) is used as a more specific classification than the generic "Construction" category. Documented in Run_Context.md CBS Mapping Rule. |
| EST-DEC-002 | CBS code MGMT assigned to Project Manager (R-02) hours | R-02 is categorized as "Management" in Professional_Staff_Rates.csv. CBS code MGMT is directly derived from the role category. |
| EST-DEC-003 | No fallback pricing used | FALLBACK_POLICY=STRICT and all line items have complete hours (Level_of_Effort.csv) and rate (Professional_Staff_Rates.csv) evidence. No TBD amounts required. |
| EST-DEC-004 | Assumed_Project_Parameters.csv listed as a source but not directly used for pricing | This source provides contextual project parameters (durations, areas, quantities, financial estimates). None of these parameters directly drive the pricing of DEL-08-02. Included in Source_Index.md for completeness per the brief. |
| EST-DEC-005 | Scope limited to DEL-08-02 production cost only; not the cost of executing deficiency management during construction | The estimate covers the cost of producing the Deficiencies Management Narrative deliverable (a proposal document), not the cost of performing deficiency management activities during the construction phase. The latter would be captured in construction general requirements pricing. |
