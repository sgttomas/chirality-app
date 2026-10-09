# R2-PROOF-01-B2 independent code review and integration

Reviewer: existing TASK /root/group_c_successor/cfb_design_review, separate from
route_persistence author. Read-only source review and focused existing tests;
no source edits, new probes, scratch workaround or new child. Reviewer waited
for the serial Rust window, reused its existing target/offline cache and released
the window when both test processes exited.

## Original blocking finding and exact repair

Original candidate7e1105579cfff5c22d12177cc64964184fb34c3f was NOT READY (P2).
Replacing admission with byte-identical/mode-identical fresh inode after descriptor
replacement at CommitDirectorySync/After or CommitReadback/Before could return
Confirmed(revision2), because final readback validated selected snapshot/descriptor
against cached admission without rechecking its held binding. This is an observed
persistent substitution, not a demand for impossible transient-adversary exclusion.

Author added both maintained tests against unchanged7e core; both failed (0/2),
returning Confirmed. Exact red-core/test/log hashes and small patches are retained
in author basis. Repaired candidatececa6e972fc5224673bc305f82fc51d43cf02368 reuses
existing check_admission after selected-pair readback and before acknowledgment.
Both cases now return Uncertain, retain original Attempt, block retry and perform
no cleanup. Cold reopen may observe revision2 but cannot recreate acknowledgment.
Independent review verified red identities and inspected the minimal repair.

## Final verdict and checks

READY atceca6e972fc5224673bc305f82fc51d43cf02368 for dormant test proof only.
Independent focused default32/32 and distribution-successor32/32 passed.
Measured maximum counted Rust allocation bound418090bytes matches author for
these fixtures. It includes retained capacities plus cumulative requested Rust
allocations, not OS/C buffers, RSS or every possible workload. Author's prior
non-test library check is distinct evidence; no broader library rerun was needed
because production reachability did not change. Exact core SHA-256
f95c3ff233edd319e44155472f1e0da001cd63edeb5b4a10f6baaaf67e71a9f6;
test SHA-25613011add9071741c2ec421745bf63e174269554b473e84f45564ceab08878bbe.

- `/private/tmp/c3-r2-review-default.log` SHA-256 `1454f8c966d52bf0933aee10c00db615b340312a25644998e3e7742ffa48d983`.
- `/private/tmp/c3-r2-review-distribution.log` SHA-256 `ebbb266875d445bac0c5b0b41bcd1f023e5b9bcf87e382fa965d90a507e63f0a`.

Manager integrated unchanged as99d7c246e9. App tree in author and manager is
ca2f9f1ab853906928694b1480af1b349a7013ea. Final combined metadata/head backcheck
and selected CI still precede merge. Earlier B1 source bootstrap omission,
four author identity regressions and entry-budget failure remain in evidence;
their earlier passing suites do not override the later independent finding.

## Proportionality and maintainability

The approximately1753 initial core lines and1139 test lines are broadly justified
by a closed codec, separate bootstrap/admission/commit/read protocols, bounded
POSIX wrappers and actual-file fault schedules. Line count alone is not a defect.
The concrete maintenance weakness was repeated phase identity validation allowing
an omission; reuse of the existing helper is a smaller repair than a new framework.
The reviewed tests exercise filesystem/cut behavior rather than merely echoing
struct fields. The module remains fixture-specific, not a reusable product journal.

A credible simpler future path is to retain codec/transition invariants and fault
regressions as a specification while implementing a separately selected production
mechanism. Retire this test-only module if that design supersedes it; do not keep
a permanent unreviewed dependency simply because a proof exists. Any reuse requires
exact production policy, OS/failure and consumer review. No automatic lib include,
generic shared-helper extraction or production activation is approved here.

## Remaining limits

No production lib/Cargo/Host/AA-CAP/RS/CRP/CAM changes. Dedicated test binary
isolates its allocator. No native/supplier/child-process helper, physical power-loss,
cross-process or hostile-actor qualification; no rollback freshness or product Q
proof. TestBudget is not product policy and no retirement/ID reset is introduced.
Constructed/historical bytes never mint authorship, role, grant, act or performed
duty. This result does not establish App recovery, PM05 sufficiency or90%.
