# domain-documents — Brief Schema

Use this skill with a generic TASK shell (no profile) like this:

```md
PURPOSE: Draft Knowledge Artifacts for KTY-01 (Pressure Vessel Design)
RequestedBy: ORCHESTRATOR

ScopePath: /abs/path/to/KTY-01_Pressure-Vessel-Design
TaskSkill: domain-documents

RuntimeOverrides:
  KTY_PATH: /abs/path/to/KTY-01_Pressure-Vessel-Design
  DECOMPOSITION_REF: /abs/path/to/_Decomposition
  DECOMP_VARIANT: DOMAIN
  AUTHORITY_MODE: SOURCE_FIDELITY
  RUN_PASSES: FULL
  ALLOW_OVERWRITE_STATES: "OPEN, INITIALIZED"
  SOURCES_ROOT: /abs/path/to/_Sources
  COMBINED_SOURCE_AUTHORITY_PATH: /abs/path/to/shared/source/root
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `domain-documents` | Must match skill folder name |
| `ScopePath` | Absolute path to the Knowledge Type folder | Normally equals `KTY_PATH` |
| `RuntimeOverrides.KTY_PATH` | Absolute path to one Knowledge Type folder | Must contain (or expect) `_CONTEXT.md`, `_STATUS.md` |
| `RuntimeOverrides.DECOMPOSITION_REF` | Path to DOMAIN decomposition folder or doc(s) | Used to locate `KnowledgeTypes.csv`, `HandbookUnits.csv`, `DomainLedger.csv` |

## Optional fields

| Field | Default | Allowed values | Notes |
|---|---|---|---|
| `RuntimeOverrides.DECOMP_VARIANT` | `DOMAIN` | `DOMAIN` only | **Fixed to DOMAIN.** This skill is DOMAIN-only; PROJECT/SOFTWARE variants use `four-documents` |
| `RuntimeOverrides.AUTHORITY_MODE` | `SOURCE_FIDELITY` | `SOURCE_FIDELITY`, `SCA_DRIVEN` | Authority policy for factual content |
| `RuntimeOverrides.RUN_PASSES` | `FULL` | `FULL`, `P1_P2`, `P3_ONLY` | See pass semantics below |
| `RuntimeOverrides.ALLOW_OVERWRITE_STATES` | `OPEN, INITIALIZED` | Comma-separated state list | Safe-update gate for `_STATUS.md` |
| `RuntimeOverrides.SCA_SNAPSHOT_PATH` | omitted | Absolute path | Required when `AUTHORITY_MODE: SCA_DRIVEN` |
| `RuntimeOverrides.SUPERSESSION_MAP_PATH` | omitted | Absolute path | Required and valid only when `AUTHORITY_MODE: SCA_DRIVEN` |
| `RuntimeOverrides.ROOT_NAME` | omitted | String | Canonical root name used to filter supersession rows such as `AppliesToRoots` |
| `RuntimeOverrides.FACILITY_ID` | omitted | String | Facility identifier used to filter supersession rows such as `AppliesToFacilities` |
| `RuntimeOverrides.ALLOW_OVERWRITE_OVERRIDE` | omitted | `SCA_AUTHORIZED` | Permits active content overwrite for the dispatched KTY only when SCA inputs are present |
| `RuntimeOverrides.UNIT_SCOPE` | `EXAMPLES_ONLY` | `EXAMPLES_ONLY`, `ALL_MAPPED` | Which handbook units form the evidence set |
| `RuntimeOverrides.ARTIFACT_NAMING` | `PREFIXED_TYPED_SLUG` | `PREFIXED_TYPED_SLUG`, `TYPED_SLUG`, `PREFIXED_SLUG` | Artifact file naming policy |
| `RuntimeOverrides.MAX_ARTIFACTS` | `25` | Positive integer | Hard cap on artifact file count |
| `RuntimeOverrides.SOURCES_ROOT` | Provided by ORCHESTRATOR | Absolute path | Shared source/reference file root |
| `RuntimeOverrides.COMBINED_SOURCE_AUTHORITY_PATH` | omitted | Absolute path | Additional admitted source authority root for combined/cross-root source packages; source material remains subordinate to structured SCA supersession in `SCA_DRIVEN` mode |
| `RuntimeOverrides.REPORT_TO` | `ORCHESTRATOR` | Free-form | Where to report run outcome |

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## DECOMP_VARIANT

**This skill is DOMAIN-only.** `DECOMP_VARIANT` is fixed to `DOMAIN`. Any other value halts the run with `RUN_STATUS=UNSUPPORTED_VARIANT`. The PROJECT and SOFTWARE variants use the `four-documents` skill (fixed 4-document kit), not this skill.

## AUTHORITY_MODE

`SOURCE_FIDELITY` is the default and preserves existing behavior: source
material bounded by `SourceSpan` is factual authority, while decomposition data
scopes and routes the work.

`SCA_DRIVEN` is used only when SCOPE_CHANGE dispatches regeneration after an
accepted amendment. In this mode, admitted decomposition state, structured SCA
artifacts, and `SUPERSESSION_MAP_PATH` are current factual authority. Source
material is provenance verification only and must not override accepted
SCA/decomposition truth.

`SUPERSESSION_MAP_PATH` without `AUTHORITY_MODE: SCA_DRIVEN` fails input
validation. `ALLOW_OVERWRITE_OVERRIDE: SCA_AUTHORIZED` is accepted only with
`AUTHORITY_MODE: SCA_DRIVEN`, `SCA_SNAPSHOT_PATH`, and
`SUPERSESSION_MAP_PATH`, and only for active `Scoping.md` / `KA-*.md` files in
the dispatched `KTY_PATH`.

Do not infer supersessions from SCA prose.

### SCA-driven example

```md
PURPOSE: Regenerate KTY content from accepted SCA authority.
RequestedBy: SCOPE_CHANGE

ScopePath: /abs/path/to/KTY-03-02_Onboarding-Checklist
TaskSkill: domain-documents

RuntimeOverrides:
  KTY_PATH: /abs/path/to/KTY-03-02_Onboarding-Checklist
  DECOMPOSITION_REF: /abs/path/to/domain-root/_Decomposition
  DECOMP_VARIANT: DOMAIN
  AUTHORITY_MODE: SCA_DRIVEN
  SCA_SNAPSHOT_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510
  SUPERSESSION_MAP_PATH: /abs/path/to/domain-root/_ScopeChange/SCA-004_2026-04-21_1510/Supersession_Map.csv
  ROOT_NAME: Example_Domain_Root
  FACILITY_ID: FAC-001
  ALLOW_OVERWRITE_OVERRIDE: SCA_AUTHORIZED
  RUN_PASSES: FULL
  SOURCES_ROOT: /abs/path/to/_Sources
  COMBINED_SOURCE_AUTHORITY_PATH: /abs/path/to/shared/source/root
```

## RUN_PASSES semantics

| Value | Steps run | Use case |
|---|---|---|
| `FULL` | Steps 1–7 (Pass 1 drafting + Pass 2 consistency + Pass 3 source-fidelity + status) | Default single-run completion |
| `P1_P2` | Steps 1–5 + Step 7 (drafting + cross-artifact consistency only) | When source-fidelity check must be deferred |
| `P3_ONLY` | Step 1 (full reads incl. source) + Step 6 (source-fidelity) + Step 7 | Re-verify existing drafts against source; requires existing KA-*.md files and accessible source |

## UNIT_SCOPE values

- `EXAMPLES_ONLY` → use `KnowledgeTypes.csv.ExampleUnitIDs` (default, bounded)
- `ALL_MAPPED` → use all `UnitID` values from `DomainLedger.csv` where `KnowledgeTypeID(s)` includes this KTY (best-effort; may be large)

## ARTIFACT_NAMING values

- `PREFIXED_TYPED_SLUG` (default) → `KA-01_{Type}__{Slug}.md`
- `TYPED_SLUG` → `{Type}__{Slug}.md`
- `PREFIXED_SLUG` → `KA-01_{Slug}.md`

Where:
- `Type` = base archetype (`Reference|Guidance|Checklist|Procedure`) from `CanonicalSchema`
- `Slug` = filesystem-safe slug from the Knowledge Subject name (letters/numbers/hyphen; collapse whitespace)

## Read boundary

The skill reads:
- Files within `{KTY_PATH}`: `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md`, sibling `_MEMORY.md` / `MEMORY.md` whenever `_STATUS.md` is read, existing `KA-*.md` + `Scoping.md` (for Pass 2/3)
- Decomposition data under `{DECOMPOSITION_REF}`: `KnowledgeTypes.csv`, `HandbookUnits.csv`, `DomainLedger.csv`, or root-specific equivalent register names
- Authoritative source files under `{SOURCES_ROOT}`, `COMBINED_SOURCE_AUTHORITY_PATH`, or paths listed in `_REFERENCES.md` (referenced by `SourceSpan`)
- In `AUTHORITY_MODE: SCA_DRIVEN`, structured SCA artifacts under `SCA_SNAPSHOT_PATH` and `SUPERSESSION_MAP_PATH`

When `ROOT_NAME` or `FACILITY_ID` is provided, supersession rows with scoping fields such as `AppliesToRoots` or `AppliesToFacilities` must be filtered to the dispatched root/facility before being applied.

`_MEMORY.md` / `MEMORY.md` is never factual authority. It is read only as
non-authoritative operational context paired with `_STATUS.md`.

## Write boundary

The skill writes only within `{KTY_PATH}`:
- `Scoping.md` (Pass 1 always; Pass 3 updates the Source-Fidelity Log)
- Variable `KA-*.md` Knowledge Artifact files (Pass 1 creates; Pass 3 may correct)
- `_STATUS.md` (safe-update only: `OPEN → INITIALIZED` when Pass 1/2 ran)

`ALLOW_OVERWRITE_OVERRIDE: SCA_AUTHORIZED` may bypass
`ALLOW_OVERWRITE_STATES` only in `AUTHORITY_MODE: SCA_DRIVEN` with complete SCA
snapshot inputs, and only for the dispatched KTY. It does not authorize
metadata edits or cross-KTY writes.

The skill does NOT modify:
- `_CONTEXT.md`
- `_REFERENCES.md`
- `_MEMORY.md` / `MEMORY.md`
- `_SEMANTIC.md`

## Lifecycle states

DOMAIN lifecycle: `OPEN → INITIALIZED → IN_PROGRESS`

This skill handles the `OPEN → INITIALIZED` transition (during Pass 1/2 runs). The `IN_PROGRESS` transition is handled downstream by `WORKING_ITEMS`.

**Note:** `SEMANTIC_READY` is NOT a valid state in the DOMAIN lifecycle. It belongs to PROJECT/SOFTWARE (four-documents pipeline) only.

## Notes

- One invocation processes one Knowledge Type folder. ORCHESTRATOR dispatches one task per in-scope KTY.
- The brief does not include `AllowedTools` because this is a reasoning-first drafting skill. Safe-update of `_STATUS.md` uses `tools/scaffolding/write_status.sh` if available.
- Authoritative source access is mandatory — runs that cannot read the source file halt with `FAILED_INPUTS`.
