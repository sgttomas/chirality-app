# Source Index

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-01-03_2026-02-04_1322 |
| **Deliverable** | DEL-01-03 BondingAndInsuranceEvidence |

---

## Source Documents (Priority Order)

### Priority 1: Explicit Pricing Sources

| Source | Location | Status | Content |
|--------|----------|--------|---------|
| Vendor quotes | N/A | NOT FOUND | No vendor quotes available for this administrative deliverable |
| Budgetary quotes | N/A | NOT FOUND | No budgetary quotes available |
| Surety rate quotes | N/A | NOT FOUND | No surety rate quotes available |

**Decision:** D-002 - No explicit pricing sources available; proceed with allowances.

---

### Priority 2: Rate Tables / Cost Libraries

| Source | Location | Status | Content |
|--------|----------|--------|---------|
| _RateTables/ | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/_RateTables/` | NOT FOUND | Directory does not exist |
| Project rate tables | N/A | NOT FOUND | No project-specific rate tables available |

**Decision:** D-002 - No rate tables available; proceed with allowances.

---

### Priority 3: Quantity Sources (Deliverable Documents)

| Source | Location | Status | Content Used |
|--------|----------|--------|--------------|
| _CONTEXT.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/_CONTEXT.md` | READ | Deliverable identification, anticipated artifacts, acceptance criteria |
| Datasheet.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/Datasheet.md` | READ | Attributes (bond types, validity period), conditions, document structure |
| Specification.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/Specification.md` | READ | Requirements REQ-01 through REQ-10, verification methods, acceptance gate |
| Guidance.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/Guidance.md` | READ | Principles, considerations, trade-offs, example documents |
| Procedure.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/Procedure.md` | READ | Steps 1-6, effort drivers, verification checkpoints, records |
| _REFERENCES.md | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-01_Compliance & Submission/1_Working/DEL-01-03_BondingAndInsuranceEvidence/_REFERENCES.md` | READ | Reference to RFP Section 5.3.1 |

---

### Priority 4: Project Context Sources

| Source | Location | Status | Content Used |
|--------|----------|--------|--------------|
| AGENTS.md | `/Users/ryan/ai-env/projects/chirality-app-test/AGENTS.md` | READ | Agent framework, project paths |
| AGENT_ESTIMATING.md | `/Users/ryan/ai-env/projects/chirality-app-test/agents/AGENT_ESTIMATING.md` | READ | Estimating protocol, spec, structure |
| RFP Document | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf` | NOT READ (PDF) | Referenced but not accessible for estimate preparation |

---

## Quantity/Cost Driver Extraction Summary

| Document | Extracted Drivers |
|----------|-------------------|
| **_CONTEXT.md** | Deliverable type (Compliance Document), responsible party (Proposal Manager), anticipated artifacts (Agreement to Bond, Bond cost statement, Insurance summary) |
| **Datasheet.md** | Bond types (performance, labor and material), validity period (60-90 days), bond cost basis (1-3% typical), surety relationship status (TBD) |
| **Specification.md** | 10 requirements defining scope; verification methods identifying responsible parties and effort |
| **Guidance.md** | Surety processing time (1-2 weeks), team considerations, trade-offs, illustrative examples |
| **Procedure.md** | 6 procedural steps with responsible parties and verification checkpoints; timeline constraints |

---

## Source-to-Line-Item Traceability

| LineID | Description | Primary Source |
|--------|-------------|----------------|
| L-001 | RFP Requirements Extraction | Procedure.md Step 1 |
| L-002 | Surety Coordination | Procedure.md Step 2; Guidance.md Principle 1 |
| L-003 | Bond Cost Statement | Procedure.md Step 3; Guidance.md Principle 2 |
| L-004 | Insurance Summary | Procedure.md Step 4 (conditional); _CONTEXT.md |
| L-005 | Package Assembly | Procedure.md Step 5 |
| L-006 | Final QC | Procedure.md Step 6; Specification.md verification table |
| L-007 | Estimator Support | Procedure.md Step 3; Specification.md REQ-07 |
| L-008 | Surety Processing Fee | Guidance.md (industry practice assumption) |
| L-009 | Insurance Broker Fee | Procedure.md Step 4 (conditional) |
| L-010 | Document Control | Procedure.md Records section |
| L-100 | Contingency | BOE.md contingency method; Decision D-004 |

---

## Missing Sources (Gaps)

| Gap | Source Expected | Impact | Resolution |
|-----|-----------------|--------|------------|
| RFP Section 5.3.1 | RFP PDF | Cannot verify specific bond/insurance requirements | Extract PDF when accessible |
| Professional services rate table | _RateTables/ | Cannot validate hourly rates | Provide rate table |
| Surety quote | External | Cannot validate surety fees | Obtain quote from surety/broker |
| Historical proposal data | Project records | Cannot benchmark effort estimates | Review past proposals |
