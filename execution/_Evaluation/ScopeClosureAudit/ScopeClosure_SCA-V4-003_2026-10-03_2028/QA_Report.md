# QA — Scope Closure Audit SCA-V4-003

## Coverage
- Actions checked: 23 of 23 (register `Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`, verified against the group-2 and group-3 manifests)
- ScopeOfWork: 147 of 147 accepted blocks parsed from SOW_REVISIONS_A/B at their group-2 hashes and applied in order to the prior blobs at `eff378ffa2`; 19 of 19 results byte-equal to the current files
- Downstream reruns checked: 8 of 8 recommended classes (REVISE ×19, UPDATE ×20 with the FX repair, currency, DAG-004 successor, audit-decomp, project-setup closing records, Coverage_Telemetry rebuild, Design re-pins)
- Dependencies.csv files scanned for orphans: 41 (929 rows, 922 ACTIVE), plus the registered analyzer's snapshot `CLOSURE_APP_V4_SCA003_2026-10-03_1936` (orphan_count 0)
- Arcs recomputed from all 41 registers (ARC_EFFECT rule, Tarjan) and compared with DAG-004 `DependencyEdges.csv` and `CandidateEdges.csv`: equal (129 + 83)
- Deliverable _CONTEXT.md files checked: 20 affected for Name/PackageID; 41 for byte changes since `eaa6a37730` (none)
- _STATUS.md: 20 affected (all IN_PROGRESS); change history since `eaa6a37730` (only the Q-13 act, 6 files)
- Supersession: 1 delta row (path, ref, override type, fact in canonical, replacement in working); accumulator `--check-map` run to this folder (30 rows, 0 findings)
- Modified-entity trace: every `ScopeOfWork.md`, `_CONTEXT.md`, `_DEPENDENCIES.md` and `Dependencies.csv` searched for OI-009
- Design files scanned for SoW pins: 219 (`.md`, `.csv`, `.json`, `.txt` under the 41 `Design/` folders)
- Manifests re-run here: DAG-004 `MANIFEST.sha256` 37/37 OK; DAG-004 `SOURCE_MANIFEST.sha256` 128/130 (the two FX files); DAG-003 `MANIFEST.sha256` 37/37 OK; group-3 `ACCEPTED_MANIFEST.csv` 36/42 equal, 3 status records equal their H-3 finalized hashes, 3 differ by design
- KTY remediation manifest rows checked: 0 (NOT_APPLICABLE, SOFTWARE)
- `.Archive/` scanner exclusion surfaces checked: 0 (NOT_APPLICABLE)
- Commits bound: `fa16393978` (candidate), `388fc730b9` (records), `c8ae213134` (group 3), `a44252d103` (H-1..H-3), `2d5e6845c5` (REVISEs), `0e3c55eec5` (registers), `4ca22437f7` (currency, DAG-004 candidate), `6358ce132d` (V25), `ad16b789ec` (DECISION-3), `c147bb3abe` (DAG-004 published), `90d3a5b6a7` (FX; HEAD)

## Limitations
- `validate_scope_of_work.py`, `derive_review_checklist.py`, `check_boundary_owner_resolution.py`, the register validators and the `audit-decomp` script were not re-executed; their results are taken from RV/, DX/, FX and POSTACCEPT/, whose records bind the audited bytes. The forward application of the accepted blocks was re-executed independently.
- Register row content (quotes, statements, annotations) was not re-extracted; the audit compared output hashes with the DX records, re-derived the arc sets and guards, and checked the FX diff cell by cell.
- The Design-file check is a hash-presence scan for the 19 prior and revised SoW hashes. It did not re-derive the 17-file SCA-V4-001 set; ASC-ISS-007 relies on C-02 and V23b for that and reports what the scan shows.
- The contract's closure statuses do not include `OPEN_PENDING_DERIVATIVE_CLOSURE`; the report explains its relation to `CLOSED_WITH_OBSERVATIONS`.
- During the run another writer added uncommitted lines to 20 `MEMORY.md` files; they are not audited inputs. All audited inputs equal their blobs at `HEAD`.
- No network; read-only git.

## Self-Assessment
- All passes completed: yes (Pass 7 NOT_APPLICABLE for SOFTWARE; Pass 6 run because row 21 is `SupersessionBindingPresent = YES`)
- All findings have evidence: yes (EvidenceFile and SourceRef on all 10)
- No silent resolutions: yes. The record/filesystem divergences are reported with both sides cited: the handoff records understating completed propagation (ASC-ISS-001), DEL-09-02 against Open_Issues and D-021 (ASC-ISS-002), the DAG-004 handoff against C-02 (ASC-ISS-007), and CHECKPOINT_C against the publication route for the CASE-002 update (ASC-ISS-010).
- Snapshot immutable after this write; `_LATEST.md` moved to this snapshot and links the SCA-V4-001 and SCA-V4-002 snapshots.
