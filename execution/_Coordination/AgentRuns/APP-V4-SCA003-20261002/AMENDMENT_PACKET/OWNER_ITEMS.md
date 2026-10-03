# Owner items — SCA-V4-003 (scope-change groups 1 and 2)

## Summary for the owner's review (one page)

**What this amendment does.** It writes into the deliverables' Scopes of Work
what the last two design passes found and what you decided along the way
(DECISION-K1, DECISION-K3 as revised, DECISION-L). There is no new policy of
my own: each change points at your decision, an accepted basis text or a
recorded ruling. Nothing is applied until you accept it.

- **209 proposals, one ledger.** 185 recommended in, 9 held for later, 15
  left out (superseded, duplicated, withdrawn at their source, or not needed).
- **The six new deliverables' contracts catch up with your decisions.**
  Request recovery (K-4 quit asks first; three distinct "stop" operations),
  plans and delegation (K-5, K-10), native requests and **the App act control**
  (K1-4, K-8; the one new requirement), sign-in and model access (K-1, K-3,
  K-12, L-1, L-7), workflow registration (K-6, K-7, L-4, chaining under L-2)
  and roles (L-2, K-10).
- **The fourteen first-increment contracts get pass 2's fixes.** The
  "who asks" wording (K1-1), earlier acts (K1-2, K1-3), identity (K1-4),
  receiver lists, pointers and corrections.
- **Effect on the graph:** 10 new links. 5 sit inside the large held cycle
  and change nothing; 5 put the recovery, plans and access deliverables
  before the ones that use them. The cycles are unchanged and nothing that is
  free now becomes blocked. A successor graph (DAG-004) follows for your
  acceptance.

**What I recommend you hold for later.**
- Anything that rests on **the A12 mapping** for network-destination grants
  (DEL-04-01's criterion, DEL-05-02's destination surfaces): you deferred it
  to the phase review, which has not happened (Q-9).
- **DEL-03-01's read-basis criterion** (AC-004) against a host that supplies
  no workspace identity: a protected criterion, and the basis text says
  otherwise (Q-7).

**What needs a separate yes.** Moving the six new deliverables from
INITIALIZED to IN_PROGRESS, as you did for the first increment (Q-13).

**What you need to answer.** The quick sheet below. "Accept the remaining
items as recommended" covers everything.

---

**Status: PROPOSED.** Evidence: [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md),
[LEDGER.md](LEDGER.md) / [LEDGER.csv](LEDGER.csv), [ARC_EFFECT.md](ARC_EFFECT.md),
[BASIS_AMENDMENT.md](BASIS_AMENDMENT.md). The exact ScopeOfWork blocks come
from P2 (`SOW_REVISIONS_A.md`, `_B.md`) for the group-2 decision.

Items marked **required** are the decisions the scope-change contract
reserves to you. The others decide a conditional or optional item, or confirm
a reading.

## Quick answer sheet

"Accept the remaining items as recommended" accepts every row. Declining an
item drops only the ledger rows named against it.

| # | Decision | Recommendation | Required by |
|---|---|---|---|
| Q-1 | Amendment identity and posture | `SCA-V4-003`; predecessor SCA-V4-002 | contract |
| Q-2 | Scope (group 1): the ledger's INCLUDE rows | Accept | contract (group 1) |
| Q-3 | Write boundary, route and register (group 2) | Accept as outlined; SoWs by REVISE after group 3 | contract (group 2) |
| Q-4 | The 10 new links, and R22-4 for NR-01…NR-04 | Keep 10; add the 3 sentences; drop NR-03 | R22-4; ARC_EFFECT |
| Q-5 | The App act control in DEL-01-04 (SC3-01-04-1 replaces SC2-01-04-1) | Include | K1-4, K-8 |
| Q-6 | DEL-03-01 additions: destination elements (S-01-2), catalog edition (S-01-3) | Include both | owning decision |
| Q-7 | DEL-03-01 REQ-004/AC-004 against R13-1 (S-01-4) | **Hold** | owning decision |
| Q-8 | Custody of the shared fixtures FX-PIPE-01 and SH-1 (S-01-5) | DEL-03-01 keeps them; include | phase-review item |
| Q-9 | Items resting on the A12 mapping (SC2-04-01-2, R2-04-01-b, S-0502-1, R-0502-2) | **Hold** unless you confirm the mapping now | SCA-V4-001 O-15 |
| Q-10 | OI-009 (account home) in the issues list | **B**: mark it decided, with the status word you choose | proposed, not assumed |
| Q-11 | Optional items (list below) | Include; drop the two the sources advise dropping | sources |
| Q-12 | Basis items (6) | None now: 3 held, 3 not needed | sources |
| Q-13 | R22-5: six deliverables INITIALIZED → IN_PROGRESS | Yes, now, as a separate act | R22-5 |
| Q-14 | Register conventions (SatisfactionStatus) | Hold for the register owners' pass | DAG-003 open matter |
| Q-15 | Receivers sentences that let mirror rows be extracted (P1-06…P1-10) | Include | registers follow the SoW |
| Q-16 | Commit each decision snapshot before the next stage; SCA-V4-002 effective-state note | Accept | SCA-V4-002 Q-13, Q-14 |

---

## A. Required by the scope-change contract

### Q-1 · Amendment identity and posture — required

- **Identity:** `SCA-V4-003`, from `scan_next_amendment_id.sh … V4` (run under
  zsh).
- **Posture:** `ACCEPTED_PREDECESSOR`. `_ScopeChange/_LATEST.md` keeps naming
  SCA-V4-002 until you accept group 3.
- **Predecessor's standing:** SCA-V4-002 stays
  `OPEN_PENDING_DERIVATIVE_CLOSURE` for derivatives only; see Q-16.

### Q-2 · Scope of the change (group 1) — required

**Recommendation: accept the 185 INCLUDE rows** (IMPACT §2–§3): 101
ScopeOfWork items in 19 deliverables, 81 register items (10 new links, 30
mirror groups, 41 statement and notes items), 2 Open_Issues edits and the
Change Register entry. All are `MODIFY`; nothing is added, removed or moved;
no ID changes. The DEFER and DROP rows are listed with reasons in the ledger.

### Q-3 · Write boundary, route and register (group 2) — required

**Recommendation: accept the outline** (IMPACT §10).
- **Direct writes:** `Open_Issues.csv` (OI-009, OI-018) and the SCA-V4-003
  snapshot folders; after group 3, the Decision Log entry and the pointer.
- **The 19 Scopes of Work** change only after group 3, by `scope-of-work`
  REVISE, one per brief, `STATUS_POLICY=NO_STATUS_TOUCH`. Then
  `dependency-extract` UPDATE for 20 registers, the currency audit and
  DAG-004.
- **ScopeChanging** (provisional): YES for DEL-01-02…01-05, 02-02, 02-03,
  02-04, and DEL-03-01 if Q-6 is accepted; NO for the rest. No deliverable is
  ISSUED, so no row authorizes a reopening.
- **Supersession:** none for the SoW edits; one row for OI-009 under Q-10 B.
- The exact blocks and the dry-run come from P2 at the group-2 decision.

## B. The links and the act control

### Q-4 · Ten new links; R22-4 for NR-01…NR-04

**Recommendation: keep the 10, add three sentences, drop NR-03.**

| Link (user → supplier) | Where | Why |
|---|---|---|
| DEL-04-03 → DEL-02-01 | held | Run records carry the workflow identity and disposition words (pass 2) |
| DEL-04-03 → DEL-02-02 | held | Run records carry the run-start text and its check (R20-10) |
| DEL-01-04 → DEL-04-02, → DEL-02-03, → DEL-02-04 | held | The App places the checkpoint display and offers the roles (R17-7, R22-1) |
| DEL-01-04 → DEL-01-03, → DEL-01-05 | admitted | Plan mode in the turns it sends; the model choice and Codex account |
| DEL-02-03, DEL-03-03, DEL-02-02 → DEL-01-02 | admitted | Recovery's custody events, relaunch facts and run-end definition |

- **Effect:** 202 → 212 links; the six cycles are unchanged, singly, in
  pairs and together; the admitted layer stays acyclic; the guards hold
  (ARC_EFFECT §2–§3).
- **R22-4:** NR-01, NR-02 and NR-04 get the consuming sentence (P1-01,
  P1-02, P1-03). NR-03 (DEL-09-09 → DEL-01-02) is dropped: the trace case
  reaches those facts through the adapter, which NR-02 already covers.
- **R20-10** also had no sentence on DEL-04-03's side; P1-05 adds it.
- **Alternative:** drop any link with its sentence. With none left, no
  successor graph is needed on link grounds.

### Q-5 · The App act control (SC3-01-04-1)

**Recommendation: include.** It replaces pass 2's SC2-01-04-1. It adds A15
(registering a workflow revision, one reviewed draft or several library
entries in one act, R21-3), DEL-02-02 as a user, "interface script" among
what may not operate it, and "presenting or operating it answers no pending
request". Your K1-4 asked for exactly this collection; K-8 placed
registration on it. Where it runs, so that no automation can operate it,
stays with OI-008 at the phase review.

## C. Owning decisions and held items

### Q-6 · DEL-03-01: destination elements and catalog edition

- **S-01-2 (include):** the catalog carries a host's external-contact
  declaration and destination-request entry. It writes your DECISION-5
  (SWBPIPE intake) into the catalog's contract; LOOP already relies on it.
- **S-01-3 (include):** the catalog names the edition a consumer found and
  the event for a new one. Four Design files rely on it, and DEL-05-01's
  register asks for "catalog identity".
- Both are additions to DEL-03-01's scope. **Alternative:** hold either; the
  Design keeps it labelled PROPOSED.

### Q-7 · DEL-03-01 REQ-004/AC-004 and a host without workspace identity (S-01-4)

**Recommendation: hold.** The change would let a fixture read lack workspace
identity or generation when a host declares it supplies neither (R13-1).
AC-004 is a protected criterion, and the basis (V4-HI-11) requires all four
elements; pass 2 recorded SWBPIPE's gap as a host non-conformance. The point
of need is a host join, which DECISION-3 defers. **Alternative:** include it
now, with R-01-3's matching notes.

### Q-8 · Custody of the shared fixtures (S-01-5)

**Recommendation: DEL-03-01 keeps custody, and its OUT-003 says so.** The
fixture catalogue FX-PIPE-01 and the simulated host SH-1 already live in its
Design folder, and CA, XT and ADAPTER use them. **Alternative:** record
another custodian; then no SoW change.

### Q-9 · Items that wait for the A12 mapping

**Recommendation: hold** SC2-04-01-2 and R2-04-01-b (DEL-04-01's AC-007/VER-007
naming the DECISION-5 grant as an A12 subclass) and S-0502-1 option A with
R-0502-2 (DEL-05-02 naming the panel's destination surfaces). Your SCA-V4-001
answer O-15 deferred them until the mapping is confirmed, at the phase review;
pass 3's sitting covered other questions. **Alternative:** confirm the
mapping now; then all four rows are included.

### Q-10 · OI-009 (Codex account home) in the issues list

- **Facts:** OI-009 asks to "choose separated versus shared Codex account
  state". Your K-1 chose shared settings with a separate sign-in, and L-7
  made you the App implementation owner. The mechanism was observed working
  at Codex 0.158.0 (OBS-2 O-6); sign-in with a real credential was not
  observed (L-6).
- **Option B, recommended:** change the status from OPEN to a decided value,
  with the Consequence citing K-1, L-7 and O-6. The list has no ready word for
  "decided by the owner"; existing values are `RESOLVED_BY_SOURCE`,
  `RESOLVED_FOR_CURRENT_DEFINITION_RUN` and `RESOLVED_BY_GROUP2`. You choose
  the word. One supersession row then records the change against the frozen
  GROUP3 list, and the stale telemetry's open-issue count differs by one more
  (pre-change audit COV-116).
- **Option A:** keep OPEN and add a pointer to K-1, as SCA-V4-002 did for
  OI-012. The list then reads as undecided although the choice is made.

### Q-11 · Optional items

**Recommendation: include** SC2-04-01-4 (with "captured through DEL-01-04's
App act control"), S-02-2 and R-02-3, S-03-3 and R-03-4, S-03-4, S-04-3,
S-11-1 (P2 may also point at the OBS-2 and OBS-3 records), SC3-01-02-10,
SC3-01-02-11, SC3-01-05-13, the OI-018 pointer, R3-01-02-d and R3-01-03-f.
Each is small and grounded; the consumer-side ones change no link.
**Drop** SC3-02-02-5 ("host-supplied" is the basis's own word) and S-0906-4
(its source finds no change needed).

### Q-12 · Basis items

**Recommendation: no basis change in SCA-V4-003** (BASIS_AMENDMENT).
- **Hold:** the ARCHITECTURE §4 allow-list sentence recording K1-5 (it does
  not contradict K1-5; a basis edit would force a coverage recompute); whether
  boundary-refused destination requests are recorded (your phase review); and
  whether V4-HI-02 names the catalog edition (for the basis owner if Q-6 is
  accepted).
- **Not needed:** the start-up traffic item (answered by K-12 and L-3); the
  V4-HI-11 item (no change proposed); the SIWC custody change (you saw no
  pressing need; it returns only if a trigger fires).

### Q-13 · R22-5: lifecycle of the six new deliverables

**Recommendation: yes, now, as a separate act.** DEL-01-02, 01-03, 01-04,
01-05, 02-02 and 02-04 are INITIALIZED, but each has owner-directed design
work at v0.2, which SPEC §3.2 calls IN_PROGRESS. You directed the same move
for the first increment (DECISION-6, BASIS-ALIGN). It is recorded in each
`_STATUS.md` by you or WORKING_ITEMS; it is not an amendment action and the
REVISEs do not touch status. The pre-change audit notes one visible effect:
16 missing-artifact rows of these six become WARNINGs (35 → 51) because the
audit grades IN_PROGRESS deliverables more strictly; the post-change comparison
will attribute them to this move, not to the amendment. **Alternatives:**
after group 3; or leave INITIALIZED.

### Q-14 · Register conventions

**Recommendation: hold** R-02-4 (one SatisfactionStatus convention, TBD or
PENDING, across registers) for the register owners' pass that DAG-003 already
lists (P2 O-6). The two maturity reconciliations (R-03-2, R2-04-03-g) are
included; extraction sets their values from the revised Scopes of Work.

### Q-15 · Receivers sentences for mirror rows (P1-06…P1-10)

**Recommendation: include.** Registers are extracted from the Scope of Work
only. Pass 2's C1-B proposed 32 mirror rows in DEL-03-01, 03-02, 03-03 and
01-01, and C1-C one in DEL-05-01, without a sentence naming the other
deliverable. For 24 of C1-B's rows and for the DEL-05-01 row, the Scope of
Work names no such deliverable today (checked by script). One sentence per
Scope of Work, as pass 2's C1-A drafted for its own mirrors, grounds them. **Alternative:** you or WORKING_ITEMS declare those rows by
hand in each `_DEPENDENCIES.md`.

### Q-16 · Snapshots and the predecessor's record

**Recommendation: accept.** Commit each decision snapshot before the next
stage uses it (SCA-V4-002 Q-14). After group 1, write a short effective-state
note for SCA-V4-002: pass 2 re-pinned the Design files and fixed the HANDOFF
line; `Coverage_Telemetry.json` is still to be rebuilt.

---

## Not in this amendment

- **`Coverage_Telemetry.json` rebuild** (carried since SCA-V4-001; your
  BASIS-ALIGN DECISION-8). Still stale; OI-009 under Q-10 B adds one more
  difference.
- **Design re-pins after the REVISEs** (20 deliverables' Design headers pin
  their Scope of Work and register bytes; GUIDE last). At the next design
  touch.
- **Supplier-side mirrors pass 2 noted but did not propose** (DEL-04-01,
  04-03, 02-01, 02-03 toward the six new deliverables) and the consumer rows
  owed by DEL-04-03 and DEL-11-02 for DEL-02-04: no source proposed them; a
  later amendment or the register owners.
- **Root `AGENTS.md` instruction notices** raised in pass 3 (L-2 against
  "verified idle boundary"; the analytics-off flag against "does not veto the
  user's Codex configuration"): instruction changes need their own scope.
- **The Codex version-advance check** (R19-5): optional, needs a download and
  your separate yes.
