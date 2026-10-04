# RV3-CA1 — review of DEL-11-01 CA-v0.1 (unit EU-F2, owner O-F)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit (B-18). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct.
- **Unit**, as `O-F.md` "EU-F2 — frozen". Committed in `f324107696`; `git status --ignored` on DEL-11-01, DEL-11-03 and `F/` is clean. Re-hashed:
  - `CONTINUITY_ACCOUNT.md` `1a4a0ca6…6ab2`;
  - `ca.continuity-account.schema.json` `bf973751…`;
  - `F/ca/build_ca.py` `eb36d829…`, `check_ca.py` `7a04f752…`;
  - `F/ca/vendor/VENDOR.json` `3502235f…`;
  - `F/ca/records/MANIFEST.sha256` `3107f652…` (both records `OK`).
- **Basis read:**
  - DEL-11-01 `ScopeOfWork.md` (`272f7622…`, which matches the pin);
  - `reference/REFERENCES.md` §1/§2, `ARCHIVES.md`, `archive_digests.py`, `SOURCE_INVENTORY.md`;
  - PRD §11;
  - `conceptual/DECISIONS.md` (OD-09) and this run's `OWNER_DECISIONS.md` "Direction";
  - DEL-10-03 RA-v0.1 and RA-v0.2 (X-1, §4.2);
  - DEP-006, OI-024;
  - R23-32 F-R6/F-R7/F-R8/F-R11 and R23-44.

## Verdict: **READY**

There are no BLOCKING or MAJOR findings. There are 2 MINOR findings and 2 NOTEs.

The account is a linked view (F-R6): it links the primary records by git identity and adds only standing, selector, route, owner and point of need. Every check it calls real is real, and I reproduced each one independently. No lane is eligible for retirement. Both owner acts are quoted exactly.

## Real checks, reproduced

| Check | My run | Result |
|---|---|---|
| Commit | `git cat-file -t 22ed9383a4…` | A commit, and an ancestor of HEAD |
| C-1: v3.0.1 against REFERENCES §2 | REFERENCES §2 names source `485051eac923…` and installer `eea43a0d…`. `git show 485051eac9:projects/chirality-app-dev/frontend/package.json` gives `"version": "3.0.1"`. The source is an ancestor of `22ed9383a4` | **matches**. The remote is not re-checked (no network), as stated |
| C-2: App v3 lane | `git rev-parse 22ed9383a4:projects/chirality-app-dev` gives `3fb53704…`; `git rev-list --count 485051eac9..22ed9383a4 -- projects/chirality-app-dev` gives **225** | **passed**, active |
| C-3: archives | `archive_digests.py verify`. The script is read-only in `verify` mode (only `record` writes); I read it first. Output went to my scratch only | **19 of 19 OK, exit 0**, "All recorded archives unchanged." No archive path is repeated here |
| C-4: thesis | Tree at `22ed9383a4` and at HEAD: `47fc49e96c2931ba18090f1a82d56a49f230b3ee` (19 files). This equals PRD §11 l.511. `git status --porcelain --untracked-files=all` under the thesis is empty | **matches** |
| C-5 | `2b0572fe04` is a commit, and REFERENCES §1 names `2b0572fe049c8ffaa02d61b7dbbc3ae41bc589f6` | **passed** |
| C-6 | Tag `archive/agent-runs-2026-09-25` (object `13af3862…`) peels to `8007c592…`, as REFERENCES states | **matches** |
| Linked-record hashes | REFERENCES, ARCHIVES, SOURCE_INVENTORY, PRD, OPERATING_METHOD and DECISIONS | All equal the account's pins |
| `check_ca.py` | Rerun | **21/21**, plus a NOTICE (see CA1-N1) |

## Obligations and owner acts

- **No lane is eligible.** In the built `CA-1.continuity-account.json`, all four lanes (App v3, Runtime, SWBPIPE = `projects/chirality-piping`, Root) have:
  - `retirement_intended: false`;
  - `continuing_obligations: not_supplied`;
  - `disposition: null`;
  - `retirement_eligible: false`.

  The lanes are DEP-006's (Root/Runtime/App/Piping), matching RA X-1. RE-1 is enforced by the schema: N-2 and N-3 are refused. N-1 confirms that a decided replacement makes no lane eligible.
- **OD-09.**
  - The exact text "Preserve the old projects and archives until I decide v4 has replaced the fallback." is the third quoted sentence of DECISIONS.md row OD-09 (verified).
  - The actor is the owner.
- **Direction item 2.**
  - The exact text "1 yes, 2 no rewrite, 3 go, 4 A+C" is in `OWNER_DECISIONS.md`, with Effect "2: git history is not rewritten …".
  - The recorder is HELP_HUMAN; the actor is the owner.

### CA1-R1 — MINOR — OD-09's recorder is stated as a fact the record does not state

- **Claim (record).** `"recorder": "the v4 conceptual undertaking's recorder (conceptual/DECISIONS.md)"`.
- **Evidence.** DECISIONS.md says its OD entries quote "the owner's opening message to HELPS_HUMANS in the session that created this working root (preserved verbatim in the run record, `OPENING_BRIEF.md`)", and that "The quotations below are exact; the grouping and IDs are the agent's". It does not name a writer.
- **Consequence.** The actor ≠ recorder property is real in substance, since the owner did not write the file. But the recorder field asserts an identity that no record states. This is the same pattern as EB1-R8.
- **Repair.** Record "the agent of the session that received the owner's opening message to HELPS_HUMANS; the record does not name its writer", and cite `OPENING_BRIEF.md` as custody.
- **Note on the check.** K-9's actor-≠-recorder test is a string inequality, so it would pass any recorder text other than "the owner". Say so as a limit.

### CA1-R2 — MINOR — OD-09 is quoted in part, and its other two sentences bear on C-1/C-5 and C-3 (§5)

- **Evidence.** Row OD-09 also says "Pin the investigation revision separately from the published v3.0.1 fallback release … Preserve both references." and "Inventory relevant Git-ignored archives in the original checkout … and establish stable read access."
- **Consequence.** Not wrong, but the account cites only the retention sentence, while C-1, C-5 and C-3 rest on the other two.
- **Repair.** Name all three sentences, or say which classes each one supports.

## Notes

- **CA1-N1 — vendored DEL-10-03: re-pin needed, no content effect.**
  - `check_ca.py` prints "NOTICE live ra moved since vendoring (531b65b7b63f -> 811c868cf468)".
  - The vendored copy (`531b65b7…`) is RA-v0.1, the bytes O-E froze and committed at `caed56b8ea`. The live file is RA-v0.2 (`811c868c…`, committed `ce64a97a2a`).
  - I compared RA-v0.1 and RA-v0.2: §1.3 (X-1…X-5) and §4.2 are **byte-identical**. RA-v0.2 changes only S-6's ACT pin, F-RA1's wording and `ra_check`.
  - So the lane basis K-10 reads is unchanged, and the re-pin is bookkeeping. Re-pin to `811c868c…` (R23-21).
  - Also correct the stale wording in three places: VENDOR.json's "not frozen, untracked when vendored", CA's header "RA-v0.1 draft (O-E, not frozen)", and O-F's limit CF-5 "an unfrozen draft". True when vendored, RA-v0.1 has since been frozen and committed, and superseded.
- **CA1-N2 — K-3 depends on the original checkout.** K-3 rebuilds at the commit and reproduces the account, archives included, only where the original checkout is present. CF-1 states that elsewhere C-3 is `not_run`, never `changed`. That is correctly bounded.

## Not checked

- `build_ca.py`'s determinism.
- The five schema negatives individually: they ran inside `check_ca.py`, 21/21.
- The thesis front matter (U-CA-5, declared).
