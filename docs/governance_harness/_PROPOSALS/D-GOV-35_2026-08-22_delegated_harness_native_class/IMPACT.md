# D-GOV-35 Proposed Impact and Conformance Assessment

Status: `CANDIDATE IMPACT ANALYSIS — NO AUTHORITY OR APPLICATION`

Basis: `main@6b0c5219b6a2653e2fc491b1d998abcf78fcf776`

## Authority and artifact classification

`D-GOV-35.proposed.md` and `AGENTS.proposed.patch` are candidate governed
records. This impact analysis is derivative assessment. None is authoritative
unless and until the owner rules and the owning application workflow lawfully
changes the live surfaces. Existing decisions and immutable evidence remain
authoritative or evidentiary only according to their own contracts.

The proposal changes no live instruction, standard, contract, deliverable,
lifecycle, pointer, product source, project loop, hold, or pin. The proposed
patch is intentionally inactive.

## Workflow-Component Design Standard conformance

The proposed design conforms to
`docs/WORKFLOW_COMPONENT_STANDARD.md` as follows, subject to the explicit
normative concordance amendment described below:

| Requirement | Assessment |
|---|---|
| Human authority (R1, R9) | PASS. D-GOV-35 remains proposed; validation and Git acts are not represented as owner acceptance. |
| Runtime classification (§3, R8, R12) | PASS. Native descent is separated from role classification; Agent 2 construction still requires explicit TASK, ephemeral-generalist, or approved dedicated-specialist entry. |
| Explicit delegation and evidence (§4, R8) | PASS WITH CALIBRATION. The two executable classes are named, and native non-delegation evidence is expressly `instruction-asserted`, not mechanism-proven. |
| Capability and containment (§4.1, R3, R16) | PASS. No implicit capability inheritance is introduced; hard outer filesystem/network/process/root/account/policy containment remains required. |
| Epistemic controls (§8, R5-R7, R13) | PASS. The proposal does not overclaim mechanical enforcement and preserves provenance, gaps, and conflict visibility. |
| Handoff and closure (§9, R14) | PASS. Owner ruling, Root application, App WP-06, receiving-loop adoption, validation, and blocker recording remain separate gates. |
| Proportional design (§13, R17) | PASS. The packet supplies only the ruling candidate, inactive exact patch, impact map, and hash/readiness index. |

One ratified sentence is presently inconsistent with live Root doctrine:
`docs/WORKFLOW_COMPONENT_STANDARD.md` section 4.1 says Agent 0 delegates only to
named Agent 1 roles, while `AGENTS.md` permits direct bounded Agent 2 dispatch.
D-GOV-35 proposes to prospectively supersede that sentence with the bounded
Root rule and thereby resolves the normative decision underlying TM-ROOT-126.
The standards file remains byte-identical in this proposal tranche; exact-text
propagation belongs to the post-ruling application tranche. The same tranche
must reconcile the concordant stale statements in `docs/TYPES.md` section 4.3
and `docs/DBM_Agent_Instruction_Architecture.md` section 2 rather than silently
claiming documentary closure.

## Decomposition Standard conformance

`docs/DECOMPOSITION_STANDARD.md` is an external normative constraint, not an
agent or delegation layer. D-GOV-35 does not alter its seven gates, I1-I10,
entity model, identifiers, ledgers, package roles, or accepted decomposition
truth. The proposal is therefore **conformant / no normative decomposition
delta**. It preserves I1 human validation, I2 no invention, I8 traceable
rationale, and I9 ledger/telemetry separation by treating the proposal and
impact map as candidate/derivative artifacts rather than decomposition truth.

## Direct downstream authority and implementation surfaces

| Surface | Current relation | Required follow-on if ruled |
|---|---|---|
| D-GOV-14 item 7 | RULED; broader sole-executable-path clause | D-GOV-35 supersedes only the exclusivity clause; legacy SDK bridge retirement survives. |
| Root `AGENTS.md` | Live doctrine, SHA-256 `268becd0bac9da8421b30089e4e4167a5e5f79bf3892d0f72ad41a63180a3aeb` | Apply the separately reviewed patch only in the authorized instruction tranche. |
| `docs/WORKFLOW_COMPONENT_STANDARD.md` §4.1 | Ratified D-GOV-14 text, SHA-256 `5de31f552bea356629ad29af9bc664f33d49392d1c63fc2fb4dc70614abd7df9` | Propagate the ruled Agent 0 direct bounded-Agent-2 semantics; preserve the standard as external, not an agent. |
| `docs/TYPES.md` §4.3; `docs/DBM_Agent_Instruction_Architecture.md` §2 | TM-ROOT-126 concordance evidence | Reconcile to the ruled hierarchy wording in the application tranche or record an explicit blocker. |
| App `docs/CONTRACT.md` K-SUBAGENT-1/2/3 | App authority; managed-child enforcement claims | App loop distinguishes managed vs native evidence and records the instruction+config assertion boundary. |
| D-APP-68 disposition 4 | RULED App transcription of D-GOV-14 item 7 | App loop prospectively amends through its own instrument; immutable D-APP-68 remains historical authority and is not rewritten. |
| DEL-08-04 `ScopeOfWork.md` | Live App deliverable SOW for managed-delegation admission | App WP-06 adds the native class and parity/evidence requirements without moving DEL-08-05 record ownership. |
| `subagent-governance.ts:205-213` | Requests for untyped/generalist delegation that reach the existing governance gate are denied; file SHA-256 `2b2d750be8fb3974593599631f64f920bc3b3fd4512640545bf1a22e61ec215c` | App WP-06 determines and implements the native-class integration and tests; no Root code write. |

## Pinned and mirrored downstream surfaces

The inventory below applies the notice discipline of root `AGENTS.md`'s
agent-index change-notice rule. This tranche does not edit `agents/**`, but the
same detection-plus-notice discipline is applied because it proposes a root
instruction-index/runtime-doctrine change consumed by App and Piping.

### Chirality App loop

- **Live corpus (not a detector for this change):** the App authority-reference
  corpus at
  `projects/chirality-app-dev/execution/_Reconciliation/References/AUTHORITY_CORPUS.json`
  is currently `v18` and does **not** contain root `AGENTS.md`. It is therefore
  not an active detector for this particular byte change; any corpus expansion
  or version bump is App-owned.
- **Live generated mirror:** App's packaged instruction-root path actively
  mirrors root `AGENTS.md` into the desktop/runtime bundle. The governing
  implementation surfaces are
  `projects/chirality-app-dev/frontend/package.json` (the `extraResources`
  instruction-root payload) and
  `projects/chirality-app-dev/frontend/scripts/verify-instruction-root-integrity.mjs`
  (required root file and source-to-bundle SHA comparison). A post-ruling App
  candidate must rebuild and verify rather than manually repin generated bytes.
- **Root-owned mutable/stale downstream Chirality App projection:**
  `exports/chirality-app/export-manifest.csv` pins the accepted Root
  `AGENTS.md` bytes in the tracked public-release projection. It is a stale
  derivative, not App-loop authority and not immutable historical evidence.
  Its governing regeneration profile is
  `exports/chirality-app/export_public.py`. A later authorized instruction
  application handoff must regenerate the projection through that owning
  export workflow or record an explicit deferral. N1 neither edits nor
  regenerates the export.
- **Historical/immutable exact-hash pins:** an exact search for the accepted
  Root `AGENTS.md` SHA identifies the following App evidence surfaces:
  - `projects/chirality-app-dev/execution/PKG-09_Validation_Packaging_Security_and_Release/1_Working/DEL-09-06_Network_Key_Attachment_and_Renderer_Security_Checks/Evidence/Packaged_Security_Proof_2026-08-20/instruction-root/manifest.json`;
  - `projects/chirality-app-dev/execution/PKG-09_Validation_Packaging_Security_and_Release/1_Working/DEL-09-06_Network_Key_Attachment_and_Renderer_Security_Checks/Evidence/Packaged_Security_Proof_2026-08-20/instruction-root/summary.json`;
  - `projects/chirality-app-dev/execution/PKG-09_Validation_Packaging_Security_and_Release/1_Working/DEL-09-06_Network_Key_Attachment_and_Renderer_Security_Checks/Evidence/Packaged_Security_Proof_2026-08-20/Remediation_01/instruction-root/manifest.json`;
  - `projects/chirality-app-dev/execution/PKG-09_Validation_Packaging_Security_and_Release/1_Working/DEL-09-06_Network_Key_Attachment_and_Renderer_Security_Checks/Evidence/Packaged_Security_Proof_2026-08-20/Remediation_01/instruction-root/summary.json`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_DAPP86_HELPER_PARITY_RERUN_2026-08-20/instances/A2-PKG02-PARITY-EXECUTOR-01/evidence/baseline/SOURCE_MANIFEST.sha256`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_DAPP86_HELPER_PARITY_RERUN_2026-08-20/instances/A2-PKG02-PARITY-EXECUTOR-01/evidence/baseline/PACKAGE_MANIFEST.sha256`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_DAPP88_HELPER_BUNDLE_RESUME_R3_2026-08-04/instances/A2-DAPP88-R3-DIAGNOSE-02-R2/evidence/packages/single/FILE_HASHES.txt`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_DAPP88_HELPER_BUNDLE_RESUME_R3_2026-08-04/instances/A2-DAPP88-R3-DIAGNOSE-02-R2/evidence/packages/standard/FILE_HASHES.txt`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_DAPP88_HELPER_BUNDLE_RESUME_R3_2026-08-04/instances/A2-DAPP88-R3-IMPLEMENT-02/evidence/PACKAGE_MANIFEST.md`;
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_PARITY_INSTRUMENT_2026-08-03/instances/A2-PARITY-EXECUTOR-01/evidence/baseline/PACKAGE_MANIFEST.sha256`; and
  - `projects/chirality-app-dev/execution/_Coordination/AgentRuns/APPDEV_LOGIN_PROOF_R16_STAGING_2026-08-22/instances/WI-PKG09-R16-STAGING-01/executor-attempt-2/integrity-evidence.log`.
  These files are evidence of their recorded candidates, never live mirrors;
  they must not be rewritten. App decides whether a new candidate needs new
  evidence.
- **Historical corpus/process-input snapshot:**
  `projects/chirality-app-dev/execution/_Reconciliation/DeliverableConcordance/RUN_D55_CONCORDANCE_2026-07-11_1904Z/AUTHORITY_MAP.md`
  classifies root/project `AGENTS.md` as `FROZEN_PROCESS_INPUT` for that
  source-state-bound run. It is immutable evidence, not current authority or a
  live pin, and must never be rewritten.
- **Semantic mirrors and authority surfaces:** the App-local `AGENTS.md`,
  D-APP-68, K-SUBAGENT contracts, DEL-08-04 SOW,
  DEL-08-05 record contract, and runtime governance code semantically mirror
  parts of the Root delegation contract. They require App-owned assessment and
  prospective amendment; Root does not write them.

### Chirality Piping loop

- **Live corpus/pin search:** no active Piping authority-reference corpus or
  executable SHA-pinned contract
  mirror containing Root `AGENTS.md` was identified. Piping's local
  `projects/chirality-piping/AGENTS.md` imports Root delegation semantics by
  reference and is therefore a **live semantic mirror** requiring local
  assessment.
- **Historical/immutable exact-hash pins:** Piping run-basis evidence pins Root
  `AGENTS.md` SHA-256
  `268becd0bac9da8421b30089e4e4167a5e5f79bf3892d0f72ad41a63180a3aeb`
  in:
  - `projects/chirality-piping/execution/_Reconciliation/DeliverableConcordance/TM_PIP_038_040_TREATMENT_2026-08-09/RUN_BASIS.md`;
  - its
    `OWNER_RULING_2026-08-09_TM_PIP_038_040/RUN_BASIS.md`; and
  - `projects/chirality-piping/execution/_Coordination/_TaskManagement/TM_PIP_040_CLOSURE_PROPOSAL_2026-08-09/RUN_BASIS.md`.
  These are immutable provenance for those runs, not live mirrors, and must not
  be rewritten or treated as adopting D-GOV-35.
- **Historical corpus/process-input snapshot:**
  `projects/chirality-piping/execution/_Reconciliation/DeliverableConcordance/DELIVERABLE_CONCORDANCE_2026-07-11_1305/AUTHORITY_AND_SOURCE_RELIABILITY_MAP.md`
  identifies root `AGENTS.md` as `FROZEN_PROCESS_INPUT` for its frozen run.
  This map is immutable run evidence, not a live mirror or authority, and must
  never be rewritten.
- Piping owns whether to acknowledge the notice, assess local delegation prose,
  or create a new accepted run basis. No Piping product, register, lifecycle,
  DAG, or authority change is implied.

## Required routed notices after ruling

The Root application tranche must route one coordination notice to the App
coordination surface and one to the Piping coordination surface. Each notice
must identify the pre/post Root `AGENTS.md` SHA-256, describe the two delegation
classes and the `instruction-asserted` evidence boundary, list the relevant
pinned/mirrored surfaces above, and state the receiving loop's follow-on.
Notices are coordination, not authority; receiving loops adopt, amend, decline,
or defer under their own instruments and cadence.

## Non-effects and blockers

- D-GOV-35 still requires an owner ruling.
- The Root instruction application tranche is blocked on that ruling.
- App contract/SOW/code/test changes are App WP-06 work and require App-loop
  authority; no App file is changed here.
- Historical corpus snapshots, packaged evidence, run bases, D-GOV-14, and
  D-APP-68 are not overwritten.
- No current hold, lifecycle, pointer, pin, release, publication, or merge gate
  is lifted.
