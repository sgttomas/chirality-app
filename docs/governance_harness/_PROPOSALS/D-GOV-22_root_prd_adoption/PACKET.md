# D-GOV-22 — Adoption of the Chirality Root PRD (exact-candidate instrument)

> **Status: CANDIDATE — NOT RULED.** This packet binds nothing (K-AUTH-1). It
> becomes authority only through an explicit owner ruling recorded in
> `docs/governance_harness/_DECISIONS/` and bound to git SHAs per §8. Silence,
> file creation, validation, commit, or Git transport is not approval.
>
> **Provisional ID:** D-GOV-22 (next free after D-GOV-21; reconcile to the
> actual next-free ID at staging, per the D-GOV-20 collision-repair precedent).
>
> **CandidateSubject:** the adoption-ready root PRD, Revision 5, as the exact
> bytes committed at `d9ea86f88504cb8d859a4cf3f042bac00d38fe57` (PR #340
> branch `claude/root-prd-lane-a-20260725`):
>
> | File | sha256 |
> |---|---|
> | `execution/_Coordination/PRD_CANDIDATE_2026-07-25_root_product.md` | `d85ac3f941ee6808c9a62888bc488cec2198c2814b4f14641094cf0e0f1d04cb` |
> | `execution/_Coordination/PRD_CANDIDATE_2026-07-25_concordance_annex.md` (derivative package; adopted **as evidence companion**, per its own never-adopted status note) | `100b1287e9e9d2353e8f411f6962b51d722fd6b23f951ae94cec11948ff5f09b` |
>
> **AcceptedBasis:** all file/line citations in this packet are against
> `d9ea86f88` (the commit containing Rev 5). Re-verify if staged against a
> later basis.
>
> **AcceptedCandidateSHA:** TBD — assigned when this exact packet is
> committed; the owner ruling approves that exact candidate SHA (§8). Should
> the branch advance past `d9ea86f88` before ruling, the sha256 hashes above
> are the byte-identity check: the ruling adopts those exact bytes.
>
> **FramedBy:** Agent-drafted (Agent 0, `HELP_HUMAN` posture) under the
> owner's Lane A direction, root-PRD inquiry session, 2026-07-25, after four
> adversarial-review cycles by an independent second agent and five in-session
> owner rulings (RD-1..RD-5). Run record:
> `execution/_Coordination/AgentRuns/ROOT-PRD-LANE-A-20260725/`.
>
> **RecordConvention:** Options + Recommendation + Owner ruling; verbatim
> ruling fence and exact-candidate-SHA approval per the D-GOV-18/19/21
> pattern; supersede-never-edit.

---

## 0. Purpose

Adopt the Chirality Root product requirements document — the first integrated
PRD for the root product — as accepted product direction, by an owner ruling
bound to the exact candidate bytes named above. This is the instrument the
owner selected at RD-3 ("A+y": a `D-GOV-*` decision record on the
exact-candidate-SHA pattern, carrying a bidirectional concordance map against
`docs/DIRECTIVE.md` §1 — Annex A below). Adoption closes D-GOV-21 §6 step 5
(Lane A) and unlocks step 7 sequencing (root decomposition remains behind its
own gates).

## 1. Owner directions of record

All transcribed in the PRD §9 with verbatim fences, and in Loop Receipts 37
and 38 (`execution/_Coordination/LOOP_RECEIPTS.md`):

1. **RD-3 (instrument), ruled 2026-07-25, selection verbatim:** "A+y
   (Recommended)". Fixes this packet's form: exact-candidate `D-GOV-*`
   record + bidirectional PRD ↔ DIRECTIVE §1 map, uncovered items `TBD`, the
   map drawn against DIRECTIVE §1 **as it stands** with the RD-1 divergence
   recorded, obligation (a) sequenced after adoption.
2. **Final-cycle direction, 2026-07-25:** "Consider this as the final review
   cycle. Incorporate what has merit from your perspective and proceed from
   there." Staging this packet is the "proceed" step; the ruling below
   remains exclusively the owner's.
3. RD-1, RD-2, RD-4, RD-5 rulings: recorded verbatim at PRD §9.1–§9.5;
   SHA-binding of all five rulings occurs **here**, at this instrument's
   ruling (PRD §10.3).

## 2. Decision to make

- **O-A — ADOPT.** The owner adopts the Rev 5 PRD exact bytes as the accepted
  product direction for Chirality Root. Effects per §3; implementation
  tranche per §5.
- **O-B — DECLINE / DEFER.** The candidate remains immutable evidence; Lane A
  reopens for whatever revision the owner directs; nothing takes effect.

## 3. What adoption effects (on the PRD's own terms, §10.3)

1. **The 17 PROPOSED items take effect as accepted commitments**: the v1
   boundary (§3); OBJ-1..OBJ-7; D-13, D-14, D-15, D-16; the §7.2 governed
   promotion relationship; §8.3 release authority; falsifiers F4, F5, F6.
   TRANSCRIBED and CLARIFIED items carry their own upstream authority and are
   unaffected by this ruling except as newly cross-referenced.
2. **All five RD rulings become SHA-bound** at this record's publication
   (K-AUTH-2), completing what the in-session rulings began.
3. **The concordance map (Annex A) becomes the recorded divergence state**
   between the PRD and `docs/DIRECTIVE.md` §1: C-1 stays
   `RESOLVED-IN-PRINCIPLE — concordance pending` until obligation (a) lands.
4. The adopted-copy placement per RD-4-D and the §9.1 follow-on obligations
   are **authorized as the implementation tranche** (§5) — authorized by this
   ruling, executed after it, each instruction-surface touch remaining an M2
   human-gated act.

## 4. What adoption does not do

Restating the PRD's own §10.3 closing paragraph, as binding scope limits on
this ruling:

- Does **not** materialize anything under root `execution/` (`PKG-*`/`DEL-*`
  stay behind the D-GOV-21 §5.3 gate; G0 continues to enforce).
- Does **not** create or accept a root decomposition (D-GOV-21 §6 step 8 is
  its own future act).
- Does **not** change the public-export boundary (verified against
  `tools/export/export_public.py` `ROOT_DIRS`: `docs/` is already exported,
  `execution/` is already excluded — RD-4-D needs no boundary change).
- Does **not** amend the ratified `docs/DIRECTIVE.md` §1 genus clause. That
  is obligation (a), an exact-prose human-gated M2 supersession in the
  implementation tranche, after and separately from this ruling.
- Does **not** resolve conflicts C-2 or C-4 (carried open, §6).

## 5. Implementation tranche upon an O-A ruling

Authorized by the ruling, executed as ordinary follow-on work, every
instruction-surface touch human-gated (M2):

1. **Publication:** decision record in `_DECISIONS/` with the verbatim ruling
   fence and all SHAs; `_REGISTER.md` row; loop receipt; EffectiveSHA
   reported to the owner after the human merge gate.
2. **RD-4-D placement:** the adopted PRD bytes copied to root `docs/`
   (proposed: `docs/PRD_ROOT.md`, final name at owner's discretion), with a
   pointer block identifying the adopted exact SHA and the candidate's
   immutable home in `execution/_Coordination/`; candidates and revision
   evidence remain untouched there.
3. **Obligation (a):** exact-prose candidate for the DIRECTIVE §1 genus
   clause supersession (D-GOV-21 pattern), presented for separate owner
   ruling — closing C-1.
4. **Obligation (b):** `README.md` genus reword.
5. **Obligation (c):** propagation survey of SPEC/TYPES/AGENTS.md
   "operating system" prose; findings returned as proposals, not applied
   silently.
6. **C-2 correction tranche** (CONTRACT §1 invariant-index arithmetic) and
   **C-4** (README export description) proposed alongside, each separately
   gated.

## 6. Items expressly put to the owner at this ruling

The PRD flags these for confirmation **at the adoption instrument** — that
is, here:

1. **C-3 — pre-repo lineage date.** ID-3 records owner testimony of roughly
   three years of prior development lineage; an earlier Agent 0 brief
   asserted an in-repo start of 2026-02-18, while git shows the first commit
   (`7bee9ae41`, "Initial migrated Chirality repository") is 2026-05-18. ID-3
   (testimony) and ID-4 (git fact) are stated separately in the PRD. **The
   owner is asked to confirm or correct the ID-3 lineage testimony**; no
   in-repo source can settle it.
2. **ID-1, ID-2, ID-3 synthesis confirmation.** These identity claims are
   labeled OWNER_DECLARED as Agent 0 syntheses of in-session owner framing,
   not warranted verbatim (PRD §1.1). The PRD states the owner confirms or
   corrects them at adoption. An O-A ruling without noted corrections
   confirms them as accurate syntheses.

## 7. Options and recommendation

**Recommendation: O-A.** The candidate has closed four independent
adversarial-review cycles with every disposition recorded; all five reserved
decisions are ruled and incorporated verbatim; provenance is fully labeled
(42 stable commitments = 33 TRANSCRIBED / 5 CLARIFIED / 4 PROPOSED; 17
PROPOSED items total, inert until this ruling); both validators pass; and the
document claims nothing this ruling would falsify. Remaining open items
(C-2/C-3/C-4, obligations (a)–(c)) are recorded, routed, and none is a
defect *of* the candidate — deferring adoption would not advance any of them.

## 8. Ruling mechanics and owner ruling

Per the D-GOV-18/19/21 pattern: the owner rules against the
AcceptedCandidateSHA (the commit containing this exact packet), naming O-A or
O-B. The ruling is recorded verbatim in the decision record's ruling fence,
attributed against `docs/governance_harness/human_actors.md` (D-GOV-04), and
SHA-bound at publication (K-AUTH-2). If implementation must change any
approved prose, it returns for re-approval; the final applied commit
(EffectiveSHA) is recorded in the decision record.

```text
RULING: (to be recorded verbatim in the decision record; this packet is
superseded, never edited)
```

---

## Annex A — Bidirectional concordance map (PRD ↔ `docs/DIRECTIVE.md` §1)

**Scope and method (RD-3-y).** Both directions are mapped between the Rev 5
PRD (at `d9ea86f88`) and `docs/DIRECTIVE.md` **§1 "Founding Intent" as it
stands** (lines 11–21 at the same basis) — the ratified clause set, not the
RD-1 ruled wording. Uncovered items on either side are marked `TBD`
(K-INVENT-1). Statuses: **COVERED** (substance present on the other side),
**PARTIAL** (some substance present, remainder noted), **DIVERGENT**
(both sides speak; they disagree; the divergence is recorded, not resolved
here), **TBD** (no counterpart in the mapped scope). A `TBD` against
DIRECTIVE §1 often reflects only that §1 is a founding-intent summary — where
the substance lives elsewhere in ratified DIRECTIVE, the row says so
informatively; the map's scope remains §1 per RD-3-y.

### A.1 DIRECTIVE §1 → PRD

| # | DIRECTIVE §1 element (line) | PRD counterpart | Status |
|---|---|---|---|
| E1 | Genus clause: "Chirality is a governed, filesystem-native agent operating system for deliverable-heavy professional work" (:13) | ID-0 ruled two-level genus (§1.1); §1.2 genus record; §9.1 ruling. The ruled formulation **contains** "filesystem-native agent operating system" as the second level but frames the whole differently. | **DIVERGENT** — RD-1 ruled; C-1 open; closed only by obligation (a). The ratified clause remains in force as written until then. |
| E2 | Private canonical monorepo; root = release-managed shared instruction surface (`AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`) (:13) | O-1 (§5.2), same member list and release-managed character | COVERED |
| E3 | Serves working-roots under `projects/*`/`domains/*`, and — D-GOV-21 exception — the root product's own working root at the repository root (:13) | O-9 (§5.2, the single governed exception with its containment contract); ID-1a (§1.1); §6.1 ruled sequence; §7.1 downward service | COVERED |
| E4 | Also packaged as a desktop harness run against a user-selected working folder (:13) | §2.3 consuming-contexts row ("desktop-harness user-selected folders"); §7.1; §8.1 (exception not extended to desktop-selected folders) | **PARTIAL** — acknowledged as a consuming context and scope boundary; the desktop-harness *packaging itself* carries no PRD requirement → `TBD` for any future packaging commitment |
| E5 | Core insight: "if the filesystem is the database, architecture is a state-and-authority specification, not a service mesh" (:15) | N-1 (§5.1, files-as-authority with the K-DOMAIN-1 exception); OBJ-7 (file-native continuity and recoverability) | COVERED |
| E6 | Purpose: accelerate deliverable-heavy work (EPC, design-build, software, domain-knowledge, proposals) (:19) | §2.1 problem statement; §2.2 applicability; OBJ-2 (governed production end to end) | COVERED |
| E7 | Purpose: make agentic work auditable and controllable for reliance in professional, regulated, high-stakes contexts (:20) | OBJ-2 (provenance sufficient for reliance); OBJ-3 (evaluation/iteration loops close); §5.4 E-1..E-8 (evidence commitments) | COVERED |
| E8 | Purpose: keep humans in charge at every decision gate; agents handle mechanical work (:21) | ID-2 (§1.1); N-3 (§5.1); OBJ-2 (every consequential judgment human); §4.2 three human judgments; §8.3 release authority | COVERED |

### A.2 PRD → DIRECTIVE §1

| PRD element | DIRECTIVE §1 counterpart | Status |
|---|---|---|
| ID-0 ruled genus (§1.1, §9.1) | E1 | **DIVERGENT** (same divergence as A.1/E1, recorded once, counted once) |
| ID-1 dual nature — application environment **and** generative operating form (§1.1) | First half → E1 ("agent operating system", the contained level). Second half (generative operating form / self-development) | **PARTIAL** — self-development substance sits in E3's D-GOV-21 exception clause; the "generative operating form" framing itself is `TBD` in §1 *(informative: supported by ratified DIRECTIVE §2.6 as amended and D-GOV-21, outside this map's scope)* |
| ID-1a self-application independently accepted (§1.1) | E3 (the D-GOV-21 exception clause) | COVERED |
| ID-2 human judgment as governing hinge (§1.1) | E8 | COVERED |
| ID-3 pre-repo lineage (owner testimony) / ID-4 in-repo git history (§1.1) | — | **TBD** — §1 does not address lineage *(C-3 put to the owner at §6 of this packet)* |
| §2.1 problem; §2.2 applicability | E6 | COVERED |
| §2.3 users, actors, consuming contexts (incl. RD-5 staged A→B→C trajectory, §9.5) | E4 (consuming contexts, partially); the user taxonomy and staged trajectory | **PARTIAL** — trajectory and taxonomy are `TBD` in §1 *(they are PRD-original, ruled at RD-5)* |
| §3 v1 boundary [PROPOSED] | — | TBD — v1 staging is PRD-original |
| OBJ-1 discoverable normative authority | — | TBD in §1 *(informative: DIRECTIVE §Authority chain, outside §1, is the substance N-6 transcribes)* |
| OBJ-2 governed production to human issuance | E6 + E8 | COVERED |
| OBJ-3 evaluation/iteration loops close | E7 | COVERED |
| OBJ-4 self-application without self-authorization | E3 | **PARTIAL** — the exception is stated in §1; the safety contract (falsifiers, G0–G4) is `TBD` in §1 *(informative: lives in D-GOV-21 §5)* |
| OBJ-5 variant specialization with governed convergence | E3 (downward service) | **PARTIAL** — upward governed promotion is `TBD` in §1 *(PRD-original §7.2, PROPOSED)* |
| OBJ-6 coordination legibility under concurrency | — | TBD — PRD-original |
| OBJ-7 file-native continuity | E5 | COVERED |
| §4 four functional categories and generative loop | — | TBD — PRD-original framing (OWNER_DECLARED), by design not in DIRECTIVE |
| §5.1 N-1..N-9 normative basis | E5 (N-1), E8 (N-3) | **PARTIAL** — N-2, N-4..N-9 cite ratified sources outside §1 (DIRECTIVE §2/§3/§Authority chain, CONTRACT, SPEC); `TBD` within §1 only |
| §5.2 O-1..O-10 operative product | E2 (O-1), E3 (O-9) | **PARTIAL** — O-2..O-8, O-10 cite sources outside §1; `TBD` within §1 only |
| §5.3 D-1..D-16 developmental machinery (D-3 retired) | — | TBD in §1 *(informative: substance lives in governance-harness records and AGENTS.md, outside §1)* |
| §5.4 E-1..E-8 evidence | E7 | PARTIAL — the specific evidence surfaces are `TBD` in §1 |
| §6 self-application discipline and concurrency direction | E3 | PARTIAL — §6.2 discipline and §6.3 concurrency direction `TBD` in §1 |
| §7 variant specialization and governed promotion | E3 | PARTIAL — as OBJ-5 |
| §8 non-goals, falsifiers, release authority | E8 (release is a human judgment) | PARTIAL — falsifiers and non-goals `TBD` in §1 |
| §9 owner decisions (five RULED records) | — | TBD — decision mechanics are PRD/harness-original; §1 predates them |
| §10 concordance and document control | — | TBD — self-referential document mechanics |

### A.3 Reading the map

One **DIVERGENT** pair exists (E1/ID-0 — the RD-1 genus), recorded here and
closed only by obligation (a) in the implementation tranche; falsifier F5
tests that it does not become permanent and unrecorded. No other
contradiction between the PRD and DIRECTIVE §1 was found: every remaining gap
is a `TBD` — one side speaking where the other is silent — which is the
expected relationship between a founding-intent summary and a full PRD, not a
conflict. Rows marked *informative* point outside the map's ruled scope
(DIRECTIVE beyond §1, CONTRACT, D-GOV records) and carry no mapping claim.
