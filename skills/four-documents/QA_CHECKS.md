# QA CHECKS — four-documents

## Minimum output validity checks

1. The four document files exist after a successful Pass 1 run.
2. `DECOMP_VARIANT=DOMAIN` is rejected with `UNSUPPORTED_VARIANT`.
3. `P3_ONLY` does not proceed unless the four existing documents and `_SEMANTIC_LENSING.md` are already present.
4. The run does not modify metadata files other than the safe `_STATUS.md` update.
5. Source-grounding gaps appear as `TBD`, assumptions, or conflict-table entries rather than invented content.
6. The run stays within the target deliverable folder.

## Failure reporting expectations

Use `FAILED_INPUTS` when:
- authoritative source materials are unavailable,
- required existing files for `P3_ONLY` are missing,
- overwrite protection blocks the run.

Use `UNSUPPORTED_VARIANT` when `DECOMP_VARIANT=DOMAIN`.

## Required evidence/log expectations

- Record inaccessible source materials as missing.
- Record source rereads for substantive Pass 3 changes.
- Record any conflict-table additions when source materials and decomposition context disagree.
