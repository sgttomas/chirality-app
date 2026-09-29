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
- **DECISION-5 (V4-HOST-02, host-agent network destinations),** with its
  confirmation:
  - Option B: a two-level allow list (category switches and named
    destinations), plus permissions requested during the work, scoped
    **once**, **this run** or **always**.
  - **MCP:** stateless MCP revision 2026-07-28 only ("MCP V2", a reading the
    owner confirmed).
  - **Always off:** analytics, a silent provider switch and background
    downloads.
  - **Record and show:** every destination contacted is recorded and shown.
  - **Other points:** the "in local operation" qualifier is dropped; the
    person-only grant was not objected to and stands.
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
- **R8-13 (DECISION-5):** applied in place by node B1 to LOOP (NW-8…NW-16,
  MS-14…MS-22), PANEL §3.8, ACT §2.7 (A12 subclass "network-destination
  grant" under D2 (e), INTEGRATION), AS §3, RS R15, HOSTING, C, ADAPTER and
  GUIDE (B-11, M7.9, HC-7.7…HC-7.9). All 18 pins are verified.
- **The SWBPIPE handoff** carries a note that SWBPIPE's embedded plan predates
  D-20.

## PRs

- [#1046](https://github.com/sgttomas/chirality/pull/1046): relay record,
  merged `d1cc97ce`.
- [#1050](https://github.com/sgttomas/chirality/pull/1050): the intake
  (reviews V9 and V9b), merged `bc0337b3`.
- [#1051](https://github.com/sgttomas/chirality/pull/1051): DECISION-5 and
  this closeout (reviews V10 and V10b). Its merge is established by GitHub.

## Checks

- **Review of #1050:** V9 returned MERGE AS DRAFTS with 0 BLOCKING items; its
  fixes were rechecked by V9b, which returned MERGE.
- **Review of #1051:** V10 found one BLOCKING item, in this receipt, plus
  four SHOULD-FIX items. All were fixed; V10b is the recheck.
- **DAG currency:** both DAG-001 manifests pass. No ScopeOfWork, register,
  lifecycle or DAG-bound file changed.

## Limits and open items

- **Host joins are deferred** until the owner resumes SWBPIPE UI-SUCCESSOR.
  No join, witness or adoption is claimed.
- **Waiting on the owner:**
  - LOOP N-OPEN-4: how a category switch combines with its named entries.
    The interim reading treats them as alternatives;
  - taking up the governance phase;
  - R8-Q4b: whether a launch environment variable counts as A13 evidence
    (deferred).
- **Waiting on SWBPIPE:** its owner decisions, listed in the answers' §2.
- **For the next accepted-basis update:**
  - V4-WF-05 (the first half is phased to the governance layer);
  - V4-HOST-01 and V4-ARC-11 (OAuth; no default);
  - V4-HOST-02, revised per DECISION-5;
  - the SoW wording that assumes runs wait: EXEC F-29, CA F-22 and GUIDE G-12.
    These join the C1 proposals of the predecessor run.
- **Open elsewhere:**
  - LOOP N-OPEN-5: evidence that an MCP server is stateless. The PROPOSED
    reading treats a server with no evidence as not stateless.
  - The DECISION-5 host obligations (M7.9, HC-7.7…HC-7.9) go to SWBPIPE in the
    next relay, when UI-SUCCESSOR resumes. RELAY SQ-16 and SQ-30 keep the old
    V4-HOST-02 wording, as relayed.
- **Minor review items carried:** V9 N-3 and N-7; the V10 NOTEs.
