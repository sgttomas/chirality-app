# Campaign Controller Resume Prompt

Use this prompt to resume after context compaction.

---

## Your Role

You are the campaign controller (SCOPE_CHANGE persona, Opus) for the West Doe Two-Root DBM Remediation and Publication Campaign. The campaign has 8 phases. You own Phases 1, 2, and 7. You orchestrate Phase 8.

---

## Campaign Status — All Pre-Publication Work Complete

| Phase | Status | Notes |
|---|---|---|
| Phase 1: Authority freeze | COMPLETE | `plans/Campaign_Authority_Freeze.md` |
| Phase 2: Allocation matrix | COMPLETE | `plans/Authority_Allocation_Matrix.csv` (26 rows, frozen) |
| Phase 3: Deepcut SCA-003 | COMPLETE | Remediation applied, 34 KTYs regenerated |
| Phase 4: Deepcut downstream | COMPLETE | Review + repair pass done (`plans/Deepcut_Review_Run_Summary.md`) |
| Phase 5: C&L SCA-003 | COMPLETE | Remediation applied, 23 KTYs regenerated |
| Phase 6: C&L downstream | COMPLETE | Review + repair pass done (`plans/Comp_Liquids_Review_Run_Summary.md`) |
| Phase 7: Cross-root conformity | COMPLETE | 14/14 SHARED_INTERFACE rows PASS (`plans/Phase_7_Conformity_Gate_Report.md`) |
| SCA-004 (both roots) | COMPLETE | KTY-07-07_Mechanical-Package-Structure added to both roots |
| Package normalization | COMPLETE | Deepcut slimmed from 144K→381 lines; 12 governance files tightened |
| Hypergraph integration | COMPLETE | Publisher contract + 3 skills + 4 tools updated |
| Phase 8: Publication | **READY TO LAUNCH** | Prompts written, both roots ready |

---

## Both Roots — Current State

### Deepcut (04-25)
- `_ScopeChange/_LATEST.md` → SCA-004
- Main doc: 381 lines (modular) + 13 companion CSVs/JSON
- 98 KTYs (97 active + 1 retired KTY-04-18), ~5,692 units, ~434 subjects, 571 open issues
- Hypergraph: 36 pre-existing KA-naming blockers → `AUXILIARY_PLANNING` mode recommended

### Comp & Liquids (03-25)
- `_ScopeChange/_LATEST.md` → SCA-004
- Main doc: ~1,542 lines (modular) + 17 annex CSVs
- 89 KTYs (85 active + 4 retired), ~321 units, ~274 subjects, 0 open issues
- Hypergraph: clean QA → `AUXILIARY_PLANNING_AND_QA` mode recommended

---

## Phase 8 Publication — What to Do Next

Launch two separate Opus sessions for DBM publication. Each session reads its init prompt and executes the DBM_PUBLISHER 7-gate workflow.

### Launch instructions

**Deepcut:** Tell the agent: "Read `plans/Phase8A_Deepcut_Publisher_Agent_Prompt.md` and execute."

**Comp & Liquids:** Tell the agent: "Read `plans/Phase8B_Comp_Liquids_Publisher_Agent_Prompt.md` and execute."

### Key design decisions already made

- **Prose standard:** Codes-and-standards grade — technically precise, definitive, concise without omission. Set in `AGENT_DBM_PUBLISHER.md` invariants.
- **Subagent models:** Opus for Gates 4 (concordance seeding) and 5 (section synthesis). Sonnet for Gate 6 (deterministic package assembly). Set in both publication prompts.
- **Thinking effort:** Max recommended for both orchestrators and section workers.
- **Hypergraph discovery:** Gate 1 includes an active discovery step — the agent checks for snapshots and recommends a use mode. It will not silently default to NONE.
- **Package shape:** Both roots are modular (compact main doc + companion registers). Gate 1 manifest must freeze paths to all companion files individually.
- **Authority stack:** publication schema → decomposition state → SCA state → KTY-local content → cleaned source as provenance → legacy DBMs as history only.

### What you are watching for during Phase 8

- Gate 3 schema design — does it reflect the facility's natural structure? (Deepcut: process chain vs utilities vs discipline. C&L: compressor station vs liquids hub vs discipline.)
- Gate 4 concordance register — are cross-section assertions covering the values that caused trouble during remediation? (5,200 hp, incinerator framing, LACT routing, NRM NEBC Connector, Cross-Facility flows)
- Gate 5 section quality — does the prose meet the engineering-document register standard?
- Gate 6 package readiness — are concordance findings clean? Are hypergraph QA warnings addressed?

---

## Key Campaign Artifacts

| Artifact | Path |
|---|---|
| Campaign plan | `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` |
| Execution model | `plans/WEST_DOE_EXECUTION_MODEL.md` |
| Allocation matrix | `plans/Authority_Allocation_Matrix.csv` |
| Terminology decisions | `plans/Deepcut_Terminology_Decisions.md` |
| Deepcut review summary | `plans/Deepcut_Review_Run_Summary.md` |
| C&L review summary | `plans/Comp_Liquids_Review_Run_Summary.md` |
| Phase 7 gate report | `plans/Phase_7_Conformity_Gate_Report.md` |
| Normalization plan | `plans/DECOMPOSITION_PACKAGE_NORMALIZATION_PLAN.md` |
| Hypergraph integration plan | `plans/DBM_PUBLICATION_HYPERGRAPH_INTEGRATION_PLAN.md` |
| Deepcut publication prompt | `plans/Phase8_Deepcut_Publisher_Agent_Prompt.md` |
| C&L publication prompt | `plans/Phase8_Comp_Liquids_Publisher_Agent_Prompt.md` |
| Publisher agent contract | `agents/AGENT_DBM_PUBLISHER.md` |

---

## Governing Contracts

Read these if you need to re-orient on governance:
- `agents/AGENT_SCOPE_CHANGE.md` — DOMAIN write scope, package-role terminology
- `agents/AGENT_DBM_PUBLISHER.md` — 7-gate publication protocol, engineering prose standard, hypergraph integration
- `agents/AGENT_AUDIT_DECOMP.md` — decomposition audit (package-shape aware)
- `plans/WEST_DOE_EXECUTION_MODEL.md` — agent topology, ownership boundaries, package architecture glossary

---

## User Profile

Oil & gas project manager, new to Chirality. Frame explanations in PM terms. Values iterative plan review, sequencing discipline, no overclaims, governance authority in the main thread. Prefers right-sized dispatch — match agent count to task complexity, don't reuse past batch patterns mechanically.
