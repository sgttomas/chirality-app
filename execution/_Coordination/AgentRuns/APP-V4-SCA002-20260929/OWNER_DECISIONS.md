# Owner decisions — APP-V4-SCA002-20260929

## Direction to start (owner, exact, 2026-09-29)

**Question.** "Should you run a closure audit on SCA-V4-001 first or can we
run the audit after you complete SCA-V4-002 and determine if a DAG-003 is
required?"

**Recorder's proposal.** Run it now:

1. In parallel: the SCA-V4-001 closure audit, and preparation of
   SCA-V4-002's package, folding in any gaps the audit finds.
2. The SCA-V4-002 checkpoints.
3. REVISE the affected SoWs and re-extract.
4. DAG-003 for owner acceptance, if the new arcs are confirmed.
5. SCA-V4-002's closure audit.

**Owner:**

> "Proposal accepted.  Proceed accordingly."

## Scope of SCA-V4-002, as decided so far

The sources are APP-V4-BASIS-ALIGN-20260928 DECISION-8 and DECISION-10.

1. DEL-10-03 ScopeOfWork REQ-005: "the minimal local-first host loop".
2. "Consumes" sentences, where the dependency is real, for:
   - N-18: DEL-02-01 → DEL-03-02;
   - N-21: DEL-02-03 → DEL-03-02;
   - N-24: DEL-02-03 → DEL-03-03;
   - X-1: DEL-02-03 → DEL-01-04.
3. Carried text items:
   - the DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012;
   - the DEL-03-03 CLM-002 tail;
   - the A17b line join in HOST_INTEGRATION.
4. **To be proposed at group 1, not assumed** (V13 F3): the Open_Issues
   OI-001/002 status.
5. Record fixes V13 raised:
   - F2: `_ScopeChange/_LATEST.md` needs `Latest:`/`Updated:` lines;
   - F1: the group-3 manifest label, disclosed but not rewritten.

The SWBPIPE handoff "local-first" note is carried with the next relay to
SWBPIPE. It is not part of this amendment.

## Checkpoint A: SCA-V4-002 scope-change groups 1 and 2 (owner, exact, 2026-09-29), DECISION-2

**Context.** The owner reviewed the packet (commit `f05bd1bbd`) on the review
page https://claude.ai/artifact/QQmWJoHTRfkXriBs66ghNS. The files were:

| File | sha256 |
|---|---|
| OWNER_ITEMS.md | `1d46458c…` |
| IMPACT_ASSESSMENT.md | `46444eab…` |
| BASIS_AMENDMENT.md | `091871fd…` |
| SOW_REVISIONS.md | `440d4d50…` |
| ARC_EFFECT.md | `4b3aeec0…` |

The recorder's message said: "When you're ready, reply 'accept the remaining
items as recommended', or name the items you want changed."

> "accept the remaining items as recommended"

## Effects

- **SCA-V4-002 groups 1 and 2 are accepted**, as recommended in OWNER_ITEMS
  Q-1…Q-15. That covers:
  - identity, scope, write boundary, route and register;
  - all four arcs kept (N-18, N-21, N-24, X-1);
  - OI-001/002 kept OPEN (option A);
  - the Q-6 same-class fixes included;
  - the OI-012 pointer;
  - A17b as a line break;
  - the §11.2 pointer form;
  - ASC-ISS-001 option (a): the 17 DL rows;
  - the DEL-04-01 qualifier;
  - ASC-ISS-006 option (a): reading-rule notes;
  - the SCA-V4-001 effective-state record;
  - each decision snapshot committed before the next stage;
  - DECISION-8 confirmed as the deferral record for the Design re-pins.
- **Timing disclosure.** The owner decided while the pre-change audit-decomp
  baseline (node P3, method step 5) was still running; it had been
  interrupted by a connection error and resumed. The group-1 snapshot is
  written only after the baseline completes. If the baseline finds anything
  that changes the packet, the owner is told before application.
