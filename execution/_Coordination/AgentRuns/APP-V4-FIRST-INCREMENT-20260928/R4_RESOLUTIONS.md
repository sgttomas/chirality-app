# R4 integration rulings — Wave-2 feedback into the whole set (sweep A1)

Integrator: HELP_HUMAN. Sources:

- [reviews/V2.md](reviews/V2.md) residuals;
- W7 `DEL-02-03/EXEC-v0.1` findings F-1…F-16;
- W8 `DEL-03-03/ADAPTER-v0.1` findings F-1…F-12;
- W9 `CA-v0.1` / `XT-v0.1` findings;
- owner DECISION-2 (D5, D6) in [OWNER_DECISIONS.md](OWNER_DECISIONS.md).

Earlier rulings (R1–R3) stand unless amended here. Labels are as before.
Wave-1 files take a **v0.4** version bump; W7 and W8 files move to **v0.2**.
Each file gains a "## Changes from v0.3" (or "from v0.1") table keyed by R4
IDs and the source finding IDs. For MINOR residuals, apply the finder's
proposed fix unless a ruling below contradicts it.

## Owner decision application

- **R4-1 (D5, SETTLED by DECISION-2).** Host content read by the App's Codex
  through the external channel may flow to the App conversation's selected
  model, cloud included. This is the person's flexibility. The App:
  - does not gate enablement on the model destination;
  - **records** each run's model destination (DEL-04-03 run record);
  - **shows** it in the channel status (DEL-03-03), as information only.

  A host may restrict its own channel (DEP-001). V4-HOST-02 still governs the
  host's embedded agent. DEL-03-03 closes U-X2. DEL-04-03 and DEL-03-03 carry
  the destination element.
- **R4-2 (D6, deferred by DECISION-2).** App-side run holds stay
  `UNRESOLVED{D6}` pending SWBPIPE SQ-02. Every file that relies on an App
  hold:
  - carries per-checkpoint **hold support** (EXEC §3.6);
  - never claims an App hold it cannot enforce;
  - records **action during hold**;
  - adopts neither interposed App code (HP-1) nor reliance on
    `turn/interrupt` (HP-2).

  HP-3 (a named-rule decline of a tool-permission request) stays a permitted
  best effort under D3. DEL-02-03 F-10 is carried to C1 as a SoW gap, with D6
  as its home.

## Hold machine and checkpoints (owner: DEL-02-03; all adopt)

- **R4-3 Resume point and re-hold (EXEC §4.7; W7 F-2).** EXEC's definition is
  adopted everywhere:
  - The resume point is HD-5.
  - A lapse after resume re-holds the same arrival: "waiting — re-held, lapsed
    at ‹t› after resume". The run stops at its next action. Nothing done is
    undone. Gated outputs show standing *lapsed*. The person is asked again for
    the whole scope.
  - A5 and A12 never re-hold.
  - The interim "performed + act-lapsed" display is withdrawn.

  Files: WD I-4, ACT §4.3, RS L-12, AS §4, LOOP C-4, PANEL W-5e.
- **R4-4 No resumption of an ended run (W7 F-4).** An ended run is never
  resumed. Acts after the run ends are shown "after run end" and change
  nothing. Continuation is a new run carrying a **continues ⟨run⟩** link, which
  inherits nothing. An interruption is not a run end. Replace "unless DEL-02-03
  defines resumption" in WD U-21, ACT §2.3, LOOP and PANEL. RS adds the link.
  PROPOSED.
- **R4-5 Capture after arrival (SP-6; W7 F-3).** An act counts toward a
  checkpoint only if it was captured at or after that checkpoint's arrival.
  Earlier acts are shown as "prior act not counted". PROPOSED; U-E4 stays open
  for the owner if he prefers to count prior acts. Repair LOOP FX-C4 and WD-EX
  R-16 against C's T15→T16 order.
- **R4-6 A12 supersedes only when established (W7 F-5).** A refused A12 does
  not count at a checkpoint, and it does not supersede a setting that is in
  force. A pending A12 leaves the checkpoint *waiting*. A lost confirmation
  makes it *unknown*. Files: ACT §2.5, RS L-0, AS, WD, LOOP C-8, PANEL W-5g.
- **R4-7 Mixed items (W7 F-1).** WD §4.3.7 adds MX-3 (a lost decision
  observation → *unknown*), MX-6 (every item left → the arrival is closed
  "replaced" by the next arrival) and MX-8 (application error or unknown after
  A5 → disposition unchanged, annotated). R2-18/R3-3 are CONFIRMED by DEL-02-03.
- **R4-8 Unsupported reason (W7 F-8).** WD §4.2.4 *unsupported* gains
  "checkpoint hold not enforceable on this surface", from EXEC §3.6 hold
  support.
- **R4-9 Grant-setting subject without A8 (W7 F-13).** When no A8 names a
  setting, the subject is the setting content named by the checkpoint's own
  declaration: the classes, grant values and scope it states. A declaration
  that names none is **invalid** for A12. INTEGRATION. File: ACT §4.2, WD.
- **R4-10 R3-1 class in the records (W7 F-6; V2 m-1).** RS R8 and AS §4 add
  "objects a named output concerns".
- **R4-11 RS elements (W7 F-7).** RS adds:
  - arrival and performance ordinals;
  - run-resumed event;
  - re-held and replaced annotations;
  - A12 control effect;
  - "prior act not counted";
  - continues ⟨run⟩;
  - action during hold;
  - transfer links;
  - revision verification;
  - compatibility-report reference;
  - model destination (R4-1).

## Acts, capture and the external channel

- **R4-12 Elicitation and user input are not act evidence (W7 F-9; W8 F-3).**
  HOSTING R9 and §6.1: answers to Codex user-input or MCP elicitation requests
  are **not act evidence**, and are never host act capture. HOSTING also
  classifies the MCP config, status and call surfaces, and the App-initiated
  `mcpServer/tool/call` (the App is the caller).
- **R4-13 App-side configuration is never A13 evidence (W8 F-4).** Where A13 is
  captured App-side is set by DEL-04-01 (U-X1), consistent with EXEC CAP-1…9.
  An App-side Codex configuration that an agent could write is never A13
  evidence. The host's refusal is the authoritative "off" (W8 F-2; ADAPTER
  VER-002 reading).
- **R4-14 Constraint carriage is assurance-rated (W8 F-1).** P §3.3, ACT §4.4,
  WD §4.2.2 and R2-12 no longer say "the external adapter carries". They say
  the constraint is carried with a **carriage assurance**: App-assured,
  host-held, model-supplied or absent. Model-supplied carriage alone does not
  satisfy R2-12. This strengthens the SQ-02 option where the host evaluates the
  declaration itself.
- **R4-15 Author identity unverified (W8 F-8).** P §3.3 author identity allows
  the value **unverified**. RS R11 adds the matching evidence limit.
- **R4-16 App reporter of "channel not enabled" (W8 F-7).** C §4.1: the App
  reports *channel not enabled* when its own configuration is off, and the host
  reports it when the host channel is off.
- **R4-17 FX-25 wording (W8 F-5).** ACT FX-25 reads "drives T9–T10, observes
  T11–T12".

## Fixtures and residuals

- **R4-18 T15 (V2 MAJOR-1; W9 CA F-7/XT F-7).** ACT FX-20, AS F2, RS E7, PANEL
  PC-22 and WD-EX R-5a re-point to C's T15: class P-03, scope {FX-W1; {S-4}},
  ⟨set-2⟩. Their labels-only local variants are removed, or kept as
  `L-‹file›-n` with a reason.
- **R4-19 V2 minors m-1…m-13.** Apply as proposed in V2:
  - ⟨set-T15⟩ → ⟨set-2⟩, ⟨S-new⟩ → S-5, §10.6 → §10.7;
  - rename colliding FA-n and N-n labels;
  - EXAMPLES OP-C10 class per R3-4, and P cites R3-4;
  - RS "A1/A2 when the person performs them" aligned with ACT §2.4;
  - LOOP change-table count;
  - use T16a instead of local S-4 act cases;
  - close the "to be confirmed at V2" markers;
  - add R3 (and now R4) to Consumed inputs.
- **R4-20 Fixture additions requested by Wave 2.** C §10 adds:
  - an App-file subject and an App-side library (W7 F-15);
  - a catalog-edition addition event, used by XT L-XT-1 (W9 XT F-5).

  WD E1 adopts an optional OP-C12 host-check step (W9 CA F-5). ADAPTER adds
  rehearsals for two submissions before acknowledgment and for an App restart
  (W9 XT F-4).
- **R4-21 Harness-capability reached-when (W7 F-16).** Reached-when kind (a) on
  a *harness capability* is **not holdable** in App runs pending D6. WD states
  this; hold support reports it.

## Carried to closeout C1 (no sweep edits)

- SoW gaps: DEL-02-03 F-10 (App hold point) and every "OI-001/002 open" SoW
  text.
- All register findings: V1 RF-*, X-16, W7, W8 F-11, W9 CA F-2 / XT F-2.
- HANDOFF wording (W9 CA F-8).
- Out-of-scope receivers: DEL-02-02, DEL-09-01, DEL-09-07 (D1).
- Multi-row A4 purpose after partial lapse (U-03 / WD U-05c). The EXEC
  whole-scope request satisfies every option; it stays an open owner question
  at its point of need.
