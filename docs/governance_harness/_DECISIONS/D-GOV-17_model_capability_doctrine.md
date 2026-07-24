# D-GOV-17 — Canonical model-capability doctrine and related dispositions

Status:       RULED
HumanRuling:  M1-D (owner-formulated: no durable model/capability doctrine; per-session steering supplies it; attribution evidence rules survive), M2 floor-plus-corrections (owner-selected), M3-A, M4-A — Ryan Tufts, 2026-07-18, in-session
Ruling SHA:   bind-at-publish per the D-GOV-02 caveat; the publication commit of this RULED state is the ruling SHA
Date:         2026-07-18
FramedBy:     Owner-directed architecture-evaluation remediation program (2026-07-18); D-APP-61 M3-C precedent (project-local re-home of the runtime capability convention)

## Decision to make

Four separable matters arising from the 2026-07-18 four-lens architecture
evaluation and its owner-directed remediation. Each matter is ruled
independently; unselected matters produce no change. No matter has operative
effect before its ruling.

## M1 — Canonical home for the model-capability doctrine

The only current home of model/capability doctrine is the app-dev project
agent index (`projects/chirality-app-dev/AGENTS.md`, section "Runtime
capability convention", owner-revised 2026-07-12, re-homed under D-APP-61
M3-C). The proposed canonical text is
`docs/governance_harness/_PROPOSALS/D-GOV-17/MODEL_CAPABILITY_DOCTRINE.proposed.md`
(exact bytes, SHA-pinned in the package README). It is a generic redraft: the
substance of the app-dev convention plus the capability-invariance principle,
with no project-local references.

- **M1-A (recommended): canonical section in root `AGENTS.md`.** Place the
  proposed text verbatim as a new root `AGENTS.md` section. Root `AGENTS.md`
  is the runtime doctrine home; this is runtime doctrine. The app-dev section
  is then converted, in a project-fenced follow-up, to a local binding that
  cites the canonical section and retains only its historical rescission
  note.
- **M1-B: a standalone doctrine document in the docs directory** carrying
  the proposed text verbatim, referenced from root `AGENTS.md` by one
  citation line. Same app-dev follow-up as M1-A. (Not selected; no such
  file was created.)
- **M1-C: decline.** The doctrine stays project-local; the app-dev section
  remains its sole home; this proposal package remains a non-authoritative
  record.

Risk/tradeoff: M1-A/B make the doctrine available to every project (piping
currently has no equivalent section) and give the capability-invariance
principle a citable canonical statement; M1-C avoids adding root doctrine but
leaves each future project to re-derive its own convention. Adoption by any
project other than app-dev remains that project's own act through its own
instruments; this ruling compels no project to bind.

## M2 — Instruction-surface validator boundary (codification of the F3 residual)

D-GOV-02 and `docs/CONTRACT.md` already bound machine BLOCKs to "objective
preconditions and hygiene only." The residual gap: no repo-wide rule governs
validators that check instruction, launcher, or loop surfaces, where the
PR #268 near-miss showed a hygiene check can silently become a judgment gate
that rejects owner-adopted text. D-APP-61 Appendix V corrected this for
app-dev only.

- **M2-A (recommended): adopt the following codifying paragraph** as a ruled
  caveat of this record, with a one-line pointer added beside the existing
  D-GOV-02 note in `docs/CONTRACT.md`:

  > Instruction-surface validators — validators that check instruction,
  > launcher, or loop surfaces rather than run artifacts — enforce
  > structural properties and byte parity only (tagged-block equivalence,
  > required-file presence, structural duplication of canonical mechanics),
  > never vocabulary occurrence alone. No validator finding may be
  > constructed such that content the owner has adopted or ruled is
  > mechanically rejected; where ruled text trips such a validator, the
  > validator is presumed defective and is corrected under review — never
  > the ruled text. This generalizes D-APP-61 Appendix V and extends the
  > D-GOV-02 caveat that BLOCKs apply to objective preconditions and
  > hygiene only.

- **M2-B: decline** as sufficiently covered by D-GOV-02 and project-level
  precedent.

## M3 — Scope-of-Work conversion provenance disposition (F4)

The four-document → SOW conversions carry no deliverable-local conversion
records. Central provenance exists:
`execution/_Coordination/AgentRuns/SOW-STAGE2-EXEC-20260712-01/snapshots/CONVERSION_CLOSURE/repair_integration/.../PROJECT_MANIFEST.tsv`
binds each production `ScopeOfWork.md` SHA-256 to its integration merge
commit (`74b9804cf…`), with instance evidence under the same run.

- **M3-A (recommended): rule the centralized closure record canonical.**
  The central manifest is the canonical conversion provenance; deliverable-
  local conversion records are not required; forward traceability resolves
  through the central manifest. Recorded in this decision record only — no
  file backfill.
- **M3-B: backfill** one dated conversion-pointer record per converted
  deliverable (53 files) citing the central manifest.

## M4 — MEMORY template disposition (F7a)

`docs/templates/MEMORY_TEMPLATE.md` requires title `# Memory — {{DEL-ID}}`
and five minimum sections. Actual practice is universal and identical:
53/53 deliverable `MEMORY.md` files use `# MEMORY - DEL-XX-YY` with a
`## Decisions And Evidence` section; 0/53 conform to the template. The
divergence is uniform, which makes practice the de facto convention and the
template the outlier.

- **M4-A (recommended): revise the template to codify practice** — title
  `# MEMORY - DEL-XX-YY`; required section `## Decisions And Evidence`;
  optional sections (e.g. `## Open Items`, `## Dependency Note`) permitted
  by topic-then-chronology guidance. No deliverable file changes.
- **M4-B: mass-conform** the 53 `MEMORY.md` files to the current template.
- **M4-C: defer.**

## Caveats to adopt with any ruling

- No matter has operative effect before its ruling; implementations apply
  only the ruled matters' exact staged bytes or enumerated edits.
- M1-A/M1-B implementation places the proposed doctrine bytes verbatim
  (conditional status line replaced as the ruled implementation directs) and
  is verified byte-against the SHA pinned in the package README.
- Project adoption beyond app-dev is offer-only through each project's own
  instruments; nothing here writes any project surface other than the named
  app-dev follow-up.
- A machine PASS from any validator referenced here remains structural
  evidence only, never approval (K-DOMAIN-4 analogue; D-GOV-02).

## Human Ruling

Ruled in-session by Ryan Tufts (owner, K-AUTH-1), 2026-07-18, transcribed by
the agent at owner direction. The same message rules D-APP-62 O-A; that
sentence is also transcribed in the D-APP-62 packet with the same
canonicalization.

<!-- BEGIN OWNER RULING VERBATIM -->
For M1, I want to go even further than option C to say there should be no mention of canonical models or even model capability types as all of that should be given in per-session steering instructions.  For M2 it's going to be hard to cover all possible cases in a deterministic validator, so instead of trying to anticipate them there should be an allowance for failures and then corrections as a means of finding exceptions that need to be included - perhaps, or do you see a better way?  For M3 I rule "M3-A". For M4 I rule "M4-A", and last I rule "O-A" for D-APP-62.
<!-- END OWNER RULING VERBATIM -->

Canonical ruling-text SHA-256 (UTF-8 bytes between the markers, excluding the
marker lines and the newline delimiters adjacent to them):
`411a5956d97ee94365fbfc92d931a51aa0f24870f6243208dd004247bf15e12b`

**Recorded owner selections (structured follow-up, same session,
2026-07-18)** resolving the two matters the message left open:

- M1-D scope: "Keep attribution rules (Recommended)" — all capability-tier
  and model-assignment doctrine is removed from durable instruction
  surfaces and supplied per-session; recording which model actually ran,
  and recording mid-wave substitutions, survive as minimal model-agnostic
  evidence rules.
- M2 shape: "Floor + corrections (Recommended)" — one anticipatory floor
  invariant plus the recorded-exception correction protocol.

## Ruled outcome

- **M1-D (supersedes options A–C).** No durable instruction surface carries
  canonical-model or model-capability-type doctrine; capability and model
  direction is given in per-session steering. The proposed doctrine text is
  NOT placed in any home; the package remains a historical record. The
  app-dev "Runtime capability convention" section is replaced, in a
  project-fenced follow-up, by a minimal model-agnostic **execution
  attribution** note: record which model actually ran each dispatched role
  in the governed run record (pointed to from the handoff-ledger entry;
  minimum attribution in the entry when no run record exists), and record
  any mid-wave substitution where the wave's execution is recorded. The
  2026-07-12 capability-tier prescriptions are rescinded going forward and
  survive as historical record (verbatim preserved in D-APP-61 Appendix Q2
  and Git history).
- **M2 (floor + corrections; supersedes the staged M2-A enumeration).**
  One anticipatory rule only: **a validator finding may never mechanically
  reject content the owner has adopted or ruled; where ruled text trips a
  validator, the validator is defective and is corrected under review —
  never the ruled text.** All other instruction-surface validator boundary
  cases are discovered empirically: a wrong block or wrong pass is recorded
  as a dated, supersede-never-edit exception entry (in the affected
  project's near-miss corpus, or this record's supersession chain for
  root-scoped validators) and the correction rides PR review. No exhaustive
  anticipatory enumeration is attempted.
- **M3-A.** The centralized conversion closure record
  (`SOW-STAGE2-EXEC-20260712-01`, `PROJECT_MANIFEST.tsv` binding each
  production `ScopeOfWork.md` SHA-256 to its integration merge commit) is
  the canonical provenance for the four-document → SOW conversions;
  deliverable-local conversion records are not required.
- **M4-A.** `docs/templates/MEMORY_TEMPLATE.md` is revised to codify actual
  corpus practice.

## Implementation notes (recorded at ruling execution)

- Same-branch implementation: CONTRACT.md pointer beside the D-GOV-02 note
  (M2 floor); MEMORY_TEMPLATE.md revision (M4-A); proposal-package README
  status updated to the M1-D outcome. M3-A requires no file change beyond
  this record.
- The app-dev `AGENTS.md` attribution rewrite (M1-D follow-up) is
  project-fenced and serializes behind the open corpus-remediation tranche
  on the shared app-dev surfaces; it executes as a micro-tranche with its
  own receipt after that tranche merges.
