# R15 rulings — items returned by the residual sweep

Integrator: HELP_HUMAN. Input: `WAVE_B/RX.md`. R1–R14 stand.

## R15-1 "No model chosen" is not a destination refusal (RX #41) — DERIVED

V4-HOST-01 gives the person options with no default, so a host loop with no
model selected cannot start a turn. That is a run that does not start, not a
refusal at the network boundary: no destination exists to refuse. LOOP F-2
and MS-02 record it as "run not started — no model selected"; RS adds that
cause to its run-start or run-end element (whichever RS uses for a run that
never reaches its first turn), with no destination entry. The evidence is the
loop's own configuration state at start ("observed absence" stays as MS-02's
evidence wording).

## R15-2 GUIDE citations of the record arrangement (RX #14)

Done in node B8 with the GUIDE re-pin.
