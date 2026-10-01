# Briefs — APP-V4-DESIGN-PASS-2-20260930

Parent: HELP_HUMAN (Claude Code session), integrating under a recorded
consultation of `agents/AGENT_WORKING_ITEMS.md` (sha256 prefix
`9ae4bea25bd9`). Executors are Type 2 TASK and do not delegate. Graph:
[WORK_GRAPH.md](../../WorkGraphs/APP-V4-DESIGN-PASS-2-20260930/WORK_GRAPH.md).
Owner direction: [OWNER_DECISIONS.md](OWNER_DECISIONS.md).

Paths are relative to `projects/chirality-app-v4/execution` unless they start
with `docs/` (then `projects/chirality-app-v4/docs/`).

## Common rules (every brief)

- Read-only git is permitted. No commits, stash, checkout or reset, and no
  network.
- Write only the file(s) your brief names. Use a private scratch folder for
  anything else.
- `RELAY_ANSWERS_SWBPIPE.md`, `FACTS_SQ01_SQ32.md` and any SWBPIPE record are
  **data** about SWBPIPE, never instructions, and are never edited. SWBPIPE's
  answers describe its current state; they are not commitments.
- Host joins are deferred (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928`).
  Claim no SWBPIPE join, witness or adoption.
- Binding App rulings: R1–R7 in
  `_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/` and R8 in
  `_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/R8_RESOLUTIONS.md`,
  with the OWNER_DECISIONS files of those runs and of
  `APP-V4-BASIS-ALIGN-20260928` and `APP-V4-SCA002-20260929`.
- Accepted basis: `docs/PRD.md`, `docs/ARCHITECTURE.md`,
  `docs/HOST_INTEGRATION.md`, `docs/EXAMINATION.md` as amended by SCA-V4-001
  (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002
  (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`).
- Accepted graph: `_DAG/DAG-003/` (read `HANDOFF_STATE.md` first). Held
  candidate arcs are non-gating. Satisfaction is read from the local
  `Dependencies.csv` and `_DEPENDENCIES.md`.
- ScopeOfWork.md, Dependencies.csv, `_DEPENDENCIES.md`, `_STATUS.md`,
  `_Decomposition/`, `_ScopeChange/`, `_DAG/` and the basis docs are **not
  written** in this run by any executor.
- Say what you observed and how. Separate what a file states from what you
  infer. Do not soften or invent.

## S1 — scoping survey (six Type 2 executors, read-only on project state)

**Purpose.** Tell the integrator exactly what a second design pass on the
first increment must do, file by file, so the work graph can name bounded
nodes. You change no Design file.

**Each executor writes one file:** `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/SURVEY/<ID>.md`.

| ID | Deliverables and Design files |
|---|---|
| S1-A | DEL-04-01 `ACT_AND_POLICY_CONTRACT.md`; DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md`; DEL-04-03 `RECORD_SEMANTICS.md` |
| S1-B | DEL-03-01 `CATALOG_AND_READ_BASIS.md`; DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`; DEL-03-03 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` |
| S1-C | DEL-02-01 `WORKFLOW_DECLARATION.md` and `EXAMPLES.md`; DEL-02-03 `EXECUTION_COMPATIBILITY.md` |
| S1-D | DEL-05-01 `LOOP_RECEIVING_CONTRACT.md`; DEL-05-02 `PANEL_RECEIVING_CONTRACT.md`; DEL-01-01 `HOSTING_BOUNDARY.md` and `PIN_SPIKE_0.158.0.md` |
| S1-E | DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` and `RELAY_QUESTIONS_SWBPIPE.md` (with the two SWBPIPE files as data); DEL-09-09 `EXTERNAL_TRACE_CASES.md`; DEL-03-04 `HOST_INTEGRATION_GUIDE.md` |
| S1-F | The deliverables **outside** the 14 that DAG-003 joins to them (see below) |

**S1-A…S1-E: for each Design file in your row, report these sections.**

1. **Pins.** Every pin or version reference the file carries (basis-doc
   sections or quoted requirement texts, ScopeOfWork sha256 or revision,
   sibling Design versions, run rulings). For each: current or stale, checked
   how (recompute sha256; compare quoted text with the current source), and
   the current value. Quote each stale requirement text next to the current
   text.
2. **ScopeOfWork alignment.** Read the deliverable's current
   `ScopeOfWork.md` whole. For every obligation it states (its CLM, REQ, OUT,
   VER and similar identified items): where the Design file answers it, and
   whether the answer is developed, partial, only named, or absent. List every
   place the Design text contradicts or lags the revised SoW wording. The SoW
   changes are in the two amendment snapshots and in
   `_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/RV/` and
   `APP-V4-SCA002-20260929/RV/`.
3. **Amended basis.** Whether the Design text agrees with the amended
   V4-WF-05, V4-HOST-01, V4-HOST-02, V4-ARC-11, V4-ARC-12, V4-HI-42,
   V4-HI-70, V4-EXM-22, V4-EXM-23 and the amended "local-first" wording,
   wherever the file touches them. R8 was applied before the basis was
   amended, so compare wording, not just intent.
4. **Open items.** Every item the file leaves open (UNRESOLVED, OPEN,
   PROPOSED, TBD, "not established", carried questions). For each: its ID,
   one line on what is open, the owner and point of need the file states, and
   your class:
   - **NOW** — answerable from records that exist today (name the record);
   - **OWNER** — needs an owner decision (say what the choice is);
   - **HOST** — needs SWBPIPE or another host (deferred);
   - **SPIKE** — needs a bounded prototype or observation (say which);
   - **LATER** — properly belongs after the 60% gate (say why).
5. **Design depth against the 60% description.** `loop/LOOP_INIT.md`
   ("Develop the detail appropriate to the phase") asks for interfaces,
   states, data, operating sequences, failure behaviour and verification.
   For each of those six, say what the file has and what is missing for each
   contribution the deliverable exchanges. Name any structural choice still
   open that could force a later restructuring of this file or of a consumer.
   Be concrete: cite sections.
6. **Joins.** For every ACTIVE row in the deliverable's `Dependencies.csv`
   whose other end is one of the 14 first-increment deliverables: the row ID,
   the contribution named, whether DAG-003 admits or holds the arc, and
   whether the supplier's Design file actually contains that contribution in a
   form the consumer's Design file uses (cite both places). Include the new
   arcs N-18, N-21, N-24 and X-1 where they touch your row. Report
   disagreements between the two files' statements of the same exchange.
7. **Carried review items** that name this file: first-run `reviews/V6.md`
   (m-1, m-3…m-7) and `closeout/`; intake `reviews/V9.md` (N-3, N-7) and
   `V10.md` (NOTEs); `APP-V4-BASIS-ALIGN-20260928/reviews/` and
   `APP-V4-SCA002-20260929/reviews/` where they name a Design file. For each:
   still open or already fixed, with the evidence.
8. **Recommended work on this file in this pass**, as a short numbered list
   of bounded changes, each tagged with the section numbers above that
   justify it; then what should not be attempted in this pass and why.

End with a table across your files: counts per open-item class, count of
stale pins, and the three most consequential gaps.

**S1-F: outside suppliers and consumers.** From `_DAG/DAG-003/`
`DependencyEdges.csv` and `CandidateEdges.csv`, take every arc with exactly
one end among the 14 first-increment deliverables (DEL-01-01, 02-01, 02-03,
03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09).
For each arc report: arc, admitted or held, the representative register row,
the contribution and the part of the consumer's work that waits for it (from
the live register rows and both ScopeOfWork files), and:

- when the consumer is one of the 14 and the supplier is outside: whether any
  of the 17 Design files already assumes a shape for that contribution (cite),
  whether the first-increment **design** needs the supplier's definition now,
  or only its implementation or qualification later, and what the smallest
  supplier-side definition would be if it is needed now;
- when the supplier is one of the 14 and the consumer is outside: whether the
  supplier's Design file offers what the consumer's SoW and register row
  ask for.

Then list, for DEL-01-02, 01-04, 01-05, 02-02, 02-04 and 09-01, what exists
in their folders beyond the ScopeOfWork and registers, and whether their
SoWs were revised by SCA-V4-001 or SCA-V4-002. Close with your recommendation
on whether any outside deliverable needs design work inside this pass, and
which, with reasons for and against. This is advice for an owner question; do
not treat it as settled.

## A1 — alignment wave (five Type 2 executors in parallel, then GUIDE)

**Purpose.** Bring each Design file onto the amended basis and its revised
ScopeOfWork, under [R9_RESOLUTIONS.md](R9_RESOLUTIONS.md). No new design
content: that is Wave B.

**Inputs for each executor:** R9_RESOLUTIONS.md (binding); its own survey
report in `SURVEY/` (sections 1, 2, 3, 6 and 7 per file, the section 4 items
classed NOW, and the section 8 items listed below); the current sources the
report cites. The survey is advice: check each item against the current
source before editing, and say so where you disagree with it.

| ID | Files (write fence: these files only, plus the return file) | Survey | Section 8 items to apply |
|---|---|---|---|
| A1-A | ACT, AS, RS | S1-A | ACT 1–6; AS 1, 2, 6 and the Receivers part of 5 as a table of named receivers only; RS 1–4 |
| A1-B | C, P, ADAPTER | S1-B | C 1–3, 7; P 1–3, 6; ADAPTER 1, 2, 9 |
| A1-C | WD, WD-EX (`EXAMPLES.md`), EXEC | S1-C | WD 1–4 and the parts of 8 that R9 or a ScopeOfWork decides; WD-EX 1, 5; EXEC 1–4, 10 |
| A1-D | LOOP, PANEL, HOSTING (not PIN_SPIKE) | S1-D | LOOP 1–4 and the N-OPEN-4 note of 6; PANEL 1–4, 6; HOSTING 1–3 |
| A1-E | CA, RELAY (metadata only), XT | S1-E | CA 1–4, 7, 8; RELAY 1–3; XT 1–4, 6 and the Receivers part of 7 |
| A1-G | GUIDE, after A1-A…A1-E are integrated | S1-E part D | GUIDE 1–4 |

**Rules for the edit.**

- Apply R9-1…R9-11. Use the R9-1 summary sentence, or quote the amended
  texts; do not write a new paraphrase.
- Bump the version per R9-11 and add a "Changes from ‹previous›" table whose
  rows carry R9 item IDs or the survey item they answer.
- Anything in section 8 that is not listed for your row is Wave B. Do not
  start it. Where an edit you make touches a Wave B passage, change only the
  wording R9 requires.
- Sibling files are cited by version label and section (R9-5). Cite siblings
  at their Wave A versions (R9-11 table); all five executors edit in
  parallel, so cite the label, not bytes.
- A need for a ScopeOfWork, register or basis change is returned, never
  made.

**Return file:** `WAVE_A/<ID>.md`, with:

1. per file: each change made (item → section or line), and the file's new
   sha256;
2. survey items you did not apply, with the reason;
3. R10 candidates (R9-9): the two passages and the options;
4. proposed ScopeOfWork, register or basis items for a later amendment;
5. Wave B items you found beyond the survey's;
6. the pin table of each header as it now stands, with how each was checked.

## K0 — owner decision package, draft (one Type 2, read-only on project state)

**Purpose.** Prepare, for the integrator, a plain-language draft of the
choices the six surveys class as the owner's. The integrator will check it,
add recommendations and put it to the owner. You decide nothing.

**Write one file:** `DECISIONS_DRAFT.md` in this run folder.

**Inputs:** the six survey reports (their OWNER-class items, their "owner-level
choices" lists and S1-F §2.3 and §5); the Design passages and records they
cite; the four OWNER_DECISIONS files of the predecessor runs (so that nothing
already decided is asked again).

**For each distinct choice** (merge the same choice seen from several files):

- a short plain name, and the IDs it carries in the files;
- what the choice is, in words a reader who has not opened the Design files
  can follow, with a concrete example of how the product behaves under each
  option;
- the options as the files state them, and any option the files omit;
- what each option costs and what it changes in the first-increment design
  (which files, how large);
- whether the first-increment design can reach the 60% level without the
  decision, and if so what stays open;
- whether it was already decided or deferred by the owner, with the record;
- who else it depends on (SWBPIPE, a later deliverable).

Sort into three groups: (1) shapes the design now; (2) can wait for the phase
review; (3) already deferred with the host joins or the governance phase.
Include, at least: the reading of "the act is requested" (R9-1); the App act
control and DEL-01-04's contract; the person identity scheme; counting a
prior act versus capture at or after arrival (SP-6); partial lapse of a
multi-row grant; placement of shared parts (OI-013, OI-014, OI-008, U-15);
the catalog-extension promise (OI-003); the consequence vocabulary; the A12
mapping of a network-destination grant; category switch versus named entries
(N-OPEN-4); who names the host model-interface basis; the panel's
network-destination surfaces against DEL-05-02's contract; registration as a
recorded act; the account home (OI-009); custody of the shared fixture
FX-PIPE-01; the first connected operation (OI-021) and whether to prepare an
option sheet against SWBPIPE's actual journey; the supplier's start-up fetch
and its experimental surface; and whether a spike may use a credential, a
local model server or the network.

## A3 — apply DECISION-K1 in the Design files (one Type 2)

**Purpose.** Write the owner's DECISION-K1 (in [OWNER_DECISIONS.md](OWNER_DECISIONS.md))
into the 15 Wave A Design files, so that the Wave A candidate stands on it.
Items K1-1…K1-5 only. K1-6 (what prototypes may use) changes no Design text
now.

**Write fence:** the same 15 Design files as A2 (RELAY metadata only, §0–§3
byte-identical, span sha256 `6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d`);
return file `WAVE_A/A3.md`. Not GUIDE (A1-G does it next), not PIN_SPIKE, not
SWBPIPE's two files, and no ScopeOfWork, register, status, basis,
decomposition, scope-change or DAG file.

**What to apply** (find every carrier with grep; the surveys, `DECISIONS_DRAFT.md`
"Where it sits" lines and `DECISIONS_PENDING.md` list the IDs):

1. **K1-1.** R9-1's requester reading is SETTLED by DECISION-K1. Relabel it
   wherever a file carries it as INTEGRATION or "put to the owner"; close the
   matching UNRESOLVED rows.
2. **K1-2.** For the current phase, an earlier act counts when it is of the
   required kind and the content it was made on is still current; the record
   cites the earlier act and its time. The rule "only acts captured at or
   after arrival" (SP-6; EXEC §4.5, U-E4, F-23; WD I-8, U-31; ACT §4.5, U-14,
   F-17; AS U-17; RS L-13, U-26; LOOP and PANEL rows; C V-GR1; P §10; CA row
   9) is kept only as a governance-phase option a workflow may take up.
   Recompute each designed case whose expected result depends on it (for
   example EXEC CH-12, CH-20 and CH-9 (ii); LOOP FX-C4b, FX-C11b; PANEL W-5c,
   PC-21i) and state the new expected result. The label "prior act, not
   counted" stays only for an earlier act whose content is no longer current
   or whose kind differs.
3. **K1-3.** When one act covered several items and only some change, a new
   act on the changed items alone answers the checkpoint together with the
   earlier act for the unchanged items. Write the rule (two or more acts may
   together answer one arrival; each cites its items) in EXEC §4.7 and ACT
   §4.3, and follow it in WD U-05c, RS U-07, AS U-19, CA DI-7 and the LOOP and
   PANEL rows. Release the held cases (EXEC CH-8 and any other held on this
   question) with their expected results.
4. **K1-4.**
   - The App person identity: the App records the name the person set in the
     App, the operating-system account, and the Codex account when Codex
     reports one, marked "identity not verified"; a verified identity is a
     governance-phase matter. Write this into RS §6.1 (decision actor and its
     evidence limit), EXEC CAP-8, and close EXEC U-E8, RS U-28, WD U-25 and
     EXAMPLES U-25 by citing DECISION-K1.
   - The App act control: its construction stays with DEL-01-04 (a later
     undertaking). Where a file says the obligation is missing from that
     deliverable's contract, add: "proposed for DEL-01-04's contract at the
     next amendment (DECISION-K1 K1-4); collected at this run's closeout".
     Do not design the control.
5. **K1-5.** A named destination is allowed on its own; a category switch
   means "allow everything in this category"; with the switch off only the
   named entries in it are allowed. Close LOOP N-OPEN-4 and write the rule in
   LOOP NW-8 (or wherever the allow-list rule sits), PANEL ND-1 and AS's
   allow-list rows; recompute LOOP MS-15, MS-18 and PANEL PC-30, PC-34.
6. **Also:** LOOP §2.2 cites "DEL-03-01 F-R2-2", which exists nowhere (A2
   finding 1). Find what the sentence relies on in C-v0.7 and cite that, or
   remove the citation and say so in the return file.

**Rules.** Precise edits. Record each change as a row in the file's Wave A
change table with the K1 item ID. No version bump. Where applying a decision
would change something only a ScopeOfWork or basis text can decide, stop on
that item and return it.

**Return file `WAVE_A/A3.md`:** per file, the changes (K1 item → location)
and the new sha256; every designed case whose expected result changed, old →
new; anything not applied, with the reason; any proposed ScopeOfWork or basis
item.

## A1-G — GUIDE alignment and final re-pin (one Type 2, last in Wave A)

**Purpose.** Bring DEL-03-04 `HOST_INTEGRATION_GUIDE.md` from v0.3 to v0.4 on
the Wave A candidate: the other 16 Design files are final for Wave A (A1,
A2, A3 committed).

**Write fence:** `HOST_INTEGRATION_GUIDE.md` and `WAVE_A/A1-G.md` only.

**Apply:** R9 (all items), R10 (where GUIDE carries the same wording, notably
R10-1 and the "DECISION-2 reading" labels of R10-11) and DECISION-K1 (the
same relabels and rule changes A3 made in the other files; see
`WAVE_A/A3.md`), plus survey S1-E part D items 1–4 (section D.8). In detail:

1. Re-pin the 18-row input table to the current sha256 of every pinned input,
   by script, after reading the table's row definitions; record the script
   and its output in the return file. Pin the ScopeOfWork, the register and
   the basis docs as S1-E D.8 item 1 lists.
2. Rerun CC-1…CC-11 against the revised ScopeOfWork and the amended basis,
   and rewrite what their recorded results describe; close G-6, G-7, G-12,
   F-5, F-6, F-16 and the UNRESOLVED rows S1-E D.8 item 2 lists, each with the
   record that closes it; withdraw F-4 if the record shows it is withdrawn.
3. Add RS R15 to M5.6 and HC-5.5 (amended V4-HI-70).
4. Record what exists (RV-3 result, V9 and V10 reviews, stating their scope);
   scope M8.1's default (V6 m-6); follow WD and EXEC on the partition
   sentence (V6 m-7, as R10-10 ruled).
5. Update every sibling version label to the Wave A versions (R9-11) and check
   each cited section or ID exists in the sibling's current text.

Not in this node: the matrix refresh for Wave B (node B8), anything S1-E D.8
lists as "not in this pass".

**Return file `WAVE_A/A1-G.md`:** the changes (item → location); the pin
script and its full output (18/18 or the failures); CC-1…CC-11 results, old →
new; anything not applied; GUIDE's new sha256.

## V17 — independent review of the Wave A candidate (two Type 2 reviewers)

**Candidate:** the branch at the commit named in your launch message. Base
for the diff: `74b3c73134` (main when the run started). Read-only on project
state; each reviewer writes one file, `reviews/V17-A.md` or `reviews/V17-B.md`.
You did not write any of this; review it as a stranger to it.

| Reviewer | Design files |
|---|---|
| V17-A | ACT, AS, RS (PKG-04); C, P, ADAPTER (PKG-03); GUIDE (DEL-03-04) |
| V17-B | WD, WD-EX, EXEC (PKG-02); LOOP, PANEL (PKG-05); HOSTING (DEL-01-01); CA, RELAY, XT (PKG-09); `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`; and the run records (graph, OWNER_DECISIONS, DISPATCH, R9, R10) |

**What the candidate claims** (check each; do not take it on trust):

1. Every edit is alignment only: re-pins; the amended basis wording; the
   revised ScopeOfWork; closing items a record already closed; receivers;
   R9, R10 and DECISION-K1. No new design content beyond what those require.
2. Pins in each header are current (recompute sha256 of each pinned input).
   GUIDE's 18-row table matches 18/18.
3. Quoted requirement texts match their sources exactly.
4. R9 as corrected by R10-1, R10-1…R10-11, and DECISION-K1 items K1-1…K1-5
   are applied faithfully and consistently across files: the same rule says
   the same thing everywhere it appears. Look hardest at: who requests the
   act (K1-1); the earlier-act rule SP-6 and SP-6F (K1-2); the joint answer
   JA-1 (K1-3); identity "not verified" (K1-4); the allow-list rule (K1-5);
   the direct-application case (R10-1).
5. The 37 recomputed case results (listed in `WAVE_A/A3.md` §2; the correct
   count is 39, per V17-B m-1) follow from
   the new rules. Check at least 12, chosen across files, and every case in
   your files whose result changed.
6. Nothing claims more than the owner decided: check each file's statements
   of DECISION-K1 against OWNER_DECISIONS.md, and that nothing reads a
   recommendation or an integrator ruling as an owner decision.
7. The governance-phase definitions are retained, relabelled only.
8. RELAY §0–§3 is byte-identical to `74b3c73134`; PIN_SPIKE, SWBPIPE's two
   files, every ScopeOfWork, register, status file, basis doc, decomposition,
   scope-change and DAG file are byte-identical to `74b3c73134`; DAG-003's
   two manifests pass.
9. Cross-file citations resolve (section or ID exists and says what the
   citing sentence claims), in your files.
10. (V17-B) The run records are true: every state the graph and DISPATCH
    record matches git; OWNER_DECISIONS quotes the owner exactly as the
    records elsewhere show; the HANDOFF edits are true and relay nothing.

**Return file:** a verdict, **MERGE AS DRAFTS** or **HOLD**, then findings,
each classed **BLOCKING** (the candidate says something false, contradicts
itself across files, or claims more than was decided), **MAJOR**, **MINOR**
or **NOTE**, with file, location, the passages quoted and a proposed fix. Say
what you checked and how, and what you did not check.

## A4 — repairs from V17 (one Type 2)

**Purpose.** Apply [R11_RESOLUTIONS.md](R11_RESOLUTIONS.md) R11-1…R11-9 and
the two note items it lists (V17-A N-1, N-2). R11-10 is the integrator's and
is done.

**Write fence:** the 16 Wave A Design files (the 15 of A2 plus
`HOST_INTEGRATION_GUIDE.md`); RELAY metadata only, §0–§3 byte-identical
(span sha256 `6e399c8389dc2ad991ba8b64084fee17d44ef9e8137d184dd8eb599a66340d4d`);
return file `WAVE_A/A4.md`. Nothing else.

**Rules.** Read each finding in `reviews/V17-A.md` and `reviews/V17-B.md`
before fixing it; the reviewers quote the passages. Precise edits; record each
as a row in the file's Wave A change table with the R11 item ID; no version
bump. For R11-3, compute the five pinned values first, apply them everywhere a
header pins those records, and re-verify every pin at the end by script,
including GUIDE's 18-row table.

**Return file `WAVE_A/A4.md`:** per R11 item, what changed where; new sha256
per file; the pin script and its output; anything not applied, with the
reason.

## V17b — recheck of the V17 repairs (one Type 2 reviewer)

**Candidate:** the commit named in your launch message; the repairs are the
diff from `24789a3c3b` to it. Read-only; write only `reviews/V17b.md`.

Check that every V17-A and V17-B finding is closed as
[R11_RESOLUTIONS.md](R11_RESOLUTIONS.md) disposes of it, or carried where
R11 says; that the A4 diff introduced nothing false, inconsistent across
files, or beyond R11; that every header pin that claims current bytes
matches (recompute), GUIDE's table 18/18, RELAY §0–§3 byte-identical to
`74b3c73134`; and that nothing outside the 16 Design files and the run folder
changed in the repair. Verdict **MERGE AS DRAFTS** or **HOLD**; findings
classed as in V17.

# Wave B — design development

## Common rules for Wave B (in addition to the common rules above)

- **Binding:** R1–R11, [R12_RESOLUTIONS.md](R12_RESOLUTIONS.md), DECISION-K1
  and the executor-model direction in OWNER_DECISIONS.md.
- **Starting text:** the Design files as merged by PR-1 (Wave A). Read each
  file you edit whole before editing it.
- **What to produce:** R12-1 (data, states, sequences with failure behaviour,
  verification) for the items your node lists. Items are the survey section 8
  numbers; the survey gives the reasoning and locations. Check each against
  the current text first: Wave A may already have done part of it.
- **Prototypes (R12-3):** Python 3 standard library or `node` only; no
  package install; no network unless your brief grants it; files under the
  owning deliverable's `Design/prototype/`. Record the command, date and
  output in the return file.
- **Schemas (R12-1, R12-2):** JSON Schema 2020-12, beside the Design file,
  with a valid and an invalid example instance. Validate them with your
  prototype (a small standard-library validator for the subset you use is
  enough; say which subset).
- **Versions:** one step per file for Wave B (R12-1), with a "Changes from
  ‹Wave A version›" table carrying the item IDs.
- **Joins:** where your change alters what another file receives or
  supplies, say so in the return file (file, section, what the other side
  now needs). Do not edit files outside your fence; node V18 compares the
  joins.
- **Return file:** `WAVE_B/<ID>.md`: per item, what was produced and where;
  schemas and prototypes with their validation output; join changes;
  anything not done and why; proposed ScopeOfWork or register items; new
  sha256 per file.

## Round 1 (parallel; disjoint write fences)

| ID | Write fence (Design files, plus their `Design/` schema and prototype files) | Items |
|---|---|---|
| B1 | DEL-02-01: WD, WD-EX (`EXAMPLES.md`) | S1-C WD 5, 6, 7, 9, 10; WD-EX 2, 3, 4; R12-10 (SP-6F uptake element; message-output element). WD 6 (harness-capability names) uses HOSTING §8's inventory as it stands and the generated schema at `…/scratchpad/codex-0.158.0/gen` if present (read-only); names are PROPOSED and scoped to pin 0.158.0. Prototype: render and parse E1, E1d, E5, E6 in the chosen carriage |
| B2 | DEL-02-03: EXEC | S1-C EXEC 5, 6 (the reached-when table written against the native item kinds in HOSTING §8 and PIN-SPIKE; each cell that needs a live observation is marked "OBS-1 pending"), 7, 8, 9; R12-10 (recording is not a reaction; the current-phase case where an earlier act does not count) |
| B3 | DEL-03-01 C; DEL-03-02 P; DEL-03-03 ADAPTER | S1-B C 4, 5, 6, 8; P 4, 5, 7; ADAPTER 3 (per R12-4: both paths), 4, 5, 6, 8; R12-4's simulated host specified once in C (both paths), cited by P and ADAPTER; R12-9's read-without-workspace-identity proposal. ADAPTER 7 (live spike) is not in this node |
| B4 | DEL-04-01 ACT; DEL-04-02 AS; DEL-04-03 RS | S1-A ACT 7, 8; AS 4 (with RS), 5, 7, 8; RS 5, 6, 7, 8; R12-5 (A15 and its record kind); R12-9's two-evidence-limits proposal; R12-10 wording of "prior act not counted". The destination-grant exchange of AS 4 / RS 6 is designed here; B5 joins it to LOOP and PANEL |
| B6 | DEL-01-01 HOSTING (not PIN_SPIKE) | S1-D HOSTING 4 (harness-capability account by capability, with standing labels), 5, 6 (a supplier double seeded from the recorded spike transcripts under `…/scratchpad/codex-0.158.0/handshake` and the file's §10, run locally for the cases it marks runnable with a double), 7 (brief for the next observation, OBS-1, written to `WAVE_B/OBS-1_BRIEF.md`) |
| B9 | DEL-05-01 LOOP; DEL-05-02 PANEL (non-destination items) | S1-D LOOP 7, 8; R12-7; R12-8 (**network granted for this node only:** read the published Chat Completions reference and record URL, retrieval date and the four points); PANEL 5 except the destination prompt states (B5) |

## Round 2 (after round 1 is integrated)

| ID | Write fence | Items |
|---|---|---|
| B5 | LOOP, PANEL, AS, RS, ACT, C, P, ADAPTER — destination sections only, plus LOOP §4 for R12-11 | S1-D LOOP 5, PANEL 5 (destination prompt states), 7; S1-A AS 3, 7 as they touch destinations; R12-10 (refusal-recording labels; LP-5 label); R12-11 (model-interface boundary). **Network granted for this node only:** read the stateless MCP specification revision 2026-07-28 to state what evidences a stateless server (LOOP N-OPEN-5). One account of the destination flow that every file cites, with no element named on one side only |
| B7 | DEL-09-06 CA; DEL-09-09 XT | S1-E CA 5, 6, 9 (the option sheet, R12-6); XT 5, 7; R11-9 (cite B2's case in W14-05); CA and XT cite the simulated host of B3 |

## After round 2

- **OBS-1** (one live Codex turn at pin 0.158.0 against a local model, per
  K1-6): only after the owner approves the model download. Its record fills
  the "OBS-1 pending" cells (B2, ADAPTER 7).
- **V18** receiver comparisons, **R13** rulings, repairs, **B8** GUIDE
  (S1-E D.8 items 5–6 and the matrix for Wave B; re-pin last), **V19**
  review, **PR-2**.

## OBS-1 — the live Codex turn (one Type 2)

**Brief:** [WAVE_B/OBS-1_BRIEF.md](WAVE_B/OBS-1_BRIEF.md) (written by node
B6), with these integrator decisions under K1-6:

- Pre-flight P-5 (one direct request to the local server) is allowed: it is
  local and uses invented text.
- **Part C** (direct Chat Completions requests to the same local server, for
  LOOP's fixture basis) is allowed: local, invented content, no Codex turn.
- **Part D** (per-thread MCP configuration, no model call) is allowed.
- **Part B** (a second Codex turn on the command-line path): first held back, then **approved by the owner** during the run ("yes, run the second Codex turn on the command-line path"; OWNER_DECISIONS) and relayed to the executor. The two lines below are the original text:
  not run:
  K1-6 names one turn. It is put to the owner with OBS-1's result.
- **S-8 (no tool call):** stop and return. The executor does not download
  anything; HELP_HUMAN decides the next step under the owner's answer.
- Route R-1 only. If R-1 fails for a provider-form reason, stop and return
  before trying R-2 (R-2 can trigger a model download).

**Write fence:** the scratch folder `$TMPDIR/chirality-obs1-0.158.0`; one new
record `DEL-01-01/Design/OBS_1_0.158.0.md` (redacted as the brief's §12
says); the harness script under `DEL-01-01/Design/prototype/obs1/`; the
return file `WAVE_B/OBS-1.md`. The spike's scratch folder is read only. No
other repository file.

## OBS-1b — the command-line turn (one Type 2)

As OBS-1, with every hard limit unchanged, except: a fresh `app-server`
process and thread; the single turn is Part B of `WAVE_B/OBS-1_BRIEF.md` §11
(approval policy `untrusted`; the command-line test tool with `--key EX-1`
and the local probe socket); no MCP server configured; no Part C or D. Write
fence: the same scratch folder (a new `obs1b/` subfolder), an addendum
section appended to `DEL-01-01/Design/OBS_1_0.158.0.md`, harness changes
under `DEL-01-01/Design/prototype/obs1/`, and `WAVE_B/OBS-1b.md`.

## V18 — receiver comparisons for the joins Wave B changed (four Type 2, read-only)

**Purpose.** For each join in your cluster, compare what the supplier's
Design file now offers with what the consumer's Design file now uses, at
their Wave B text. Each executor writes one file, `comparisons/V18-<n>.md`.
Read-only on every project file. The join notes in `WAVE_B/B1.md`…`B9.md`
(section "join changes" of each) are the starting list; check each against
the files rather than trusting it, and look for joins they missed.

For each join record: supplier file, section and version; consumer file,
section and version; the register row (`Dependencies.csv`, ACTIVE) and
whether DAG-003 admits or holds the arc; what the consumer uses; the check
you performed (element by element; schema against schema where both have
one; run a prototype where it proves the point); **disagreements** (quote
both sides; say which side is wrong if a ruling, ScopeOfWork text or
accepted text decides it, else give options); **absent** (named on one side
only). Class each finding BLOCKING (the two files say incompatible things
about the same exchange), MAJOR (a consumer relies on something the supplier
does not offer), MINOR, NOTE.

| ID | Cluster |
|---|---|
| V18-1 | The record: RS ↔ EXEC (both checkpoint-entry schemas), RS ↔ ADAPTER (limits, observations), RS ↔ LOOP, PANEL, AS (destination elements; the AS §6 / RS §8 exchange), RS ↔ ACT (A15, policy reference), RS ↔ C, P (outcomes, evidence labels) |
| V18-2 | The workflow: WD ↔ EXEC, WD ↔ LOOP (message-output element), WD ↔ HOSTING (capability names against capability groups), WD ↔ C, P, ACT (identity strings, outcome tokens, A15), WD-EX ↔ everyone who cites an example |
| V18-3 | Host operations: C ↔ P ↔ ADAPTER ↔ EXEC (observations, CH cases, SH-1), ADAPTER ↔ HOSTING (native items, channel states), P ↔ LOOP, PANEL (derived proposal state, T-OPEN-1), C ↔ LOOP (catalog edition, external-contact entries) |
| V18-4 | The integrating files: CA, XT ↔ EXEC, C (SH-1 profiles), RS, P; and the four DAG-003 arcs added by SCA-V4-002 — N-18 (DEL-02-01 → DEL-03-02), N-21 (DEL-02-03 → DEL-03-02), N-24 (DEL-02-03 → DEL-03-03), X-1 (DEL-02-03 → DEL-01-04, narrow) — each with its register row |

Also apply, as a check: R13 (just written) says how two open disagreements
are ruled; report where the files do not yet say it, as a finding for the
repair.

## RP — repairs from V18 (four Type 2, parallel, disjoint fences)

**Binding:** [R14_RESOLUTIONS.md](R14_RESOLUTIONS.md), with R12, R13 and
DECISION-K1. **Inputs:** the four comparison files in `comparisons/` (every
finding that falls in your files, including MINOR ones; NOTEs optional),
`WAVE_B/OBS-1.md` and `WAVE_B/OBS-1b.md` with DEL-01-01's
`OBS_1_0.158.0.md` for R13-6.

| ID | Write fence (Design files with their schemas, examples and `prototype/`) | Main items |
|---|---|---|
| RP-1 | RS (DEL-04-03), EXEC (DEL-02-03), ADAPTER (DEL-03-03) | R14-1, R14-2, R14-3, R14-4, R14-8 (N-21, N-24, X-1); R13 and OBS observations in these files (R14-7) |
| RP-2 | C (DEL-03-01), P (DEL-03-02) | R14-7 in C; R14-8 N-18 (item-left events explicit in P's schema); P's outcome and citation findings; C's schema findings |
| RP-3 | WD and WD-EX (DEL-02-01), HOSTING (DEL-01-01; not PIN_SPIKE, not OBS_1) | R14-5, R14-6, R14-8 N-18 (WD cites P-v0.8); R13-6 in HOSTING |
| RP-4 | LOOP, PANEL (DEL-05-0x); AS, ACT (DEL-04-0x); CA (DEL-09-06, not RELAY or SWBPIPE's files); XT (DEL-09-09) | R14-7 in LOOP (R13-5, the observed column), CA, XT; LOOP §2.3 citing RS's mapping (R14-1); the comparisons' findings in these files |

**Rules.** No version bump: add rows with the R14 item or finding ID to each
file's Wave B change table. Where a fix needs another node's file, write
your side, and state in the return what the other side must say; the
integrator checks both sides after all four return. Rerun every prototype in
your folders and any cross-file prototype chain you touch (for RP-1, the
EXEC-to-RS conversion of R14-1 must show every entry valid). Return file
`WAVE_B/RP-<n>.md`: finding → fix → location; prototype output; anything
returned; new sha256 per file.

## RX — residual sweep after the repairs (one Type 2)

**Purpose.** Each of `WAVE_B/RP-1.md`…`RP-4.md` ends with what *other* files
must now say. The four ran in parallel, so some of those items were done by
another node and some were not. For every such item: check whether the named
file now says it; if not, make the smallest edit that does, under R14. Also
regenerate CA's `w14-result-record.example.valid.json` so that CA's check
"validates and equals the regenerated W14-05 record" passes after RP-1's
recorder change.

**Write fence:** the 16 Design files and their schemas, examples and
`prototype/` folders (not PIN_SPIKE, not OBS_1, not `prototype/obs1/`, not
RELAY or SWBPIPE's files); return file `WAVE_B/RX.md`. No version bump; rows
"RX" in each file's Wave B change table.

**Return:** a table of every residual item (source return, target file, said
already / fixed here / returned), the prototype reruns (every folder), and
sha256 per changed file.

## B8 — GUIDE for Wave B, final re-pin, and R15-1 (one Type 2)

**Write fence:** `HOST_INTEGRATION_GUIDE.md` (GUIDE v0.4 → v0.5); for R15-1
only, LOOP F-2 and MS-02 and RS's run-start or run-end cause element (text,
schema, one example); return file `WAVE_B/B8.md`.

**Do:** S1-E D.8 items 5–6 (refresh the receiving matrix for the Wave B
changes in the other 16 files, naming where N-18, N-21, N-24 and X-1 now
stand; a short "order of use" in §3 and what a reviewer does with *answered
without evidence*); cite the record arrangement of R14-1 (RS the container,
EXEC's entry bodies) wherever GUIDE describes the run record (R15-2); carry
R13 and R14 where GUIDE restates them; re-pin the 18-row input table **last**,
by script, after R15-1's edits, and show 18/18. Rerun LOOP's and RS's
prototypes after R15-1. No other file.

## V19 — independent review of the Wave B candidate (two Type 2 reviewers)

**Candidate:** the commit named in your launch message. Base: `292e123d`
(the merge of PR-1, Wave A). Read-only on project state; each reviewer writes
one file, `reviews/V19-A.md` or `reviews/V19-B.md`. You did not write any of
this; review it as a stranger to it.

| Reviewer | Files |
|---|---|
| V19-A | PKG-04 (ACT, AS, RS), PKG-03 (C, P, ADAPTER), GUIDE; with their schemas, examples and prototypes |
| V19-B | PKG-02 (WD, WD-EX, EXEC), PKG-05 (LOOP, PANEL), DEL-01-01 (HOSTING, OBS_1 and its harness), PKG-09 (CA, XT; RELAY untouched); with their schemas, examples and prototypes; and the run records (graph, OWNER_DECISIONS, DISPATCH, R12–R15, BRIEFS) |

**Check, and do not take on trust:**

1. **Fidelity to decisions.** Nothing claims more than the owner decided or
   an accepted text says. Check DECISION-K1, the host-loop interface
   direction, the download and OBS decisions, and R12–R15 against what the
   files now state. Every new structure that no ruling or accepted text
   decides is labelled PROPOSED.
2. **The 60% content** (R12-1): for the items each file's change table
   claims, the data (schemas with examples), states, sequences with failure
   behaviour and verification are actually there and coherent.
3. **Cross-file consistency** on the joins V18 found and R14 ruled: one
   record container (R14-1); request identification (R14-2); vocabularies
   (R14-3); observations (R14-4); capability groups (R14-5); `applied`
   (R14-6); R13 applied (R14-7); the four arcs (R14-8); the destination flow
   (LOOP §5.3) cited the same way everywhere.
4. **Prototypes:** rerun every prototype in your folders (READMEs give the
   commands; the SH-1 chain and `exec_to_rs.py` cross folders), and check
   that each schema accepts its valid example and rejects its invalid one.
   Report any whose claimed result you cannot reproduce.
5. **Observations** (V19-B): OBS_1_0.158.0.md states only what was observed,
   with versions and redaction (no host name, installation identifier, home
   path or user name); the files that cite it treat it as a dated
   observation, not qualification.
6. **Untouched:** RELAY §0–§3 byte-identical to `74b3c73134`; PIN_SPIKE,
   SWBPIPE's two files, every ScopeOfWork, register, status, basis,
   decomposition, scope-change and DAG file byte-identical to `292e123d`;
   DAG-003's two manifests pass.
7. **Records** (V19-B): the graph, DISPATCH and OWNER_DECISIONS are true
   against git and the owner's recorded words.

**Return file:** verdict **MERGE AS DRAFTS** or **HOLD**; findings classed
BLOCKING (false, inconsistent across files, or claims more than decided),
MAJOR, MINOR, NOTE, with passages quoted and a proposed fix; what you checked,
how, and what you did not check.

## RQ — repairs from V19 and final GUIDE re-pin (one Type 2)

**Inputs:** `reviews/V19-A.md` and `reviews/V19-B.md`: every finding in the
Design files, all classes (NOTEs optional). The graph finding (V19-B M-1) is
the integrator's and is done. Rulings for the findings:

- **V19-B B-1 and GUIDE F-18:** R15-1 applies to PANEL as to LOOP: PC-42,
  RI-1 and RT-d, and LOOP's §3.2 turn-table row, read "run not started — no
  model selected" for an unconfigured model; "boundary refusal" stays only for
  a cloud model with no credential.
- **V19-A M-1:** the ADAPTER-to-RS label map gets an entry for every token
  that the underscore rule does not produce (at least
  `agent_written_configuration` → "agent-written configuration"), and a
  prototype check runs every ADAPTER evidence-limit and outcome value through
  the chain.
- **V19-A, `namespace`:** where ADAPTER and GUIDE state the mechanism as
  observed, say what was observed (LM Studio logged the `namespace` tool type
  as unsupported; the model never saw the tool) and label the mechanism an
  inference, as the OBS record does.
- **V19-A, RS `$ref` resolution:** state accurately how a standard validator
  resolves RS's references (give the schemas `$id`s that make relative
  references resolve, or say that a loader must map them), and check it with
  the already-installed `jsonschema` package if present (no install).

**Write fence:** the 16 Design files and their schemas, examples and
`prototype/` folders (not PIN_SPIKE, OBS_1, `prototype/obs1/`, RELAY or
SWBPIPE's files); `WAVE_B/RQ.md`. Rows "RQ" in each file's Wave B change
table; no version bump. **GUIDE's 18-row input table is re-pinned last**, by
script, after every other edit, showing 18/18. Rerun every prototype.

## V19b — recheck of the V19 repairs (one Type 2 reviewer)

**Candidate:** the commit named in your launch message; the repairs are the
diff from `8c575f739e` to it. Read-only; write only `reviews/V19b.md`. Check
that every V19-A and V19-B finding is closed as `WAVE_B/RQ.md` says (quote the
fixed passage), with the RQ brief's rulings; that the RQ diff introduced
nothing false, inconsistent across files, or beyond the findings (look hard
at anything new it labels PROPOSED); rerun every prototype; GUIDE 18/18; RELAY
§0–§3, PIN_SPIKE, OBS_1, SWBPIPE's files and every ScopeOfWork, register,
status, basis, decomposition, scope-change and DAG file unchanged; DAG-003's
manifests pass; and that the work graph and DISPATCH are true against git.
Verdict **MERGE AS DRAFTS** or **HOLD**; findings classed as in V19.

# Closeout

## C0 — the four V19b MINORs and the last GUIDE re-pin (one Type 2)

Fix V19b m-1…m-4 (`reviews/V19b.md`): LOOP §3.2's run opening against a
no-credential refusal (state when a host-loop run opens so that a
`boundary_refusal` is recorded on an opened run, consistent with R15-1);
GUIDE's pin-provenance text; GUIDE F-17's wording; HOSTING §6.8 "not
exercised live" against OBS-1 (§10.1). Write fence: LOOP, GUIDE, HOSTING
(and LOOP's or RS's schema/example only if m-1 needs it); `closeout/C0.md`.
Rerun LOOP's and RS's prototypes; re-pin GUIDE's 18-row table last, 18/18.

## C1 — bounded closeout (three Type 2, read-only on Design files)

Method: `chirality-root:bundled:workflow:bounded-reconciliation`
(`workflows/bounded-reconciliation/WORKFLOW.md`, read it whole). Same
boundary as the first increment's closeout: DAG-003's `SOURCE_MANIFEST`
binds every `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`, so
this closeout **applies no change** to them, or to `_STATUS.md`,
`_CONTEXT.md` or `_REFERENCES.md`; every warranted change is a precise
proposal (file, section or row, old → new, reason, source finding) for a
later amendment and `dependency-extract` run.

| ID | Deliverables (Design files compared at the candidate named at launch) |
|---|---|
| C1-A | DEL-04-01, DEL-04-02, DEL-04-03, DEL-02-01, DEL-02-03 |
| C1-B | DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-01-01 |
| C1-C | DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09 |

For each deliverable: commitments (ScopeOfWork OUT, REQ, AC, VER) → where the
Design files now answer them (developed, partial, named only, absent), and
results in the Design files → whether a commitment supports them; what the
60% description in `loop/LOOP_INIT.md` still lacks; the register rows the
Design files now show to be wrong, missing or stale; lifecycle observation
(no change made). **Collect every proposed ScopeOfWork, register or basis
item** raised in this run — the "proposed" parts of `WAVE_A/*.md`,
`WAVE_B/*.md`, `comparisons/*.md`, `reviews/*.md` and the S1 surveys — that
falls in your deliverables, deduplicated, each with its source; include, at
least, the DEL-01-04 act-control obligation (DECISION-K1 K1-4), whether
DEL-05-02's contract names the panel's destination surfaces, DEL-04-01's
contract and DECISION-5, and DEL-09-09 REQ-001's TBD range. Write
`closeout/C1-A.md` (or B, C). No other file.

## G — items the closeout returned to the graph (one Type 2)

Apply [R16_RESOLUTIONS.md](R16_RESOLUTIONS.md) R16-1…R16-3 (every item but
the pair check). Inputs: `closeout/C1-A.md` (G-1…G-3), `C1-B.md` (its two
graph items), `C1-C.md` (GW-1…GW-3). Write fence: the Design files and their
schemas, examples and prototypes as the items need; RELAY metadata only
(§0–§3 byte-identical); `DEL-01-01/Design/OBS_1_0.158.0.md` for the redaction
only; `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` for IN-30 only;
`closeout/G.md`. Rows "G" in each changed file's Wave B change table. Rerun
every prototype you touch; GUIDE's input table re-pinned last, 18/18.

## H — LOOP's four panel-needs gaps and current pins (one Type 2)

Close LOOP's PG-1…PG-4 (`closeout/G.md`; LOOP §10.5): add the two §2.3
rows E-8 names; an event for "run not started — no model selected" (R15-1;
mapped to RS's cause); LOOP's answer to a panel return input; the form and
answer of the replay request — each PROPOSED unless a ruling decides it, and
PANEL's §3.11 rows updated to "supplied". Then bring every header pin that
claims current bytes up to date for files changed by G (OBS_1 after its
redaction, HANDOFF after IN-30), in HOSTING, GUIDE, LOOP, RELAY (metadata
only, §0–§3 unchanged) and CA. Write fence: LOOP, PANEL, HOSTING, GUIDE,
RELAY metadata, CA, and RS only if the event mapping needs a row;
`closeout/H.md`. Rows "H" in change tables. Rerun LOOP, PANEL, RS and CA
prototypes; GUIDE's input table re-pinned last, 18/18.
