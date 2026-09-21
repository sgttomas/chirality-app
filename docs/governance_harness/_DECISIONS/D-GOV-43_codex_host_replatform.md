# D-GOV-43 — Codex host re-platform: stock App Server owned by the App host

Status: `RULED 2026-09-11` — owner ruling recorded; coordinated application
tranche and functional spike pending

Date: `2026-09-11` (America/Edmonton)

AcceptedBasis: `a75adecf13f055c092ffa92809f66e7817c44242`

ProposalSHA: `3ef2ef524956498f8923323dc6cf9d672dbeb50b` (revision 3 text of
`docs/governance_harness/_PROPOSALS/D-GOV-43_2026-09-11_codex_host_replatform/D-GOV-43.proposed.md`)

RulingRecordedIn: the commit that introduces this file on branch
`claude/chirality-v3-mvp-trial-ab05cb`, merged to `main` through a pull
request under the owner's direction below; the merge SHA is recorded in
`_REGISTER.md` (K-AUTH-2)

ApplicationSHA: TBD (the coordinated application tranche)

EffectiveSHA: TBD

## Owner ruling (verbatim)

Owner Ryan Tufts, 2026-09-11 (America/Edmonton), in the Chirality v3
Codex-only MVP trial session:

> I rule D-GOV-43 accepted as revision 3 at commit 3ef2ef524, with the
> post-build minimum-not-ceiling clarification. The three folded choices
> stand.

Struck items: none.

In the same message the owner directed: "You may push changes and open a PR
and merge once the CI goes green."

## Decision

The fourteen ruling items of `D-GOV-43.proposed.md` at ProposalSHA are
adopted as written, with the three folded choices (bounded coordinated
authority, inexpensive preservation of daemon-era chats, retirement of the
residency requirements) standing. Findings 1 to 7, "Surfaces touched", the
gates, and `IMPACT.md` at the same SHA are the record of what is authorized.
`AGENTS.proposed.patch` at that SHA is the exact Root instruction delta the
application tranche applies. The three review rounds
(`REVIEW_FEEDBACK_R1.md` to `R3.md`) are the record of how the text reached
revision 3.

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

Implementation entry for the separate implementing session:
`projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/HANDOFF.md`.
