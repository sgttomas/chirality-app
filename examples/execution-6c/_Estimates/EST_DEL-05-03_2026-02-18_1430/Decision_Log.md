# Decision Log: EST_DEL-05-03_2026-02-18_1430

## Decisions Applied During This Run

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| RD-001 | BASIS_OF_ESTIMATE set to RATE_TABLE | BOE Section 4 PKG-02 table specifies RATE_TABLE for DEL-05-03. The brief provided a path to BASIS_OF_ESTIMATE.md (the strategy document), which was read and validated. The per-deliverable plan explicitly assigns RATE_TABLE to DEL-05-03. | All line items use RATE_TABLE method. |
| RD-002 | CBS mapping: R-02 (PM) -> MGMT; R-18 (Estimator Senior) -> FIN | Deterministic mapping from Professional_Staff_Rates.csv Category column: Management -> MGMT, Financial -> FIN. | CBS codes assigned consistently across all ESTIMATING runs. |
| RD-003 | No construction pricing content lines produced for DEL-05-03 | BOE Section 4 PKG-02 cost ownership rules: "Pricing narrative + assumptions writing belongs here. Construction pricing COMPILATION is in DEL-05-01/05-02." DEL-05-03 is pure narrative -- no dual cost nature. | Only 2 production cost lines in Detail.csv. |
| RD-004 | FALLBACK_POLICY STRICT applied; no fallback needed | All 2 line items priced from available PRICE_SOURCES. No missing evidence requiring fallback. | No ALLOWANCE or PARAMETRIC fallback lines. |
| RD-005 | Upstream DEL-05-01/05-02 estimates referenced for context but NOT as pricing sources | Per non-negotiable invariant "Avoid recursive ingestion" -- prior estimate snapshots are not used as pricing evidence. Upstream totals are cited in Run_Context.md and Summary.md for context only. | Provenance is clean; no circular references. |
