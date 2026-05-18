# TOOL POLICY — domain-source-atomize

## Preferred tool order

This skill is LLM-reasoning-only over the assigned slice — there is no deterministic tool the worker runs from inside the dispatch. The orchestrator (`DOMAIN_DECOMP`) runs `tools/decomp/*` and `tools/retrieval/*` outside the worker; this skill consumes their outputs (skeleton, dispatch plan, asset manifest) as runtime parameters.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted from `SKILL.md`. TASK does not whitelist any tool for this skill.

### Operationally invoked

None inside the worker.

The surrounding pipeline uses these deterministic tools (orchestrator side, not worker side):
- `tools/decomp/build_source_skeleton.py` (Phase 1 prep — produces `SKELETON_PATH`)
- `tools/decomp/render_source_html.py` (Phase 1 prep + Phase 2.5 — produces HTML review surface)
- `tools/decomp/build_atomization_brief.py` (Phase 2 dispatch — produces the worker's brief)
- `tools/decomp/merge_source_atomizations.py` (Phase 2 close — consumes the worker's outputs)
- `tools/decomp/merge_vocabulary_seeds.py` (Phase 2 close — consumes the worker's vocab seeds)
- `tools/source_catalog/build_source_database.py` and `tools/retrieval/build_source_index.py` (Phase 2.5 — catalog and index the merged outputs)

These are orchestrator-side, not worker-side. The worker never invokes them.

## Expected use of reasoning

The worker uses LLM reasoning to:

1. **Identify atomic units** in the assigned slice — segment prose into single-concept statements, suitable for downstream partition and Knowledge-Type assignment.
2. **Classify IN / OUT / TBD** per the SKILL contract's classification rules.
3. **Surface candidate canonical terms** for vocabulary seeding.
4. **Detect cross-source `Corrects` references** when the source text explicitly indicates an earlier-source correction (rare — only when noted).
5. **Resolve target SectionID** for each atom by matching its MD line to the skeleton's section line ranges (intersected with `TARGET_SECTION_IDS`).
6. **Compute `ContentHash` = sha1(UnitStatement)[:12]** — this is mechanical but the LLM must produce the correct hash deterministically per its own output. Downstream merge verifies; mismatches fail the merge.

## Disallowed use

- No deterministic tool invocation from inside the worker (no `Bash`, no `python3`, no shell-out).
- No writing outside `OUTPUT_LEDGER_PATH` or `OUTPUT_VOCAB_SEED_PATH`.
- No reading outside `MD_PATH[LINE_START..LINE_END]`, `SKELETON_PATH`, or `ASSET_MANIFEST_PATH`.
- No reading of other sources' MD or skeletons (cross-source reconciliation belongs to Gate 3).
- No reading of the v1.1 archive at `domains/piping-design/.archive/_Decomposition/` (fresh-decomposition path).
- No sub-agent fanout (TASK is a leaf in this dispatch pattern).
- No final stable-ID assignment (`HBA-<PREFIX>-NNNNN` is the merge tool's job).
- No cross-source `Corrects` validation (the merge tool surfaces unresolved refs).
- No vocabulary canonicalization across sources (`merge_vocabulary_seeds.py` does this).
- No invocation of retrieval indexes (Gate 3 / Gate 4 ratification, not Phase 2).

## Write boundary

Exactly two writes per invocation:

```
<OUTPUT_LEDGER_PATH>
<OUTPUT_VOCAB_SEED_PATH>
```

Both paths are absolute. Parent directories must exist; this skill does not create directories.

If a write would violate the boundary, the worker returns `RUN_STATUS=FAILED` with an explanatory note and does NOT attempt a workaround.
