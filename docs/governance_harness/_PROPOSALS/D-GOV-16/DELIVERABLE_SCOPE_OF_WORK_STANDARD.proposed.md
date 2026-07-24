# Deliverable Scope-of-Work Standard

> **Status: RATIFIED IF AND ONLY IF D-GOV-16 IS RULED APPROVED.** Before that
> owner ruling, these exact bytes are an inactive proposal and have no
> operational or normative effect.

## 1. Purpose and boundary

`ScopeOfWork.md` is the canonical, human-readable production contract for one
PROJECT or SOFTWARE deliverable's contribution to its package objectives and
project scope. It consolidates the production content formerly held in
`Datasheet.md`, `Specification.md`, `Procedure.md`, and `Guidance.md` without
consolidating control-plane or generated state.

The following remain separate: `_STATUS.md`, `_CONTEXT.md`,
`_DEPENDENCIES.md`, `_REFERENCES.md`, `_SEMANTIC.md`, structured dependency
registers, evidence, review records, and immutable run records. DOMAIN/KTY
surfaces, archives, fixtures, templates, packet/case schemas, and analogous
independent schemas are outside this standard.

`ScopeOfWork.html` is an on-demand derivative. It is never authoritative and
must not be tracked per deliverable.

## 2. Authority, lifecycle, and migration neutrality

After D-GOV-16 activation, a newly initialized or successfully converted
PROJECT or SOFTWARE deliverable uses one valid `ScopeOfWork.md` as its sole
canonical production contract. An existing unconverted four-document kit may
remain authoritative only under the bounded legacy-transition rule in §7.

Conversion is lifecycle-neutral: it must not modify `_STATUS.md`, change a
lifecycle state, imply content acceptance, or turn proposed content into
accepted content. Substantive additions, deletions, or reinterpretations are
not format conversion. Record them as `CONFLICT` and route them through
SCOPE_CHANGE or a human ruling.

An `ISSUED` deliverable may be converted only as an explicitly human-approved
administrative representation replacement. Its four source documents,
`_STATUS.md`, accepted basis, and lifecycle state must be hash-bound before
conversion; semantic change fails the migration and proceeds only through the
governed scope-change process. Format migration alone never reissues or
reauthenticates the deliverable.

Historical evidence is not rewritten. Migration receipts provide forward
traceability from source commit and source hashes to the replacement contract.

## 3. Canonical form

The document begins with this YAML subset:

```yaml
---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-XX-YY
package_id: PKG-XX
decomposition_basis: path/to/accepted/decomposition@<commit>
project_scope_refs: [SOW-NNN]
package_objective_refs: [OBJ-NNN]
---
```

The exact `deliverable_id` and `package_id` widths are supplied by the active
project decomposition rather than inferred from examples. Both reference
lists must be non-empty. A schema marker selects a parser; it does not prove
acceptance, lifecycle, or professional reliance.

The required level-two headings, in order, are:

1. `Purpose and Objective Traceability`
2. `Deliverable Definition — Ontology`
3. `Completion and Reliance Basis — Epistemology`
4. `Production and Verification Method — Praxeology`
5. `Governing Values and Decisions — Axiology`
6. `Output and Evaluation Matrix`

Headings state the practical question first. Content must remain grounded in
accepted decomposition, sources, and decisions; philosophical labels do not
license unsupported abstraction.

## 4. Identifier grammar

The machine-readable catalog is `tools/scope_of_work/id_catalog.json`.
Validators and converters consume that catalog rather than hard-coding
independent prefix lists. Local definitions use this form:

```markdown
- **REQ-017** — The output shall ...
```

External references qualify the local identifier with the deliverable ID:
`DEL-03-02-REQ-017`. Local IDs use exactly three decimal digits and are unique
within one Scope of Work.

| Prefix | Meaning | Primary section |
|---|---|---|
| `OUT` | Expected output | Ontology |
| `CLM` | Descriptive claim | Any substantive section |
| `REQ` | Normative requirement | Epistemology |
| `AC` | Acceptance criterion | Epistemology |
| `VER` | Verification method | Praxeology |
| `AX` | Governing value, rationale, or authority constraint | Axiology |
| `TBD` | Unresolved information | Any substantive section |
| `CON` | Unresolved conflict | Any substantive section |
| `REM` | Remaining item in `_STATUS.md` | `_STATUS.md` only |

The registered deterministic checklist tool consumes the validated
deliverable `AC-*` definitions and emits them in source order with exact text,
qualified identity, candidate hash and source location, and matrix-linked
`VER-*` records or explicit `HUMAN_REVIEW: <method>`. REVIEW consumes that
artifact; it must not mint a second acceptance-criterion namespace,
re-extract, paraphrase, reorder, renumber, or silently omit criteria. Agent or
human judgment begins only in an actual human-gated review and remains
distinct from checklist compilation.

Every `OUT-*` cites at least one project-scope and package-objective reference.
Every `AC-*` cites at least one `VER-*` or uses the matrix syntax
`HUMAN_REVIEW: <method>`. Every declared `OUT-*`, `AC-*`, and `VER-*` is
consumed by at least one matrix row; orphan evaluation definitions fail
validation.

## 5. Output and evaluation matrix

The matrix binds expected production to evaluation intent. Its required
columns are:

```text
Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation
```

Tests implement verification methods and produce evidence; tests do not
silently define scope or acceptance criteria. `_STATUS.md ## Remaining` is the
current delta against this stable target and references qualified
Scope-of-Work IDs.

## 6. Migration traceability

Migration dispositions are `PRESERVED`, `MERGED`, `SPLIT`, `SUPERSEDED`,
`DEFERRED`, and `CONFLICT`. They describe migration handling only; they are
not epistemic labels, lifecycle states, or human rulings.

Every converted source range maps to one or more target IDs and records the
source file, source line range, source SHA-256, target document SHA-256, and
disposition. `MERGED` and `SPLIT` preserve every contributing source
reference. No omitted content is inferred to be unimportant.

Conversion occurs in an isolated branch or worktree. A verified replacement
integration adds `ScopeOfWork.md` and removes the four legacy production files
atomically, preserving source blobs in Git and binding the migration receipt.
An as-is dual-format conversion branch is never merged into an accepted
baseline.

## 7. Format resolution and transition

| Files present | Interpretation |
|---|---|
| Four valid legacy production documents only | `LEGACY_FOUR_DOC`; transitional compatibility for an existing unconverted deliverable |
| One valid `ScopeOfWork.md` only | `SOW_V1`; canonical production contract |
| Both complete formats | `MIGRATION_DUAL` only in an isolated, explicitly authorized conversion workspace; otherwise `AMBIGUOUS` and invalid |
| Partial legacy kit, invalid `ScopeOfWork.md`, or neither at or beyond `INITIALIZED` | `INVALID` |

An accepted deliverable state contains exactly one canonical production
format. New deliverables use `SOW_V1`. Legacy-only deliverables remain valid
during the authorized transition window but must not receive new
four-document production initialization after activation.

The `four-documents` skill and legacy readers remain supported compatibility
surfaces until all authorized conversions, caller migrations, audit closure,
and rollback windows complete. Retirement requires a later evidence-backed
owner act; D-GOV-16 activation alone does not delete them.

## 8. Lifecycle integration

`INITIALIZED` means that the deliverable's selected production contract exists
and validates for its current format. The lifecycle sequence and human gates
do not change:

```text
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

Format migration preserves the current lifecycle state. It is neither a
promotion nor a review outcome. `_STATUS.md` remains the sole lifecycle
authority.

## 9. HTML derivative

The renderer accepts only a validated `ScopeOfWork.md`. Its UTF-8 output is
deterministic for identical source bytes and renderer version, contains the
canonical source SHA-256 and schema/renderer versions, escapes source text,
and contains no scripts, external resources, network dependencies, forms, or
authority claims.

## 10. Acceptance and failure

A conversion is not acceptable unless all source ranges are dispositioned,
internal IDs and references resolve, objective mappings exist, the evaluation
matrix closes, lifecycle bytes are unchanged, and independent parity,
checklist, and applicable consumer checks pass. Silent claim loss, unresolved
authority ambiguity, `_STATUS.md` mutation, lifecycle drift, or use outside
the authorized migration scope fails closed.

Checklist compilation is read-only and idempotent. Identical validated source
bytes and the same accepted format basis produce byte-identical
`chirality-review-checklist/v1` JSON. Invalid candidates, legacy-only input,
or dual-format ambiguity without an exact accepted migration authority fail
without emitting a new output artifact.

Failed conversion changes are not integrated. Preserve a failed handoff with
evidence, blockers, and rerun requirements; restore or retain the last
accepted single-format baseline. Rollback of an integrated replacement uses
the bound pre-migration commit and is a human-authorized Git/integration act,
not an agent-inferred content decision.
