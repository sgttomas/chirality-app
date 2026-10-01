# Receipt — APP-V4-DESIGN-PASS-2-20260930

This was the second design pass on the 14 first-increment deliverables,
planned through accepted DAG-003. Graph:
[WORK_GRAPH.md](../../WorkGraphs/APP-V4-DESIGN-PASS-2-20260930/WORK_GRAPH.md).

## Owner acts

All are recorded with the owner's exact text in
[OWNER_DECISIONS.md](OWNER_DECISIONS.md):

- **Start:** "Start the next first-increment design pass using DAG-003."
- **DECISION-K1:** "accept all six as recommended". This covers six points:
  - the agent asks for a checkpoint's act, and the product records what it
    observes;
  - in the current phase, an earlier act of the required kind counts when
    its content is still current;
  - after a partial lapse, a new act on the changed items, with the earlier
    act for the unchanged ones, answers the checkpoint;
  - the App act control is proposed for DEL-01-04's contract, and the person
    is recorded with an "identity not verified" mark;
  - a named allow-list entry stands on its own;
  - what prototypes may use.
- **Executor model:** "Ensure you are using `opus-5.5` models on `high`
  reasoning for your Type 1 and Type 2 agent instances."
- **Model download:** Qwen3 4B approved. It was not needed: an installed
  model was used, and nothing was downloaded.
- **Host-loop model interface:** "keep Chat Completions for the host loop as
  recommended." V4-ARC-10 stands.
- **OBS-1 follow-ups:** a second turn on the command-line path, then "Run the
  command-line turn locally".

## What landed

- **Wave A, alignment**
  ([#1065](https://github.com/sgttomas/chirality/pull/1065), merged
  `292e123d`):
  - 16 Design files re-pinned to the basis as amended by SCA-V4-001 and
    SCA-V4-002, and to their revised ScopeOfWork contracts;
  - the checkpoint wording now follows the amended V4-WF-05 and V4-HI-42;
  - DECISION-K1 written in, with 39 case results recomputed;
  - rulings R9 to R11;
  - the SWBPIPE handoff now shows the current standing and a list of changes
    not yet relayed.
- **Wave B, design development**
  ([#1067](https://github.com/sgttomas/chirality/pull/1067), merged
  `d01ad98a`). All new structures are PROPOSED unless a ruling decides them.
  - **Workflow declaration:** carried as a fenced JSON block in
    `WORKFLOW.md`.
  - **Execution:** a current-phase recorder and the App-run reached-when
    table.
  - **Records:** RS format 0.1 as the one container.
  - **Host operations:**
    - a catalog interface;
    - proposal identity and observation;
    - an adapter mapping for both the MCP and command-line paths;
    - a simulated host, SH-1.
  - **Hosting:** a capability account at pin 0.158.0.
  - **Network destinations:** joined end to end, with a stateless-MCP
    evidence rule.
  - **Connected activity:** an option sheet against SWBPIPE: 0 of 10 steps
    are examinable there now, and 9 of 10 on SH-1.
  - **Verification:** schemas with examples, and local prototypes in every
    folder.
- **Live observations at Codex 0.158.0 on a local LM Studio model (OBS-1 and
  OBS-1b)**:
  - the MCP path produced no tool call, because LM Studio ignored the
    `namespace` tool type;
  - the command-line path ran through Codex;
  - Chat Completions stream shapes were observed;
  - at start-up, Codex contacted chatgpt.com and github.com with analytics
    off and no sign-in.
- **Rulings R12 to R16.** R16-1 corrects R12-10: recording a declined
  destination request is required by DEL-04-03 CLM-004.
- **Closeout:**
  - [CLOSEOUT_ACCOUNT](closeout/CLOSEOUT_ACCOUNT.md) collects 42 distinct ScopeOfWork items, register
    items (counted by rows in C1-A and C1-C and by items in C1-B), 5 basis items
    and one new held arc. None is applied.
  - The items returned to the graph were done in node G (R16), except the
    LOOP/PANEL pair check, which was V20-A's; LOOP's four panel-needs gaps
    were closed in node H; V20-A's findings were repaired in RV20.
  - D0: DAG-003 is current.
  - 14 MEMORY rows.

## Checks

- **Scoping:** six surveys (S1-A to S1-F).
- **Receiver comparisons:** V18-1 to V18-4 covered 58 joins, including N-18,
  N-21, N-24 and X-1.
- **Independent reviews:**
  - V17-A and V17-B both returned HOLD; V17b then returned MERGE AS DRAFTS.
  - V19-A returned MERGE AS DRAFTS and V19-B returned HOLD; V19b then
    returned MERGE AS DRAFTS.
  - V20-A returned HOLD (one label inconsistency) and V20-B MERGE; both
    were repaired in RV20; the recheck V20b returned MERGE.
- **Prototypes:** rerun by the integrator after each round and by every
  reviewer. The reviewers' independent `jsonschema` checks agreed.
- **GUIDE input pins:** 18/18.
- **DAG-003:** manifests 37/37 and 130/130; the analyzer reports
  NO_DEPARTURE_FOUND.
- **Write fences:** verified by `git status` after each writing executor, as
  DISPATCH records; reviewers' and comparators' own reports state their
  fences.
- **Executors:** after the owner's direction they ran on Claude Opus 5.5 at
  high effort. Earlier nodes ran on Claude Fable 5.1, as recorded in
  [DISPATCH.md](DISPATCH.md).

## Limits

- All Design files stay DRAFT: unsupplied, unimplemented and not accepted.
- No case has run against a product candidate.
- Observations are dated and at one version; nothing is qualified.
- Host joins stay deferred (DECISION-3). No SWBPIPE join, witness or adoption
  is claimed, and nothing was relayed.
- No ScopeOfWork, register, status, basis, decomposition, scope-change or DAG
  file changed. Applying the closeout's proposals is a later amendment.
- Open for the owner's phase review:
  - the consequence vocabulary;
  - OI-003, OI-008, OI-009, OI-013 and OI-014;
  - the A12 mapping of a destination grant;
  - DEL-05-02's destination surfaces;
  - the supplier's start-up traffic;
  - whether RS records a first turn refused "selection not established";
  - how long a host loop holds events for replay (OI-013);
  - OI-021 and the next relay, when UI-SUCCESSOR resumes.
- This undertaking does not pass the 60% gate.
