---
name: dbm-concordance-verify
description: Post-synthesis cross-section semantic concordance verification for rewritten DBM package outputs.
compatibility: Chirality TASK; dispatched by DBM_PUBLISHER after deterministic package concordance and source-supersession findings exist.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - dbm-concordance-verify

## Purpose

Verify semantic concordance across the synthesized DBM section outputs after deterministic concordance checks have run. The skill reads all section bodies and assertion outputs together, interprets deterministic findings in context, and emits a package-local semantic verification report plus findings CSV.

This skill is a verifier only. It does not rewrite sections, modify the frozen concordance register, dispatch other workers, or read raw KTY-local source files.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `DBM_PUBLISHER` during Gate 6 after `check_concordance.py` and source-supersession validation have emitted package findings.

## Inputs

### Required

- `SECTIONS_ROOT`
- `CONCORDANCE_REGISTER_PATH`
- `CONCORDANCE_FINDINGS_PATH`
- `OUTPUT_VERIFICATION_PATH`
- `OUTPUT_VERIFICATION_FINDINGS_PATH`

### Optional

- `SOURCE_SUPERSESSION_FINDINGS_PATH`
- `PUBLICATION_RULES_PATH`
- `PUBLICATION_INPUT_MANIFEST`
- `PACKAGE_SNAPSHOT_PATH`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SECTIONS_ROOT` | Root containing all current `SEC-*` section output folders | **Required** | Path under `_Publication/DBM/sections/` |
| `CONCORDANCE_REGISTER_PATH` | Frozen approved concordance register | **Required** | CSV path under `_Publication/DBM/_Planning/` |
| `CONCORDANCE_FINDINGS_PATH` | Deterministic `check_concordance.py` findings | **Required** | CSV path under the package snapshot |
| `OUTPUT_VERIFICATION_PATH` | Semantic verification markdown output | **Required** | `Publication_Concordance_Verification.md` under package snapshot |
| `OUTPUT_VERIFICATION_FINDINGS_PATH` | Semantic verification findings CSV output | **Required** | `Publication_Concordance_Verification_Findings.csv` under package snapshot |
| `SOURCE_SUPERSESSION_FINDINGS_PATH` | Source-supersession findings when validation was run | unset | CSV path under package snapshot |
| `PUBLICATION_RULES_PATH` | Approved publication rules for restatement and TBD policy context | unset | Markdown path |
| `PUBLICATION_INPUT_MANIFEST` | Frozen input manifest for admitted-source context | unset | Markdown path |
| `PACKAGE_SNAPSHOT_PATH` | Immutable package snapshot root | inferred from outputs | Path under `_Publication/DBM/package/` |

## Tool usage

This is a reasoning-only semantic verification skill. It has no deterministic tool requirement and therefore omits `allowed-tools`.

Disallowed behavior:
- no writes outside `OUTPUT_VERIFICATION_PATH` and `OUTPUT_VERIFICATION_FINDINGS_PATH`,
- no modification of section outputs,
- no modification of `Publication_Concordance_Register.csv`,
- no modification of KTY-local files or planning artifacts,
- no raw KA/KTY source reads; verify only synthesized section/package outputs.

## Outputs

- `{OUTPUT_VERIFICATION_PATH}` - markdown report with one verdict per register key plus summary findings
- `{OUTPUT_VERIFICATION_FINDINGS_PATH}` - CSV findings for package readiness aggregation

## Verification observations

This skill produces semantic observations for agent/human review. It does not produce automatic readiness verdicts or blocking decisions. All observations are candidates for human disposition.

Allowed observation types:
- `CONFIRMED` - sections agree semantically
- `NORMALIZATION_ARTIFACT` - apparent mismatch is formatting/normalization only, not an engineering conflict
- `SEMANTIC_MISMATCH` - sections disagree on an engineering fact
- `IMPLICIT_CONFLICT` - section prose implies a value/state that contradicts another section
- `COVERAGE_GAP` - synthesized sections reveal a potentially material item absent from another section
- `NEEDS_HUMAN_RULING` - the verifier cannot safely determine agreement without human/domain judgment

All non-CONFIRMED observations are presented as candidate findings for disposition. None automatically block readiness.

## Method

1. **Validate inputs and write boundary.** Confirm required paths exist and output paths resolve under the package snapshot.
2. **Read synthesized section outputs.** Read all `SEC-##.md`, `SEC-##_QA.md`, `SEC-##_ASSERTIONS.csv`, and `SEC-##_ASSERTION_DISCOVERY.csv` under `SECTIONS_ROOT`.
3. **Read frozen control artifacts.** Read the concordance register, deterministic findings, and source-supersession findings when provided.
4. **Verify every register key.** For each `AssertionKey`, compare section prose, assertion rows, omission statuses, and deterministic findings in context.
5. **Interpret deterministic findings.** Distinguish real engineering disagreement from normalization artifacts.
6. **Search for semantic gaps in synthesized prose.** Identify implicit conflicts and register gaps visible in section text or discovery outputs.
7. **Emit fixed outputs.** Write the markdown report and findings CSV. Do not rewrite any input.

## Findings CSV schema

`Publication_Concordance_Verification_Findings.csv` must contain:
- `AssertionKey`
- `Verdict`
- `Blocking`
- `ImpactedSections`
- `DeterministicFindingRefs`
- `SourceSupersessionRefs`
- `EvidenceRefs`
- `Explanation`
- `RecommendedAction`

## Report structure

`Publication_Concordance_Verification.md` must contain:
1. `## Verification Summary`
2. `## Per-Key Verdicts`
3. `## Deterministic Finding Interpretation`
4. `## Implicit Conflicts`
5. `## Register Gaps`
6. `## Human Rulings Required`
