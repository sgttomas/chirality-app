# D-GOV Register — Governance Harness Decisions (**RULED 2026-07-01**; published, SHA-bound)

All seven decisions were ruled by the owner in-session on 2026-07-01
("All as recommended") and published by CHANGE in commit `82a35c545`
(2026-07-01; the Ruling SHA was backfilled into the records by `f1549afb1`).
Per K-AUTH-1 the rulings are the owner's acts, recorded here; per K-AUTH-2 each
is bound to that publication commit's git SHA (D-GOV-02 conditional severity is
satisfied). Canonical per-decision records: the `D-GOV-01..07_*.md` files in
this directory — this register is a navigational summary; on any disagreement
the records govern.

| ID | Decision | HumanRuling | Unblocks |
|---|---|---|---|
| D-GOV-01 | Substrate authority | **RULED: Option A** — files as sole governance authority; projection-only databases; guard-only write interventions; engine stores exempt via K-DOMAIN-1; supersession clause in force | The v3 architecture; procedural closure of the thrice-flipped fork |
| D-GOV-02 | Severity & override | **RULED: adopt as drafted** — five severities, exit codes, observation-boundary caveat, conditional SHA-TBD, no non-overridable block on issuance | Exit-code contract in PR 1; later CI wrapping |
| D-GOV-03 | Pilot scope | **RULED: as recommended** — app-dev + piping + `_DomainEngines/` read/report; `domains/*` deferred | Bounded first release |
| D-GOV-04 | Human actor identity | **RULED: as recommended** — committed allowlist; refuse (exit 2) absent it; adopted briefs committed | Attribution checks; BLOCK-capable scope checks |
| D-GOV-05 | Minimal governance basis | **RULED: Option A** — ratify minimal harness basis now; full root ratification on its own track; trailer grammar rides this | Enforcement claims on a ratified minimum |
| D-GOV-06 | `open_pipe_stress` current truth | **RULED: affirm ADOPTED** per the 2026-06-21 Gate-2 ruling; CHANGE-published cleanup of the six contradicting surfaces directed | Resolves the drift exemplar; first live self-check fixture |
| D-GOV-07 | Domain gate SHA binding | **RULED: as recommended** — bind to content SHA-256 *and* git SHA; existing acceptances grandfathered WARN | Deferred domain-shape verifier prerequisite |
| D-GOV-08 | Epistemic vocabulary operationalization | **RULED: Option B** — warrant ladder audit-time diagnostic; FACT optional; TYPES §10.5 + thesis ch.5 corrections directed; review-severity enum registered | `TYPES.md` §10.5 / thesis ch. 5 corrections at ruling; registration of the review-finding severity enum; `evidence-check` semantics |
| D-GOV-09 | Full root governance ratification | **RULED 2026-07-11: owner act transcribed** — all root `docs/` governance ratified in full (executed in PR #173, merge `73a0cb79b`); completes the D-GOV-05 "full ratification on its own track" track; D-GOV-05 subsumed, not amended | Harness ratification-label propagation (PR #174, all 27 K-* RATIFIED); removal of the automatic DRAFT advisory cap (severity still governed by D-GOV-02); amendments of ratified canon under owner direction |
| D-GOV-10 | Workflow-component architecture normalization | **RULED 2026-07-11: all recommendations accepted** — split the normative standard from HELPS_HUMANS; distinguish semantic approval from authorized routine Git closeout; require all Type 2 agents to requalify; isolate implementation from active reconciliation lanes | New workflow-component standard; HELPS_HUMANS persona rewrite; agent disposition audit and staged migration |
| D-GOV-11 | Runtime agent hierarchy and role ownership | **RULED 2026-07-11** — HELP_HUMAN is sole Agent 0 Supervising Architect; Agent 1 supports direct and nested entry; Agent 2 supports TASK, ephemeral generalist, and approved dedicated-specialist forms; EVALUATION absorbs legacy reconciliation-audit semantics; RECONCILIATION is recreated for deliverable concordance; PDF2MD/DRAWING_EXTRACT remain Agent 1 | Supersedes conflicting D-GOV-10 hierarchy and role-disposition claims; governs instruction refactor and later runtime bridge |
| D-GOV-12 | Multi-agent orchestration and package-level WORKING_ITEMS | **RULED 2026-07-11** — terminal fan-out/fan-in and supervised many-to-many agency are complementary; humans may prescribe or delegate pattern selection; HELP_HUMAN manages cross-package work; WORKING_ITEMS manages one package and its Agent 2 work graph | Extends D-GOV-11 with live parent-mediated coordination, package-level WORKING_ITEMS, work-graph persistence, and software-profile-first qualification |
| D-GOV-13 | Dedicated Agent 2 requalification | **RULED 2026-07-12: APPROVED through D-GOV-14 item 4**, published at `d22f80bf5d6c1190ce151df75d936bfcf4d38bc3` — retain 14 dedicated specialist packages whose stable output/recovery contracts and live compatibility references exceed a generic brief | Named execution permitted only through declared hierarchy, context, tool, permission, and write-scope gates; replacement-first consolidation remains available |
| D-GOV-14 | PR #188 review closure | **RULED 2026-07-12: all nine items APPROVED**, published at `d22f80bf5d6c1190ce151df75d936bfcf4d38bc3` — ratifies three standards, approves D-GOV-13, confirms SCHEDULING and legacy-bridge retirement, K-AGENTS interpretation, public boundary, and revised active-proto-run carve-out | Hold PR #188 merge until proto-run handoffs integrate, branch rebases, and full validation passes |
| D-GOV-15 | Deliverable Scope-of-Work Stage 1 | **RULED 2026-07-12: all nine items APPROVED**, published at `58aa81d62f4a32e3c2d687e4356a1e4be8141674` from proposed snapshot `c4c5dd2df0d7b5424d48672c38d1eef37262e2f6`; owner directed publication without pilot implementation in the ruling session; owner-authorized 2026-07-12 addendum assigns candidate `AC-*` checklist compilation to a registered deterministic tool and limits REVIEW to exact consumption plus human-gated judgment | Authorizes candidate machinery and exact isolated PKG-07/PKG-13 pilot variance, lifecycle/content neutrality, qualified native orchestration with sequential fallback, RECONCILIATION preservation audit, fail-closed abort, and Stage-2 gates; repeated agentic checklist extraction is not a gate; exact TYPES/SPEC ratification and remaining-corpus conversion stay reserved for D-GOV-16 |
| D-GOV-16 | Deliverable Scope-of-Work Stage 2 | **RULED 2026-07-12: items 1–10 APPROVED exactly as proposed**, proposed snapshot `31e5efd985db4cc7b25543e11a65933979e07e4f`; published at `7584718aa32b112e415331736d1a8e68c12ac176` | Ratifies the exact successor standard and approves the exact queued TYPES/SPEC patches, deterministic checklist/REVIEW boundary, single-format/lifecycle transition, bounded remaining-144 conversion, ISSUED protocol, atomic pilot replacement, acceptance/abort/rollback gates, and later human-gated legacy retirement; owner-directed stop requires a fresh governed orchestration plan from synchronized `main` before Stage-2 implementation |
| D-GOV-17 | Canonical model-capability doctrine and related dispositions | **RULED 2026-07-18** — M1-D (owner-formulated: no durable model/capability doctrine anywhere; per-session steering supplies it; minimal model-agnostic attribution evidence rules survive), M2 floor-plus-corrections (a validator finding may never mechanically reject owner-ruled content; all other boundary cases discovered via recorded supersede-never-edit exception entries), M3-A (centralized SOW conversion manifest canonical; no local backfill), M4-A (MEMORY template revised to codify practice); ruling verbatim + SHA-256 `411a5956d97ee94365fbfc92d931a51aa0f24870f6243208dd004247bf15e12b` in the decision record | Staged doctrine package retained as historical record, never placed; app-dev `AGENTS.md` attribution rewrite executes as a project-fenced follow-up micro-tranche; capability never confers authority (K-AUTH-1) regardless of steering content |
| D-GOV-18 | Agent-index re-disposition (ORCHESTRATOR, EVALUATION, CHANGE, control-loop functions) | **RULED** — "I APPROVE D-GOV-18 items 1–8 at commit 9a900b3b76dda415cc4d41185350eb2e5a436302" (owner, 2026-07-21; run `AGENT-INDEX-REDISPOSITION-20260721`, basis `main@0c066652cd527eb1559f715e914262d2bda42602`) — proposed items 1–8: (1) ORCHESTRATOR → PROJECT_SETUP rename/narrow to setup + estimation; (2) EVALUATION realized as thin Agent 1 shell + `evaluation-protocol` skill (full demotion structurally infeasible); (3) control-loop Function 5 → HELPS_HUMANS, Function 3 stays; (4) CHANGE slim-to-authority now, `change-method` a future Reuse Candidate; (5) REVIEW/SCOPE_CHANGE ruled SAFE, future-slim only; (6) App Dev couplings deferred to the App Dev loop by owner consent; (7) scope-not-granted enumerated; (8) five sequential PRs (PR-0 ruling; PR-1 CHANGE; PR-2 EVALUATION gated on App Dev EVALUATION fan-in; PR-3 atomic rename incl. validator keys; PR-4 F5 move) | On ruling: supersedes the D-GOV-11 matrix rows ORCHESTRATOR (RETAIN/EXPAND) and EVALUATION (EXPAND); records the first CHANGE slim tranche; no lifecycle act, specialist removal, machinery retirement, or historical-evidence rewrite. Implementation proceeds through the Item 8 PR sequence, each merge human-approved |
| D-GOV-19 | Chirality framework: knower and accountability | **RULED 2026-07-23** — owner approved exact candidate `981149df247fb6564768f8451e3b12dd591d9197`; information as externalizable substrate; knowledge as situated, potentially mistaken or revisable achievement of a knower; relational SHA/scope/purpose-bound authentication; the permanent accountability gap as the sole primary chirality of knowledge; configurational multiplicity as the operative term; quantum superposition confined to a non-foundational Appendix D analogy | Authorizes a concordant `CHIRALITY_FRAMEWORK.md` Revision 3 and thesis revision; exact later prose, merge, and publication remain separately owner-gated; no operational-interface change, thesis authentication, external-publication apply, or domain-snapshot amendment |
| D-GOV-20 | Shared runtime authority, project registration, and local-agent pilot | **RULED 2026-07-22; reconciled to next-free ID 2026-07-23** — owner explicitly instructed implementation of the accepted Shared Runtime and Local-Agent Pilot: promote the app harness to a root-owned runtime, use one per-user headless daemon as the exclusive engine/session/credential/delegation/tool/residency owner, preserve checkout-contained project truth, and keep agent roles model-independent | Authorizes the bounded shared-runtime governance and implementation sequence; root runtime/export work, app extraction, domain convergence, and PEC migration remain separately fenced by D-APP-73, D-T0-23, D-PEC-56, and SCA-APP-003 |

Note (2026-07-01): with D-GOV-08 the register extends to root-governance
vocabulary decisions framed by the harness family; the RULED banner above
covers D-GOV-01..07 only.

## Completed

1. **CHANGE publication** of the decision set + `PLAN_INDEX.md` — commit
   `82a35c545`, 2026-07-01 (Ruling SHA backfilled into the records by
   `f1549afb1`). This is what SHA-bound the rulings.
2. **`docs/PLAN.md` adoption** — maintainer applied the proposed roadmap edits
   reflecting ruled status, 2026-07-01.
3. **D-GOV-06 cleanup slice** — CHANGE-published correction of the six
   contradicting surfaces (2026-07-01): the `RULINGS_PUBLISHED.md` stale
   closing paragraph; both halves of the `DOMAIN_ENGINE_INDEX.md` banner; the
   profile YAML header comments plus the `open_issues` "Profile stays DRAFT"
   entry; the file renamed to `profiles/open_pipe_stress.yaml` (validator
   re-run: VALID, report regenerated by the tool); D-T0-06's stale HumanRuling
   line annotated; the `_DomainEngines/_LATEST.md` framing reworded. Its diff
   is the harness's first live self-check fixture. Three residual stale
   surfaces outside the six ruled ones were **deliberately retained by owner
   ruling (2026-07-01) as live self-check test material** — the harness must
   catch them; do not clean them up: the `DOMAIN_ENGINE_INDEX.md` layout-tree
   annotation "(PROPOSAL; HumanRuling = TBD)"; the D-T0-06 title line carrying
   the same tag; and the RULINGS_PUBLISHED.md action-flow line "Update the
   DRAFT profile per rulings."
   *Note (2026-07-02): these three are a retained floor, not the complete
   live-finding inventory — see Completed item 11. The other seven D-T0 title
   tags and all eight `Ruling SHA: TBD` fields were genuine post-ruling drift,
   cleaned and backfilled at owner direction; the three surfaces above stay
   byte-identical and `self-check` still catches them (now pinned at
   STALE_RULING_ANNOTATION=2, TITLE_CONTRADICTS_RULING=1, STALE_DRAFT_DIRECTIVE=1).*
4. **`human_actors` allowlist** per D-GOV-04 — created at owner direction,
   `docs/governance_harness/human_actors.md` (2026-07-01); identity checks
   refuse (exit 2) absent it.
5. **First PR** per plan v3 §First PR — landed 2026-07-01 at owner direction
   (PR #1, merge commit `71a67d0b1`): `tools/practitioner_harness/` (charter,
   adapter manifests + loader, `prose-bullet-v1` parser with caveat classes,
   `status` three targets, `drift`/`self-check`, `brief` CANDIDATE-only) and
   the `write_status.sh` precondition guard (canonical file; regenerated
   export copy byte-identical), reconciled with the `transition.ts` prior art
   (divergences recorded in the charter). Verified at merge: `drift` measures
   92/154 (all 92 in piping) against the recorded baseline; `self-check`
   detects the three retained stale surfaces of item 3; 110 tests pass.
6. **Phase 2 (fixtures + self-check hardening) — complete** per plan v3
   §Roadmap Phase 2, landed across four PRs at owner direction (2026-07-01,
   except PR #5 on 2026-07-02): PR #2 (merge `cf5fae242`) added the
   adversarial archive-fixture corpus (verbatim pre-images from
   `git show 15c958e06^`, re-anchored to a synthetic home prefix) plus the
   `STALE_OPEN_ISSUE` and `DRAFT_BASIS_AS_BINDING` detectors; PR #3 (merge
   `12894ad3f`) added the GEN-7 `_LATEST` pointer-currency self-check
   (`f0b5dbf96`); PR #4 (merge `55a26cf06`) added GEN-8 (project-tree
   machine-absolute-path lint, SPEC §0.2.4; a 19-file instruction-class
   baseline that trends down like 92/154) and GEN-9 (agent-registry currency,
   K-AGENTS-1), with adversarial-review hardening of the GEN-9 token
   boundaries and `run_self_check` root normalization; PR #5 (`62be11e96`)
   corrected GEN-8 to audit git-tracked files only, excluding gitignored
   build output (D-GOV-01) so the 19-file baseline is stable on built
   checkouts. This resolves the consistency audit's confirmed findings §4
   items 3 and 6. Verified at each merge: suite green (150 tests at PR #5);
   `validate_path_anchors.py` PASS; the three retained stale surfaces of
   item 3 still fire.
7. **AGENTS.md `DELIVERABLE_TASK` removal** — owner ruled 2026-07-01 on the
   consistency audit's §4-item-3 registry drift: remove rather than retain as
   a live fixture. All three references dropped (narrative list, index row
   citing `AGENT_DELIVERABLE_TASK.md` — a file living only in gitignored
   `agents/.archive/` — and the `WORKING_ITEMS` dispatch row); landed in PR #4
   commit `66fbfd765`. The GEN-9 live baseline now pins zero registry drift in
   both directions; the audit catalogue carries dated resolution annotations.
8. **Phase 3 (brief + adoption) — complete** per plan v3 §Roadmap row 3,
   landed at owner direction 2026-07-02 (PR #6, merge `89394d129`). Adoption
   stays a human act: no harness command flips a brief's state. New
   committed-adoption verification per D-GOV-04 (`brief --verify-adoption`):
   identity-first refusal (exit 2) against the `human_actors` allowlist;
   scratch-dir / untracked / uncommitted-edit adoptions surface as REVIEW
   and fence nothing; clean committed adoption binds the publication SHA
   (K-AUTH-2). CANDIDATE briefs now carry adoption placeholder fields and
   steps. `next` lists practitioner-selected active work (the tool never
   selects). Adversarial review fixed two defects pre-merge: case-variant
   scratch paths and symlinked brief paths could previously activate a
   fence (both now fail closed).
9. **Phase 4 (checks) — complete** per plan v3 §Roadmap row 4, landed at
   owner direction 2026-07-02 (PR #9, merge `47329529c`). `run-validations`
   executes only manifest-declared commands under the mutation-control
   contract (porcelain snapshots + content fingerprints of already-dirty
   tracked files; evidence records `practitioner-harness-evidence/v1`;
   timeouts labeled, never inferred); `scope-check` judges diffs against
   the adopted fence (deny-wins matcher, blind spots stated in every
   output); `evidence-check` applies the D-GOV-08 Option B provenance
   ladder (completeness, never sufficiency); `closeout-digest` composes
   and never gates. Exactly two BLOCK conditions exist: scope violations
   against an ACTIVE fence (D-GOV-04; REVIEW-capped otherwise) and
   governed-file mutation by a validation command (unconditional,
   K-WRITE-2 — adversarial review closed a hole where an unadopted brief's
   `evidence_targets` could exempt governed mutations). `CONTRACT_SOURCE`
   and the charter basis now cite D-GOV-08 @ `5f0f45c2b` alongside
   D-GOV-01..07 @ `82a35c545` (conscious pin update; no test pinned the
   old string). Suite at merge: 230 passed on the built primary checkout
   (clean worktrees: 229 + 1 environment-conditional skip).
10. **Phase 5 (cache + CI) — closed, precondition unmet**, owner ruling
   2026-07-02 (in-session): the plan's gate "only after query pain is
   real" covers the entire phase — cache AND CI wrapper. Measured on the
   primary checkout 2026-07-02: `status` 0.07–0.19 s, `drift --all`
   0.20 s, `self-check` 3.9–4.4 s — no query pain. Nothing built;
   authority stays in authored files. Reopens only on owner direction
   when the gate condition holds.
   *Addendum (2026-07-02, later the same day): the owner reassessed after
   Phases 3–4 landed and re-ruled the CI half — the gate now reads as
   cache-only. The CI wrapper landed at owner direction (PR #10, merge
   `e9f79cb1b`): `.github/workflows/governance-harness.yml` runs the
   harness suite + `self-check` on every PR and push to main; BLOCK exits
   fail the run per D-GOV-02; REVIEW never gates; no new checks, no
   authority. Its first run caught a real guard defect (BSD `sed -i ''`
   silently failing to update `**Current State:**` on GNU sed), fixed in
   the same PR with the guard's awk/ENVIRON idiom; the staging export
   copy was regenerated per the documented canonical-edit flow. The cache
   half stays closed: query-pain precondition re-measured unmet the same
   day.*
11. **Audit-findings slice** — three findings from an owner-run harness audit
   resolved at owner direction 2026-07-02 (PR #11, merge `e5a237363`). Two
   were harness defects: `evidence-check`/`closeout-digest` read `--out-dir`
   without generated-root containment (arbitrary outside-root JSON could pose
   as harness-captured evidence) — now routed through `ensure_generated_scope`
   fail-closed; and the `RULING_SHA_TBD` self-check detector fired on
   backtick-quoted prose (a live false positive on `D-GOV-02`'s own rule text)
   — now suppresses code-span quotations while mid-line bold fields keep
   firing. The third was genuine content drift: all eight `_DomainEngines/`
   D-T0 records carried stale `(PROPOSAL; HumanRuling: TBD)` title tags and
   `Ruling SHA: TBD` fields after their 2026-06-21 ruling. Owner ruled
   clean-and-backfill (D-GOV pattern `f1549afb1`): publication commit
   `6e70b5aac` verified per record (`git log -S`), seven titles flipped to
   `(RULED 2026-06-21)`, eight SHA fields backfilled, stale bind-at-publish
   prose corrected. The three retained fixture surfaces (item 3) are
   byte-identical and still caught; live pins moved consciously
   (STALE_RULING_ANNOTATION 9→2, TITLE_CONTRADICTS_RULING 8→1, RULING_SHA_TBD
   10→0). Suite: 235 on the built primary checkout (234 + 1 in clean
   worktrees).

## Now actionable

**The plan v3 build roadmap is complete through Phase 4 (Completed items
5–9); Phase 5 is closed precondition-unmet (item 10).** The harness's
remaining growth is use, not construction: candidate briefs, human
adoption, and the tranche checks on live work — each tranche at owner
direction. Parked items keep their existing homes (audit catalogue §6,
thesis owner-revision pack §7, piping schema alignment, domain-shape
verifier per D-GOV-07). Design changes supersede a D-GOV-* record or
arrive as PR review — never a new plan document.

Standing nuances carried forward: the D-GOV-06 cleanup corrected the live
`_DomainEngines/` contradiction surfaces, so any regression fixture for
them must be a **synthetic/frozen snapshot** (the PR #2 corpus is the
pattern), not a live file — except the three surfaces **deliberately
retained** as live test material (Completed item 3), which `self-check`
still catches. The GEN-8 19-file baseline and GEN-9 zero-drift pins move
only by conscious, documented update.

## Terminal-artifact rule (restated)

Planning is closed. Design changes from here supersede a D-GOV-* record or
arrive as PR review — never a new plan document.
