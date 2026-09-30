# QA — Scope Closure Audit SCA-V4-002

## Coverage
- Actions checked: 16 of 16 (register `Amendment_Actions.csv`, sha256 `158702bf…c579d`, verified against the group-2 and group-3 manifests)
- Downstream reruns checked: 9 of 9 recommended (REVISE ×9 runs, UPDATE ×11 runs, currency, DAG-003 successor, audit-decomp, project-setup closing records, Coverage_Telemetry rebuild, Design re-pins, superseding SCA-V4-001 audit)
- Dependencies.csv files scanned for orphans: 41 (820 ACTIVE rows), plus the registered analyzer's snapshot `CLOSURE_APP_V4_SCA002_2026-09-29_2056` at the same register bytes
- Deliverable _CONTEXT.md files checked: 41 for the B-06c line (5 amended, 36 unamended); 12 affected deliverables for Name/PackageID, lifecycle and the DEL-04-01 mirror
- KTY remediation manifest rows checked: 0 (NOT_APPLICABLE, SOFTWARE)
- `.Archive/` scanner exclusion surfaces checked: 0 (NOT_APPLICABLE)
- Supersession: 18 delta rows (paths, refs, override type, fact/replacement substrings), accumulator `--check-map` run to this folder (29 rows, 0 findings)
- Manifests re-run here: DAG-003 `SOURCE_MANIFEST.sha256` 130/130 OK; DAG-003 `MANIFEST.sha256` 37/37 OK; DAG-002 `SOURCE_MANIFEST.sha256` 98 OK / 32 FAILED (the expected departure, superseded)
- Commits bound: `70376aff2` (candidate), `af918ee50` (group 3, H-1..H-4), `1efd4bcda` (REVISEs, B-06a), `8cd783d8d` (registers), `b547125db` (closure/currency audits, DAG-003 candidate), `e995b329d` (V15), `b99df0989` (DECISION-4), `a254be160` (HEAD, DAG-003 published)

## Limitations
- `validate_scope_of_work.py`, `check_boundary_owner_resolution.py` and the `audit-decomp` script were not re-executed; their results are taken from the RV records and `POSTACCEPT/`, whose input manifests bind the audited bytes (V15 reproduced the RV VERIFYs independently).
- The B8 recompute rule over all 144 `Consolidated_Coverage.csv` rows was not re-executed; this audit checked the 31 HOST_INTEGRATION rows directly and that no other row differs from `39c97257b`.
- The Design-file check is a hash-presence scan (no file pins an SCA-V4-002 prior SoW hash or the pre-A-01 HOST_INTEGRATION hash; 7 files pin CA1's superseded basis-document hashes). It does not re-derive CA1's 17-file list; that list is cited as CA1 recorded it.
- The parallel CA3 snapshot was read only for its `_LATEST.md`, `scope_closure_summary.json` and `SUPERSESSION_NOTE.md`; its verdict is reported as written, not re-audited.
- No network; read-only git.

## Self-Assessment
- All passes completed: yes (Pass 7 NOT_APPLICABLE for SOFTWARE; Pass 6 run because row 14 is `SupersessionBindingPresent = YES`)
- All findings have evidence: yes (EvidenceFile and SourceRef on all 8)
- No silent resolutions: yes. The one record/filesystem divergence (the handoff records understating completed propagation) is reported as ASC-ISS-001 with both sides cited; the difference between the amendment's `OPEN_PENDING_DERIVATIVE_CLOSURE` and this audit's `CLOSED_WITH_OBSERVATIONS` is explained in the report header, not merged.
- Snapshot immutable after this write; `_LATEST.md` moved to this snapshot and links the parallel SCA-V4-001 snapshot.
