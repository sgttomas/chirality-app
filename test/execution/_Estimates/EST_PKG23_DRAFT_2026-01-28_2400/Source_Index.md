# Source Index

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
| Date | 2026-01-28 |

---

## Source Discovery Summary

| Source Type | Count | Status |
|-------------|-------|--------|
| Vendor Quotes | 0 | None found |
| Budgetary Quotes | 0 | None found |
| Rate Tables | 0 | None found |
| Historical Data | 0 | None found |
| Design Quantities | 0 | All TBD |

**Pricing Basis:** Fallback typical model (allowances) per Decision D-008

---

## Searched Locations

### 1. Explicit Pricing Sources (Priority 1)

| Location | Search Pattern | Result |
|----------|----------------|--------|
| `execution/_Estimates/_RateTables/` | `*.csv`, `*.xlsx`, `*.md` | No fire protection rate tables found |
| `execution/PKG-23_Fire_Protection/0_References/` | `*quote*`, `*pricing*`, `*budget*` | No pricing documents found |
| Deliverable `_REFERENCES.md` files | All PKG-23 deliverables | No pricing references indexed |

### 2. Rate Tables / Cost Libraries (Priority 2)

| Location | Search Pattern | Result |
|----------|----------------|--------|
| `execution/_Estimates/_RateTables/` | `fire*`, `protection*`, `alarm*`, `foam*` | Directory exists but no relevant tables |
| Project workspace | `*rate*`, `*unit cost*`, `*estimate*` | No rate tables discovered |

### 3. Quantity Sources (Priority 3)

| Location | Document | Quantity Data |
|----------|----------|---------------|
| DEL-23.01 Datasheet.md | Fire Protection Design Drawing Set | Quantities TBD; drawings INITIALIZED |
| DEL-23.02 Datasheet.md | Fire Protection Technical Specification | Performance requirements TBD |
| DEL-23.03 Datasheet.md | Fire Protection Design Calculations | Fire water demand TBD; hydraulic calcs TBD |
| DEL-23.04 Datasheet.md | Fire Protection Data Sheet Package | Equipment data TBD |
| DEL-23.05 Datasheet.md | Fire Protection Installation & Test Records | N/A (post-construction) |

### 4. Reference Documents (Employer's Requirements)

| Document | Location | Extraction Status |
|----------|----------|-------------------|
| Volume 2 Part 1: General Requirements | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_1_Employers_Requirements.pdf` | Not extracted |
| Volume 2 Part 2: Civil & Process Mechanical | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_2_Employers_Requirements.pdf` | Not extracted |
| Volume 2 Part 3: Building Works | `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_3_Employers_Requirements.pdf` | Not extracted |

---

## Design Document Status

| Deliverable | Status | Quantities Available | Notes |
|-------------|--------|---------------------|-------|
| DEL-23.01 | INITIALIZED | No | Fire water loop layout TBD; hydrant locations TBD |
| DEL-23.02 | INITIALIZED | No | Specifications TBD |
| DEL-23.03 | INITIALIZED | No | Fire water demand TBD; hydraulic calcs TBD |
| DEL-23.04 | INITIALIZED | No | Equipment data sheets TBD |
| DEL-23.05 | INITIALIZED | N/A | Post-construction records |

---

## Quantity Extraction Results

### From Decomposition

| Parameter | Value | Source |
|-----------|-------|--------|
| Storage tank count | 3 × 15,000 MT | Decomposition Section 1.1 |
| Railcar stations | 32 stations on 2 tracks | Decomposition Section 1.1 |
| Permitted throughput | 1,000,000 MT/annum | Decomposition Section 1.1 |
| Product | CSD canola oil | Decomposition Section 1.1 |

### From Deliverable Documents

| Quantity | Extracted Value | Status |
|----------|-----------------|--------|
| Fire water loop length | TBD | Pending DEL-23.01 |
| Fire hydrant count | TBD | Pending DEL-23.01 |
| Fire alarm device count | TBD | Pending DEL-23.01 |
| Foam system capacity | TBD | Pending DEL-23.03 |
| Fire water demand (gpm) | TBD | Pending DEL-23.03 |
| Fire water duration (hours) | TBD | Pending DEL-23.03 |

---

## Fallback Model Application

**Trigger:** No pricing sources or explicit quantities found; fallback typical model applied per AGENT_ESTIMATING protocol.

**Model Components Used:**

| Component | Application | Reference |
|-----------|-------------|-----------|
| Allowance placeholders | All materials and construction line items | A-001 through A-017 |
| Indirects factors | CI=18%, P=2%, PM=6%, COM=3% | D-009 |
| Contingency baseline | 20-30% by CBS bucket with allowance-heavy adjustment | D-008 |

**Disclosure:** All fallback model uses labeled in Detail.csv as `Method=ALLOWANCE` or `Method=PARAMETRIC` with `Confidence=LOW` or `Confidence=MEDIUM` and traced to assumption/decision IDs in SourceRef.

---

## Recommended Pricing Sources for Next Iteration

### Priority 1: Vendor Budgetary Quotes
1. Fire hydrant vendor (e.g., Mueller, Kennedy, AVK) — dry-barrel hydrants rated -40°C
2. Fire alarm system vendor (e.g., Honeywell, Edwards, Notifier) — addressable FACP and devices
3. Foam system vendor (e.g., Chemguard, Angus Fire, Kidde) — proportioning system, foam chambers
4. Fire protection contractor — installation budgetary quotes

### Priority 2: Rate Tables
1. BC Lower Mainland fire protection labor rates
2. Fire protection equipment rental rates
3. Underground utility installation rates (coordinate with PKG-03)

### Priority 3: Historical Data
1. Similar fire protection systems for tank farm facilities
2. Foam system costs for combustible liquid storage
3. Fire alarm system costs for industrial facilities

---

## Source Index Maintenance

| Action | Next Steps |
|--------|------------|
| Add vendor quotes | Place in `execution/_Estimates/_RateTables/` or deliverable `0_References/` |
| Add rate tables | Create `FireProtection_Rates.csv` in `_RateTables/` |
| Extract ER requirements | Process Volume 2 Part 1 for fire protection specifications |
| Update quantities | Complete DEL-23.01, DEL-23.03 design documents |

---
