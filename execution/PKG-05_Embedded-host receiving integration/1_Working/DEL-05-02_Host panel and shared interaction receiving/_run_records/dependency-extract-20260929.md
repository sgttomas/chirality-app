# DEL-05-02 dependency-extract run — 2026-09-29

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
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/ScopeOfWork.md` | full | `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/_REFERENCES.md` | full | `7cbde728abc6f9b871ceaede1fdb91a77541fba81c67dc2326bc9152828912fd` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | full | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | ID/name/package lookups | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | ID/title lookups | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` |
| `projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv` | ID lookups | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv` | ID lookups | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` |
| `projects/chirality-app-v4/execution/_Decomposition/Objectives.csv` | ID lookups | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | ID lookups | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |

Pre-update `Dependencies.csv` SHA256 `92067b628007cee18b20e2f2a4282549e7e1e21354bbbae1394f38df117618fc`; pre-update `_DEPENDENCIES.md` SHA256 `abf784e0c13cedffca64324866c0656087a4f8a9ea6104d10fc24f411485c975` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 20
enum invocations=22, id invocations=36, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Source hash after run: `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Dependencies.csv` — SHA256 `2889aa5f910b1123347d821f27a7e609d5a9a8f8dc7fe6c6825813bef1900568`
- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/_DEPENDENCIES.md` — SHA256 `db27f5bce5c222ebe342f192e68aba2987bb0517eced22082afbbcf34795496b`
- This record is the third output; its digest is returned in the DX-2 return file to avoid a self-hash.
