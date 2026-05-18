# BRIEF SCHEMA — domain-source-atomize

This is the dispatch contract. The DOMAIN_DECOMP orchestrator composes one INIT-TASK brief per dispatch unit (typically via `tools/decomp/build_atomization_brief.py`) following this schema.

## INIT-TASK brief shape (required fields)

```
PURPOSE: Atomize lines <LINE_START>..<LINE_END> of <SOURCE_NAME> (dispatch unit <DISPATCH_UNIT_ID>; ~<EST_TOKENS> estimated MD tokens; <N> target sections)
RequestedBy: DOMAIN_DECOMP
ActingSurface: TASK+domain-source-atomize

ScopePath: <quarantined work folder; typically OUTPUT_LEDGER_PATH.parent>
TaskSkill: domain-source-atomize

AllowedWriteTargets:
  - "<OUTPUT_LEDGER_PATH>"
  - "<OUTPUT_VOCAB_SEED_PATH>"

RuntimeOverrides:
  SOURCE_NAME: <doc_stem>
  SOURCE_PREFIX: <short prefix>
  DISPATCH_UNIT_ID: UNIT-<prefix>-NNNN
  MD_PATH: <absolute path to <book>.md>
  LINE_START: <integer>
  LINE_END: <integer>
  SKELETON_PATH: <absolute path to <book>_skeleton.json>
  ASSET_MANIFEST_PATH: <absolute path to <book>_assets_manifest.json>
  OUTPUT_LEDGER_PATH: <absolute path; per-unit atom CSV>
  OUTPUT_VOCAB_SEED_PATH: <absolute path; per-unit vocab CSV>
  TARGET_SECTION_IDS:
    - SEC-<prefix>-NNNN
    - SEC-<prefix>-NNNN
    ...

CustomInstructions:
  - Read ONLY lines LINE_START..LINE_END of MD_PATH. Atoms whose SourceRef line falls outside that range MUST NOT be emitted.
  - Every emitted atom MUST map to one of the TARGET_SECTION_IDS (its SectionID column).
  - LocalSeq is monotonic across atoms in the same dispatch unit. Final stable IDs are NOT assigned here — the merge step assigns HBA-<PREFIX>-NNNNN.
  - ContentHash MUST be sha1(UnitStatement)[:12]; this column is load-bearing for dedup and HTML cross-reference.
  - SourceRef is dual: `<book>.md:L####` (the MD line) and `<book>.html#anchor` (the HTML anchor; SectionID when no finer applies).
  - InOutStatus ∈ {IN, OUT, TBD}. Default IN for substantive technical statements; OUT for boilerplate; TBD for ambiguous content.
  - Do not invent (AOP-08).
  - Write ONLY to OUTPUT_LEDGER_PATH and OUTPUT_VOCAB_SEED_PATH.

ExpectedOutputs:
  - <OUTPUT_LEDGER_PATH>
  - <OUTPUT_VOCAB_SEED_PATH>
```

## Required `RuntimeOverrides` fields

| Field | Type | Example | Notes |
|---|---|---|---|
| `SOURCE_NAME` | string | `Pipe-Stress-Engineering` | doc_stem |
| `SOURCE_PREFIX` | string | `PSE` | used downstream for ID assignment |
| `DISPATCH_UNIT_ID` | string | `UNIT-PSE-0007` | dispatch unit identifier from the plan |
| `MD_PATH` | absolute path | `/.../Pipe-Stress-Engineering.md` | the assembled source MD |
| `LINE_START` | integer ≥ 1 | `3815` | inclusive lower bound |
| `LINE_END` | integer ≥ `LINE_START` | `4488` | inclusive upper bound |
| `TARGET_SECTION_IDS` | list[string] | `[SEC-PSE-0156, SEC-PSE-0157, …]` | every atom must map to one |
| `SKELETON_PATH` | absolute path | `/.../Pipe-Stress-Engineering_skeleton.json` | section metadata reference |
| `ASSET_MANIFEST_PATH` | absolute path | `/.../Pipe-Stress-Engineering_assets_manifest.json` | asset metadata reference |
| `OUTPUT_LEDGER_PATH` | absolute path | `/.../PSE_UNIT-PSE-0007_atoms.csv` | per-unit atom CSV destination |
| `OUTPUT_VOCAB_SEED_PATH` | absolute path | `/.../PSE_UNIT-PSE-0007_vocab.csv` | per-unit vocab seed CSV destination |

## Optional `RuntimeOverrides` fields

| Field | Type | Example | Notes |
|---|---|---|---|
| `MAX_ATOMS` | positive integer | `200` | smoke-test bound; halt when reached |
| `SOURCE_HTML_PATH` | string | `audit/Pipe-Stress-Engineering.html` | when known, included in dual SourceRefs |

## `AllowedWriteTargets`

Exactly two entries:

```
- "<OUTPUT_LEDGER_PATH>"
- "<OUTPUT_VOCAB_SEED_PATH>"
```

`AllowedWriteTargets` is the TASK-shell write-quarantine seal. The skill cannot write anywhere else.

## Recommended `CustomInstructions` content

`CustomInstructions` carry run-specific reinforcement; they do not replace skill hydration. The contract in `SKILL.md` remains authoritative. The orchestrator's brief-builder (`tools/decomp/build_atomization_brief.py`) includes a defensive set of one-line reminders re-stating the constraints above — line-range discipline, target-section discipline, ContentHash rule, dual-SourceRef rule, IN/OUT/TBD enum, the no-invention rule, and the write-boundary rule.

When a particular dispatch surfaces a recurrent worker error (e.g., chronic over-atomization in dense reference sections, or chronic misclassification of TBD vs OUT), the orchestrator MAY add one or two run-specific reminders. Do not duplicate the skill contract.

## Brief-builder

Use `tools/decomp/build_atomization_brief.py` to render a valid INIT-TASK brief from a `<book>_dispatch_plan.json` plus a `unit_id`. This is the deterministic source of truth for the brief shape; hand-composed briefs SHOULD be reserved for emergencies.

## Example invocation (manual)

```text
$ python3 tools/decomp/build_atomization_brief.py \
    --dispatch-plan path/to/Pipe-Stress-Engineering_dispatch_plan.json \
    --unit-id UNIT-PSE-0007 \
    --md path/to/Pipe-Stress-Engineering.md \
    --skeleton path/to/Pipe-Stress-Engineering_skeleton.json \
    --asset-manifest path/to/Pipe-Stress-Engineering_assets_manifest.json \
    --output-ledger-path /work/PSE/PSE_UNIT-PSE-0007_atoms.csv \
    --output-vocab-seed-path /work/PSE/PSE_UNIT-PSE-0007_vocab.csv
```

The orchestrator pipes this stdout into the TASK dispatch surface.
