# Source Index

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-01-02_2026-02-04_1322 |
| **Deliverable** | DEL-01-02 FormalSubmissionPackage |

---

## Source Classification

### Priority 1: Explicit Pricing Sources (Vendor Quotes, Budgetary Quotes)

| Source | Location | Type | Applied |
|--------|----------|------|---------|
| None available | — | — | No |

**Note:** No vendor quotes or budgetary pricing found for DEL-01-02. This is expected for a proposal management deliverable (internal effort).

---

### Priority 2: Rate Tables / Cost Libraries

| Source | Location | Type | Applied |
|--------|----------|------|---------|
| None available | `_Estimates/_RateTables/` | — | No |

**Note:** `_RateTables/` directory exists but is empty. No project-specific labor rates available.

---

### Priority 3: Quantity Sources (Deliverable Documents)

| Source | Location | Content Extracted | Applied |
|--------|----------|-------------------|---------|
| **_CONTEXT.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/_CONTEXT.md` | Deliverable description, acceptance criteria, anticipated artifacts | Yes |
| **Datasheet.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Datasheet.md` | Submission parameters, execution requirements, key components list, role contingency | Yes |
| **Specification.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Specification.md` | Requirements R-01 through R-08, verification methods, compliance thresholds, TBD items | Yes |
| **Guidance.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Guidance.md` | Principles P-01 through P-05, considerations, trade-offs, examples, QA framework | Yes |
| **Procedure.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Procedure.md` | 12-step procedure (Steps 0-12), prerequisites, verification checkpoints, personnel roles | Yes |
| **_REFERENCES.md** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/_REFERENCES.md` | RFP and addenda references | Yes |

---

### Priority 4: Fallback Typical Model (Allowances)

| Source | Application | Confidence |
|--------|-------------|------------|
| Professional judgment | All line items priced using labor hour estimates x assumed rates | LOW |
| Typical proposal management effort | Effort estimates based on 12-step procedure complexity | LOW |
| Industry standard rates | Assumed rates: PM $200/hr, Graphics $125/hr, Admin $100/hr | LOW |

---

## Extracted Cost Drivers

### From Procedure.md

| Step | Driver | Extracted Quantity | Pricing Basis |
|------|--------|-------------------|---------------|
| Step 0 | Dependency verification | 20+ upstream deliverables to verify | Included in Step 2 |
| Step 1 | Content freeze coordination | 1 freeze event | 4 hours PM |
| Step 2 | File collection | 20+ deliverable files | 6 hours PM |
| Step 3 | RFP structure verification | RFP Sections 6-9 | 3 hours PM |
| Step 4 | Graphics optimization | Multiple images (Example 2: 22MB to 13MB) | 8 hours Graphics |
| Step 5 | PDF assembly | 1 PDF, TOC, bookmarks | 5 hours PM |
| Step 6 | Compliance verification | 8 requirements (R-01 to R-08) | 4 hours PM |
| Step 7 | Size check | 1 check + potential optimization | 2 hours PM |
| Step 8 | QA review | Page-by-page review, punch list | 8 hours total |
| Step 9 | Email preparation | 1 email package | 2 hours PM |
| Step 10 | Final check | Checklist + sign-off | 2 hours PM |
| Step 11 | Submission | 1 submission + monitoring | 2 hours PM |
| Step 12 | Post-submission | Archive + debrief | 2 hours PM |

### From Datasheet.md / Specification.md

| Driver | Source Section | Impact on Estimate |
|--------|----------------|-------------------|
| 15 MB size limit | Constraint C-01; R-01 | Graphics optimization effort |
| RFP Sections 6-9 order | Constraint C-02; R-02 | Structure verification effort |
| Execution requirements | Constraint C-03; R-03 | Signature collection coordination |
| Addenda acknowledgement | Constraint C-07; R-07 | Verification effort |
| 20+ upstream deliverables | Prerequisites table | File collection scope |
| Revision control | R-05 | Revision contingency allowance |

### From Guidance.md

| Driver | Source Section | Impact on Estimate |
|--------|----------------|-------------------|
| QA framework | F-003, QA dimensions | QA review scope and effort |
| Email fragility mitigation | P-05, B-004 | Submission buffer and monitoring |
| File size optimization | Example 2 | Graphics optimization approach |
| Revision scenarios | Example 1 | Revision contingency allowance |

---

## Source Reliability Assessment

| Source Type | Reliability | Notes |
|-------------|-------------|-------|
| Vendor quotes | N/A | None available |
| Rate tables | N/A | None available |
| Deliverable documents | HIGH | Well-structured, comprehensive procedure |
| Decomposition | MEDIUM | Provides context but limited cost data |
| Professional judgment | LOW | No historical baseline; typical effort assumed |

---

## Sources Not Used

| Source | Reason |
|--------|--------|
| RFP 2024_004 full text | Not directly accessible; content extracted via decomposition |
| Appendix G (Letter of Offer) | Template not accessible; not required for cost estimate |
| Appendix H | Template not accessible; not required for cost estimate |
| Addenda 01, 02, 03 | Full text not accessible; scope changes summarized in decomposition |

---

## Pricing Basis Summary

| Basis | Line Count | Amount | % of Base |
|-------|------------|--------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 15 | $10,700 | 100% |
| CONTINGENCY | 1 | $1,600 | 15% of base |
