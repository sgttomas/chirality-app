# Run Context — EST_DEL-02-04_2026-02-18_1130

## Run Configuration

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-04_2026-02-18_1130 |
| **AsOf** | 2026-02-18T11:30:00-07:00 |
| **Scope** | DEL-02-04 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-02-04 |

## Resolved Paths

| Input | Path |
|---|---|
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO (read from deliverable folder) |
| **Deliverable Folder** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-04_Structure, Envelope, Roof & Overhead Doors |

## Price Sources (Resolved)

| Source File | Source Type | Relevance to DEL-02-04 |
|---|---|---|
| Structural_Concrete_Rates.csv | Rate Table | HIGH — foundations, concrete, structural steel, rebar, formwork, roof framing |
| Building_Envelope_Rates.csv | Rate Table | HIGH — wall panels, roof panels, insulation, air barrier, glazing, doors, flashing |
| Interior_Architectural_Rates.csv | Rate Table | MEDIUM — sealed concrete flooring (IA-08) |
| Mechanical_System_Rates.csv | Rate Table | LOW — sump rough-in only (bay sump rough-in embedded in slab is DEL-02-04) |
| Electrical_System_Rates.csv | Rate Table | LOW — not directly applicable (electrical scope is DEL-02-06) |
| Equipment_Pricing.csv | Rate Table | HIGH — overhead doors EQ-01 (8 units, car-wash grade) |
| Professional_Design_Fees.csv | Rate Table | MEDIUM — structural engineering design fees (DF-03) |
| Construction_Labour_Rates.csv | Rate Table | REFERENCE — labour rates embedded in unit rates; not separately applied |
| Assumed_Project_Parameters.csv | Parameters | HIGH — building area (PP-05), door counts (PP-13), sump count (PP-18) |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-02-04 | PKG-002 | DEL-02-04_Envelope-Structure-Roof-and-Doors | TRUE | Structure, Envelope, Roof & Overhead Doors for Main PSB |

## CBS Mapping Rule

CBS codes are assigned deterministically based on the physical system being estimated:

| CBS Code | Meaning | Mapping Rule |
|---|---|---|
| 03-CONCRETE | Concrete and formwork | Foundations, slabs, reinforcing, formwork |
| 05-STEEL | Structural steel | W-shapes, HSS, OWSJ, metal deck, misc steel |
| 07-ENVELOPE | Building envelope and roofing | Wall panels, roof panels, insulation, air barrier, flashing, sealant |
| 08-OPENINGS | Doors, glazing, hardware | Overhead doors, person doors, storefront entries, glazing, hardware |
| 09-FLOORING | Interior flooring | Sealed concrete, slab sealer/densifier |
| 31-EARTHWORK | Sump rough-in | Sump blockouts embedded in structural slab |
| 50-DESIGN | Professional design fees | Structural engineering design fees |

## Quantity Basis (from Assumed_Project_Parameters.csv)

| Parameter | Value | Source |
|---|---|---|
| Main PSB ground floor area | 18,000 sf / 1,672 m2 | PP-05 |
| Fire apparatus bays | 4 | PP-11 |
| PW shop bays | 4 | PP-12 |
| Total overhead doors (main building) | 8 | PP-13 |
| Bay sumps | 8 | PP-18 |
| Estimated building perimeter | ~540 lf / ~165 lm | ASSUMPTION ASM-02 (based on ~160x110 ft footprint from PP-05 notes) |
| Bay area (approx) | 12,000 sf / 1,115 m2 | ASSUMPTION ASM-03 (8 bays at ~1,500 sf each) |
| Office/shared area (approx) | 6,000 sf / 557 m2 | ASSUMPTION ASM-04 (18,000 - 12,000 sf) |
| Wall height (average) | 6.5 m (21.3 ft) | ASSUMPTION ASM-05 (accommodates 16 ft clear door + structure) |
| Gross wall area | ~1,073 m2 | ASSUMPTION ASM-06 (perimeter 165 lm x avg height 6.5 m) |

## Warnings

- [WARNING] Quantity basis relies on assumed building footprint dimensions (PP-05 notes: ~160x110 ft). Actual quantities TBD pending architectural program confirmation from DEL-02-01.
- [WARNING] Foundation type not yet selected by DB; estimate assumes screw piles per SC-14 as most cost-effective for Penhold soils (Decision DEC-01).
- [WARNING] Sump rough-in cost is included in DEL-02-04 per cost ownership rules; sump assemblies and plumbing connections are excluded (DEL-02-05).
- [WARNING] Overhead door backup power mechanism cost excluded (assigned to DEL-02-07 per cost ownership rules).
