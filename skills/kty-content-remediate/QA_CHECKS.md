# kty-content-remediate - QA Checks

Minimum checks for a valid run.

## Non-negotiable invariants

| Invariant | Requirement |
|---|---|
| One KTY per run | `KTY_PATH` resolves to exactly one KTY folder |
| Supported mode | `MODE` is `RETIRE_KTY`, `VERIFY_KTY`, or `EMIT_DISPOSITION` |
| One-writer rule | `domain-documents` remains the only writer of active `Scoping.md` and `KA-*.md` factual content |
| No active factual edits | This skill never modifies active factual content; `RETIRE_KTY` writes only tombstone stubs after archive |
| No metadata edits | `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md` / `MEMORY.md`, and `_SEMANTIC.md` are untouched |
| No manifest edits | `KTY_Remediation_Manifest.csv` is not updated by this skill |
| Structured authority only | Supersession decisions come from structured SCA artifacts and `Supersession_Map.csv` |
| No prose supersession inference | Do not infer supersessions from SCA prose |
| Archive non-authority | `.Archive/` is history/evidence only, not factual authority |
| .Archive/ scanner exclusion | `.Archive/` scanner exclusion is recorded and respected |

## Input validation

| Check | Validation |
|---|---|
| KTY path exists | `KTY_PATH` exists and is readable |
| SCA snapshot exists | `SCA_SNAPSHOT_PATH` exists and contains accepted SCOPE_CHANGE artifacts |
| Decomposition authority exists | `DECOMPOSITION_REF` resolves to admitted decomposition truth |
| Evidence output authorized | `REVIEW_OUTPUT_PATH` and optional `DISPOSITION_EVIDENCE_PATH` are in `AllowedWriteTargets` |
| Factual authority present | Factual checks have `SUPERSESSION_MAP_PATH` and `SOURCE_ACTION_REF` |
| No sibling scan | The run did not inspect unrelated KTY folders |

## RETIRE_KTY checks

| Check | Validation |
|---|---|
| Active file enumeration | Only root-level `Scoping.md` and `KA-*.md` were considered active candidates |
| Archive created | `{KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/` exists when files were retired |
| Files preserved | Every retired active-looking file has an archived copy |
| Tombstone stubs | Every retired original path begins with `[RETIRED]` and includes amendment id, source action ref, archive path, and non-authority statement |
| No content rewrite | No regenerated factual sections were written by this skill |
| Evidence emitted | Report lists archived files, tombstone paths, authority basis, and blockers |

## VERIFY_KTY checks

| Check | Validation |
|---|---|
| Report only | No KTY files were modified |
| Current-content boundary | `.Archive/` was excluded from current factual assessment |
| SCA comparison | Observed content state was compared against admitted decomposition and SCA artifacts |
| Factual-use gate | Report states whether current content is allowed, blocked, retired, or regeneration-only |
| Blockers surfaced | Missing authority, ambiguous disposition, or contradictions are not silently resolved |

## EMIT_DISPOSITION checks

| Check | Validation |
|---|---|
| Evidence fields present | Output includes `CONTENT_DISPOSITION_STATE`, `FACTUAL_USE_GATE`, `AUTHORITY_BASIS`, `SOURCE_ACTION_REF`, and `LAST_VERIFIED_AT` |
| Trigger fields present | Output includes `EntityType`, `EntityID`, `AffectedSubjects`, `AffectedHBK`, `CanonicalRootName`, and `FacilityID` fields, with blanks only when not applicable |
| Archive path explicit | `ARCHIVE_AND_STUB` evidence includes `ArchivePath` |
| Manifest untouched | SCOPE_CHANGE remains responsible for manifest row updates |
| Evidence paths resolvable | Every listed evidence path exists or is marked `location TBD` with blocker notes |

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- `KTY_PATH`
- `MODE`
- `AMENDMENT_ID`
- `SOURCE_ACTION_REF`
- expected and observed disposition
- files archived or verified
- evidence outputs written
- .Archive/ scanner exclusion status
- no blockers, or explicit blocker list

## Failure reporting

| Condition | Report |
|---|---|
| Missing KTY path | `RUN_STATUS=FAILED_INPUTS` |
| Unsupported mode | `RUN_STATUS=FAILED_INPUTS` |
| Missing SCA snapshot | `RUN_STATUS=FAILED_INPUTS` |
| Missing structured supersession authority for factual checks | `RUN_STATUS=FAILED_INPUTS` |
| Dispatch does not match expected disposition | `RUN_STATUS=BLOCKED_EXPECTATION_MISMATCH` |
| Archive write target not authorized | `RUN_STATUS=BLOCKED_WRITE_SCOPE` |
| Existing archive collision cannot be resolved safely | `RUN_STATUS=BLOCKED_ARCHIVE_COLLISION` |

## Invalid states

A run is invalid when:

- active factual content was rewritten instead of archived or verified
- `_STATUS.md`, `_CONTEXT.md`, or `_REFERENCES.md` was modified
- `KTY_Remediation_Manifest.csv` was modified by this skill
- `.Archive/` content was treated as current factual authority
- supersession was inferred from SCA prose instead of structured artifacts
- findings lacked evidence paths or explicit `location TBD`
