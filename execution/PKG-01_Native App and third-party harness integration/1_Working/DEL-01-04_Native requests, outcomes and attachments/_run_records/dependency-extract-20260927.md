# DEL-01-04 dependency extraction — 2026-09-27

- Actual terminal TASK: `/root/renewal_research_strategy/dep_del_01_04`; parent WORKING_ITEMS `/root/renewal_research_strategy`, under HELP_HUMAN `/root`; delegated-harness-native descendant. No further delegation, Git mutation or external messaging. The manager records actual dispatch/return separately.
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; source basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`, unchanged method in setup candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree integration `82efe62783bbe8ac7d21476a6662195c0b0a7587` per brief.
- Timestamp: 2026-09-28T03:14:57+00:00. MODE UPDATE, STRICTNESS CONSERVATIVE, CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT. Only ScopeOfWork.md supplied extraction evidence for both passes.
- Enforcement: workspace-write host permission is broader than this brief; instructions limited writes to own Dependencies.csv, _DEPENDENCIES.md and this run record. No claim of a narrower host-enforced capability. No other role body, sibling source contract or governing source body was loaded.

## Result and interpretation

Pass 1 completed and checked before Pass 2: 6 anchors (1 parent, 3 scope, 2 objective). Pass 2: 13 execution rows (6 local deliverable interfaces/handoffs, 7 external contribution/decision rows). Total 19 ACTIVE, 0 RETIRED, 0 DECLARED, 0 UNKNOWN. Closure NOT_APPLICABLE 6 / TBD 13 / SATISFIED 0. IDs DEP-01-04-001 through DEP-01-04-019.

Local targets are DEL-01-01, DEL-01-02, DEL-02-02 twice (distinct incoming/outgoing interfaces), DEL-04-01 and DEL-04-03. DEL-01-03 exclusion/shared scope does not evidence a consumed production input. External rows preserve five owner choices at their exact points of need, DEP-005 respective supplier witness inputs and VER-005 actual person/recorder qualification evidence. Human witness identity/location is unresolved; no global human permission or professional-certification gate is inferred. Technical receipt and decisions remain distinct from local INITIALIZED maturity. Optional UI reuse, unresolved storage/allocation/pin, absent runtime observations and separate joined witnesses remain unclaimed.

Declared mirror added/refreshed/retired = 0/0/0; two placeholder entries skipped. The full pre-extraction human-owned prefix is byte-identical; prior Run History retained. Pre-extraction _DEPENDENCIES.md SHA256: `6fe45618080a60d4f757b08607566f6893a4501e447c633dac351255ca952994`. No preexisting Dependencies.csv.

## Validation

- `python3 tools/validation/validate_dependencies_schema.py "projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv"`: exit 0. Result: "VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv\n  Columns: 29 (29 required + 0 extension)\n  Data rows: 19"
- `python3 tools/validation/validate_enum.py <enum> <value>`: all 22 distinct pairs below exited 0:
  - DEPENDENCY_CLASS: ANCHOR, EXECUTION.
  - ANCHOR_TYPE: IMPLEMENTS_NODE, NOT_APPLICABLE, TRACES_TO_REQUIREMENT.
  - DIRECTION: DOWNSTREAM, UPSTREAM.
  - DEPENDENCY_TYPE: CONSTRAINT, HANDOVER, INTERFACE, OTHER, PREREQUISITE.
  - TARGET_TYPE: DELIVERABLE, EXTERNAL, REQUIREMENT, WBS_NODE.
  - EXPLICITNESS: EXPLICIT.
  - CONFIDENCE: HIGH.
  - ORIGIN: EXTRACTED.
  - STATUS: ACTIVE.
  - SATISFACTION_STATUS: NOT_APPLICABLE, TBD.
- `bash tools/validation/validate_id_format.sh <type> <value>`: all 33 distinct supported ID values exited 0.
  - DEL: DEL-01-01, DEL-01-02, DEL-01-04, DEL-02-02, DEL-04-01, DEL-04-03.
  - PKG: PKG-01, PKG-02, PKG-04.
  - DEP: DEP-01-04-001 through DEP-01-04-019.
  - SOW: SOW-005, SOW-014, SOW-129.
  - OBJ: OBJ-001, OBJ-002.
- OI-001/002/008/012/014 and external DEP-005 are exact accepted companion-row identifiers; the validator supports neither OI nor that external DEP form, so these were checked by source membership instead of misapplying local dependency format rules.
- Python assertions passed: source hash before/after matches dispatch; 29 columns; 19 unique IDs; one parent; no duplicate semantic row; source loci present; all quotes verbatim and <=30 words; target identity placement; human prefix unchanged; history retained; source/index/class/external/closure counts agree. Quote/locus/prefix checks cover local EVQ-003, EVQ-004 and DRB-006 conditions with zero findings. Optional whole-root EVQ/DRB check was not run.
- No product verification, implementation, graph acceptance, lifecycle advance, adoption or release performed. No integrity warnings.

## Actual read origins and SHA256

Paths below are repository-relative to `/Users/ryan/.codex/worktrees/077c/chirality`. Hash identifies complete file bytes; read extent identifies actual supplied content. Mutable dispatch hash here is the validation-time image, and its earlier read image was `54a159bb63488d7463cc2ffeefc335eb2f70a6ecb22591a38f1fe895f0ddaad1`; no row-state or unrelated manager write is asserted immutable.

| Origin | Actual read extent | SHA256 |
|---|---|---|
| `AGENTS.md` | full | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `agents/AGENT_TASK.md` | full | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `workflows/dependency-extract/WORKFLOW.md` | full | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/execution.json` | full | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` |
| `workflows/dependency-extract/resources/brief.md` | full | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | full | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | full | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_BRIEF.md` | full | `736418e84c8cba42655c75dfe6020fd32d0fec628718071122f3580cff0ac4ae` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_WORK_ITEMS.csv` | assigned row and referenced local-target paths; concurrent manager state | `1644b2fd0c7deccf95f37e739c2bbd822ce2492cd5c4ac28df298a9de5b2c538` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md` | full; only extraction source | `7261a58f93d4531ca080c16d7fe088818871c3444085bade2eb2350ace94e60a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/_REFERENCES.md` | full | `1c6d5c2a653be29484a0fbd37faefc0947c92dae487eb66d0bc3d4d18e6ad42c` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` | full | `9d44c2ad12f484f3d13901f28d99725ac7fc538dfacc85b832cdbe3c62b8fb81` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv` | PKG-01 | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` | DEL-01-01..04, DEL-02-02, DEL-04-01/03 | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` | SOW-005/014/129 | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv` | OBJ-001/002 | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv` | OI-001/002/008/012/014 | `b65578a0ff34a45d705aac3d8b714e0a0632bec73fd73c5cc0ac8a19c85dc821` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/External_Dependencies.csv` | DEP-005 | `fa2922f7a4d8c5b31e86752ef44fb654ec037cc46995153ced6345e90c84c134` |
| `tools/validation/validate_id_format.sh` | full implementation | `370c946c301323b1bb273d268f04d4dc4187b865d9d2865b5273f0dd27d0acac` |
| `tools/validation/validate_enum.py` | full implementation | `562934b075b20e7ec366baf60146cf7524acaebad8612b87873c4828dbeeaa70` |

## Output identities

- `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv` — SHA256 `45546cfeeac2509b975d42dccb132fee6f1baf62600d1c9b8559c7ac665f61e3`.
- `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/_DEPENDENCIES.md` — SHA256 `3caaec7fb441ac3fa4110738e806f08f05beb096d1c0954ddc86b3088228f74f`.
- This record: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/_run_records/dependency-extract-20260927.md`; its final hash is returned to the caller outside the file to avoid a self-hash claim.
