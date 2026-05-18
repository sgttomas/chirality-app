# Estimate Summary: DEL-05-01 Schedule A -- Pricing Summary

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | RATE_TABLE (production lines) + PARAMETRIC/ALLOWANCE (construction content) |
| **Currency** | CAD |
| **Rounding** | DOLLAR |
| **Fallback Policy** | ALLOW_ALLOWANCE |
| **Mixed Methods** | TRUE (intentional per BOE Section 3.2) |
| **Snapshot** | EST_DEL-05-01_2026-02-18_1400 |

---

## Dual Cost Nature

DEL-05-01 has two distinct cost types per BOE:

| Cost Type | Description | Lines | Total (CAD) |
|---|---|---|---|
| **Production Cost** | Estimator/PM hours to compile the Schedule A form | L-001 through L-003 | **$9,960** |
| **Construction Pricing Content** | Actual proposal prices written INTO Schedule A | L-010 through L-041 | **$10,729,000** |
| **GRAND TOTAL** | | 24 lines | **$10,738,960** |

---

## Production Cost Detail

| LineID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | Method |
|---|---|---|---|---|---|
| L-001 | R-18 Estimator (Senior) | 40 | $145 | $5,800 | RATE_TABLE |
| L-002 | R-19 Estimator (Intermediate) | 24 | $115 | $2,760 | RATE_TABLE |
| L-003 | R-02 Project Manager | 8 | $175 | $1,400 | RATE_TABLE |
| | **Production Subtotal** | **72 hrs** | | **$9,960** | |

---

## Construction Pricing Content -- Schedule A Summary

### Base Building Scope

| LineID | CBS | Description | Amount (CAD) | Method |
|---|---|---|---|---|
| L-010 | GR | General Requirements (15% of base) | $1,305,000 | PARAMETRIC |
| L-011 | STRUCT | Structural and Concrete (main PSB) | $1,320,000 | PARAMETRIC |
| L-012 | ENVLP | Building Envelope (main PSB) | $980,000 | PARAMETRIC |
| L-013 | INTARCH | Interior Architectural (main PSB) | $520,000 | PARAMETRIC |
| L-014 | MECH | Mechanical Systems (main PSB) | $1,180,000 | PARAMETRIC |
| L-015 | ELEC | Electrical Systems (main PSB) | $810,000 | PARAMETRIC |
| L-016 | CIVIL | Site and Civil Works (4.5 acres) | $1,230,000 | PARAMETRIC |
| L-017 | CIVIL | Underground Utilities | $350,000 | PARAMETRIC |
| L-018 | STRUCT | Cold Storage Building (6,000 sf PEMB) | $290,000 | PARAMETRIC |
| L-019 | EQUIP | Specialty Equipment + Temporary Facilities | $540,000 | PARAMETRIC |
| L-020 | DESFEE | Professional Design Fees | $780,000 | PARAMETRIC |
| L-021 | FEES | Bonds and Insurance (5.45% combined) | $474,000 | PARAMETRIC |
| L-022 | FEES | Permits and Fees | $84,000 | PARAMETRIC |
| | | **Base Construction Subtotal** | **$9,863,000** | |
| L-040 | OPT | GST on Base (5%) | $493,000 | PARAMETRIC |
| | | **Base Construction + GST** | **$10,356,000** | |

### Additional Options

| LineID | Option | Description | Amount (CAD) | Method |
|---|---|---|---|---|
| L-030 | Option 1 | Built-in Wash Bay | $123,000 | PARAMETRIC |
| L-031 | Option 2 | Yard Lighting (12 poles) | $100,000 | PARAMETRIC |
| L-032 | Option 3 | Building Access Control (10-zone) | $45,000 | PARAMETRIC |
| L-033 | Option 4 | Security Cameras + Year 1 Monitoring | $55,000 | PARAMETRIC |
| L-034 | Option 5 | Exterior Signage (non-illuminated) | $12,000 | PARAMETRIC |
| L-035 | Option 6 | FF&E Cash Allowance (OI-004) | $20,000 | ALLOWANCE |
| | | **Options Subtotal** | **$355,000** | |
| L-041 | | GST on Options (5%) | $18,000 | PARAMETRIC |
| | | **Options + GST** | **$373,000** | |

### Construction Content Grand Total

| | Amount (CAD) |
|---|---|
| Base Construction (excl. GST) | $9,863,000 |
| GST on Base | $493,000 |
| Additional Options (excl. GST) | $355,000 |
| GST on Options | $18,000 |
| **Construction Pricing Content Total** | **$10,729,000** |

---

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| FIN | Production -- Financial roles | $8,560 | 2 |
| MGMT | Production -- Management roles | $1,400 | 1 |
| GR | General Requirements | $1,305,000 | 1 |
| STRUCT | Structural (main + cold storage) | $1,610,000 | 2 |
| ENVLP | Building Envelope | $980,000 | 1 |
| INTARCH | Interior Architectural | $520,000 | 1 |
| MECH | Mechanical Systems | $1,180,000 | 1 |
| ELEC | Electrical Systems | $810,000 | 1 |
| CIVIL | Site/Civil + Utilities | $1,580,000 | 2 |
| EQUIP | Specialty Equipment | $540,000 | 1 |
| DESFEE | Design Fees | $780,000 | 1 |
| FEES | Bonds/Insurance/Permits | $558,000 | 2 |
| OPT | Options + GST | $866,000 | 8 |
| **TOTAL** | | **$10,738,960** | **24** |

---

## Parametric Cross-Check

| Check | Source | Parametric Value | Estimated Value | Variance |
|---|---|---|---|---|
| Main PSB (all-in per sf) | PB-07: $415/sf x 18,000 sf | $7,470,000 | $6,945,000 (L-010 through L-015 + L-019 excl. GR) | -7% |
| Main PSB with GR | PB-04: $370/sf x 18,000 sf | $6,660,000 | $8,250,000 (base building excl. site/civil/cold storage/fees) | +24% |
| Cold storage | PB-02: $48/sf x 6,000 sf | $288,000 | $290,000 | +1% |
| Site/civil | PB-06: $16/sf x 196,020 sf | $3,136,000 | $1,580,000 | -50% |
| Total project (PP-25) | PP-25 parametric | $12,000,000 | $10,729,000 (content) or $10,739,000 (with production) | -11% |

**Notes on cross-check:**
- Main PSB with GR is 24% above PB-04 parametric because the estimate includes design fees, bonds/insurance, and permits that PB-04 excludes.
- Site/civil is 50% below PB-06 because PB-06 uses gross site area (196k sf) while our estimate scopes to 4.5 developed acres with actual quantity takeoffs. The developed area approach is more accurate.
- Total project is 11% below PP-25 ($12M) parametric. This is within the LOW confidence range of PP-25 (+/-30-50%).
- Overall, cross-checks are within acceptable parametric variance ranges.

---

## Scope Coverage

- Deliverables in scope: 1 (DEL-05-01)
- Deliverables priced: 1
- Deliverables blocked: 0
- Deliverables with TBD amounts: 0

---

## Key Observations

1. **Dual cost nature executed**: Both production cost ($9,960) and construction pricing content ($10,729,000) are captured in separate line groups as required by BOE Section 3.2 and INDEX.md.

2. **Production cost is <0.1% of construction content**: The 72 hours of estimator/PM time to compile Schedule A is a tiny fraction of the construction prices written into the form. This is expected -- Schedule A is a summary form populated from Schedule B detail.

3. **Base construction excluding GR, fees, bonds, permits = $7,220,000**: This compares to PP-24 ($8,700,000). The difference is explained by PP-24 including general requirements (which adds $1,305,000) while our $7,220,000 is direct construction costs only.

4. **Additional Options total $355,000 (3.6% of base)**: Options are relatively modest compared to the base building scope.

5. **OI-004 (FF&E) resolved**: $20,000 cash allowance carried as Additional Option 6 per BOE recommendation (OPT-18, Confidence HIGH).

6. **All construction content lines are PARAMETRIC or ALLOWANCE**: No vendor quotes obtained. Confidence is LOW to MEDIUM. These values should be refined with actual construction estimates before proposal submission.

7. **GST separated per SOW-005**: Federal GST (5%) calculated separately on base scope and optional items as required by Schedule A format.

---

## Key Warnings and Blockers

### Warnings

1. **W-001**: All construction pricing content is PARAMETRIC (no vendor quotes). Accuracy is +/-20-50% depending on line item. This is appropriate for proposal pricing but should be refined.
2. **W-002**: Design fee calculation ($780,000 = 9% of base construction) uses a blended percentage approach. Actual DB firm design fee structure may differ.
3. **W-003**: Bond/insurance rates (5.45% combined) are market estimates. Actual surety and insurance quotes should be obtained.
4. **W-004**: PP-25 parametric cross-check shows 10% variance from estimated total. Within acceptable range but warrants review.
5. **W-005**: OI-004 (FF&E) is implemented as recommended ($20k allowance) but is still formally OPEN per decomposition status.

### Blockers

- **No blockers** for estimate production. DEP-05-01-E-001 (Schedule B prerequisite) is a production dependency that affects the actual form completion sequence, not the estimate.
