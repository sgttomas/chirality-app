# Work graph — App v4 design pass 4 (remaining deliverables), tranche 1

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, under
`loop/LOOP_INIT.md`. Coordination: `bundled:chirality-root/coordinated-knowledge-work`
(owner's selection; see "Coordination" below).

- **Run:** `APP-V4-DESIGN-PASS-4-20261003`; records in
  [`AgentRuns/APP-V4-DESIGN-PASS-4-20261003/`](../../AgentRuns/APP-V4-DESIGN-PASS-4-20261003/).
- **Maintainer:** HELP_HUMAN under the recorded WORKING_ITEMS consultation.
- **Owner direction (exact):** "1 yes, 2 no rewrite, 3 go, 4 A+C"; then the
  coordination-method direction in OWNER_DECISIONS.md.
- **Graph basis:** DAG-004.
- **Tranche 1:** DEL-06-01, DEL-06-02, DEL-01-06, DEL-09-01, DEL-09-02,
  DEL-09-05, DEL-09-07, DEL-09-11. Tranche 2 (PKG-07, PKG-08, PKG-10,
  PKG-11, DEL-09-10, DEL-09-12) follows.

## Coordination

**Consumer and usable result.** The consumer is the owner assessing the 60%
position (LOOP_INIT: developed design and interfaces, and a route to
completion with no further structural change anticipated), and after that
the implementer. A deliverable's result is usable when its Design files let
an implementer build without reopening structure: each interface is checked
against the supplier's or receiver's actual Design text, and its open
matters are named with who decides them.

**Early path before multiplying work.** The three surveys found one shared
premise that could invalidate several designs: no act or record kind exists
for a person's decision on a decision package (S1-A S-1/S-2, S1-C S-1, S1-B
SQ-5). It touches DEL-06-01, 06-02, 09-05, 09-11 and the first-increment ACT,
RS and pass-3 AAC files. The first unit taken all the way through is
therefore **one decision package decided by the person**:
package record (DEL-06-01) → decision view (DEL-06-02) → act through the
App act control (DEL-01-04 AAC) → act record (DEL-04-03 RS, schema-valid) →
the DEL-09-05 VER-004 case → reconstruction by DEL-09-11's reader from the
files alone. Its consumption check is a bounded connected prototype
(LOOP_INIT: "bounded implementation and connected tests when they can
resolve a design question"): a fixture package, the act record validated
against `RS_RECORD.schema.json`, and an isolated reader given only the
input-set manifest. Its premises are ruled in R23-8…R23-10. Work that depends on
that premise does not expand until the path works; independent branches
continue.

**Owners (standing, Type 2, `type2-opus-high`).** Each survey agent keeps
its deliverables through design, findings, repair and integration, so its
context carries over:

| Owner | Agent | Deliverables | Starts now on |
|---|---|---|---|
| O-A | S1-A's | DEL-06-01, 06-02 | The early path (R23-8, R23-9), including the A16 and package rows in ACT, RS and AAC |
| O-B | S1-B's | DEL-01-06, 09-01, 09-02 | DEL-09-01 (R23-1, R23-3; SCC-003 R1 milestones), then DEL-01-06 (R23-13) |
| O-C | S1-C's | DEL-09-05, 09-07, 09-11 | DEL-09-07's designable-now set (S1-C B4), then 09-05's VER-004 case and 09-11's reader on the early path (R23-10) |

Ordinary design decisions are the owner's. An owner stops the affected part
and escalates when a change would restructure a first-increment or pass-3
Design file, add a register row (after running the reach script, R23-2),
touch an owner-reserved item, or remove, narrow or bypass an existing check.
The host needs HELP_HUMAN to start each turn (SendMessage); a standing
assignment does not run by itself.

**Review.** One standing independent reviewer (RV, fresh `type2-opus-high`)
is started when the first unit freezes. Each owner has at most one frozen
unit waiting for review and continues the next unit meanwhile. The reviewer
who raises a finding confirms its repair; a fresh reviewer only for a named
competence, independence or assumption problem. Cheap checks run where
defects enter: JSON Schema validation when a schema or record is written,
the reach script when a row is proposed, hash checks when a pin is written.
Before a merge, the independent review the merge policy requires covers the
actual candidate and checks only what the unit reviews did not establish
(placement, references, pins, cross-owner interfaces).

**Shared rulings.** Cross-owner findings come to HELP_HUMAN for one recorded
ruling (R23 onward); adoption is checked in the returned files, not assumed
from the message.

**Agent 1.** HELP_HUMAN coordinates directly. A WORKING_ITEMS instance is
introduced if integration work starts delaying owner-facing work.

**Reporting.** Usable results and material gaps, not agent rosters.

## Nodes

| ID / outcome | Write scope | Needs | Check | State |
|---|---|---|---|---|
| S0 Direction, graph, briefs | Run folder; this graph | Owner direction | Committed | COMPLETE |
| S1 Scoping surveys (A, B, C) | `SURVEY/S1-*.md` | S0 | Obligations, joins, owner choices, design scope | COMPLETE |
| R23 Rulings on the surveys | `R23_RESOLUTIONS.md` | S1 | — | COMPLETE |
| VC Codex version-advance check to 0.160.0 | Scratch; a DEL-01-01 drift record | Owner's yes (given) | Types regenerated and compared; OBS harnesses rerun; affected statements listed | COMPLETE (R23-22) |
| K Questions for tranche 1 | `DECISIONS_PENDING.md`; R23-8…R23-14 | S1 | Owner returned them; ruled | COMPLETE |
| E Early path: one decision package decided | Owners' Design folders; ACT §2.1, RS §6.1/§13.6 and schema, AAC §1.2 (rows only, O-A); prototype under the run folder | R23-8…R23-10 | Schema-valid act record; isolated reader reconstructs the decision | COMPLETE (RR-E, RR-F) |
| O-B1 DEL-09-01 design | DEL-09-01 `Design/` | R23 | RV review | COMPLETE |
| O-C1 DEL-09-07 design (designable-now set) | DEL-09-07 `Design/` | R23 | RV review | COMPLETE |
| D Remaining tranche-1 design, review, closeout | Per LOOP_INIT | E | RV, RV2; C1, C2; P1 MERGE | COMPLETE (PR) |
| T2 Tranche 2 (PKG-07, PKG-08, PKG-10, PKG-11, DEL-09-10, DEL-09-12) | Per LOOP_INIT | Tranche 1 merged | — | PLANNED |
