# Four-document consumer inventory

Status: CANDIDATE EVIDENCE — caller classification; not a migration ruling  
Observed commit: `67ba77e5107f941e6fcc7382ef467b6b018e972d`  
Observed date: 2026-07-12  
Search vocabulary: `Datasheet.md`, `Specification.md`, `Procedure.md`,
`Guidance.md`, `four-documents`, `four document`, and `four-document`

The commit-bound search returns **5,307 unique tracked paths**. The sorted
path list has SHA-256:

```text
0f1c52b4497676fc93b15b07bbe35c11614010813d87959e55574cf391c36560
```

| Top-level family | Matching paths | Classification coverage |
|---|---:|---|
| `projects/` | 2,755 | Active App Dev callers; live source content; project plans/receipts/evidence |
| `domains/` | 2,494 | Independent DOMAIN/KTY and generated decomposition/source evidence |
| `skills/` | 20 | Active callers, retirement candidates, or analogous independent schemas |
| `docs/` | 16 | Active canon, explanatory material, or historical governance evidence |
| `tools/` | 14 | Active callers, compatibility tests, retirement candidates, or analogous validators |
| `agents/` | 6 | Active instruction consumers |
| `exports/` | 1 | Derivative export material |
| `_DomainEngines/` | 1 | Historical loop evidence |

## Finding

The production kit is a typed runtime grammar, not merely four filenames.
Active consumers bind it to lifecycle transitions, TASK dispatch, semantic
enrichment, review, audits, coverage, consistency checking, and the App Dev
workspace interface. Replacement therefore requires dual-format compatibility
before any legacy caller can retire.

This inventory classifies callers; it does not direct edits to historical
records or to independent schemas that happen to reuse words such as
“Specification” or “Procedure.”

## A. Active normative and instruction consumers

| Surface | Current dependency | Stage-1 disposition |
|---|---|---|
| `docs/TYPES.md` | Defines the kit, per-file roles, lifecycle meaning, and knowledge-type/task-scope grammar | Candidate dual-format design only; exact amendment is reserved for Stage 2 |
| `docs/SPEC.md` | Makes all four files MUST, binds creation to `TASK+four-documents`, and defines `OPEN → INITIALIZED` | Candidate dual-format design only; exact amendment is reserved for Stage 2 |
| `docs/DIRECTIVE.md` | Explains the philosophical four-document correspondence | Preserve during Stage 1; propose explanatory update with exact Stage-2 canon |
| `agents/AGENT_ORCHESTRATOR.md` | Dispatches four-documents passes and ties Pass 3 to semantic readiness | Add feature-gated candidate support; legacy remains authoritative |
| `agents/AGENT_REVIEW.md` | Reads four files, derives checklist rows from `Specification.md`, and cross-checks requirements/procedure/guidance | Candidate REVIEW reads deliverable `AC-*` directly; no lifecycle transition in Stage 1 |
| `agents/AGENT_AUDIT_EPISTEMIC.md` | Audits the kit and cross-document epistemic consistency | Add candidate claim/reference graph audit while retaining legacy audit |
| `agents/AGENT_AUDIT_DECOMP.md` | Requires the standard four-file set for project/software deliverables | Add variance-aware candidate recognition |
| `agents/AGENT_EVALUATION_STRUCTURE_AUDIT.md` | Counts and requires each production filename | Add format-resolver output without silently changing legacy report meaning |
| `agents/AGENT_PREPARATION.md` | Explicitly distinguishes DOMAIN preparation from fixed project production files | Preserve the boundary; do not extend the pilot into DOMAIN/KTY |
| `agents/AGENT_PROJECT_DECOMP.md` | Describes the downstream project deliverable bundle using the four production filenames | Preserve during Stage 1; exact decomposition-output amendment is reserved for Stage 2 |

Primary citations are the named files at the observed commit. The binding
sections include `TYPES.md` “Standard Document Kit,” `SPEC.md` §§3.1–3.2,
ORCHESTRATOR setup phases, and REVIEW “Gate 1 — Completeness.”

## B. Active skill and tool consumers

| Consumer family | Files observed | Stage-1 disposition |
|---|---|---|
| Production method | `skills/four-documents/{SKILL,BRIEF_SCHEMA,QA_CHECKS,TOOL_POLICY}.md` | Retain throughout Stage 1; replacement-first retirement candidate only after all callers move |
| Semantic pipeline | `skills/semantic-matrix-build/{SKILL,BRIEF_SCHEMA}.md`; `skills/lens-register/{SKILL,BRIEF_SCHEMA,TOOL_POLICY}.md`; `skills/semantic-lensing/SKILL.md`; `tools/validation/validate_semantic_matrix.py`; `validate_semantic_pipeline_scope.py`; `validate_p3_disposition.py`; related validator tests | Add feature-gated `ScopeOfWork.md` sections/claim references; preserve legacy contracts |
| Deliverable reading and consistency | `skills/content-digest/SKILL.md`; `skills/deliverable-consistency/BRIEF_SCHEMA.md`; `tools/validation/scan_deliverable_consistency.py` | Add resolver-driven candidate input while retaining legacy behavior |
| Proposal production | `skills/proposal-format/{SKILL,BRIEF_SCHEMA}.md` | Add candidate production-format and variance inputs; retain legacy proposal behavior |
| Coverage and structure | `tools/reporting/generate_coverage_csv.py`; `tools/evaluation/count_deliverable_files.sh`; `tools/validation/check_four_documents.sh` | Version output or add fields; never silently reinterpret existing columns |
| Status/history guards | `tools/scaffolding/write_status.sh`; practitioner-harness guard tests | Preserve lifecycle authority; candidate conversion must leave `_STATUS.md` byte-identical |
| Tool catalog | `tools/EXTERNAL_TOOLS.md` | Register the new components and mark retirement only after replacement evidence |

`check_four_documents.sh` and the `four-documents` skill are **retirement
candidates**, not Stage-1 deletions. Their removal is lawful only after the
candidate format is ratified, all active callers redirect, compatibility
behavior is proven, and the corpus migration is complete.

## C. App Dev runtime/interface consumers

The active application surface includes:

- `projects/chirality-app-dev/frontend/src/lib/workspace/filesystem.ts`, whose
  deliverable contracts and knowledge buckets are filename-based;
- `projects/chirality-app-dev/frontend/src/components/shell/document-view.tsx`,
  whose document allowlist names all four files; and
- the associated API, workspace, MCP, dependency-register, scanner, and
  document-contract tests under `frontend/src/__tests__/`.

Stage 1 may add feature-gated candidate Markdown viewing and format resolution,
but the App Dev Desktop harness is not the pilot orchestration substrate and
legacy workspace behavior remains the default outside the variance.

## D. Historical evidence — preserve byte-for-byte

References in these classes describe work at their recorded source state and
must not be rewritten merely to modernize terminology:

- project `loop/LOOP_RECEIPTS.md` records;
- completed workplans and prior execution/reconciliation plans;
- `docs/governance_harness/briefs/TRB-*.md` and prior review/handoff evidence;
- immutable concordance ledgers, claim maps, wave records, and receipts;
- deliverable `_STATUS.md` histories that name `TASK+four-documents`; and
- archived or generated domain-decomposition evidence that quotes source
  material.

Their old path/line references remain valid at their pinned commits. A later
conversion receipt supplies forward traceability rather than rewriting them.

## E. Analogous independent schemas — explicitly out of scope

These consumers use some of the same ordinary-language document names but do
not implement the project deliverable kit:

- `skills/domain-documents/` and DOMAIN/KTY production surfaces;
- `skills/scope-change-packet/` and
  `tools/validation/validate_scope_change_packet.py`;
- `skills/scc-resolution-case/` and
  `tools/validation/validate_scc_resolution_case.py`; and
- drawing-extraction identifiers and other domain-specific `AC-*` tags.

They remain governed by their own schemas. Global filename or identifier
replacement would be incorrect.

## F. Explanatory and derivative references

The thesis, glossary, design analysis, public export, and generated domain
review artifacts contain explanatory or copied references. Update current
explanatory canon only after the Stage-2 exact text is ruled. Regenerate
derivative exports from accepted sources; never hand-edit them as authority.

## Identifier collision result

Short local namespaces are not globally unused. Current primary sources
already include REVIEW `AC-001` examples, proposal-format `REQ-12`, drawing
equipment `AC-*` tags, `K-VAL-*`, and `SEC-CON-*`. The candidate design must
therefore register local membership and width in `TYPES.md`, use qualified
external references such as `DEL-07-03-AC-001`, and derive validation from the
registered catalog rather than ad-hoc word-boundary regexes.

REVIEW's existing `AC-*` meaning is not renamed: the candidate design unifies
it with deliverable acceptance criteria, so REVIEW consumes the deliverable's
`AC-*` records instead of creating a second checklist namespace.

## Reproduction and limits

The initial tracked search is reproducible against the bound commit with:

```sh
git grep -Il -E \
  'Datasheet\.md|Specification\.md|Procedure\.md|Guidance\.md|four-documents|four documents|four-document' \
  67ba77e5107f941e6fcc7382ef467b6b018e972d -- \
  | sed 's#^[^:]*:##' | LC_ALL=C sort
```

Results were classified by primary path, file charter, and use context. Raw
hits inside the 616 production documents, generated DOMAIN evidence, exports,
or immutable historical records are evidence of content or provenance, not
automatically executable callers. The Stage-1 machinery lane must regenerate
this inventory after implementation and fail closure on any active caller that
is neither migrated nor expressly retained.

The top-level table is exhaustive for the 5,307-path search result. Sections
A–C enumerate the executable/normative caller groups; D classifies immutable
project/governance records; E classifies independent DOMAIN/KTY and packet/case
schemas; and F classifies explanatory and derivative material. Thus a raw hit
has a disposition even when listing each generated evidence path would obscure
rather than improve the caller graph.
