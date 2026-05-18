# Estimate Summary — EST_DEL-02-04_2026-02-18_1130

## Deliverable

| Field | Value |
|---|---|
| **Deliverable** | DEL-02-04 — Structure, Envelope, Roof & Overhead Doors |
| **Package** | PKG-002 — Main Public Services Building (PSB) |
| **Basis of Estimate** | RATE_TABLE |
| **Currency** | CAD |
| **Rounding** | DOLLAR |

## BasisOfEstimate_Used

All line items priced using unit rates from the provided rate table sources (Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Interior_Architectural_Rates.csv, Equipment_Pricing.csv, Professional_Design_Fees.csv). Quantities are derived from the Assumed_Project_Parameters.csv building area (18,000 sf ground floor) and confirmed counts (8 overhead doors, 8 bay sumps), supplemented by dimensional assumptions documented in Assumptions_Log.md. One line item (L-027, sump rough-in) uses an assumed rate not directly from a rate table, flagged as LOW confidence.

## Estimate Total

| CBS Code | Description | Amount (CAD) | Lines | Share |
|---|---|---|---|---|
| 03-CONCRETE | Foundations, slabs, formwork, reinforcing | $370,390 | 8 | 21.5% |
| 05-STEEL | Structural steel framing, OWSJ, deck, misc | $461,668 | 4 | 26.8% |
| 07-ENVELOPE | Wall panels, masonry, roof panels, air barrier, flashing, sealant | $554,790 | 6 | 32.2% |
| 08-OPENINGS | Overhead doors, glazing, storefront, person doors, hardware | $249,100 | 6 | 14.5% |
| 09-FLOORING | Sealed concrete floor finish | $58,520 | 2 | 3.4% |
| 31-EARTHWORK | Sump rough-in blockouts | $6,000 | 1 | 0.3% |
| 50-DESIGN | Structural engineering design fees | $20,801 | 1 | 1.2% |
| **TOTAL** | | **$1,721,269** | **28** | **100%** |

## Cost Per Square Foot

| Metric | Value |
|---|---|
| Total estimate | $1,721,269 |
| Building footprint | 18,000 sf |
| **Cost per sf** | **$95.63/sf** |

## Cross-Check Against Parametric Benchmark

PP-21 from Assumed_Project_Parameters.csv estimates main PSB construction value at $6,600,000 (18,000 sf x $370/sf). DEL-02-04 at $1,721,269 represents approximately 26.1% of the total main PSB construction value. For a structure/envelope deliverable this percentage is within a reasonable range (typically 25-35% of total building cost for steel-framed institutional buildings with metal panel envelope).

## Key Warnings and Blockers

1. **Quantity assumptions dominate uncertainty.** Building footprint dimensions (PP-05: ~160x110 ft) are design-basis assumptions. Actual areas and perimeters will change when architectural program (DEL-02-01) is confirmed.

2. **Foundation type assumed.** Screw piles (SC-14) selected as the assumed foundation type for costing. DB may select spread footings or another system after geotechnical review. A spread footing approach could change CBS 03-CONCRETE by +/- 15-20%.

3. **Sump rough-in rate is not from rate tables.** L-027 ($6,000 total) uses an assumed $750/each rate for sump blockouts in slab. This is a LOW confidence estimate. Impact on total is minimal (0.3%).

4. **Overhead door backup power mechanism excluded.** Per cost ownership rules, the secondary opening mechanism cost (backup power) is assigned to DEL-02-07, not DEL-02-04. DEL-02-04 includes only the doors, motorized openers, and car-wash grade hardware.

5. **Interior partitions and finishes excluded.** Per cost ownership rules, interior partitions and finishes are DEL-02-01 scope, not DEL-02-04.

6. **Concrete aprons excluded.** Site concrete aprons at overhead doors are DEL-03-03 (Site & Civil) scope per cost ownership rules.

## Dependencies Affecting Estimate Readiness

- **DEL-02-01** (Architectural Program): Preliminary floor plan concept needed to confirm actual building dimensions and bay vs office area split.
- **DEL-02-02** (Firehall) and **DEL-02-03** (Public Works): Bay layouts needed to confirm structural framing grid and door locations.
- **DEL-02-07** (Emergency Power): Door secondary opening mechanism integration scope not yet confirmed.
- **Geotechnical Report** (RFP Appendix D): Required for foundation type confirmation.
- **Alberta Building Code**: Specific load tables and code edition required for structural design confirmation.

None of these constitute hard blockers to producing an estimate; they represent information that will refine quantities in future iterations.
