# D-GOV-08 — Epistemic vocabulary operationalization

Status:       RULED
HumanRuling:  Option B approved as recommended by owner (Ryan Tufts), 2026-07-01
Ruling SHA:   5f0f45c2b89909efd37b801395e857554e22f292 (publication commit, 2026-07-01)
Date:         2026-07-01
FramedBy:     seed-to-leaf consistency audit, 2026-07-01

## Decision to make

The audit found the warrant lifecycle (UNWARRANTED → CITED → REVIEWED →
AUTHENTICATED, `TYPES.md` §10.4) operationalized in zero tools and exactly one
audit agent (`AGENT_AUDIT_EPISTEMIC.md`); the `FACT` label (§10.3) defined but
used nowhere as a token; `TYPES.md` §10.5 mapping every epistemic primitive to
an enforcing invariant **except the labeling act itself**; thesis ch. 5 §5.4
misattributing labeling enforcement to R5/R6/R7; and `TYPES.md` §10.4 / thesis
ch. 6 leaning on a "CRITICAL findings" severity that no vocabulary defines
(the review-agent enum CRITICAL/MAJOR/MINOR/OBSERVATION exists only in
`SE_Design_Analysis.md` §7.3). Is the epistemic vocabulary producer-obligatory
or diagnostic, and where does the review severity enum live?

## Options

- **A:** Producer-emitted labels. Every producing agent and tool must emit
  warrant states and epistemic labels, backed by a new enforcing invariant and
  verifier checks that make the §10.5 mapping true by construction.
- **B (recommended):** The warrant ladder is an **audit-time diagnostic**
  computed over content by auditing components (`AGENT_AUDIT_EPISTEMIC` today;
  the future harness `evidence-check`), not a producer-emitted state.
  Producing agents are not required to emit warrant states; the warranting
  function is carried by the concrete mechanisms already in practice — SHA
  bindings, cited Source columns, Inspector/CHECKING attribution, K-CLAIM-1
  phrase routing. The practitioner harness's deliberate non-emission of
  warrant states is the seed-correct behavior. The `FACT` label is declared
  optional/reserved: positive assertions ride citations, not FACT tags. At
  ruling, `TYPES.md` §10.5's Status-primitive row is corrected to map to its
  actual enforcement (audit-time assessment + the K-CLAIM-1 boundary), and
  thesis ch. 5 §5.4/§5.3.4's enforcement attribution is corrected as a dated
  addition. The review-finding severity enum (CRITICAL/MAJOR/MINOR/OBSERVATION,
  `SE_Design_Analysis.md` §7.3) is registered in `TYPES.md` as a third
  distinct severity vocabulary — distinct from the §11 harness taxonomy and
  from the `docs/rubrics/AUDIT_AGENT.md` Blocker/High/Medium/Low rubric —
  resolving the undefined "CRITICAL findings" references in `TYPES.md` §10.4
  and thesis ch. 6.

## Recommendation

Option B. Basis: it matches universal practice across all audited layers (no
producing tool or agent emits warrant states today); it avoids over-claiming
enforcement that does not exist (K-CLAIM-1); and it opens no control gap,
because the warranting function is already carried by the mechanisms listed
above. Option A would invent an obligation with no existing practice behind it
and require new enforcement machinery solely to make its own claim true.

## Consequence

Re-opening this fork requires superseding this record. Any future proposal for
producer-obligatory warrant states or FACT tagging must cite and argue against
this ruling.
