# DEL-09-09 dependency-extract run — 2026-10-03 (SCA-V4-003 propagation)

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
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/ScopeOfWork.md` | `fafd126f1743c18a3d9e79bef6023cbb94ddab0914634e052fb0114b8468786f` |

Pre-update `Dependencies.csv` SHA256 `e0e3297adb7350c58694aae88062d1bb35778c4440a5e91374f3d8c7c9663bb8`; pre-update `_DEPENDENCIES.md` SHA256 `fb23e7bfb2a572298233a501f40e5cb2bf810568478874d246d012328643fc39` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 24
enum invocations=21 (failures 0), id invocations=39 (failures 0), parent anchors=1
```

- Local deterministic checks (scratch `apply.py`): PASS; no quote outside the current ScopeOfWork, none over 30 words.
- Warnings: none.
- Source hash after run: `fafd126f1743c18a3d9e79bef6023cbb94ddab0914634e052fb0114b8468786f` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv` — SHA256 `e439fb4c01d6cc4bb43eed680f785da4d2d9cc3600a48e7fc02683156e1ce895`
- `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/_DEPENDENCIES.md` — SHA256 `79e497b5a3664a8c007b570334145df9ce3d0ce003ba6ea8f94f038f5f277bcf`
- This record is the third output; its digest is returned in the DX return file to avoid a self-hash.
