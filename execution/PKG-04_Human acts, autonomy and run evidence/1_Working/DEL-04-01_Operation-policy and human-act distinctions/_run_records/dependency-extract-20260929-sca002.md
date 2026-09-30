# DEL-04-01 dependency-extract run — 2026-09-29 (SCA-V4-002 propagation)

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
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/ScopeOfWork.md` | full | `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_REFERENCES.md` | full | `026a1239474260ee8de0e956db219bf7bb87b38b5f3f3bb77ce276c87cac458d` |

Pre-update `Dependencies.csv` SHA256 `8f826f6c03d6a8a6fc116fdcd2e0d9c1501241b5d0eb4212c5f032132737756a`; pre-update `_DEPENDENCIES.md` SHA256 `92df6f3ead9679d1a51f0f2efa8ef5c6cb8adc2036b34905bb74a3238ef1a2fc` (both read in full).

## Verification

```text
schema exit=0: VALID: projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 29
enum invocations=21, id invocations=56, all_ok=True
```

- Local deterministic checks: PASS.
- Target ID re-resolution in current companion CSVs: PASS.
- Warnings: none.
- Source hash after run: `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` (unchanged).

## Output identities

- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Dependencies.csv` — SHA256 `d3892649dbc008d81b9a183d34c44cf68e0765d886a04dce924e69f456c5c9c1`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_DEPENDENCIES.md` — SHA256 `b504a28b63a3940479a636700b81428f4e107881253d133be632bd6601fe2db6`
- This record is the third output; its digest is returned in the DX return file to avoid a self-hash.
