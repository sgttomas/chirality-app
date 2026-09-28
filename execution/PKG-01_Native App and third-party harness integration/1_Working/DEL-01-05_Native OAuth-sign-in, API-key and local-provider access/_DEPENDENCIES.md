# Dependencies: DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register
- **Status:** COMPLETE — local extraction and mandatory checks passed; no project graph or closure claim.
- **Register:** `Dependencies.csv` — v3.1, 29 canonical columns; 16 ACTIVE EXTRACTED rows: 11 ANCHOR (1 parent, 10 traces) and 5 EXECUTION (4 upstream, 1 downstream). No RETIRED or DECLARED rows.
- **Targets:** 3 DELIVERABLE execution rows, 2 DOCUMENT execution rows; EXTERNAL=0, UNKNOWN=0. The two document locations and decision/definition values remain unresolved.

| ID | Class / type | Direction | Target |
|---|---|---|---|
| DEP-01-05-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 |
| DEP-01-05-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-009 |
| DEP-01-05-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-010 |
| DEP-01-05-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-011 |
| DEP-01-05-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-012 |
| DEP-01-05-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-132 |
| DEP-01-05-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-133 |
| DEP-01-05-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-149 |
| DEP-01-05-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-150 |
| DEP-01-05-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 |
| DEP-01-05-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 |
| DEP-01-05-012 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 |
| DEP-01-05-013 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 |
| DEP-01-05-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 |
| DEP-01-05-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-009 |
| DEP-01-05-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-010 |

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Extraction lifecycle: ACTIVE=16; RETIRED=0. Closure: NOT_APPLICABLE=11 anchors; PENDING=5 execution rows; SATISFIED=0. ProposedMaturity is blank throughout.
- INITIALIZED on local DELIVERABLE targets is only a checked contract threshold. Actual selected protocol/pin, embedding evidence, capability handoff and accountable decision/definition records remain separately required and unclaimed.

## Run Notes
- Method: `chirality-root:bundled:workflow:dependency-extract`; basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; current unchanged setup candidate `ddd721a90ade401d452d102e6e40d1ffdae654eb`, identical-tree integration `82efe62783bbe8ac7d21476a6662195c0b0a7587` as dispatched.
- SCOPE=DEL-01-05; RUN_ROOT=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` (available; canonical companion IDs/labels used).
- SOURCE_DOCS=ScopeOfWork.md; ANCHOR_DOC=ScopeOfWork.md; EXECUTION_DOC_ORDER=[ScopeOfWork.md]; DOC_ROLE_MAP=DEFAULT. Pass 1 produced all 11 anchors before Pass 2 produced execution rows.
- MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE. No prior CSV existed. Human-owned mode/upstream/downstream bytes and prior Run History preserved.
- Declared mirroring: added=0, refreshed=0, retired=0, skipped=2 initial-setup placeholders; no readable declared edges.
- DEL-01-01 rows represent separate actual inputs: protocol/pin and embedding-qualification evidence. DEL-05-01 receives an explicit requirements/limits handoff. Exclusion/ownership lists in REQ-009 create no additional edges.
- OI-009 actual Owner-with-App-implementation-owner choice remains OPEN; OI-010 supported API-key behavior remains OPEN. Their required records are DOCUMENT targets with unknown paths, not invented deliverables. Point-of-need constraints do not prevent honest initial definition or independent work.
- OI-012/DEP-005 selected supplier pin, published protocol and configured endpoint capability evidence remain unresolved. Configured-server/candidate/substitution observations remain required qualification work; product behavior and test steps alone do not establish an external production handoff or provider construction assignment.
- App provider, host model/loop and embedding interfaces remain distinct. Actual human acts, supplier qualification, host conformance, lifecycle advancement, release and adoption are not established here. Account-home choice is not resolved by Root/v3 authentication separation.
- All 16 quotes are verbatim source substrings of at most 30 words with precise loci. Mandatory schema, used enums and supported ID checks passed; one parent; no duplicate rows. Source SHA256 before/after: `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6`. Optional whole-execution EVQ/DRB report not run; local quote/locus/prefix checks passed.
- Exact validation results and source hashes: `_run_records/dependency-extract-20260927.md`. No nonfatal Tree-integrity warnings; unresolved semantic values are retained above.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:23+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available and IDs/labels validated; 16 ACTIVE (11 ANCHOR, 5 EXECUTION), 0 RETIRED; no Tree warnings; OI-009/OI-010/OI-012 and technical-input fulfilment remain unresolved.
