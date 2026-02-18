# Source Index

## Indexed Price Sources

### Source 1: Optional_Items_Pricing.csv

- **Path:** `_PriceSources/Optional_Items_Pricing.csv`
- **Source type:** Rate table (consumed as RATE_TABLE; source self-describes as PARAMETRIC basis)
- **Parsing notes:** CSV with columns: ItemID, Category, Description, Unit, PriceMin, PriceMax, RecommendedPrice, Basis, Confidence, Notes
- **Relevant rows for DEL-05-02:**
  - **OPT-04** (YardLighting): Yard light pole + fixture + base + wiring; per unit installed; $7,500 each (range $6,500-$9,000); MEDIUM confidence
  - **OPT-05** (YardLighting): Yard lighting conduit run from panel to first pole; $80/lm (range $65-$95); MEDIUM confidence
- **Cannot support:** Quantity determination (quantity comes from PP-20 and site design)

### Source 2: Assumed_Project_Parameters.csv

- **Path:** `_PriceSources/Assumed_Project_Parameters.csv`
- **Source type:** Project parameter table (supports quantity assumptions, not unit rates)
- **Parsing notes:** CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes
- **Relevant rows for DEL-05-02:**
  - **PP-20**: Yard lighting poles (if optional elected) = 12 each; ASSUMPTION; LOW confidence; depends on site layout from DEL-03-01
- **Cannot support:** Unit rate derivation (unit rates come from Optional_Items_Pricing.csv)

## Dependency Evidence (read-only; not a price source)

- **Path:** `PKG-005_.../DEL-05-02_.../Dependencies.csv`
- **Used for:** Blocker/readiness assessment only (see Blockers.md)
- **NOT used for:** Unit rate or pricing evidence
