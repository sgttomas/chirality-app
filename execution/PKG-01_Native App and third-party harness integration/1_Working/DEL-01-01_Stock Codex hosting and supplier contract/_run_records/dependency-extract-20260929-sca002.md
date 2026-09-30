# DEL-01-01 dependency-extract run — 2026-09-29 (SCA-V4-002 propagation)

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
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/ScopeOfWork.md` | full | `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/_REFERENCES.md` | full | `ae868706f2630a658c18fa1e4bf63af1fabfceed5029f0d183109b5ad1cb226e` |

Pre-update `Dependencies.csv` SHA256 `0fd327a4c13cb764de4f3437b71ff316f987dbe2a480757d8e3907f7f64dbde7`; pre-update `_DEPENDENCIES.md` SHA256 `20a3c87694b9917d4a92b1bd882463b7d1f6de343832348b73f0050517d17796` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 24
enum invocations=22, id invocations=45, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Warnings: none.
- Source hash after run: `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Dependencies.csv` — SHA256 `9fdb3ce3d8c180f58bf64d9fcf3476e3835dd6c8641bf4f4f203bc10f1f13d08`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/_DEPENDENCIES.md` — SHA256 `e0d6d2c711befb59d5b8985fda08ed4b2fe59fc1f2bd44657271554f70c9779a`
- This record is the third output; its digest is returned in the DX return file to avoid a self-hash.
