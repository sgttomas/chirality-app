# D-GOV-43 — Codex host re-platform: stock App Server owned by the App host

Status: `TRANSCRIBED 2026-09-11` — the owner ruled and this candidate was
transcribed verbatim into
`docs/governance_harness/_DECISIONS/D-GOV-43_codex_host_replatform.md`;
that record governs. Historical text follows. This file is the prepared decision
record. It becomes the ruling only when the owner states the ruling, HELP_HUMAN
(or the implementing agent) copies this file to
`docs/governance_harness/_DECISIONS/D-GOV-43_codex_host_replatform.md`,
fills the three bracketed fields verbatim from the owner's words, adds the
register row below to `docs/governance_harness/_DECISIONS/_REGISTER.md`, and
commits under a tranche manifest. Nothing in `_DECISIONS/` is edited after
that; later change supersedes.

Date: `[owner ruling date, America/Edmonton]`

AcceptedBasis: `a75adecf13f055c092ffa92809f66e7817c44242`

ProposalSHA: `3ef2ef524956498f8923323dc6cf9d672dbeb50b` (revision 3 text of
`docs/governance_harness/_PROPOSALS/D-GOV-43_2026-09-11_codex_host_replatform/D-GOV-43.proposed.md`)

ApplicationSHA: TBD (the coordinated application tranche)

EffectiveSHA: TBD

## Owner ruling (verbatim)

> [owner's words]

Struck items, if any: `[none | list of folded choices or ruling items struck]`

## Decision

The fourteen ruling items of `D-GOV-43.proposed.md` at ProposalSHA are
adopted as written, with the three folded choices (bounded coordinated
authority, inexpensive preservation of daemon-era chats, retirement of the
residency requirements) standing unless struck above. Findings 1 to 7,
"Surfaces touched", the gates, and `IMPACT.md` at the same SHA are the
record of what is authorized. `AGENTS.proposed.patch` at that SHA is the
exact Root instruction delta the application tranche applies.

## Clarification adopted with the ruling (round-3 review)

The post-build checks listed in ruling item 12 (S-6, S-8, and verification of
the bundle signature and the Codex pin) are the expected minimum, not an
absolute ceiling. Repeat an affected check when a source, configuration or
packaging change invalidates its earlier evidence, for example when packaged
instruction roots resolve differently from development files. Do not repeat
unaffected tests merely because another stage has begun. This does not add
another acceptance programme.

## Application boundary

This record authorizes, together and bounded to this decision, the Root
amendments and the Runtime and App changes named in `IMPACT.md`, applied in
one coordinated tranche with its own M2/G4 manifest; notices to the Runtime,
App and PEC loops record that application. It authorizes the functional spike
on the production path against ruling item 12, one consolidated signed build
after independent source review, and the owner's native verification. The
implementation author's code is reviewed by a separate independent source
reviewer; the three proposal reviews do not substitute. Material scope or
behaviour changes and consequential findings return to the owner; routine
implementation choices do not. This record does not authorize release,
publishing, acceptance of unknown future bytes, any change to the Codex
sole-engine rule, local-model work, or reliance on the retired daemon path.

Supersedes in the stated parts, never edited: D-GOV-20 items 2, 3 and 4 on
the App MVP Codex path; D-GOV-36's daemon-owned custody exception and
bootstrap namespace. Read with: D-GOV-28, D-GOV-35, D-GOV-37 to D-GOV-42.

## Register row (append to `_REGISTER.md` after the D-GOV-42 row)

```
| D-GOV-43 | Codex host re-platform: stock App Server owned by the App host | **RULED [date]** — “[owner's words]”; revision 3 at `3ef2ef52…`; post-build minimum-not-ceiling clarification adopted | Stock pinned App Server child over stdio with the full protocol; Chirality effective Codex home with separated authentication; user-chosen policy; daemon and supplier-admission retirement; bounded coordinated Root/Runtime/App application; eight-check spike on the production path; no release, publishing or local-model work. |
```
