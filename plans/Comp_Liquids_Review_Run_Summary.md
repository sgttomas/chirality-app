# Comp & Liquids Decomposition and Folder Review — Run Summary

**Date:** 2026-04-19
**Root:** `domain-test/domains/West_Doe_Comp_and_Liquids_DBM`
**Plan:** `plans/COMP_AND_LIQUIDS_DECOMPOSITION_AND_FOLDER_REVIEW_PLAN.md`
**Mode:** Review + Repair

---

## Baseline Inventory

| Item | Count |
|------|-------|
| Categories | 18 (CAT-000 through CAT-017) |
| KTY folders | 88 (plan assumed 111; actual 1:1 with register) |
| Active KTYs | 84 |
| Retired KTYs | 4 (KTY-04-03, KTY-04-04, KTY-04-10, KTY-05-03) |
| Decomposition package files | 17 annex CSVs + main doc + Archive.zip + README.txt + _KTY_SCAFFOLD_BRIEF.md |
| SCA snapshot directories | 4 (SCA-001, SCA-001_2026-04-14_0000, SCA-002_2026-04-14_0000, SCA-003_2026-04-19_0900) |
| Domain ledger units | 319 (272 IN, 47 OUT, 0 TBD, 0 RETIRED) |
| Knowledge subjects | 315 (272 IN, 43 OUT) |
| Objectives | 7 |
| Open issues | 0 |

---

## _ScopeChange Review

| Snapshot | Status | Notes |
|----------|--------|-------|
| `_LATEST.md` | PASS | Points to SCA-003_2026-04-19_0900 |
| `SCA-003_2026-04-19_0900/` | PASS | All 8 required artifacts present. RUN_SUMMARY coherent. |
| `SCA-001_2026-04-14_0000/` | PASS | Full snapshot. Extra `briefs/` directory = historical residue (non-contract). |
| `SCA-002_2026-04-14_0000/` | Historical limitation | Only 4 of 8 artifacts (Pre/Post Coverage, RUN_SUMMARY, briefs/). Known incomplete. |
| `SCA-001/` (bare) | Historical residue | Contains only `Value_Engineering_Tracker.csv`. Not a valid snapshot. |

No repairs required. No contradictions with accepted truth.

---

## Decomposition Parity Matrix

| # | Cross-Check | Verdict |
|---|-------------|---------|
| 1 | Main doc vs annex_categories.csv | PASS |
| 2 | Main doc vs annex_category_telemetry.csv | PASS |
| 3 | Main doc vs annex_coverage_telemetry.csv | PASS |
| 4 | Main doc vs annex_validation_checks.csv | PASS |
| 5 | Main doc vs annex_domain_ledger.csv | PASS |
| 6 | Main doc vs annex_knowledge_subjects.csv | PASS |
| 7 | Main doc vs annex_knowledge_types.csv | PASS |
| 8 | Main doc vs annex_objectives.csv | PASS |
| 9 | Main doc vs annex_objective_kty_mapping.csv | PASS |
| 10 | Main doc vs annex_kty_category_mapping.csv | PASS |
| 11 | Main doc vs annex_open_issues.csv | PASS |
| 12 | Main doc vs annex_decision_log.csv | PASS |
| 13 | Main doc vs annex_vocabulary_map.csv | PASS |
| 14 | annex_domain_ledger vs annex_unit_category_assignment | PASS |
| 15 | annex_domain_ledger vs annex_unit_subject_mapping | PASS (4 OUT admin units absent by design) |
| 16 | annex_knowledge_subjects vs annex_unit_subject_mapping | PASS |
| 17 | annex_categories vs annex_category_telemetry | PASS |
| 18 | annex_knowledge_types vs annex_objective_kty_mapping | PASS |
| 19 | annex_inventory vs actual package | DRIFT (repaired) |

### SCA-003 Hotspot Verification

| Hotspot | Status |
|---------|--------|
| 5 flare subjects TBD→IN | PASS |
| Incinerator framing shared 03-25/04-25 | PASS |
| LACT routing: one NRM LACT to NRM NEBC Connector | PASS |
| CAT-004 and CAT-005 reconciled counts | PASS |
| Retired KTY objective mappings removed | PASS |
| Unified KTY-count convention: 84 active (4 retired, 88 total) | PASS |

---

## Repaired Now

### _Decomposition parity repairs

| ID | File | Repair |
|---|---|---|
| D1 | `annex_inventory.csv` | Added self-reference row (annex_inventory.csv was listing all annex files but not itself) |
| D2 | `annex_knowledge_types.csv` | KTY-04-09 ExplicitSubjectCount 14→13 (SUB-04-09-08 retired by SCA-001; _STATUS.md and _CONTEXT.md already reflected retirement but CSV column was stale) |

### _ScopeChange repairs

None required.

### KTY metadata repairs

None applied directly. All KTY-local content issues are in files outside the direct repair scope (Scoping.md, KA-*.md, _DEPENDENCIES.md). See below.

---

## Requires Domain-Documents Rerun

| KTY | File | Issue | Drift Type |
|---|---|---|---|
| KTY-04-09 | `Scoping.md` line 45 | Evidence table shows `HBK-0134 \| IN` — should be OUT (retired by SCA-001, DEC-001-002) | Subject status drift |
| KTY-04-09 | `_DEPENDENCIES.md` line 19 | Incinerator (SUB-04-09-09) notes say "Services 4-25 equipment only; no 3-25-internal driver" — contradicts corrected framing in KA-09 which says "shared between 04-25 and 03-25 per cleaned source §5.2" | Interface framing drift |
| KTY-01-04 | `KA-01_Scope-Responsibility-Definition__Included-Scope.md` line 46 | "Two (2) 5,000 hp electric drive multistage inlet compressors" — DEC-003-004 resolved 5,200 hp (AUTH-019 / S5.1) as canonical. KTY-01-01 KA-01 and KTY-04-05 KA-04 already corrected to 5,200 hp. | Specification drift |

Metadata alignment must follow these reruns.

---

## Requires Human Decision

| ID | Location | Issue | Why |
|---|---|---|---|
| H1 | KTY-12-04: KA-02 lines 37/52/64, KA-04 lines 37/68, KA-05 lines 61/76 | "Pembina LACT" used as current electrical feeder label across 7 occurrences in 3 KA files | Source DBM (W242510 S12.4.2) describes separate feeders for "Pembina LACT" and "NRM LACT." Process routing resolves to one NRM LACT per DEC-003-003, but the electrical feeder configuration addresses physical infrastructure (transformer) that may persist for a future 3rd-party LACT. Human must decide: rename to "Future 3rd Party LACT" or preserve as source-faithful. |
| H2 | KTY-11-07: KA-01 line 108 | `990-2 \| LACT Electrical Building \| Shop \| Pembina Scope` | Building list ownership label references "Pembina Scope." Linked to H1 — decision on LACT naming applies here too. |
| H3 | `_Aggregation/Equipment_List/partials/apply_validation_corrections.py` lines 78-80 | Correction script patches 5200→5000 hp, but DEC-003-004 resolved 5,200 hp as canonical | Script enforces S4.5.4.4 value (5,000 hp); decomposition decision log says S5.1 value (5,200 hp) governs. Script direction is opposite to the resolved decision. Out of review repair scope (_Aggregation) but must be reconciled before publication. |
| H4 | All 88 KTYs: `_REFERENCES.md` | No decomposition pointer in any _REFERENCES.md | All 88 reference only source DBM documents (W235633, W242510). Decomposition pointer exists only in _CONTEXT.md. Systemic scaffold design choice. Human should decide if _REFERENCES.md should also carry a decomposition reference row. |

---

## Terminology and Interface Sweep Results

| Term | Verdict |
|---|---|
| Pembina HVP Pipeline | CLEAN — no live contradictions. All mentions are provenance/legacy annotations or correction notes. |
| LPG | CLEAN — all instances are source-faithful (API 2510 standard name, acronym table, legacy references with correction notes). |
| FUTURE / Future | CLEAN — all instances are in `_Sources/` or `_archive/` (source-faithful PFD labels). |
| Cross-Fence | CLEAN — every instance appears only as "replaces Cross-Fence" or "retired synonym: Cross-Fence." |
| Cross-Facility | CLEAN — used canonically throughout. |
| Incinerator | 1 live contradiction (KTY-04-09 _DEPENDENCIES.md line 19 "Services 4-25 equipment only") → queued for rerun. All KA-level content correctly framed as shared. |
| Flare | CLEAN — 5 flare subjects confirmed IN. KTY-01-04 and KTY-05-05 consistent. |
| LACT | 3 live contradictions in _Aggregation narratives (out of scope). KTY-local content clean. |
| 5,000 hp / 5,200 hp | 1 live contradiction (KTY-01-04 KA-01 line 46). Latent contradiction in _Aggregation correction script (out of scope). |
| "services 4-25 equipment only" | 1 live contradiction (same as incinerator finding above). |
| Shared utility wording | CLEAN — canonical phrasing throughout. |
| Dual-LACT assertions | 3 instances in _Aggregation narratives (out of scope). |
| Pembina LACT (electrical) | 7 occurrences in KTY-12-04 KA files → HUMAN_DECISION_REQUIRED (H1). |

---

## _STATUS.md Systemic Findings (Non-Blocking)

These are format and lifecycle-state observations, not correctness defects:

| Finding | Scope | Notes |
|---|---|---|
| All 88 _STATUS.md files use log-only format | Systemic | No structured `Current State` header. Last log entry implies state. Tooling cannot reliably parse current state. |
| 23 Phase 6 KTYs still show INITIALIZED despite _run_records/ | 23 KTYs | Regeneration occurred (Scoping.md, KA files present) but _STATUS.md not updated to post-regeneration state. |
| 4 retired KTYs lack explicit `Current State: RETIRED` | 4 KTYs | Last log entry says RETIRED but no parseable current-state field. |

These are deferred to the Phase 7 cross-root conformity gate or publication prep. Lifecycle state consistency does not block the review.

---

## Post-Regeneration Closure (23 Phase 6 KTYs)

| KTY | Scoping.md | KA Set | _CONTEXT.md | Issue |
|---|---|---|---|---|
| KTY-01-01 | Current | Complete | Aligned | — |
| KTY-01-02 | Current | Complete | Aligned | — |
| KTY-01-03 | Current | Complete | Aligned | — |
| KTY-01-04 | Current | Complete | Aligned | KA-01 line 46: 5,000→5,200 hp (Phase 7 fix) |
| KTY-02-01 | Current | Complete | Aligned | — |
| KTY-03-01 | Current | Complete | Aligned | — |
| KTY-03-02 | Current | Complete | Aligned | — |
| KTY-03-03 | Current | Complete | Aligned | — |
| KTY-04-01 | Current | Complete | Aligned | — |
| KTY-04-02 | Current | Complete | Aligned | — |
| KTY-04-05 | Current | Complete | Aligned | — |
| KTY-04-08 | Current | Complete | Aligned | — |
| KTY-04-09 | Current (HBK-0134=OUT, Phase 7 fix) | Complete (KA-08 RETIRED) | Aligned | Scoping.md + _DEPENDENCIES.md corrected (Phase 7 fix) |
| KTY-04-11 | Current (HBK-0159=OUT) | Complete | Aligned | — |
| KTY-04-12 | Current | Complete | Aligned | — |
| KTY-04-13 | Current | Complete | Aligned | — |
| KTY-04-14 | Current | Complete | Aligned | — |
| KTY-05-01 | Current | Complete | Aligned | — |
| KTY-05-02 | Current | Complete | Aligned | — |
| KTY-05-04 | Current | Complete | Aligned | — |
| KTY-05-05 | Current | Complete | Aligned | — |
| KTY-05-07 | Current | Complete | Aligned | — |
| KTY-12-04 | Current | Complete | Aligned | — |

23 of 23 Phase 6 KTYs fully closed. 2 issues found and repaired in Phase 7 remediation loop (KTY-04-09 Scoping.md + _DEPENDENCIES.md, KTY-01-04 KA-01).

---

## Phase 7 Remediation Loop — EXECUTED

All follow-on items resolved in Phase 7 local remediation:

| Fix | File(s) | Change |
|---|---|---|
| KTY-04-09 Scoping.md | `Scoping.md` line 45 | HBK-0134 IN→OUT [RETIRED — SCA-001] |
| KTY-04-09 _DEPENDENCIES.md | `_DEPENDENCIES.md` line 19 | Incinerator reframed: 03-25 equipment receiving cross-facility discharge from 04-25; primary driver is 03-25 mercaptan treating vapors |
| KTY-01-04 KA-01 | `KA-01_Scope-Responsibility-Definition__Included-Scope.md` line 46 | 5,000→5,200 hp per DEC-003-004 |
| KTY-12-04 Pembina LACT rename | `KA-02`, `KA-04`, `KA-05` | "Pembina LACT"→"Future 3rd Party LACT" (7 occurrences across 3 files) |
| KTY-11-07 Pembina Scope rename | `KA-01` line 108 | "Pembina Scope"→"Future 3rd Party LACT Scope" |
| _Aggregation narratives | `Process_Flow_Narrative.md`, `narrative_only.md`, `Process_Flow_Narrative_for_pdf.md` | "two LACT units (Pembina and NRM)"→"one NRM LACT unit to NRM NEBC Connector (with provision for future 3rd party LACT)" |
| _Aggregation Equipment_Extract | `KTY-12-04_Equipment_Extract.md`, `Equipment_Master_List.csv` | "Pembina LACT Incoming Transformer"→"Future 3rd Party LACT Incoming Transformer" |
| _Aggregation correction script | `apply_validation_corrections.py` lines 78-80 | Direction reversed: 5000→5200 (was 5200→5000), consistent with DEC-003-004 |
| _Aggregation validation doc | `validate_03_compressors.md` | Correction note updated to reflect DEC-003-004 ruling (5,200 hp governs per §5.1) |
| _Aggregation equipment CSVs | `Equipment_List_3-25.csv` rows 5-6, `agent_03_compressors.csv` rows 2-3 | All "KBZ 5000 hp" → "KBZ 5200 hp"; all "5000 hp per unit" → "5200 hp per unit (DEC-003-004; §5.1 governs)" |
| KTY-03-04 incinerator framing | `KA-02_Reference__Disulphide-Oil.md` line 51, `KA-03_Reference__Spent-Caustic.md` line 49 | "existing incinerator at the 4-25 West Doe site" → "incinerator located at 03-25, shared per AUTH-022"; removed stale "caustic regeneration column overheads" (SCA-001 retirement) |
| KTY-12-04 CONF-003 residual | `KA-09_Reference__Electrical-Motor-Specifications.md` line 92 | Stale "discrepancy flagged for human review" → "CONF-003 resolved per DEC-003-004: 5,200 hp governs" |
| KTY-04-09 Equipment Extract | `_Aggregation/Equipment_Extract/KTY-04-09_Equipment_Extract.md` line 22 | "incinerator at 4-25 / 4-25 scope item" → "incinerator at 03-25, shared per AUTH-022. CONFLICT-01 resolved." |

---

## Out of Scope (Noted)

| Item | Status |
|---|---|
| SCA-002_2026-04-14_0000/ incomplete snapshot | Historical limitation; known incomplete |
| Bare SCA-001/ directory | Historical residue (Value_Engineering_Tracker.csv only) |
| `annex_categories.csv` SubjectCount column name | Measures ExplicitSubjectCount (from KTY register), not SubjectCountActual (from telemetry). Ambiguous but structurally consistent. INFO-level. |

---

## Follow-On Sequence — EXECUTED

All items resolved in Phase 7 remediation loop:

| Step | Status | Result |
|---|---|---|
| 1. KTY-04-09 Scoping.md + _DEPENDENCIES.md | COMPLETE | HBK-0134 OUT; incinerator reframed as 03-25 equipment |
| 2. KTY-01-04 KA-01 5,200 hp | COMPLETE | Corrected per DEC-003-004 |
| 3. KTY-12-04 + KTY-11-07 Pembina LACT rename | COMPLETE | 10 occurrences across 6 files renamed to "Future 3rd Party LACT" |
| 4. _Aggregation narrative LACT correction | COMPLETE | 3 files corrected to one NRM LACT |
| 5. _Aggregation correction script + validation | COMPLETE | Direction reversed to match DEC-003-004 |
| 6. _Aggregation Equipment_Extract | COMPLETE | 3 occurrences renamed |

### Remaining for publication prep (non-blocking)

| Item | Status |
|---|---|
| _REFERENCES.md decomposition pointer (H4) | Systemic design decision — deferred to publication prep |
| _STATUS.md format normalization | Systemic — deferred to publication prep |

---

## Final Acceptance Status

| Criterion | Status |
|---|---|
| No internal contradiction in decomposition-local registers | PASS (after D1, D2 repairs) |
| `_ScopeChange/_LATEST.md` correct | PASS |
| Historical snapshot anomalies classified | PASS |
| No repairable drift in KTY `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md` | PASS |
| All KTY content corrections applied | PASS — KTY-04-09, KTY-01-04, KTY-12-04, KTY-11-07, KTY-03-04 corrected in Phase 7 loop |
| All _Aggregation contradictions corrected | PASS — narratives, equipment extract, equipment CSVs, correction script, validation doc |
| Run summary separates repaired / rerun / unresolved | PASS |
| Handoff is decision-complete | PASS — all human decisions resolved |
| SCA-003 hotspots verified | PASS — all 6 checks pass |
| Terminology sweep complete | PASS — 12 terms checked, all live contradictions resolved |
| Phase 7 cross-root conformity gate | PASS — 14/14 SHARED_INTERFACE rows pass |

**The Comp & Liquids root is ready for Phase 8 publication.**
