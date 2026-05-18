# Evaluation Protocol — AB-2026-01424 WDMLRL Example Project

This protocol evaluates the example project as a demonstration of the Chirality agent instruction architecture. It assesses whether the agent system's outputs conform to the design basis (DBM) and whether the project content is faithful to the source material (RFP and addenda).

**References governing this evaluation:**
- `docs/DBM_Agent_Instruction_Architecture.md` — Design basis for agent behavior and outputs
- `docs/SE_Design_Analysis.md` — SE disciplines the architecture claims to realize
- `_Sources/` — Ground truth (RFP, addenda, appendices)
- `_Decomposition/WDMLRL_Decomposition_Claude.md` — Basis for all downstream work

**Data sources for this evaluation:**
- SA-1 through SA-7 collection reports (decomposition, coordination, structure, dependencies, estimates, reconciliation, aggregation)
- 117 content digests in `_Evaluation/content-digests/`

---

## Dimension 1: Decomposition Fidelity (I1-I10)

**Question:** Does the decomposition faithfully and completely capture the source material?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| D-1.1 | Every RFP scope item has a corresponding SOW entry | Cross-reference RFP sections 3.1-3.4 against SSOW in decomposition | No RFP requirement omitted; omissions documented as OUT with rationale |
| D-1.2 | No invented scope items (I2) | Verify each SOW item cites a source reference | Every SOW item traces to RFP text or appendix |
| D-1.3 | Partitions are flat (I3) | Inspect package hierarchy | No nested packages; all PKGs at same level |
| D-1.4 | No overlap / no gaps (I4) | Check ledger: every IN-scope item assigned to exactly one PKG | Zero unassigned items; zero multi-assigned items |
| D-1.5 | Stable identifiers (I5) | Compare R1 vs R2 decomposition IDs | No ID renumbering between revisions |
| D-1.6 | Deterministic ID coupling (I6) | Verify DEL-XXX-YY first 3 digits match PKG-XXX | 100% conformance |
| D-1.7 | Objective mapping (I7) | Check all 8 objectives mapped to supporting packages | Zero unmapped objectives |
| D-1.8 | Vocabulary Map exists (I10) | Check for vocabulary section with canonical terms | Present with 15+ terms |
| D-1.9 | Ledger + telemetry present (I9) | Check for machine-checkable ledger and coverage metrics | Both present; metrics internally consistent |
| D-1.10 | Addenda incorporation | Verify SCA-001 (Addenda 2,3,4) changes reflected in R2 | Scope items added/modified per addenda content |

### Data Sources
- SA-1 decomposition report
- Decomposition document (direct read)
- RFP and addenda PDFs (spot-check)

---

## Dimension 2: Source Faithfulness

**Question:** Does the project content accurately reflect what the RFP actually says?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| S-2.1 | Building program completeness | Compare RFP Section 3.4 building program against DEL content | All RFP-stated spaces, systems, and features accounted for in deliverables |
| S-2.2 | Dimensional accuracy | Spot-check key dimensions (13,000 sq ft, 130'x100', 35' ceiling, 50,000L cistern, 100 LPM pump) across content digests | Consistent with RFP; deviations flagged as ASSUMPTION |
| S-2.3 | Contractual terms preserved | Check CCDC 14-2013, completion deadline (Dec 31 2026), variable-price foundation, County fee responsibility | Correctly stated in deliverable documents |
| S-2.4 | Addenda changes propagated | Verify Addendum 4 changes (precast walls, folding doors, corbel cranes, mezzanine railing) appear in affected deliverables | Changes reflected in _CONTEXT.md amendments and dependency refreshes |
| S-2.5 | No hallucinated requirements | Sample 10-15 deliverable specifications; verify requirements trace to RFP text | Requirements cite RFP sections; no unsourced mandatory requirements |
| S-2.6 | TBDs where RFP is silent | Verify that items not specified in RFP are marked TBD, not invented | TBD labels present for unspecified parameters |

### Data Sources
- RFP PDF (sections 1-4)
- Addenda PDFs
- Content digests (sampled)
- Decomposition vocabulary map

---

## Dimension 3: Structural Conformance (DBM Section 3)

**Question:** Do agent outputs follow the structural template mandated by the design basis?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| T-3.1 | Deliverable folder minimum fileset | SA-3 structure audit results | 117/117 have _STATUS, _CONTEXT, _DEPENDENCIES, _REFERENCES |
| T-3.2 | Document kit completeness | SA-3 results | 117/117 have Datasheet, Specification, Guidance, Procedure (state >= INITIALIZED) |
| T-3.3 | _SEMANTIC.md coverage | SA-3 results | Count of deliverables with semantic lens |
| T-3.4 | _MEMORY.md presence | SA-3 results | Count and assess whether absence is a violation or expected |
| T-3.5 | Package subfolder structure | SA-3 results | All 21 packages have 0_References, 1_Working, 2_Checking, 3_Issued |
| T-3.6 | Tool root presence | Filesystem check | _Aggregation, _Coordination, _Decomposition, _Estimates, _EstimatePrep, _Reconciliation, _Sources present |
| T-3.7 | Snapshot immutability pattern (R4) | SA-5 results | Estimate snapshots are timestamped folders; reruns create new folders |
| T-3.8 | _LATEST.md pointers | SA-5, SA-7 results | Present where required; point to most recent snapshot |

### Data Sources
- SA-3 structure audit
- SA-5 estimate audit
- SA-7 aggregation audit

---

## Dimension 4: Dependency Quality (DBM Section 9)

**Question:** Are dependency registers schema-compliant, complete, and evidence-backed?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| Q-4.1 | Schema conformance (v3.1) | SA-4 results | All Dependencies.csv have 29+ required columns |
| Q-4.2 | IMPLEMENTS_NODE anchor presence | SA-4 results | Every deliverable has at least one |
| Q-4.3 | Evidence coverage (K-PROV-1) | SA-4 results | 100% of rows have EvidenceFile populated |
| Q-4.4 | Enum validity | SA-4 results | All enum fields use canonical values per TYPES.md |
| Q-4.5 | Dependency graph coherence | SA-6 DepClosure results | Orphan count = 0; SCCs documented with remediation path |
| Q-4.6 | Bidirectional consistency | SA-6 results | Bidirectional pairs identified; no contradictory direction claims |
| Q-4.7 | Hub analysis | SA-6 results | High-degree nodes identified and explainable by project structure |

### Data Sources
- SA-4 dependency schema audit
- SA-6 reconciliation (DepClosure) report

---

## Dimension 5: Evidence-First Epistemology (DBM Section 11.2)

**Question:** Do agent outputs distinguish fact from inference and surface uncertainty?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| E-5.1 | TBD labeling for unknowns (K-INVENT-1) | Sample content digests | Missing values labeled TBD, not guessed |
| E-5.2 | ASSUMPTION flagging | Sample content digests | Inferred values explicitly labeled ASSUMPTION with rationale |
| E-5.3 | Conflict surfacing (K-CONFLICT-1) | Sample content digests | Conflicts produce Conflict Tables with HumanRuling = TBD |
| E-5.4 | Source citations in specifications | Sample Specification.md files | Requirements cite RFP sections or appendix references |
| E-5.5 | Lensing enrichment annotations | Sample content digests | Enrichment markers (A-001, B-001, etc.) flag decision points |
| E-5.6 | No silent resolution of ambiguity | Sample Guidance.md files | Ambiguities escalated to human, not resolved by agent |

### Data Sources
- Content digests (sampled across disciplines)
- Direct reads of selected deliverable files

---

## Dimension 6: Lifecycle and Control Loop (DBM Sections 6, 11.6)

**Question:** Is lifecycle state consistent and is the control loop infrastructure present?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| L-6.1 | Lifecycle state validity | SA-3 results | All states are valid enum values per TYPES.md |
| L-6.2 | Lifecycle state consistency | SA-3 results | State matches file inventory (e.g., SEMANTIC_READY implies _SEMANTIC.md exists) |
| L-6.3 | Coordination representation declared | SA-2 results | _COORDINATION.md exists with valid mode |
| L-6.4 | Session handoff artifacts | SA-2 results | Assess whether NEXT_INSTANCE_STATE.md absence is expected at this project stage |
| L-6.5 | _STATUS.md history integrity | Sample _STATUS.md files | History section shows forward-only transitions with timestamps and actors |

### Data Sources
- SA-2 coordination report
- SA-3 structure audit
- Direct reads (sampled)

---

## Dimension 7: Estimation and Aggregation Pipeline (DBM Section 9.4)

**Question:** Do estimate and aggregation outputs follow the snapshot contract and produce internally consistent results?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| A-7.1 | Estimate snapshot structure | SA-5 results | All sampled snapshots contain Summary.md, Detail.csv, QA_Report.md |
| A-7.2 | Estimate coverage | SA-5 results | Snapshots exist for all 117 deliverables |
| A-7.3 | Rerun handling | SA-5 results | Reruns create new timestamped folders; originals preserved |
| A-7.4 | Aggregation QA | SA-7 results | Grand total balanced; 0 schema issues, 0 conflicts, 0 duplicates |
| A-7.5 | SCA-001 delta tracking | SA-7 results | Aggregation correctly identifies changed deliverables and computes deltas |
| A-7.6 | BOE presence | SA-5 results | BASIS_OF_ESTIMATE.md exists in EstimatePrep snapshots |
| A-7.7 | Estimate-to-aggregation consistency | SA-5 + SA-7 results | Aggregated total = sum of individual estimate snapshots |

### Data Sources
- SA-5 estimate audit
- SA-7 aggregation audit

---

## Dimension 8: Reconciliation and Coverage Verification (DBM Section 6)

**Question:** Do reconciliation outputs confirm structural and dependency integrity?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| R-8.1 | Decomposition coverage | SA-6 DecompCoverage results | 100% forward and reverse coverage; 0 orphan folders |
| R-8.2 | Context fidelity | SA-6 results | _CONTEXT.md fields match decomposition for all 117 deliverables |
| R-8.3 | Objective coverage | SA-6 results | All 8 objectives mapped to at least one package |
| R-8.4 | SCA-001 regression check | SA-6 results (PRE vs POST) | No regressions; improvements documented |
| R-8.5 | Dependency closure status | SA-6 DepClosure results | Overall status documented; SCC cycle explained |

### Data Sources
- SA-6 reconciliation audit (both DecompCoverage and DepClosure)

---

## Dimension 9: Cross-Deliverable Content Coherence

**Question:** Are deliverables internally consistent with each other across packages?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| C-9.1 | Design-to-construction traceability | Sample design PKGs (001-009) → construction PKGs (010-018) | Construction deliverables reference their design predecessors |
| C-9.2 | Cross-discipline interface consistency | Check interfaces at architectural/structural/MEP boundaries | Interface dependencies are bidirectional and non-contradictory |
| C-9.3 | Vocabulary consistency | Sample deliverables for canonical term usage | Terms match Vocabulary Map; no semantic drift |
| C-9.4 | Shared parameter consistency | Check key parameters (building dimensions, equipment specs, code references) across packages | Consistent values; deviations flagged |
| C-9.5 | Scope boundary clarity | Check deliverables with documented scope conflicts | Conflicts have Conflict Table entries with proposed resolution |

### Data Sources
- Content digests (cross-package comparison)
- Decomposition vocabulary map

---

## Dimension 10: SE Property Realization (SE_Design_Analysis.md)

**Question:** Does the project demonstrate the SE properties the architecture claims?

### Checks

| ID | Check | Method | Pass Criteria |
|----|-------|--------|---------------|
| SE-10.1 | Fault containment | Verify deliverable-local agents wrote only within their folders | No cross-deliverable contamination |
| SE-10.2 | Traceability chain | Trace a sample deliverable from SOW item → package → deliverable → doc kit → dependency register | Complete chain with no broken links |
| SE-10.3 | Configuration baseline | Verify SCA-001 change propagation | Changes tracked in decomposition, reflected in affected _CONTEXT.md, dependency registers refreshed |
| SE-10.4 | V-model coverage | Decomposition (left leg) verified by coverage audit (right leg) | AUDIT_DECOMP passes; coverage telemetry at 100% |
| SE-10.5 | Human authority preservation | Check that no agent output claims to approve, certify, or issue | All proposals labeled PROPOSAL; approvals reserved for human |

### Data Sources
- All SA reports
- Content digests
- Reconciliation reports

---

## Scoring Framework

Each dimension is scored on a 4-level scale:

| Score | Meaning |
|-------|---------|
| **EXEMPLARY** | All checks pass; outputs exceed minimum requirements; demonstrates mature practice |
| **CONFORMANT** | All mandatory checks pass; minor observations noted |
| **PARTIAL** | Most checks pass; some gaps or inconsistencies that do not compromise structural integrity |
| **NON-CONFORMANT** | Mandatory checks fail; structural integrity compromised |

**Overall project score** is the lowest dimension score (weakest-link principle), with narrative assessment for nuance.

---

## Execution Plan

The evaluation will be executed in three phases:

### Phase A: Automated Checks (data already collected)
Dimensions 3, 4, 6, 7, 8 — these can be scored directly from SA-1 through SA-7 reports.

### Phase B: Source Verification (requires PDF reads)
Dimensions 1, 2 — requires reading RFP sections and cross-referencing against decomposition and deliverable content.

### Phase C: Content Quality Assessment (requires digest analysis)
Dimensions 5, 9, 10 — requires systematic analysis of content digests for epistemological quality, cross-deliverable coherence, and SE property demonstration.

---

EOF
