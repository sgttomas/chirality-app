# DEL-020-03: Dependencies

**Deliverable ID:** DEL-020-03_Closeout-Docs
**Dependency Tracking Status:** TRACKED
**Register Schema:** v3.1
**Last Run:** 2026-02-26

## Upstream Dependencies
- **DEL-020-01** (Commissioning): Commissioning reports must be included in closeout documentation
- **DEL-020-02** (Final-Inspection): Final inspection records and CCC must be included
- **PKG-019** (Construction Management & OH&S): Quality control records and inspection documentation
- **PKG-021** (Bonding, Insurance & Warranty): Warranty documentation to be organized

## Internal Package Dependencies
None identified beyond upstream dependencies.

## External Package Dependencies
- **PKG-021** (Bonding, Insurance & Warranty): Warranty documents incorporated into final archive

## Cross-Project Dependencies
None currently identified.

## Dependency Notes
Closeout documentation compilation occurs throughout final phases of project, collecting and organizing records from all prior deliverables. Final closeout archive represents comprehensive project record.

## Monitoring
Dependencies will be monitored through documentation collection checklist and project completion reports.

---

## Extracted Dependency Register

**Total rows:** 14 (14 ACTIVE, 0 RETIRED)
**ANCHOR rows:** 6 ACTIVE (1 IMPLEMENTS_NODE, 5 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 8 ACTIVE (4 PREREQUISITE, 2 CONSTRAINT, 2 INTERFACE)

### ANCHOR Dependencies (Pass 1 -- Tree/Definition)

| DependencyID | AnchorType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-020-03-A001 | IMPLEMENTS_NODE | WBS_NODE | PKG-020 -- Commissioning & Closeout | HIGH | ACTIVE |
| DEP-020-03-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 -- Complete all work by December 31 2026 | HIGH | ACTIVE |
| DEP-020-03-A003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-006 -- Deliver project within contract price | HIGH | ACTIVE |
| DEP-020-03-A004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0094 -- Payment claim letter | HIGH | ACTIVE |
| DEP-020-03-A005 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0095 -- WCB Letter of Clearance | HIGH | ACTIVE |
| DEP-020-03-A006 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0096 -- Statutory Declaration | HIGH | ACTIVE |

### EXECUTION Dependencies (Pass 2 -- DAG/Information Flow)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass | Status |
|---|---|---|---|---|---|---|---|
| DEP-020-03-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-020-01 Building Systems Commissioning | HIGH | ADVISORY | ACTIVE |
| DEP-020-03-E002 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-020-02 Final Inspection & CCC | HIGH | BLOCKING | ACTIVE |
| DEP-020-03-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-019-04 Construction Quality Control | HIGH | ADVISORY | ACTIVE |
| DEP-020-03-E004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-021-05 Guarantee Period Obligations | HIGH | ADVISORY | ACTIVE |
| DEP-020-03-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-008-04 As-Built Survey | MEDIUM | INFO | ACTIVE |
| DEP-020-03-E006 | UPSTREAM | CONSTRAINT | DOCUMENT | AB-2026-01424-WDMLRL_RFP.pdf (R-01) | HIGH | BLOCKING | ACTIVE |
| DEP-020-03-E007 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 Contract | HIGH | BLOCKING | ACTIVE |
| DEP-020-03-E008 | UPSTREAM | INTERFACE | EXTERNAL | WCB Alberta | HIGH | ADVISORY | ACTIVE |

---

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- ANCHOR_DOC: Datasheet.md (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (Procedure ranked first by workflow clarity heuristic)
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (present and validated)
- _REFERENCES.md: present (read-only; used for document pointer resolution)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic
- ANCHOR_DOC: AUTO -> Datasheet.md
- EXECUTION_DOC_ORDER: AUTO -> Procedure.md, Specification.md, Guidance.md

**Decomposition validation status:** AVAILABLE. Decomposition file confirmed at `_Decomposition/WDMLRL_Decomposition_Claude.md`. Used for:
- Confirming DEL-020-03 exists in PKG-020 deliverable table (Section 7)
- Confirming SOW-0094, SOW-0095, SOW-0096 mapping in scope ledger (Section 8)
- Confirming OBJ-002 and OBJ-006 objective mapping
- Resolving target deliverable IDs: DEL-020-01, DEL-020-02, DEL-019-04, DEL-021-05, DEL-008-04

**Extraction decisions:**
- Parent anchor (A001) set to PKG-020 as the package-level WBS node. The decomposition does not expose a finer-grained WBS identifier for the deliverable.
- SOW items (A004-A006) extracted as TRACES_TO_REQUIREMENT rather than additional IMPLEMENTS_NODE anchors, because SOW items represent requirements the deliverable fulfills, not the structural position in the tree.
- OBJ-002 and OBJ-006 extracted as TRACES_TO_REQUIREMENT. These are objectives the deliverable supports, confirmed in decomposition Section 7 PKG-020 table.
- DEL-020-02 (E002) marked BLOCKING for estimating because CCC issuance is the critical-path gate for the lien holdback release sequence. Without CCC timing, closeout schedule cannot be estimated.
- DEL-008-04 (E005) marked INFO for estimating: as-built survey is ASSUMPTION-scope per _CONTEXT.md broader description; the interface exists but does not gate the core SOW-0094/0095/0096 deliverables.
- RFP (E006) and CCDC 14-2013 (E007) marked BLOCKING for estimating because they define the requirements and contractual framework for the three mandatory closeout documents. Without these, scope cannot be confirmed.
- WCB Alberta (E008) marked ADVISORY: external dependency with lead time implications but does not change scope or quantities.

**Items NOT extracted (conservative filtering):**
- Design discipline packages PKG-001 through PKG-007 (as-built drawing sources): Not extracted because the as-built drawing compilation scope is ASSUMPTION-tagged and no explicit information-flow statement names specific design discipline deliverables as required inputs. The Procedure Step 5.1 references "each design discipline" generically. CONSERVATIVE strictness requires explicit identification.
- PKG-009 inspection reports/regulatory permits: Referenced in Procedure Step 8.1 archive assembly checklist but not stated as an explicit prerequisite or constraint. At CONSERVATIVE strictness, this generic archive inclusion does not meet the information-flow threshold.
- Financial reconciliation: Listed in _CONTEXT.md but no Specification requirement or Procedure step addresses it; Guidance CON-005 flags this as TBD. Not extracted.
- Downstream dependencies: No explicit downstream consumers of DEL-020-03 outputs are identified in the source documents. The deliverable produces a final archive delivered to the Owner, but no other project deliverable is stated to require DEL-020-03 output as an input.

**Warnings:** None.

**Quality check results:**
- Schema: PASS (all required columns present, CSV parseable)
- DependencyID uniqueness: PASS (14 unique IDs)
- Evidence coverage: PASS (all ACTIVE rows have EvidenceFile and SourceRef)
- Enum normalization: PASS (all values canonical)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE)
- _DEPENDENCIES.md consistency: PASS (counts match CSV)

---

## Run History

| Timestamp | Mode | Strictness | Consumer Context | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active | Retired |
|---|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE (WDMLRL_Decomposition_Claude.md) | None | 6 | 8 | 14 | 0 |

---

## Lifecycle Summary

**Extraction Lifecycle:**
- ACTIVE: 14
- RETIRED: 0

**Closure Lifecycle (SatisfactionStatus):**
- TBD: 6 (all ANCHOR rows -- satisfaction not yet assessed)
- PENDING: 8 (all EXECUTION rows -- inputs not yet received)
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are provided for downstream estimating workflows:

### Blocking Dependencies (gate estimating readiness)

1. **DEP-020-03-E002 (DEL-020-02 Final Inspection & CCC):** CCC issuance is the critical-path prerequisite for the lien holdback release package. Estimating for DEL-020-03 cannot determine the closeout submission timeline without knowing the expected CCC date. The CCC date also initiates the 2-year guarantee period (RFP Section 2.10.2). This is the single most important scheduling dependency for this deliverable.

2. **DEP-020-03-E006 (RFP -- R-01):** The RFP defines the three mandatory closeout documents and their specific requirements. The RFP is available and has been reviewed; this dependency is functionally satisfied for scope definition purposes, though the actual contractual execution depends on the executed contract.

3. **DEP-020-03-E007 (CCDC 14-2013):** The executed contract governs payment terms, holdback mechanics, and closeout obligations. The full text is not available in _Sources/ (location TBD). Until the contract text is available, payment timeline assumptions (e.g., 28-day payment per Lensing Item E-004) cannot be confirmed. Priority: obtain CCDC 14-2013 closeout and payment provisions per Lensing Item F-001.

### Advisory Dependencies (may affect quantities/approach)

4. **DEP-020-03-E001 (DEL-020-01 Commissioning):** Commissioning reports are a compilation input. Their availability affects archive completeness timing but does not change the scope of the three mandatory documents.

5. **DEP-020-03-E003 (DEL-019-04 QC Management):** QC records are a compilation input. Same impact pattern as commissioning reports.

6. **DEP-020-03-E004 (DEL-021-05 Warranty):** Warranty documentation is a compilation input from PKG-021. Same impact pattern.

7. **DEP-020-03-E008 (WCB Alberta):** External dependency with lead time. The WCB clearance request should be initiated several weeks before anticipated CCC issuance (per Guidance P-03). Lead time should be factored into the closeout schedule estimate.

### Scope Uncertainty Affecting Estimates

The decomposition explicitly maps only SOW-0094, SOW-0095, SOW-0096 to this deliverable. The broader scope (as-built drawings, O&M manuals, warranty docs, commissioning reports, archive assembly) described in _CONTEXT.md is tagged ASSUMPTION. Estimating should:
- Treat the three mandatory documents (SOW-0094/0095/0096) as the minimum confirmed scope.
- Include the broader compilation/archive scope as a likely but unconfirmed scope item pending human ruling on Conflict CON-001 in Guidance.
- Note that the broader scope primarily involves coordination and compilation effort (PM hours), not material procurement or trade labor.
