# Work graph — App v4 first increment: second design pass

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, applied
under [`loop/LOOP_INIT.md`](../../../../loop/LOOP_INIT.md).

- **Stable run identity:** `APP-V4-DESIGN-PASS-2-20260930`. Run records:
  [`AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/).
- **Maintainer:** HELP_HUMAN, this session, under the recorded
  WORKING_ITEMS consultation (as in the three predecessor runs), dispatching
  bounded Type 2 TASK executors directly.
- **Branch:** `claude/chirality-app-v4-60-percent-a41fd5`, at `main`
  `74b3c73134` when the run started.
- **Predecessor:** `APP-V4-SCA002-20260929`, merged in
  [#1061](https://github.com/sgttomas/chirality/pull/1061) at `45ffd91d`.
- **Owner direction (exact):** "Start the next first-increment design pass
  using DAG-003." See [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md)
  for the reading and the standing directions that apply.

## Intent and route

- **Result:** the 14 first-increment deliverables' Design files stand on the
  amended basis and the revised ScopeOfWork contracts, and are developed
  further toward the 60% level (interfaces, states, data, operating
  sequences, failure behaviour, verification). They stay DRAFT, unsupplied and
  unaccepted.
- **Graph basis:** accepted DAG-003 (`_DAG/_LATEST.md`), CURRENT per
  `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218`. Both DAG-003 manifests
  pass at the start of the run (37/37 and 130/130). The 78 held arcs are
  non-gating; they organize co-development and receiver comparisons.
- **Route through DAG-003:** as in the first pass: roots DEL-04-01 and
  DEL-01-01; the SCC-002 members DEL-03-01/02/03, DEL-02-01/03, DEL-04-02/03
  and DEL-05-01/02 co-developed; then DEL-09-09, DEL-09-06 and DEL-03-04 as
  integrating consumers (GUIDE re-pinned last).
- **Not written in this run:** ScopeOfWork.md, registers, `_STATUS.md`,
  `_Decomposition/`, `_ScopeChange/`, `_DAG/` and the basis docs. A finding
  that needs one of them is returned as a proposal for its own route.
- **Excluded:** SWBPIPE construction, host joins (deferred, DECISION-3), the
  relay; the Coverage_Telemetry rebuild; the audit-script fix; product
  implementation beyond a bounded spike that answers a design question;
  qualification, lifecycle CHECKING/ISSUED, SCC closure, a DAG successor.
- **Completion conditions:**
  1. Every Design file is re-pinned to current sources, GUIDE last, with the
     pins verified by script.
  2. Each node below has produced its stated result, reviewed against the
     revised ScopeOfWork.
  3. Receiver comparisons recorded for the joins the pass changes, including
     N-18, N-21, N-24 and X-1.
  4. Owner-level choices found are decided or left open at a stated point of
     need.
  5. DAG-003 currency rechecked at the end; no bound file changed.
  6. Independent review, bounded closeout, receipt, MEMORY rows and the final
     PR merged.

## Work

States: PLANNED, READY, ACTIVE, BLOCKED, UNCERTAIN, COMPLETE.

| ID / outcome | Write scope | Needs | Completion check | State |
|---|---|---|---|---|
| S0 Graph, direction, survey briefs | Run folder; this graph | Owner direction | Committed | COMPLETE |
| S1 Scoping survey (S1-A…S1-F) | `SURVEY/S1-*.md` only | S0 | Six reports: pins, SoW alignment, amended basis, open items by class, 60% depth, joins, carried review items, recommended work; outside neighbours | COMPLETE — [SURVEY/](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/SURVEY/): 184 stale pins across 16 files; open items classed; fence verified (`fbebb12a5`) |
| S2 Route: nodes for the pass, owner questions | This graph; `BRIEFS.md`; `R9_RESOLUTIONS.md` | S1 | Each node bounded with a write fence and a check | COMPLETE for Wave A; Wave B nodes are named below and briefed after Wave A integrates |
| **Wave A — alignment** | | | | |
| A1-A…A1-E Re-pin, amended-basis wording, revised-SoW alignment, records-closed items, receivers | The 15 Design files by cluster (ACT, AS, RS / C, P, ADAPTER / WD, WD-EX, EXEC / LOOP, PANEL, HOSTING / CA, RELAY metadata, XT); `WAVE_A/<ID>.md` | S2; [R9](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R9_RESOLUTIONS.md) | Each file one version step (R9-11); no leftover stale wording; RELAY §0–§3 byte-identical; PIN_SPIKE untouched | COMPLETE `344d86e3e` — fences verified; RELAY span `6e399c83…` unchanged; DAG-003 source manifest 130/130; 11 disagreements returned → [R10](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/R10_RESOLUTIONS.md) (R10-1 corrects R9-2) |
| A1-G GUIDE alignment and re-pin | GUIDE; `WAVE_A/A1-G.md` | A3 | 18/18 pins by script; CC-1…CC-11 rerun against the revised SoW | COMPLETE `871232216` — GUIDE v0.4; 18/18; CC-1…CC-11 rerun; no new R10 candidates. DAG-003 manifests 37/37 and 130/130; no file outside the Design files, this run and HANDOFF changed since `74b3c73134` |
| A2 Apply R10; sibling-citation pass over the 15 files; HANDOFF truth fixes | 15 Design files; `WAVE_A/A2.md`; `HANDOFF_SWBPIPE_DOMAINS.md` (integrator) | A1 | R10 applied; every cross-file citation checked; RELAY span unchanged | COMPLETE `42456ca08` — 12 files; 3 citation fixes; 1 dangling citation passed to A3; HANDOFF `dda9380d1` |
| A3 Apply DECISION-K1 in the files | 15 Design files; `WAVE_A/A3.md` | A2; K1 | Every carrier updated; expected case results recomputed | COMPLETE `ce4088219` — 13 files; 37 case results recomputed; new rules SP-6 (current phase) with SP-6F kept for the governance phase, JA-1 joint answer; N-OPEN-4 closed. Carried to Wave B: a declaration element for taking up SP-6F (B1) |
| V17 Independent review of Wave A (V17-A, V17-B) | `reviews/V17-*.md` | A1-G | Verdict covering the candidate | ACTIVE |
| P1 PR-1: Wave A | — | V17, CI | Merged under the standing direction | PLANNED |
| **Owner package** | | | | |
| K0 Decision package draft | `DECISIONS_DRAFT.md` | S1 | Every owner-class choice from the surveys stated with options and consequences | COMPLETE `be55f3250` — 27 choices in three groups |
| K1 Owner checkpoint: the choices that shape the design now, with recommendations | `DECISIONS_PENDING.md`; `OWNER_DECISIONS.md` | K0 | Decided, or left open at a stated point of need | COMPLETE — [DECISION-K1](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md): all six accepted as recommended |
| **Wave B — design development** (briefed after Wave A; content from the surveys' section 8 and K1) | | | | |
| B1 Declared-part carriage and schema, with a local parse/render prototype; harness-capability names | WD, WD-EX; HOSTING (capability account) | P1; K1 where it bears | Schema PROPOSED; E1, E1d, E5, E6 render and parse | PLANNED |
| B2 Current-phase recorder, App-run reached-when table, end-to-end sequences | EXEC (with LOOP §2.4.1 and ADAPTER §7.7) | P1; R9-1 confirmed or changed at K1 | One transition table and event list for the current phase; sequences for an App run and an App → host transfer | PLANNED |
| B3 Catalog interface and read-result model; proposal identity, observation and per-item transitions; one shared test double | C, P, ADAPTER, XT | P1 | Interface meanings stated; the double specified once and cited by the four files | PLANNED |
| B4 Record format and writer/reader sequences; policy-class record and act lifecycle; standing components and receiver conditions; consequence vocabulary draft | RS, ACT, AS | P1; K1 where it bears | PROPOSED structures; failure behaviour per sequence | PLANNED |
| B5 Network destinations end to end: tool subject, check position, request states, records and displays | LOOP, PANEL, AS, RS, ACT, C, P, ADAPTER | B3, B4 drafts | One account each file cites; no element named on one side only | PLANNED |
| B6 Hosting operations and lifecycle tables; supplier double from the recorded spike transcripts; next-spike brief | HOSTING; a spike record | P1 | Runnable-with-a-double cases exercised locally, or the reason they were not | PLANNED |
| B7 Connected activity: per-step failure behaviour, result record, current-phase sequence; trace suite order and reset; optional OI-021 option sheet | CA, XT | B2, B3 | Per CA/XT survey items | PLANNED |
| V18 Receiver comparisons for the joins Wave B changes (incl. N-18, N-21, N-24, X-1) | `comparisons/` | B1…B7 | Per join: version received, check, disagreements, absent | PLANNED |
| R… Repair rounds and rulings | Design files | V18 | Findings dispositioned | PLANNED |
| B8 GUIDE matrix refresh and final re-pin | GUIDE | R… | 18/18 pins by script | PLANNED |
| V19 Independent review of the Wave B candidate | `reviews/` | B8 | Verdict covering the candidate | PLANNED |
| P2 PR-2: Wave B | — | V19, CI | Merged | PLANNED |
| **Closeout** | | | | |
| D0 DAG-003 currency recheck | Read-only | P2 | Both manifests pass; no bound file changed | PLANNED |
| C1 Bounded closeout (`bounded-reconciliation`): commitment ↔ result per deliverable; proposed SoW, register and basis items for a later amendment | `closeout/` | P2 | Account written; proposals not applied | PLANNED |
| F Receipt, MEMORY rows, final PR and its review | `RECEIPT.md`; 14 `MEMORY.md` | C1 | Final PR merged | PLANNED |

## Holds and owner-held choices

- No hold on Wave A or Wave B from owner choices: DECISION-K1 decided all six.
- **Download gate (K1-6):** before any chat model is downloaded into LM
  Studio, HELP_HUMAN names the model, its source and its size to the owner
  and waits for a yes. The Codex sign-in is asked for only if the local route
  cannot produce a tool call.
- The read-only fetch of the two published specifications is allowed (K1-6).

## Next safe action

When V17 returns: repair any blocking finding and recheck it, then open PR-1 with the CI monitor on, and enable auto-merge once nothing blocking remains.
