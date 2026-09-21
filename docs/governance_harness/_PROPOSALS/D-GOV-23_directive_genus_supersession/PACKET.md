# D-GOV-23 — Exact-prose supersession of the DIRECTIVE §1 genus clause (obligation (a))

> **Status: CANDIDATE — NOT RULED.** This packet binds nothing (K-AUTH-1). It
> becomes authority only through an explicit owner ruling recorded in
> `docs/governance_harness/_DECISIONS/` and bound to git SHAs per §6. Silence,
> file creation, validation, commit, or Git transport is not approval.
>
> **Provisional ID:** D-GOV-23 (next free after D-GOV-22; reconcile to the
> actual next-free ID at staging, per the D-GOV-20 collision-repair
> precedent).
>
> **AcceptedBasis:** `main@08f526277` (the D-GOV-22 EffectiveSHA; the
> DIRECTIVE §1 prose quoted in Annex A is verified against this state).
>
> **AcceptedCandidateSHA:** TBD — assigned when this exact packet is
> committed; the owner ruling approves that exact candidate SHA (§6).
>
> **FramedBy:** Agent-drafted (Agent 0, `HELP_HUMAN` posture) executing
> D-GOV-22 packet §5 item 3 at explicit owner direction ("proceed with
> obligation (a)", 2026-07-25, in-session).
>
> **RecordConvention:** D-GOV-18/19/21/22 exact candidate-SHA ruling
> pattern; supersede-never-edit. The Annex A replacement prose is applied
> **exactly** on an O-A ruling; any deviation discovered at application
> returns for re-approval.

---

## 0. Purpose

Perform PRD §9.1 follow-on obligation (a): supersede the ratified
`docs/DIRECTIVE.md` §1 genus clause with the RD-1 ruled genus formulation,
by an exact-prose, human-gated act on the D-GOV-21 pattern. This closes
**C-1** — the one DIVERGENT pair in the D-GOV-22 Annex A concordance map —
and completes the concordance the RD-1 ruling left pending.

## 1. Authority chain for this act

1. **RD-1 ruling** (owner, in-session 2026-07-25, selection verbatim
   "C — Two-level formulation"; recorded in PRD §9.1 and Receipt 37): fixed
   the ruled genus text reproduced exactly in Annex A.
2. **D-GOV-22 ruling** (owner, 2026-07-25, against candidate SHA
   `90fae458b`): adopted the PRD carrying that ruling and **authorized this
   tranche** (packet §5 item 3) while expressly *not* amending DIRECTIVE §1
   itself (packet §4) — this separate act was always required.
3. **Owner direction of record** (2026-07-25, in-session): "Merge PR #341
   and proceed with obligation (a)." This packet is the "proceed" step; the
   ruling below remains exclusively the owner's.

Until an O-A ruling here, the ratified DIRECTIVE §1 clause remains in force
as written (M2: every instruction-surface change is an independently
authorized, human-gated governance act).

## 2. Decision to make

- **O-A — SUPERSEDE.** The Annex A replacement paragraph lands in
  `docs/DIRECTIVE.md` §1 exactly as written; C-1 closes at the applied
  commit.
- **O-B — DECLINE / DEFER.** DIRECTIVE §1 stands; C-1 remains
  `RESOLVED-IN-PRINCIPLE — concordance pending`; falsifier F5 continues to
  watch that the divergence does not become permanent and unrecorded.

## 3. Scope — exactly one paragraph

The change is the §1 opening paragraph only (Annex A). Expressly **not**
changed by this act:

- The DIRECTIVE preamble sentence (line 5: "…the Chirality agent operating
  system") and every other "operating system" usage in DIRECTIVE, SPEC,
  TYPES, and `AGENTS.md` — these are **obligation (c)**, the propagation
  survey, whose findings return as proposals.
- `README.md` — **obligation (b)**, staged separately.
- The §1 paragraph's second-level description of the instruction surface as
  "a release-managed agent operating system" (retained verbatim inside the
  replacement): under the ruled two-level formulation the agent operating
  system is the *contained* level, so that description remains consistent
  and is deliberately kept.
- The adopted PRD, its candidates, and the D-GOV-22 record (immutable;
  supersede-never-edit).

## 4. Effect on the recorded divergence state

On the applied commit of an O-A ruling: **C-1 CLOSES** (the D-GOV-22
Annex A map's single DIVERGENT pair becomes concordant); PRD §1.2's
"ruled, concordance pending" description is satisfied by events —
the PRD file itself is not edited (adopted bytes; any future PRD amendment
is an M2 tranche per RD-4). The decision record for this act states the
closure; the register row and loop receipt carry it.

## 5. Options and recommendation

**Recommendation: O-A.** The ruled genus is already the adopted product
identity (D-GOV-22); DIRECTIVE §1 as it stands is the last live surface
carrying the superseded-in-principle wording as authority. The replacement
retains every operational clause of the existing paragraph verbatim —
monorepo topology, instruction-surface membership, working-roots, the
D-GOV-21 exception, desktop-harness packaging — and changes only the genus
sentence it opens with, replacing one sentence with the ruled two. Deferral
keeps the constitution's first sentence in recorded divergence from the
adopted PRD's first commitment.

## 6. Ruling mechanics and owner ruling

Per the exact-candidate pattern: the owner rules against the
AcceptedCandidateSHA (the commit containing this exact packet), naming O-A
or O-B. On O-A, the implementation tranche applies Annex A exactly to
`docs/DIRECTIVE.md`, publishes the decision record (verbatim ruling fence,
all SHAs, C-1 closure), adds the register row and loop receipt, and reports
the EffectiveSHA after the human merge gate. If the applied prose must
deviate from Annex A for any reason, it returns for re-approval instead.

```text
RULING: (to be recorded verbatim in the decision record; this packet is
superseded, never edited)
```

---

## Annex A — Exact candidate prose

**Target:** `docs/DIRECTIVE.md` §1 "Founding Intent", the opening paragraph
(line 13 at the AcceptedBasis). One paragraph replaced; nothing else in the
file changes.

### A.1 Current text (exact, to be superseded)

> Chirality is a governed, filesystem-native agent operating system for deliverable-heavy professional work. It is maintained as a private canonical monorepo whose root is the **shared instruction surface** — a release-managed agent operating system (`AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`) — that serves multiple project and domain **working-roots** nested under `projects/*` and `domains/*`, and — under the D-GOV-21 exception — the root product's own working root at the repository root. The same instruction surface is also packaged as a desktop harness that runs agents against a user-selected working folder.

### A.2 Replacement text (exact, applied verbatim on an O-A ruling)

> Chirality Root is the canonical human-governed application environment and generative operating form for governed professional knowledge work. It contains a filesystem-native agent operating system together with the normative basis, developmental machinery, evidence, and human judgment by which that operating system is formed and governed (RD-1 ruled genus, adopted through D-GOV-22). It is maintained as a private canonical monorepo whose root is the **shared instruction surface** — a release-managed agent operating system (`AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`) — that serves multiple project and domain **working-roots** nested under `projects/*` and `domains/*`, and — under the D-GOV-21 exception — the root product's own working root at the repository root. The same instruction surface is also packaged as a desktop harness that runs agents against a user-selected working folder.

### A.3 Construction notes (non-binding)

The first two sentences are the RD-1 ruled genus text **verbatim**, with one
addition: the parenthetical provenance pointer "(RD-1 ruled genus, adopted
through D-GOV-22)" appended to the second sentence, so the constitution's
genus clause carries its own authority trail the way the D-GOV-21 exception
clause does. Sentences three and four are the existing paragraph's remaining
text, unchanged byte-for-byte; their subject pronoun "It" now refers to
Chirality Root. If the owner prefers the ruled text with **no** provenance
parenthetical, striking it is a one-clause deviation that must return as a
revised candidate (exact-prose discipline) — say so at ruling and Rev 2 of
this packet will carry it.
