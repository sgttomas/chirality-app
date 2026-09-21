# equation-audit procedure

WORKING_ITEMS coordinates this procedure and assigns bounded visual or semantic stages to TASK. Tool commands resolve against the declared tool root.

### Phase 0 — Pre-flight (Gate 0)

1. Validate `WORK_DIR` exists and contains `page_NNNN.png` + `page_NNNN.md` files produced by pdf2md-orchestration.
2. Resolve `SOURCE_AUDIT_ROOT`:
   - If not provided, derive from `WORK_DIR`: walk up to find the source root and use `{source}/audit/equations/`.
   - If the legacy flat layout exists (`{source}/audit/equations.html` etc.) and the new layout does NOT exist, run:
     ```
     python3 tools/equation_audit/migrate_audit_layout.py --source-audit-dir {source}/audit/
     ```
     This is idempotent and is a no-op on already-migrated layouts. After migration the working state lives under `{source}/audit/equations/working/` and `_LATEST.md` points to "(no snapshot yet)".
3. Scan current state:
   ```
   python3 tools/equation_audit/scan_equation_audit_state.py --audit-root {SOURCE_AUDIT_ROOT}/working/
   ```
   Capture: `total`, `verified`, `flagged`, `backcheck`, `unreviewed`, `overlaps`, and any warnings (orphan sidecar keys).
4. **Gate 0 (human confirmation):**
   > "Source `{book}`: WORK_DIR `{WORK_DIR}`, audit root `{SOURCE_AUDIT_ROOT}`.
   > Current state: {total} equations total, {verified} verified, {flagged} flagged, {backcheck} backcheck-pending, {unreviewed} unreviewed.
   > Warnings: {warnings list or 'none'}.
   > ENABLE_CROPS: {ENABLE_CROPS}. ALLOW_UNREVIEWED at close: {ALLOW_UNREVIEWED}.
   > Proceed to Phase 1?"

### Phase 1 — Extract

1. Run the equation extractor against the current `WORK_DIR`, writing into `working/`:
   ```
   python3 tools/equation_audit/audit_equations.py \
       --work-dir {WORK_DIR} \
       --out-html {SOURCE_AUDIT_ROOT}/working/equations.html \
       --out-jsonl {SOURCE_AUDIT_ROOT}/working/equations.jsonl \
       --title "{TITLE}"
   ```
   The tool reads existing `verified.json`/`flagged.json`/`backcheck.json` under `working/` and re-renders the audit HTML with prior review state preserved (equations whose hash hasn't changed retain their badges).
2. If `ENABLE_CROPS=true`:
   a. Build the list of pages with display equations from `equations.jsonl`.
   b. For each such page, build a dispatch brief:
      ```
      python3 tools/equation_audit/build_equation_bbox_brief.py \
          --image-path {WORK_DIR}/page_{NNNN}.png \
          --page-md-path {WORK_DIR}/page_{NNNN}.md \
          --page-num {N} \
          --output-path {WORK_DIR}/page_{NNNN}_eq_bboxes.json \
          --expected-equation-hashes <hashes from JSONL>
      ```
   c. Spawn TASK+`Workflow: equation-bbox-detect` dispatches in batches of `BATCH_SIZE`. Each writes one bbox JSON.
   d. After all batches complete, crop:
      ```
      python3 tools/equation_audit/crop_equation_regions.py \
          --work-dir {WORK_DIR} \
          --crops-dir {SOURCE_AUDIT_ROOT}/working/crops/
      ```
   e. Re-run `audit_equations.py` with `--crops-dir {SOURCE_AUDIT_ROOT}/working/crops/` so each equation chunk embeds the source crop beside the rendered KaTeX and raw LaTeX.
3. Report:
   > "Phase 1 complete. Extracted {N} display equations across {P} pages.
   > {ENABLE_CROPS: ' Crops: {C} written.' or ''}
   > Audit HTML: `{SOURCE_AUDIT_ROOT}/working/equations.html`."

### Phase 2 — Review (Gate 2)

This is a human-driven phase. WORKING_ITEMS does NOT advance until the human exports their review.

1. Direct the human to open `{SOURCE_AUDIT_ROOT}/working/equations.html` in a browser.
2. The human marks each equation Verified, Flagged (with corrected LaTeX OR a natural-language note), or leaves it Unreviewed. Filters (`Hide verified`, `Only flagged`, `Only backcheck`) help navigation.
3. When the human clicks "Export verified.json + flagged.json", two timestamped files download. The human moves them into `{SOURCE_AUDIT_ROOT}/working/`.
4. Re-scan state:
   ```
   python3 tools/equation_audit/scan_equation_audit_state.py --audit-root {SOURCE_AUDIT_ROOT}/working/
   ```
5. **Gate 2 (human confirmation):**
   > "Browser review complete. {V} newly verified, {F} flagged for fix, {B} backcheck items still pending, {U} unreviewed remain.
   > Of {F} flagged, {Fp} have prose-shaped descriptions (will dispatch equation-flag-interpret) and {Fl} have LaTeX-shaped descriptions (will apply directly).
   > Proceed to Phase 3 (Apply fixes)? If no flags pending and no backcheck, you may skip to Phase 6 (Close)."

### Phase 3 — Apply fixes

#### Phase 3a — Interpret prose notes

1. Load `working/flagged.json` (or the most recent timestamped export if canonical is empty).
2. For each entry whose `description` is prose-shaped (heuristic per `validate_flagged_schema.py` — no `\<command>` AND >=3 distinct English stop-words):
   a. Build a dispatch brief:
      ```
      python3 tools/equation_audit/build_equation_interpret_brief.py \
          --flagged-json {SOURCE_AUDIT_ROOT}/working/flagged.json \
          --equation-hash {hash} \
          --output-path {SOURCE_AUDIT_ROOT}/working/.interpret/{key}.json \
          [--page-image-path {WORK_DIR}/page_{NNNN}.png]
      ```
   b. Spawn TASK+`Workflow: equation-flag-interpret` dispatches in batches of `BATCH_SIZE`.
3. For each successful dispatch (`RUN_STATUS=SUCCESS`), merge the worker's `interpreted_latex` back into `flagged.json`'s `description` field for that key. Atomic write; preserve the file's other entries.
4. For each `RUN_STATUS=NO_FINDINGS` dispatch (note was too ambiguous), preserve the original entry and immediately obtain human clarification using the Gate 5 review surface. Return to Phase 3a with that clarification before attempting Phase 3b. The schema gate remains closed while unresolved prose exists.

#### Phase 3b — Validate schema (Gate 3b — automated, not human)

1. Run the schema validator:
   ```
   python3 tools/equation_audit/validate_flagged_schema.py --flagged-json {SOURCE_AUDIT_ROOT}/working/flagged.json
   ```
2. If exit code != 0:
   - The validator's stderr lists which entries still have prose descriptions or missing fields.
   - Loop back to Phase 3a for the offending entries (some may be ambiguous; re-dispatch with better disambiguation, or obtain human clarification through the Gate 5 review surface before returning to Phase 3a).
3. Continue to Phase 3c only when exit code == 0.

#### Phase 3c — Apply fixes

1. Run the deterministic fix-applier:
   ```
   python3 tools/equation_audit/process_flagged.py \
       --audit-dir {SOURCE_AUDIT_ROOT}/working/ \
       --work-dir {WORK_DIR} \
       --source-md {SOURCE_MD} \
       --title "{TITLE}"
   ```
   The tool: (a) reruns `validate_flagged_schema.py` as a safety gate, (b) replaces each flagged equation's LaTeX in `page_NNNN.md` + `page_NNNN.anchored.md`, (c) reassembles `{SOURCE_MD}` via `assemble_markdown.py`, (d) re-cleans via `clean_pdf2md_output.py`, (e) writes/extends `backcheck.json` with one entry per applied fix, (f) archives `flagged.json` to a timestamped `.bak` and resets it to `{}`, (g) re-runs `audit_equations.py` to refresh the audit HTML.
2. Capture stdout from `process_flagged.py` — it reports `applied=N failures=M`.
3. Report:
   > "Phase 3 complete. {N} fixes applied; {M} failures. Backcheck queue: {B} entries pending re-review."

### Phase 4 — Re-extract

1. `process_flagged.py` already ran `audit_equations.py` at the end of Phase 3c, so the audit HTML now shows fixed equations as `Backcheck` state.
2. If `ENABLE_CROPS=true`, regenerate crops for any pages whose equations changed. Use the bbox detect workflow again for those pages only.
3. No human gate here — proceed automatically to Phase 5.

### Phase 5 — Verify backcheck (Gate 5)

This is a human-driven phase. WORKING_ITEMS does NOT advance until the human reviews each backcheck item.

1. Direct the human to re-open `{SOURCE_AUDIT_ROOT}/working/equations.html` (or refresh it).
2. For each `Backcheck`-state equation, the human picks:
   - **✓ Verified** — accept the fix; the entry moves into `verified.json` on next export.
   - **⚠ Flag** — the fix is still wrong; describe further correction (LaTeX or prose); the entry moves into `flagged.json` on next export.
3. Surface any Phase 3a `NO_FINDINGS` ambiguity reasons to the human at this gate — these equations need direct human attention.
4. Human exports updated sidecars and moves them into `{SOURCE_AUDIT_ROOT}/working/`.
5. Re-scan state.
6. **Gate 5 (human confirmation):**
   > "Backcheck review complete. {V_new} backcheck items accepted as verified, {F_new} re-flagged for further correction.
   > If {F_new} > 0: loop back to Phase 3 (Apply fixes). Otherwise proceed to Phase 6 (Close)."

If `{F_new} > 0`, return to Phase 3a. Iteration continues until backcheck is empty.

### Phase 6 — Close (Gate 6)

1. Run the state scanner:
   ```
   python3 tools/equation_audit/scan_equation_audit_state.py --audit-root {SOURCE_AUDIT_ROOT}/working/
   ```
2. Check closure eligibility:
   - `flagged == 0` (no pending fixes)
   - `backcheck == 0` (no pending re-reviews)
   - `unreviewed <= ALLOW_UNREVIEWED` (default 0 — full coverage; smoke tests may set higher)
   - `overlaps == 0` (no equation in multiple states)
3. If flags, backcheck, or overlaps remain, return to the corresponding review/fix stage. If only unreviewed coverage exceeds the allowance, return to Phase 2 or record an explicit human revision to `ALLOW_UNREVIEWED`. That allowance changes coverage only; it cannot waive flags, backcheck, or overlaps.
4. **Gate 6 (human confirmation):**
   > "Ready to close: {V} verified, {U} unreviewed (allowance: {ALLOW_UNREVIEWED}).
   > Promote `working/` to snapshot `EQ_{book}_{YYYY-MM-DD}_{HHMM}/`?"
5. Promote to snapshot:
   - Create a fresh `{SOURCE_AUDIT_ROOT}/snapshots/EQ_{book}_{YYYY-MM-DD}_{HHMM}/`; if that name already exists, choose a new timestamp or unique suffix. Assemble all closure files before freezing the directory. Never reuse an existing closed snapshot.
   - Copy (not move) every file from `working/` into the snapshot directory: `equations.html`, `equations.jsonl`, `verified.json`, `flagged.json` (typically `{}` at close), `backcheck.json`, `crops/` (if present), the most recent timestamped browser exports.
   - Write `Brief.md` (the runtime parameters used for this closure), `RUN_SUMMARY.md` (state counts, fix count, dispatch counts, loop iterations), and `QA_Report.md` (closure-eligibility check results).
6. Update `{SOURCE_AUDIT_ROOT}/_LATEST.md`:
   - Replace its contents with a pointer to the new snapshot's relative path, the closure timestamp, and the headline metrics (verified count, total equation count).
7. Report:
   > "Phase 6 complete. Snapshot: `{SOURCE_AUDIT_ROOT}/snapshots/EQ_{book}_{TS}/`.
   > _LATEST pointer updated.
   > Working state remains live for the next iteration."
