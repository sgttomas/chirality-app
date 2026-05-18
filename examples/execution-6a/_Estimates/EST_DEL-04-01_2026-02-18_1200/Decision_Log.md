# Decision Log — EST_DEL-04-01_2026-02-18_1200

## Decisions Made During This Run

| DecisionID | Category | Decision | Rationale | Impact |
|---|---|---|---|---|
| DEC-RUN-001 | Scope boundary | DEL-04-01 estimate covers building shell only (framing, cladding, roof, gutters/downspouts, anchor bolts, erection). Doors, foundation/floor, electrical/ventilation, site work excluded. | Cost Ownership Rules provided in the INIT-TASK brief explicitly assign these items to other deliverables (DEL-04-02, DEL-04-03, DEL-04-04, PKG-003). | Shell-only pricing uses PB-01 (not PB-02 turnkey) as the parametric model. |
| DEC-RUN-002 | Parametric model selection | PB-01 selected as primary parametric model over PB-02. | PB-01 description matches the DEL-04-01 scope boundary exactly: "shell only — includes framing; roof; wall cladding; gutters/downspouts; anchor bolts; erection; does NOT include: foundation; floor; doors; electrical; ventilation." PB-02 includes items outside DEL-04-01. | Unit rate = $32/sf (recommended) from PB-01. |
| DEC-RUN-003 | Rate selection | Used PB-01 RecommendedRate ($32/sf) rather than range endpoints. | RecommendedRate represents the source's best single-point estimate within the $28-35/sf range. MEDIUM confidence is appropriate for parametric estimating at this project stage. | Amount = 6,000 sf x $32/sf = $192,000. |
| DEC-RUN-004 | Fallback to ALLOWANCE | Design engineering line (L-0401-02) priced as ALLOWANCE ($10,000) because no explicit design fee source exists in PRICE_SOURCES. | FALLBACK_POLICY = ALLOW_ALLOWANCE permits this. Design effort for a simple PEMB configuration is modest. ~5% of construction cost is a reasonable engineering allowance for a straightforward building. | Mixed methods: PARAMETRIC (primary) + ALLOWANCE (fallback). ALLOW_MIXED_METHODS = TRUE. |
| DEC-RUN-005 | Rounding | All amounts rounded to nearest dollar per ROUNDING = DOLLAR. | Brief specifies DOLLAR rounding. | No rounding impact (all computed amounts are whole dollars). |
| DEC-RUN-006 | CBS assignment | CBS codes assigned as 04.01.SHELL and 04.01.DESIGN based on deliverable scope and line item nature. | No CBSHint was present in the decomposition for DEL-04-01. Deterministic mapping rule: {PackageNumber}.{DeliverableNumber}.{ItemCategory}. Documented in Run_Context.md. | CBS is deterministic and traceable. |
