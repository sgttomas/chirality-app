# TOOL POLICY — dbm-section-publish

## Preferred tool order

1. Read the frozen publication planning artifacts.
2. Read the deterministic `SECTION_CONTEXT_PATH` packet when provided as structural context for framing, completeness checks, factual-use eligibility, open items, and QA.
3. Read only the mapped KTY-local files permitted by the approved section map.
4. Use direct reasoning to synthesize the section body and QA artifact.

## Allowed deterministic tools

### TASK-enforced

- None — this skill has no deterministic tool requirement, so the `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

None by this skill. It consumes deterministic planning outputs produced upstream rather than invoking tools itself.

## Expected use of reasoning

This skill is reasoning-heavy. It must:
- interpret mapped inputs under `MappingRole` / `ContributionScope`,
- use section context packets without promoting them to body-authoring authority except for the narrow `OVERVIEW` framing exception,
- apply publication-rule precedence,
- synthesize coherent engineering prose,
- in `FULL_ENGINEERING_DBM` mode, preserve material engineering detail and design-basis tables in DBM-native body structure,
- preserve uncertainty as `TBD`, assumptions, or conflicts rather than inventing reconciliations,
- preserve uncertainty as `TBD`, assumptions, or conflicts rather than inventing reconciliations.

## Disallowed use

- No dispatching of other skills or agents.
- No guessed discovery of inputs outside the frozen planning artifacts.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as content authority. `_MEMORY.md` may be read only as non-authoritative operational context whenever `_STATUS.md` is read.
- No modification of any `CAT-* / 1_Working / KTY-*` source files.
- No package-level assembly.
- No use of QA/export scaffolds as the default body structure in `FULL_ENGINEERING_DBM` mode.

## Write boundary

The skill may write only:
- one section body markdown file,
- one section QA markdown file.

All writes must remain inside the section-local publication folder named in the INIT-TASK brief.
