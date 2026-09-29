# Owner decisions — APP-V4-BASIS-ALIGN-20260928

## Direction to start (owner, exact, 2026-09-28)

> "go ahead with the next undertaking as recommended."

**The recommendation it answers.** This is the recorder's last message of run
APP-V4-SWBPIPE-INTAKE-20260928. The next undertaking should bring the accepted
basis in line with what the owner has decided, before more design work builds
on it. It covers:

- the proposed ScopeOfWork, register and dependency-graph (DAG-002) changes
  from the first closeout (C1-A/B/C, CLOSEOUT_ACCOUNT);
- the accepted-basis wording updates: V4-WF-05 (phased checkpoints), V4-HOST-01
  and V4-ARC-11 (OAuth; no default), and V4-HOST-02 (DECISION-5);
- the SoW wording that assumes a run waits at a checkpoint: EXEC F-29, CA F-22,
  GUIDE G-12 and LOOP G-6.

Earlier recommendations the recorder treats as carried into "as recommended",
**to be confirmed at the checkpoints**, not assumed:

- recording IN_PROGRESS for the 14 first-increment deliverables;
- the ruling on the disputed arc DEL-03-02 → DEL-04-03 (lean: not proposed).

## Governance route

Both routes have owner checkpoints. No governed file changes before the owner
accepts the packet at the checkpoint that governs it.

- **Accepted basis and ScopeOfWork:** `scope-change`, grouped checkpoints 1–3.
  The accepted amendment is applied by `scope-of-work` MODE=REVISE, one
  deliverable per brief.
- **Registers and DAG:** register changes are applied by bounded
  per-deliverable briefs (`dependency-extract` or human declaration, as the
  row requires). A currency audit then records the DEPARTURE, and
  `project-dag` TRIGGER=SUCCESSOR prepares DAG-002 for the owner's acceptance
  at checkpoint 2.

## Checkpoint A: owner answers (exact, 2026-09-28), DECISION-6 (partial)

| Question presented | Owner's answer (exact) |
|---|---|
| Accept the wording package (SCA-V4-001) as prepared? | "I want to review the packet first" |
| Four closeout corrections that widen or sharpen scope: adopt which? | "what do you recommend and why" |
| Record the 14 first-increment deliverables as IN_PROGRESS now? | "Yes, record IN_PROGRESS (Recommended)" |
| Dependency arcs for DAG-002: 41 arcs, keep X-1, disputed arc out? | "Accept the 41; keep X-1 (Recommended)" |

## Effects

- **Scope-change groups 1–2** are not yet accepted. The owner is reviewing the
  packet. No doc, decomposition or SoW edit is applied.
- **Lifecycle:** the owner directs recording INITIALIZED → IN_PROGRESS for
  DEL-04-01, 04-02, 04-03, 03-01, 03-02, 03-03, 03-04, 02-01, 02-03, 05-01,
  05-02, 01-01, 09-06 and 09-09 (SPEC: by the Human or WORKING_ITEMS).
- **Arc set** (for DAG-002 preparation):
  - the refreshed 41 are accepted, with X-1 kept;
  - N-12 and N-B8 are not proposed.

  DAG-002 itself still needs the owner's acceptance at checkpoint C.

## Checkpoint A: acceptance (owner, exact, 2026-09-28), DECISION-7

**Context.** The owner reviewed the packet (revision 2; OWNER_ITEMS.md
sha256 `2b90eb4a…`, BASIS_AMENDMENT.md `04bdc916…`, SOW_REVISIONS.md
`9b4d700d…`, IMPACT_ASSESSMENT.md `7fd523c2…`) on the review page
https://claude.ai/artifact/3ek3uuPUR1v9jgpTjoF6ec. The page states: "To
accept everything still open, reply in chat: accept the remaining items as
recommended".

> "accept the remaining items as recommended"

## Effects

**Scope-change checkpoint groups 1 and 2 for `SCA-V4-001` are accepted**, as
recommended in OWNER_ITEMS.md revision 2. That covers O-1 through O-15, O-17
through O-19 and O-21 through O-26:

- the scope of the change;
- the write boundary and the application route;
- the V4-WF-05, V4-HOST-01/ARC-11 and V4-HOST-02/ARC-12 texts, and the
  consequential edits;
- the four scope additions (S-01-4, S-01-5, S-02-3, S-03-2);
- the model-destination reading;
- direct consumption (O-11, O-12, O-13);
- the DECISION-5 SoW allocation (O-14, O-15);
- "local-first" amended (O-8);
- the OI-001/OI-002 pointers;
- DEL-08-01 and DEL-09-07 included;
- the supersession typing, the `ScopeChanging` values and two decision
  snapshots;
- SoW frontmatter unchanged;
- the R8-11 reading;
- the OQ-02 markers left for later.

O-16, O-20 and O-27 through O-30 were already decided or done (DECISION-6).

**Next, per the accepted route (O-3):**

1. Write the group-1 and group-2 decision snapshots.
2. Apply the basis documents, the decomposition edits and the `_CONTEXT.md`
   mirrors as the candidate.
3. Run the post-change audit with the baseline's seven-package scope, then an
   independent review.
4. Present group 3 (the audited poststate) at checkpoint B.
5. Only after group-3 acceptance: `scope-of-work` REVISE for the 16 SoWs,
   the register rows, the currency audit, and DAG-002 (checkpoint C).

## Checkpoint B: scope-change group 3 (owner, exact, 2026-09-29), DECISION-8

**Custody.** The owner's answers to a structured question in the active chat,
transcribed by the recorder. The package presented was the candidate at
`230bf1e64` with Handoff_State and RUN_SUMMARY at `9ae24fc0f`, and review
V11: READY FOR GROUP 3.

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint B (scope-change group 3 for SCA-V4-001): accept the applied, audited result? | "Accept (Recommended)" |
| Coverage_Telemetry.json goes stale; no writer: how to handle? | "Record as stale, fix later (Recommended)" |
| "local-first" outside this amendment (DEL-10-03 REQ-005; the SWBPIPE handoff note)? | "Small follow-on amendment (Recommended)" |

## Effects

- **SCA-V4-001 group 3 is ACCEPTED on 2026-09-29.** Write the group-3 decision
  snapshot, the immutable `SCA-*` accepted snapshot and
  `_ScopeChange/_LATEST.md`.
- **Apply H-1…H-3** with `{ACCEPT_DATE}` = 2026-09-29, then H-4 (the second
  coverage recompute) and H-5 (post-acceptance validation and audit).
- **Coverage_Telemetry.json:** STALE_REBUILD_REQUIRED, owned by the
  decomposition owner. It is fixed later by a bounded brief. The closure
  verdict stays OPEN_PENDING_DERIVATIVE_CLOSURE for this derivative only.
- **Follow-on amendment SCA-V4-002**, after SCA-V4-001 closes: DEL-10-03
  REQ-005 "local-first". The SWBPIPE handoff note carries forward with the
  next relay to SWBPIPE.
- **Propagation now authorized:**
  - `scope-of-work` REVISE for the 16 SoWs, one deliverable per brief;
  - then the register rows;
  - then the DAG-001 currency audit and the DAG-002 candidate, for owner
    checkpoint C.

## project-setup INCREMENTAL, Phase 5.1 plan (owner, exact, 2026-09-29), DECISION-9

| Gate question presented | Owner's answer (exact label) |
|---|---|
| Setup of SCA-V4-001 (register `069645d9…`): 0 scaffold, 0 retired, 16 modified (0 held), routed to scope-of-work REVISE then VERIFY; dependency refresh under FULL_GRAPH for the 16 plus 2 neighbours (DEL-01-04, DEL-02-02); closure audit; DAG currency audit → DAG-002 at checkpoint C. Confirm this incremental plan? | "Confirm (Recommended)" |

## Effects

The plan is confirmed, and writing may begin:

- REVISE in four parallel groups, one deliverable per brief, each followed by
  VERIFY;
- `dependency-extract` for the 18 deliverables;
- `audit-dep-closure`;
- a `project-dag` currency audit and the TRIGGER=SUCCESSOR candidate;
- owner checkpoint C;
- the SETUP_LOG line.

Lifecycle is preserved (STATUS_POLICY PRESERVE_CURRENT).

## Checkpoint C: DAG-002 (owner, exact, 2026-09-29), DECISION-10

**Custody.** The owner's answers to a structured question in the active chat,
transcribed by the recorder. The package presented was `DAG_PREP/CHECKPOINT_C.md`
and `DAG_PREP/REVIEW_PACKET.md`, at commit `5f03b7796`. Review V12 returned
READY FOR CHECKPOINT C.

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint C: accept DAG-002 (37 added arcs: 15 admitted, 22 held; six cycles unchanged; strict audit passes; review nothing blocking; releases 15 DAG-pending deliverables). Decides both project-dag checkpoints together. | "Accept DAG-002 (Recommended)" |
| Four accepted arcs not produced (N-18, N-21, N-24, X-1): how to handle? | "A: add wording in SCA-V4-002 (Recommended)" |

The owner then interrupted the turn and, in a new message, said
"continue". Nothing had been written in between.

## Effects

- **DAG-002 is ACCEPTED on 2026-09-29, covering project-dag checkpoints 1
  and 2.**
  - Publish `_DAG/DAG-002/` byte for byte against REVIEW_PACKET.md, with
    ACCEPTANCE_RECORD.md, HANDOFF_STATE.md and MANIFEST.sha256.
  - Write `_DAG/_LATEST.md` in the prepared §11.2 form.
  - DAG-001 is superseded and kept unchanged as history.
  - A follow-up currency audit clears the 15 DAG-pending flags.
- **SCA-V4-002 scope is widened.** It now includes:
  - the DEL-10-03 "local-first" item;
  - "consumes" sentences, where the dependency is real, for N-18
    (DEL-02-01 → DEL-03-02), N-21 (DEL-02-03 → DEL-03-02), N-24
    (DEL-02-03 → DEL-03-03) and X-1 (DEL-02-03 → DEL-01-04);
  - the carried text items: the DEL-09-07, DEL-01-04 and DEL-02-02 SoW text
    on OI-001/002/012; Open_Issues OI-001/002 status; the DEL-03-03 CLM-002
    tail; the A17b line join.

  A later currency audit picks up the resulting rows as a small departure.

## Recorder's note on DECISION-10 (V13 N1)

CHECKPOINT_C §9 listed four questions. The owner was asked two (DAG-002
acceptance, and the four arcs). The other two were:

- DEL-01-01 as a new supplier (C2-3);
- DEL-09-06 as a new consumer, with the guard kept as a standing note (C2-4).

Both were applied as recommended in the package without a separate owner
answer, and are recorded as such in DAG-002/HANDOFF_STATE.md. The owner may
revisit either.
