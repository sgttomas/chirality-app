# Source Index

## Snapshot Identification

| Attribute | Value |
|---|---|
| **Snapshot ID** | EST_DEL-05-03_2026-02-04_1323 |
| **Deliverable** | DEL-05-03 Pricing Narrative and Assumptions |

---

## Source Discovery Summary

| Category | Sources Found | Priority |
|---|---|---|
| Explicit Pricing Sources (quotes, proposals) | 0 | N/A |
| Rate Tables / Cost Libraries | 0 | N/A |
| Quantity Sources | 5 | PRIMARY |
| Embedded Fallback Model | 1 | FALLBACK |

---

## Primary Sources (Quantity and Scope)

### 1. _CONTEXT.md

| Field | Value |
|---|---|
| **Source Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/_CONTEXT.md |
| **Type** | Deliverable context metadata |
| **Relevance** | Defines deliverable identity, acceptance criteria, scope traceability |
| **Used For** | Establishing deliverable scope and acceptance criteria |
| **Priority** | PRIMARY |

---

### 2. Datasheet.md

| Field | Value |
|---|---|
| **Source Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/Datasheet.md |
| **Type** | Deliverable datasheet |
| **Relevance** | Defines document attributes, conditions, content structure, key narrative elements |
| **Used For** | Extracting narrative section structure (8 canonical sections); identifying TBD items |
| **Priority** | PRIMARY |

**Key Extractions:**
- Content Structure: 8 sections (Introduction, Addenda Integration, Base Scope Assumptions, Exclusions, Allowances, Additional Options, Value Alternatives, Pricing Assumptions)
- Key Narrative Elements: 6 TBD items requiring estimator input
- Conditions: Addenda acknowledgement, scope exclusions, allowance treatment, FF&E treatment, Additional Options, Value Alternatives

---

### 3. Specification.md

| Field | Value |
|---|---|
| **Source Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/Specification.md |
| **Type** | Deliverable specification |
| **Relevance** | Defines requirements R-1 through R-10; verification methods; acceptance criteria |
| **Used For** | Pricing verification effort (L-011); understanding compliance requirements |
| **Priority** | PRIMARY |

**Key Extractions:**
- 10 requirements (R-1 through R-10) requiring verification
- Verification responsibility: Estimator/Commercial Lead + Proposal Manager
- Cross-document consistency requirements (R-8)

---

### 4. Guidance.md

| Field | Value |
|---|---|
| **Source Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/Guidance.md |
| **Type** | Deliverable guidance |
| **Relevance** | Provides principles, considerations, trade-offs, and examples for narrative production |
| **Used For** | Understanding complexity and effort drivers; example content templates |
| **Priority** | SECONDARY |

**Key Extractions:**
- 5 principles (source fidelity, addenda integration, allowances, exclusions, value alternatives)
- 5 considerations (timing, market conditions, site access, procurement lead times, design consistency)
- 3 trade-offs (detail vs. page budget, conservatism vs. competitiveness, allowances vs. fixed pricing)
- 5 examples (addenda acknowledgement, allowance statement, exclusion statement, value alternative, pricing assumptions)

---

### 5. Procedure.md

| Field | Value |
|---|---|
| **Source Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/Procedure.md |
| **Type** | Deliverable procedure |
| **Relevance** | Defines production workflow (8 steps), prerequisites, verification checkpoints |
| **Used For** | Pricing effort breakdown; understanding workflow and dependencies |
| **Priority** | PRIMARY |

**Key Extractions:**
- 8 production steps (Review Context, Review Schedules, Draft Narrative, Cross-Reference Schedules, Cross-Reference Related Deliverables, Review Against Specification, Final Review, Update Status)
- Prerequisites: 7 input deliverables (decomposition, DEL-05-01, DEL-05-02, DEL-02-01, DEL-04-01, DEL-08-01, DEL-09-01, DEL-09-02)
- Verification checkpoints: 8 process verification + final content verification

---

## Rate Tables and Cost Libraries

| Source | Status | Notes |
|---|---|---|
| _RateTables/ directory | EMPTY | No rate tables available |
| Industry cost databases | NOT AVAILABLE | No RS Means or equivalent provided |
| Historical project data | NOT AVAILABLE | No comparable project data provided |

**Impact:** All pricing based on allowances due to absence of rate data. Confidence = LOW.

---

## Explicit Pricing Sources

| Source | Status | Notes |
|---|---|---|
| Vendor quotes | NOT AVAILABLE | Not applicable for professional services narrative production |
| Budgetary quotes | NOT AVAILABLE | N/A |
| Proposals | NOT AVAILABLE | N/A |
| Budget sheets | NOT AVAILABLE | N/A |

---

## Fallback Model

| Model | Applied | Notes |
|---|---|---|
| Embedded Typical Model | YES | Professional services rate assumption (~$150/hr) based on Alberta market |
| Allowance-based pricing | YES | All line items priced as LS allowances |
| Default contingency | YES | 15% PCT_BY_BUCKET applied |

---

## Source Traceability Matrix

| Line ID | Primary Source | Section/Element | Confidence |
|---|---|---|---|
| L-001 | Datasheet.md | Content Structure - Section 1 | LOW |
| L-002 | Datasheet.md | Content Structure - Section 2 | LOW |
| L-003 | Datasheet.md | Content Structure - Section 3 | LOW |
| L-004 | Datasheet.md | Content Structure - Section 4 | LOW |
| L-005 | Datasheet.md | Content Structure - Section 5 | LOW |
| L-006 | Datasheet.md | Content Structure - Section 6 | LOW |
| L-007 | Datasheet.md | Content Structure - Section 7 | LOW |
| L-008 | Datasheet.md | Content Structure - Section 8 | LOW |
| L-009 | Specification.md | R-8 (Consistency with Schedules A/B) | LOW |
| L-010 | Procedure.md | Step 5 (Cross-Reference Related Deliverables) | LOW |
| L-011 | Specification.md | Requirements R-1 through R-10 | LOW |
| L-012 | Procedure.md | Step 7 (Final Review and Approval) | LOW |
| L-013 | Procedure.md | Step 7 (Document Integration) | LOW |
| L-100 | D-005 | Contingency decision | LOW |

---

## Recommendations

1. **Provide rate tables** in `_RateTables/` for professional services hourly rates (estimator, commercial lead, proposal manager)
2. **Add historical data** from comparable proposal production efforts if available
3. **Track actuals** during DEL-05-03 production to build internal rate data for future estimates

---

**Source Index Completed:** 2026-02-04 13:23
