# F-VC09-01 — bounded DEL-09-01 source-owner correction proposal

Status: PROPOSED only. Recommended named change: **CC-EXP-IN5-01**.
Source basis: `7262736ab1315e611426a5f012caef78c0ee64c2`.
Original finding remains open. This packet neither repairs canonical bytes nor
adopts a clarification, changes pins, closes VC09 or qualifies a route.

## Controlling meaning and custody

This is the delegated DEL-09-01 technical source-owner assessment by TASK
`/root/group_b_successor/support_identity`, under WORKING_ITEMS
`/root/group_b_successor`. Parent explicitly authorized a proposal and requires
independent review before any canonical change. It is not a personal owner
ruling or an independently reviewed Design stance yet. Proposal-format is the
selected method; exact context/source hashes are in SOURCE_BASIS.json.

The sources establish a narrow answer, not two equally permissible outcomes for
an absent package:

1. R23_RESOLUTIONS.md R23-20 (INTEGRATION) distinguishes planned/unattempted
   `not-run` from attempted-at-start-or-later `blocked`, with a stated cause.
   This general rule permits blocked at case start; this proposal preserves it.
2. RV-EXP-U1.md EXP-R-C/P1 found the packaged-without-package loophole. Its repair
   confirmation (lines198–199, CONFIRMED READY) expressly confirms the schema's
   native_packaged conditional for **every outcome except not-run**, and identifies
   EXP-EX-04 as not-run with the missing package, consistent with R23-20.
3. Published EXP-v0.2 §3.5 EXP-R2, §6.1 and §9 NB-3 state the same specific
   exception. NB-3 says without a package the case is not-run. Before a candidate
   is named, §6.1 lists missing input without a fabricated result. Once planned
   for a named candidate, the honest not-run record is required.
4. Source correspondence checks confirm the current protocol, result schema and
   valid examples match their bytes at publication merge
   `09106477e351c6e5bde85259c55a00cc8fc5f7f5` (PR1077). METHOD.md independently names
   that publication. Review confirmation and publication are distinct evidence;
   this does not authenticate the historical human/chat act.
5. IN-5's blanket “Native packaged route blocked” when its bundled input is
   absent is therefore an unreconciled shorthand, not permission to bypass the
   more specific published rule. Package present plus an attempted case stopped
   by another stated prerequisite can still be blocked. A route unavailable and
   not attempted is not-run (NB-2). A failed actual evaluation remains fail.

Changing the rule to admit a native_packaged blocked result without a package
would reopen EXP-R2, NB-3, its schema repair and receiving criteria. That is a
consequential new rule proposal, not an alternative reading authorized by IN-5.
There is no source warrant to choose it or ask the owner to decide it merely to
repair this text. If a later reviewer identifies a contrary accepted disposition,
stop the affected correction and present that exact conflict; do not normalize it.

- PROPOSAL: Publish a separately identified IN-5 clarification without mutating frozen support
  - Evidence: EXP IN-5 against §6.1/NB-2/NB-3/EXP-R2; R23-20; RV-EXP-U1 repaired EXP-R-C; published schema/example correspondence; METHOD Authority/Selection and source publication clauses.
  - Change: Prepare `Design/clarifications/CC-EXP-IN5-01.md` as **EXP-IN5-CLARIFICATION-v1**, explicitly bound to the unchanged EXP-v0.2 protocol hash. It must identify IN-5's missing-package wording as the corrected reading, reproduce the exact proposed If-absent replacement in PROPOSED_TEXT.patch.txt, preserve the general attempted-blocked rule, and state its separate reviewed technical adoption boundary. The manager propagates that source to actual consumers before they claim the clarified reading. Do not apply the row patch in place to the frozen published protocol or repoint existing pins. Independent source review precedes any adoption.
  - Why: Correct the source interpretation while preserving every historical support identity and the already-correct schema/consumer behavior.
  - Risk: An additive clarification can be overlooked by a reader selecting only the old protocol. Therefore its adoption notice must name the affected consumers and exact source identity; it cannot silently be considered part of existing canonical selection. A later consolidated protocol revision needs an explicit successor publication and receiving plan.
  - Status: PROPOSED

## Minimal text and route consequences

PROPOSED_TEXT.patch.txt shows exactly one cell replacement in IN-5; every other
cell remains unchanged. It is conceptual successor text, not an executable
instruction to modify the frozen file. The preferred additive clarification
carries those words until an explicitly reviewed consolidated successor is chosen.
R23-21 requires changed rulings to get a new superseding ID; this proposal does
not revise R23-20 or claim its ID for new semantics. The clarification has its own
name/version and retains the prior source. It adds no new EXP record fields.

COUNTEREXAMPLES.json contains four complete derived illustrative record values
and actual schema results: missing-package not-run valid; missing-package blocked
invalid even if an attempt is asserted; existing-package attempted blocked valid;
missing-package pass invalid. These are schema checks, not proof that a package
or attempt occurred. The pre-candidate no-record case is described separately;
no blank or fictional candidate record is minted for it.

The proposal does not admit a runner, supply M1, create M2/package content, perform
install/launch or supply M3. native_development remains separate and is not forced
packaged. Existing schema checks still refuse false package claims. A record's
schema-validity or not-run label is not supplier/reference qualification, S3,
owner action, current reliance or acceptance. A present package does not itself
prove an attempted native case or its prerequisite witness.

## Consumer impact and prospective adoption

Exact source-lock paths and hashes are retained in SOURCE_BASIS.json.

| Consumer | Current dependency and consequence of in-place protocol edit | Required treatment for this proposal |
|---|---|---|
| `app/examination/check.py`, `admission/admission_check.py` | Their sources.json files pin EXP protocol; drift refuses | Preserve files/pins and already-correct schema behavior; receive clarification notice |
| Proposed legacy support identity and canonical EXP/PKG | declaration.v1.json pins protocol; canonical reader/declaration depends on the fixed legacy/full publication closure | Keep all old declarations and source identities; do not relabel corrected bytes as the original published tuple or silently mutate six-role selection |
| SQ receiver | sq_receiving/pins.json directly pins protocol and canonical dependencies | Existing missing-package exception stays; any claim to consume the new clarification requires its own explicit source adoption, not a global pin refresh |
| B7 preparation and native forms | standalone sources.json and pre_run_inputs.pins.json pin protocol; native form wrapper also fixes underlying helpers/source manifests | Preserve exact historical plan/form/pre-run checks. A separately selected clarification must not change blank forms into execution records |
| S4 receiving | Indirect dependency through unchanged canonical EXP/PKG closure; current Host source mismatch remains a separate known hold | No S4 renewal, invented current export or qualification follows. Preserve prior cohorts/limits |
| Journey/PKG record producers and examiners | Rely on EXP outcomes, even where no executable pin exists | Notify DEL-01-06 and EXP OUT-1…6 receiving owners of exact clarification and not-run/blocked boundary; owners assess any actual record affected |

For an actual prior record that relied on the wrong IN-5 wording, use EXP §6.2's
case-specific impact assessment and preserve its old evidence. Do not assume such
a record exists from this textual defect or rewrite historical records. A source
clarification cannot retroactively establish that a producer read it.

MISSING:
- Independent review of this source-owner stance and precise correction proposal.
- Named technical adoption/source publication and affected consumer dispositions;
  these are future work, not supplied by this packet. No actual misclassified
  native record was supplied; its existence is not invented.

NEEDS_HUMAN_RULING: none on the demonstrated current meaning. A future proposal
to relax EXP-R2 or alter qualification/owner rights would be a separate consequential
change; this assignment does not propose it. Technical owners still must review
and select the additive clarification before it becomes an adopted source.

DEPENDENCY_NOTES:
- DEL-09-01 owns the correction; DEL-01-06 and EXP receiving journey owners own
  their adoption and affected records. Manager owns notices, graph and acceptance
  coordination. Source hashes, independent review and any later Git merge are
  separate from an actual owner/product decision.
- No canonical protocol, schema, prototype, pin, code or MEMORY is edited. No
  implementation, build, native/supplier action, download or new agent/worktree.
- Original F-VC09-01 remains open; no repair, schema-level admission or VER pass is
  claimed by proposing replacement wording.
