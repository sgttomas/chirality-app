# TOOL POLICY — dbm-concordance-seed

## Preferred tool order

1. Read the frozen publication planning artifacts, evidence atoms, risk inventory, and any optional draft candidate input.
2. Read only the mapped KTY-local files permitted by the approved section map for the assigned sections.
3. Use direct reasoning to transform evidence atoms into typed candidates, refine draft candidates when provided, and add grounded new candidates.
4. Write exactly one scope-local candidate CSV and one scope-local QA markdown file.

## Allowed deterministic tools

### TASK-enforced

- None — this skill has no deterministic tool requirement, so the `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

None by this skill. It consumes deterministic evidence atoms and risk inventory produced upstream rather than invoking tools itself.

## Expected use of reasoning

This skill is reasoning-heavy. It must:
- interpret raw evidence atoms and risk inventory rows in light of the approved section map and publication rules,
- infer appropriate typed fields such as `AssertionDomain`, `ComparisonRule`, `ComparisonParameter`, `NormalizationHint`, `NormalizationContract`, and `Criticality` from explicit mapped content,
- propose authority / required-section ownership conservatively,
- preserve ambiguity as `NEEDS_REVIEW` rather than inventing certainty,
- distinguish genuine new candidates from duplicates or out-of-scope noise.

## Disallowed use

- No dispatching of other skills or agents.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as concordance authority. `_MEMORY.md` may be read only as non-authoritative operational context when `_STATUS.md` is read.
- No mutation of `Publication_Concordance_Register.csv`, `Publication_Concordance_Evidence_Atoms.csv`, `Publication_Concordance_Risk_Inventory.csv`, `Section_Map.csv`, or any other frozen planning artifact besides the two scope-local outputs named in the brief.
- No writing to section output folders, package folders, or KTY-local source folders.
- No section-body authoring or package-readiness judgment.

## Write boundary

The skill may write only:
- one scope-local concordance candidate CSV,
- one scope-local concordance seed QA markdown file.

Both writes must remain inside `_Publication/DBM/_Planning/` and within the exact paths named by the INIT-TASK brief.
