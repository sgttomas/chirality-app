# Simulated post-acceptance audit — SCA-V4-003 (node AK1-R)

**What this is.** H-1 and H-2 were applied to a scratch copy of the
candidate as revised for V24 M-1, and the unchanged audit was run on it. This
checks that the group-3 package's records and pointer parse once applied.
- The scratch copy was taken from the working tree after the AK1-R record
  revision.
- Nothing in the repository was edited by the simulation; it wrote only
  under the session scratchpad.
- It is a simulation, not the H-3 record; H-3 runs after the real act.

| Item | Value |
|---|---|
| Script | `simulate_postaccept.py` (sha256 `8a39a7de4346b18198aa1d4c9820e9933bc31c1d9b2950c4b8fc74964fba08dd`) |
| Output | `simulated_postaccept.json` (sha256 `48e7713a8622f3e80558932a0efc0f0c8910839a7d728c41465a26e0fed5a526`) |
| Audit script | `RUN/BASELINE/audit_checks.py`, unchanged (`8c3bef06…b0d3`); `tools/evaluation/audit_structure.py` (exit 0); inventory as POSTCHANGE |
| Scope | PKG-01, 02, 03, 04, 05, 09, 10 |
| H-1 (test date `2026-10-03`) | `SOFTWARE_DECOMP.md` `ea3388bc…d7d5` → `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`; old block once; exactly 2 lines added (entry and blank); no `{` left |
| H-1 expected result by act date | `2026-10-03`: `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`; `2026-10-04`: `54d7cb4f67773bde9fb5c9f550dd6ca246b806393d6681fde755a8b10c2c9583` (only `{ACCEPT_DATE}` varies) |
| H-2 | `_ScopeChange/_LATEST.md` `2b7938bc…c2e1` → test bytes (`{UTC}` = placeholder `20261004T120000Z`, so the hash is not a prediction); registered `_latest_pointer_target` = `SCA-V4-003_2026-10-03_1827`, `_pointer_matches` True |

## Result

**0 BLOCKER, 51 WARNING, 77 INFO.**

- **Check 10:** `active_snapshot_status` PASS and `handoff_state_status`
  PASS. The active snapshot is `SCA-V4-003_2026-10-03_1827`; no required
  artifact is missing and there is no residue.
- **Closure verdict read:** `OPEN_PENDING_DERIVATIVE_CLOSURE`. State fields
  are single-valued and allowed.
- **Registered pointer parser:** target SCA-V4-003, match True.

**Against POSTCHANGE (0 / 52 / 77):**
- COV-129 is absent; the records exist.
- COV-123 (INFO) changes only its working `SOFTWARE_DECOMP.md` hash, from
  `ea3388bc` to `983199cc` (H-1).
- Every other issue is identical, and the Matrix is identical.

**Without the M-1 line** (V24's run on the committed records), the same
simulation gave 1 BLOCKER (closure verdict []). The fix is confirmed.

**Known wording limits** of the unchanged script, disclosed and not edited
(m-1):
- COV-121 and COV-123 attribute the working-vs-GROUP3 differences to the
  SCA-V4-001/002 registers only.
- `expected_source.predecessor_amendment` stays SCA-V4-001.
- The parity extension lists `SOFTWARE_DECOMP.md`, `_ScopeChange/_LATEST.md`
  and `Open_Issues.csv` as differing from SCA-V4-002's accepted poststate.
  This is expected for the SCA-V4-003 edits.

**Not simulated:** F-1 to F-4. They write records the audit reads only for
file presence, the closure verdict and the state fields, which the candidate
records already carry in parsable form. When F-3 and F-4 change those values,
each must stay single-valued in the two files.
