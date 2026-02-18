# Estimate Summary: DEL-03-04 Site Utilities Distribution & Allowance-Based Tie-Ins

## Run Identification

| Field | Value |
|-------|-------|
| Snapshot | EST_DEL-03-04_2026-02-18_2100 |
| Deliverable | DEL-03-04 -- Site Utilities Distribution & Allowance-Based Tie-Ins |
| Package | PKG-003 -- Site & Civil Works |
| Basis of Estimate | RATE_TABLE (primary) + ALLOWANCE (tie-ins per DEC-004 and connection fees) |
| Currency | CAD |
| Rounding | DOLLAR |
| RUN_STATUS | WARNINGS |

## Estimate Total

| Category | Amount (CAD) | Method | Line Count |
|----------|-------------|--------|------------|
| On-site utility distribution (RATE_TABLE) | $149,200 | RATE_TABLE | 11 |
| Civil design fees -- utility routing | $3,730 | RATE_TABLE | 1 |
| **Subtotal RATE_TABLE** | **$152,930** | RATE_TABLE | 12 |
| Municipal tie-in allowance (DEC-004) | $35,000 | ALLOWANCE | 1 |
| Utility connection fees | $39,000 | ALLOWANCE | 5 |
| **Subtotal ALLOWANCE** | **$74,000** | ALLOWANCE | 6 |
| **GRAND TOTAL** | **$226,930** | MIXED | **18** |

## Totals by CBS

| CBS | Description | Amount (CAD) |
|-----|-------------|-------------|
| 31.00 | Site Utilities -- Design | $3,730 |
| 31.40 | Site Utilities -- Water Distribution | $41,000 |
| 31.41 | Site Utilities -- Sanitary Sewer Distribution | $31,000 |
| 31.42 | Site Utilities -- Gas Distribution | $16,800 |
| 31.43 | Site Utilities -- Power Distribution | $38,400 |
| 31.44 | Site Utilities -- Telecom Distribution | $12,000 |
| 31.45 | Site Utilities -- Common Trench | $10,000 |
| 31.49 | Site Utilities -- Tie-In Allowance (DEC-004) | $35,000 |
| 31.50 | Site Utilities -- Utility Connection Fees | $39,000 |
| **TOTAL** | | **$226,930** |

## Dual-Method Breakdown

This is a dual-method deliverable as specified in the brief:

1. **Method=RATE_TABLE ($152,930 / 67%):** Design coordination hours and on-site distribution piping/conduit from municipal tie-in points to buildings. Covers CBS 31.00 through 31.45. Rates from Underground_Utility_Rates.csv (UU-01 through UU-09) and Professional_Design_Fees.csv (DF-02).

2. **Method=ALLOWANCE ($74,000 / 33%):** Tie-in execution labor/materials at municipal stubs per DEC-004 ($35,000) plus utility connection fees from providers ($39,000). Covers CBS 31.49 and 31.50. Values from UU-12 and FP-11 through FP-15.

## Key Warnings and Blockers

### Warnings

1. **DEC-004 ALLOWANCE VALUE PENDING OWNER CONFIRMATION:** The $35,000 tie-in allowance uses UU-12 recommended value. The Owner has not pre-set this value (DEC-004 states "no value pre-set"). Owner must confirm or DB must propose the allowance amount.

2. **UTILITY RUN LENGTHS ARE ASSUMED:** All distribution quantities are based on assumed distances from municipal stubs to buildings (ASM-001: 120 m to PSB; ASM-002: 40 m branch to Cold Storage). Actual lengths depend on post-award survey files (DEP-03-04-007) and underground services drawings (DEP-03-04-006).

3. **COLD STORAGE UTILITY REQUIREMENTS PARTIALLY TBD:** Water service to Cold Storage (ASM-004, L-0304-02/04) and absence of sanitary service to Cold Storage (ASM-005) are assumptions pending design confirmation.

4. **CONNECTION FEES AT RECOMMENDED VALUES:** Utility connection fees (FP-11 through FP-15) are carried at recommended parametric values. Actual fee schedules from Town of Penhold and providers are TBD.

5. **MIXED METHODS USED:** 12 lines at RATE_TABLE, 6 lines at ALLOWANCE. Authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE.

### Blockers (from Dependency Evidence)

| Blocker | DependencyID | Status | Impact on Estimate |
|---------|-------------|--------|-------------------|
| Owner-provided underground services drawings | DEP-03-04-006 | PENDING | Run lengths are assumed; actual survey data could materially change distribution quantities |
| Survey files from civil engineering firm | DEP-03-04-007 | PENDING | Same as above; site layout confirmation needed |
| Town of Penhold municipal servicing standards | DEP-03-04-009 | PENDING | May affect connection specifications and fees |
| Utility Provider connection standards | DEP-03-04-010 | PENDING | May affect connection method and costs |

### Cost Ownership Verification

| Scope Area | Included? | Notes |
|-----------|-----------|-------|
| On-site utility distribution (pipe/conduit from tie-in point to 1.5m outside buildings) | YES | L-0304-01 through L-0304-11 |
| Utility tie-in to municipal stubs (DEC-004 allowance) | YES | L-0304-12 |
| Civil design fees for utility routing | YES | L-0304-18 |
| Utility connection fees/permits | YES | L-0304-13 through L-0304-17 |
| Building service ENTRY (from 1.5m outside to interior) | NO | Owned by PKG-002 (DEL-02-05/DEL-02-06) |
| Bulk earthwork/trenching for utility corridors | NO (included in pipe rate) | UU rates are all-inclusive; bulk earthwork owned by DEL-03-02 |
| Stormwater management | NO | Owned by DEL-03-02 |
