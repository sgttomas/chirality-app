# Active SCOPE_CHANGE Snapshot

**Status:** `OPEN_PENDING_DERIVATIVE_CLOSURE`
**Active snapshot:** `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`
**Amendment:** `SCA-V4-001`, the App v4 basis alignment for owner decisions DEC-4 and DEC-5 (run `APP-V4-BASIS-ALIGN-20260928`)
**Accepted:** checkpoint group 3 on 2026-09-29, DECISION-8 (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/`); groups 1 and 2 on 2026-09-28, DECISION-7 (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/`, `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/`)
**Accepted predecessor:** none (`FIRST_AMENDMENT`)
**Post-acceptance validation:** `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/`

SCA-V4-001 aligns the accepted App v4 basis documents and the decomposition
package with the owner's decisions DEC-4 and DEC-5. It makes 47 `MODIFY`
actions:
- phased checkpoints (V4-WF-05);
- model access by OAuth sign-in or an API key, with no default (V4-HOST-01,
  V4-ARC-11);
- the host-agent network destinations (V4-HOST-02, V4-ARC-12, V4-HI-70);
- "local-first" amended.

Topology is unchanged: 11 packages, 41 deliverables and 262 scope IDs. No
lifecycle state or dependency register changed.

The snapshot is open pending derivative closure. These items remain
separately governed and open:
- the 16 ScopeOfWork REVISEs (`project-setup` INCREMENTAL → `scope-of-work`);
- the dependency-register rows;
- the DAG-001 departure and the DAG-002 candidate (owner checkpoint C);
- `Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by the
  decomposition owner);
- the design re-pins;
- `audit-scope-closure`;
- the follow-on SCA-V4-002, for DEL-10-03 REQ-005.

It makes no release, publication or reliance claim.
