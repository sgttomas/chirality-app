# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| **Snapshot ID** | EST_DEL-01-02_2026-02-04_1322 |
| **Estimate Label** | DEL-01-02_FormalSubmissionPackage |
| **Pricing Date** | 2026-02 |
| **Currency** | CAD |
| **Deliverable** | DEL-01-02 FormalSubmissionPackage |
| **Package** | PKG-01 Compliance & Submission |
| **RUN_STATUS** | WARNINGS |

---

## Currency and Conversion

- **Currency:** CAD (Canadian Dollars)
- **Evidence:** User directive specified CAD as project currency
- **Conversion Assumptions:** N/A (single currency estimate)

**Decision:** D-001 (Currency selection)

---

## Scope Inclusions

This estimate covers the cost of producing DEL-01-02 FormalSubmissionPackage, including:

1. **Proposal Manager Labor** — Coordination, assembly, content freeze management, QA oversight, submission execution
2. **Administrative/Coordinator Labor** — File collection, content organization, graphics handling
3. **QA Review Labor** — Senior reviewer time for quality assurance
4. **PDF Assembly and Tools** — Software licensing/usage for PDF compilation, optimization
5. **Graphics Optimization** — Image compression and format conversion effort
6. **Submission Execution** — Email preparation, proof of submission retention, monitoring
7. **Contingency** — Reserve for uncertainty

### CBS Mapping

| CBS Code | Category | Applies to DEL-01-02 |
|----------|----------|---------------------|
| **E** | Engineering & Design | No |
| **PM** | Project Management / EPCM | Yes (Proposal Management) |
| **P** | Procurement | No |
| **MAT** | Equipment & Materials | No |
| **FRT** | Freight / Logistics | No |
| **CD** | Construction Directs | No |
| **CI** | Construction Indirects | No |
| **INST** | Installation | No |
| **EI** | E&I / Controls | No |
| **COM** | Commissioning | No |
| **OHP** | Contractor OH&P | No |
| **CONT** | Contingency | Yes |
| **ESC** | Escalation | No (mode=NONE) |
| **TAX** | Taxes | Excluded |

**Decision:** D-002 (CBS mapping to PM)

---

## Scope Exclusions

This estimate does NOT cover:

1. **Upstream Content Creation** — All proposal content (DEL-02 through DEL-09) is excluded; covered by separate deliverables
2. **Compliance Matrix Development** — DEL-01-01 is a separate deliverable
3. **Bonding and Insurance** — DEL-01-03 is a separate deliverable
4. **Post-Submission Activities** — Evaluation response, contract negotiation, interviews
5. **Owner's Costs** — Town of Penhold internal effort
6. **Taxes** — GST/PST excluded from this estimate
7. **Escalation** — Mode set to NONE per default

**Decision:** D-003 (Scope exclusions)

---

## Contracting Assumptions

- **Delivery Model:** Internal proposal management by Design-Build proponent
- **Responsibility:** Proposal Manager role within bidding organization
- **No external contractor pricing:** This is in-house effort for proposal preparation

**ASSUMPTION:** A-001 (Internal labor model)

---

## Location/Productivity Assumptions

- **Location:** Alberta, Canada (Penhold area)
- **Work Type:** Office-based proposal management
- **Productivity:** Standard office productivity assumed; no site work involved

**ASSUMPTION:** A-002 (Office-based work)

---

## Pricing Sources Hierarchy

This estimate uses the following priority for pricing:

| Priority | Source Type | Applied |
|----------|-------------|---------|
| 1 | Vendor Quotes | None available |
| 2 | Rate Tables | None available in _RateTables/ |
| 3 | Allowances | Yes — All line items |

**Decision:** D-004 (Allowance-based pricing)

All line items are priced using professional judgment allowances based on:
- Typical proposal management effort for Design-Build RFPs
- Scope complexity inferred from the 4 documents
- 12-step procedure with multiple QA gates

---

## Indirects Model

- **Model:** Factor-based (embedded in labor allowances)
- **Rationale:** Proposal management is inherently indirect cost; no separate indirects line

**Decision:** D-005 (Indirects embedded in PM)

---

## Contingency Method and Rationale

- **Method:** PCT_BY_BUCKET (default)
- **Contingency Rate:** 15% of base estimate
- **Rationale:** High uncertainty due to:
  - No rate tables available
  - No historical data for similar deliverables
  - Allowance-heavy estimate
  - TBD items in source documents (submission email address, RFP heading structure, etc.)

**Decision:** D-006 (Contingency at 15%)

---

## Escalation Method

- **Mode:** NONE (default)
- **Rationale:** Proposal preparation occurs within a short timeframe before Aug 30, 2024 deadline; no escalation adjustment required

**Decision:** D-007 (No escalation)

---

## Rounding Policy

- **Rounding:** Nearest $100 CAD
- **Rationale:** Appropriate precision for allowance-based proposal management estimate

**Decision:** D-008 (Rounding to $100)

---

## Completeness Metrics Summary

| Metric | Value |
|--------|-------|
| % Lines Priced by QUOTE | 0% |
| % Lines Priced by RATE_TABLE | 0% |
| % Lines Priced by ALLOWANCE/PARAMETRIC | 100% |
| % Deliverables with Explicit Quantities | 0% (quantities are labor hours, estimated) |
| Overall Confidence | LOW |

---

## Known Gaps

1. **No rate tables available** — All pricing is allowance-based
2. **TBD items in source documents** — Submission email address, RFP Section 6-9 exact headings, execution requirements by entity type
3. **No vendor quotes** — Software/tools assumed as existing overhead
4. **Effort estimation** — Based on typical proposal management without historical baseline

---

## References

- **Decision Log:** `Decision_Log.md` (this snapshot)
- **Assumptions Log:** `Assumptions_Log.md` (this snapshot)
- **Source Index:** `Source_Index.md` (this snapshot)
- **Deliverable Documents:**
  - `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Datasheet.md`
  - `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Specification.md`
  - `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Guidance.md`
  - `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-02_FormalSubmissionPackage/Procedure.md`
