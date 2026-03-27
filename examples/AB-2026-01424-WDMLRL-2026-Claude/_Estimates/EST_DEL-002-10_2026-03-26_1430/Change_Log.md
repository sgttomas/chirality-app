# Change Log -- EST_DEL-002-10_2026-03-26_1430

## Prior Snapshot Reference

| Field | Value |
|---|---|
| Prior RunID | EST_DEL-002-10_2026-02-26_2239 |
| Prior Total | $13,330 CAD |
| Prior Basis | PARAMETRIC |
| Prior Status | STALE (post-SCA-001) |

## Changes in This Snapshot

### 1. Basis of Estimate Changed

| Field | Prior | Current |
|---|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC | RATE_TABLE |
| FALLBACK_POLICY | ALLOW_PARAMETRIC | ALLOW_ALLOWANCE |

**Rationale:** Run brief specifies RATE_TABLE. The LOE hours x staff rates approach is classified as RATE_TABLE (not PARAMETRIC) in this run because the rates come from a defined rate table (Professional_Staff_Rates.csv). Functional pricing method is identical; classification differs per brief instruction.

### 2. CBS Codes Normalized

| Field | Prior | Current |
|---|---|---|
| CBS labels | LABOR-MGMT, LABOR-DESIGN (ad hoc) | CBS-01, CBS-02 (per CBS_Taxonomy.csv) |

**Rationale:** Prior estimate used non-canonical CBS labels. This run applies the canonical CBS_Taxonomy.csv codes (CBS-01 = Design & Engineering, CBS-02 = Project Management).

### 3. Scope Increase -- SCA-001 (Addenda 2, 3, 4)

| Change | Lines Added | Amount Added |
|---|---|---|
| Steel roof framing calculations | DL-005, DL-006 | +$3,480 |
| Precast wall panel connection design | DL-007, DL-008 | +$2,420 |
| Crane corbel design (precast panels) | DL-009 | +$1,360 |
| Interior precast wall analysis | DL-010, DL-011 | +$1,210 |
| Additional PM coordination (hybrid system) | DL-012 | +$660 |
| **Total scope increase** | **8 lines** | **+$9,130** |

### 4. Scope Trace Lines Updated

- DL-014 (Concrete Superstructure) updated to reference precast walls + steel roof
- DL-017 (Crane Support) updated to reference corbel-mounted on precast
- DL-022 (Interior Precast Walls) added as new scope trace line

### 5. No Changes to Baseline

- Baseline hours (90 hrs) and rates unchanged from prior estimate
- Baseline amount ($13,330) identical to prior estimate
- Cost Estimator hours (4 hrs) not adjusted

## Net Impact

| Metric | Prior | Current | Delta |
|---|---|---|---|
| Total | $13,330 | $22,460 | +$9,130 (+68.5%) |
| Hours | 90 | 150 | +60 (+66.7%) |
| Priced lines | 4 | 12 | +8 |
| Scope trace lines | 12 | 13 | +1 |
