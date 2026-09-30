# SCA-V4-002 group-2 authority pointer

**Accepted snapshot:** `checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/`
(`DECISION.md` `094aec9d…`; `ACCEPTED_MANIFEST.csv` `fd851925…`).

**Scope of the acceptance** (the same owner act, DECISION-2 of run
`APP-V4-SCA002-20260929`):
- the exact amendment in BASIS_AMENDMENT.md (sha256 `091871fd…4238`),
  SOW_REVISIONS.md (sha256 `440d4d50…d00d`) and ARC_EFFECT.md (sha256
  `4b3aeec0…ddc0`), rendered in
  `SCA-V4-002_2026-09-29_1901/Amendment_Preview.md`; B-04 and C-01
  acceptance-conditional; B-06a timed with the SoW REVISEs;
- the register `SCA-V4-002_2026-09-29_1901/Amendment_Actions.csv` at SHA-256
  `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`, 16 rows;
- `Supersession_Delta.csv` (18 rows) and `Propagation_Plan.md` (Q-3 write
  boundary and route);
- Q-3, Q-8, Q-9 and Q-14, and the exact text behind Q-4, Q-6, Q-7 and Q-10
  to Q-13,

as bounded in its `DECISION.md` and `ACCEPTED_MANIFEST.csv`.

**Next:** checkpoint-group-3 preparation in the candidate
`SCA-V4-002_2026-09-29_1901/` (posture `ACCEPTED_PREDECESSOR`; predecessor
`SCA-V4-001_2026-09-28_2155`): apply the non-conditional edits, recompute the
31 HOST_INTEGRATION rows of `Consolidated_Coverage.csv`, accumulate the
supersession map, run the post-change audit over the baseline's seven
packages, check DAG-002 currency, and dispatch the independent review.

**Limits.** This pointer is amendment-qualified. It is not `_LATEST.md`. It
authorizes no B-04, C-01 or B-06a application, no ScopeOfWork REVISE, no
dependency-register, DAG or lifecycle change, and no accepted `SCA-*`
snapshot before group-3 acceptance.
