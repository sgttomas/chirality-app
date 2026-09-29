# Owner items — SCA-V4-002 (scope-change groups 1 and 2)

## Summary for the owner's review (one page)

**What this packet does.** It tidies up the text that SCA-V4-001 and DAG-002
left behind. There is no new policy. Every change points at a decision you
have already made. Nothing is applied until you accept it.

- **"Local-first" (your DECISION-8).** DEL-10-03's Scope of Work still says
  "the minimal local-first host loop". It will say that the loop runs on a
  local or cloud model you choose, with no default, a cloud model being
  reached by OAuth sign-in or an API key (your DECISION-4).
- **Four missing dependency links (your DECISION-10).** The graph lacks four
  links you accepted, because two Scopes of Work say the other deliverable
  "owns" something rather than that they "use" it. I checked both sides'
  design files. **All four are real**, so I recommend one "consumes"
  sentence for each.
  - **Effect on the graph:** 4 more held links inside the one big cycle
    that is already held. The cycles are unchanged, and nothing that is
    free now becomes blocked.
  - **DAG-003:** a small successor is needed afterwards for your acceptance.
- **Old "still open" wording.** Five Scopes of Work still call the
  reserved-act and classifier questions (OI-001, OI-002) or the Codex pin
  (OI-012) open or undecided, although you ruled them for the first
  increment (DECISION-1). They will point at your rulings, as SCA-V4-001
  did for the others. This includes the DEL-03-03 sentence ("retains
  unresolved reserved-act and classifier decisions").
- **A line join.** One long line in HOST_INTEGRATION is split in two. The
  words and the meaning are unchanged.

**From the closure audit of SCA-V4-001 (verdict OPEN).**
- **The main finding** is a bookkeeping one. SCA-V4-001's record of which
  original texts it overrode names eleven of them only in notes, not
  row by row. I recommend adding the 17 missing rows now (Q-10). Nothing
  already accepted is rewritten.
- **Three smaller fixes:**
  - one DEL-04-01 description phrase, "checkpoints override autonomy",
    phased like DEL-09-07's (Q-11);
  - a one-line reading rule, so that people who open the decomposition
    pointer learn that amendments apply (Q-12);
  - a short record that SCA-V4-001's follow-up work is done (Q-13).

**What I recommend you keep as it is.**
- **OI-001/OI-002 stay OPEN in the issues list** (Q-5). Eight later Scopes
  of Work still rely on them being open at their own point of need, and the
  product-level question (PRD OQ-02) is still open.

**Not in this amendment, and done after it:**
- rebuilding `Coverage_Telemetry.json`;
- re-pinning the 17 Design files;
- the SWBPIPE "local-first" note.

**What you need to answer.** Use the quick sheet below. "Accept the
remaining items as recommended" covers everything.

---

**Status: PROPOSED, revision 2** (with the CA1 closure-audit fold-in).
Evidence:
[IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md),
[BASIS_AMENDMENT.md](BASIS_AMENDMENT.md),
[SOW_REVISIONS.md](SOW_REVISIONS.md) and [ARC_EFFECT.md](ARC_EFFECT.md).

Items marked **required** are the ones the scope-change contract reserves to
you. The others confirm a reading or decide a conditional edit.

## Quick answer sheet

"Accept the remaining items as recommended" accepts every row below.
Declining an item drops only the edits named against it.

| # | Decision | Recommendation | Required by |
|---|---|---|---|
| Q-1 | Amendment identity and posture | `SCA-V4-002`; predecessor SCA-V4-001 | contract |
| Q-2 | Scope of the change (group 1) | Accept items 1–3 and the pointer fix | contract (group 1) |
| Q-3 | Write boundary, route and register (group 2) | Accept as listed; SoWs by REVISE after group 3 | contract (group 2) |
| Q-4 | The four arcs N-18, N-21, N-24, X-1 | Keep all four, with the drafted sentences | DECISION-10 |
| Q-5 | Open_Issues OI-001/OI-002 status | **A: keep OPEN** (no edit) | V13 F3 (proposed, not assumed) |
| Q-6 | Same wording defect in DEL-04-02 CLM-004 and the DEL-01-01 [N] line | Include | found here |
| Q-7 | OI-012 pointer to your pin decision (row stays OPEN) | Include | found here |
| Q-8 | HOST_INTEGRATION join: line break or paragraph break | Line break | layout |
| Q-9 | `_ScopeChange/_LATEST.md` in SPEC §11.2 form at the pointer move; V13 F1 disclosed | Accept | V13 F2, F1 |
| Q-10 | ASC-ISS-001: SCA-V4-001's note-only supersession bindings | **(a): add 17 path-level rows now** | CA1 |
| Q-11 | ASC-ISS-002: DEL-04-01 "checkpoints override autonomy" | Include, with its mirror | CA1 |
| Q-12 | ASC-ISS-006: reading rule "GROUP3 as amended by the active amendment" | **(a): add the note** | CA1 |
| Q-13 | ASC-ISS-003: SCA-V4-001 effective-state record | Write it after group 1; cite it at the pointer move | CA1 |
| Q-14 | Commit each decision snapshot before the next stage uses it | Accept | V11 F3 lesson |
| Q-15 | ASC-ISS-005: DECISION-8 is the record that deferred the Design re-pins | Confirm | CA1 |

---

## A. Required by the scope-change contract

### Q-1 · Amendment identity and posture — required

- **Identity.** `SCA-V4-002`, from `scan_next_amendment_id.sh … V4`.
- **Posture.** `ACCEPTED_PREDECESSOR`. `_ScopeChange/_LATEST.md` keeps
  naming SCA-V4-001 until you accept group 3.
- **Predecessor's standing.** SCA-V4-001's closure verdict stays
  `OPEN_PENDING_DERIVATIVE_CLOSURE`. Its open items are carried in
  SCA-V4-002's handoff, so moving the pointer hides nothing.

### Q-2 · Scope of the change (group 1) — required

**Recommendation: accept.** The scope is:
1. DEL-10-03 REQ-005, "local-first" aligned with DECISION-4 D4-3;
2. the four consumption sentences (Q-4);
3. the OI-001/002/012 text in DEL-09-07, DEL-01-04 and DEL-02-02, the
   DEL-03-03 CLM-002 tail (with REQ-005, which cites it), and the A17b line
   join;
4. the pointer fix (Q-9).

The proposed additions are separate items: Q-5 to Q-7 and Q-10 to Q-13.

- **DEL-09-07 CLM-002.** DEL-09-07's CLM-002 says the same thing as its
  TBD-002/003, so it is aligned too; otherwise the SoW would contradict
  itself.
- **Nothing structural.** No ID, package or deliverable is added, removed or
  moved.

### Q-3 · Write boundary, route and register (group 2) — required

**Recommendation: accept.**
- **Write boundary:** exactly the AffectedFiles of the 16-row register
  (IMPACT §3.2), plus the SCA-V4-002 snapshot folders and pointers.
- **Route:** as for SCA-V4-001.
  - The docs, decomposition and `_CONTEXT.md` edits go into the candidate.
  - The SoWs change only after group 3, by `scope-of-work` REVISE, one per
    brief, with `STATUS_POLICY=NO_STATUS_TOUCH`.
  - Then the register UPDATE, the currency audit and DAG-003 (IMPACT §7).
- **`ScopeChanging`:** `YES` only for DEL-10-03.
- **`SupersessionBindingPresent`:** `YES` only for row 14 (Q-11).
- **What this accepts:** the exact SoW blocks (26, or 22 without Q-6), the
  basis edits A-01 and B-01…B-06, the pointer write C-01, and the Decision
  Log entry B-04 with its slot rules.

## B. The four dependency links

### Q-4 · Keep N-18, N-21, N-24 and X-1 — DECISION-10 option A

**Recommendation: keep all four.** The evidence, the sentences and the
computation are in ARC_EFFECT.

| Arc | Real? | Why |
|---|---|---|
| N-18 DEL-02-01 → DEL-03-02 | Yes | The workflow contract's subject binding and item decisions use the proposal contract's item dispositions, item-left events and applied-outcome identities (WD §8, §4.3.6–4.3.7; P §13 "Provide to DEL-02-01") |
| N-21 DEL-02-03 → DEL-03-02 | Yes | Execution recording and replay use the same outputs (EXEC §9.1, §4.11–4.12) |
| N-24 DEL-02-03 → DEL-03-03 | Yes | The adapter passes checkpoint arrivals and act records on the external channel to DEL-02-03 for recording, in the current phase (ADAPTER §7.7) |
| X-1 DEL-02-03 → DEL-01-04 | Yes, narrowly | DEL-02-03's App-side capture fixture waits for DEL-01-04's act control and person identity (EXEC §5, CH-23 AWAITING INPUT). You kept X-1 in DECISION-6 |

**SCC effect**, computed from the 41 live registers:
- arcs go from 198 to 202, all 4 added arcs are held, and 124 stay admitted;
- the 6 SCCs are unchanged; SCC-002 keeps its 13 members;
- DEL-04-01 gains no supplier, and nothing points into DEL-09-06.

**Expected DAG-003:**
- **Changes:** +4 held arcs, 0 removed.
- **DAG pending until accepted:** DEL-02-01, DEL-02-03, DEL-03-02, DEL-03-03
  and DEL-01-04. All are already held for these arcs, so nothing gets
  blocked.
- **Alternative:** drop an arc (option D). Delete its clause; if all four
  are dropped, no DAG-003 is needed for arcs.

## C. Proposed additions (V13 F3, and found in this pass)

### Q-5 · Open_Issues OI-001/OI-002 status — proposed, not assumed

- **Facts.** Both rows are `OPEN`. Their Consequence field, updated under
  SCA-V4-001 (O-17, where you accepted "status stays OPEN"), already points
  to DECISION-1 D2/D3 and names what remains: operation-specific additions
  (OI-021) and host adoption (DEP-001).
- **Option A, recommended: no edit.** Reasons:
  - the rulings are for the first increment's App/shared contracts;
  - the product-level list (PRD OQ-02) is still marked open (O-26);
  - eight later-undertaking Scopes of Work (DEL-01-02, 01-03, 08-02, 09-02,
    09-05, 09-11, 09-12, 11-03) rely on the rows being OPEN at their own
    point of need.

  The Scopes of Work revised here say "ruled for the first increment",
  which is compatible with OPEN.
- **Option B.** Set both to `RESOLVED_FOR_FIRST_INCREMENT`, following OI-017's
  scoped-resolution precedent (text in BASIS_AMENDMENT B-03). This makes the
  list read as resolved, but:
  - the eight Scopes of Work above would then contradict it, and would need
    a follow-on sweep;
  - the stale telemetry would gain another difference (OPEN 23 → 21).

### Q-6 · The same wording defect in two first-increment Scopes of Work — proposed

- **Facts.**
  - DEL-04-02 CLM-004 says you "decide the unresolved … choices in OI-001
    and OI-002", while its own TBD-001/002 say they are ruled.
  - DEL-01-01's [N] source line says "no selected version/environment is
    established", while its CLM-003 and TBD-002 record the 0.158.0 pin.
- **Recommendation: include** (F-0402-01…02, F-0101-01…02). It is the same
  class as the DEL-03-03 tail you already scoped in. No link changes.

### Q-7 · OI-012 pointer — proposed

**Recommendation: include** (B-02). The row stays OPEN. Its Consequence gains
one sentence: DECISION-1 D4 selected 0.158.0 for definition and generation,
and the implementation and qualification pin remain open. This mirrors
O-17.

### Q-8 · The HOST_INTEGRATION join: line break or paragraph break

- **Facts.** Before SCA-V4-001, "**Open detail** marks …" was on the same
  line as "are retained.", inside the status paragraph. So there was no
  paragraph break to restore.
- **Recommendation: a line break** (A-01). It keeps the paragraph as it was
  and reads the same when rendered.
- **Alternative:** a blank line, so that "Open detail" becomes its own
  paragraph. Its result hash is in A-01, and it shifts SourceLine by 2
  instead of 1.

### Q-9 · The pointer form (V13 F2) and the manifest label (V13 F1)

- **F2.** At the group-3 pointer move, write `_ScopeChange/_LATEST.md` with
  `Latest:` and `Updated:` first (C-01). The registered parser was tested on
  it. **Recommendation: accept.**
- **F1.** One row of SCA-V4-001's group-3 manifest says its bytes equal the
  presented bytes. For `OWNER_DECISIONS.md` they do not: DECISION-8 was
  appended after the presentation. The snapshot is immutable, so this is
  disclosed in SCA-V4-002's Brief, not rewritten. Nothing to decide.

## D. From the SCA-V4-001 closure audit (CA1, verdict OPEN)

### Q-10 · ASC-ISS-001: bind SCA-V4-001's eleven note-only supersessions at path level

- **Facts.**
  - SCA-V4-001 marked 22 actions as overriding an accepted text. Eleven of
    them (actions 18–25, 36, 42 and 46) have no row of their own; they are
    mentioned only in other rows' notes.
  - As a result, no row names the frozen GROUP3 `ScopeLedger.csv` or
    `Deliverables.csv` as the overridden source.
  - The method rates this CRITICAL. The record you accepted (DECISION-7)
    bound the 11-row delta, and V11 accepted the notes convention.
- **Option (a), recommended.** Add 17 rows to SCA-V4-002's supersession delta,
  one per overridden fact (BASIS_AMENDMENT Part D), and re-accumulate the
  map from SCA-V4-001's.
  - **Checks:** 18/18 original texts found in GROUP3; the accumulator
    passes with 29 rows.
  - **Nothing rewritten:** SCA-V4-001's files stay as they are.
  - **Why:** it is cheap, conforms to the method, and lets a later audit
    close ASC-ISS-001.
- **Option (b).** Rule that the notes convention is enough for SCA-V4-001.
  Any change to the method would then be separate Root work.

### Q-11 · ASC-ISS-002: DEL-04-01 "PKG-02 checkpoints override autonomy"

**Recommendation: include** (B-05). It becomes "PKG-02 checkpoint acts are
never substituted by autonomy (holds only in the governance phase)", the
wording SCA-V4-001 used for DEL-09-07 (D-12b). The DEL-04-01 `_CONTEXT.md`
mirror changes with it, and one supersession row (D-014) binds it. It has no
graph effect. **Alternative:** record that the phrase stands.

### Q-12 · ASC-ISS-006: how readers find out that GROUP3 has been amended

- **Facts.**
  - The coordination file tells readers to open `_LATEST_ACCEPTED.md`,
    which names GROUP3 only.
  - Five `_CONTEXT.md` files carry amended text but still say "Accepted
    basis: GROUP3".
  - Only `_ScopeChange/_LATEST.md` leads to the amendments.
- **Option (a), recommended.** Add one reading-rule sentence, "read as
  amended by the active `_ScopeChange/_LATEST.md`", to `_LATEST_ACCEPTED.md`,
  `_Decomposition/_LATEST.md` and those five `_CONTEXT.md` lines (B-06).
  - **Timing:** `_LATEST_ACCEPTED.md` is bound by DAG-002, so its edit is
    timed with the SoW changes and falls inside the same DAG-003 departure.
  - **Why:** it fixes the actual reader route.
- **Option (b).** Record that your O-22 reading (frontmatter stays on GROUP3)
  also covers these surfaces. It costs nothing, but a reader who follows the
  documented route still never meets the amendments.

### Q-13 · ASC-ISS-003: record that SCA-V4-001's follow-up work is done

- **Facts.** SCA-V4-001's records still list as open the 16 SoW REVISEs,
  the registers and DAG-002, all now complete. The records are group-bound
  and are not edited.
- **Recommendation.**
  - After you accept group 1, write one new effective-state record in the
    append-only post-acceptance folder (C-02), citing the CA1 audit and
    your Q-10 ruling.
  - At SCA-V4-002's pointer move, the new §11.2 `_LATEST.md` cites it
    (C-01).
  - This combines the V13 F2 fix with the effective state, without
    touching the pointer while SCA-V4-002 is a candidate.

### Q-14 · Commit each decision snapshot before the next stage

**Recommendation: accept.** This is SCA-V4-001's V11 F3 lesson: its group-1
snapshot was finalized after application.

### Q-15 · ASC-ISS-005: the Design re-pin deferral

**Recommendation: confirm** that your DECISION-8 acceptance ("Accept
(Recommended)", which accepted the handoff saying "re-pin at the next design
pass") is the record that deferred the 17 Design re-pins. They are re-pinned
once, after SCA-V4-002's REVISEs, with GUIDE (DEL-03-04) last.

---

## Out of scope, sequenced after SCA-V4-002

- **`Coverage_Telemetry.json`** (ASC-ISS-004). It stays
  STALE_REBUILD_REQUIRED under your DECISION-8 answer 2. It is rebuilt once,
  after SCA-V4-002, by the decomposition owner's bounded brief, and then
  `audit-decomp` closes COV-119/120.
- **The 17 Design files** (ASC-ISS-005). They are re-pinned at the next
  design pass, after the REVISEs (Q-15).
- **The SWBPIPE "local-first" handoff note.** It goes with the next relay to
  SWBPIPE (DECISION-8).

## Considered and not proposed

- **Consumer-side sentences for N-05 and N-07** (V12 F6). Those links are
  already in DAG-002, so the sentences would change nothing.
- **Sweeping the eight later-undertaking Scopes of Work** that say OI-001/002
  "remain OPEN". They are correct under Q-5 option A, and they belong to
  their own undertakings.
- **DEL-04-01's closing clause** ("a concrete unruled operation waits for
  OI-001/OI-002"). It is consistent with option A.
- **`Allocation_Rationale.csv`.** It stays as history, as you accepted.

## What the workflow requires that this packet does not yet have

- **The pre-change `audit-decomp` baseline** for the affected packages. It
  needs a dispatched run, or a documented reuse of the CA1 audit's inputs,
  before group 1 is presented (IMPACT §4).
- **The decision snapshots, the candidate snapshot, the independent review
  and the post-change audit.** These are later stages.
