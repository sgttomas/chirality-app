# Estimate Summary: DEL-02-02 -- Firehall Apparatus Bays & Support Spaces

## Run Identity

| Field | Value |
|---|---|
| **Snapshot** | EST_DEL-02-02_2026-02-18_1036 |
| **Deliverable** | DEL-02-02 -- Firehall Apparatus Bays & Support Spaces |
| **Package** | PKG-002 -- Main Public Services Building (PSB) |
| **Basis of Estimate** | RATE_TABLE (primary) with ALLOWANCE fallback where noted |
| **Currency** | CAD |
| **Rounding** | DOLLAR |

## Estimate Total

| Category | Amount (CAD) |
|---|---|
| **DEL-02-02 Grand Total** | **$279,279** |

## Totals by CBS

| CBS Code | Description | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|---|
| 03-CONCRETE | Sealed concrete floor finishing | $30,829 | 6 | 11.0% |
| 09-FINISHES | Interior finishes (partitions, ceilings, paint, tile, doors) | $62,850 | 26 | 22.5% |
| 10-SPECIALTIES | Lockers, accessories, partitions | $92,600 | 3 | 33.1% |
| 11-EQUIPMENT | Breathing air compressor system | $55,000 | 1 | 19.7% |
| 22-PLUMBING | Bay sump assemblies | $18,000 | 1 | 6.4% |
| 23-MECH | Compressed air distribution piping | $20,000 | 1 | 7.2% |
| **TOTAL** | | **$279,279** | **38** | **100.0%** |

## Totals by Major Scope Element

| Scope Element | SOW Ref | Amount (CAD) | % of Total |
|---|---|---|---|
| **Apparatus bay floor finishing + ceiling paint** | SOW-0202 | $44,460 | 15.9% |
| **Bunker gear lockers (40 units)** | SOW-0206 | $88,000 | 31.5% |
| **Breathing air compressor system** | SOW-0203/SOW-0205 | $55,000 | 19.7% |
| **Compressed air distribution piping** | SOW-0203 | $20,000 | 7.2% |
| **Bay sump assemblies (4 fire bays)** | SOW-0202 | $18,000 | 6.4% |
| **Decontamination area fit-up** | SOW-0205 | $22,087 | 7.9% |
| **Support rooms fit-up (locker room, gear storage, SCBA, compressor, EMS)** | SOW-0205/SOW-0206 | $31,732 | 11.4% |
| **TOTAL** | | **$279,279** | **100.0%** |

## BasisOfEstimate_Used

- **Primary method:** RATE_TABLE -- unit rates derived from 9 price source files (see Source_Index.md).
- **Fallback method:** ALLOWANCE -- applied to 1 line item (L-005: compressed air distribution piping) where no direct rate table entry existed. FALLBACK_POLICY=ALLOW_ALLOWANCE was in effect.
- **Mixed methods:** ALLOW_MIXED_METHODS=TRUE. 37 of 38 lines are RATE_TABLE; 1 is ALLOWANCE.

## Key Cost Drivers

1. **Bunker gear lockers ($88,000 / 31.4%)** -- Largest single cost element. 40 units at $2,200 each. Quantity is confirmed (PP-15, Addendum 03 s1.13). Unit rate is mid-range for heavy-duty ventilated fire service lockers.

2. **Breathing air compressor system ($55,000 / 19.6%)** -- Complete system including compressor, dryer, cascade storage, fill panels, and room-level distribution piping. LOW confidence due to wide pricing range ($45k-$65k). Resolves CON-M-01 cost ownership to DEL-02-02.

3. **Apparatus bay floor finishing ($27,300 / 9.7%)** -- Sealed concrete densifier + sealer for 780 m2 (8,400 sf across 4 bays). Rate is established at $35/m2 per IA-08.

## Scope Exclusions (priced elsewhere)

The following items are within the firehall functional scope but are priced under other deliverables per cost ownership rules:

| Item | Priced Under | Reason |
|---|---|---|
| Overhead doors (hardware, frames, openers) | DEL-02-04 | Envelope/doors scope |
| HVAC system for bays | DEL-02-05 | Mechanical scope |
| Apparatus bay exhaust extraction systems | DEL-02-05 | Mechanical scope |
| Bay display systems (screens + mounting + connectivity) | DEL-02-06 | Electrical/IT scope |
| Electrical distribution, lighting in bays | DEL-02-06 | Electrical scope |
| Compressed air electrical feed | DEL-02-06 | Electrical scope |
| Water fill station (2-inch) | DEL-02-05 | Plumbing scope |
| General interior partitions and finishes (non-bay-specific) | DEL-02-01 | Architectural program scope |

## Blockers and Warnings

| Severity | Item | Impact |
|---|---|---|
| WARNING | Support room areas are approximate ranges from Functional Program | Quantities based on midpoint assumptions; actual areas may vary 15-20% at detailed design |
| WARNING | Compressed air piping is an allowance ($20,000) | No detailed routing available; quantity and rate are estimates |
| WARNING | Breathing air compressor system has LOW confidence | Wide price range ($45k-$65k); actual cost depends on system configuration selected |
| INFO | DEP-0202-E09: Alberta Building Code full text not yet obtained | May affect code compliance verification but does not directly affect pricing |
| INFO | No upstream deliverables have been estimated yet within this run | Cross-deliverable cost allocation verified by ownership rules only |
