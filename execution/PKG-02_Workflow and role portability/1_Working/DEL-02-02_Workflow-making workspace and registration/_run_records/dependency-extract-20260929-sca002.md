# DEL-02-02 dependency-extract run — 2026-09-29 (SCA-V4-002 propagation)

- Role: Type 2 TASK executor, node DX of run APP-V4-SCA002-20260929 (Claude Code subagent launched by the run coordinator; delegated-harness-native). No descendants.
- Brief: the DX dispatch message for run APP-V4-SCA002-20260929, reusing `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides (SOURCE_DOCS ScopeOfWork.md only; ANCHOR_DOC ScopeOfWork.md; DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`; MODE UPDATE; STRICTNESS CONSERVATIVE; guards on DEL-09-06, N-12, N-B8 and DEL-04-01 suppliers). Basis commit 1efd4bcda.
- Effective write scope: this deliverable's Dependencies.csv, _DEPENDENCIES.md and this record (instruction-enforced; host filesystem permission is broader). Read-only git; no network; no source/status/reference/Design/decomposition/_DAG writes.
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
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/BRIEFS.md` | DX section | `b8a80e044c19ce2690b572971664f67de4560f1eba1bd5924c2b5db42e99043e` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET/ARC_EFFECT.md` | full (coordinator check only) | `4b3aeec0f041266dce0e2fae754c129d4473ff8c3268c0b5c638529c6951ddc0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET/SOW_REVISIONS.md` | full (orientation only; not an extraction source) | `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` |
| `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` | full | `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5` |
| `projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv` | ID/name/package lookups | `552df0609e7c5b4d0837b8571224fe20885a7252f99444dca2266701889f6bf3` |
| `projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv` | ID/title lookups | `a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0` |
| `projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv` | ID lookups | `055703d9a7147ab982731b783366b5fde2ef1ba805a9fe60b6c2b742182aa56e` |
| `projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv` | ID lookups | `d813629785ecfcca8dba613c908fd64a66df8849928523587bdd6b58458b935f` |
| `projects/chirality-app-v4/execution/_Decomposition/Objectives.csv` | ID lookups | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/Packages.csv` | ID lookups | `f51b411c9f5573b385755bbef2cb96c5819f0fbab01c79ac1e982253b4756663` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/ScopeOfWork.md` | full | `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/_REFERENCES.md` | full | `f2e2f58932a2d41c9d6ebb1b3d7339250872cd381dd10e1e3f6043c205cb6307` |

Pre-update `Dependencies.csv` SHA256 `88b3a9f3a71b03843a7cf037c015d36d6b821caed00d8013f8fa8fea0ea317e1`; pre-update `_DEPENDENCIES.md` SHA256 `56b0cd65dad421db83167a9a3e54d48dfab2d1cb8b795185150bf91ce48673a1` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 19
enum invocations=22, id invocations=41, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Warnings: none.
- Source hash after run: `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Dependencies.csv` — SHA256 `be14a079c872695ee6720c75bfe96b91dbac6ad4c228fb577ee044f1e32f7e0a`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/_DEPENDENCIES.md` — SHA256 `379ef690d62b11ba4836e33434f6804d0026cbb4068bc6cdbafc8fd33373c624`
- This record is the third output; its digest is returned in the DX return file to avoid a self-hash.
