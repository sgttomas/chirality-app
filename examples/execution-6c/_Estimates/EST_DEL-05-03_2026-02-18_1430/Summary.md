# Estimate Summary: DEL-05-03 Pricing Narrative & Assumptions

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **Currency** | CAD |
| **Rounding** | DOLLAR |
| **Fallback Policy** | STRICT |
| **Mixed Methods** | FALSE |
| **Snapshot** | EST_DEL-05-03_2026-02-18_1430 |

---

## Deliverable Context

DEL-05-03 is a **T4 narrative deliverable** under PKG-02 (Financial Proposal). It documents the pricing assumptions, allowances, exclusions, addenda impacts, and value alternatives that underpin the construction pricing in Schedule A (DEL-05-01) and Schedule B (DEL-05-02). This is a pure proposal production cost -- no construction pricing content is embedded in this deliverable.

**Cost ownership (per BOE):** Pricing narrative and assumptions writing belongs to DEL-05-03. Construction pricing COMPILATION is in DEL-05-01/05-02. Value alternatives analysis is in DEL-05-03.

---

## Production Cost Summary

| LineID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | Method |
|---|---|---|---|---|---|
| L-001 | R-02 Project Manager | 12 | $175 | $2,100 | RATE_TABLE |
| L-002 | R-18 Estimator (Senior) | 8 | $145 | $1,160 | RATE_TABLE |
| | **Total** | **20 hrs** | | **$3,260** | |

---

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| MGMT | Production -- Management (PM) | $2,100 | 1 |
| FIN | Production -- Financial (Estimator) | $1,160 | 1 |
| **TOTAL** | | **$3,260** | **2** |

---

## Scope Coverage

- Deliverables in scope: 1 (DEL-05-03)
- Deliverables priced: 1
- Deliverables blocked: 0
- Deliverables with TBD amounts: 0

---

## PKG-02 Context (Upstream Estimates)

| Deliverable | Production Cost | Construction Content | Grand Total |
|---|---|---|---|
| DEL-05-01 (Schedule A) | $9,960 | $10,729,000 | $10,738,960 |
| DEL-05-02 (Schedule B) | $6,020 | $10,729,000 | $10,735,020 |
| **DEL-05-03 (Pricing Narrative)** | **$3,260** | **N/A** | **$3,260** |
| **PKG-02 Production Cost Total** | **$19,240** | | |

Schedule A and Schedule B construction pricing content is reconciled at $10,729,000 (base $9,863,000 + options $355,000 + GST $511,000). DEL-05-03 does not carry construction pricing content -- it documents the narrative and assumptions underlying those figures.

---

## Key Observations

1. **Pure production cost deliverable**: DEL-05-03 is 20 hours of PM and estimator time to write the pricing narrative. No construction pricing content is embedded. This is the smallest of the 3 PKG-02 deliverables by cost.

2. **PM-led effort**: The Project Manager carries 60% of the hours (12 of 20). This reflects the narrative's scope -- allowances, exclusions, value alternatives, and cross-deliverable coordination -- which require PM-level commercial judgment rather than detailed estimating.

3. **Estimator hours focused on assumptions documentation**: The 8 hours of R-18 Senior Estimator time are for documenting the pricing basis, quantity assumptions, market pricing date, and parametric methodology that underpin the Schedule A/B figures.

4. **Heavy upstream dependency network**: Dependencies.csv identifies 6 upstream deliverable interfaces (DEL-05-01, DEL-05-02, DEL-02-01, DEL-02-02, DEL-04-01, DEL-08-01, DEL-09-02) plus RFP and Addendum 03 constraints. All are ADVISORY except DEL-05-01/05-02 and RFP which are BLOCKING for narrative consistency.

5. **Cross-deliverable coordination scope**: The PM hours account for coordination across pricing (DEL-05-01/02), concept design (DEL-02-01), design brief (DEL-02-02), construction methodology (DEL-04-01), schedule (DEL-08-01), and site conditions (DEL-09-02).

6. **PKG-02 production cost split**: DEL-05-01 ($9,960 / 72 hrs) > DEL-05-02 ($6,020 / 44 hrs) > DEL-05-03 ($3,260 / 20 hrs). Total PKG-02 production cost is $19,240 / 136 hours. The narrative is the lightest-touch deliverable because it describes and contextualizes pricing produced elsewhere.

---

## Key Warnings and Blockers

### Warnings

1. **W-001**: OI-004 (FF&E treatment) is formally OPEN per decomposition. Upstream estimates assume $20,000 cash allowance as Additional Option 6. This narrative must document the FF&E assumption clearly. If OI-004 resolution differs, the narrative must be updated.
2. **W-002**: All upstream construction pricing content (DEL-05-01/05-02) is PARAMETRIC with no vendor quotes. The pricing narrative must acknowledge the parametric basis and associated accuracy range (+/-20-50%).
3. **W-003**: Level-of-effort hours are PARAMETRIC planning estimates (not actual tracked hours). Confidence is MEDIUM with +/-20-30% accuracy per INDEX.md Data Quality Statement.
4. **W-004**: Value alternatives analysis (SOW-028) is scoped to DEL-05-03 per cost ownership rules. The PM hours must cover this analysis within the 12-hour allocation. If value alternatives require significant engineering input, additional discipline hours may be needed.

### Blockers

- **No blockers** for estimate production. All pricing sources (staff rates + level of effort) are available and sufficient for RATE_TABLE method.
- DEL-05-01 and DEL-05-02 BLOCKING dependencies (DEP-05-03-004, DEP-05-03-005) are resolved for estimating purposes -- the pricing figures from those estimates are available for narrative reference.
