# TOOL POLICY — dbm-section-publish

## Preferred tool order

1. Read the frozen publication planning artifacts.
2. Read only the mapped KTY-local files permitted by the approved section map.
3. Use direct reasoning to synthesize the section body, QA artifact, and assertions CSV.

## Allowed deterministic tools

### TASK-enforced

- None — this skill has no deterministic tool requirement, so the `allowed-tools` frontmatter field is intentionally omitted.

### Operationally invoked

None by this skill. It consumes deterministic planning outputs produced upstream rather than invoking tools itself.

## Expected use of reasoning

This skill is reasoning-heavy. It must:
- interpret mapped inputs under `MappingRole` / `ContributionScope`,
- apply publication-rule precedence,
- synthesize coherent engineering prose,
- preserve uncertainty as `TBD`, assumptions, or conflicts rather than inventing reconciliations,
- emit structured assertion rows suitable for later deterministic concordance checks.

## Disallowed use

- No dispatching of other skills or agents.
- No guessed discovery of inputs outside the frozen planning artifacts.
- No use of `_Aggregation/*`, `_Coordination/*`, `_Evaluation/*`, `_Reconciliation/*`, `_MEMORY.md`, or `_SEMANTIC.md` as content authority.
- No modification of any `CAT-* / 1_Working / KTY-*` source files.
- No package-level assembly or concordance checking.

## Write boundary

The skill may write only:
- one section body markdown file,
- one section QA markdown file,
- one section assertions CSV file.

All writes must remain inside the section-local publication folder named in the INIT-TASK brief.
