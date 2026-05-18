# Run Context — EST_DEL-011-02_2026-02-27_0848

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-02_2026-02-27_0848 |
| **AsOf** | 2026-02-27T08:48Z |
| **Scope** | DEL-011-02 |
| **ScopeResolvedSummary** | 1 deliverable: DEL-011-02 Steel Plate Floor Embedments (PKG-011 Building Structure & Envelope) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-011-02 |

## Warnings

- W-01: Many engineering parameters for DEL-011-02 are TBD pending issuance of upstream design deliverables (DEL-002-08, DEL-002-10, DEL-002-12). Plate dimensions, thicknesses, exact count, anchorage details, and design loads are not yet available. Quantities are estimated parametrically from Appendix B conceptual layout and Datasheet assumptions.
- W-02: SC-08 (Embedded steel plates supply+install) rate from Structural_Concrete_Rates.csv is ALLOWANCE basis with LOW confidence. Mixed method used under ALLOW_MIXED_METHODS=TRUE.
- W-03: Wash bay steel plate scope boundary with SOW-0027a / DEL-018-05 is unresolved (CON-011-02-03). Wash bay plates are included in this estimate per Appendix B / SOW-0024 scope.
