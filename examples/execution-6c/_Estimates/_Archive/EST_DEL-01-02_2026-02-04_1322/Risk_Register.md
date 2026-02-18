# Risk Register

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-01-02_2026-02-04_1322 |
| **Deliverable** | DEL-01-02 FormalSubmissionPackage |
| **Contingency Method** | PCT_BY_BUCKET |
| **Contingency Amount** | $1,600 CAD (15% of base) |

---

## Risk Entries

### R-001: Upstream Deliverable Delays

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Risk Driver** | Schedule / Interface |
| **Cause** | Upstream deliverables (DEL-02 through DEL-09) are late or incomplete |
| **Consequence** | Content freeze delayed; compressed assembly timeline; increased overtime; potential errors |
| **Affected CBS/WBS** | PM / PKG-01 |
| **Suggested Mitigation** | Establish firm content freeze deadline 48 hours before submission; communicate consequences to content owners; identify critical path items early |
| **Contingency Handling** | Revision contingency (A-017, $1,000) partially covers rework; overtime premium not included |

---

### R-002: File Size Non-Compliance

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Risk Driver** | Scope / Productivity |
| **Cause** | Final PDF exceeds 15MB after optimization attempts |
| **Consequence** | Additional optimization cycles required; content may need to be removed; potential quality degradation |
| **Affected CBS/WBS** | PM / L-004, L-007 |
| **Suggested Mitigation** | Set 12MB target with 3MB buffer; optimize images before assembly (not after); use vector formats where possible |
| **Contingency Handling** | Graphics optimization hours (A-006) may be insufficient; contingency provides buffer |

---

### R-003: Signature/Execution Delays

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Risk Driver** | Interface / Schedule |
| **Cause** | Authorized signatory unavailable for final execution; seal requirements unclear |
| **Consequence** | Submission delayed; proposal may be disqualified if not properly executed |
| **Affected CBS/WBS** | PM / L-006, L-010 |
| **Suggested Mitigation** | Identify signatory and backup early (Datasheet.md role contingency); prepare execution pages separately; confirm seal requirements with RFP |
| **Contingency Handling** | Time risk, not cost risk; contingency does not specifically cover this |

---

### R-004: Email Submission Failure

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Risk Driver** | Interface / Productivity |
| **Cause** | Email submission fails due to server limits, spam filters, network issues, or incorrect address |
| **Consequence** | Proposal not received by Town; potential disqualification if not resolved before deadline |
| **Affected CBS/WBS** | PM / L-011 |
| **Suggested Mitigation** | Test email submission in advance; submit with 1-hour buffer before deadline; monitor for confirmation; have backup submission plan |
| **Contingency Handling** | Guidance.md P-05 provides escalation protocol; resubmission effort covered by revision contingency (A-017) |

---

### R-005: TBD Items Unresolved

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Risk Driver** | Scope |
| **Cause** | TBD items in source documents (submission email address, RFP heading structure, execution requirements) not resolved before assembly |
| **Consequence** | Assembly blocked or incorrect; rework required after resolution |
| **Affected CBS/WBS** | PM / L-003, L-006 |
| **Suggested Mitigation** | Follow TBD Resolution Plan in Specification.md; resolve all TBD items 7 days before content freeze |
| **Contingency Handling** | Rework effort covered by revision contingency (A-017) |

---

### R-006: QA Review Scope Creep

| Field | Value |
|-------|-------|
| **Risk ID** | R-006 |
| **Risk Driver** | Scope / Productivity |
| **Cause** | QA review identifies significant issues requiring content changes, not just assembly corrections |
| **Consequence** | QA review extends beyond 8 hours; content owners must make changes; reassembly required |
| **Affected CBS/WBS** | PM / L-008 |
| **Suggested Mitigation** | Define QA scope clearly (assembly quality, not content quality); upstream deliverables should be QA'd before handoff |
| **Contingency Handling** | Content changes are upstream scope; assembly rework covered by revision contingency |

---

### R-007: Labor Rate Variance

| Field | Value |
|-------|-------|
| **Risk ID** | R-007 |
| **Risk Driver** | Price |
| **Cause** | Assumed labor rates (PM $200/hr, Graphics $125/hr, Admin $100/hr) differ from actual rates |
| **Consequence** | Estimate under/over-stated by rate variance percentage |
| **Affected CBS/WBS** | All PM line items |
| **Suggested Mitigation** | Confirm actual rates with project accounting; provide rate tables for future estimates |
| **Contingency Handling** | 15% contingency provides buffer for moderate rate variance (+/- 15%) |

---

### R-008: Revision Cycle Required

| Field | Value |
|-------|-------|
| **Risk ID** | R-008 |
| **Risk Driver** | Scope / Quality |
| **Cause** | Errors discovered after initial submission requiring resubmission before deadline |
| **Consequence** | Additional assembly, QA, and submission effort; compressed timeline for revision |
| **Affected CBS/WBS** | PM / L-015 |
| **Suggested Mitigation** | Robust QA process (Step 8); submit with time buffer (1:00 PM vs 2:00 PM deadline) |
| **Contingency Handling** | Revision contingency (A-017, $1,000) specifically covers one revision cycle |

---

## Risk Summary

| ID | Risk Driver | Likelihood | Impact | Handling |
|----|-------------|------------|--------|----------|
| R-001 | Upstream delays | Medium | High | Mitigation + partial contingency |
| R-002 | File size | Medium | Medium | Mitigation + contingency |
| R-003 | Signature delays | Low | High | Mitigation (time risk) |
| R-004 | Email failure | Low | High | Mitigation + escalation protocol |
| R-005 | TBD unresolved | Medium | Medium | Mitigation + contingency |
| R-006 | QA scope creep | Low | Medium | Mitigation + upstream scope |
| R-007 | Rate variance | Medium | Medium | Contingency buffer |
| R-008 | Revision needed | Medium | Medium | Explicit revision allowance |

---

## Contingency Allocation

| Category | Contingency $ | Rationale |
|----------|---------------|-----------|
| General estimate uncertainty | $1,000 | 100% allowance-based pricing; no historical baseline |
| Rate variance buffer | $300 | Assumed rates may differ +/- 15% |
| Unforeseen rework | $300 | QA issues, TBD resolution complications |
| **Total Contingency** | **$1,600** | 15% of base estimate |

Note: Revision contingency (A-017, $1,000) is a separate line item in base estimate, not part of the 15% contingency.
