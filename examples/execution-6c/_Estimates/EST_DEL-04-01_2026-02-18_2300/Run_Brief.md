# Run Brief (verbatim)

```
SCOPE: DEL-04-01
RUN_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-06_Construction Methodology + Administration/1_Working/DEL-04-01_ConstructionMethodologyNarrative
ESTIMATES_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/
BASIS_OF_ESTIMATE: RATE_TABLE
CURRENCY: CAD
DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
DEPENDENCY_SOURCES: AUTO
PRICE_SOURCES:
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv"
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv"
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv"
OUTPUT_LABEL: DEL-04-01
UPDATE_LATEST_POINTER: FALSE
FALLBACK_POLICY: STRICT
ALLOW_MIXED_METHODS: FALSE
ROUNDING: DOLLAR
EXCLUSIONS:
  - "_Estimates/**"
  - "_Aggregation/**"
  - "_Reconciliation/**"
  - "_Archive/**"
```

## BOE Context (from invoker)

- **Name:** Construction Methodology Narrative
- **Package:** PKG-06 (Construction Methodology + Administration)
- **Tier:** T2 (depends on DEL-02-01 concept and DEL-09-02 site conditions)
- **Substance:** Narrative
- **Cost Drivers:** Construction manager hours; staging, logistics, site safety, H&S plan, permits/inspections, sequencing. Depends on DEL-02-01 (concept) and DEL-09-02 (site conditions).
- **Cost Ownership:**
  - Construction methodology (staging, logistics, safety, sequencing) belongs to DEL-04-01 (NOT in DEL-04-02 or DEL-04-03)
  - Construction administration (cleaning, transport, site services -- SOW-020) belongs to DEL-04-01 (NOT in DEL-04-02 or DEL-04-03)
  - Budget control + change management belongs to DEL-04-02 (NOT here)
- **NOTE:** SOW-019 (construction methodology) and SOW-020 (construction administration) are BOTH mapped to DEL-04-01. The estimate must account for BOTH scope items.
