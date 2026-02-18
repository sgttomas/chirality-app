# Assumptions Log

## Assumptions

| AssumptionID | Assumption | Basis | Impact if Wrong |
|---|---|---|---|
| ASM-001 | The $20,000 FF&E cash allowance is a fixed value that will not change during this estimate snapshot. | DEC-005 (Gate 5, 2026-02-17); Addendum 03 s1.18; OPT-18 (PriceMin=PriceMax=$20,000). | If Owner changes the allowance value, a new estimate snapshot is required. No rework beyond re-running with updated inputs. |
| ASM-002 | The DB allocation breakdown (Meeting/Training $8k, Lunchroom $6k, Reception $3k, Misc $3k) is informational and may be rebalanced during design with Owner approval. | Brief instructions; SOW-0506 Notes in decomposition. | If allocation becomes binding, Detail.csv may need to be restructured into multiple lines. Currently carried as a single LS line per brief direction. |
| ASM-003 | FF&E scope excludes all items owned by DEL-05-06 (connected appliances requiring plumbing or dedicated electrical). The boundary between "loose FF&E" and "connected appliances" is clear per the brief. | Brief instructions; DEP-0507-E002 (interface dependency with DEL-05-06). | If boundary is unclear during procurement/design, double-counting or gaps could occur. The dependency register flags this interface. |
