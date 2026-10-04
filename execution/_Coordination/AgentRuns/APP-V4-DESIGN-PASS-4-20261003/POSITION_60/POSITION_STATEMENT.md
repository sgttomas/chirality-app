# App v4: where the design stands against 60%

**This is a position statement for the owner. Nothing in it is decided.**
It was prepared by HELP_HUMAN at the close of design pass 4 tranche 2, from
the cited [evidence inventory](INVENTORY.md) and the run records. Gap IDs
(G-nn) refer to that inventory's Part C.

The 60% gate (`loop/LOOP_INIT.md`) is passed when the owner judges there is
"developed design/interfaces and a route to completion for which further
structural changes are no longer anticipated". Closing this tranche or
merging its PR does not pass that gate.

## The short answer

**Not yet.** The App's own design is close. Every one of the 41 deliverables
has Design files and is IN_PROGRESS. Every pass-4 unit was reviewed to READY
with no open finding; the last mechanical rounds are covered by the pre-merge
review.

What stands between here and 60% is three things:

1. **Further design-agent work.** About a dozen gaps can be closed by the
   design agents in one more bounded pass, with no decision from you.
2. **A short set of your own decisions.** Several are already marked for
   "the owner's phase review".
3. **The SWBPIPE host side.** You deferred the host joins (DECISION-3).
   While they stay deferred, the App ↔ host interfaces are designed from the
   App side only. The changes a host answer could force are named and
   bounded, but not ruled out.

How to treat point 3 at the gate is the main choice for you; see the last
section.

## What is established

- **Design coverage.** All 41 deliverables have developed Design files.
  Pass 4 designed the last 21: 8 in tranche 1, then 13 in tranche 2 covering PEC, connectors,
  Domains, project definition, adoption and replacement continuity, and
  practitioner validation.
- **Interfaces inside the App.** These were checked against the other side's
  actual Design text where the inventory cites it. Pass 4 added the shared
  rows: the A16 "decide" act across ACT, RS, AAC, DEL-02-03 and GUIDE, and
  the connector standing vocabulary across PKG-06, -07, -08 and DEL-09-10.
  It then took one connected path end to end and had it read cold:
  - a decision package decided by the person;
  - the connector standing;
  - the execution basis;
  - the replacement packet.
- **Graph and scope.** DAG-004 is current: 128 of 130 sources match, and the
  2 are recorded DEL-01-03 drift. No ScopeOfWork, register, DAG or
  Open_Issues file changed in pass 4.
- **Your earlier decisions are carried, not reopened.** The AGENTS.md change
  you approved (D-GOV-52) is adopted by App v4. For App v3 and Runtime it is
  recorded as delivered, with no receiving decision yet (DEL-11-02).

## Reliance limits

- **Nothing is built, signed or qualified.** All product evidence is fixture
  or prototype; no App candidate exists (G-30). Supplier observations cover
  one Codex pin on one local model.
- **Prototype checkers mostly compare text.** Their unenforced rules are
  listed in each Design file and pass to implementation.
- **Review independence is limited.** Every pass-4 review was Claude
  reviewing Claude, in the same session, which you accepted as a practical
  concession. Read and write isolation was not observed to be enforced by
  the host (G-31).

## What remains, by who closes it

### A. Design agents, with no decision from you (one bounded pass)

| Gap | Work |
|---|---|
| G-10 | Carry pass-4 rulings into HOSTING, ACCESS, WR, RECOVERY and NPTD: App-origin reads (R23-50/53); a thread with no turn has no items (R23-37.2); R23-30.1/2 |
| G-11 | Update GUIDE M10 for the tranche-2 suppliers (PRC, CFB, DRC, RTD) |
| G-12 | RP and EXP adopt PV's practitioner shapes (U-PV-3, U-PV-4) |
| G-13 | Consumers of WD §9 confirm or object |
| G-14 | One receiver comparison over current versions, limited to joins changed since V18/F0 |
| G-16 | FX-PIPE-01 adopts L-LHQ-1/2 |
| G-17 | DEL-09-05 designs the rest of its VER items (two delegations, graph, queue, recovery witness) |
| G-18, G-19 | DEL-08-01 §6–§8 with a VER map; DEL-09-10's dossier |
| G-20 | DEL-10-01 runs VER-004, 005, 007 and 008. Its own file says this comes before the 60% review |
| G-22 | DEL-02-01's declared chaining |
| G-25 | A record mapping each role-named owner ("integrator", "shared contract owner", …) to you or to an agent, for you to confirm |
| G-29 | SCA-V4-003's derivative closure, plus CASE-002's drafted DAG-004 evidence update (R23-55.3) |

### B. Decisions reserved to you

These would come to you as one prepared package with a recommendation for
each, after A. None is asked now.

| Gap | Decision | Already pointed at you by |
|---|---|---|
| G-21 | Practice notes PN-1/2/3/5/6 | DEL-10-02, "at the 60% stage discussion" |
| G-26 | The items marked "owner's phase review": consequence vocabulary (CV), process division (PD), PANEL F-12, U-A2 | ACT §8.5; P2 and P3 receipts |
| G-01 | Whether to confirm the A12 mapping, which releases the held Q-9 rows | SCA-V4-003 Q-9 ("hold unless you confirm the mapping") |
| G-02 | Accept a DAG-005 for the three bundle-seam arcs into DEL-01-06, or decide no rows. They form no cycle (checked) | DA §5; SPEC §5.4 (successor acceptance is yours) |
| G-03 | How each of the six SCC cases is treated. Each recommends R1 | scc-resolution-case |
| G-04, G-08 | Placement (OI-013, OI-014) and the first connected operation (OI-021). Both are shared with the SWB side | Open_Issues |

R23-54 also settles G-24. Under L-7 the "App implementation owner" is you;
genuine choices labelled that way come to you, and items already settled by
the basis are recorded and shown to you.

### C. Outside parties

- **SWBPIPE host joins** (G-07, G-05, G-01's Q-7). These are deferred by
  your DECISION-3. The structural changes they could still bring are named:
  - DEL-03-01's AC-004, if a host supplies no workspace identity (Q-7);
  - placement (OI-013/014);
  - the first connected operation (OI-021);
  - durable host receipts for later reconstruction (G-05).
- **PEC and Domains** (G-09, G-06). PEC needs its owner's agreement;
  Domains has no provider yet (OI-026). Both are optional or later, as at
  30%.
- **Codex supplier observations not yet made** (G-30): sign-in, API key,
  stock-route delegation. You chose "not now" for sign-in and API key (L-6).

## The choice in front of you

How should the host side count at 60%?

- **(Recommended) Assess 60% with the host side as a stated qualification,
  as 30% did with external scope.** First, run A as one bounded design pass
  (pass 5). Then I bring you B as one package. You then judge 60% knowing
  exactly which host answers could still change structure, and where.
- **Or resume the host joins first.** Lift DECISION-3's deferral for the
  joins that bear on structure (Q-7, OI-013/014, OI-021, receipts), and
  assess 60% after them. This retires the conditional structural risk, but
  depends on the outside SWB session's timing.

Neither route needs anything from you before pass 5 starts, apart from
choosing to start it.
