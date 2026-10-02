# R20 rulings — on F-B's findings F-37…F-40

Integrator: HELP_HUMAN. Input: [F/F-B.md](F/F-B.md). R1–R19 stand.

## R20-1 "Or it completes" (F-37) — INTEGRATION

An App run ends only by DEL-01-02 DEF-4 (the person's end) or the run
owner's end. When the agent reports the workflow finished, the App offers
"End run" (and, under R19-2 (b), "End ‹A› and start ‹B›"); the person's
choice ends it with cause `completed`. Nothing ends a run from the agent's
words alone. F-B's reading is adopted.

## R20-2 The DEL-02-03 prototype (F-38) — INTEGRATION

F-B's fence is extended to `DEL-02-03/Design/prototype/` to bring
`_delegation` and the two EV-3a readings to the v0.7 rule.

## R20-3 The run-end line (F-39) — INTEGRATION

When a run ends and no run starts with the next turn, the App prefixes the
person's next turn with one App-written line saying the run ended (workflow
and revision named). DEL-02-02 words it, beside its run-start framing, in
the same schema; RS records it as part of the per-run supply evidence (F-C
chooses the spelling).

## R20-4 No role against declared compatible roles (F-40) — INTEGRATION

A run whose conversation has no role, for a workflow that declares
compatible roles, is "unsupported": shown and recorded; the person may still
proceed. WD §4.7 states it (F-D).

## R20-5 The agent's proposal line (U-NIR-8) — INTEGRATION

The agent proposes a next workflow with one exact line,
`Next workflow: ‹origin›:‹name›`, naming one registered workflow. The App
reads only that line form (never prose; EXEC RC-5) and offers "Start
‹workflow› (proposed by the agent)". The product guidance shipped with the
App (DEL-02-04) tells the agent to use this form when it proposes one.

## R20-6 The handoff summary (U-NIR-9; D6 U-R12) — INTEGRATION

On "Continue as ‹role›", the App asks the source conversation's agent, in a
visible turn of that conversation, to draft a handoff summary; the person
edits it in the new conversation before sending. The App adds a header
naming the source conversation; the summary carries no instructions beyond
the person's own text, and nothing is sent until the person sends it.

## R20-7 WD's declared contract version (F-D) — INTEGRATION

The declared part's contract version stays `WD-v0.8`: it versions the
declared part's meaning, not the file label, and no declared-part meaning
changed in WD-v0.9. A declaration naming `WD-v0.9` remains an unknown
version (L-WDEX-33a).

## R20-8 F-A's two questions — INTEGRATION

- Codex goals stay a §8.4 note beside HCG-B04 (no new group HCG-A18); DEL-01-03
  NPTD shows them as its goals line. WD's S-11 count stays 27.
- The three new HOSTING fixtures stand: "the schema and its fixtures"
  includes new fixture files where a row adds a rule.
