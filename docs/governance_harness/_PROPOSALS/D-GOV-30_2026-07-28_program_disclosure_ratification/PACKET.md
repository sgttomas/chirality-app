# D-GOV-30 — Program Disclosure and Prospective Ratification

> **Status: CANDIDATE — AWAITING_RULING.** This packet and every file beside
> it are proposals. They bind nothing (K-AUTH-1). File creation, hashing,
> validation, commit, Git transport, or review is not a ruling. The owner
> ruling is recorded later, in-session, in the D-GOV-30 decision record
> against this packet's immutable bytes.

| Field | Value |
|---|---|
| Candidate decision ID | D-GOV-30 (numbering rationale in §3) |
| Candidate basis | `main@85ea0628fa4e57dd6aae53b06139b2b8734a9612` |
| Prepared by | Bounded Agent 2 AUTHOR run `GOV-STEP2-ROOT-20260728`, HELPS_HUMANS lane, supervised by HELP_HUMAN (Agent 0 session of record) |
| Artifact class | proposal package; non-authoritative |
| Date | 2026-07-28 |
| Record convention | exact-candidate-SHA; supersede-never-edit after ruling |
| Decision record | `docs/governance_harness/_DECISIONS/D-GOV-30_program_disclosure_and_ratification.md` |

## 1. Purpose

D-GOV-30 does two things and only two things:

1. **Disclosure.** It places the verified facts of the 2026-07-28
   architecture-remediation merge window (PRs #389–#408) into the Root
   governance record, exactly as evidenced, with no softening and no
   overclaim.
2. **Prospective ratification.** It presents four enumerated present-state
   items for an owner ruling that accepts each — individually declinable —
   as the current governed state going forward.

**No retroactive cure.** The 2026-07-28 self-merges are **disclosed
procedural exceptions** performed under a recorded owner direction. This
record never claims they complied with D-8 (`docs/PRD_ROOT.md` §1, table
row D-8: "never self-merge") or `execution/_Coordination/LOOP_INIT.md` §7 as
then in force. Nothing here converts the historical acts into compliant
acts. The ruling, if given, ratifies the **present state** prospectively.

## 2. Owner direction of record — cited by reference

The blanket direction that authorized the window is already transcribed
verbatim in
`execution/_Coordination/CHIRALITY_PROGRAM_ARCH_REMEDIATION_CLOSEOUT_2026-07-28.md`
(§"Owner ruling", the block-quoted direction beginning "Finish out your plan
now (attaining your goal) with self merge of PRs and auto approve for owners
rulings…"). That file's SHA-256 at this candidate basis is
`27c3e36cf11c94521a87eabb0f0dfd9563e42915aa8af9c87681f7f8776caaac`.
This packet cites that transcription; it does not claim to be the first or
canonical transcription, and it does not re-transcribe the direction as a
second authority surface.

## 3. Candidate-ID discipline — why this record is numbered 30

The immutable, hash-pinned OD7-G1 packet
(`docs/governance_harness/_PROPOSALS/OD7-G1_program_record_closeouts_2026-07-27/PACKET.md`,
§3) records `D-GOV-29` as the next Root decision-ID candidate observed by
its scan. That claim is left byte-for-byte untouched. This instrument takes
`D-GOV-30` so that it can coexist with — and, in item R-4, present for
approval — the OD7-G1 package without colliding with or superseding the
packet's recorded ID discipline. `D-GOV-29` remains available to later
OD7-era work if still free at its own rescan. Numbering past 29 supersedes
nothing.

## 4. Evidence basis — frozen, content-addressed

The disclosure facts in §5 are drawn from two frozen evidence packages
landing via the separate evidence PR (branch `gov/step1-evidence-landing`,
commit `02b1f091a`):

| Evidence package | Manifest | Manifest SHA-256 |
|---|---|---|
| `execution/_Evaluation/MERGE_APPROVAL_MATRIX_2026-07-28_85EA0628/` | `ARTIFACT_HASHES.sha256` | `53844bfdcedaf5bae4396241375deba5dd35cc5b6d483342efac4a28268fccc1` |
| `execution/_Evaluation/CHIRALITY_PROGRAM_POST_REMEDIATION_HORIZON_2026-07-28_85EA0628/` | `ARTIFACT_HASHES.sha256` | `a592b5094b4de86f6abda5faba5244588e8461c58eb29c3af332012351a1d7d6` |

Both packages are derivative evidence built over the frozen basis
`main@85ea0628fa4e57dd6aae53b06139b2b8734a9612`. They are cited as exact
SHA-256-pinned inputs; they are not decomposition truth and carry no
authority of their own.

## 5. Disclosure — the enumerated facts of record

The following facts are disclosed exactly as verified in the merge-approval
matrix. They are stated without softening and without overclaim.

1. **One owner act authorized the window.** The 2026-07-28 blanket
   direction (§2) is the sole authorization behind all 20 merges
   #389–#408. Every named per-decision ruling ID in the window is a
   recording vehicle for that one act, not an independent authorization.
2. **Zero GitHub reviews exist across the window.** The approval record is
   entirely in-repo, authored by the executing run.
3. **Author == merge actor on 20/20 PRs.** The actor `sgttomas` both
   authored and merged every PR in the window, against then-live D-8
   ("never self-merge", `docs/PRD_ROOT.md:454`, transcribed from
   `execution/_Coordination/LOOP_INIT.md` §7). The acts were authorized by
   the direction; the conflict remains unreconciled in the normative
   document.
4. **K-MERGE-1 (`docs/CONTRACT.md:115`): 10 SATISFIED / 10 NOT_EVIDENCED /
   0 VIOLATED.** The NOT_EVIDENCED rows — #391, #396, #398, #399, #400,
   #402, #404, #405, #406, #408 — pinned no approved source SHA, so the
   invariant is unfalsifiable there, not disproven. Git structure is clean
   on all 20 (merge^2 == headRefOid).
5. **PR #398 is an unforced mid-chain gap** (merge
   `2d6adab3a9c76e51b0f0349284715a5a5c9e3592`): no citing record exists
   for it.
6. **PR #408 is structurally self-ratifying** (merge
   `85ea0628fa4e57dd6aae53b06139b2b8734a9612`): the terminal closeout
   declares itself owner-approved-on-merge in the same commit.

The disclosure effect of this record does not depend on any ruling below.
Once published, the facts above are of record whether or not any R-item is
approved.

## 6. Informed-batch statement

The owner ruling sought here is an **informed batch**: it is taken over
frozen, enumerated, exact-SHA evidence (§4, §5, §7), with per-line decline
available on each R-item (§8). That is categorically different from
pre-authorization of unknown future content. This record is **not citable
as precedent for blanket approval** — neither for future self-merge, nor
for future auto-approval of rulings, nor for any batch whose subjects are
not frozen and enumerated before the ruling.

## 7. Ruling items

Each item below is individually declinable. "Accepted as current state"
means: the owner prospectively ratifies the named present state as the
governed state going forward. It does not assert that the acts that
produced the state complied with then-live procedure (§1), and it amends no
normative document.

Convention: the fenced blocks below are **marked ruling slots**. The
operative verbatim per-item rulings are recorded in the D-GOV-30 decision
record against this packet's immutable bytes; this packet is never edited
after hashing (supersede-never-edit).

### R-1 — RT-A trace-maintenance effective-state closeout

Accept as current state the Root trace RT-A effective-state closeout of
Root Receipt 57 lineage:
`execution/_Coordination/ROOT_TRACE_MAINTENANCE_EFFECTIVE_STATE_CLOSEOUT_2026-07-28.md`
(SHA-256 at this basis
`05d68b1f66c80fcc42f1a36eb3f71a0e5a6a45dfb37cf81c79fa1eab2450e645`),
including its recorded application commit, PR #389 merge ancestry, and
87-postimage byte identity.

Ruling slot (R-1):

<!-- BEGIN OWNER RULING VERBATIM -->
<<RULING PLACEHOLDER — OWNER RETURN VERBATIM: D-GOV-30>>
<!-- END OWNER RULING VERBATIM -->

### R-2 — Record-currency repair

Accept as current state the record-currency repair of Root Receipt 58:
`execution/_Coordination/PROGRAM_ARCH_REMEDIATION_RECORD_CURRENCY_2026-07-28.md`
(SHA-256 at this basis
`6a3504ca944772befb96c71cecead629943f46e1fd918d8c7ae46dcbc5ae9fe9`),
comprising the four approved pointer and closeout corrections it records.

Ruling slot (R-2):

<!-- BEGIN OWNER RULING VERBATIM -->
<<RULING PLACEHOLDER — OWNER RETURN VERBATIM: D-GOV-30>>
<!-- END OWNER RULING VERBATIM -->

### R-3 — Program closeout and terminal disposition

Accept as current state the program closeout and terminal disposition
`COMPLETE_FOR_ARCHITECTURE_REMEDIATION / PASS_WITH_BOUNDED_WARNINGS` of
Root Receipt 59, recorded in
`execution/_Coordination/CHIRALITY_PROGRAM_ARCH_REMEDIATION_CLOSEOUT_2026-07-28.md`
(SHA-256 at this basis
`27c3e36cf11c94521a87eabb0f0dfd9563e42915aa8af9c87681f7f8776caaac`).
Acceptance of R-3 explicitly closes, by enumeration, the two structural
gaps disclosed in §5:

- the **#398 citation gap** — PR #398, merge
  `2d6adab3a9c76e51b0f0349284715a5a5c9e3592`, previously cited by no
  record, is hereby named and enumerated by SHA; and
- the **#408 self-ratification gap** — PR #408, merge
  `85ea0628fa4e57dd6aae53b06139b2b8734a9612`, whose closeout declared
  itself owner-approved-on-merge in the same commit, is hereby presented
  to the owner as an enumerated subject of an independent later ruling
  rather than resting on its own declaration.

Ruling slot (R-3):

<!-- BEGIN OWNER RULING VERBATIM -->
<<RULING PLACEHOLDER — OWNER RETURN VERBATIM: D-GOV-30>>
<!-- END OWNER RULING VERBATIM -->

### R-4 — OD7-G1 tranche hash manifests — approval by SHA-256

Root Receipt 53 made the OD7-G1 Root packages "effective only after
explicit owner approval of both final hash manifests." R-4 presents
exactly those two manifests for owner approval by SHA-256. Both were
re-verified at this candidate basis: `shasum -a 256 -c` reproduces all 15
member hashes (15/15 OK).

**Manifest 1:**
`docs/governance_harness/_PROPOSALS/OD7-G1_program_record_closeouts_2026-07-27/ARTIFACT_HASHES.sha256`
— file SHA-256
`d6421ce6076238fd49dc0469d1160f8dc7698b2e730d8833e57136baaa957aa0`,
covering ten members:

| Member | SHA-256 |
|---|---|
| `BATCH_CANDIDATE_MANIFEST.csv` | `72203a8d682b28a4b905d33b09eb57e278fa4b44d16553d4254f06bcbe24e856` |
| `HANDOFF.md` | `b235d282da326c271f46ca7600103867fb5e570af48f3309b426e158e8984ad4` |
| `ID_SCAN.json` | `86c58999b11a55c32ec57c530bd8758d3a6db91a7436f6b705966cc69ae9eb32` |
| `PACKAGE_MANIFEST.json` | `b81bb00e2f0f405abd0dc19971515e969dd2e32362e2b593b3f7901f8c797d3b` |
| `PACKET.md` | `897c2b9304bcad01536707f47757d318f3ca7dd0bb75bcd3ef34ff195dc1b4d0` |
| `PROPOSED_NOTICE_D-GOV-26_DETECTOR_CLAIM_CORRECTION_2026-07-27.md` | `8dcacdaab7d5327e7fc630c500fd6bb26086854852722eab9078b1f1a1e936ae` |
| `PROPOSED_ROOT_MANIFEST_ROOT-OD7-G1-20260727.yaml` | `a900ff37bcbe7e9c4dae0a6f0d25284d6cd212c51328033c29e1fd569b10962d` |
| `PROPOSED_ROOT_RECEIPT_53.md` | `b8401e2543d4024d762f87db53e79783164a0e325fe2d70973613b7e6d6a0e09` |
| `ROOT_DGOV27_EFFECTIVE_SHA.patch` | `811deefb5adb709b43bbf5b9a79fb2785cd04b3f51a8571862abb7e84049aa6c` |
| `VALIDATION.md` | `9caff93ab04b13b77938487a40dc471712d8afde55a1d0d47a9d41235a1049ee` |

**Manifest 2:**
`docs/governance_harness/_PROPOSALS/OD7-G1_ROOT_MANIFEST_G4_CORRECTION_2026-07-27/ARTIFACT_HASHES.sha256`
— file SHA-256
`574f82592171dad9d4597fdf1591a2b7adf1f857af23cd246f087ef32dc6a35b`,
covering five members:

| Member | SHA-256 |
|---|---|
| `CORRECTED_ROOT_MANIFEST_ROOT-OD7-G1-20260727.yaml` | `fc4b3e7214fd0de7019b8c411026c0911783810d81f6d7543762731b593bf2d1` |
| `CORRECTED_ROOT_RECEIPT_53.md` | `88f5d86946f5630adfd2614ed1a8d6265b238bfbb0bfaf1c6a931a933251ab1a` |
| `PACKAGE_MANIFEST.json` | `5ca21bd56f83fb12e519638df3e97e08788710fcfd809d6326041d592b258135` |
| `PACKET.md` | `f5dec651eb54e65ea9aca752787637c12d0e9e5127e6cb80b3fd05023538e504` |
| `VALIDATION.md` | `7acb57ea186e86a9e1621d6de11c9203169bce754323a1c7cb1b16f66a6ccd98` |

Approval of R-4 is approval of exactly these bytes and satisfies Receipt
53's conditional gate for the OD7-G1 Root packages. It does not rule
`D-GOV-29` into or out of existence (§3), and it does not alter the OD7-G1
packet's own application conditions, which still govern any later
application collision.

Ruling slot (R-4):

<!-- BEGIN OWNER RULING VERBATIM -->
<<RULING PLACEHOLDER — OWNER RETURN VERBATIM: D-GOV-30>>
<!-- END OWNER RULING VERBATIM -->

## 8. Decline semantics

- Each R-item stands or falls alone. Declining any R-item leaves the other
  rulings and the §5 disclosure fully effective.
- A declined R-item returns to its owning workflow for a refreshed
  candidate under that workflow's own instruments; nothing is silently
  re-presented.
- Declining R-3 does not un-merge PR #398 or PR #408; it leaves their
  disclosed gaps open of record.
- Declining R-4 leaves the OD7-G1 Root packages non-effective per Receipt
  53's own conditional gate.
- Partial approval is recorded per item in the decision record; no
  aggregate "approved" summary may be written that obscures a declined
  item.

## 9. What this record does not rule

- **No loop-local substance.** App, PEC, and Piping ratifications are
  separate loop instruments under their own authorities. D-GOV-30 rules
  none of their content.
- **No D-8 amendment.** Reconciling D-8 / LOOP_INIT §7 with the disclosed
  window is a separate successor-policy instrument. Until that instrument
  exists, D-8 stands as written.
- **No cure of historical nonconformance** (§1).
- **No precedent for blanket approval** (§6).
- No lifecycle, implementation, activation, runtime, dependency, estimate,
  schedule, release, or professional-reliance authority is created.

## 10. RECEIPT_DRAFT — Root Receipt 60 (draft; not appended now)

Verified against `execution/_Coordination/LOOP_RECEIPTS.md` at this basis
(SHA-256
`f10a022732262ba9e98d252e0f13fb110142630a42c7f8607dffc640779fd518`):
Receipt 59 is the current cursor; the next-free receipt is **60**. The
draft below is appended to `LOOP_RECEIPTS.md` only in the completion
commit after the owner session — never by this candidate tranche. Rescan
the receipt cursor immediately before appending; a collision returns this
draft for refresh.

```markdown
### Receipt 60 — 2026-07-28 — Program disclosure and prospective ratification (D-GOV-30)

- **Owner act of record:**
  <!-- BEGIN OWNER RULING VERBATIM -->
  <<RULING PLACEHOLDER — OWNER RETURN VERBATIM: D-GOV-30>>
  <!-- END OWNER RULING VERBATIM -->
- **Parent receipt:** Receipt 59. Execution-time receipt scan governed; no
  cursor was silently renumbered.
- **Candidate identity:** exact D-GOV-30 packet
  `docs/governance_harness/_PROPOSALS/D-GOV-30_2026-07-28_program_disclosure_ratification/PACKET.md`,
  CandidateSubjectSHA256 recorded in the D-GOV-30 decision record;
  candidate basis `main@85ea0628fa4e57dd6aae53b06139b2b8734a9612`.
- **Disclosed:** the six enumerated facts of the 2026-07-28 merge window
  (PRs #389–#408) entered the record exactly as evidenced by the frozen
  merge-approval matrix and post-remediation horizon packages; the
  2026-07-28 self-merges stand as disclosed procedural exceptions under
  the recorded owner direction, with no claim of D-8/LOOP_INIT §7
  compliance and no retroactive cure.
- **Ruled:** per-item dispositions for R-1 (RT-A effective-state
  closeout), R-2 (record-currency repair), R-3 (program closeout and
  terminal disposition, enumerating the #398 and #408 gaps by SHA), and
  R-4 (OD7-G1 hash-manifest approval by SHA-256) are recorded verbatim in
  the D-GOV-30 decision record; any declined item is named here, not
  absorbed.
- **Informed batch:** the ruling is an informed batch over frozen,
  enumerated, exact-SHA evidence with per-line decline — not a precedent
  for blanket approval.
- **Gate:** disclosure and prospective present-state ratification only. No
  D-8 or LOOP_INIT amendment, no cure of historical nonconformance, no
  loop-local App/PEC/Piping substance, no decomposition, scope,
  lifecycle, activation, implementation, runtime, dependency, estimate,
  schedule, repin, release, or professional-reliance act is authorized,
  and nothing here is citable as precedent for blanket approval or
  self-merge.
```
