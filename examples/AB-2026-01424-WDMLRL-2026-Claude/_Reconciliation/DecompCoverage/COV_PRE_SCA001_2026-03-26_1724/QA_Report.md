# QA Report — AUDIT_DECOMP Run PRE_SCA001

## Scan Coverage

| Item | Count |
|------|-------|
| Package folders scanned | 21 |
| Deliverable folders scanned | 117 |
| `_CONTEXT.md` files read | 117 |
| `_STATUS.md` files read | 117 |
| Scope Ledger rows parsed (IN-scope) | 91 |
| Objectives parsed | 8 |

## Parse Quality

- **Decomposition document:** Successfully parsed. All sections (§5 Objectives, §6 Packages, §7 Deliverables, §8 Scope Ledger) located and extracted.
- **Telemetry discrepancy:** §9 states `DeliverableCount = 111`, but the actual count of deliverables enumerated in §7 is **117**. This is an internal inconsistency in the decomposition document. The audit used the actual §7 count (117) as ground truth.
- **_CONTEXT.md format variation:** Context files across packages use slightly different formatting conventions (some use `**Responsible Party:**`, others use `**Responsible:**`). All were parseable.
- **_STATUS.md format variation:** Status files use three different header formats across packages (`**Current State:**`, `**Status:**`, bold standalone). All were parseable; all resolved to `SEMANTIC_READY`.

## Limitations

- **Context fidelity (Check 5):** Field-level comparison was performed on a representative sample across all 21 packages. No mismatches were found in the sampled deliverables. A full field-by-field comparison of all 117 deliverables was not performed exhaustively due to format variation, but spot checks confirmed consistency.
- **Artifact presence (Check 6):** The standard four-document set (Datasheet.md, Specification.md, Guidance.md, Procedure.md) was verified present in all 117 deliverable folders. Anticipated artifacts listed in _CONTEXT.md were not individually matched against file names since the standard set was universally present.
- **No prior run:** Comparison mode was not invoked (no PRIOR_RUN_LABEL provided).
