# equation-audit contract

## Runtime Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `WORK_DIR` | MUST | — | Per-page `_pdf2md_work/` produced by pdf2md-orchestration (contains `page_NNNN.png`, `page_NNNN.md`, `page_NNNN.anchored.md`) |
| `SOURCE_AUDIT_ROOT` | MUST | `{WORK_DIR/..}/{book}/audit/equations/` | Versioned-snapshot layout root for this source's equation audit |
| `SOURCE_MD` | MUST | — | The assembled `<book>.md` (domain-decomp's eventual input) — `process_flagged.py` reassembles this after applying fixes |
| `TITLE` | MUST | — | Human-friendly title used in the audit HTML banner |
| `BOOK` | SHOULD | derived from `SOURCE_MD` filename stem | Used in snapshot directory naming |
| `ENABLE_CROPS` | MAY | `false` | Run per-page bbox detection + cropping at Phase 1; embeds per-equation PNG crops in the audit HTML |
| `ALLOW_UNREVIEWED` | MAY | `0` | Maximum tolerated unreviewed-equation count at Phase 6 close. Useful for smoke tests or partial-coverage closures |
| `BATCH_SIZE` | MAY | 5 | Number of equation-bbox-detect or equation-flag-interpret dispatches to run in parallel per batch |

---

## Workflow requirements

- **Tools are deterministic; violation is a design defect.** `audit_equations.py`, `process_flagged.py`, `validate_flagged_schema.py`, `scan_equation_audit_state.py`, `migrate_audit_layout.py`, `crop_equation_regions.py`, and the brief-builders are Python scripts with no LLM API calls. If a pipeline stage requires LLM reasoning, it belongs in a TASK+workflow dispatch, not in a tool invocation.
- **LLM reasoning is dispatched via workflows.** Per-flag interpretation of prose correction notes is performed by `equation-flag-interpret` TASK dispatches; per-page bbox detection is performed by `equation-bbox-detect` TASK dispatches. WORKING_ITEMS does not interpret notes or estimate bboxes itself.
- **Hash-keyed identity is load-bearing.** Equations are keyed by `sha1(latex)[:12]`. When a fix is applied, the equation's hash changes; the OLD verified/flagged sidecar entries for the OLD hash become stale automatically (correct behavior — needs re-review). `backcheck.json` is the bridge: a fix-applied-but-not-yet-verified entry.
- **Working state is mutable; snapshots are immutable.** Phase 6 closure promotes the current `working/` state into a new immutable snapshot under `snapshots/EQ_{book}_{TS}/` and updates `_LATEST.md` to point at it. Snapshots MUST NOT be modified after creation.
- **Schema gate before fix-apply.** `process_flagged.py` refuses to apply any flagged entry whose `description` is prose-shaped. WORKING_ITEMS’ Phase 3a converts prose to LaTeX via the `equation-flag-interpret` workflow; Phase 3b runs `validate_flagged_schema.py` as a gate; Phase 3c applies. Skipping Phase 3a-3b is a contract violation.
- **Sidecar-fallback convention is preserved.** Canonical `verified.json`/`flagged.json`/`backcheck.json` files take priority; if empty or missing, the most recent timestamped browser export (`*_verified_<TS>.json` / `*_flagged_<TS>.json`) is used. WORKING_ITEMS never edits browser exports directly — the canonical file is always the source of truth.
- **WORKING_ITEMS does not write outside its scope.** Writes are confined to `{SOURCE_AUDIT_ROOT}/` and (via `process_flagged.py`) `{WORK_DIR}/page_NNNN.md` / `page_NNNN.anchored.md` plus the reassembled `{SOURCE_MD}`. WORKING_ITEMS MUST NOT touch other sources' audit folders, other agents' decomposition state, or any path not explicitly authorized in the run brief. `WORK_DIR` may be a declared sibling of the source root.

---

## Artifacts and tool interfaces

### Filesystem layout

```
{source_root}/                                    e.g. _Sources/MWK_1956/
  audit/
    pages -> ../../{book}_pdf2md_work/            ← symlink (preserved across migration)
    equations/
      _LATEST.md                                  ← pointer to most recent snapshot
      working/                                    ← mutable live state
        equations.html                            ← rendered audit surface
        equations.jsonl                           ← one JSON per equation
        verified.json                             ← canonical sidecar (may be {} when empty)
        flagged.json                              ← canonical sidecar
        backcheck.json                            ← canonical sidecar
        {book}_verified_{TS}.json                 ← human-exported timestamped sidecar
        {book}_flagged_{TS}.json
        flagged.json.{TS}.bak                     ← rotated by process_flagged.py
        .archive/                                 ← legacy archive (preserved verbatim)
        crops/                                    ← per-equation PNG crops (when ENABLE_CROPS)
          page_NNNN_eq_NN.png
      snapshots/
        EQ_{book}_{YYYY-MM-DD}_{HHMM}/            ← immutable snapshot per closure
          Brief.md                                ← runtime parameters
          RUN_SUMMARY.md                          ← state counts, fix count, iteration count
          QA_Report.md                            ← closure-eligibility check results
          equations.html                          ← frozen
          equations.jsonl                         ← frozen
          verified.json                           ← frozen
          flagged.json                            ← frozen (typically {})
          backcheck.json                          ← frozen (typically {})
          crops/                                  ← frozen (when present in working/)

{book}_pdf2md_work/                              ← per-page pdf2md-orchestration scratch (shared with pdf2md-orchestration)
  page_NNNN.png
  page_NNNN.md                                    ← may be modified by process_flagged.py
  page_NNNN.anchored.md                           ← may be modified by process_flagged.py
  page_NNNN_eq_bboxes.json                        ← written by equation-bbox-detect dispatches
```

### Tool dependencies

| Tool | Path | Phase |
|---|---|---|
| Migrate (legacy → versioned) | `tools/equation_audit/migrate_audit_layout.py` | 0 (one-shot) |
| State scan | `tools/equation_audit/scan_equation_audit_state.py` | 0, 2, 5, 6 |
| Equation extract | `tools/equation_audit/audit_equations.py` | 1, 4 |
| Bbox-detect brief | `tools/equation_audit/build_equation_bbox_brief.py` | 1 |
| Bbox crop | `tools/equation_audit/crop_equation_regions.py` | 1 |
| Interpret brief | `tools/equation_audit/build_equation_interpret_brief.py` | 3a |
| Schema validate | `tools/equation_audit/validate_flagged_schema.py` | 3b |
| Fix-apply | `tools/equation_audit/process_flagged.py` | 3c |
| Assemble (re-) | `tools/pdf2md/assemble_markdown.py` | 3c (via process_flagged.py) |
| Clean (re-) | `tools/reporting/clean_pdf2md_output.py` | 3c (via process_flagged.py) |
| Prune (snapshots + exports) | `tools/equation_audit/prune_old_snapshots.py` | Operational (out-of-band; not part of the 0–6 loop) — keeps the most recent N per category (default 20). Run periodically once a source has accumulated many closures/exports |

### Workflows dispatched

| Workflow | Path | Phase | Dispatch shape |
|---|---|---|---|
| `equation-flag-interpret` | `workflows/equation-flag-interpret/` | 3a | One TASK per flagged entry with a prose description |
| `equation-bbox-detect` | `workflows/equation-bbox-detect/` | 1 (when `ENABLE_CROPS`) | One TASK per page containing display equations |
