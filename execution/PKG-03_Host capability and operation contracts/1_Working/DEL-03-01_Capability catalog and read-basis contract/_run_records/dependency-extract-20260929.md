# DEL-03-01 dependency-extract run — 2026-09-29

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
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/ScopeOfWork.md` | full | `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/_REFERENCES.md` | full | `01fd037c39c659a5e55c19d668cdd1a67b4e6b2069c2430165b32501c59d4967` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | full | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | ID/name/package lookups | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | ID/title lookups | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` |
| `projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv` | ID lookups | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv` | ID lookups | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` |
| `projects/chirality-app-v4/execution/_Decomposition/Objectives.csv` | ID lookups | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | ID lookups | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |

Pre-update `Dependencies.csv` SHA256 `36f9efd7cfeb78aa3c70a8ded53dc1c6959dbddb2e070c6966674fcb86ef2ad8`; pre-update `_DEPENDENCIES.md` SHA256 `b564d35aa593e1c0ddfa327f9b0f8c789655926aa76b10c491150f5f6a48eae2` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 31
enum invocations=24, id invocations=60, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Source hash after run: `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Dependencies.csv` — SHA256 `930796b5f1b82537ca24fc061b71b0947e5f7db3ab6e3f8552f5d4f05491407e`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/_DEPENDENCIES.md` — SHA256 `dd5cd73d5ab08fe1ae9a717e21ff50ab79f446f8b344ff921ff7a627f63e6bca`
- This record is the third output; its digest is returned in the DX-2 return file to avoid a self-hash.
