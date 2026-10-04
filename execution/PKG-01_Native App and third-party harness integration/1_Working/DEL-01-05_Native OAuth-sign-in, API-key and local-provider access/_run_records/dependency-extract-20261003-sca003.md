# DEL-01-05 dependency-extract run — 2026-10-03 (SCA-V4-003 propagation)

- Role: Type 2 TASK executor, node DX of run APP-V4-SCA003-20261002 (Claude Code subagent dispatched by the HELP_HUMAN session; delegated-harness-native). No descendants.
- Brief: run `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (model: SCA-V4-002 DX). MODE UPDATE; STRICTNESS CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; extraction guards of SOW_REVISIONS_A/B and the accepted Handoff_State. Basis commit 2d5e6845c5.
- Effective write scope: the 20 named registers' Dependencies.csv, _DEPENDENCIES.md and this record, plus the run folder `DX/` (instruction-enforced; host filesystem permission is broader). Read-only git; no network; no ScopeOfWork, _STATUS.md, DAG, Design or decomposition writes.
- Human-owned `_DEPENDENCIES.md` prefix (before `## Extracted Dependency Register`) preserved byte-for-byte; prior Run History preserved and one entry appended.

## Read identities

| Origin | SHA256 |
|---|---|
| `AGENTS.md` | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `workflows/dependency-extract/WORKFLOW.md` | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/execution.json` | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` |
| `workflows/dependency-extract/resources/brief.md` | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/BRIEFS.md` | `d62e4e4607c7d8b60108f1ee6c65b4b4331e825b5cde89ceaa5320c04a5a8ae1` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md` | `29c0a07b50d695a15bbff52b36d5925725cc7f3e78d0caf997ee9fd3c3b28c2e` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/ARC_EFFECT.md` | `25073317e9cde08ea38d90a37be8823c74bcf32d00d4490fffe9e743320894e7` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/LEDGER.csv` | `e28661cdf3375e156c44dad50c98c6413d56376fa9e0f961e2295472a8a35f12` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/SOW_REVISIONS_A.md` | `42c9167aadf8f0f88cc42b6e746af221140c2b7a00b7feaca552692e0cc7fc07` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/SOW_REVISIONS_B.md` | `d7b5cb2422cfdc69755e582b920351dccfced4d8871dc722f87ada48cfbb94df` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/RV/RA.md` | `a51e00acba5516ed713b7556e83bd08f2c92aab18fd9f4dbd8c6b02d027764e3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/RV/RB.md` | `1193a420064d815e27a0f76ebb108dbb85c1b1b6ec25eaa62ab3a198f8f48018` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Handoff_State.md` | `775fb93ffebb0114ba70c395ac42b1b4361a4ed8145a2c96d23dbf30813038f8` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Propagation_Plan.md` | `54891ede651588f4485b10385f696b364c5842242d3835d3030c84660f5786d8` |
| `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv` | `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | `552df0609e7c5b4d0837b8571224fe20885a7252f99444dca2266701889f6bf3` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` |
| `projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv` | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |
| `tools/coordination/analyze_dep_closure.py` | `2b8de3cbd2439ba1234aadf10e07348c4e2d30dd73da66cd0d88774e417a9adc` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/ScopeOfWork.md` | `2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3` |

Pre-update `Dependencies.csv` SHA256 `3b038c98f97cd6855b42b10e1602a24c34152f3defa582c037d6ee642f4796a6`; pre-update `_DEPENDENCIES.md` SHA256 `7f9f3f8101ccbdcd0dca2bb6f6a4d75217c35802a4940542f83e82530a9030b0` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 17
enum invocations=21 (failures 0), id invocations=24 (failures 0), parent anchors=1
```

- Local deterministic checks (scratch `apply.py`): PASS; no quote outside the current ScopeOfWork, none over 30 words.
- Warnings: none.
- Source hash after run: `2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Dependencies.csv` — SHA256 `7100a2e6fefa0879734d2461e9eceb1d2e86b9621a9b240c0ac7783ddc35bbca`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/_DEPENDENCIES.md` — SHA256 `7fab9eef1d2fcc53c1f555880dbed9805990247e16ed41b4610ec12faff32b03`
- This record is the third output; its digest is returned in the DX return file to avoid a self-hash.
