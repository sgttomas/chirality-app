# Decision Log — EST_DEL-02-01_2026-02-18_2100

## Decisions Carried Forward from Prior Run

### DEC-R-001 — DF-01 Treated as RATE_TABLE Method
Carried forward unchanged.

### DEC-R-009 — Bay Floor Finishes Attributed to DEL-02-04
Carried forward unchanged.

### DEC-R-010 — Door Count (18 single + 1 double)
Carried forward unchanged.

## Superseded Decisions

The following prior-run decisions set items to TBD under STRICT fallback. They are now superseded because Interior_Architectural_Rates.csv (PS-27) provides rate table evidence:

| Prior Decision | Superseded By | Resolution |
|---|---|---|
| DEC-R-002 (design fee TBD — incomplete subtotal) | DEC-R-011 | Construction subtotal now complete; fee computable |
| DEC-R-003 (ceiling TBD — no rate) | DEC-R-012 | IA-05 provides rate |
| DEC-R-004 (accessibility TBD — no rate) | DEC-R-013 | IA-15/16/17/18 provide rates |
| DEC-R-005 (signage TBD — no rate) | DEC-R-014 | IA-19/20/21 provide rates |
| DEC-R-006 (partitions TBD — no rate) | DEC-R-015 | IA-01/02/04 provide rates |
| DEC-R-007 (floor finish TBD — no rate) | DEC-R-016 | IA-08 provides rate |
| DEC-R-008 (paint TBD — no rate) | DEC-R-017 | IA-12/13 provide rates |

## New Decisions in This Run

### DEC-R-011 — Design Fee Now Computable

| Field | Value |
|---|---|
| Decision | L-010 resolved: 7% of $157,317 construction subtotal = $11,012 |
| Rationale | All 9 construction line items (L-001 through L-009) are now priced, yielding a complete construction subtotal. DF-01 (7%) can be applied. |

### DEC-R-012 — Ceiling Priced from IA-05

| Field | Value |
|---|---|
| Decision | L-006 resolved: 483 m2 × $68/m2 (IA-05) = $32,844 |
| Rationale | IA-05 (suspended acoustic tile ceiling, 600x600 lay-in, T-bar grid) is a direct match for the ceiling scope. |

### DEC-R-013 — Accessibility Priced as Composite from IA-15/16/17/18

| Field | Value |
|---|---|
| Decision | L-007 resolved: composite of IA-15 (6 × $325 = $1,950) + IA-16 (8 m2 × $230 = $1,840) + IA-17 (2 × $1,100 = $2,200) + IA-18 (1 × $3,500) = $9,490 |
| Rationale | Alberta Building Code barrier-free requirements for a public building of this type require accessible hardware, tactile surfaces, grab bars, and accessible signage. Component counts are estimated. |

### DEC-R-014 — Signage Priced as Composite from IA-19/20/21

| Field | Value |
|---|---|
| Decision | L-008 resolved: composite of IA-19 (14 × $450 = $6,300) + IA-20 (1 × $2,000) + IA-21 (28 × $115 = $3,220) = $11,520 |
| Rationale | Exit sign count (14) based on building layout and Alberta Fire Code egress requirements. Room sign count (28) based on room count estimate from Datasheet.md. |

### DEC-R-015 — Partitions Priced from Blended IA-01/02/04

| Field | Value |
|---|---|
| Decision | L-004 resolved: 325 m2 × $93/m2 (blended) = $30,225. Blend: 70% IA-02 ($82 non-rated) + 20% IA-01 ($112 fire-rated) + 10% IA-04 ($132 wet area). |
| Rationale | Typical office/admin layout: majority non-rated partitions, some fire-rated at corridors/exits, some wet-area at washrooms/kitchen. 70/20/10 split is a standard assumption for institutional buildings. |

### DEC-R-016 — Floor Finish Priced from IA-08

| Field | Value |
|---|---|
| Decision | L-005 resolved: 483 m2 × $35/m2 (IA-08) = $16,905 |
| Rationale | IA-08 (sealed concrete floor — densifier + sealer) matches the scope: finish-only application on structural slab provided by DEL-02-04. Finish applies to office/admin/shared areas only (483 m2). |

### DEC-R-017 — Paint Priced from Blended IA-12/13

| Field | Value |
|---|---|
| Decision | L-009 resolved: 650 m2 × $14.05/m2 (blended) = $9,133. Blend: 85% IA-12 ($13 standard latex) + 15% IA-13 ($20 epoxy/wet area). |
| Rationale | Standard office/corridor walls receive standard latex paint; washrooms, kitchen, and decon areas receive washable epoxy/semi-gloss. 85/15 split reflects the proportional area of standard vs wet environments. |

### DEC-R-018 — Unit Conversion (sf to m2)

| Field | Value |
|---|---|
| Decision | Quantities converted from sf (used in prior run assumptions) to m2 to match Interior_Architectural_Rates.csv units. Conversion: 1 m2 = 10.764 sf. |
| Rationale | Rate table units are m2. Using m2 in Detail.csv ensures direct traceability to source rates without intermediate conversion errors. |
| Conversions | 3,500 sf → 325 m2; 5,200 sf → 483 m2; 7,000 sf → 650 m2 |
