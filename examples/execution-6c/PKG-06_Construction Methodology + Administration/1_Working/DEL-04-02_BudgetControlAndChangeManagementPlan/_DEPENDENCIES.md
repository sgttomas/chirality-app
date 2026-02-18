# Dependencies: DEL-04-02 Budget Control and Change Management Plan

## Dependency Tracking Mode
- **Mode:** TRACKED (extracted via DEPENDENCIES agent run 2026-02-18)
- **Prior mode:** NOT_TRACKED (dependencies previously coordinated externally by humans per original _DEPENDENCIES.md)
- **Notes:** Dependencies below are extracted from source documents and registered in Dependencies.csv. The prior NOT_TRACKED designation reflected proposal-phase coordination practice; this run upgrades the register to full extraction per AGENT_DEPENDENCIES.md PROTOCOL.

---

## Declared Dependencies

### Upstream (I need these before I can proceed)
- DEL-05-01: Appendix H Schedule A — budget baseline input (Procedure HOLD POINT 1)
- DEL-05-02: Appendix H Schedule B — cost code structure input (Procedure HOLD POINT 1)
- DEL-05-03: Pricing Narrative and Assumptions — change pricing consistency (Procedure HOLD POINT 2)
- DEL-04-03: Communications and Reporting Plan — reporting cadence coordination (REQ-8)
- DEL-08-01: Detailed Project Schedule — schedule integration context (REQ-8)
- DEL-09-01: Risk Register and Mitigation Plan — contingency allocation input (REQ-7, REQ-8)
- DEL-04-01: Construction Methodology Narrative — construction approach context (Guidance §Key Integration Points)
- RFP Section 7: Normative governing requirements (Specification §Standards)
- Addendum 03: Scope and cost clarifications required for baseline (REQ-10, Tier 1 Inviolable)

### Downstream (These need me)
- DEL-01-02: Formal Submission Package — this plan is a required component of the proposal PDF (Decomposition §15 Project Delivery Plan criterion)

---

## Extracted Dependency Register

### Summary

| Class | Direction | Count (ACTIVE) |
|-------|-----------|---------------|
| ANCHOR | UPSTREAM | 3 |
| EXECUTION | UPSTREAM | 8 |
| EXECUTION | DOWNSTREAM | 1 |
| **Total ACTIVE** | | **12** |
| RETIRED | | 0 |

### Compact Table (ACTIVE rows)

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|---|
| DEP-04-02-A001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | DEL-04-02 | DEL-04-02 (PKG-06 node) | HIGH | TBD |
| DEP-04-02-A002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-020 | SOW-020 Budget control + change management narrative | HIGH | TBD |
| DEP-04-02-A003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-002 | OBJ-002 Maximize Project Delivery Plan score | HIGH | TBD |
| DEP-04-02-E001 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-01 | DEL-05-01 Appendix H Schedule A Pricing Summary | HIGH | PENDING |
| DEP-04-02-E002 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-02 | DEL-05-02 Appendix H Schedule B Cost Breakdown | HIGH | PENDING |
| DEP-04-02-E003 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-03 | DEL-05-03 Pricing Narrative and Assumptions | HIGH | PENDING |
| DEP-04-02-E004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-03 | DEL-04-03 Communications and Reporting Plan | HIGH | PENDING |
| DEP-04-02-E005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-08-01 | DEL-08-01 Detailed Project Schedule | MEDIUM | PENDING |
| DEP-04-02-E006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 | DEL-09-01 Risk Register and Mitigation Plan | HIGH | PENDING |
| DEP-04-02-E007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 | DEL-04-01 Construction Methodology Narrative | MEDIUM | PENDING |
| DEP-04-02-E008 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | DEL-01-02 Formal Submission Package | HIGH | PENDING |
| DEP-04-02-E009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | — | RFP Section 7 Requirements | HIGH | PENDING |
| DEP-04-02-E010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | — | Addendum 03 Scope and Cost Clarifications | HIGH | PENDING |

---

## Run Notes

### Run Configuration
- **Run date:** 2026-02-18
- **MODE:** UPDATE (overwrite)
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO — scanned deliverable folder; all present documents read
- **ANCHOR_DOC (chosen):** Datasheet.md (contains explicit identification, WBS/package references, related deliverables)
- **EXECUTION_DOC_ORDER (chosen):** Specification.md, Procedure.md, Guidance.md, _CONTEXT.md, _REFERENCES.md, _SEMANTIC.md
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- **Decomposition status:** LOCATED AND READ — anchor validation performed against decomposition §6, §7, §8, §10, §15

### Defaults Applied
- `RegisterSchemaVersion`: v3.1 (set on all rows)
- `FirstSeen`/`LastSeen`: 2026-02-18 (initial extraction run)
- `Status`: ACTIVE for all extracted rows
- `SatisfactionStatus`: TBD for ANCHOR rows; PENDING for EXECUTION rows

### Anchor Validation Notes
- DEL-04-02 confirmed in decomposition §8 as the canonical deliverable definition node under PKG-06.
- SOW-020 confirmed in decomposition §10 Scope Ledger (maps to DEL-04-01 in scope ledger row, but _CONTEXT.md explicitly states SOW-020 as the scope item for DEL-04-02; decomposition §7 PKG-06 lists SOW-020 as one of the scope items: SOW-019, SOW-020, SOW-021 for PKG-06 covering DEL-04-01, DEL-04-02, DEL-04-03).
  - ASSUMPTION noted: SOW-020 as labelled in decomposition §10 states "Construction admin narrative" (cleaning, transportation, site services) which maps to DEL-04-01 per the scope ledger. However, _CONTEXT.md explicitly assigns SOW-020 to DEL-04-02. The _CONTEXT.md explicit assignment is used as authoritative for this deliverable's trace anchor.
- OBJ-002 confirmed in decomposition §6 and §15 evaluation crosswalk.

### Extraction Notes
- Pass 1 (ANCHOR): 3 rows extracted — 1 IMPLEMENTS_NODE (parent anchor), 2 TRACES_TO_REQUIREMENT (SOW-020 and OBJ-002).
- Pass 2 (EXECUTION): 10 rows extracted — 3 PREREQUISITE (DEL-05-01, DEL-05-02, DEL-05-03 as explicit inputs that gate plan sections), 4 INTERFACE (DEL-04-03, DEL-08-01, DEL-09-01, DEL-04-01 as required integration inputs), 1 HANDOVER (DEL-01-02 as downstream consumer), 2 CONSTRAINT (RFP Section 7 and Addendum 03 as governing document constraints).
- DEL-05-01/02/03 classified as PREREQUISITE (not merely INTERFACE) because source documents explicitly establish HOLD POINT conditions and REQ statuses dependent on their completion before plan sections can be finalized.
- DEL-04-03, DEL-08-01, DEL-09-01, DEL-04-01 classified as INTERFACE because the plan must describe integration with them but they do not gate plan completion in the same way — placeholders are explicitly permitted by Procedure.
- The prior NOT_TRACKED mode is preserved in the declared section header as historical context; this run does not delete the original mode declaration.
- RFP and Addendum 03 PDFs not accessible via text extraction; TargetLocation set to _Sources/ per _REFERENCES.md.

### Warnings
- None of schema, lifecycle, or integrity class — all required columns present; single IMPLEMENTS_NODE found; DependencyIDs unique.
- [NOTE] SOW-020 scope ledger assignment ambiguity documented above in Anchor Validation Notes. Conservative assignment maintained per _CONTEXT.md explicit statement.

---

## Lifecycle Summary

| Dimension | Count |
|-----------|-------|
| Total rows | 13 |
| ACTIVE | 13 |
| RETIRED | 0 |
| SatisfactionStatus = TBD | 3 |
| SatisfactionStatus = PENDING | 10 |
| SatisfactionStatus = SATISFIED | 0 |
| Confidence = HIGH | 11 |
| Confidence = MEDIUM | 2 |
| Confidence = LOW | 0 |

### Tree Integrity
- IMPLEMENTS_NODE rows (ACTIVE): 1 — PASS (single parent anchor found)
- AMBIGUOUS_ANCHOR: No — PASS

### DAG Integrity
- All EXECUTION rows cite EvidenceFile and SourceRef — PASS
- No UNKNOWN TargetType deliverables — PASS (document targets use TargetType=DOCUMENT with location noted as TBD for PDFs)
- FromDeliverableID = DEL-04-02 on all rows — PASS

---

## Run History

| Run Date | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Rows |
|----------|------|-----------|---------------------|----------|-------------|
| 2026-02-18 | UPDATE | CONSERVATIVE | LOCATED (Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md) | SOW-020 scope ledger ambiguity noted (non-fatal); no blocking warnings | 13 |
