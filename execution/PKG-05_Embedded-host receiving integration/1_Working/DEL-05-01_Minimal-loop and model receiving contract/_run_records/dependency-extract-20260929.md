# DEL-05-01 dependency-extract run — 2026-09-29

- Role: Type 2 TASK executor, node DX-2 of run APP-V4-BASIS-ALIGN-20260928 (Claude Code subagent launched by the run coordinator; delegated-harness-native). No descendants.
- Brief: `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md` DX section plus the DX-2 dispatch message (SOURCE_DOCS ScopeOfWork.md only; MODE UPDATE; STRICTNESS CONSERVATIVE; guard on DEL-09-06 relay-file pointers). Basis commit 557716cf7.
- Effective write scope: this deliverable's Dependencies.csv, _DEPENDENCIES.md and this record (instruction-enforced; host filesystem permission is broader). Read-only git; no network; no source/status/reference/Design/decomposition writes.
- Human-owned `_DEPENDENCIES.md` prefix (before `## Extracted Dependency Register`) preserved byte-for-byte; prior Run History preserved and one entry appended.

## Read identities

| Origin | Read extent | SHA256 |
|---|---|---|
| `AGENTS.md` | full | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `workflows/dependency-extract/WORKFLOW.md` | full | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/execution.json` | full | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` |
| `workflows/dependency-extract/resources/brief.md` | full | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | full | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | full | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md` | DX section | `aec0fa8ed521a1067826a980e840d8540db5d26efd1a9c832a96a769ad691211` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/ScopeOfWork.md` | full | `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/_REFERENCES.md` | full | `56c1c696a2ce9ae0c28a042d1cc980cb55e5dca8d06fbd3a2f648371bd6f7f62` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | full | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | ID/name/package lookups | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | ID/title lookups | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` |
| `projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv` | ID lookups | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv` | ID lookups | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` |
| `projects/chirality-app-v4/execution/_Decomposition/Objectives.csv` | ID lookups | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | ID lookups | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |

Pre-update `Dependencies.csv` SHA256 `fd44d166f9396d0e9a9ed7a516d1dc6054d5d8337817a9d007ddfd8cd1daf5dd`; pre-update `_DEPENDENCIES.md` SHA256 `46bbb080e248cb2dcf0d46b2221b95caa4f489265426d5c570325e59d43a9d63` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 25
enum invocations=21, id invocations=50, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Source hash after run: `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Dependencies.csv` — SHA256 `6c86f2263ea36a87f58024a85ecdeebcf5c13088503a2478aa92dcb6de5f03e6`
- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/_DEPENDENCIES.md` — SHA256 `7c1e6eecd77337ff60754735a805f00069902d1aee3194b01026862ec5e29c2d`
- This record is the third output; its digest is returned in the DX-2 return file to avoid a self-hash.
