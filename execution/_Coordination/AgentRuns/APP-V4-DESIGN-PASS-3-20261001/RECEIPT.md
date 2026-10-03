# Receipt — APP-V4-DESIGN-PASS-3-20261001

The third design pass. It gave the six standalone-App deliverables (DEL-01-02,
01-03, 01-04, 01-05, 02-02, 02-04) their first Design files and aligned the
first-increment files with them. It was planned through accepted DAG-003.
Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-DESIGN-PASS-3-20261001/WORK_GRAPH.md).

## Owner acts

All are recorded with the owner's exact text in
[OWNER_DECISIONS.md](OWNER_DECISIONS.md):

- **Start:** "Proceed as recommended." This meant a decision sitting first,
  then the design pass, with the amendment folded in.
- **DECISION-K3, as revised:**
  - K-1…K-6 and K-8…K-12 as recommended;
  - K-7 the owner's choice: only registered revisions run, and drafts are
    tried in conversation.
- **Sign in with ChatGPT:** assessed at the owner's request
  ([ASSESSMENT_SIWC.md](ASSESSMENT_SIWC.md)). The owner noted that pinning
  can only last so long.
- **DECISION-L:**
  - L-1 and L-3…L-7 as recommended.
  - L-2 the owner's choice: a conversation's role is fixed, and workflows
    chain within a conversation, either (a) sequentially or (b) on the
    agent's proposal with the person confirming.
  - L-4 clarified: shipped workflows are registered by the release.
  - "run the local check".
- **Closeout:** "yes, run the closeout."

## What landed

- **The design work**
  ([#1072](https://github.com/sgttomas/chirality/pull/1072), merged
  `a533dc2d`). All new structures are PROPOSED unless a ruling decides them.
  - **New Design files (v0.2), each with schemas, examples and a prototype:**

    | File | Deliverable | Covers |
    |---|---|---|
    | RECOVERY | DEL-01-02 | three kinds of stop, quit and relaunch, a Codex process per App home |
    | NPTD | DEL-01-03 | plan, tool, delegation and goal views; delegation availability read at run time |
    | NIR and AAC | DEL-01-04 | request cards; the person-only act control, including several registrations in one act |
    | ACCESS and the account-home record | DEL-01-05 | shared settings with a separate sign-in; a second App home for API-key conversations; start-up traffic per the person's plugin setting |
    | WR | DEL-02-02 | library revisions; the workflow supplied per run as turn text and checked against Codex's history; chaining |
    | ROLE | DEL-02-04 | role guidance fixed per conversation; "Continue as ‹role›" |

  - **First-increment files updated:**
    - HOSTING-v0.9, EXEC-v0.7, RS/ACT-POLICY/AS-v0.9;
    - WD/WD-EX-v0.9, CA-v0.7;
    - ADAPTER/XT-v0.7, LOOP/PANEL-v0.9;
    - GUIDE-v0.6.
  - **Observations at Codex 0.158.0 on a local LM Studio model:** OBS-2 and
    OBS-3. They covered interrupt, quit and restart, requests resolved by
    Codex, delegation (through an adapter), resume and fork instructions,
    shared settings, start-up traffic, plan mode and per-turn workflow
    supply.
  - **Rulings:** R17–R21.
- **Closeout (this PR):**
  - C0 fixed the remaining MINORs.
  - C1-A and C1-B are the bounded reconciliation, with the account in
    [closeout/CLOSEOUT_ACCOUNT.md](closeout/CLOSEOUT_ACCOUNT.md).
  - G applied R22.
  - GUIDE was re-pinned 25/25.
  - MEMORY rows were added for 18 deliverables.
- **SCA-V4-003** was opened as run `APP-V4-SCA003-20261002`. It carries the
  contract proposals of passes 2 and 3 and is prepared toward its first
  owner checkpoint.

## Checks

- **Surveys:** S1-A…C.
- **Join consolidation:** F0, with 112 rows and 25 conflicts ruled.
- **Independent reviews:**
  - V21-A and V21-B returned MERGE AS DRAFTS (5 MAJOR in all), repaired in
    RV21-A/B;
  - the rechecks V21b-A and V21b-B returned MERGE AS DRAFTS.
- **Prototypes:** all rerun clean in the twenty touched Design folders after
  every repair.
- **Citations and pins:**
  - the citation check over the run found none missing;
  - GUIDE is at 25/25.
- **DAG-003:**
  - manifests 37/37 and 130/130;
  - the analyzer reports NO_DEPARTURE_FOUND;
  - every proposed row is SCC-neutral.
- **Write fences:** verified after each writing executor (DISPATCH).
- **Executors:** Claude Opus 5.5, high effort.
- **Deviation:** OBS-2 continued past stop condition S-9 (recorded).

## Limits

- All Design files stay DRAFT: nothing is implemented, qualified or
  accepted.
- No case has run against an App candidate.
- Observations are dated, at one Codex version and one local model.
- Host joins stay deferred (DECISION-3). No SWBPIPE join or adoption is
  claimed. The next-relay list gained the plan-billing note; nothing was
  relayed.
- No ScopeOfWork, register, `_STATUS.md`, decomposition, DAG or basis file
  changed. The six deliverables stay INITIALIZED. Moving them to IN_PROGRESS
  is put to the owner with SCA-V4-003 (R22-5).
- **Open for the owner or the phase review:**
  - OI-008 (where act capture runs);
  - the child-role carrier under K-1 (unobserved);
  - an instruction-change notice for Root `AGENTS.md`'s "verified idle
    boundary" sentence, which L-2 no longer matches;
  - a version-advance check against the current Codex release (it needs a
    download);
  - the items carried from pass 2.
- This undertaking does not pass the 60% gate.
