# OD7-G1 — Program Record Closeout Candidates

> **Status: CANDIDATE — NOT APPROVED OR APPLIED.** This package and the two
> linked project-local proposal packages are proposals. They bind nothing
> (K-AUTH-1). Preparation, validation, hashing, or later Git transport is not
> owner approval.

| Field | Value |
|---|---|
| Candidate batch | `OD7-G1` |
| Candidate basis | `main@fb16e32ed60bb4f384cf1e07a83c4a14ff63bbae` |
| Accepted derivative input | `execution/_Evaluation/CHIRALITY_PROGRAM_OD7_MAINTENANCE_2026-07-26_EF164C20/` |
| Prepared by | `HELPS_HUMANS` (Agent 1), managed by `HELP_HUMAN` |
| Artifact class | proposal package; non-authoritative |
| Date | 2026-07-27 |

## 1. Objective

Return exact candidate bytes for the six bounded OD7-G1 record and
coordination closeouts. No live decision, register, receipt, pointer, notice,
decomposition, hold, product, or existing authoritative file is changed by
this staging package.

The current-basis rescan found one material correction to the accepted
evaluation's proposed Piping pointer target: SCA-007 establishes decomposition
revision `0.10`, not `0.9`. Candidate C04 therefore proposes
`_LATEST.md` `0.6 → 0.10` and separately returns the missed
`SOFTWARE_DECOMP.md` frontmatter `0.9 → 0.10` residue for explicit owner
approval. Neither edit is silently absorbed.

## 2. Exact candidates

| Candidate | Owning loop | Proposed effect | Exact candidate source |
|---|---|---|---|
| `OD7-G1-C01` | Root | Backfill D-GOV-27 `EffectiveSHA` to PR #355 merge `bfb21d11a955b98eb0a4885cc7777ad8df27fd75`, with one Root receipt and one tranche manifest | `ROOT_DGOV27_EFFECTIVE_SHA.patch`, `PROPOSED_ROOT_RECEIPT_53.md`, `PROPOSED_ROOT_MANIFEST_ROOT-OD7-G1-20260727.yaml` |
| `OD7-G1-C02` | App | Add a D-APP-75 effective-state closeout for PR #363 merge `18e5dda568689daadaa05aff65bd4b810489409b` and reconcile only its register row | App proposal package |
| `OD7-G1-C03` | Piping | Backfill D-30's publication SHA to `712df44816cf5253223b449fec0f10b48abd585c` | Piping proposal package |
| `OD7-G1-C04` | Piping | Correct decomposition currency to accepted SCA-007 revision `0.10`: `_LATEST` `0.6 → 0.10` plus separately presented frontmatter `0.9 → 0.10` | Piping proposal package |
| `OD7-G1-C05` | Root issuer / App receiver | Deliver an additive correction withdrawing only the false D-GOV-26 Root-SPEC/CONTRACT detector and repin claim; record `NO_LOCAL_CORPUS_CHANGE` in App | `PROPOSED_NOTICE_D-GOV-26_DETECTOR_CLAIM_CORRECTION_2026-07-27.md` plus App proposal package |
| `OD7-G1-C06` | Root issuer / Piping receiver | Deliver a factual D-30 mismatch notice; authorize no repin, successor, or Piping client scope | Piping proposal package |

`BATCH_CANDIDATE_MANIFEST.csv` is the exact cross-package write map.

## 3. Candidate-ID discipline

The current scan observes:

- next Root decision ID candidate: `D-GOV-29`;
- next App decision ID candidate: `D-APP-76`;
- next Piping decision ID candidate: `D-58`;
- next Piping decomposition decision-log ID candidate: `DEC-091`;
- next Root/App/Piping receipt candidates: `Receipt 53`, `Receipt-92`, and
  `Receipt-76`.

None is reserved or made authoritative here. C01–C06 do not require a new
decision ID. The three receipt identifiers are used only in exact candidate
fragments and must be rescanned immediately before application; a collision
returns the affected loop package for a refreshed candidate and owner review.
`D-58` and `DEC-091` remain available, if still free, for later substantive
Piping retire-or-replace work—not this batch.

## 4. Direct-write boundaries

If and only if the owner approves exact candidate bytes, the smallest
application surfaces are those in `BATCH_CANDIDATE_MANIFEST.csv`. In
particular:

- historical D-GOV-26 and D-30 coordination/decision substance remains
  byte-identical except for the single allowed D-30 publication-SHA field;
- D-APP-75's ruled record and frozen APP-HOLD-1 proposal remain byte-identical;
- no D-30 or D-APP-48 JSON is repinned;
- App corpus membership, resolver behavior, and hashes do not change;
- Piping remains a non-client of the Root runtime;
- no new package, deliverable, dependency, lifecycle state, scope item,
  runtime behavior, product code, or implementation authority is created;
- no SCOPE_CHANGE gate is approved or bypassed; and
- acknowledgement is tracked but is not a closure veto for the issuing loop.

The public export currently pins D-GOV-27. C01's proposed Root tranche
manifest records an explicit derivative-regeneration deferral because the
change is identity metadata only. A later export must regenerate from the
then-current source; the deferral is not a claim that the derivative remains
byte-current.

## 5. Authority routes

1. `HELPS_HUMANS` presents this exact batch and its per-loop hash manifests.
2. The owner may approve all six, approve a named subset, return amendments,
   or defer. A subset that invalidates a combined receipt or manifest returns
   that loop package for a narrowed exact candidate; nothing is inferred.
3. Approved Root, App, and Piping writes execute through their owning
   closeouts and `CHANGE`; Git records integration but does not create
   authority.
4. Any execution-time rescan disagreement, changed source byte, ID collision,
   ancestry failure, or failed validation stops application and returns a
   refreshed candidate.

## 6. Rollback

Before merge, revert only the proposed application paths if any validation
fails. After merge, append a superseding closeout where required; do not
rewrite accepted receipts or historical notices. Reverting the D-APP-75
display closeout cannot deactivate the already merged hold. Reverting a
coordination notice cannot undo the underlying historical facts.

## 7. Owner gate

DecisionID: `OD7-G1-EXACT-CANDIDATE-BATCH`
RequestedBy: `HELPS_HUMANS` through `HELP_HUMAN`
Question: Approve all or a named subset of C01–C06 for application through
their owning closeouts?
Recommendation: approve all six, including C04's rescan-corrected `0.10`
target and separately visible frontmatter repair. They close deterministic
record/navigation debt without broadening product scope or inventing
provenance.
DownstreamBlocked: application of C01–C06 only; later OD7 gates remain
independent.
