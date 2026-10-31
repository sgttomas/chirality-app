# Current admission full-document receiving — v1

The direct review/change file checker now has an explicitly selected current
entry: `app/examination/admission/current_admission.py --profile current-v1`.
It receives the six full source files in `sources.current-v1.json`, as inspected
at App main `7658f1bea245cb7068b681644aae86f47061ac3f`. It is not a new
EXP schema, result revision, runtime admission, supplier qualification or
acceptance requirement. The legacy reader, rules, source lock, declarations and
frozen publication bytes remain unchanged and separately usable on their
original subjects.

## Exact subjects and changed meaning

| Full input | Original SHA256 | Current SHA256 |
|---|---|---|
| EXAMINATION_PROTOCOL.md | `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` | `c7aa2fcfcc43558cbcf9244aae576b6ad0911ab17aa1a8f52112053969e4cb83` |
| DEL-09-01 ScopeOfWork.md | `8e53669468bd5885739ceaeb633dc5a3b134a04f1bf862235d8d2272dd5f658a` | `a60b02a8cfa40abf1819d08420a94e2539c6b1c83fa3e22f045c079dbaaa65fd` |

The other four source hashes are unchanged: the three EXP-v0.2 schemas and
`prototype/check_exp.py` (`f55ad634…`). Schema IDs, EXP-v0.2 label, prototype
and maintained admission rule bodies retain their original meaning.

The protocol differs in only its current-decision correspondence paragraph
and §13 U-EXP-1. These receive the already-authorized SUP1 advance from the
historical 0.158.0 definition/generation pin to 0.160.0; R23-22's qualification
pin remains candidate-bound to the newest passed version-advance check at build
time. Historical recordings retain their actual pin. No qualified supplier
or App distribution, signing or release evidence is supplied by pin selection.

ScopeOfWork adds the SUP source, carries existing D2/D3 first-increment
reserved-act/routine-permission rulings instead of listing them as undecided,
updates OI-012 consistently, and adds the already merged terms-adoption note.
The first reconciliation is commit `8a8e2d7152ba0a9b720436a4128a52303521b60c`;
`11753a17` only relocated Design to Work. The terms note is `3f4a9114`, integrated
with PR34/37. No REQ-001…008, criterion, rule body or schema changed.

ScopeOfWork was reconciled by inspection and is deliberately NOT edited in
this adoption: its exact inspected `a60b02a8…` bytes are the receiving subject,
and its obligations already cover this implementation. This Work account and
`deliverable.yaml` identify the new entry and checks without making the source
claim circular. A later full-source change requires another deliberate adoption.
Dependency conditions and gates remain unchanged: this receiving implementation
fulfills existing source/record obligations, not a new supplier contribution or
acceptance prerequisite. Historical `Design/` locator strings in the source manifest stay intact; the
maintained `deliverable_path` resolver locates their operational `Work/` files.

## Authority, with original source identity

The following historical artifacts were inspected read-only at
`sgttomas/chirality@727762ed39873685493575138914ddcc89b9ac06`, under
`projects/chirality-app-v4/execution/_Coordination/AgentRuns/`:

| Relative artifact | SHA256 | Received authority/limit |
|---|---|---|
| `APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` | `51190a8e187b05a13e81f27e023ca7c9f5d8ae547c2016aed94ad65fe9785883` | Owner's “update the pinned Codex version to the latest” direction; development evidence, not qualification |
| `APP-V4-GROUP-A-20261004/changes/SUP1.md` | `10360605f7e067d06f621ec2d2199794de402387ab36c9492fb0aa6692fc4a03` | Named 0.160.0 development/definition adoption and preserved qualification obligations |
| `APP-V4-GROUP-A-20261004/reviews/V0-SUP1.md` | `28f811b68ebbd18c24086fc8ec45a05421f2bf29211bf5104e614bab5c697b30` | Independent readiness for that source/propagation scope, not App qualification or release |
| `APP-V4-DESIGN-PASS-4-20261003/R23_RESOLUTIONS.md` | `21b2ccfa0f63d61671eddcebe5c2a41dccd2fc5f901e529808605bd017b3fc11` | R23-22.2 candidate-time qualification-pin rule; changed relied-on behavior returns to owner |
| `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` | `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c` | D2 reserved acts and D3 routine Codex permissions, preserving host-owned lists and operation-specific additions |

DEL-01-01 ScopeOfWork [S] and its generation-correspondence record already
identify this provenance. These are recorded acts at their actual historical
source, not newly authenticated owner acts. The terms note receives the separate
approved applicability disposition, with distribution/replacement still not made.
Historical Root citations are not runtime inputs: ordinary checks need only this
App repository and prepared Python dependencies, never a sibling checkout.

## Selection and compatibility boundary

The current adapter requires the named profile. Its immutable manifest digest
binds the complete source map and exact unchanged legacy reader/rules digests.
It loads those checked code bytes in a private module namespace, so a caller's
`admission_rules` or `admission_check` import cannot substitute different rules.
No shared module is patched. Validation, review and change-join logic execute
through the unchanged `Support(project, manifest)` implementation.

There is no automatic fallback. Missing/unknown/historical profile names,
changed manifests, dependency bytes or any of the six full source files refuse.
A caller cannot replace the source selection with an old lock or rehashed source
map. The current profile on frozen original documents refuses, and the original
profile on changed current documents still refuses. Original historical joins
remain testable with the existing legacy `Support(project=<frozen root>)` API.
The original direct CLI is not silently upgraded to current meaning.

Reports name `exp-current-admission-check/1`, `current-v1`, the manifest/source
and tool digests, read extent, unchanged EXP tuple and actual input identities.
They retain false producer-use/authority/review claims and
`route_admission: not_established`. Records are never rewritten or relabelled;
reported file consistency is not actual review, repair, independence or a human
act. Criterion changes still require their existing matching disposition citation;
the tool does not authenticate it or invent a new approval requirement.

The prior documentary-v3 projections are NOT the basis for this adoption: they
exclude the changed correspondence/U-EXP-1/TBD/SUP/terms-note extents. This
profile deliberately checks full bytes instead. Canonical support, SQ worker,
pre-run/native-form and historical terminal/S4 cohorts continue selecting their
existing frozen reader/source inputs. No transitive pins are renewed here.

## Verification and remaining limits

The existing 16 admission regressions select the current route, including
unchanged positive/negative review/change/schema cases, real file CLI and both
import orders. Example resolution now uses `deliverable_path`, preserving its
historical locator identity. Boundary tests cover both full-document drifts,
missing/tampered/unknown/mixed selections, caller module substitution, immutable
report selection and explicit frozen/current incompatibility. Historical original
joins remain covered; canonical/SQ/pre-run/native-form compatibility is checked
separately without modifying their sources or pins. Focused PR CI includes the
current route and boundary suite; manual full Python coverage retains it too.

Unrelated terminal/S4 stale-source failures are not repaired or hidden by this
work. No supplier/model/native execution, package adoption, publisher identity,
acceptance or release is performed. Existing changed-behavior, qualification,
signing and release choices remain with their recorded owners at the existing
points of need; this technical receiving adoption adds none.
