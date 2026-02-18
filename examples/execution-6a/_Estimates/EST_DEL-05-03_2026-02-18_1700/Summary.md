# Estimate Summary -- DEL-05-03 Option - Access Control

**Snapshot:** EST_DEL-05-03_2026-02-18_1700
**Date:** 2026-02-18
**Currency:** CAD
**Rounding:** DOLLAR

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Declared Basis | QUOTE |
| Actual Method(s) | PARAMETRIC (fallback; no vendor quote exists) |
| Fallback Policy | ALLOW_ALLOWANCE (ALLOW_MIXED_METHODS=TRUE) |
| Confidence | LOW |
| Status | REQUIRES VENDOR QUOTE REPLACEMENT |

---

## Totals

### By Deliverable

| DeliverableID | Name | Amount (CAD) | Line Count | Confidence |
|---|---|---|---|---|
| DEL-05-03 | Option -- Access Control | $45,000 | 1 | LOW |

### By CBS

| CBS | Description | Amount (CAD) |
|---|---|---|
| 26 05 00 | Electronic Access Control and Intrusion Detection | $45,000 |

### Grand Total

| | Amount (CAD) |
|---|---|
| **DEL-05-03 Total** | **$45,000** |

---

## Scope Coverage

- **In scope:** DEL-05-03 (1 deliverable)
- **Scope item:** SOW-0502 -- Optional priced item: Access control system for multiple zones within main building; ancillary buildings excluded.
- **Package:** PKG-005 (Optional Priced Items & Owner-Elected Additions)

### What is included in this estimate

- Access control system for main building (10-zone base): readers, controllers, head-end software, door contacts, request-to-exit devices, wiring, programming, commissioning
- Software licensing for access control
- Installation labor (bundled in system price)

### What is explicitly excluded (owned by other deliverables)

| Excluded Item | Cost Owner | Reference |
|---|---|---|
| IT network infrastructure that access control connects to | DEL-02-06 | Brief: Cost Ownership Rules |
| Door hardware (standard locksets, closers) | DEL-02-01 | Brief: Cost Ownership Rules |
| Electrical power circuits to door controllers | DEL-02-06 | Brief: Cost Ownership Rules |

---

## Key Warnings and Blockers

### Warnings

1. **BASIS_MISMATCH:** Declared QUOTE but no vendor quotes exist. All lines priced as PARAMETRIC using Optional_Items_Pricing.csv. Requires vendor quote replacement before final submission.
2. **QUANTITY_TBD:** Number of controlled zones/doors assumed at 10 (per PP-28). Actual count depends on DEL-02-01 floor plan, which is an unresolved upstream prerequisite (DEP-05-03-003).
3. **LOW_CONFIDENCE:** All AccessControl price source lines are rated LOW confidence. Price range is $35,000-$55,000; midpoint ($45,000) used.

### Blockers (from dependency evidence)

| Blocker | Source | Impact |
|---|---|---|
| DEL-02-01 floor plan required for zone mapping | DEP-05-03-003 | Cannot finalize zone count or placement without floor plan concept |
| DEL-02-06 coordination for low-voltage power, conduit, network | DEP-05-03-004 | Interface coordination needed; does not block pricing but blocks detailed scope definition |

---

## Pricing Range (sensitivity)

Based on OPT-06 price range:

| Scenario | Amount (CAD) | Notes |
|---|---|---|
| Low | $35,000 | OPT-06 PriceMin; 10 zones assumed |
| Recommended (used) | $45,000 | OPT-06 RecommendedPrice; 10 zones assumed |
| High | $55,000 | OPT-06 PriceMax; 10 zones assumed |

If additional zones are required beyond 10, each zone adds approximately $2,500-$4,000 (recommended $3,200 per OPT-07).
