# D-GOV-31 — Merge-Gate Policy Succession (dual D-8 successor candidates)

> **Status: DUAL CANDIDATES — NOT SELECTED, NOT RULED.** This packet and
> every file beside it are proposals. They bind nothing (K-AUTH-1). File
> creation, hashing, validation, commit, Git transport, or review is not
> selection and not adoption. No owner selection, ruling, or adoption is
> contained anywhere in this package. The live `docs/PRD_ROOT.md` D-8 row
> ("never self-merge") remains fully in force.

| Field | Value |
|---|---|
| Provisional decision ID | D-GOV-31 (verified next-free at the candidate basis; rationale in §2) |
| Candidate basis | `main@4f7808acb2802443370d045efa198152934c1674` |
| Prepared by | Bounded Agent 2 AUTHOR run `GOV-STEP3-D8-CANDIDATES-20260729`, HELPS_HUMANS lane, supervised by HELP_HUMAN (Agent 0 session of record) |
| Artifact class | proposal package; two complete, separately hashed candidates; non-authoritative |
| Date | 2026-07-29 |
| Record convention | exact-candidate-SHA; supersede-never-edit after ruling |
| Decision record | **not yet created** — per the D-GOV-28 precedent the D-GOV-31 decision record is created at adoption, and the `_DECISIONS/_REGISTER.md` row arrives with it; this tranche adds no register row |

## 1. What is superseded, and why now

The subject is one stable Root product commitment, `docs/PRD_ROOT.md` §5.3
row D-8 (line 454 at the candidate basis), verbatim:

```text
| **D-8** | Git closeout runs through the change-management role with human-gated PRs; **never self-merge**. | TRANSCRIBED — `execution/_Coordination/LOOP_INIT.md` §7; standing workplan §Closeout; K-MERGE-1 |
```

Its recorded sources are `execution/_Coordination/LOOP_INIT.md` §7
(line 126: "use CHANGE for Git closeout; never self-merge."), the standing
workplan closeout section, and invariant K-MERGE-1 (`docs/CONTRACT.md`
line 115). D-13 permits amending the adopted PRD only by a superseding
instrument bound to a git SHA; D-1 permits exactly two change vehicles —
superseding a `D-GOV-*` record, or PR review. This package uses the first,
via the exact-candidate-SHA pattern established by D-GOV-28
(`docs/governance_harness/_DECISIONS/D-GOV-28_root_runtime_stewardship.md`
and its `_PROPOSALS/D-GOV-28_root_runtime_stewardship/` package).

Why a successor is due now, on the record:

1. **The disclosed conflict.** D-GOV-30 placed the verified facts of the
   2026-07-28 merge window (PRs #389–#408) into the governance record:
   author equal to merge actor 20/20 against the then-live D-8; K-MERGE-1
   10 SATISFIED / 10 NOT_EVIDENCED per the frozen matrix at
   `execution/_Evaluation/MERGE_APPROVAL_MATRIX_2026-07-28_85EA0628/`.
   Those acts stand as disclosed procedural exceptions under a recorded
   owner direction — expressly without retroactive cure and expressly
   without amending D-8. The rule and the owner's working practice are
   therefore in recorded, unreconciled tension.
2. **The routed requirement.** The post-remediation horizon package
   (`execution/_Evaluation/CHIRALITY_PROGRAM_POST_REMEDIATION_HORIZON_2026-07-28_85EA0628/`)
   found `HZN-001`/`HZN-002`: no successor exists, and one is
   `NECESSARY_BEFORE_NEXT_WORK` that would rely on a changed self-merge
   posture. Its `HANDOFF.md` enumerates the exact pending input this
   package now supplies, and its return at
   `execution/_Evaluation/CHIRALITY_PROGRAM_POST_REMEDIATION_HORIZON_2026-07-28_85EA0628/returns/HZN-GOV-01/RETURN.md`
   carries the candidate feedback checklist both candidates were drafted
   against.
3. **The owner's recorded policy intent** (§3) calls for normalizing a
   bounded exception while keeping the permission default.

This package prepares the successor as **two complete candidates** and
stops. Selection, horizon rerun, adoption, propagation, and publication
are all later, separately gated acts (§6).

## 2. Candidate-ID discipline — why this instrument is numbered 31

At the candidate basis the `_DECISIONS/` series ends at D-GOV-30, ruled
2026-07-28 and merged to `main`. The immutable OD7-G1 packet
(`docs/governance_harness/_PROPOSALS/OD7-G1_program_record_closeouts_2026-07-27/PACKET.md`
§3) records `D-GOV-29` as its scan's next-free observation; that claim is
left byte-for-byte untouched, `D-GOV-29` remains available to later
OD7-era work under the numbering discipline D-GOV-30 established, and this
instrument takes the next unclaimed identifier, `D-GOV-31`. A deterministic
scan at the basis finds no existing `D-GOV-31` reference in `docs/`,
`execution/`, or `agents/`.

## 3. Owner's recorded policy intent

The owner directed, in-session during program planning (loop-readiness
transition program, HELP_HUMAN session of record; transcribed by the
session and carried here under the OWNER_DECLARED discipline — an owner
act of record whose exact wording is subject to owner confirmation at
adoption):

> Requiring permission to merge is sometimes what I want (especially early
> into some work) and self-merging is sometimes what I want (especially as
> work has progressed to the point I don't perceive much risk in
> self-merge). … Keeping the default as needing permission should continue
> for now but taking exception, when the agent has explicit approval to do
> so, should also be normalized.

Both candidates carry this intent identically: the default stays
human-gated; a bounded, recorded, expiring owner grant normalizes the
exception; and execution authority is never semantic approval.

## 4. The two candidates

Each candidate is a complete Rev 7 PRD revision produced by copying the
live `docs/PRD_ROOT.md` at the candidate basis (SHA-256
`0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`) and
changing only the declared delta: the D-8 row, a new annex §5.3.1 carrying
the policy, and the minimally necessary provenance-key and document-control
reconciliation. Each candidate's `POLICY_DELTA.md` declares the exact
changed-line set and the propagation table; each candidate is independently
complete and never refers to the other for content. The two differ in
exactly seven scope-bearing lines.

| Identity | Candidate A — ROOT-ONLY | Candidate B — SHARED-CHANGE-POLICY |
|---|---|---|
| Scope | Root-loop Git closeout only; other loops' merge discipline unchanged, under their own instruments | Shared CHANGE role behavior across all registered loops; M6-notice propagation obligation; stricter local discipline controlling until each loop adopts or acknowledges under its own instruments |
| Package path | `CANDIDATE_A_ROOT_ONLY/` | `CANDIDATE_B_SHARED_CHANGE/` |
| Subject (PRD candidate) SHA-256 | `d21a2d8d4bc2deb2a32dbe4936f1e4647efabac24158adeae4f45fa4a18d8d35` | `15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748` |
| `POLICY_DELTA.md` SHA-256 | `5b4a7c18219d7456afa0308a2ccb962ff425b960518cfd27292feefef3b44cbe` | `6f21bc06cbcdec6b4321496c626a80be656efe484fe63e05e7f67b3b1137cd4d` |
| `ARTIFACT_HASHES.sha256` SHA-256 | `61697d4345811dd4778ddcff835bd0d11dff8b613b9ac7591a725ce7b2628122` | `67febe11cdccea2db043b526100d415ad7a31cc44450133eea8a8590af0a3cac` |
| Propagation obligations enumerated | 7 (plus one express non-obligation) | 9 (plus one express non-obligation) |

The subject of any later `SELECT` or `APPROVE` token is the PRD candidate
file identified by its SHA-256 above, within the containing candidate
commit assigned at Git closeout.

## 5. Mandatory policy content — carried identically by both candidates

Both candidates' annex §5.3.1 carries, in normative text:

1. the unchanged human-gated default (permission to merge required absent
   a grant);
2. the bounded owner grant with mandatory fields — authoring actor, merge
   executor, scope, duration, expiry, exclusions — recorded before or at
   exercise (OD-style transcription or PR-carried), never after;
3. the key sentence: "A bounded owner grant may authorize merge execution
   within its recorded scope and term. It never constitutes semantic
   approval of future unknown content. Each merge still requires a human
   approval vehicle bound to the exact source HEAD, verification that HEAD
   remains unchanged, and a separately recorded effective merge identity.";
4. the four distinct closeout identities — semantic approval, approved
   source SHA, merge authorization, effective merge SHA — introduced as
   the successor discipline to "never self-merge" (the prior corpus
   conflated them; no merger-versus-author test ever existed as a
   deterministic check);
5. the owner token grammar, living in the policy and never in
   transcription records;
6. the express exclusions (no agent-authored semantic auto-approval; no
   content mutation after approval; no force push, rebase, or invented
   conflict resolution; no authority beyond scope and expiry; no lifecycle
   or issuance authority merely from merge permission);
7. K-MERGE-1 unchanged with strengthened evidencing: the approved source
   SHA pinned in a durable record before merge, curing the NOT_EVIDENCED
   failure mode documented in the frozen merge-approval matrix.

## 6. Selection → horizon → adoption pipeline

From the approved program plan (Step 3 of the loop-readiness transition
program, as carried in this run's dispatch brief of record):

> prepare both → commit/hash both candidate-only → owner selects one
> without adoption → HZN-GOV-01 rerun against the selected committed
> candidate → resolve findings → owner adopts → publish through human
> merge

The horizon package's rerun procedure, quoted verbatim from
`execution/_Evaluation/CHIRALITY_PROGRAM_POST_REMEDIATION_HORIZON_2026-07-28_85EA0628/HANDOFF.md`
§Rerun:

> 1. Run `HZN-GOV-01` against the exact committed candidate before
>    adoption.
> 2. If adopted, recheck the exact final bytes, application identity, and
>    resulting SHAs.
> 3. Present the governance result and boundary findings for owner
>    disposition.
> 4. Only then prepare the exact comparison-HTML revision and route its
>    separate CHANGE closeout.

Pipeline discipline:

- **Selection is not adoption.** An owner `SELECT` token against this
  packet chooses which committed candidate proceeds to the horizon rerun.
  It adopts nothing and changes no live surface. The token is lawful here
  because both candidates, their SHA-256 identities, their scopes, and the
  selection's effect are pre-fixed in this immutable packet — consistent
  with the token-grammar rule the policy itself carries.
- **The D-GOV-31 record is created at adoption**, per the D-GOV-28
  precedent, binding the ruling to the exact candidate SHA; the register
  row arrives with it. Until then this package is discoverable through
  `_PROPOSALS/` only, by design.
- **Publication runs under the still-current D-8**: the adoption and
  application PR is human-gated and is not self-merged. The successor
  never consumes its own not-yet-effective merge exception.

## 7. Propagation obligations — enumerated, not performed

Adoption of either candidate creates follow-on obligations that are
Step-4 work by other owners. They are enumerated with verified locations
and owners in each candidate's `POLICY_DELTA.md` §4 (seven rows for
Candidate A; nine for Candidate B, which adds the shared CHANGE
instruction surfaces and the routed M6 notices to every registered loop).
Nothing in this package performs any of them. Expressly a non-obligation
in both candidates: SHA-pinned historical mirrors, frozen proposal and
evidence packages, receipts, and OD transcription records are not
rewritten.

## 8. What this package does not do

- No owner selection, ruling, or adoption; no ruling slot is filled
  anywhere.
- No edit to `docs/PRD_ROOT.md`, `execution/_Coordination/LOOP_INIT.md`,
  `docs/CONTRACT.md`, `agents/AGENT_CHANGE.md`, any register, receipt,
  decision record, or any other existing file.
- No D-GOV-31 decision record and no `_REGISTER.md` row — both are
  created at adoption.
- No retroactive cure of, or compliance claim about, the 2026-07-28 window
  or any other historical act.
- No grant is issued, exercised, or pre-approved; no merge is authorized.
- No loop-local App, PEC, or Piping substance; Candidate B's cross-loop
  effect is prospective and notice-mediated only.
- No decomposition, scope, lifecycle, activation, implementation, runtime,
  dependency, estimate, schedule, repin, release, or
  professional-reliance act.

## 9. Package hash manifest discipline

Each candidate folder carries `ARTIFACT_HASHES.sha256` over its own two
content files, written after those files were final. The package-level
`ARTIFACT_HASHES.sha256` beside this packet covers this `PACKET.md` and
both candidates' hash manifests, and is written last. The packet is not
edited after the package-level manifest is written; any later correction
is a superseding act.
