# DEL-01-01 dependency extraction — 2026-09-27

- Actual executor: native terminal TASK `/root/renewal_research_strategy/dep_del_01_01`, parent WORKING_ITEMS `/root/renewal_research_strategy`, under HELP_HUMAN `/root`. Native child dispatch; no child delegation, Git mutation or external messaging. The manager's internal target-classification clarification was consumed during this run: internal-project owner decisions are EXTERNAL only to this bounded unit; VER-005 stays conditional.
- Supplied basis: selected `chirality-root:bundled:workflow:dependency-extract`, method revision `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; setup source candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb`, reported identical-tree main integration `82efe62783bbe8ac7d21476a6662195c0b0a7587`. Manager reports individual PASS and combined check ongoing. No independent claim of global acceptance/review made here.
- Scope/write boundary: only own `Dependencies.csv`, `_DEPENDENCIES.md`, and this one record. Filesystem host access is broader; enforcement is instruction-bound plus actual workspace sandbox. No other full role body was intentionally consulted.
- Read scope: Root/TASK and selected workflow/resources read in full; catalog relevant descriptor selected (an initial overbroad index output was truncated; it did not activate other methods). Brief full; dispatch row and path lookup; own SoW/index/references full; decomposition markdown full; companion Package/Objectives/Scope rows as relevant, Deliverables identity fields only. No sibling SoW or acceptance/source-body expansion. Validator source bodies read to check ID/enum/shape contracts; schema helper was displayed through line 250 (full returned file).
- Initial source SHA256 `eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773` matched dispatch before writes and after checks. Initial index SHA256 `2951663109cf4d291793544e0fbfb153fd22dbefd0bb1f5ddaeb5efe00104386`; prior register absent. Human-owned prefix SHA256 `859763632ec1a6b0b81dd9ce72fdc6335bf41c56398c9bf66beb549eea78c16f` preserved exactly; prior Run History preserved exactly.
- Pass 1 completed before pass 2: 1 parent PKG-01 + 11 SOW + 3 objective anchors; canonical IDs/mappings confirmed. Pass 2: 9 evidence-grounded execution rows, 4 upstream/5 downstream. No exclusion-only, adjacency, citation-only or guessed sequence edge.
- Final counts: 24 ACTIVE EXTRACTED; 15 ANCHOR / 9 EXECUTION; 0 RETIRED / 0 DECLARED / 0 UNKNOWN. EXTERNAL 3: 1 external supplier interface contribution and 2 internal-project owner decisions external only to this unit. DELIVERABLE execution rows 6. Satisfaction NOT_APPLICABLE 15 / TBD 9; SATISFIED 0. Declared mirrors added/refreshed/retired 0; placeholders skipped 2; unread 0.
- Unresolved facts: OI-008 allocation; OI-012 selected supplier pin; DEP-005 version/environment and actual interface/capability evidence; all technical artifacts and receiving/qualification witnesses remain unclaimed. No unresolved target-identity hypothesis. Local INITIALIZED required maturity (6 rows) is checked contract scope only, never input receipt. The reciprocal DEL-01-05 input remains **when needed**. No supplier deployment, new allocation, act sequence, global closure, graph, status, adoption, release or professional reliance is established.

## Actual checks

- Reads, hash checks, CSV creation, two-pass row assembly and preservation/consistency assertions ran in one inline `python3 - <<'PY'` shell invocation; output only to the three allowed artifacts. All assertions PASS.
- `python3 tools/validation/validate_dependencies_schema.py projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Dependencies.csv` — exit 0; 29 required / 0 extension columns; 24 rows; canonical row semantics PASS.
- `python3 tools/validation/validate_enum.py DEPENDENCY_CLASS <value>`: ANCHOR, EXECUTION — all exit 0.
- `python3 tools/validation/validate_enum.py ANCHOR_TYPE <value>`: IMPLEMENTS_NODE, NOT_APPLICABLE, TRACES_TO_REQUIREMENT — all exit 0.
- `python3 tools/validation/validate_enum.py DIRECTION <value>`: DOWNSTREAM, UPSTREAM — all exit 0.
- `python3 tools/validation/validate_enum.py DEPENDENCY_TYPE <value>`: CONSTRAINT, HANDOVER, INTERFACE, OTHER, PREREQUISITE — all exit 0.
- `python3 tools/validation/validate_enum.py TARGET_TYPE <value>`: DELIVERABLE, EXTERNAL, REQUIREMENT, WBS_NODE — all exit 0.
- `python3 tools/validation/validate_enum.py EXPLICITNESS <value>`: EXPLICIT — all exit 0.
- `python3 tools/validation/validate_enum.py CONFIDENCE <value>`: HIGH — all exit 0.
- `python3 tools/validation/validate_enum.py ORIGIN <value>`: EXTRACTED — all exit 0.
- `python3 tools/validation/validate_enum.py STATUS <value>`: ACTIVE — all exit 0.
- `python3 tools/validation/validate_enum.py SATISFACTION_STATUS <value>`: NOT_APPLICABLE, TBD — all exit 0.
- `python3 tools/validation/validate_enum.py LIFECYCLE_STATE INITIALIZED` — exit 0. TBD is the workflow's unspecified-maturity placeholder; no invented lifecycle enum used.
- `bash tools/validation/validate_id_format.sh DEL <value>`: DEL-01-01, DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-01-06 — all exit 0.
- `bash tools/validation/validate_id_format.sh DEP <value>`: DEP-01-01-001, DEP-01-01-002, DEP-01-01-003, DEP-01-01-004, DEP-01-01-005, DEP-01-01-006, DEP-01-01-007, DEP-01-01-008, DEP-01-01-009, DEP-01-01-010, DEP-01-01-011, DEP-01-01-012, DEP-01-01-013, DEP-01-01-014, DEP-01-01-015, DEP-01-01-016, DEP-01-01-017, DEP-01-01-018, DEP-01-01-019, DEP-01-01-020, DEP-01-01-021, DEP-01-01-022, DEP-01-01-023, DEP-01-01-024 — all exit 0.
- `bash tools/validation/validate_id_format.sh OBJ <value>`: OBJ-001, OBJ-002, OBJ-004 — all exit 0.
- `bash tools/validation/validate_id_format.sh PKG <value>`: PKG-01 — all exit 0.
- `bash tools/validation/validate_id_format.sh SOW <value>`: SOW-097, SOW-099, SOW-100, SOW-101, SOW-118, SOW-119, SOW-121, SOW-128, SOW-131, SOW-135, SOW-149 — all exit 0.
- Qualified TargetRefIDs `chirality-app-v4:OI-008`, `chirality-app-v4:OI-012`, `chirality-app-v4:DEP-005` identify cited project issue/external records, not Deliverable/Dependency row IDs. Their literal tokens and locators were checked against the SoW; the ID helper has no OI or qualified-reference format. Non-deliverable TargetDeliverableID is empty.
- Local assertions: all 29 columns exact order; 24 unique IDs and semantic rows; exactly one parent; all mandatory content populated, allowing only semantically inapplicable ID slots and empty ProposedMaturity; every quote verbatim and ≤30 words; evidence/source locus nonblank; prefixes correct; target canonical identity/mapping; source hash unchanged; human-owned prefix/history exact; summary/lifecycle counts agree. PASS.
- Validator subprocesses: 69; all exit 0. Optional whole-execution EVQ/DRB omitted; local checks establish no blank quote, placeholder locus or prefix mismatch. No concurrent report output.

## Actual read identities (SHA256)

| Read file/origin | SHA256 |
|---|---|
| `AGENTS.md` | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `workflows/index.json` | `2bfa2c5faae1081c55ce95fd3d81c00b1d87ba1f51d0bc13e03c8fcb6ccdafb3` |
| `workflows/dependency-extract/WORKFLOW.md` | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/execution.json` | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` |
| `workflows/dependency-extract/resources/brief.md` | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_BRIEF.md` | `736418e84c8cba42655c75dfe6020fd32d0fec628718071122f3580cff0ac4ae` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_WORK_ITEMS.csv` | `98a6ff936f604363351054edfef8935f789f15f21d4cb34bed8f30a03e538eba` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/ScopeOfWork.md` | `eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/_REFERENCES.md` | `ae868706f2630a658c18fa1e4bf63af1fabfceed5029f0d183109b5ad1cb226e` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` | `9d44c2ad12f484f3d13901f28d99725ac7fc538dfacc85b832cdbe3c62b8fb81` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv` | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv` | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `tools/validation/validate_dependencies_schema.py` | `75cd74768cc8edf91c6f40b582f0fb570d2427894e6c2236ea2fe7d384291f5f` |
| `tools/validation/validate_enum.py` | `562934b075b20e7ec366baf60146cf7524acaebad8612b87873c4828dbeeaa70` |
| `tools/validation/validate_id_format.sh` | `370c946c301323b1bb273d268f04d4dc4187b865d9d2865b5273f0dd27d0acac` |

The dispatch table hash is captured at completion and may change as the manager records other launches; this unit's selected source/path row stayed unchanged.

## Output identities

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Dependencies.csv` — SHA256 `008863b143a87d1c1880e54c173c88631a58e4792ed9d6d966780c1765a5b783`.
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/_DEPENDENCIES.md` — SHA256 `b3f8bdbda038b26ef5283e3c9ee90e068a371bbe3144af8660fe1a23a26590db`.
- This record is the third output; its post-write hash is returned to the parent, avoiding a self-referential hash claim.

Return: local extraction and required checks PASS; broader graph/closure decisions remain with downstream work.
