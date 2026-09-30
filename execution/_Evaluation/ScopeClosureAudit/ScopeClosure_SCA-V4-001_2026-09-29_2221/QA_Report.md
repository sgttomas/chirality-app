# QA — Scope Closure Audit SCA-V4-001 (superseding snapshot)

## Coverage

| Check | Checked | Detail |
|---|---|---|
| Actions | 47 of 47 | Byte-for-byte reconstruction from the accepted packet, compared with the bytes at `102f09c1a` (CA1's basis; all equal) and with the current bytes (SCA-V4-001 text present in every target; differences explained by SCA-V4-002's accepted register and RV returns). 21 Part B rows and 11 B7 mirrors re-checked on current CSVs; 144 `Consolidated_Coverage.csv` rows re-hashed against current documents |
| Downstream reruns | 6 of 6 recommended | 4 COMPLETED (one of them, DAG-002, since superseded by DAG-003), 2 DEFERRED_BY_HUMAN with deciding records. The SETUP_LOG line was also checked |
| `Dependencies.csv` files scanned for orphans | 41 | 826 rows, through `analyze_dep_closure.py` |
| Dependency run records | 41 of 41 | Each deliverable has a run record binding its current `ScopeOfWork.md` hash (11 `…-sca002.md`, 30 earlier) |
| Deliverable `_CONTEXT.md` files checked | 41 | Every non-empty `Deliverables.csv` column value present; 0 mismatches. All 41 `_STATUS.md` unchanged since `67a2fac4b` |
| Supersession | 22 YES rows; 11 + 18 delta rows; 29 map rows | Accumulator check mode, both SCA-V4-001-only and chained; 18 SCA-V4-002 rows verified for path, superseded fact, replacement, ref and applicability |
| KTY remediation manifest rows | 0 | NOT_APPLICABLE (SOFTWARE) |
| `.Archive/` scanner exclusion surfaces | 0 | None present |
| Design files scanned for stale pins | 19 Markdown (37 files under `Design/`) | 17 stale, the same set as CA1 |
| Prior audit input manifest | 389 rows | 341 OK, 48 changed; the changed set is enumerated in `SUPERSESSION_NOTE.md` |

## Tool runs

All tools ran read-only against the working tree at `a254be160` (clean).
Outputs went to this snapshot or to the session scratchpad `CA3/`.

**Registered tools:**
- `tools/coordination/accumulate_supersession_map.py` (`d967144d…`):
  - SCA-V4-001 only (`--delta`, `--check-map`): exit 0, 11 rows, 0 findings;
    output map `e8e43320…a801`, byte-identical to the snapshot map
    (scratch `Expected_Map_SCA001.csv`; findings file `c7312589…`, empty);
  - chained (`--prior-map` SCA-V4-001, `--delta` SCA-V4-002, `--check-map`
    SCA-V4-002): exit 0, 29 rows, 0 findings; output byte-identical to
    `SCA-V4-002/Supersession_Map.csv`. In this snapshot as
    `Expected_Supersession_Map.csv` and `Supersession_Map_Findings.csv`.
- `tools/coordination/analyze_dep_closure.py` (`2b8de3cb…`), run on the
  execution root before DAG-003 was published: exit 0, `orphan_count` 0,
  `orphan_dependencies` PASS, `run_status` COMPLETE. Stdout in the scratchpad
  (`df72522f…`); its `accepted_dag` block equals the recorded currency-2057
  evidence (added arcs and DAG-pending set identical).
- `tools/coordination/audit_dag.py --canonical --strict`: exit 0 on
  `_DAG/DAG-002` and on `_DAG/DAG-003`.
- `tools/scope_of_work/validate_scope_of_work.py`: 16/16 PASS on the current
  bytes.
- `tools/scope_of_work/check_boundary_owner_resolution.py`: 16/16 exit 0.
- `shasum -a 256 -c`:
  - DAG-003 `MANIFEST.sha256` 37/37; `SOURCE_MANIFEST.sha256` 130/130;
  - DAG-002 `MANIFEST.sha256` 37/37; `SOURCE_MANIFEST.sha256` 98 OK / 32
    changed (the expected SCA-V4-002 departure); DAG-001 `MANIFEST.sha256` 61/61;
  - CA1 `INPUT_MANIFEST.sha256`: 341 OK / 48 changed;
  - this snapshot's `INPUT_MANIFEST.sha256`: 491/491 OK at write time.

**Own scripts,** in the scratchpad `CA3/`:
- `verify_pass1_ca3.py` (`cf73647c…`), extending CA1's `verify_pass1.py`
  (`3291e34f…`) with the `102f09c1a` comparison and the SCA-V4-002 explanation;
- `verify_partB.py` (`03aeb822…`, CA1's script, unchanged);
- inline Python for the run-record bindings, the `_CONTEXT.md` mirrors, the
  Design pins, the DL-row checks, the quote check and the E-0203-04 sentence
  survival.

## Limitations

- **Scripts are not in the repository.** They stay in the session scratchpad;
  hashes are above and the methods are stated in the report.
- **DAG state moved during the run.** The node started at `b99df0989`
  (DAG-002 current, DEPARTURE observed); commit `a254be160` published DAG-003
  before this snapshot was written. The analyzer run predates that commit;
  the DAG-003 manifests, strict audit and currency pointer were checked
  afterwards. The snapshot binds the later state; both are disclosed.
- **Pass 1 on shared targets.** Where SCA-V4-002 edited the same file, this
  audit verifies that the SCA-V4-001 text is present and that the change is
  the accepted SCA-V4-002 action (by RV prior/result hashes and diffs). It
  does not re-verify SCA-V4-002's own edits against its packet; that is the
  SCA-V4-002 closure audit's work.
- **Registers not re-extracted under SCA-V4-002** (8 of the 18) bind
  `SOFTWARE_DECOMP.md` at its SCA-V4-001 hash; sufficient for SCA-V4-001,
  noted for SCA-V4-002 (report, Recommendations 4).
- **Design scan.** Substring scan for the four superseded basis-document hash
  prefixes and each deliverable's pre-revision SoW hash prefix over the 19
  Markdown Design files; the 18 non-Markdown files under `Design/generated/`
  were not scanned.

## Self-Assessment

- All passes completed: yes. Passes 0–6 were run; Pass 7 is NOT_APPLICABLE
  with the reason recorded.
- All findings have evidence: yes. Each issue-log row has an `EvidenceFile`
  and a `SourceRef`.
- No silent resolutions: yes. ASC-ISS-001 is closed on cited owner records
  and verified rows, not by re-reading the method; the CA1 snapshot is
  unchanged and its verdict stands as history. The DAG pointer change is
  disclosed rather than folded into the earlier observation.
- Read-only on project state: yes. Only this snapshot and
  `ScopeClosureAudit/_LATEST.md` were written.
- Superseding-snapshot rules: new timestamped folder; `SUPERSESSION_NOTE.md`
  names the superseded snapshot, the reason and the changed inputs; the
  superseded bytes are unchanged (hashes recorded); `_LATEST.md` moved.
