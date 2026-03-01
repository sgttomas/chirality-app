# Assumptions Log (BOE)

| AssumptionID | Statement | Impact if wrong | Confidence |
|---|---|---|---|
| BOE-A01 | Tiers derived from BLOCKING dependencies only | Non-blocking coordination may be under-sequenced | MEDIUM |
| BOE-A02 | Cyclic dependencies handled as SCC bundles (same tier) | May mask a needed strict gate | MEDIUM |
| BOE-A03 | Package-level deliverable mapping DEL-003/DEL-004 uses representative deliverables | Tiering for utility tie-ins may shift | LOW |
