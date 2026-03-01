# DEL-015-01_Power-Service Dependencies

## Dependency Status
**Tracking**: ACTIVE
**RegisterSchemaVersion**: v3.1

---

## Upstream Dependencies
- Utility company electrical service connection (external)
- Building structure and electrical room (PKG-011)
- IFC electrical design drawings (PKG-004)
- Welding equipment specifications from Owner (Camrose County)
- Utility Tie-In coordination (DEL-018-06 / SOW-0081 scope boundary)
- RFP (R-01) and Appendix B Electrical (R-05) as governing documents

## Downstream Dependencies
- DEL-015-02: Lighting Installation (requires MDP operational)
- DEL-015-03: Receptacle Installation (requires MDP operational)
- DEL-015-04: Equipment Power Circuits (requires MDP operational)
- DEL-015-05: Low-Voltage Systems (backup power / power supply consideration)
- DEL-016-01: Overhead Cranes (crane power circuits originate from this service)

---

## Extracted Dependency Register

**Total rows**: 15
**ACTIVE**: 15 | **RETIRED**: 0

### ANCHOR rows (3)

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence |
|---|---|---|---|
| DEP-015-01-A001 | IMPLEMENTS_NODE | SOW-0051 -- Provide three-phase power supply to the building | HIGH |
| DEP-015-01-A002 | TRACES_TO_REQUIREMENT | OBJ-001 -- Code-compliant facility | HIGH |
| DEP-015-01-A003 | TRACES_TO_REQUIREMENT | OBJ-005 -- Electrical systems to operational readiness | HIGH |

### EXECUTION rows (12)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-015-01-E001 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-004 -- Electrical Design | HIGH | BLOCKING |
| DEP-015-01-E002 | UPSTREAM | PREREQUISITE | EXTERNAL | Utility company three-phase service | HIGH | BLOCKING |
| DEP-015-01-E003 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-011 -- Building Construction | HIGH | BLOCKING |
| DEP-015-01-E004 | UPSTREAM | CONSTRAINT | EXTERNAL | Owner welding equipment specs | MEDIUM | ADVISORY |
| DEP-015-01-E005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-018-06 -- Utility Tie-Ins | MEDIUM | ADVISORY |
| DEP-015-01-E006 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-015-02 -- Lighting | HIGH | ADVISORY |
| DEP-015-01-E007 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-015-03 -- Receptacles | HIGH | ADVISORY |
| DEP-015-01-E008 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-015-04 -- Equipment Power | HIGH | ADVISORY |
| DEP-015-01-E009 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-015-05 -- Low-Voltage | MEDIUM | ADVISORY |
| DEP-015-01-E010 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-016-01 -- Overhead Cranes | HIGH | ADVISORY |
| DEP-015-01-E011 | UPSTREAM | CONSTRAINT | DOCUMENT | R-01 -- Main RFP | HIGH | INFO |
| DEP-015-01-E012 | UPSTREAM | CONSTRAINT | DOCUMENT | R-05 -- App B-Elec | HIGH | INFO |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- SCOPE: DEL-015-01
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to Procedure.md, Specification.md, Guidance.md, Datasheet.md)

**Paths used:**
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- DELIVERABLE_PATH: `PKG-015_Electrical & Low-Voltage Installation/1_Working/DEL-015-01_Power-Service/`
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 2026-02-25)
- _REFERENCES.md: present, used for document target resolution

**Source documents scanned (4):**
1. `Datasheet.md` -- ANCHOR_DOC (contains Identification, Attributes, Conditions, References)
2. `Procedure.md` -- EXECUTION_DOC #1 (contains explicit Prerequisites table, workflow Steps, Verification)
3. `Specification.md` -- EXECUTION_DOC #2 (contains Requirements, Scope, Verification)
4. `Guidance.md` -- EXECUTION_DOC #3 (contains Principles, Considerations, Trade-offs, Conflict Table)

**Files excluded from scan:** `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md` (generated/metadata files)

**Decomposition validation:**
- Decomposition located and used for anchor validation and label resolution.
- SOW-0051 confirmed in scope ledger: PKG-015 / DEL-015-01 / OBJ-001, OBJ-005
- OBJ-001 and OBJ-005 confirmed in objectives section.
- All downstream deliverable IDs confirmed in decomposition Section 7, PKG-015.
- DEL-018-06 confirmed in decomposition as assigned SOW-0080, SOW-0081, SOW-0082.
- PKG-004 and PKG-011 confirmed as packages in decomposition Section 6.
- DEL-016-01 confirmed in decomposition Section 7, PKG-016.

**Warnings:** None.

**Integrity check results:**
- Parent anchor (IMPLEMENTS_NODE) count: 1 -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- DependencyID uniqueness: 15 unique out of 15 -- PASS
- CSV parseable: PASS
- Enum values canonical: PASS

**Assumptions recorded:**
- SOW-0081 scope boundary between DEL-015-01 and DEL-018-06 is flagged via Conflict Table CON-015-01-004 but both deliverables are recorded. The INTERFACE relationship (DEP-015-01-E005) reflects the current ambiguity.
- Welding equipment specs (DEP-015-01-E004) are listed as ADVISORY rather than BLOCKING because the primary impact is on PKG-004 design inputs, not directly on this deliverable's installation scope.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1 2026-02-25) | None | 3 | 12 | Initial extraction. CONSUMER_CONTEXT=TASK_ESTIMATING. |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE rows (total) | 15 |
| RETIRED rows (total) | 0 |
| ANCHOR / ACTIVE | 3 |
| EXECUTION / ACTIVE | 12 |

### SatisfactionStatus breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 4 |
| TBD | 9 |
| SATISFIED | 2 |

**Notes:**
- PENDING: PKG-004 design (E001), utility service (E002), building structure (E003), welding specs (E004) -- these prerequisites are not yet satisfied.
- SATISFIED: R-01 RFP (E011) and R-05 App B-Elec (E012) -- governing documents are available and have been consumed.
- TBD: Downstream deliverables and the DEL-018-06 interface have not yet reached the phase where satisfaction can be evaluated.

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-relevant observations

1. **Three BLOCKING upstream dependencies** (DEP-015-01-E001, E002, E003) gate meaningful estimating for DEL-015-01:
   - **PKG-004 (Electrical Design):** Service voltage, ampacity, MDP sizing, and grounding design are all TBD pending IFC design. Without these, material quantities and specifications for the service entrance, MDP, conductors, and grounding system cannot be finalized. This is the single most significant estimating blocker.
   - **Utility service (External):** Utility provider identity, three-phase availability, and service connection requirements are all TBD. Utility infrastructure costs (if any) and lead times are unknown.
   - **PKG-011 (Building structure):** Electrical room dimensions and location must be confirmed before MDP sizing and installation method can be estimated.

2. **One ADVISORY upstream constraint** (DEP-015-01-E004):
   - **Welding equipment specifications (Owner):** These affect welding circuit sizing (currently estimated at 50A 240V per App B-Elec). If actual welding equipment demands differ, circuit sizing and potentially MDP capacity change. Impact on total estimate is moderate.

3. **Key TBD values affecting estimating:**
   - Service voltage (208Y/120V vs 480Y/277V) -- affects conductor sizing, transformer requirements, MDP configuration.
   - Service ampacity -- the single most critical sizing parameter; depends on PKG-004 load schedule.
   - Crane power circuit ampacity -- depends on crane selection (PKG-016).
   - HVAC/mechanical loads on MDP -- not yet enumerated on App B-Elec.
   - Spare capacity decision (20-25% margin) -- Owner decision pending.

4. **Downstream ENABLES edges** (E006-E009) indicate that all PKG-015 branch circuit deliverables depend on this service. Estimating for DEL-015-02 through DEL-015-05 should assume this service is commissioned first.

5. **Interface with PKG-016** (DEP-015-01-E010): Crane power circuit sizing feeds back into MDP capacity requirements. Crane procurement selection should be coordinated with electrical design.
