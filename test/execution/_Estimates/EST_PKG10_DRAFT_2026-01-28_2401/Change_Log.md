# Change Log

## Snapshot Comparison

| Field | Value |
|-------|-------|
| Current Snapshot | EST_PKG10_DRAFT_2026-01-28_2401 |
| Previous Snapshot | None (first estimate for PKG-10) |
| Comparison Status | N/A |

---

## Summary

This is the **first estimate snapshot** for PKG-10 Railcar Unloading System. No previous snapshot exists for comparison.

**Snapshot Details:**
- **Package:** PKG-10 Railcar Unloading System
- **Deliverables:** 5 (DEL-10.01 through DEL-10.05)
- **Base Estimate:** $3,913,000 CAD
- **Contingency:** $996,000 CAD (25.4%)
- **Total Estimate:** $4,909,000 CAD
- **Confidence Level:** LOW (100% allowance-based pricing)

---

## Baseline Established

This snapshot establishes the baseline estimate for PKG-10 with the following characteristics:

### Scope Coverage
- 32 railcar unloading arms (articulating bottom-loading type)
- 32 quick-connect couplers (dry-break type)
- 400 lm gravity flow header piping (8-12 inch)
- 32 spill containment pans
- 8 sump pumps for containment drainage
- 32 flow indicators
- Atmospheric venting system (32 connections)
- Isolation valves and fittings
- Full EPC scope: Engineering (5 deliverables) + Materials + Construction + Indirects + Commissioning

### Pricing Basis
- **Method:** 100% allowance/parametric (fallback typical model)
- **Sources:** Decomposition + deliverable datasheets for quantities; industry typical ranges for pricing
- **Maturity:** INITIALIZED deliverables; no vendor quotes

### Key Assumptions (Top 5 by Impact)
1. Unloading arms @ $50k/unit × 32 = $1,600,000 (±20%)
2. Header piping 400 lm @ $700/lm = $280,000 (±20%)
3. Containment pans 32 units @ $8k/unit = $256,000 (±25%)
4. Unloading arm installation @ $8k/unit × 32 = $256,000 (±25%)
5. Header piping installation @ $450/lm × 400 lm = $180,000 (±25%)

---

## Next Estimate Run — Expected Changes

When the next estimate snapshot is created for PKG-10, expect changes in the following areas:

### High Probability Changes (Likely ±10-30% variance)
1. **Unloading arm pricing** — vendor quotes will replace $50k/unit assumption (actual quotes may be $45k-65k/unit range)
2. **Header piping length** — DEL-10.01 layout drawings will provide actual piping length (assumed 400 lm may be 320-480 lm actual)
3. **Sump pump quantity** — DEL-10.01 containment design will define pump count (assumed 8 pumps may be 4-16 actual)
4. **Engineering effort** — deliverable progression from INITIALIZED to IN_PROGRESS will refine scope and effort (±10-20%)

### Medium Probability Changes (Possible ±20-50% variance in specific items)
5. **Containment configuration** — individual pans vs grouped zones vs common containment will be defined (affects pan cost ±30% and installation approach)
6. **Quick-connect pricing** — clarify if integral to arms or separate procurement (may eliminate separate line item or adjust pricing)
7. **Food-grade material requirements** — material selection (carbon steel vs stainless steel) will be defined (stainless steel upgrade potential +20-40% on piping/containment)
8. **Labor rates** — project rate tables will replace assumed $110/hr composite rate (actual rates may vary ±15%)

### Lower Probability Changes (May affect specific buckets)
9. Atmospheric venting scope — vent configuration (individual vs manifold) and flame arrestor requirements
10. Flow indicator specifications — indicator type (visual, electronic, integrated with controls)
11. Commissioning scope — testing procedures and acceptance criteria will be defined
12. Interface coordination — PKG-07/PKG-14/PKG-17/PKG-20 interfaces may add or clarify scope

---

## Change Tracking for Future Runs

**Recommended tracking for next snapshot:**

1. **Pricing source changes:** Document transition from ALLOWANCE to QUOTE or RATE_TABLE for each line item that receives vendor data
2. **Quantity refinements:** Track changes to equipment counts, piping lengths, or other quantities when design details available
3. **Scope additions/deletions:** Identify new line items added or removed based on design progression
4. **CBS reallocations:** Note if line items move between CBS buckets due to scope clarification
5. **Contingency changes:** Track contingency % changes as estimate confidence improves (expect reduction from 25% to 15-20% when quotes obtained)

**Delta reporting format (for next run):**
```
| CBS | Previous Base | Current Base | Delta $ | Delta % | Driver |
|-----|---------------|--------------|---------|---------|--------|
| ... | ...           | ...          | ...     | ...     | ...    |
```

---

## Archive Note

When the next PKG-10 estimate snapshot is created, this snapshot (EST_PKG10_DRAFT_2026-01-28_2401) should be retained for audit trail. Do not overwrite or delete.

**Snapshot Lifecycle:**
- Created: 2026-01-28
- Status: BASELINE (first estimate for PKG-10)
- Archived: (future date when superseded by next snapshot)

---

*Change log prepared per AGENT_ESTIMATING Phase 4.4 (Publish Snapshot). Future snapshots will include delta analysis vs this baseline.*
