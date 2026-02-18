# Decision Log: EST_DEL-02-02_2026-02-18_1036

## Defaults Applied

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | ROUNDING=DOLLAR applied to all amounts | Per run brief; all line items rounded to nearest dollar |
| DEC-EST-002 | ALLOW_MIXED_METHODS=TRUE; FALLBACK_POLICY=ALLOW_ALLOWANCE | Per run brief; allows ALLOWANCE method where rate table evidence is missing |
| DEC-EST-003 | Compressed air distribution piping priced as ALLOWANCE ($20,000) | No direct rate table entry for piping distribution layout. Allowance based on typical 4-bay compressed air distribution (4 runs x ~15-25m each + ceiling drops + valves + fittings). FALLBACK_POLICY authorizes this. |

## Scope Resolution Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-004 | Overhead doors excluded from DEL-02-02 estimate | Per cost ownership rules: overhead doors (hardware, frames, openers) belong to DEL-02-04. |
| DEC-EST-005 | HVAC and apparatus bay exhaust systems excluded from DEL-02-02 estimate | Per cost ownership rules: HVAC to DEL-02-05; exhaust extraction units to DEL-02-05. |
| DEC-EST-006 | Bay display systems excluded from DEL-02-02 estimate | Per cost ownership rules: screens + mounting + connectivity belong to DEL-02-06. |
| DEC-EST-007 | Electrical distribution and lighting excluded from DEL-02-02 estimate | Per cost ownership rules: all electrical to DEL-02-06. |
| DEC-EST-008 | Water fill station excluded from DEL-02-02 estimate | Per cost ownership rules: plumbing fixtures belong to DEL-02-05. However, DEL-02-02 does include bay sumps as bay-specific fit-up. |
| DEC-EST-009 | Bay sumps included in DEL-02-02 (not DEL-02-05) | Bay sumps are bay-specific functional fit-up items. Cost ownership rules state: "Fire bay functional fit-up ... -> DEL-02-02." Sumps are integral to bay function (snow melt, minor washing). |
| DEC-EST-010 | Breathing air compressor system priced under DEL-02-02 | Per cost ownership rules: "Compressed air EQUIPMENT (compressor, piping, drops) -> DEL-02-02 (NOT DEL-02-05; resolves CON-M-01)." Both EQ-08 and MS-08 confirm this assignment. |
| DEC-EST-011 | General interior partitions/finishes for shared spaces excluded | Per cost ownership rules: "Interior partitions, finishes, doors -> DEL-02-01 (NOT DEL-02-02)." Only bay-specific fit-up items are included in DEL-02-02. |

## CBS Mapping Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-012 | CBS codes assigned per deterministic mapping rule documented in Run_Context.md | CBS codes follow CSI MasterFormat division mapping: 03=Concrete, 09=Finishes, 10=Specialties, 11=Equipment, 22=Plumbing, 23=Mechanical. |

## Quantity Derivation Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-013 | Bay area = 2,100 sf each (midpoint of 2,000-2,200 sf range) | Addendum 03 s1.21 provides 2,000-2,200 sf per bay. Midpoint used. See ASM-001. |
| DEC-EST-014 | Support room areas use midpoint of Functional Program ranges | All support room areas are provided as ranges in Addendum 03 s1.21. Midpoints used for all rooms. See ASM-002 through ASM-008. |
| DEC-EST-015 | Partition quantities estimated from room perimeter geometry | Wall areas derived from approximate room perimeter x 3m (10 ft) wall height, less openings. Rough estimate suitable for proposal-stage pricing. |
