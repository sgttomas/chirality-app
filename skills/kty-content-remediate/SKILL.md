---
name: kty-content-remediate
description: Archive, tombstone, verify, and emit disposition evidence for DOMAIN KTY content after an approved scope change without rewriting active Knowledge Artifact content.
compatibility: Chirality TASK in generic shell mode (no profile); SCOPE_CHANGE-dispatched KTY content disposition evidence pass.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL - kty-content-remediate

## Purpose

Apply a bounded content-disposition pass for one DOMAIN Knowledge Type folder
after an approved scope-change amendment.

This skill exists to keep the one-writer rule intact:

- `domain-documents` is the only writer of active `Scoping.md` and `KA-*.md`
  factual content.
- `kty-content-remediate` never modifies active factual content. It only
  archives retired active-looking files, leaves non-factual `[RETIRED]`
  tombstone stubs, verifies the current content state, and emits evidence for
  SCOPE_CHANGE.

`.Archive/` is a derivative retirement store. It preserves history and evidence,
but it is never factual authority and must be excluded from downstream scanners,
allowlists, section maps, publication inputs, and regeneration inputs.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `SCOPE_CHANGE` Gate 5 KTY remediation orchestration.

## Supported modes

| Mode | Behavior |
|---|---|
| `RETIRE_KTY` | Move active-looking `Scoping.md` and `KA-*.md` files into `{KTY_PATH}/.Archive/`, leave `[RETIRED]` tombstone stubs at the original paths, and emit evidence. |
| `VERIFY_KTY` | Inspect current `Scoping.md` and `KA-*.md` files against admitted decomposition and SCA artifacts. Emit a report only. |
| `EMIT_DISPOSITION` | Emit disposition evidence for SCOPE_CHANGE manifest update. Do not update the manifest directly. |

## Inputs

### Required

- `ScopePath` - absolute path to one KTY folder; normally equals `KTY_PATH`
- `TaskSkill` - `kty-content-remediate`
- `RuntimeOverrides.KTY_PATH` - absolute path to one KTY folder
- `RuntimeOverrides.MODE` - `RETIRE_KTY`, `VERIFY_KTY`, or
  `EMIT_DISPOSITION`
- `RuntimeOverrides.DECOMPOSITION_REF` - admitted decomposition package or
  snapshot that governs the KTY
- `RuntimeOverrides.SCA_SNAPSHOT_PATH` - accepted SCOPE_CHANGE snapshot path
- `RuntimeOverrides.AMENDMENT_ID` - `SCA-{NNN}`
- `RuntimeOverrides.REVIEW_OUTPUT_PATH` - markdown report path

### Required for SCA-driven factual checks

- `RuntimeOverrides.SUPERSESSION_MAP_PATH` - path to the accepted
  `Supersession_Map.csv`
- `RuntimeOverrides.SOURCE_ACTION_REF` - `Amendment_Actions.csv` row or
  decision reference that required this KTY disposition

### Optional

- `RuntimeOverrides.DISPOSITION_EVIDENCE_PATH` - optional CSV evidence output
- `RuntimeOverrides.ENTITY_TYPE` - triggering entity type from manifest row
- `RuntimeOverrides.ENTITY_ID` - triggering entity id from manifest row
- `RuntimeOverrides.AFFECTED_SUBJECTS` - semicolon-separated affected `SUB-*`
  ids, when known
- `RuntimeOverrides.AFFECTED_HBK` - semicolon-separated affected `HBK-*` ids,
  when known
- `RuntimeOverrides.CANONICAL_ROOT_NAME` - root disambiguator for multi-root
  projects
- `RuntimeOverrides.FACILITY_ID` - facility scope token, when applicable
- `RuntimeOverrides.ARCHIVE_RUN_ID` - stable run id used under `.Archive/`;
  default `{AMENDMENT_ID}_{YYYY-MM-DD}_{HHMM}`
- `RuntimeOverrides.EXPECTED_DISPOSITION` - expected manifest action:
  `ARCHIVE_AND_STUB`, `VERIFY_ONLY`, `NO_ACTION`, or `UNKNOWN`
- `RuntimeOverrides.MAX_FILES` - soft cap on `KA-*.md` files inspected;
  default `100`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `KTY_PATH` | KTY folder to remediate or verify | **Required** | Absolute path to one `KTY-*` folder |
| `MODE` | Remediation mode | **Required** | `RETIRE_KTY`, `VERIFY_KTY`, `EMIT_DISPOSITION` |
| `DECOMPOSITION_REF` | Admitted decomposition authority | **Required** | Absolute path |
| `SCA_SNAPSHOT_PATH` | Accepted SCOPE_CHANGE snapshot | **Required** | Absolute directory path |
| `AMENDMENT_ID` | Amendment identifier | **Required** | `SCA-{NNN}` |
| `SUPERSESSION_MAP_PATH` | Accepted supersession map | Required for factual checks | Absolute path |
| `SOURCE_ACTION_REF` | Amendment action or decision reference | Required for factual checks | Stable action/decision id |
| `REVIEW_OUTPUT_PATH` | Markdown report output | **Required** | Path in `AllowedWriteTargets` |
| `DISPOSITION_EVIDENCE_PATH` | Structured evidence CSV | omitted | Path in `AllowedWriteTargets` |
| `ENTITY_TYPE` | Triggering entity type | omitted | `KNOWLEDGE_TYPE`, `KNOWLEDGE_SUBJECT`, `HANDBOOK_UNIT`, `CATEGORY`, `VOCAB_TERM`, `OTHER` |
| `ENTITY_ID` | Triggering entity id | omitted | Stable id or term string |
| `AFFECTED_SUBJECTS` | Affected subject ids | omitted | Semicolon-separated `SUB-*` ids |
| `AFFECTED_HBK` | Affected handbook unit ids | omitted | Semicolon-separated `HBK-*` ids |
| `CANONICAL_ROOT_NAME` | Root disambiguator | omitted | Canonical root token |
| `FACILITY_ID` | Facility scope token | omitted | Facility id or blank |
| `ARCHIVE_RUN_ID` | Archive subfolder token | `{AMENDMENT_ID}_{timestamp}` | Filesystem-safe token |
| `EXPECTED_DISPOSITION` | Expected action from manifest draft | `UNKNOWN` | `ARCHIVE_AND_STUB`, `VERIFY_ONLY`, `NO_ACTION`, `UNKNOWN` |
| `MAX_FILES` | Soft cap on KA file count | `100` | Positive integer |

## Read boundary

The skill reads only:

- `{KTY_PATH}/Scoping.md`
- `{KTY_PATH}/KA-*.md`
- `{KTY_PATH}/.Archive/` for archive-collision and prior-evidence checks only
- admitted decomposition material under `{DECOMPOSITION_REF}`
- accepted SCOPE_CHANGE artifacts under `{SCA_SNAPSHOT_PATH}`, including
  `Amendment_Actions.csv`, `KTY_Remediation_Manifest.csv` when present,
  `Supersession_Delta.csv`, and `Supersession_Map.csv`

This skill must not scan sibling KTY folders. It must not treat `.Archive/` as
current content.

## Write boundary

Writes are limited to:

- `{KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/...` in `RETIRE_KTY`
- original `{KTY_PATH}/Scoping.md` and `{KTY_PATH}/KA-*.md` paths only to
  replace retired factual content with non-factual tombstone stubs in
  `RETIRE_KTY`
- `REVIEW_OUTPUT_PATH`
- optional `DISPOSITION_EVIDENCE_PATH`

This skill does not write `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`,
decomposition files, SCOPE_CHANGE manifests, `_Aggregation`, hypergraph outputs,
or publication outputs.

## Tool usage

- Reasoning-first only.
- No deterministic helpers are declared.
- The `allowed-tools` frontmatter field is intentionally omitted.

## Authority rules

In all modes, current factual authority is the accepted upstream state supplied
by SCOPE_CHANGE:

1. admitted decomposition state,
2. structured SCA artifacts, especially `Amendment_Actions.csv` and
   `KTY_Remediation_Manifest.csv` when present,
3. `Supersession_Map.csv`,
4. source material only as provenance evidence.

Source material does not override accepted SCA or decomposition truth during
this skill. Do not infer supersessions from SCA prose. Supersession decisions
must come from structured SCA artifacts and `Supersession_Map.csv`.

## Method

### Step 0 - Preconditions

1. Confirm `KTY_PATH` is one KTY folder.
2. Confirm `MODE` is supported.
3. Confirm `DECOMPOSITION_REF`, `SCA_SNAPSHOT_PATH`, and `AMENDMENT_ID` are
   readable.
4. Confirm `REVIEW_OUTPUT_PATH` and optional `DISPOSITION_EVIDENCE_PATH` are in
   `AllowedWriteTargets`.
5. For factual checks, confirm `SUPERSESSION_MAP_PATH` and
   `SOURCE_ACTION_REF` are present. If not, return `RUN_STATUS=FAILED_INPUTS`.
6. Enumerate only root-level `Scoping.md` and `KA-*.md` files under
   `KTY_PATH`. Exclude `.Archive/` from current-content enumeration.

### Step 1 - Resolve Expected Disposition

1. Read `Amendment_Actions.csv` and, when present,
   `KTY_Remediation_Manifest.csv` from `SCA_SNAPSHOT_PATH`.
2. Match this KTY by `KTY_PATH`, KTY id, or `SOURCE_ACTION_REF`.
3. Record the expected action:
   - `ARCHIVE_AND_STUB`
   - `REGENERATE_CONTENT`
   - `VERIFY_ONLY`
   - `NO_ACTION`
   - `UNKNOWN`
4. If `MODE` conflicts with the expected action, do not improvise. Emit
   `RUN_STATUS=BLOCKED_EXPECTATION_MISMATCH`.

### Step 2 - RETIRE_KTY

Run only when `MODE = RETIRE_KTY`.

1. Identify active-looking content files:
   - `Scoping.md`
   - `KA-*.md`
   - exclude files whose first substantive line begins with `[RETIRED]`
2. Create `{KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/`.
3. Move each active-looking file into the archive subfolder, preserving the
   original filename.
4. At each original path, write a tombstone stub:
   - first line: `[RETIRED]`
   - amendment id
   - source action reference
   - archive path
   - statement that the stub is not factual authority
5. Do not alter `_STATUS.md`, `_CONTEXT.md`, or `_REFERENCES.md`.
6. Emit report and evidence listing archived files, tombstone paths, archive
   paths, authority basis, and unresolved blockers.

#### Tombstone Format

Use this exact markdown structure for every tombstone stub:

```md
# [RETIRED] {OriginalTitleOrFilename}

This file is a non-factual tombstone stub. It is not current KTY factual
authority and must not be used as source material for downstream generation,
allowlists, section maps, publication inputs, or factual current-content scans.

| Field | Value |
|---|---|
| KTY ID | {KTYID or TBD} |
| Original Path | {original path} |
| Archive Path | {KTY_PATH}/.Archive/{ARCHIVE_RUN_ID}/{original filename} |
| Amendment ID | {AMENDMENT_ID} |
| Source Action Ref | {SOURCE_ACTION_REF} |
| Authority Basis | {DECOMPOSITION_REF}; {SCA_SNAPSHOT_PATH}; {SUPERSESSION_MAP_PATH or N/A} |
| Retired At | {timestamp} |
| Factual Use Gate | RETIRED_NO_FACTUAL_USE |

See the SCA evidence report for disposition details.
```

### Step 3 - VERIFY_KTY

Run only when `MODE = VERIFY_KTY`.

1. Read current root-level `Scoping.md` and `KA-*.md` files.
2. Compare observed files to the expected disposition and admitted
   decomposition/SCA state.
3. Verify that tombstoned files are not treated as current factual content.
4. Verify that active files do not contradict structured SCA and supersession
   decisions for the target KTY.
5. Emit findings only. Do not modify content.

### Step 4 - EMIT_DISPOSITION

Run only when `MODE = EMIT_DISPOSITION`.

1. Inspect the current KTY content state.
2. Emit evidence fields suitable for SCOPE_CHANGE manifest update:
   `EntityType`, `EntityID`, `AffectedSubjects`, `AffectedHBK`,
   `CanonicalRootName`, `FacilityID`, `CONTENT_DISPOSITION_STATE`,
   `FACTUAL_USE_GATE`, `AUTHORITY_BASIS`, `SOURCE_ACTION_REF`, `ArchivePath`,
   `LAST_VERIFIED_AT`, evidence paths, and blocker notes.
3. Do not update `KTY_Remediation_Manifest.csv` directly.

## Output expectations

Every run emits a markdown report at `REVIEW_OUTPUT_PATH` containing:

- `RUN_STATUS`
- `KTY_PATH`
- `MODE`
- `AMENDMENT_ID`
- `SOURCE_ACTION_REF`
- expected disposition
- observed current-content files, excluding `.Archive/`
- evidence paths
- blocker notes
- whether .Archive/ scanner exclusion was respected

When `DISPOSITION_EVIDENCE_PATH` is provided, emit CSV rows with:

```csv
AmendmentID,SourceActionRef,EntityType,EntityID,KTYPath,AffectedSubjects,AffectedHBK,CanonicalRootName,FacilityID,Mode,ObservedFile,DispositionState,FactualUseGate,AuthorityBasis,EvidencePath,ArchivePath,LastVerifiedAt,BlockerNotes
```

## Non-negotiable constraints

- One KTY folder per run.
- This skill never modifies active factual content.
- Only `domain-documents` may write regenerated active `Scoping.md` or
  `KA-*.md` factual content.
- Do not edit `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`,
  decomposition files, SCOPE_CHANGE manifests, `_Aggregation`, hypergraph
  outputs, or publication outputs.
- Do not dispatch other skills.
- Do not treat `.Archive/` as factual authority.
- .Archive/ scanner exclusion is non-negotiable for every downstream
  scanner, allowlist, section map, publication input, and regeneration input.
- Do not infer supersessions from SCA prose.
- Missing or ambiguous authority is a blocker, not a reason to guess.

## See also

- `agents/AGENT_SCOPE_CHANGE.md` - Gate 5 dispatcher and manifest owner
- `skills/domain-documents/` - sole writer of active KTY factual content
- `skills/kty-metadata-align/` - metadata-only KTY alignment
