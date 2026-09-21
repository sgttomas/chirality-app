# D-GOV-28 — Root Runtime Stewardship PRD Amendment

> **Status: CANDIDATE — NOT RULED.** This packet and every file beside it are
> proposals. They bind nothing (K-AUTH-1). File creation, validation, commit,
> Git transport, review, or a passing concordance report is not adoption.

| Field | Value |
|---|---|
| Provisional decision ID | D-GOV-28 — verified next-free at `main@918bb48b8fcee66c031d0d6d4040a46089f96067` |
| Accepted current PRD | `docs/PRD_ROOT.md`, Rev 5 adopted by D-GOV-22 |
| Candidate | `PRD_ROOT_REV6_CANDIDATE.md` |
| Root authority | D-GOV-20 |
| Coordinating counterpart | D-T0-23 — named for coordination only; not incorporated as Root authority |
| AcceptedCandidateSHA | `NOT_ASSIGNED_UNTIL_COMMIT` |
| Record convention | exact-candidate-SHA; supersede-never-edit after ruling |
| Date | 2026-07-26 |

## 1. Decision context

The accepted program-architecture evaluation found a narrow defect: generic
runtime ownership is ruled at Root, but the accepted Root PRD does not carry a
continuing stewardship commitment from which a stable Root scope carrier,
write locus, conformance path, migration path, and regression obligation can
be derived. The owner selected OD-2 Option A for preparation:

1. reaffirm Root ownership of generic runtime semantics, with App and PEC as
   clients;
2. stage a minimal Root PRD amendment; and
3. open Root SCOPE_CHANGE intake only after the evidence-only PR #360 merged.

That direction authorizes this candidate and intake preparation. It does not
adopt PRD bytes and does not pre-approve any SCOPE_CHANGE gate.

For this remediation only, OD-3 calibrates BLOCK to a named reliance or
lifecycle claim; it does not automatically attach BLOCK to the whole product.
This calibration is decision context, not a proposed permanent PRD rule.

## 2. Exact candidate change

The full Rev 6 candidate is derived from the accepted Rev 5 product basis and
does four bounded things:

1. integrates D-GOV-27's already ruled O-1 instruction-surface enumeration
   by copying the two relied SPEC §0.2.1 sentences byte-for-byte;
2. adds one new stable requirement, O-11, for continuing Root stewardship of
   consequential generic-runtime work and preservation of all D-GOV-20
   authority, security, residency, exclusion, and implementation-gate
   boundaries;
3. copies all ten D-GOV-20 §Ruled architecture statements byte-for-byte into
   a clearly marked TRANSCRIBED block, so credentials, sessions, adapters,
   transport, state, registration, hierarchy, pilot, and export boundaries
   are not repartitioned by paraphrase; and
4. reconciles Rev 6 status, provenance counts, proposed-item inventory, and
   amendment mechanics.

O-11 supports OBJ-1, OBJ-2, OBJ-4, and OBJ-7. That relationship informs later
decomposition; this packet invents no package, deliverable, estimate,
dependency edge, or write target.

## 3. Boundary discipline

D-GOV-20 is the Root authority. The candidate quotes the ruled architecture
verbatim. It does not create a new credential, session, adapter, fallback, or
client-ownership partition.

D-T0-23 is a coordinating Tier-0 counterpart. This packet does not incorporate
it by reference into the Root PRD and therefore does not create a silent
cross-tier authority pin. Any Tier-0 maintenance remains separately governed.

Facts and behaviors not settled by D-GOV-20 are carried in `OPEN_ITEMS.csv`
with stable identifiers and OPEN or PROPOSED status. They are not drafted into
the PRD as assertions.

## 4. Decision options

### O-A — Adopt the exact Rev 6 candidate

Adopt the exact bytes named by the candidate commit. O-11 becomes a product
requirement. The existing Root SCOPE_CHANGE session may then proceed from
Gate 1 to its next explicit owner gate, using the adopted PRD as its basis.

**Effect limit:** adoption does not itself amend decomposition, create a
deliverable or write locus, approve a SCOPE_CHANGE gate, change App or PEC,
repin a contract, or authorize implementation.

### O-B — Return for revision

Retain Rev 5 as the accepted PRD and direct exact candidate changes. D-GOV-28
remains a proposal. Root SCOPE_CHANGE stays at Gate 1 with all actions marked
contingent on PRD adoption.

### O-C — Decline or defer

Retain Rev 5. A deferral is lawful only as a separately recorded interim
instrument with a named carrier, assigned continuing-runtime duties, and an
expiry or return gate. Under that branch, any App boundary correction quotes
D-GOV-20 plus the deferral record; it does not cite unadopted Rev 6 text.

## 5. Recommendation

Recommend **O-A**, subject to owner review of the exact committed candidate and
the passing deterministic concordance artifact. The generic runtime is live
and has ruled security and conformance duties; a continuing Root stewardship
requirement is the smallest product-level correction that allows those duties
to be decomposed without inventing them inside SCOPE_CHANGE.

The recommendation is not a ruling. O-B and O-C remain fully available.

## 6. Deterministic concordance gate

Run from repository root:

```sh
python3 docs/governance_harness/_PROPOSALS/D-GOV-28_root_runtime_stewardship/validate_transcriptions.py \
  --repo-root . \
  --output docs/governance_harness/_PROPOSALS/D-GOV-28_root_runtime_stewardship/CONCORDANCE_REPORT.json
```

The validator:

- reads `TRANSCRIPTION_SPEC.json`;
- reads each source from the declared Git basis with `git show`, verifies its
  expected full-file SHA-256, and does not substitute mutable working-tree
  source bytes;
- compares exact UTF-8 byte sequences;
- requires every exact-source sentence introduced or textually changed by the
  Rev 6 amendment and labeled TRANSCRIBED exactly once in its ruled source and
  exactly once in the candidate: two O-1 sentences from SPEC and ten
  shared-runtime architecture statements from D-GOV-20;
- states explicitly that inherited Rev 5 provenance-labeled synthesis is
  outside this verbatim-transcription check rather than claiming it was
  retroactively converted into quotation;
- requires the O-11 candidate marker exactly once;
- requires every declared uncovered seam in `OPEN_ITEMS.csv`;
- permits only OPEN or PROPOSED status and rejects literal `TBD` in that
  register; and
- exits nonzero on any mismatch.

A PASS is structural evidence only. It does not adopt the candidate.

## 7. Ruling mechanics

After the proposal is committed, the owner may rule O-A, O-B, or O-C against
the exact commit containing this packet and its candidate. An O-A ruling is
recorded verbatim in a new D-GOV-28 decision record, with distinct candidate,
publication, and effective SHAs. Any prose change after exact-candidate
approval returns for re-acceptance.

No authoritative file is changed in this staging tranche.
