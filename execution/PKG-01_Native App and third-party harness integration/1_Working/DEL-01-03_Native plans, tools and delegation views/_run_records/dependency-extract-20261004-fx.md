# DEL-01-03 dependency-extract run — 2026-10-04T02:15:48+00:00 (TargetLocation repair)

## Run

- **Role:** Type 2 TASK executor, node FX of run APP-V4-SCA003-20261002. A Claude Code subagent dispatched by the HELP_HUMAN session (delegated-harness-native), with no descendants.
- **Authority:** `OWNER_DECISIONS.md` DECISION-3 effect 4, "The DEL-01-03 absolute TargetLocation is repaired after acceptance", and the run's `BRIEFS.md` section "FX".
- **Basis:** HEAD `c147bb3abe`.
- **Method:** `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`), MODE UPDATE, STRICTNESS CONSERVATIVE.
- **Brief limit:** replace only the 14 absolute TargetLocation values with the project-relative form the other registers use. Change no other cell.
- **Effective write scope:** this register's `Dependencies.csv` and `_DEPENDENCIES.md` and this record. Outside the deliverable: the currency snapshot under `_Evaluation/DAGCurrency/`, its `_LATEST.md`, and the run's `DX/FX.md`. The scope is instruction-enforced; the host filesystem permission is broader. Read-only git; no network.

## What was done

- **Rows changed:** the 14 ACTIVE rows DEP-01-03-001…014 held TargetLocation under the personal Codex worktree root `/Users/…/.codex/worktrees/077c/chirality/` (the user folder is elided here so this record holds no home path).
- **The edit:** that prefix was removed byte-for-byte. Each value now begins `projects/chirality-app-v4/execution/`, the form used by every other register's TargetLocation (surveyed over the 40 other registers: 352 DELIVERABLE, 305 REQUIREMENT, 98 EXTERNAL, 40 WBS_NODE and 17 PACKAGE rows begin `projects/`).
- **Path check:** each repaired path, up to any `#fragment`, exists in the repository.
- **Byte-level check:**
  - the old file held the prefix exactly 14 times, all in TargetLocation;
  - re-parsing old and new gave the same row and column counts;
  - the only differing cells are those 14 TargetLocation cells, each equal to prefix + new value;
  - CRLF line endings were kept.
- **Rows not changed:** DEP-01-03-015…018 (`TBD`) and 019…022 (already relative).
- **No re-extraction:** the ScopeOfWork was not re-read for extraction, and no row was added, retired or re-quoted.
- **LastSeen not refreshed:** an UPDATE run would ordinarily refresh it. The brief forbids any other cell change, so it was left as it was.
- **Categories unchanged:** arc, class, type, direction, target identity, maturity and satisfaction.
- **`_DEPENDENCIES.md`:** one Run History entry was appended. The human-owned prefix and all other sections are byte-identical. The earlier Run Notes remark on the 14 absolute rows is historical; the new entry says it is superseded.

## Read identities

| Origin | SHA256 |
|---|---|
| `AGENTS.md` | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `workflows/dependency-extract/WORKFLOW.md` | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/resources/checks.md` | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/BRIEFS.md` | `8c2e019317d7ecb04bf664db9386926f16b6eaa388c3d6c7d18378ade70c2c19` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md` | `7f1c49cd469c8224ccd1fae8f3f5afae0405e0f0a27aea991287e73a7131389d` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/DX/DX_DEL-01-03.md` | `83077414ad129a35ca9e36368d628ea8da39ec664c5b57050484d6f1ae261046` |
| `projects/chirality-app-v4/execution/_DAG/DAG-004/HANDOFF_STATE.md` | `3c374f5e9fa4cfaa479699cddf5191b69bba2e0fe4707cb17acbe27dddc528ba` |
| `ScopeOfWork.md` (this deliverable; not an extraction input this run) | `0056ec198e855080da740e2fb72a3e0a37fcd304c58cca537d4ad56a11c46069` |

Pre-run hashes: `Dependencies.csv` `8b56b4cf3f6892e9a6700009a63176dc7382ac8ba52994b6a7817522620dc6ad` and `_DEPENDENCIES.md` `c31cbc9dac3512d3cea2739bcd47eac5996f1d9b27f943e36c6665506e55f367`. Both equal the DX outputs recorded in `DX/DX_DEL-01-03.md`.

## Verification

```text
validate_dependencies_schema.py: exit 0 — VALID, 29 columns (29 required + 0 extension), 22 data rows
validate_enum.py: 23 invocations, 0 failures
validate_id_format.sh: 34 invocations, 0 failures
unique DependencyIDs: yes; ACTIVE parent anchors (IMPLEMENTS_NODE): 1
validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB: exit 0; 41 registers, 929 rows, 0 ERROR, 0 WARNING
```

- **Warnings:** none.
- **Currency audit** against DAG-004 after the repair: `_Evaluation/DAGCurrency/CURRENCY_APP_V4_DEL0103_TLFIX_2026-10-03_2016/`, result `CURRENT_WITH_EVIDENCE_DRIFT`, 0 `DAG pending`.

## Output identities

- `Dependencies.csv` — SHA256 `048c2b271ed21627957d1c83948129111ec90cbbc0bc488e2e21ac1301debccc`
- `_DEPENDENCIES.md` — SHA256 `4567ff65bace12914765629b431cad2db0eeb07f132f92e0d750401c0edf874e`
- This record's digest is given in the run's `DX/FX.md`, to avoid a self-hash.
