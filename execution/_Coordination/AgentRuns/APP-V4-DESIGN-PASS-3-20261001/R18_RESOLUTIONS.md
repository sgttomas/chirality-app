# R18 rulings — after D round 1 and OBS-2

Integrator: HELP_HUMAN. Inputs: [F/F0_JOINS.md](F/F0_JOINS.md) (§2 conflicts
C-01…C-25 and gaps G-1…G-5, §5 owner items, §7 OBS-2 consequences), the
six D returns, OBS-2 (`DEL-01-01/Design/OBS_2_0.158.0.md`). R1–R17 stand
except where amended here. Labels as in R9.

## R18-1 Conflicts decided as F0 recommends — INTEGRATION

C-01 (RS defines the persisted A15 form in camelCase: `reviewedDraft
{draft: WR ID-3 string, content}`, `priorRevision`: RS `workflowTuple` or
null; WR keeps its internal object and writes through the RS writer),
C-02, C-03 (D1's reading: a closed generation's events are not re-readable;
views rebuild from Codex history), C-04 (replace `multiAgentMode`:
delegation is available when `Model.multiAgentVersion` ≠ `disabled` and the
provider accepts `namespace` tools; an effective `features.multi_agent =
false` reads missing), C-05 (only plan mode is labelled "experimental";
delegation is a stable surface and is not), C-06 (DEL-01-04 composes
`collaborationMode` on `turn/start` and sends the default mode explicitly to
leave plan mode; D2's row DEL-01-04 → DEL-01-03 is adopted), C-07 (D2's row
DEL-02-04 → DEL-01-03 is dropped; the K-10 standing is a runtime value),
C-08 (the export carries D6's three-value standing as handed), C-10 (RS
`codexAccount` is the reported email or "ChatGPT account (no email
reported)"; plan type is not recorded; HOSTING `actorRef` stays a string
derived from the same three values), C-12 (DEL-01-04 offers "Stop Codex"
and "Restart Codex", each asking first with live work), C-13, C-14, C-15,
C-18 (D6 states it; see R18-6), C-19, C-20 (generation identity = App
session + spawn counter, plus the App-owned home only if K2-1 is adopted),
C-21, C-22, C-23, C-24.

## R18-2 K-3 wording (C-09) — SETTLED wording, DERIVED scope

A workflow run that cannot start reads "run not started — no model
selected" (R15-1). An ordinary conversation with no model selected reads
"not started — no model selected". Both files state which applies.

## R18-3 Remote-control loop (C-25) — INTEGRATION

K-12 turns off what Codex's **settings** allow. The internal environment
variable `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED` is not a
setting and is not used. The network view shows the loop as observed at
0.158.0: no connection without sign-in (OBS-2 O-7); with sign-in, not
observed.

## R18-4 Delegated children (C-16) — amends R17-9's last bullet

OBS-2 O-4a observed that native child roles are honoured and that the role
file's `developer_instructions` **replace** the parent's for that child.
The App therefore supplies each child role through Codex's native agent-role
configuration, with the composition product guidance + that role (CR-1). A
child spawned without a role type is not observed; its guidance is stated
as unknown, not as inherited.

## R18-5 Act control opened by the person from an arrival row (U-NIR-5) — DERIVED (K1-1, EXEC RC-4)

When the person clicks an arrival row and that opens the act control, the
person opened it; the product did not react to the arrival. The App never
opens, focuses or notifies because of an arrival. EXEC RC-4 gains that
sentence (J-E8).

## R18-6 The person's global Codex guidance in the App home (C-18) — INTEGRATION, PROPOSED

Under K-1 the App home shares the person's `config.toml`. The App home also
shows the person's global `AGENTS.md` and skills by the same link, so that
Codex's native discovery in the App matches the person's Codex (Root
`AGENTS.md`: "skill availability follows Codex's native discovery").
`instructionSources` records what Codex reports. D4 and D6 state it.

## R18-7 Gaps — INTEGRATION

- G-1: D4 round 2 writes the receiving comparison for seam S-4.
- G-2: F's GUIDE node cites AAC-v0.1 in G-1 and M5.3.
- G-3: the goals tools and `thread/goal/cleared` are placed by D2 round 2
  as a native item group shown without translation, and by F in HOSTING
  §8.4.
- G-4: an item opened and never completed settles "not completed (turn
  ended)" at turn end, in NPTD, NIR and RECOVERY.
- G-5: the history marker Codex writes on a graceful stop is shown to the
  owner (DECISIONS_PENDING_2 visibility list) and stated in RECOVERY's quit
  sequence.

## R18-8 Held for the owner

C-11 and the per-home part of C-20 wait for U-A1; C-17 waits for the
role-change question; the start-up traffic setting waits for the plugins
trade-off. See [DECISIONS_PENDING_2.md](DECISIONS_PENDING_2.md).

## R18-9 OBS-2 standing — INTEGRATION

O-4, O-4a and O-4b were observed only through a loopback adapter that
flattened Codex's `namespace` tools for LM Studio. Files cite them as
"observed through an adapter (OBS-2), not stock behaviour". The S-9
continuation is recorded in DISPATCH; the observations after it stand with
that note.
