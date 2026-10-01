# Decisions pending (2) — APP-V4-DESIGN-PASS-3-20261001 (checkpoint L)

Prepared by HELP_HUMAN from the six D returns, OBS-2 and the join
consolidation [F/F0_JOINS.md](F/F0_JOINS.md) (§5). The recommendations are
the integrator's. Nothing here is decided until the owner's answer is
recorded in [OWNER_DECISIONS.md](OWNER_DECISIONS.md). The conflicts between
the new files that the integrator decided are in
[R18_RESOLUTIONS.md](R18_RESOLUTIONS.md).

## Part 1 — asked now

**L-1 API-key conversations (D4 U-A1; K-2).** At Codex 0.158.0 one Codex
home holds one signed-in account, so a ChatGPT sign-in and an API key held
by Codex cannot sit in the same home.
- **A. A second App-owned Codex home for API-key conversations
  (recommended).** Both homes share your settings (K-1, observed to work in
  OBS-2); API-key conversations run on their own Codex process. The hosting
  design gains a per-home dimension (one Codex process per App home).
- B. Keep one home; the App holds the key itself (for example in the macOS
  keychain) and passes it to Codex per conversation. This changes the
  accepted rule that Codex holds the credentials (ARCHITECTURE V4-ARC-04).

**L-2 Changing a conversation's role (K-9; OBS-2 O-5).** Codex 0.158.0
accepts new instructions on resume but silently ignores them, so "a change
takes effect at the next idle point" cannot work that way.
- **A. At the next idle point the conversation continues in a fork that
  carries the new guidance (recommended)**, once one more local observation
  confirms a fork takes it. Until then, and if it does not, the change
  applies to new conversations and the open conversation says "role change
  applies to new conversations".
- B. New conversations only, permanently.
- C. Add the new role text on every turn through plan-mode settings
  (experimental; the old role text stays in force beside it, so it is not a
  real change).

**L-3 Start-up traffic and plugins (K-12; OBS-2 O-7).** The one setting that
stops both start-up connections (chatgpt.com and github.com) is
`plugins = false`, which also turns off Codex plugins in the App.
- **A. Follow your own plugin setting (recommended).** If you use plugins,
  the connections happen and are shown and recorded; if you don't, the App
  turns plugins off for its Codex and the connections stop.
- B. Always off in the App: no start-up traffic, no plugins in the App.
- C. Always on: shown and recorded.

**L-4 Workflows already in a library without a registration record (D5
U-WR-4; K-7, K-8).** Every workflow in an existing project or user library
predates registration.
- **A. Register in place (recommended):** each runs after one review and
  registration act; the App lists them for review. Consistent with "only
  registered revisions run".
- B. Let them run, shown as "not registered".

**L-5 An OS password or Touch ID check per act (D3 U-AAC-2).** The person is
recorded "identity not verified" (K1-4).
- **A. None now (recommended);** offered as an option for the governance
  phase.
- B. For engineering approval and professional reliance (A6, A7) only.
- C. For every act.

**L-6 Observing sign-in and API-key flows (D4 U-A2).** K-11 excluded them.
- **A. Not now (recommended):** those cells stay labelled as resting on the
  protocol types; asked again at the phase review if the design needs it.
- B. You sign in yourself for one observation in a scratch home.

**L-7 The App implementation owner (D4 U-A11).** DEL-01-05 REQ-005 names
"the Owner with the App implementation owner" for the account-home choice.
- **A. That is you; your K-1 answer covers both (recommended).**
- B. Someone else, to be named.

## Part 2 — for your information (nothing to decide)

- **Delegation never reaches an LM Studio model** at 0.158.0: Codex sends
  its delegation tools in a format LM Studio drops. The delegation views are
  absent in those conversations. Delegation worked only through a test
  translator.
- **Only plan mode is experimental.** Delegation is a standard Codex
  feature, so it is not labelled experimental (K-5 still applies to plan
  mode).
- **After a quit**, Codex writes into the conversation that "the user
  interrupted the previous turn on purpose"; the model reads that on the
  next turn.
- **What reaches the model provider:** every model request carries your time
  zone and a Codex installation id (to your local server in OBS-2; to the
  cloud provider when one is selected).
- **An executor deviation:** during OBS-2 memory pressure turned critical
  once; the brief said stop and report; the executor reduced the load and
  continued. Recorded in DISPATCH.

## Part 3 — taken by the integrator (open to being overruled)

| Matter | What the integrator does |
|---|---|
| A selected workflow and newer revisions | Selection stays on its revision and shows that a newer one exists |
| Unmodified guidance copies on a new App release | Updated automatically, and the App says so; a modified copy is kept and flagged |
| Your global `AGENTS.md` and skills in the App | Visible to the App's Codex by the same link as your settings (R18-6) |
| The internal switch for Codex's remote-control loop | Not used; the loop is shown (no connection without sign-in) |
| Where act capture runs; how long App records are kept | Left for the phase review (OI-008; ledger retention) |
