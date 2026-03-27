# Decision Log — COV_POST_SCA001

**Run Label:** POST_SCA001
**Timestamp:** 2026-03-26T17:48

## Defaults Applied

| # | Decision | Rationale |
|---|---|---|
| DL-001 | SCOPE defaulted to ALL — no subset filtering applied | Brief specified SCOPE=ALL |
| DL-002 | DECOMP_VARIANT set to PROJECT — standard PKG/DEL folder patterns used | Brief specified DECOMP_VARIANT=PROJECT |
| DL-003 | Artifact presence assessed as structural folder presence (not individual file enumeration) | Decomposition §7 tables do not enumerate individual artifact filenames; "Covers SOW" column provides scope mapping, not file inventory. Consistent with prior run methodology. |
| DL-004 | Context fidelity: Package reference extracted using both `**Package:**` and `- **Package**:` patterns to handle two format variants across the 117 _CONTEXT.md files | Both formats correctly encode the PKG-ID; neither is incorrect. |
| DL-005 | Lifecycle state extracted by matching known state keywords (SEMANTIC_READY, OPEN, etc.) to handle two _STATUS.md format variants | Both variants correctly encode the lifecycle state. |

## Overrides

None. No human overrides were applied during this run.

## Assumptions

| # | Assumption | Impact |
|---|---|---|
| A-001 | The decomposition document's §9 Coverage & Telemetry section is the authoritative source for ScopeItemCount (IN=92, OUT=7), validated against §8 ledger rows and §4 OUT items. | Low — counts are internally consistent. |
| A-002 | SOW-0122 (new IN item from SCA-001) is correctly mapped to DEL-018-06 per D-013. No new deliverable was expected or created. | None — confirmed in filesystem. |
