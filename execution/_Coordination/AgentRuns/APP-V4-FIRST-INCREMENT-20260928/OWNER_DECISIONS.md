# Owner decisions — APP-V4-FIRST-INCREMENT-20260928

Decision ID: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`. Owner: Ryan. Recorder:
HELP_HUMAN (Claude Code session). Custody: the owner's answers to a structured
question in the active Claude Code chat, transcribed by the recorder on
2026-09-28. This is not a raw platform export and carries no platform timestamp.
The package presented was [DECISIONS_PENDING.md](DECISIONS_PENDING.md) as
committed in `8d3c66542`, together with the question texts below.

| Question presented | Owner's selected answer (exact label) |
|---|---|
| Which scope should this first 60% undertaking take? (Wave 1 is already running and is common to all options.) | "A: App/host spine (Recommended)" |
| OI-001: which human acts are always reserved to the person for the first increment? | "Five reserved acts (Recommended)" |
| OI-002: how should classifier-based routine permission modes be treated? | "App user setting; none in hosts (Recommended)" |
| OI-012: select a Codex App Server version pin now and run the protocol-generation spike? | "Pin 0.158.0 + spike (Recommended)" |

## Effects, stated at the scope decided

- **D1 scope.** This undertaking covers DEL-04-01, 04-02, 04-03, 03-01, 03-02,
  03-03, 03-04, 02-01, 02-03, 05-01, 05-02, 01-01 (boundary and pin), 09-06
  and 09-09. The standalone-App definitions (DEL-01-02…05, 02-02, 02-04) are
  left for a later undertaking; this one does not start them.
- **D2 OI-001 ruling (first increment, App/shared contracts).** The following
  are reserved to the person: (a) marking work checked; (b) accepting a
  proposal wherever the active autonomy requires a proposal; (c) engineering
  approval; (d) relying on a result for a professional purpose; (e) changing
  the autonomy grant or enabling external-agent access. No autonomy grant
  widens past a reserved act or a declared checkpoint. The host names and
  enforces its own list (V4-HI-30). Operation-specific additions are made when
  the concrete SWB operation is selected (OI-021). The ruling does not show
  that SWBPIPE has adopted this list or enforces it (DEP-001).
- **D3 OI-002 ruling.** In the App, routine tool-permission and sandbox modes
  (including any classifier-based mode) remain the user's own Codex setting
  per project/turn. They govern tool execution only and never stand in for a
  reserved or professional act. In hosts there is no classifier permission
  mode in the first increment; the SWB default proposal mode applies
  (V4-HI-41).
- **D4 OI-012.** Codex `0.158.0` (npm `@openai/codex` latest at 2026-09-28) is
  selected as the definition/generation pin for this undertaking. Spike W11 is
  authorized: a scratch-directory npm install of that version, generation of
  protocol TS/JSON Schema, and a record of observed facts. Upgrades are
  deliberate. The pin is re-examined before implementation starts. The
  selection does not establish qualification (DEP-005).

These rulings apply through the DEL-04-01 policy representation (OUT-002
"adopted decisions") and the affected v0.2 definitions. The `Open_Issues.csv`
rows and the frozen decomposition snapshot are not rewritten by this record;
the bounded closeout (C1) reconciles the pointers. Remaining open matters are
unchanged: OI-003, OI-008 (App implementation owner; proposal from W6), OI-009,
OI-013, OI-014, OI-018 and OI-021.
