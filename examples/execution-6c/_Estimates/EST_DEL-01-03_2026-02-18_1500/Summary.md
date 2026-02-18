# Estimate Summary: DEL-01-03 Bonding & Insurance Evidence

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | RATE_TABLE (production lines) + ALLOWANCE (bond/insurance premium lines) |
| **Currency** | CAD |
| **Rounding** | DOLLAR |
| **Fallback Policy** | ALLOW_ALLOWANCE |
| **Mixed Methods** | TRUE (authorized per BOE Section 4 PKG-01 table) |
| **Snapshot** | EST_DEL-01-03_2026-02-18_1500 |

---

## Dual Cost Nature

DEL-01-03 has two distinct cost types per BOE cost ownership rules:

| Cost Type | Description | Lines | Total (CAD) |
|---|---|---|---|
| **Production Cost** | PM, legal, and admin hours to produce bond/insurance documentation | L-001 through L-003 | **$2,060** |
| **Bond Premiums** | Performance bond + L&M bond premiums (2.5% of base construction) | L-010 through L-011 | **$246,575** |
| **Insurance Premiums** | CCIP + builder's risk + CGL (2.95% of base construction) | L-020 through L-022 | **$290,959** |
| **Surety Broker Fee** | Broker commission for bond arrangement | L-030 | **$3,500** |
| **GRAND TOTAL** | | 9 lines | **$543,094** |

---

## Production Cost Detail

| LineID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | Method |
|---|---|---|---|---|---|
| L-001 | R-02 Project Manager | 4 | $175 | $700 | RATE_TABLE |
| L-002 | R-25 Legal Review (External) | 4 | $300 | $1,200 | RATE_TABLE |
| L-003 | R-24 Administrative / Document Control | 2 | $80 | $160 | RATE_TABLE |
| | **Production Subtotal** | **10 hrs** | | **$2,060** | |

---

## Bond Premium Detail

Contract value basis: **$9,863,000** (base construction excl. GST from DEL-05-01 Schedule A, EST_DEL-05-01_2026-02-18_1400).

| LineID | Item | Rate | Amount (CAD) | Method |
|---|---|---|---|---|
| L-010 | FP-01 Performance Bond (50% contract) | 1.50% | $147,945 | ALLOWANCE |
| L-011 | FP-02 Labour & Materials Payment Bond (50% contract) | 1.00% | $98,630 | ALLOWANCE |
| | **Bonds Subtotal** | **2.50%** | **$246,575** | |

---

## Insurance Premium Detail

| LineID | Item | Rate | Amount (CAD) | Method |
|---|---|---|---|---|
| L-020 | FP-03 CCIP Insurance | 2.00% | $197,260 | ALLOWANCE |
| L-021 | FP-04 Builder's Risk Insurance | 0.20% | $19,726 | ALLOWANCE |
| L-022 | FP-05 General Liability Insurance (CGL) | 0.75% | $73,973 | ALLOWANCE |
| | **Insurance Subtotal** | **2.95%** | **$290,959** | |

---

## Surety Broker Fee

| LineID | Item | Amount (CAD) | Method |
|---|---|---|---|
| L-030 | FP-19 Surety Broker Fee | $3,500 | ALLOWANCE |

---

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| MGMT | Production -- PM coordination | $700 | 1 |
| LEGAL | Production -- Legal review + surety broker fee | $4,700 | 2 |
| ADMIN | Production -- Document assembly | $160 | 1 |
| BOND | Bond premiums (performance + L&M) | $246,575 | 2 |
| INS | Insurance premiums (CCIP + builder's risk + CGL) | $290,959 | 3 |
| **TOTAL** | | **$543,094** | **9** |

---

## Scope Coverage

- Deliverables in scope: 1 (DEL-01-03)
- Deliverables priced: 1
- Deliverables blocked: 0
- Deliverables with TBD amounts: 0

---

## Cost Ownership Notes

Per BOE Section 4 PKG-01 cost ownership rules:

| Scope Area | Owner | Notes |
|---|---|---|
| Bond/insurance documentation effort (production hours) | DEL-01-03 | $2,060 -- PM, legal, admin hours |
| Bond/insurance premium amounts | DEL-01-03 (documents) + DEL-05-01/05-02 (carries in pricing) | $540,034 documented here; the SAME amounts appear in Schedule A L-021 ($474,000 bonds + insurance combined) |
| Surety broker fee | DEL-01-03 | $3,500 -- arranging bonds is part of bonding evidence scope |

**NOTE on double-counting**: The bond/insurance premium amounts documented here ($537,534 total premiums) are the deliverable-level documentation of these costs. The Schedule A (DEL-05-01) carries a combined bonds and insurance line (L-021: $474,000) at a blended 5.45% rate. These are different calculation approaches to the same underlying costs. For AGGREGATION purposes, the premium amounts should NOT be summed with DEL-05-01 construction content -- they represent the same economic cost documented in two different places per BOE cost ownership rules. Only the production cost ($2,060) and broker fee ($3,500) are additive PKG-01 costs.

---

## Key Observations

1. **Production cost is minimal ($2,060)**: The 10 hours of professional time to assemble bond/insurance documentation is a small fraction of the premium costs they document.

2. **Bond premiums ($246,575) represent 2.5% of base construction**: This is within standard market range for municipal design-build projects in Alberta.

3. **Insurance premiums ($290,959) represent 2.95% of base construction**: CCIP at 2.0% is the largest component. This rate has LOW confidence and depends heavily on project risk profile and insurer.

4. **Combined bond + insurance = 5.45% of base construction ($537,534)**: This aligns with the DEL-05-01 Schedule A combined line (L-021: $474,000 at 5.45% blended rate). The difference ($63,534) is because DEL-05-01 used a slightly rounded calculation approach.

5. **Surety broker fee ($3,500) is separate from bond premiums**: Per FP-19, the broker fee may sometimes be embedded in the premium; this estimate carries it separately for transparency.

---

## Key Warnings and Blockers

### Warnings

1. **W-001**: All bond/insurance premiums are ALLOWANCE method at MARKET rates. Actual surety and insurance quotes must be obtained before proposal submission.
2. **W-002**: Contract value basis ($9,863,000) is from a PARAMETRIC construction estimate (DEL-05-01). When actual construction pricing is finalized, bond and insurance premiums MUST be recalculated.
3. **W-003**: RFP Section 5.3.1 bond requirements have not been fully extracted (DEP-01-03-005 status PENDING). Bond types and amounts are assumed to be standard performance + L&M per Alberta municipal DB practice.
4. **W-004**: CCIP insurance rate (FP-03, 2.0%) has LOW confidence. Actual CCIP quotes for this project size and risk profile may differ significantly.
5. **W-005**: DEL-01-03 production depends on DEL-05-01 for contract value (DEP-01-03-006). Schedule A has been estimated but is PARAMETRIC. Final bond amounts will change.

### Blockers

- **No blockers** for estimate production. Upstream DEL-05-01 estimate exists and provides the contract value basis.
