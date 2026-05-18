# QA CHECKS — dbm-section-publish

## Minimum output validity checks

The run is valid only when all of the following are true:

1. Both required outputs exist:
   - section body markdown,
   - section QA markdown.
2. The section body reads as coherent engineering prose under `Publication_Rules.md` rather than as a concatenated artifact dump.
3. The section body reflects current post-SCA state when mapped sources require a state choice.
4. Unsupported claims are surfaced as `TBD`, assumptions, or conflicts rather than silently guessed.
5. The section body does not use detailed inline source citations; detailed provenance belongs in QA and the package trace appendix.
6. The section QA artifact uses the required stable block structure in the required order.
7. All writes stayed inside the approved section-local publication folder.
8. When `SECTION_CONTEXT_PATH` is provided, the section QA records whether structural context was consumed and flags any mapped `PRIMARY` KTY that produced no material body contribution.
13. Body prose uses only reader-facing epistemic labels (`TBD`, `to be confirmed`, `assumed`); original governance-state labels remain in QA.
14. In `FULL_ENGINEERING_DBM` mode, the body is usable for core engineering design basis without reopening KA files for material values, capacities, configurations, interfaces, assumptions, TBDs, or design constraints.
15. In `FULL_ENGINEERING_DBM` mode, the body uses DBM-native engineering structure; mapped assertions, controlled assertions, raw caveat dumps, file-path inventories, and trace scaffolds do not stand in for the section body.
16. Design-basis tables are included, consolidated, split, or explicitly omitted/deferred with rationale. Trace-only treatment is not used for body-worthy design-basis tables.
17. `PRIMARY` KTYs with multiple material facts, tables, or open requirements are not collapsed to token mentions or one generic sentence.

## Required QA artifact structure

`SEC-##_QA.md` must contain these H2 headings in this order:

1. `## Section Summary`
2. `## Coverage Table`
3. `## Design Basis Content Coverage`
4. `## Table Treatment`
5. `## Section Adequacy Findings`
6. `## Readiness Observations`
7. `## Conflict Register`
8. `## Terminology Notes`
9. `## Gap / TBD Register`
10. `## Amendment Notes`

Content expectations by block:
- `Coverage Table` records mapped KTYs/KAs consumed plus mapped inputs skipped and why.
- `Coverage Table` must identify `PRIMARY` KTYs that materially contributed to body prose and any `PRIMARY` KTYs with zero visible body contribution.
- `Design Basis Content Coverage` records applicable content classes as `INCLUDED`, `OMITTED_WITH_RATIONALE`, `DEFERRED_UPSTREAM_MISSING`, or `NOT_APPLICABLE`.
- `Table Treatment` records design-basis table handling as `INCLUDED`, `CONSOLIDATED`, `SPLIT`, `OMITTED_WITH_RATIONALE`, `TRACE_ONLY`, `DEFERRED_UPSTREAM_MISSING`, or `NONE_APPLICABLE`.
- `Section Adequacy Findings` records fixed finding codes when present: `UNDERDEVELOPED_SECTION`, `UNJUSTIFIED_TABLE_OMISSION`, `PRIMARY_KTY_COLLAPSED`, `MISSING_DESIGN_BASIS_CLASS`, `QA_SCAFFOLD_BODY_LEAKAGE`, `NON_STANDALONE_CORE_BASIS`.
- `Readiness Observations` records KTY readiness issues.
- `Conflict Register` records contradictory values/states and both mapped positions.
- `Gap / TBD Register` preserves distinctions such as human authority rulings, `TBD`, `ASSUMPTION`, `DEFERRED_CONFIRMATION`, external responsibility, and decomposition/publication gaps.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- required runtime overrides are missing,
- mapped `PRIMARY` or `CONFLICTING` inputs are below readiness threshold,
- the section input set exceeds `MAX_KA_FILES` or the approved size limit,
- output paths fall outside the approved section-local publication folder.

Use `FAILED` when:
- a required output cannot be written despite valid inputs,
- an internal run error prevents the stable outputs from being emitted.

Even on non-blocking runs, QA must surface:
- skipped supporting inputs,
- terminology normalizations,
- remaining conflicts,
- remaining `TBD` / assumption / deferred-confirmation items,
- any reliance on amendment notes or decision-log references,
- any supersession note intentionally included in body prose under the body-note heuristic,
- any context-packet factual-use override,
- any content-adequacy fixed finding code,
- any design-basis table omitted, consolidated, split, or deferred,
- any design-basis table omitted, consolidated, split, or deferred.
