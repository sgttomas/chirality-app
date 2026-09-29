# Receipt — APP-V4-SWBPIPE-INTAKE-20260928

This run took in SWBPIPE's answers to the App v4 relay questions and applied
the owner's phased-development direction across the App v4 definition set.
Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-SWBPIPE-INTAKE-20260928/WORK_GRAPH.md).

## Owner decisions

The decisions are recorded exactly in [OWNER_DECISIONS.md](OWNER_DECISIONS.md).

- **DECISION-3:** record the answers, run the intake, and defer the host
  joins.
- **DECISION-4, with its clarification:**
  - **Checkpoints:** phased. In Phase 1 they are plan guidance that agents
    manage themselves, with no enforcement by the App or a host loop.
    Reserved acts stand, and acts are recorded only when performed. The
    governance layer is retained for workflows that need it.
  - **Loop and panel:** they keep the v4 direction, with a note for SWBPIPE.
  - **Model access:** cloud models are reached by OAuth or an API key, with no
    default.
- **Owner merge direction:** monitor PRs and merge once CI is green. Auto-merge
  is enabled only after an independent review of the candidate finds nothing
  blocking.

## What landed

- **The SWBPIPE answers, recorded as received.** The ledger gives source,
  revision, custody and hashes for:
  - the answers as delivered in #1047, then revised in #1048: sha256
    `afb6e063…`;
  - the fact sheet: `733fb88a…`.

  They are answers about SWBPIPE's current state. They are not commitments,
  and nothing was adopted.
- **The intake map (I2):** 221 rows tracing all 32 answers to the definitions
  that depend on them.
- **R8 rulings** (R8-1…R8-12): phased checkpoints and the optional `governed`
  flag; staleness scope; whole-model identity; the SWBPIPE outcome-term
  mapping; enablement (SQ-28); the loop note; model access.
- **Definitions, all still DRAFT:**
  - EXEC → v0.4;
  - WD, WD-EX, ACT, AS, RS, C, P, LOOP, PANEL and HOSTING → v0.6;
  - ADAPTER, CA and XT → v0.4;
  - GUIDE → v0.3, with 18/18 pins verified;
  - RELAY: status and ledger only.
- **The SWBPIPE handoff** carries a note that SWBPIPE's embedded plan predates
  D-20.

## PRs

- [#1046](https://github.com/sgttomas/chirality/pull/1046): relay record,
  merged `d1cc97ce`.
- [#1050](https://github.com/sgttomas/chirality/pull/1050): the intake
  (reviews V9 and V9b). Its merge is established by GitHub.

## Checks

- **Review:** V9 returned MERGE AS DRAFTS with 0 BLOCKING items; its fixes were
  rechecked by V9b, which returned MERGE.
- **DAG currency:** both DAG-001 manifests pass. No ScopeOfWork, register,
  lifecycle or DAG-bound file changed.

## Limits and open items

- **Host joins are deferred** until the owner resumes SWBPIPE UI-SUCCESSOR.
  No join, witness or adoption is claimed.
- **Waiting on the owner:**
  - V4-HOST-02: its context and options have been presented, with a
    recommendation of option B, phased;
  - R8-Q4b: whether a launch environment variable counts as A13 evidence
    (deferred).
- **Waiting on SWBPIPE:** its owner decisions, listed in the answers' §2.
- **For the next accepted-basis update:**
  - V4-WF-05 (the first half is phased to the governance layer);
  - V4-HOST-01 and V4-ARC-11 (OAuth; no default);
  - the SoW wording that assumes runs wait: EXEC F-29, CA F-22 and GUIDE G-12.
    These join the C1 proposals of the predecessor run.
- **Minor review items carried:** V9 N-3 and N-7.
