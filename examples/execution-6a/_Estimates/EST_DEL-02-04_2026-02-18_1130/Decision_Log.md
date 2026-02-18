# Decision Log — EST_DEL-02-04_2026-02-18_1130

## Defaults Applied

### DEC-01: Foundation Type Selection
- **Decision:** Screw piles (SC-14) assumed as foundation system for costing purposes.
- **Rationale:** SC-14 description notes "Galvanized; 2.75" to 3.5" shaft; 6-8m depth typical for Penhold soils," indicating rate table was developed with Penhold conditions in mind. Screw piles are a cost-effective and common foundation solution for steel-framed municipal buildings in central Alberta. DB will select actual foundation type after geotechnical review.
- **Alternative considered:** Spread footings (SC-12) at $2,500 each would yield a lower foundation unit cost but require additional excavation and backfill not included in the SC-12 rate. Net comparison is roughly equivalent; screw piles chosen for consistency with parametric basis.
- **Impact:** Foundation cost (L-001 through L-005) = $198,305. Switching to spread footings could change this by +/- 15-20%.

### DEC-02: Structural Engineering Design Fee Base
- **Decision:** Structural engineering design fee (DF-03) calculated as 2.5% of the structural construction cost (CBS 03-CONCRETE + CBS 05-STEEL = $832,058), yielding $20,801.
- **Rationale:** DF-03 description specifies "Construction cost of structural scope" as the fee base. The structural scope for fee purposes includes concrete/foundations and structural steel, but excludes envelope, openings, and flooring which are not within the structural engineer's design responsibility.
- **Impact:** L-028 = $20,801.

### DEC-03: Overhead Door Count and Grade
- **Decision:** 8 overhead doors at car-wash grade (EQ-01), consistent with PP-13 and the brief's cost ownership rules.
- **Rationale:** PP-13 explicitly derives 8 doors from 4 fire + 4 PW bays. EQ-01 specifies car-wash grade hardware. Each bay is drive-through with doors on both ends in some designs, but PP-13 counts 8 total (one door per bay opening), consistent with the quantity assumed in Equipment_Pricing.csv.
- **Note:** If the actual layout requires drive-through doors on both ends (16 total), this estimate would need to double the overhead door cost (+$160,000). The current assumption follows PP-13.

### DEC-04: Sump Rough-In Scope Boundary
- **Decision:** Sump rough-in (blockout + sleeve in structural slab) is included in DEL-02-04. Sump assemblies (oil/water separator, plumbing connections) are excluded per cost ownership rules (assigned to DEL-02-05).
- **Rationale:** The brief explicitly states: "Sump ROUGH-IN (embedded in slab) -> DEL-02-04" and "Sump ASSEMBLIES + PLUMBING connections -> DEL-02-05."
- **Impact:** L-027 = $6,000 (8 locations x $750).

### DEC-05: Interior Flooring Scope Boundary
- **Decision:** Sealed concrete floor finish (densifier + sealer) for bay and office/shared areas is included in DEL-02-04. No other flooring types (ceramic tile, VCT, rubber) are included.
- **Rationale:** SOW-0217 assigns durable/resilient interior flooring to DEL-02-04. Addendum 03 confirms sealed concrete is acceptable/desired. Interior partitions and other finishes are DEL-02-01 per cost ownership rules.
- **Impact:** L-025 + L-026 = $58,520.

### DEC-06: Overhead Door Backup Power Exclusion
- **Decision:** Overhead door secondary opening mechanism (backup power when on generator) is excluded from DEL-02-04.
- **Rationale:** Brief states: "Overhead door BACKUP POWER mechanism -> DEL-02-07 (NOT DEL-02-04)."
- **Impact:** No cost in this estimate for backup power mechanism; that cost will appear in DEL-02-07 estimate.

## Scope Resolution Decisions

### DEC-07: Concrete Aprons Excluded
- **Decision:** Concrete aprons at overhead door access points are excluded from DEL-02-04.
- **Rationale:** Specification.md Out of Scope section states "Site/civil works including concrete aprons (DEL-03-03)." Brief also excludes them: aprons are DEL-03-03 scope.
- **Impact:** No cost for aprons in this estimate.

### DEC-08: Rate Selection (RecommendedRate Used)
- **Decision:** All line items use the RecommendedRate from rate tables (the midpoint recommendation).
- **Rationale:** Rate tables provide RateMin, RateMax, and RecommendedRate. FALLBACK_POLICY=STRICT and ALLOW_MIXED_METHODS=FALSE. Using RecommendedRate provides the best single-point estimate consistent with MEDIUM confidence.
- **Impact:** Applies to all 28 line items.

### DEC-09: CBS Code Assignment Rule
- **Decision:** CBS codes follow UniFormat-inspired numeric prefixes mapped deterministically as documented in Run_Context.md.
- **Rationale:** No explicit CBSHint was provided in the decomposition. The CBS mapping rule is documented for traceability and consistency with downstream aggregation.
- **Impact:** All line items have CBS codes assigned per this rule.
