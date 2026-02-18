# Run Context — EST_DEL-07-02_2026-02-18_2130

## Run Identification

- **RunID:** EST_DEL-07-02_2026-02-18_2130
- **AsOf:** 2026-02-18T21:30:00-07:00
- **Agent:** ESTIMATING (Type 2)

---

## Inputs (as provided)

- **Scope:** DEL-07-02
- **ScopeResolvedSummary:** 1 deliverable in scope; 0 excluded; 0 blocked
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-02_KeyTeamMembersAndResumes`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/`
- **BASIS_OF_ESTIMATE:** RATE_TABLE
- **CURRENCY:** CAD
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- **DEPENDENCY_SOURCES:** AUTO (resolved to `DEL-07-02_KeyTeamMembersAndResumes/Dependencies.csv`)
- **PRICE_SOURCES:**
  1. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv`
  2. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv`
  3. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv`

---

## Resolved Defaults

- **OUTPUT_LABEL:** DEL-07-02
- **UPDATE_LATEST_POINTER:** FALSE
- **FALLBACK_POLICY:** STRICT
- **ALLOW_MIXED_METHODS:** FALSE
- **Rounding:** DOLLAR

---

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-07-02 | PKG-03 | `PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-02_KeyTeamMembersAndResumes` | TRUE | Key Team Members and Resumes |

---

## Decomposition Confirmation

- **Decomposition found:** YES
- **DEL-07-02 confirmed in decomposition:** YES (Section 8: DEL-07-02_KeyTeamMembersAndResumes; Package PKG-03)
- **SOW mapping:** SOW-017 (Provide key member resumes and roles)
- **Objective mapping:** OBJ-006 (Demonstrate a strong team & firms)

---

## CBS Mapping Rule

CBS codes assigned deterministically based on role category from `Professional_Staff_Rates.csv`:
- `Administrative` category roles -> CBS = `ADMIN`
- This is a proposal-production deliverable; all line items are labour hours.

---

## Warnings

- None.
