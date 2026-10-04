# RV3-AA1 — review of DEL-11-02 AA-v0.1 (unit EU-F3, owner O-F)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit (B-18). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct.
- **Unit**, at `b2fbfdbac8`, which is HEAD. `git status --ignored` on the PKG-11 and `F/` paths is clean. Re-hashed, all as in `O-F.md` "EU-F3 — frozen":
  - `ADOPTION_ACCOUNT.md` `583637e3…b878`;
  - `aa.adoption-account.schema.json` `0fd3c573…`;
  - `F/aa/build_aa.py` `4b435bee…`, `check_aa.py` `a5d5feee…`;
  - `F/aa/records/MANIFEST.sha256` `3ea37d11…`.
- **Checks rerun:** `check_aa.py` **19/19**; `check_ca.py` 23/23; `check_rp.py` 76/76.
- **Basis read:**
  - DEL-11-02 `ScopeOfWork.md` (pin `2d962646…`);
  - Root `AGENTS.md` before and after `7bd2283dbc`;
  - the D-GOV-52 tranche manifest and the three notices;
  - R23-30 and R23-32 (F-R9, F-R10, F-R11, F-R16);
  - `OWNER_DECISIONS_2.md`;
  - DEL-10-03 RA-v0.2 X-1;
  - `exports/chirality-app/export-manifest.csv`;
  - ROLE-v0.2, HOSTING-v0.9 and ACCESS-v0.2 at the commit.

## Verdict: **REPAIR**

There is 1 MAJOR finding, 2 MINOR findings and 3 NOTEs.

The real case is read correctly from the files and git, A-1 is recorded faithfully, and the built record AA-1 makes no false claim. But the separation of the eight facts, which is the account's central guarantee ("Evidence for one fact never establishes another"), is not enforced by its checks. It holds today only because the builder is honest (AA1-R1).

## Findings

### AA1-R1 — MAJOR — the separation rules do not keep the facts apart: evidence for one fact passes as another, including for `consumer_adopted` (§3 SR-1…SR-4; `check_aa.separation_errors`; schema)

- **Claim.** §3: "Evidence for one fact never establishes another"; SR-1…SR-4 are "checked by `check_aa.py` K-6".
- **Evidence.** I built five in-memory variants of the real `AA-1.adoption-account.json` and ran `check_aa`'s own schema validator, `separation_errors`, `evidence_errors` and `act_errors` on each. **All five pass every check (0 schema errors, 0 SR errors, 0 evidence errors, 0 act errors):**
  1. **App v3 `supplied` established by the delivered notice file.** Delivery evidence passes as supply. SR-1 only rejects `manifest_statement`/`git_commit`, and SR-2 only rejects the *publication* refs.
  2. **App v3 `observed_behavior` established by an `absence_search`**, the "found nothing" evidence.
  3. **Piping `delivered` established by the tranche manifest's statement alone.** Routing passes as delivery, because SR-1/SR-2 do not cover `delivered` or `prepared_notice`.
  4. **App v3 `consumer_adopted` established by an `agent_act`** with `consumer_id: APP-V3` whose exact text is R23-32 F-R16's "notice delivered; receiving decision not recorded". The text is found in its record, so K-5 passes, and SR-3/SR-4 pass because they check only that *an* act exists and names the consumer.
  5. **Runtime `consumer_adopted` established by the owner's approval A-1**, copied with `consumer_id: RUNTIME`.
- **Consequence.**
  - The guarantees REQ-001 and CLM-005 rest on are claimed but not implemented.
  - The most consequential fact, `consumer_adopted`, can be established for a loop whose records show no adoption. This can be done from an act whose text says the opposite (variant 4), or from a Root-level human approval rather than the receiving loop's act (F-R10; variant 5).
  - The present record is correct, but a later version, or a consumer of the status hand-over (CA, RP), would inherit any such error unchecked.
- **Repair.**
  - **A whitelist of evidence kinds per fact, enforced by the schema or SR:**
    - `prepared_notice`: manifest statement;
    - `delivered`: a `file_at_commit` under the receiving lane's path;
    - `published`: the change bytes or a commit;
    - `resolved`/`supplied`/`provider_adopted`/`observed_behavior`: candidate or observation evidence only, never a notice, an absence search or a manifest statement;
    - `consumer_adopted`: an `act`.
  - **Stronger SR-3:** the cited act must be `kind: agent_act` or a receiving loop's own act, with an `actor` that is that consumer's loop (or its integrator), and a `subject` stating adoption. Never a `human_act` approval of the change itself (F-R10).
  - **Add N-cases** for the five variants above.

### AA1-R2 — MINOR — the status statement says App v3 and Runtime "received a notice"; the evidence shows delivery, not receipt (`AA-1.status.json` `statement`; carried into CA-1 `adoption_status.ref` and RP-v0.5 `adoption.statement`)

- **Evidence.**
  - The facts record `delivered: established`: the notice file exists in each lane's `_Coordination` at the commit, placed there by the sending tranche.
  - AA's own limit says "Whether a loop read its notice is not observable (U-AA-1)".
  - R23-32 F-R16's agreed wording is "notice delivered; receiving decision not recorded".
- **Consequence.** The one sentence the owner-facing packet repeats claims slightly more than the evidence: a reader may take "received" as acknowledgement by the loop.
- **Repair.** Use "a notice was delivered to App v3's and Runtime's coordination folders; no receiving decision is recorded" (F-R16). This flows unchanged into CA and RP at their next build.

### AA1-R3 — MINOR — RN-2's Root search is scoped to `AGENTS.md` only (record `rows[RN-2/ROOT]`)

- **Evidence.**
  - The recorded `absence_search` is `git grep -F 'APP-V4-BASIS-20260926' 122c5abcf5 -- AGENTS.md`, whereas the other lanes search their whole project folder.
  - Root's governance lives in `docs/`, `workflows/`, `docs/governance_harness/` and elsewhere.
  - I widened it: `git grep -F 'APP-V4-BASIS-20260926'` at the commit over the whole repository *outside* `projects/chirality-app-v4` finds **nothing**.
- **Consequence.** The conclusion (not established) stands. But the recorded evidence covers less than the claim for the Root lane.
- **Repair.** Record the search over Root's governance paths, or the whole tree excluding the App v4 project, and state the scope.

## Notes

- **N1 — AD-1's actor and recorder are the same agent.** Actor "HELP_HUMAN, as App v4's integrator (R23 rulings)" and recorder "HELP_HUMAN". For an agent's own ruling this is direct capture, which ACT's A9 permits, and K-5 applies its distinctness rule to human acts only. It is truthful as written, with `recorder_stated_by_record: true` and R23's header reading "Integrator: HELP_HUMAN". Say "direct capture" explicitly, so the reader does not expect a separate recorder.
- **N2 — `owner_record` (RP-v0.5 S-4, S-6 standing) is undefined.** In the schema it is a bare enum value. Here it means "the owning deliverable's record" (DEL-11-01, DEL-11-02), not a record of the person. Define it in the legend or terms, since owner-facing packets reserve "owner" for the person.
- **N3 — `PLACEHOLDER_RE` in RP-v0.5** (`illustrative|invented|example|placeholder`) derives `identified` from keywords. A placeholder spelled otherwise ("TBD", "xxx") would pass. The other derivation conditions (unresolved steps, supplied standings) still hold the illustrative fixture, so this is a limit to state, not a defect now.

## The brief's questions

- **Do the eight facts stay separate in practice?** In the built record, yes: each established fact cites its own kind of evidence, and none is established from another's. In the checks, no (AA1-R1).
- **Is the D-GOV-52 case read correctly?** Yes. Checked by me in git at `122c5abcf5`:
  - Root `AGENTS.md` went from `c8ce87ef…` to `f96feb19…` at `7bd2283dbc`, and the export manifest row is `AGENTS.md,14481,f96feb19…`.
  - **App v4:** the notice is `a643415c…`, and R23-30 l.332 reads "App v4 adopts the changed Root text.". Supply, provider and behaviour are not established, with no candidate. ROLE_SUPPLY.md, HOSTING_BOUNDARY.md and ACCOUNT_AND_PROVIDER_ACCESS.md contain no "D-GOV-52" or "R23-30" at the commit or now, so "pending next revision" is correct.
  - **App v3 and Runtime:** one notice each, byte-identical (`5f4fb4d9…`). It is the only D-GOV-52 mention in each lane, and **0 commits** touch either lane after the tranche. The quoted notice line ("This loop: both edits are consistent with the v3 idle-boundary path and RB-SETTINGS. No adoption work is expected.") is verified, and is correctly attributed to the sending tranche.
  - **Piping:** no notice, no mention, and 3 commits after the tranche (piping fixes and PR #1080 merge), none mentioning D-GOV-52.
  - **PEC:** no notice, no mention, 0 commits.
  - The manifest's "hold no pin or copy … read Root AGENTS.md live" is quoted and kept `unknown`, not observed.
- **A-1.**
  - Exact text "I approve A1 and B1, go ahead" (OWNER_DECISIONS_2.md, verified).
  - Actor: the owner.
  - Recorder: HELP_HUMAN, `recorder_stated_by_record: true`.
  - Custody: "the session transcript; recorded by HELP_HUMAN (the file's own custody line)", matching the file's header.
  - **Truthful.** Its `subject` paraphrases the terms partially (the notice routing). The other terms (no separate ruling record, export regeneration, U-A9) are in the record it cites.
- **Anything claiming more than the evidence?**
  - The built record does not overclaim: RN-2 has no adopter, packaging is "publication not established", and currency is "no reliance, so no comparison".
  - The status sentence's "received" does (AA1-R2), and the separation guarantee does (AA1-R1).
- **Consumers.** RN-2's four consumers (Root, Runtime, App v3, Piping) equal RA-v0.2's X-1 and DEP-006 (K-7).

## How I checked

- Hash and status checks.
- Reran all three checkers.
- `git show`/`git grep`/`git rev-list --count` at `122c5abcf5` for each lane.
- Five adversarial variants run through `check_aa`'s own functions (scratch, in memory; no file written).
- A repository-wide basis-id search.
- Grep of the three derivative Design files at the commit and now.

## Not checked

- `build_aa.py`'s determinism.
- The schema's other negative cases individually (they ran inside `check_aa`, 19/19).
