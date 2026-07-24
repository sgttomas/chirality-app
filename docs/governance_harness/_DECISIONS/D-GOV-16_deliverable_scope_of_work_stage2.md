# D-GOV-16 — Deliverable Scope-of-Work Stage 2

Status: `RULED`
Date: 2026-07-12
HumanRuling: `APPROVED` for items 1–10 exactly as proposed — owner response,
2026-07-12: "I rule APPROVED for D-GOV-16 items 1–10 exactly as proposed.
Publish the ruling, then stop before Stage-2 implementation until a fresh
governed orchestration plan is presented from synchronized main."
Proposed SHA: `31e5efd985db4cc7b25543e11a65933979e07e4f`
Ruling SHA: `7584718aa32b112e415331736d1a8e68c12ac176`
FramedBy: D-GOV-15 Stage-1 PASS, owner checklist correction, and
RECONCILIATION proposal-eligibility handoff
AcceptedAuthority: owner approval of all ten items exactly as proposed;
publication activates those exact items, while execution remains stopped
pending a fresh governed orchestration plan from synchronized `main`

## Decision requested

The owner is asked to rule on the ten-item slate below. The recommendation is
`APPROVE ALL TEN` as one bounded Stage-2 architecture, migration, and closure
authorization. The owner may instead `AMEND`, `DEFER`, or `REJECT` any item.

No text, tool, candidate, conversion, lifecycle act, integration, retirement,
or migration authority in this proposal takes effect merely because the file
exists, validates, or is committed. Activation requires an explicit owner
ruling recorded in this decision and publication of the ruled snapshot.

### 1. Ratify the exact Scope-of-Work successor standard

Approve `chirality-deliverable-sow/v1` as the canonical PROJECT/SOFTWARE
production-contract schema and ratify only the exact successor bytes at:

`docs/governance_harness/_PROPOSALS/D-GOV-16/DELIVERABLE_SCOPE_OF_WORK_STANDARD.proposed.md`

SHA-256:
`7f74290167e3f410242bafe8bca153828a2a93e82099b8498ea6fd90eec85a6f`.

The frozen measurement standard was
`637d45769192c55ca270280c9a67d22b71afe7a1c165535cb663ce8fcaec70dc`;
the current Stage-1 candidate standard, including the owner-authorized
deterministic-checklist clarification, is
`8409bf3cebb3af947f54cca9d2e1c0b62445041bf72b81bd8aef912ce9fc0013`.
The proposed successor preserves the proven grammar while replacing pilot-only
authority language with exact transition, integration, ISSUED, failure, and
retirement contracts.

### 2. Approve exact TYPES and SPEC successor patches

Approve, but do not treat as applied until the ruled implementation tranche,
the exact patches:

- `TYPES.proposed.patch` — SHA-256
  `9614166c7db8340532d838768be2de52567862757fe0d5add3d3a90edea9d4b4`;
- `SPEC.proposed.patch` — SHA-256
  `543200af8a617e2f5673db110eef2b0a5cf742c54e70ccda8bce0cad870d4b2e`.

Both zero-context paths are under
`docs/governance_harness/_PROPOSALS/D-GOV-16/` and apply cleanly to the
current ratified files with `git apply --unidiff-zero --check`. Approval
authorizes a later controlled application to `docs/TYPES.md` and `docs/SPEC.md`;
this proposal does not apply them.

### 3. Ratify deterministic checklist ownership and REVIEW consumption

Ratify the owner-corrected boundary:

- `derive_review_checklist.py` deterministically compiles every validated
  `AC-*` in source order with exact text, qualified/source identity, candidate
  hash, and linked `VER-*` or explicit human-review method;
- invalid or unauthorized ambiguous input fails closed;
- REVIEW consumes the artifact without independent extraction, paraphrase,
  reordering, renumbering, or omission; and
- semantic assessment, findings, disposition, and lifecycle judgment remain
  in the actual human-gated REVIEW workflow.

Repeated LLM extraction is neither required evidence nor a value claim.

### 4. Adopt the single-format and lifecycle-neutral transition contract

After activation:

- new PROJECT/SOFTWARE deliverables initialize as `SOW_V1`;
- an existing unconverted complete four-document kit remains valid as
  transitional `LEGACY_FOUR_DOC`;
- both formats are allowed only as temporary `MIGRATION_DUAL` in an isolated,
  exactly authorized conversion workspace and are otherwise `AMBIGUOUS`;
- accepted deliverable state contains exactly one canonical production format;
- `INITIALIZED` becomes format-neutral: the selected production contract
  exists and validates; and
- format migration leaves `_STATUS.md` byte-identical and does not change
  lifecycle, acceptance, issuance, authentication, or professional-reliance
  status.

DOMAIN/KTY, archives, templates, fixtures, packet/case schemas, generated
trees, and analogous independent schemas remain out of scope.

### 5. Authorize bounded conversion of the remaining 144-member population

Authorize Stage-2 preparation and conversion of the 144 non-pilot members of
the frozen 154-deliverable App Dev/Piping population identified by the sizing
report and path-list digest
`b6eca2504a5d7551d96f7c0978ba6b4bc48b0e36c4d51792177fdd7a91e8df31`.

Before dispatch, ORCHESTRATOR refreshes the tracked census on synchronized
main. A changed membership, changed lifecycle population, new conflict, or
unclassified active caller produces a decision request; it does not silently
expand authority. Work proceeds in bounded package waves with disjoint writes,
calibrated concurrency or recorded sequential fallback, per-deliverable
conversion and independent verification, wave-level RECONCILIATION fan-in,
and no dual-format accepted commit.

This item does not authorize DOMAIN/KTY conversion or conversion outside the
two canonical project path families.

### 6. Approve the ISSUED handling protocol, not automatic reissuance

The frozen census contains one `ISSUED` deliverable, Piping `DEL-01-01`.
Stage 2 may prepare its representation replacement only when the source
commit, four source hashes, accepted basis, and `_STATUS.md` are bound and
independent preservation checks pass. Integration requires an explicit human
administrative representation-replacement approval that cites that evidence.

The lifecycle remains `ISSUED`; format migration does not reissue,
reauthenticate, or substantively amend the deliverable. Any semantic
difference is `CONFLICT`, aborts format migration, and proceeds only through
SCOPE_CHANGE or another human ruling.

### 7. Authorize atomic pilot replacement; prohibit as-is pilot merges

Do not merge either Stage-1 pilot branch as-is because each intentionally
contains both production formats. After the ruled canon and consumers land on
synchronized main, integrate the ten verified candidates through replacement
commits that, for each deliverable, atomically:

1. add the hash-bound `ScopeOfWork.md` content;
2. remove `Datasheet.md`, `Specification.md`, `Guidance.md`, and `Procedure.md`;
3. preserve `_STATUS.md`, lifecycle, control files, and historical evidence;
4. bind the D-GOV-15 source/pilot evidence and fresh target-base checks; and
5. pass validator, map, parity, checklist, consumer, project, containment, and
   RECONCILIATION gates.

Pilot branches and Stage-1 run packages remain derivative evidence through
the rollback window; they never become decomposition or deliverable authority.

### 8. Adopt Stage-2 acceptance and wave-release gates

No conversion wave integrates unless all applicable gates pass:

- exact ruled standard/TYPES/SPEC and migrated consumer/tool hashes;
- refreshed, classified census and active-caller inventory;
- 100% source-range disposition with no silent drop and complete merge/split
  references;
- objective/output/requirement/AC/VER/matrix closure;
- deterministic checklist output and REVIEW compatibility;
- byte-identical source/control/lifecycle inputs relative to the wave basis;
- SOW-only and retained legacy-only consumers green; missing, partial,
  ambiguous, and unauthorized dual formats fail closed;
- deterministic, bound, offline HTML where rendered;
- independent-schema, historical-evidence, archive, and out-of-scope
  containment;
- applicable root, export, agent, skill, tool, project, runtime, and
  practitioner checks; and
- per-deliverable receipts, independent verifier returns, wave audit, and an
  explicit single-format integration manifest.

Schema/mechanical, project-content/authority, preservation/containment, and
execution-substrate outcomes remain separately reported. A substrate fallback
does not become a content or schema PASS without its own evidence.

### 9. Adopt fail-closed abort and human-authorized rollback

Silent loss, invalid mapping, lifecycle/control mutation, semantic conflict,
unclassified caller, scope breach, unsupported ISSUED handling, ambiguous
accepted format, or failed required check blocks the affected deliverable and
its dependants. Independent work may continue. Preserve a FAILED handoff with
basis, evidence, blockers, and rerun requirements; do not integrate failed
candidate changes.

Before integration, rollback is deletion of the isolated candidate workspace.
After integration, rollback uses the bound pre-migration commit and replacement
manifest and requires a human-authorized, non-history-rewriting revert or
replacement act. Rollback never discards receipts or rewrites historical
evidence.

### 10. Defer legacy retirement to a separate closure ruling

Retain `four-documents`, legacy readers, legacy-only validation, and required
compatibility aliases throughout conversion and the rollback window. They may
be marked deprecated only after exact canon activation and replacement-first
caller migration. They are not retired by D-GOV-16 approval alone.

After all authorized deliverables resolve to `SOW_V1`, every active caller is
migrated or expressly retained, ISSUED handling is closed, project/root
handoffs pass, and rollback obligations are satisfied, RECONCILIATION prepares
an evidence-backed retirement/closure request. A later explicit owner act is
required to retire the legacy skill/tools/contracts and close Stage 2.

## Evidence basis

The proposal evidence index is:

`docs/governance_harness/_PROPOSALS/D-GOV-16/STAGE2_EVIDENCE_PACKAGE_INDEX.md`

SHA-256:
`8a6e48ac8247fe5147afb4208d3e7c0b4f48cb1071b1e086b4f24a2ceeded806`.

The direct findings are:

- ten candidates, 325/325 mappings, and 3,466/3,466 source lines preserved;
- all ten lifecycle/status records byte-identical and `IN_PROGRESS`;
- objective and evaluation closure PASS;
- 10/10 deterministic checklist reproduction PASS;
- legacy/SOW/missing/ambiguous, HTML, history, independent-schema,
  containment, rerun, and registered-check gates PASS;
- schema, content, and preservation PASS; conversion substrate separately
  `SUBSTRATE_FALLBACK`; native verification PASS; and
- no Stage-1 blocker, conflict, waiver, or required rerun at the named hashes
  and commits.

Stage-1 evidence proves proposal eligibility and the bounded migration method.
It does not itself prove that the 144 remaining conversions or the ISSUED
replacement have occurred.

## Required owner interface

Record one of these outcomes for each item 1–10:

- `APPROVED` — activate exactly the stated item after publication;
- `AMENDED` — state exact replacement text or conditions;
- `DEFERRED` — leave the item unauthorized and name the missing evidence; or
- `REJECTED` — close the item without authority.

Recommended response:

> I rule APPROVED for D-GOV-16 items 1–10 exactly as proposed. Publish the
> ruling, then stop before Stage-2 implementation until a fresh governed
> orchestration plan is presented from synchronized main.

If the owner does not expressly approve an item, that item remains
unauthorized. Silence, file creation, validation, a commit, or Git transport is
not approval.

## Owner ruling

The human owner ruled `APPROVED` for items 1–10 exactly as proposed on
2026-07-12 and directed:

> I rule APPROVED for D-GOV-16 items 1–10 exactly as proposed. Publish the
> ruling, then stop before Stage-2 implementation until a fresh governed
> orchestration plan is presented from synchronized main.

Publication ratifies the exact successor-standard bytes named in item 1 and
approves the exact TYPES/SPEC patch bytes named in item 2 for a later governed
implementation tranche. The patches remain unapplied. No conversion, consumer
migration, pilot replacement, lifecycle act, ISSUED representation
replacement, legacy retirement, or other Stage-2 implementation occurs in the
ruling-publication run.

The next lawful execution step is presentation of a fresh governed
orchestration plan derived from a synchronized `main` that contains this
published ruling. Approval of the ten-item architecture is not authority to
bypass that planning and synchronization gate.
