# D-GOV-16 Stage-2 Evidence-Package Index

Status: `PROPOSAL_EVIDENCE_ONLY — NO STAGE-2 AUTHORITY`

This index assembles the immutable or commit-bound evidence that proves
D-GOV-16 proposal eligibility. It is a derivative package and does not replace
deliverable, decomposition, lifecycle, source, or human-decision truth.

## Bound basis

| Basis | Identity |
|---|---|
| Frozen root main | `2770fda4c63c98ee9f18cffbafd14c9aa59f497f` |
| D-GOV-15 published ruling | `58aa81d62f4a32e3c2d687e4356a1e4be8141674` |
| D-GOV-15 current record including owner checklist addendum | SHA-256 `efd8bb14b7d29e76c53789ccdc795be1b104bd2d6d39f132d4373497e57cd1f5` |
| App pilot | `fb83ffca8a7f674db13c6cda775ca7b7d7c8ef26` |
| Piping pilot | `31c35ea9798c29cd0af16b7089186f3942dcfcb1` |
| Stage-1 schema-freeze record | SHA-256 `cb48d07951f90d52f27d076fdef89f4f3efd9e185311179b2f8c89f5f68e3471` |

## Candidate and proposed successor identities

| Surface | Identity | Meaning |
|---|---|---|
| Frozen measurement standard | SHA-256 `637d45769192c55ca270280c9a67d22b71afe7a1c165535cb663ce8fcaec70dc` | Standard bytes used for the ten conversions |
| Current Stage-1 candidate standard | SHA-256 `8409bf3cebb3af947f54cca9d2e1c0b62445041bf72b81bd8aef912ce9fc0013` | Frozen standard plus owner-authorized deterministic-checklist clarification; schema grammar unchanged |
| Schema marker | `chirality-deliverable-sow/v1` | Candidate parser selector |
| ID catalog | SHA-256 `7a1f8a1251147f7134c50058d633bb242979d2955285ce4a146cc886220be757` | Frozen local-ID membership and migration dispositions |
| Shared parser/validator contract | `tools/scope_of_work/common.py`, SHA-256 `70f0e41360ed70dc6d4ddf89aff094eb9f230bcc7958c8cf26e6c5095ea84bef` | Frozen candidate grammar |
| Deterministic checklist compiler | SHA-256 `60b276b2d8b6497de820ed06d208f7afea9daa0277b20121798abdc4a9ce3ca6` | Owner-corrected REVIEW substrate |
| Proposed ratified standard exact bytes | SHA-256 `7f74290167e3f410242bafe8bca153828a2a93e82099b8498ea6fd90eec85a6f` | Inactive unless D-GOV-16 item 1 is approved |
| Proposed TYPES patch | SHA-256 `9614166c7db8340532d838768be2de52567862757fe0d5add3d3a90edea9d4b4` | Zero-context patch; applies to current `docs/TYPES.md` with `git apply --unidiff-zero --check`; inactive |
| Proposed SPEC patch | SHA-256 `543200af8a617e2f5673db110eef2b0a5cf742c54e70ccda8bce0cad870d4b2e` | Zero-context patch; applies to current `docs/SPEC.md` with `git apply --unidiff-zero --check`; inactive |

The successor standard retains the v1 schema grammar proven by Stage 1 and
changes authority, transition, ISSUED, integration, and retirement language
needed for a post-ruling migration. The proposal does not claim that the
successor bytes were used to generate the pilots.

## Direct Stage-1 evidence

| Evidence | SHA-256 | Proven boundary |
|---|---|---|
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/PRESERVATION_AUDIT.md` | `76456dd15a42528f7948d99eeacee0c78983e5d59ca26c094b353e661650d736` | 325/325 mappings, 3,466/3,466 lines, source/status preservation, outcomes separated |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/STAGE2_ENTRY_GATES.md` | `a8ca42ad1cc725d57084cafb05d8bd3516c7697fffefba2d3bd614db86eaa1a7` | Every amended D-GOV-15 entry gate passes without waiver |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/HANDOFF.md` | `7e75cac2358a9a19217f69cae1e6d2ead0c33465420bcdfe4fb10d09a10412ca` | Proposal eligibility, no Stage-2 authority, material-change trigger |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/RETURN.md` | `4eb7dc27b4e6edc1faf6c84115ece3269b0a7f9d73b2ac8145976d310dc99139` | Terminal RECONCILIATION PASS |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/evidence/DELIVERABLE_INVENTORY.json` | `ef65cfa7bf7ed4e09285a00df20fb575271a825adb3cd1c0617730b08df835fa` | Exact ten-candidate inventory and per-deliverable facts |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/RECON-FANIN/evidence/CONTAINMENT.json` | `20d69858814e46c938a1342c71862a4b67db3c3ab599c279becbe40390b14ca4` | No protected or non-pilot tree mutation |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/HELPS-CHECKLIST/RETURN.md` | `94268880136879215a8c919b04b49d4375d29d9f5c3877c096e5f94cae56a18b` | Deterministic tool and REVIEW exact-consumer contract PASS |
| `execution/_Coordination/AgentRuns/SOW-STAGE1-20260712/instances/HELPS-CHECKLIST/evidence/TEN_PILOT_CHECKLIST_REPRODUCTION.json` | `81a796e3cdb80210ca3300c2d48723cc5cd7372909025de1b873b03c78571a40` | 10/10 byte-identical checklist reproduction |
| Stage-1 sizing report | `ba7921a9cf440e7cbd3d132eb340524e01f2fee223b9025d1ea44f488168e998` | 154 total, ten pilots, 144 remaining at the observed basis |
| Four-document consumer inventory | `6d9492464782577202b9c5c80211898341343daca78a0e4cd4db2b41fb0e80ca` | Active callers, compatibility obligations, historical and independent-schema exclusions |

Evidence paths under `execution/_Coordination/AgentRuns/` are run records;
they are not proposed canon.

## Reservation coverage

| D-GOV-15 reservation | Proposed D-GOV-16 disposition |
|---|---|
| Exact successor standard and schema | Ratify only the exact proposed standard hash; retain schema marker v1 and frozen catalog |
| Exact TYPES/SPEC text | Approve only the two hash-bound patches; apply after ruling through a controlled implementation tranche |
| `INITIALIZED` meaning | Make it format-neutral: selected production contract exists and validates |
| Deterministic checklist/REVIEW | Ratify deterministic compilation and exact REVIEW consumption; human judgment remains at review gates |
| Project-loop adoption | Authorize bounded caller/profile amendments after canon lands; require resolver-driven compatibility checks |
| Pilot candidate integration | Never merge dual-format branches as-is; authorize atomic add-SOW/remove-legacy replacement commits after ruling |
| Remaining 144 | Authorize audited waves only after census refresh and active-caller readiness; no conversion starts from this proposal |
| `ISSUED` handling | Require explicit human administrative representation-replacement approval, exact preservation, and no semantic change |
| Legacy retirement | Retain compatibility until conversion/caller/rollback closure; later evidence-backed owner retirement act required |

## Material-change and rerun rule

No rerun is required at the identities above. A change to any relied-on pilot
candidate, source, `_STATUS.md`, frozen parser/catalog/tool, checklist
contract, or commit invalidates affected evidence and requires scoped
validation, mapping, parity, HTML, checklist, verifier, and RECONCILIATION
fan-in before implementation or a renewed ruling basis.

## Post-closure source-ref disposition — 2026-07-15

After Stage-2 conversion and rollback closure, the human owner approved
removal of the two local-only pilot branch references. The branch-resident
pilot candidates at `fb83ffca8a7f674db13c6cda775ca7b7d7c8ef26` and
`31c35ea9798c29cd0af16b7089186f3942dcfcb1` were intentionally not retained
as durable Git references.

Before removal, current `main` at
`c7e88216baf32acd27e34f3e64851b0918c33a75` was checked against the accepted
conversion-closure corpus. All six App PKG-07 and four Piping PKG-13
production members matched their accepted `_STATUS.md` and `ScopeOfWork.md`
hashes, validated as `SOW_V1`, and contained no legacy four-document files.
The integrated production work is therefore present independently of the
pilot branches.

Historical records above continue to identify the basis actually evaluated
at Stage 1, but direct reproduction from those two source commits is no longer
guaranteed. Mainline Stage-1 fan-in records, Stage-2 successor evidence,
conversion-closure snapshots, and current production contracts remain
tracked. This owner-approved evidence-retention reduction does not change
production scope, lifecycle, semantic acceptance, or the Stage-2 closure
verdict.
