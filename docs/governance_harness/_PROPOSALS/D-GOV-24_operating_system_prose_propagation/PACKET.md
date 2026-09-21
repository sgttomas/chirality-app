# D-GOV-24 — Exact-prose propagation of the ruled genus to four document self-descriptions (P-1..P-4)

> **Status: CANDIDATE — NOT RULED.** This packet binds nothing (K-AUTH-1). It
> becomes authority only through an explicit owner ruling recorded in
> `docs/governance_harness/_DECISIONS/` and bound to git SHAs per §5. Silence,
> file creation, validation, commit, or Git transport is not approval.
>
> **Provisional ID:** D-GOV-24 (next free after D-GOV-23; reconcile to the
> actual next-free ID at staging, per the D-GOV-20 collision-repair
> precedent).
>
> **AcceptedBasis:** `main@628f1728e` (merge of PR #343; the four current
> sentences in Annex A are verified byte-exact against this state).
>
> **AcceptedCandidateSHA:** TBD — assigned when this exact packet is
> committed; the owner ruling approves that exact candidate SHA (§5).
>
> **FramedBy:** Agent-drafted (Agent 0, `HELP_HUMAN` posture) at explicit
> owner direction ("proceed with P-1..P-4 as a small exact-prose packet",
> 2026-07-25, in-session), carrying forward proposals P-1..P-4 of the
> obligation (c) survey
> (`execution/_Coordination/SURVEY_2026-07-25_OBLIGATION_C_operating_system_prose.md`).
>
> **RecordConvention:** D-GOV-18/19/21/22/23 exact candidate-SHA ruling
> pattern; supersede-never-edit. The Annex A replacement prose is applied
> **exactly** on an O-A ruling, extracted programmatically from this packet;
> any deviation discovered at application returns for re-approval.

---

## 0. Purpose

Propagate the RD-1 ruled two-level genus (adopted through D-GOV-22; applied
to DIRECTIVE §1 through D-GOV-23) into the four remaining sentences that use
"the Chirality agent operating system" as the *top-level* identity of the
whole system: the DIRECTIVE preamble and the CONTRACT, SPEC, and TYPES
self-descriptions. These are the only four such instances in the governed
corpus (obligation (c) survey, universe: all instruction surfaces). The six
contained-level usages the survey classified KEEP are untouched. This packet
introduces **no new semantic content** — each replacement names Chirality
Root as the top level and relocates the agent operating system to its ruled
contained level, changing nothing else in any sentence.

## 1. Authority chain for this act

1. **RD-1 ruling** (owner, 2026-07-25; PRD §9.1; Receipt 37) — the ruled
   genus.
2. **D-GOV-22** (owner, 2026-07-25) — adopted the PRD; authorized obligation
   (c) (packet §5 item 5), whose survey produced P-1..P-4 as proposals.
3. **D-GOV-23** (owner, 2026-07-25) — the DIRECTIVE §1 supersession this
   packet propagates; its scope expressly excluded these four sentences.
4. **Owner directions of record** (2026-07-25, in-session): "Merge PR #342
   and proceed with obligations (b) and (c)"; then "Merge PR #343 and
   proceed with P-1..P-4 as a small exact-prose packet" — the latter also
   selects this vehicle over the lawful PR-review alternative (adopted PRD
   §6.2). The ruling below remains exclusively the owner's.

Until an O-A ruling here, all four ratified sentences remain in force as
written (M2).

## 2. Decision to make

- **O-A — PROPAGATE.** The four Annex A replacements land exactly as
  written in their respective files.
- **O-B — DECLINE / DEFER.** The four sentences stand; the survey remains
  the record of the divergence-in-tone (no DIVERGENT conflict exists — the
  four usages predate and simply lean on the superseded genus).

## 3. Scope — exactly four sentences, nothing else

One sentence (or sentence pair, where the quoted prose spans two sentences)
per file: `docs/DIRECTIVE.md:5`, `docs/CONTRACT.md:7`, `docs/SPEC.md:5`,
`docs/TYPES.md:5`. Expressly untouched: the six KEEP instances
(DIRECTIVE:13/76/199/204, SPEC:44, TYPES:50); every normative clause of all
four documents; `README.md` (obligation (b), done); C-2 and C-4 (separate
correction proposals); the adopted PRD and all prior decision records.

## 4. Options and recommendation

**Recommendation: O-A.** The four replacements complete the genus
propagation so no governed surface still presents the pre-RD-1 top-level
identity as current self-description; each keeps its document's claim
accurate under the ruled formulation with the smallest possible change; and
the change is pure propagation of an already-ruled decision — deferral
leaves the constitution's own preamble describing a genus its §1 no longer
states.

## 5. Ruling mechanics and owner ruling

Per the exact-candidate pattern: the owner rules against the
AcceptedCandidateSHA (the commit containing this exact packet), naming O-A
or O-B. On O-A, the implementation tranche applies Annex A exactly
(programmatic extraction; each current sentence verified unique in its live
file first), publishes the decision record (verbatim ruling fence, all
SHAs), adds the register row and loop receipt, ships routed M6 change
notices if any pinned surface moved, and reports the EffectiveSHA after the
human merge gate. Any necessary deviation returns for re-approval instead.

```text
RULING: (to be recorded verbatim in the decision record; this packet is
superseded, never edited)
```

---

## Annex A — Exact candidate prose (four replacements)

Each "Current" line is quoted byte-exact from the file at the AcceptedBasis
and is verified to occur exactly once in that file at application time.

### A.1 — P-1: `docs/DIRECTIVE.md` line 5 (preamble)

Current (exact):

> This document captures the founding intent, design philosophy, and structural constraints of the Chirality agent operating system. It is the "why" document — the principles that govern all other governance documents, agent instructions, and operational decisions.

Replacement (exact):

> This document captures the founding intent, design philosophy, and structural constraints of Chirality Root and the filesystem-native agent operating system it contains. It is the "why" document — the principles that govern all other governance documents, agent instructions, and operational decisions.

### A.2 — P-2: `docs/CONTRACT.md` line 7

Current (exact):

> This document is the authoritative catalog of binding invariants for the Chirality agent operating system.

Replacement (exact):

> This document is the authoritative catalog of binding invariants for Chirality Root and the agent operating system it contains.

### A.3 — P-3: `docs/SPEC.md` line 5

Current (exact):

> This document is the authoritative specification for the physical structures, file formats, schemas, and layout conventions used in the Chirality filesystem-as-state agent operating system.

Replacement (exact):

> This document is the authoritative specification for the physical structures, file formats, schemas, and layout conventions of the filesystem-as-state agent operating system contained in Chirality Root.

### A.4 — P-4: `docs/TYPES.md` line 5

Current (exact):

> This document is the authoritative vocabulary reference for the Chirality agent operating system. It defines the canonical entities, stable identifier formats, enumerated types, agent roles, and lifecycle states.

Replacement (exact):

> This document is the authoritative vocabulary reference for Chirality Root and the agent operating system it contains. It defines the canonical entities, stable identifier formats, enumerated types, agent roles, and lifecycle states.
