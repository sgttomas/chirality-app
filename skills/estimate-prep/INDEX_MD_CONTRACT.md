# PriceSources/INDEX.md Contract (Phase SCAFFOLD)

Companion reference for `skills/estimate-prep/SKILL.md`. Defines the 7-section contract for `{snapshot}/PriceSources/INDEX.md`.

---

## Generation sequence

1. Generate the file inventory portion using `tools/reporting/generate_index_md.sh {snapshot}/PriceSources/`.
2. Augment with the 7 required sections listed below.

---

## Required sections

### 1. Header block

Must include:
- `execution root`
- `BOE path`
- `currency`
- `base year`
- `region`
- `prepared date`
- `status`

### 2. Data quality statement

With confidence level definitions aligned to ESTIMATING accuracy expectations:

| Confidence | Meaning | Accuracy |
|-----------|---------|----------|
| HIGH | Confirmed parameter or fixed allowance | Exact |
| MEDIUM | Parametric rate or typical effort estimate | +/-20-30% |
| LOW | Allowance or rough parametric | +/-30-50% |

### 3. File inventory table

Columns:
- file name
- item count
- primary consumer / used-by

### 4. PS-ID → file mapping

BOE price-source IDs mapped to files and key items.

### 5. ESTIMATING run configuration

Three subsections:

- **Deliverable-to-Package mapping** table (Package → Deliverables)
- **Per-package `PRICE_SOURCES` mapping** — for each package, list the literal file paths ESTIMATING should load. Differentiate between:
  - production-only deliverables (staff rates + LOE + parameters)
  - dual-nature deliverables that also embed construction pricing (e.g., Schedule A/B)
- **ESTIMATING usage guidance** — include verbatim:
  > "use `RecommendedRate` as point estimate; flag `Confidence=LOW` items; record `Basis` in Detail.csv Method column."

### 6. Open issues table

Issues affecting PRICE_SOURCES with impact and status.

### 7. Gaps table

Items requiring parametric estimation or future quotes, with workaround.

---

## Relationship to Detail.csv

The ESTIMATING agent consumes this INDEX.md to:
1. Locate `PRICE_SOURCES` file paths per package.
2. Apply confidence-based risk flags.
3. Record `Basis` values in `Detail.csv` rows.

Changes to INDEX.md structure impact ESTIMATING's Detail.csv generation.
