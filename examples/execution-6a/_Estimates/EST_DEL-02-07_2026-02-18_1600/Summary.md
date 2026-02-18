# Estimate Summary — DEL-02-07 Emergency Power & Backup Generator

**Snapshot:** EST_DEL-02-07_2026-02-18_1600
**Date:** 2026-02-18
**Currency:** CAD
**Rounding:** DOLLAR

---

## Basis of Estimate

| Field | Value |
|---|---|
| **Requested Basis** | QUOTE |
| **Actual Method Used** | ALLOWANCE (fallback) |
| **Reason for Fallback** | No vendor quote exists. FALLBACK_POLICY=ALLOW_ALLOWANCE permitted the fallback. |
| **Primary Pricing Source** | Equipment_Pricing.csv / EQ-04 (parametric system price) |
| **Confidence** | LOW (all line items) |

All amounts in this snapshot should be treated as budget allowances pending vendor quote replacement.

---

## Estimate Total

| Description | Amount (CAD) |
|---|---|
| **DEL-02-07 Total** | **$201,000** |

---

## Breakdown by CBS

| CBS | Description | Amount (CAD) | Lines | Method |
|---|---|---|---|---|
| 26-EMRG-GEN | Generator Equipment + Installation | $162,000 | 2 | ALLOWANCE |
| 26-EMRG-DIST | Emergency Distribution to Essential Loads | $18,000 | 1 | ALLOWANCE |
| 26-EMRG-DOOR | Door Backup Mechanism Integration | $16,000 | 1 | ALLOWANCE |
| 26-EMRG-DES | Generator-Specific Design Fees | $5,000 | 1 | ALLOWANCE |
| **TOTAL** | | **$201,000** | **5** | |

---

## Breakdown by Line Item

| LineID | Description | Amount (CAD) |
|---|---|---|
| L-0207-010 | Diesel generator system (complete) | $150,000 |
| L-0207-020 | Emergency power distribution to essential loads | $18,000 |
| L-0207-030 | Overhead door backup power mechanism (8 doors) | $16,000 |
| L-0207-040 | Generator installation labour (incremental) | $12,000 |
| L-0207-050 | Electrical engineering design fees (generator portion) | $5,000 |

---

## Scope Coverage

| Metric | Value |
|---|---|
| **Deliverables in scope** | 1 (DEL-02-07) |
| **Line items produced** | 5 |
| **Scope items covered** | SOW-0222 (primary); SOW-0216 (backup mechanism aspects) |
| **Exclusions applied** | Normal power distribution (DEL-02-06); main panels/feeders (DEL-02-06); pad site prep/grading (DEL-03-02); fuel piping beyond tank |

---

## Key Warnings and Blockers

1. **No vendor quote available.** All pricing is ALLOWANCE fallback from parametric sources. Vendor quotes should replace these allowances before finalizing.

2. **72-hour runtime unconfirmed (PP-26).** Owner has not confirmed the runtime requirement. Fuel tank sizing and potentially generator capacity depend on this. If runtime increases beyond 72 hours, the $150,000 generator system allowance may be insufficient.

3. **AHJ seismic ruling pending (DEP-0207-E009).** If seismic anchorage is required, an additional $3,000-$8,000 may be needed for anchorage hardware and engineering. Not currently included.

4. **Door backup mechanism type TBD.** The $16,000 allowance assumes $2,000/door for 8 doors. Actual mechanism (battery backup vs generator-fed circuit) will affect cost.

5. **Potential double-count risk on distribution and installation.** EQ-04 system price includes "distribution to essential loads" and "commissioning." Lines L-0207-020 and L-0207-040 may partially overlap. When vendor quote is obtained, verify scope boundaries carefully.

6. **Design fee allocation.** The $5,000 design fee (L-0207-050) may overlap with overall electrical engineering fees in DEL-02-06. Confirm allocation during design coordination.

---

## Range Analysis (for context)

Using the min/max ranges from Equipment_Pricing.csv and assumptions:

| Scenario | Amount (CAD) | Notes |
|---|---|---|
| **Low** | $160,000 | EQ-04 min ($120k) + distribution ($15k) + doors ($12k) + labour ($8k) + design ($5k) |
| **Recommended (this estimate)** | $201,000 | EQ-04 recommended ($150k) + distribution ($18k) + doors ($16k) + labour ($12k) + design ($5k) |
| **High** | $255,000 | EQ-04 max ($180k) + distribution ($22k) + doors ($24k) + labour ($18k) + design ($6k) + seismic ($5k) |

This range does not account for scope changes (e.g., expanded essential loads list, redundant generators, or significantly different runtime requirements).
