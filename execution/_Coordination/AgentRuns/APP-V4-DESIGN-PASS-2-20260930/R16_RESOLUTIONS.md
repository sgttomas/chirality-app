# R16 rulings — items the closeout returned to the graph

Integrator: HELP_HUMAN. Inputs: `closeout/C1-A.md`, `C1-B.md`, `C1-C.md`.
R1–R15 stand except R12-10's first bullet, corrected by R16-1.

## R16-1 Recording a declined destination request is required — SETTLED by DEL-04-03 CLM-004 (correcting R12-10)

R12-10 said that no accepted text requires recording a declined or refused
destination request, and Wave B labelled that recording PROPOSED everywhere.
That was wrong for the declined case. DEL-04-03's ScopeOfWork, as revised by
SCA-V4-001 (CLM-004), names "a host agent's network-destination events
(destination contacted, destination grant, destination declined) from
DEL-05-01" among the events the record format carries. So:

- **Destination declined** (the person declines an in-work request):
  recorded, SETTLED by DEL-04-03 CLM-004, in RS, AS, ACT, LOOP, PANEL and
  GUIDE.
- **A refusal the loop makes without asking the person** (a destination
  neither allowed nor requested, or a boundary refusal): no accepted text
  names it; it stays PROPOSED.
- The report to the agent ("destination not allowed by the person",
  V4-EXM-23) is unchanged.

## R16-2 The panel-needs list (C1-C GW-1) — required production

DEP-05-01-020 (ACTIVE) has LOOP consume DEL-05-02's statement of what the
panel needs the loop to emit. PANEL writes it (events and elements, with the
LOOP section that supplies each), and LOOP confirms or names each gap. This is
missing required work, done in node G, not a proposal.

## R16-3 The other returned items

- **IN-30** (the host's fixture reset; C1-C GW-2): added to RELAY's
  next-relay UNRESOLVED row (metadata only; §0–§3 unchanged) and to the
  handoff note's unrelayed list.
- **GUIDE review status** (C1-B 1): GUIDE records V19-A and V19b as its
  reviews.
- **OBS record redaction** (C1-B 2): the rollout filename that shows the time
  zone is redacted, with a change note in the record.
- **EXEC EV-3** (C1-A G-2): where HOSTING §8.4 already states a group's
  availability signal, EXEC's presence rule cites it and becomes active for
  that group; any group without one stays inactive with that reason.
- **Bookkeeping** (C1-A G-3; C1-C GW-3): applied as listed.
- **The LOOP/PANEL pair check** (C1-C GW-4): V18 compared each with P, not
  with each other. It is done in the final review (V20), after node G.
