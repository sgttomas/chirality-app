# Guidance: DEL-11.05 Marine Loading Installation & Test Records

## Purpose

This guidance document supports the development of **Marine Loading Installation & Test Records** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Provides evidence of completion, inspection, and testing for the marine loading system, demonstrating compliance with specification requirements and readiness for operation.

**Classification:** Record deliverable under the Process discipline (QA/QC responsibility), produced by the D&B Contractor.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — records verify safety-critical systems function as designed
- **OBJ-2 Throughput Capacity** — records verify equipment meets design capacity
- **OBJ-4 Operational Flexibility** — records verify operating envelope meets specification
- **OBJ-7 Environmental Protection** — records verify leak detection and containment are functional

## Principles

**Engineering rationale (Process discipline — installation and test records):**

1. **Evidence-based verification:** Records are objective evidence that the installed system meets specification requirements. They must be complete, accurate, and traceable to defined acceptance criteria.

2. **Traceability chain:** Each record must link to: equipment tag → test procedure → acceptance criteria (from DEL-11.02 or ER) → actual result → pass/fail determination.

3. **Safety-critical focus:** Loading arm ERC, leak detection, and ESD integration are safety-critical functions. Records for these systems require particular attention to witness requirements, calibration, and acceptance criteria.

4. **Turnover readiness:** The records package forms part of the turnover documentation demonstrating mechanical completion and commissioning readiness.

**ASSUMPTION:** ER defines witness/hold-point requirements and testing expectations (clause references **TBD**).

**Applicable standards context:**
- IEC 61511 — SIS testing requirements (leak detection/ESD) — **TBD**
- Project ITP — inspection and test plan — **TBD**
- Project QA/QC procedures — record format and control — **TBD**

## Cross-Document Alignment Notes

| Alignment Check | Datasheet.md | Specification.md | Procedure.md |
|-----------------|--------------|------------------|--------------|
| Record types | §Construction (record tables) | §Requirements (FAT/INS/COM) | §Steps |
| Equipment tags | §Interfaces | §Related Deliverables | §Prerequisites |
| Acceptance criteria | §Deliverable Acceptance | §Verification | §Verification |
| Interface records | §Interfaces | §Interface Requirements | §Steps |

**Cross-deliverable verification:**
- FAT records verify OEM equipment meets DEL-11.02 §4, §5, §6 requirements
- Installation records verify as-installed matches DEL-11.01 IFC drawings
- Functional test records verify DEL-11.02 §9 commissioning requirements
- Leak detection test records verify DEL-11.02 §6 alarm/ESD integration

Where acceptance criteria references are not available, keep them explicitly **TBD** and do not substitute typical criteria.

## Considerations

**Factors to consider during records development:**

### FAT Record Considerations
- OEM FAT scope should be agreed during procurement (DEL-11.06)
- Witness requirements (Contractor, Employer) per project ITP
- ERC activation test is safety-critical — ensure witnessed and documented
- Calibration certificates for test instruments required

### Installation Record Considerations
- Mechanical completion checklists should cover all scope items
- As-installed verification against IFC drawings catches construction deviations
- Torque values and alignment data required for rotating equipment
- Weld inspection records for double-walled pipe per DEL-11.02

### Commissioning Record Considerations
- Functional tests should exercise all operating modes (normal, emergency)
- Leak detection loop tests should include simulated leak and alarm/ESD verification
- ESD integration tests require coordination with PKG-29 SIS team
- All safety-critical tests should be witnessed per project ITP

### General Records Quality
- Use controlled ITR forms per project QA/QC
- Ensure all signatures are legible with date
- Track punch list items to closure before turnover
- Maintain calibration certificates current through test period

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| FAT scope vs. SAT scope | Extensive FAT at OEM (reduces site work) | Minimum FAT, full SAT on site | Balance travel/witness cost against site schedule |
| Witness requirements | Witness all hold points | Witness safety-critical only | Follow project ITP; ensure ERC and ESD tests are witnessed |
| Punch list closure timing | Close all before turnover | Accept minor items open | Safety-critical items must be closed; minor items per punch list protocol |
| Record format | Paper originals | Electronic records | Follow project document control; ensure archival compliance |

## Examples

**Reference examples and precedents:**

Anticipated record packages (from decomposition):

| Record Package | Key Content | Source Reference |
|----------------|-------------|------------------|
| FAT records | Loading arm, ERC, leak detection, sump pump FAT | DEL-11.06 OEM data, DEL-11.02 §9 |
| Installation records | Mechanical completion, as-installed verification | DEL-11.01 IFC drawings, project ITP |
| Leak detection test records | Loop tests, alarm verification, ESD integration | DEL-11.02 §6, PKG-19/29 |

**Typical record structure:**
1. Record ID and title
2. Equipment tag and location
3. Test/inspection procedure reference
4. Acceptance criteria reference (ER clause, code, specification section)
5. Test date and conditions
6. Measured/observed results
7. Pass/fail determination
8. Signatures (originator, witness, approver)
9. Attachments (calibration certs, photos, as applicable)

**Employer's Requirements expectations:** **TBD** until clause references are provided.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when specific ER clauses define testing requirements and any discrepancies with OEM FAT scope or project ITP are identified.*

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified cross-document alignment table: All 4 alignment checks confirmed accurate
  - Record types: 3 categories consistent (FAT, installation, commissioning)
  - Equipment tags: Flow from DEL-11.04 datasheets
  - Acceptance criteria: Trace to DEL-11.02 §9
  - Interface records: Cover PKG-19/20/29/03 interfaces
- Verified all 4 Principles link to evidence-based verification, traceability chain, safety-critical focus, turnover readiness
- Verified 4 Considerations sections cover FAT, installation, commissioning, and general quality
- Verified 4 Trade-offs reference appropriate testing decisions
- Verified Examples table lists 3 record packages with source references
- Verified typical record structure (9 elements) provides standard format
- Verified cross-deliverable verification: DEL-11.02 §4/5/6/9, DEL-11.01 IFC, DEL-11.06 OEM
- Confirmed Conflict Table ready for use
- All TBDs and ASSUMPTIONs retained with explicit source citations
- Pass 3 complete — document ready for WORKING_ITEMS session
