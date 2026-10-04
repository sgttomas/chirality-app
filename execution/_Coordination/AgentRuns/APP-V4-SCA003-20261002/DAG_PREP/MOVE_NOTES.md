# Move notes — DAG-004 publication (node D2)

Run `APP-V4-SCA003-20261002`, node D2, 2026-10-03, after DECISION-3 ("I accept DAG-004.", committed `ad16b789ec`). Type 2 TASK, the D1 instance continued by a coordinator message; no delegation, no git writes, no network. The fence was `_DAG/`, the `_Evaluation/` homes for DAG currency and closure, and this folder.

**The staged files were copied, not deleted.** This folder stays as the presented record, unchanged since `4ca22437f7`; only this note was added. Every copy was verified against `REVIEW_PACKET.md` (sha256 `af4a77d0…21dcd5b`):

| Staged here | Placed at (execution root) | Check |
|---|---|---|
| `DAG-004/` (33 files) | `_DAG/DAG-004/` | 33/33 equal to the packet |
| `DAG-004/` (33 files) | `_DAG/_Candidates/DAG-004/` (candidate record) | 33/33 equal |
| `CLOSURE_APP_V4_SCA003_2026-10-03_1936/` | `_Evaluation/DepClosure/` | 16/16 equal; `_Evaluation/DepClosure/_LATEST.md` now names it |
| `CURRENCY_APP_V4_SCA003_2026-10-03_1937/` | `_Evaluation/DAGCurrency/` | 24/24 equal (history; the pointer moved past it to the follow-up audit) |
| `CASE-002_EVIDENCE_UPDATE.proposed.md` | not placed | For `scc-resolution-case` later, as directed |

**Added in `_DAG/DAG-004/`:**

- `ACCEPTANCE_RECORD.md` (`31f03968…46143e3`);
- `HANDOFF_STATE.md` (`3c374f5e…c528ba`);
- `INDEPENDENT_REVIEW.md`, a copy of `reviews/V25.md` (`b0d5f45e…ce93a9f`);
- `REVIEW_PACKET.md`, a copy of this folder's (`af4a77d0…21dcd5b`);
- `MANIFEST.sha256` (`3da3059c…b37c3f`), 37 entries, all OK, with the same path set as DAG-003's.

**Pointers:**

- `_DAG/_LATEST.md` was written from `PROPOSED_LATEST.md` with `{ACCEPT_DATE}` = 2026-10-03 (`b9353a41…f55d4ca2d`; `Latest: DAG-004`, `Supersedes: DAG-003`).
- `_Evaluation/DAGCurrency/_LATEST.md` (`29baad23…adcc67a`) names the follow-up audit `CURRENCY_APP_V4_DAG004_ACCEPTED_2026-10-03_2012`: `CURRENT`, analyzer `NO_DEPARTURE_FOUND`, 0 pending.

**History.** All 335 files of DAG-001, DAG-002, DAG-003, `_Candidates/DAG-001…003` and `_DAG/cases/` have the same SHA-256 before and after publication. Their manifests check 61/61, 37/37 and 37/37.

**Not done (as directed):**

- the CASE-002 update was not applied;
- the DEL-01-03 TargetLocation was not repaired;
- no register, ScopeOfWork, `_STATUS.md` or case file was touched.
