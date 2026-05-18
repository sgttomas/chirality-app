# Source Index — EST_DEL-02-01_2026-02-18_0800

## Price Sources Loaded

| # | File | Source Type | Rows | Supports | Cannot Support | Parsing Notes |
|---|---|---|---|---|---|---|
| 1 | Structural_Concrete_Rates.csv | Rate Table | 15 | Concrete slab/floor rates (SC-03, SC-04) for sealed concrete finish context | Not directly applicable to DEL-02-01 interior scope; slab-on-grade is structural (DEL-02-04) | Parsed OK; CSV with header |
| 2 | Building_Envelope_Rates.csv | Rate Table | 15 | Interior doors/frames/hardware (BE-11, BE-12, BE-13); sealant (BE-14) | Envelope/cladding/glazing items are DEL-02-04 scope | Parsed OK; CSV with header |
| 3 | Mechanical_System_Rates.csv | Rate Table | 14 | No items directly applicable to DEL-02-01 | All items are DEL-02-05 scope (HVAC, plumbing, exhaust) | Parsed OK; CSV with header |
| 4 | Electrical_System_Rates.csv | Rate Table | 14 | No items directly applicable to DEL-02-01 | All items are DEL-02-06 scope (power, lighting, telecom) | Parsed OK; CSV with header |
| 5 | Equipment_Pricing.csv | Rate Table | 15 | No items directly applicable to DEL-02-01 architectural scope | Bay equipment (DEL-02-02/03), generator (DEL-02-07), temp facilities (PKG-001) | Parsed OK; CSV with header |
| 6 | Professional_Design_Fees.csv | Rate Table | 8 | Architectural design fees (DF-01) | Other discipline fees belong to their respective DELs | Parsed OK; CSV with header |
| 7 | Construction_Labour_Rates.csv | Rate Table | 15 | Carpenter (T-02) for partition framing; Painter (T-12) for wall finishes | Trades applicable to other DEL scopes | Parsed OK; CSV with header |
| 8 | Assumed_Project_Parameters.csv | Parameters | 29 | Building areas (PP-05, PP-06); bay counts (PP-11, PP-12); overall cost (PP-21) | Not a price source per se; provides quantity parameters | Parsed OK; CSV with header |

## Applicable Rate Table Entries for DEL-02-01

### Interior Doors, Frames, Hardware
| ItemID | Description | Unit | RecommendedRate | Source File |
|---|---|---|---|---|
| BE-11 | Hollow metal door and frame (single; commercial) | each | $1,800 | Building_Envelope_Rates.csv |
| BE-12 | Hollow metal door and frame (double; commercial) | each | $3,400 | Building_Envelope_Rates.csv |
| BE-13 | Door hardware set (commercial; per opening) | each | $600 | Building_Envelope_Rates.csv |

### Design Fees
| ItemID | Description | Rate | Basis | Source File |
|---|---|---|---|---|
| DF-01 | Architectural design fees (full service; concept through CA) | 7.0% | Construction cost of architectural scope | Professional_Design_Fees.csv |

### Labour Rates (for computed line items)
| TradeID | Trade | Fully Burdened Rate | Source File |
|---|---|---|---|
| T-02 | Carpenter | $72/hr | Construction_Labour_Rates.csv |
| T-12 | Painter | $60/hr | Construction_Labour_Rates.csv |

### No Direct Rate Table Coverage
The following DEL-02-01 cost elements have no direct rate table entries in the provided PRICE_SOURCES:
- Interior partition walls (metal stud + gypsum board) -- no $/sf or $/lf rate in any source
- Ceiling system (suspended ACT or equivalent) -- no rate in any source
- Sealed concrete floor finish/sealer (topping/sealer only, not slab) -- no finish-only rate
- Accessibility features (ramps, tactile, signage hardware) -- no rate
- Code-required signage -- no rate

Under FALLBACK_POLICY=STRICT, these items are recorded as Amount=TBD.
