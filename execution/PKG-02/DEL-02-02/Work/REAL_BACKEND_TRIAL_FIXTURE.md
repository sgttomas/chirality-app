# Real-backend clean trial and Bring back (evidence pointer)

The J2 clean-trial path ran once against the real stock Codex 0.160 app-server,
with a deterministic loopback Responses fixture scripting the model replies. The
run went through these steps:
- an invented, unregistered draft;
- the trial's own conversation, from an actual Host `thread/start`;
- `start_clean_trial` and `send_trial`;
- the trial read from native history with fidelity `verbatim`;
- the trial link naming the trial conversation, the authoring conversation and
  the acknowledged native turn;
- no run, no registration and no offer;
- Bring back pre-filled only;
- the explicit send to the authoring conversation, with the `brought back`
  observation bound to that native turn.

The account, invocation, assertions, evidence identities and limits are in
DEL-01-01's
[LOCAL_RESPONSES_WORKFLOW_FIXTURE.md](../../../PKG-01/DEL-01-01/Work/LOCAL_RESPONSES_WORKFLOW_FIXTURE.md)
("Clean trial and Bring back join").

This changes no WR commitment, and no TT, FT or SQ-BB text. It is opt-in,
synthetic, test-only evidence. It is not J2, human or native qualification. The
cold, after-relaunch Bring back path is not exercised.
