# Estimate Summary -- DEL-002-10 Structural Calculation Package

**RunID:** EST_DEL-002-10_2026-03-26_1430
**Date:** 2026-03-26T14:30:00Z
**Basis of Estimate:** RATE_TABLE (primary) + ALLOWANCE (SCA-001 scope adjustments)
**Currency:** CAD
**Prior Estimate:** EST_DEL-002-10_2026-02-26_2239 ($13,330 CAD -- STALE)

---

## Basis of Estimate Used

| Field | Value |
|---|---|
| Primary Method | RATE_TABLE -- hours x rate from Professional_Staff_Rates.csv + Level_of_Effort.csv |
| Supplement Method | ALLOWANCE -- hour adjustments for SCA-001 scope changes (Add. 2, 3, 4) |
| Hours Source (baseline) | Level_of_Effort.csv (parametric hour allocations by deliverable and role -- pre-SCA-001) |
| Hours Source (adjustments) | Allowance estimates based on structural engineering judgment of scope change impact |
| Rates Source | Professional_Staff_Rates.csv (parametric hourly rates by role, CAD) |
| Confidence Level | MED (baseline lines); LOW (allowance adjustment lines) |
| Fallback Policy | ALLOW_ALLOWANCE (used for SCA-001 scope increase items) |
| Mixed Methods | TRUE -- RATE_TABLE baseline + ALLOWANCE scope adjustments |

---

## Totals by Package / Deliverable / CBS

### By Package

| Package | Amount (CAD) |
|---|---|
| PKG-002 -- Structural Design | 22,460 |
| **Total** | **22,460** |

### By Deliverable

| Deliverable | Amount (CAD) |
|---|---|
| DEL-002-10 -- Structural Calculation Package | 22,460 |
| **Total** | **22,460** |

### By CBS

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| CBS-01 | Design & Engineering | 20,270 | 90.3% |
| CBS-02 | Project Management | 2,190 | 9.7% |
| **Total** | | **22,460** | **100.0%** |

### By Role

| RoleID | Role | Hours (Baseline) | Hours (Allowance) | Hours (Total) | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|---|---|
| R-01 | Project Manager | 6 | 4 | 10 | 165 | 1,650 | 7.3% |
| R-08 | Cost Estimator | 4 | 0 | 4 | 135 | 540 | 2.4% |
| R-13 | BIM Technician | 24 | 14 | 38 | 95 | 3,610 | 16.1% |
| R-14 | Structural Engineer | 56 | 42 | 98 | 170 | 16,660 | 74.2% |
| | **Total** | **90** | **60** | **150** | | **22,460** | **100.0%** |

### By Method

| Method | Line Items (priced) | Amount (CAD) | % of Total |
|---|---|---|---|
| RATE_TABLE | 4 | 13,330 | 59.4% |
| ALLOWANCE | 8 | 9,130 | 40.6% |
| **Total** | **12** | **22,460** | **100.0%** |

---

## Delta vs. Prior Estimate

| Metric | Prior (EST_DEL-002-10_2026-02-26_2239) | Current | Delta | Delta % |
|---|---|---|---|---|
| Total Amount | $13,330 | $22,460 | +$9,130 | +68.5% |
| Total Hours | 90 | 150 | +60 | +66.7% |
| Structural Engineer Hours | 56 | 98 | +42 | +75.0% |
| BIM Technician Hours | 24 | 38 | +14 | +58.3% |
| PM Hours | 6 | 10 | +4 | +66.7% |

### Drivers of Change

| Driver | Source | Impact (CAD) | Impact (hrs) |
|---|---|---|---|
| Steel roof framing calculations (new scope) | Add. 2, Add. 4 | +$3,480 | +24 hrs |
| Precast wall panel connection design (new scope) | Add. 2, Add. 4 | +$2,420 | +16 hrs |
| Crane corbel design in precast panels (new scope) | Add. 4, Q3 | +$1,360 | +8 hrs |
| Interior precast wall analysis (new scope) | Add. 4, Q5 | +$1,210 | +8 hrs |
| Additional PM coordination for hybrid system | Add. 2, Add. 4 | +$660 | +4 hrs |
| **Total Scope Change Impact** | | **+$9,130** | **+60 hrs** |

---

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-002-10)
- **Documents read:** 5 (Datasheet, Specification, Guidance, Procedure, Dependencies.csv)
- **Structural subsystems traced:** 9 (Concrete Superstructure [precast walls + steel roof], Foundation, Mezzanine, Crane Support [corbel-mounted], Steel Plate Embedments, Service Pit, Wash Bay, Stairs, Interior Precast Walls [new])
- **Procedural activities traced:** 4 (Design Kickoff, Internal QA Review, Discipline Coordination, P.Eng. Stamp)
- **Pricing coverage:** 100% (12 of 12 priced line items; 13 scope-trace lines at $0)

---

## Key Warnings and Coverage Gaps

1. **Mixed-method estimate.** Baseline hours are RATE_TABLE (MED confidence); SCA-001 scope adjustments are ALLOWANCE (LOW confidence). The allowance portion ($9,130, 40.6% of total) carries +/-30-50% accuracy.
2. **LOE.csv not updated for SCA-001.** The Level_of_Effort.csv baseline hours (90 hrs) were prepared before Addenda 2/3/4. The +60 hrs allowance adjustment is an estimator judgment that should be validated against actual design effort as the project progresses.
3. **Hybrid structural system complexity.** The precast walls + steel roof system is materially more complex to calculate than monolithic concrete. The allowance hours assume a competent structural engineering team familiar with both precast concrete (CSA A23.3) and structural steel (CSA S16) design. If the team requires additional learning/reference time, actual hours may exceed the estimate.
4. **Foundation reconciliation effort not separately estimated.** The LOE baseline includes foundation calculation hours on a normal ground conditions basis. If geotech (DEL-008-01) reveals conditions requiring significant foundation redesign, additional hours beyond this estimate will be needed.
5. **Crane reconciliation effort not separately estimated.** The corbel design allowance (DL-009) covers initial design using conservative 5-tonne class parameters. If crane procurement data (DEL-016-01) requires significant revision, additional hours may be needed.
6. **No material or equipment costs.** This is a professional engineering labor deliverable only.
7. **SCC bundle note:** DEL-002-10 is in an SCC bundle with DEL-002-01 (Preliminary Structural Design). There may be overlapping coordination effort.
