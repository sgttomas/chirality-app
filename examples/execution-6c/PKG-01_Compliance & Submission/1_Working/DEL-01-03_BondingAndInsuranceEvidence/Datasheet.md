# Datasheet: DEL-01-03 Bonding and Insurance Evidence

## Identification

| Property | Value |
|----------|-------|
| **Deliverable ID** | DEL-01-03 |
| **Name** | BondingAndInsuranceEvidence |
| **Type** | Compliance Document |
| **Package** | PKG-01 Compliance & Submission |
| **Discipline** | Proposal Management |
| **Responsible Party** | Proposal Manager |

**Source:** `_CONTEXT.md`

---

## Attributes

### Agreement to Bond (Proposal Stage)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Purpose** | Demonstrate surety capacity and commitment at proposal stage | **ASSUMPTION** (standard RFP practice) |
| **Format** | Letter from surety company or broker confirming capacity | **TBD** (RFP §5.3.1; specific format requirements not yet extracted) |
| **Required Content** | Confirmation of willingness to bond if proposal is accepted | **TBD** (RFP §5.3.1; content requirements not yet extracted) |
| **Bond Types Required** | Performance bond, labor and material payment bond | **ASSUMPTION** (typical for Design-Build projects; adequate evidence pending RFP §5.3.1 extraction) — *[B-003]* |
| **Bond Amounts** | **TBD** (RFP §5.3.1 or contract value percentage; essential fact requiring extraction) | **location TBD** — *[B-001]* |
| **Validity Period** | 60-90 days post-submission (must cover proposal evaluation period) | **ASSUMPTION** (Guidance Example 1; Procedure Step 2) — *[B-002]* |
| **Surety Relationship Status** | **TBD** (existing relationship vs. new establishment — affects timeline) | Proposal Manager to confirm — *[F-005]* |

### Project Identification Attributes (for Agreement to Bond letter)

| Attribute | Value | Source |
|-----------|-------|--------|
| **RFP Number** | 2024_004 | RFP title — *[B-004]* |
| **Project Name** | Penhold Public Services Building Design-Build Services | RFP title — *[B-004]* |
| **Owner Name** | Town of Penhold | RFP — *[B-004]* |
| **Anticipated Contract Value Range** | **TBD** (Estimator/Commercial Lead to provide for surety capacity confirmation) | Required for surety capacity determination — *[D-003, B-004]* |

### Regulatory Direction (RFP §5.3.1)

| Attribute | Value | Source |
|-----------|-------|--------|
| **Specific Regulatory Directions** | **TBD**: What are the specific regulatory directions from RFP §5.3.1 governing bonding and insurance at proposal stage? | RFP §5.3.1 (PDF extraction needed) — *[A-001]* |

### Bond Cost Inclusion Statement

| Attribute | Value | Source |
|-----------|-------|--------|
| **Purpose** | Confirm that bond costs are included in proposal pricing | Decomposition document (SOW-004 notes, line 314) |
| **Integration Point** | Must align with Appendix H Schedule A/B pricing | Decomposition document (DEL-05-01, DEL-05-02) |
| **Cost Basis** | 1-3% of contract value (canonical reference point) | Industry norms; Guidance Principle 2; Procedure Step 3 — *[B-005]* |
| **Inclusion Scope** | Base price plus additional options (if bonded) | **ASSUMPTION** (needs verification from RFP §5.3.1) |

### Insurance Approach Summary

| Attribute | Value | Source |
|-----------|-------|--------|
| **Purpose** | Demonstrate insurance capacity "as required" | `_CONTEXT.md` (anticipated artifacts) |
| **Insurance Types** | **TBD** (RFP §5.3.1 or contract terms; essential fact requiring extraction) | **location TBD** — *[B-001]* |
| **Minimum Coverage Amounts** | **TBD** (RFP requirements; essential fact requiring extraction) | **location TBD** — *[B-001]* |
| **Certificate Requirements** | **TBD** (proposal stage vs. contract stage; essential fact requiring extraction) | **location TBD** — *[B-001]* |

---

## Conditions

### Normal Conditions (Proposal Stage)

- Agreement to Bond is a **proposal-stage commitment**, not a final bond issuance
- Surety must be licensed to operate in Alberta (regulatory body: **TBD** — see C-004 normalization note; Specification references "Financial Services Regulatory Authority of Alberta" but name requires verification) — *[C-004]*
- **ASSUMPTION:** Standard surety prequalification applies

### Design Conditions

- Document must satisfy mandatory compliance requirement (OBJ-001)
- Must support pricing credibility (OBJ-007)
- **Source:** Decomposition document (scope traceability, line 22 of `_CONTEXT.md`)

### Limiting Conditions

- **High compliance risk item** identified in decomposition (Section 11, line 348)
- Failure to include Agreement to Bond **will result in proposal disqualification** (absolute evidentiary mandate; "may" language inappropriate for high-risk mandatory compliance item — RFP §5.3.1 to confirm mandatory vs. discretionary disqualification) — *[E-001]*
- Bond cost exclusion from pricing may affect competitiveness or compliance
- **Source:** Decomposition document (coverage & telemetry snapshot)

---

## Construction

### Document Structure

- **Agreement to Bond:** Standalone letter on surety letterhead (or broker confirmation letter)
- **Bond Cost Inclusion Statement:** Integrated narrative or table showing cost breakdown and inclusion in pricing
- **Insurance Approach Summary:** Brief narrative (as required)
- **ASSUMPTION:** Structure based on typical proposal compliance practice

### Integration Points

- Must be referenced in formal submission package (DEL-01-02)
- Bond costs must reconcile with Appendix H pricing (DEL-05-01, DEL-05-02)
- **Source:** Decomposition document (deliverable definitions, lines 171-174)

---

## References

1. **Primary:**
   - `_CONTEXT.md` — Deliverable identity, acceptance criteria, anticipated artifacts
   - Decomposition document (`Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`) — DEL-01-03 definition (lines 171-174), SOW-004 (line 277), scope ledger (line 314)

2. **Governing:**
   - RFP §5.3.1 — Agreement to Bond requirements and bond cost inclusion (**location TBD**; PDF not accessible)
   - `_REFERENCES.md` — Points to RFP source file

3. **Related Deliverables:**
   - DEL-01-02 (Formal Submission Package) — Integrates this deliverable
   - DEL-05-01 (Appendix H Schedule A) — Bond costs must be included
   - DEL-05-02 (Appendix H Schedule B) — Detailed cost breakdown including bond costs

---

## Notes

- **Missing Information:** RFP §5.3.1 details not accessible (PDF read failed); specific bond percentages, insurance types, and certificate requirements marked **TBD**
- **Assumptions Labeled:** Bond types, format expectations, and cost basis inferred from standard practice
- **Compliance Priority:** High-risk compliance item; requires careful verification against RFP §5.3.1 when PDF becomes accessible
