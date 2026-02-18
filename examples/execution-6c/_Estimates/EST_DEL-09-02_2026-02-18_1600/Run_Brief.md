# Run Brief (Verbatim) -- EST_DEL-09-02_2026-02-18_1600

The following is the verbatim INIT-TASK brief provided by the invoker.

---

```
SCOPE: DEL-09-02
RUN_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-09_Due Diligence & Risk Register/1_Working/DEL-09-02_SiteConditionsAndDueDiligenceSummary
ESTIMATES_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/
BASIS_OF_ESTIMATE: RATE_TABLE
CURRENCY: CAD
DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
DEPENDENCY_SOURCES: AUTO
PRICE_SOURCES:
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv"
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv"
  - "/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv"
OUTPUT_LABEL: DEL-09-02
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

## BOE Context for DEL-09-02

- **Name:** Site Conditions & Due Diligence Summary
- **Package:** PKG-09 (Due Diligence & Risk Register)
- **Tier:** T0 (no upstream production dependencies)
- **Substance:** Narrative
- **Cost Drivers:** PM + technical lead hours; geotech summary, wetland assessment, environmental assessment, flood zone, site grading, survey approach (files after award per Addendum 03)
- **Cost Ownership:** Site conditions summary belongs to DEL-09-02 (NOT in DEL-02-01 which USES site data; PKG-09 SUMMARIZES it). Survey approach/assumptions belong to DEL-09-02 (NOT in DEL-08-01 which notes survey timing).
