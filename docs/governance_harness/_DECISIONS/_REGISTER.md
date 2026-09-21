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
| D-GOV-21 | Root working-root exception and replacement containment contract | **RULED 2026-07-25** — "I rule APPROVED for O-A against candidate SHA c038c493e871c95871823281b45890ba9404624b" (owner; exact candidate = PACKET.md Rev 3 in `_PROPOSALS/D-GOV-21_root-working-root-exception/`) — the repository root is the root product's working root and root `execution/` its execution root, eligible for `PKG-*`/`DEL-*` only from an accepted root decomposition with guards G0–G4 registered and passing; normative clauses S1–S9 (DIRECTIVE/SPEC/TYPES) amended exactly per Annex A and no further; LOOP_INIT updated (S10); containment mechanisms M1–M7 required; D-GOV-09 remains the historical ratification act, its S1–S9 clauses prospectively amended | Authorizes candidate root-PRD development on this basis; G0 materialization fence live in governance-harness CI; PRD adoption, genus wording, accountability model, PRD placement, root decomposition, and materialization all remain separately gated (packet §11, §5.3); export-staging regeneration deferred per the implementation handoff |
| D-GOV-22 | Adoption of the Chirality Root PRD | **RULED 2026-07-25** — "I rule APPROVED for O-A against candidate SHA 90fae458bf485412e9c3a6295df193eb323c9774" (owner; exact candidate = PACKET.md in `_PROPOSALS/D-GOV-22_root_prd_adoption/`, sha256-pinning the Rev 5 adoption-ready PRD bytes at `d9ea86f88`) — the root PRD is adopted after four adversarial-review cycles and five in-session owner rulings (RD-1..RD-5, verbatim in PRD §9); 17 PROPOSED items take effect (v1 boundary, OBJ-1..OBJ-7, D-13..D-16, §7.2 promotion, §8.3 release authority, F4–F6); the bidirectional PRD ↔ DIRECTIVE §1 concordance map (packet Annex A) records one DIVERGENT pair (RD-1 genus, C-1 pending obligation (a)); C-3 confirmed and closed at ruling; adopted copy placed at `docs/PRD_ROOT.md` per RD-4-D | Closes D-GOV-21 §6 step 5 (Lane A); no materialization, decomposition, export-boundary change, or DIRECTIVE §1 amendment; obligations (a)/(b)/(c) and C-2/C-4 corrections remain separately gated follow-ons; Lane B (guards G1–G4) is the next open lane |
| D-GOV-23 | Exact-prose supersession of the DIRECTIVE §1 genus clause | **RULED 2026-07-25** — "I rule APPROVED for O-A against candidate SHA 65bb96378428a86ed8ab8581149ead056d756789" (owner; exact candidate = PACKET.md in `_PROPOSALS/D-GOV-23_directive_genus_supersession/`) — the `docs/DIRECTIVE.md` §1 opening genus clause is superseded by the RD-1 ruled two-level formulation verbatim (plus a provenance parenthetical), the remainder of the paragraph byte-identical; applied programmatically from the ruled packet in the publication commit; **C-1 CLOSED** (the D-GOV-22 concordance map's single DIVERGENT pair is concordant); routed change notices shipped to `projects/chirality-app-dev` and `domains/chirality` | Performs PRD §9.1 obligation (a) (D-GOV-22 packet §5 item 3); obligations (b) README reword and (c) propagation survey remain separately gated, as do C-2/C-4 corrections and Lane B (guards G1–G4) |
| D-GOV-24 | Exact-prose propagation of the ruled genus to four document self-descriptions (P-1..P-4) | **RULED 2026-07-25** — "I rule APPROVED for O-A against candidate SHA 444e29359883e50506ac0ea0ee5f6cc3f5f7d7de" (owner; exact candidate = PACKET.md in `_PROPOSALS/D-GOV-24_operating_system_prose_propagation/`) — the four remaining top-level-identity sentences (DIRECTIVE preamble :5, CONTRACT :7, SPEC :5, TYPES :5) now name Chirality Root as the top level with the agent operating system as its ruled contained level; applied programmatically from the ruled packet; no normative clause changed; the six contained-level usages remain by design; **the RD-1 genus propagation is complete**; routed change notices shipped to `projects/chirality-app-dev` and `domains/chirality` | Closes the obligation (c) proposal set (P-1..P-4 from the 2026-07-25 survey); remaining open root-loop items: C-2/C-4 correction proposals and Lane B (guards G1–G4) |
| D-GOV-25 | Acceptance of the first root decomposition (D-GOV-21 §6 step 8) | **RULED 2026-07-25** — "Merge PR #347 (CI green). Candidate SHA for the exact-candidate ruling: ec62af0700e530c1640698fa406398cb1cb45d29 / Decisions: 1. Record a reasoned deferral. 2. Update the labels as warranted. 3. Proceed in the manner you recommend." (owner; exact candidate = the `execution/_Decomposition/` package staged with all seven gates PENDING_OWNER_RULING; acceptance vehicle stated in the record per K-AUTH-2) — the first root decomposition (6 packages / 45 deliverables / 103 scope items, derived solely from the adopted PRD, F4 closed both directions, D-15 four-category coverage) is the accepted basis for downstream root work; ruled dispositions: OBJ-2 situated-working-root clause deferred with reasons recorded (OI-013), source-currency findings confirmed with label effect-annotations (OI-001/OI-002, adopted bytes untouched per D-13), framing strains accepted as staged (OI-003/OI-004); root Project Setup instantiates guard state (`execution/_harness/`) in the publication tranche | Closes the decomposition half of D-GOV-21 §6 step 8 and releases its Project Setup half; step 9 materialization remains behind the §5.3 gate and a further owner act; practitioner-harness adoption of the root adapter remains separately gated |
| D-GOV-26 | Closeout of the four owner-gated items by adopted recommendation | **RULED 2026-07-25** — "Delegate to `opus-5` subagents the closeout of those four owner-gated issues by following your recommendations in each case." (owner; adopts the Receipt-49 recommendations as dispositions; approval binds at the human-gated PR merge per K-AUTH-2, stated in the record) — (1) `_Archive/` status quo accepted + SPEC §1.1 local-working-state note; (2) `.github/workflows/` added to the SPEC §0.2.2 instruction-surface enumeration and `CLAUDE.md` added to the guarded set (G2/G3/G4 + tests); (3) K-WRITE-2 gloss amended in CONTRACT.md (invariant sentence unchanged; D-GOV-21 §5.1 debt closed); (4) export-staging regeneration settled as a standing deferral with a read-only boundary audit evidencing safety | Routed notice to `projects/chirality-app-dev` (SPEC + CONTRACT pinned in its authority corpus); no remaining parked owner-gated items from the D-GOV-21 era; next phase is per-deliverable initialization under the accepted decomposition |
| D-GOV-27 | Initialization-phase closing rulings (lifecycle, ResponsibleParty, register reconciliation, contract refresh, exact-prose packet) | **RULED 2026-07-25** — owner in-session via structured decision prompts, selections verbatim in the record: "Additive propagation (Recommended)" (four register/ledger objective divergences resolved additively; ledger untouched), "Update frontmatter + CON now" (four contracts amended and re-validated), "Fold in all four restatements (Recommended)" (DIRECTIVE §1/§2.6 and TYPES §1.4 amended in place; PRD §5.2 O-1 superseded by instrument per D-13, pointer-block note only); with the phase-plan decisions applied: all 45 deliverables OPEN→INITIALIZED via write_status.sh after 45× SOW_V1 validation (PR #354), live CI pin moved to INITIALIZED, ResponsibleParty "Ryan Tufts" assigned across register and 45 _CONTEXT.md; work-graph nodes returned to pending; D-GOV-26 EffectiveSHA backfilled (31b8dc94a); approval binds at the human-gated PR merge per K-AUTH-2 | Completes the initialization phase: 45 validating SOW_V1 contracts, all INITIALIZED with an accountable ResponsibleParty; next phase (semantic enrichment or production dispatch) is owner-gated future work |
| D-GOV-28 | Root Runtime Stewardship PRD Amendment | **RULED 2026-07-26 — O-A.** Owner adopted the exact Root PRD Revision 6 candidate at commit `f78a83621cbd679e6af2c41199845aca74073480`, subject SHA-256 `0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`; O-11 becomes an adopted Root product requirement; exact ruling recorded in `D-GOV-28_root_runtime_stewardship.md` | Applies Rev 6 through the human-gated M2/CHANGE tranche; Root SCA-001 may advance beyond confirmed Gate 1 only after the adoption is effective, with Gates 2–5 separately approved; no decomposition, write-locus, App/PEC scope, repin, implementation, release, or reliance authority |
| D-GOV-30 | Program disclosure and prospective ratification of the 2026-07-28 remediation end-state | **RULED 2026-07-28 — R-1, R-2, R-3, R-4 all ratified; none declined** — candidate packet at subject SHA-256 `32b4afbfb402d65fecc14558bca79f5b83fc5690bd0b4f56cc9a656ced6c35e3` (`docs/governance_harness/_PROPOSALS/D-GOV-30_2026-07-28_program_disclosure_ratification/PACKET.md`, basis `main@85ea0628f`) discloses the verified facts of merges #389–#408 (one owner act as sole authorization; zero GitHub reviews; author == merge actor 20/20 against then-live D-8; K-MERGE-1 10 SATISFIED / 10 NOT_EVIDENCED / 0 VIOLATED; #398 citation gap; #408 self-ratifying) and presents four individually declinable present-state items: R-1 RT-A effective-state closeout (Receipt 57), R-2 record-currency repair (Receipt 58), R-3 program closeout `COMPLETE_FOR_ARCHITECTURE_REMEDIATION / PASS_WITH_BOUNDED_WARNINGS` (Receipt 59, enumerating #398/#408 by SHA), R-4 OD7-G1 hash-manifest approval by SHA-256 (Receipt 53 gate); no retroactive cure; informed batch, not precedent for blanket approval; numbered 30 to coexist with the OD7-G1 packet's `D-GOV-29` observation | On ruling: per-item effects only; no D-8/LOOP_INIT amendment, no loop-local App/PEC/Piping substance, no cure of historical nonconformance, no lifecycle, implementation, release, or reliance authority |
| D-GOV-31 | Merge-gate policy succession (D-8 successor, shared-CHANGE scope) | **RULED 2026-07-29 — Candidate B adopted.** Owner token `APPROVE D-GOV-31 15fba9c3` (verbatim in the record); subject `CANDIDATE_B_SHARED_CHANGE/PRD_ROOT_REV7_CANDIDATE.md` SHA-256 `15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748` at candidate commit `3ad43c27b`, basis `main@4f7808acb`; owner selection `SELECT CANDIDATE-B` recorded at `482ec0b79`; HZN-GOV-01 rerun ADOPTION_CLEAR_WITH_NOTES pre-adoption, no blocking finding; applies PRD Rev 7 with annex §5.3.1 (bounded owner grants, four closeout identities — semantic approval, approved source SHA, merge authorization, effective merge SHA — token grammar, express exclusions, K-MERGE-1 strengthened evidencing) | On publication: the Rev 6 D-8 row ("never self-merge") is superseded and the default stays human-gated permission-required; nine POLICY_DELTA §4 Step-4 propagation obligations plus routed M6 notices to every registered loop attach — enumerated, not performed; no grant issued, exercised, or pre-approved; no retroactive cure of the 2026-07-28 window; loops bound only via their own adopt/acknowledge acts, stricter local merge discipline controlling until then |
| D-GOV-32 | Adoption of the Chirality Task Management PRD (Revision 2) | **RULED 2026-07-31 — "The PRD is accepted."** (owner, in-session, verbatim in the record with its carrying direction) — subject `plans/chirality-task-management/PRD_CANDIDATE_2026-07-31.md` Rev 2, SHA-256 `97e2ae6525ecbfdc52ff22aee85e1182a751c1090c2aa2f52faaf9e080f35d18` at candidate commit `584319dc9`, effective on `main` at PR #423 merge `c1156837f`; authored through the fresh Agent 0 inquiry (authoring basis §12) and restructured by the 2026-07-31 four-lens architecture review (findings F-1..F-30 dispositioned in PRD §20); performs the PRD_ROOT OBJ-6 "new product function" act for the cross-loop register class | On ruling: PRD Rev 2 is the accepted product basis; K-TM-1..6 adopted as product invariants; Stage-A obligations attach to the root loop — CONTRACT.md K-TM tranche, `execution/_Coordination/_TaskManagement/` minting and ~115-item seed, LOOP_INIT reader binding, first triage session, `taskmgmt` v0 — enumerated, not performed; PEC PRD §16-1 decided for the Action Item register class with a routed notice obligated; no other loop bound (F-APP-5/F-PIP-5/D-PEC adoption per loop); no CONTRACT/SPEC/agents/loop-instrument amendment, no decomposition, no implementation or reliance authority |
| D-GOV-33 | Task Management invocation-local federation survey | **RULED 2026-08-02 — "Require the survey whenever TASK_MANAGEMENT is already invoked; do not require loops to invoke TASK_MANAGEMENT."** (owner, persisted in managed run `TM-FEDERATION-SURVEY-20260802`; H2 later satisfied by the owner's verbatim direction "Merge via PR") — every already-invoked TASK_MANAGEMENT instance surveys all canonical tracked registers read-only before its requested mode, reports coverage, and preserves zero register writes; published from approved source `08ed85ae1` via PR #478, effective at merge `2c25bd2c4` | Distinguishes mandatory invocation-local receive-side discovery from the rejected standing loop sweep; extends the active manager/tool without LOOP_INIT, schedule, CI, daemon, schema, PRD/CONTRACT, register-row, foreign-write, or authority effects; checked publication completed with all required checks successful |
| D-GOV-34 | Clean-basis branch and worktree-lane creation is routine CHANGE execution | **RULED 2026-08-21 — "Mint D-GOV-34 — I rule that clean-basis branch/worktree-lane creation is routine CHANGE execution and dirty-basis lanes remain non-routine, confirming my 2026-07-19 ruling (App LOOP_RECEIPTS.md Receipt-74 Owner-Direction). D-GOV-34 binds exactly the TM-ROOT-124 amendment to agents/AGENT_CHANGE.md §Routine closeout, its G4 tranche manifest, and routed notices to the App, Piping, and domain-engine loops. It grants nothing else."** (owner; exact ruling transcribed in the record; AcceptedBasis `33e871fc38d8ef4bb51f7c25cdc6ca2e8dcb69e0`) | Binds only the TM-ROOT-124 CHANGE-instruction amendment, its G4 manifest, and three routed notices; dirty-basis lanes and every other non-routine action remain gated; no foreign-loop adoption, implementation, lifecycle, release, publication, reliance, or merge authority |
| D-GOV-35 | Delegated-harness-native delegation class | **RULED 2026-08-22 — `[click] "Approve as proposed"`; APPLIED 2026-08-22; EFFECTIVE `8deca1489a3e5921288f71d4960d555e183a6f3f`.** All eight proposed items ruled as written against proposal SHA-256 `924c1b098f1510bca9189e1ac06e4c2fd8e9d358a9fc3c4e42fdd04a53b69c88`; D-GOV-14 item 7 superseded only in its sole-executable-path exclusivity sentence; AcceptedBasis `main@abf3c1bf5996cd9333ad706df14e62df32fbbf0f`; CandidateSHA `294e846bc762b96ac780d49f0137f61eb4dde779`; PublicationSHA `ade6ecf33d4e10dab1441aeedb240061e140ff1b`; EffectiveSHA `8deca1489a3e5921288f71d4960d555e183a6f3f` | Adds delegated-harness-native beside the preserved sole Chirality-managed path; applies exact Root doctrine and three-sentence concordance through DEL-02-03 M2; routes App/Piping notices and defers public export; no hold, pin, lifecycle, implementation, release, reliance, publication, or merge authority |
| D-GOV-36 | Managed authentication custody, bootstrap and logout | **OWNER DISPOSITIONS SELECTED 2026-09-06; EFFECTIVE via PR #740 merge `e1dee34315ff4ca448b0fbc14e5542b6bad9fac2`; NARROW ACCOUNT-ONLY AUTHORITY AMENDMENT APPLIED_UNPUBLISHED 2026-09-07** — D-APP-126 records “I approve these three recommended dispositions”; candidate `4827bbe0cf309aa891c90bdf4c38586f726abb21` was merged by PR #740. The later owner act records “I approve this narrow authority amendment,” supplying the semantic/M2 authority for its faithful reviewed Root application. Exact reviewed postimages and later matching-head/main identities are recorded as evidence; Git supplies no semantic authority. | Effective narrow D-GOV-20 items 2–3 custody exception, nonexecuting bootstrap, and global hosted logout; the applied-unpublished later amendment adds dedicated authenticated account-only public Unix authority limited to nonexecuting bootstrap/status/cancellation/hosted lifecycle. No project access/consent/execution, private-supervisor access, TCP listener, additional enrollment, endpoint/wire/source acceptance, implementation, live operation, supplier acceptance, readiness, release, or downstream adoption follows. |
| D-GOV-37 | Root recognition of owning-accepted Runtime successors | **RULED implementation direction 2026-09-06** — “You have approval to make this change in Root”; bounded historical/current-proof separation and exact owning-accepted successor recognition, initial D36 Stage1 subject pinned in the record | M2/G4 repair with independent review; baseline and unchanged constraints preserved; candidate CI is not main effect or Runtime dispatch. Stage2 owning acceptance/adoption remains pending. |
| D-GOV-38 | Exact Runtime Stage2 successor adoption | **RULED 2026-09-07** — “I approve both.” Exact two-SOW subject c5054fd4f4c23338c28c3194a3227bac706f8d6813d3673deb40d8b50075a3fb accepted through Runtime; matching Root adoption authorized | New immutable Stage1+Stage2 policy and helper selection only, M2/G4 and independent checks; Root-first publication, no algorithm/history change or execution/release grant. |
| D-GOV-39 | Runtime account-authority successor adoption | **EXISTING AUTHORITY APPLIED 2026-09-07** — D-GOV-36 narrow semantic approval plus D-GOV-37 Root implementation direction; Runtime Gate 5 owner acceptance `edfd03df…` binds exact subject `0fcaae69…`, acceptance manifest `a4cd1680…`, and SCA-002→SCA-003 snapshots `8865716…` / `ce843763…` | New immutable Stage1+Stage2+account-authority policy and narrow complete-chain verification; branch-local accepted bytes report pending publication, followed by CI/publication/main backcheck; no repeat vote, SOW, Runtime write, activation, or release grant. |
| D-GOV-40 | Runtime DEL-02-06/09 SOW successor adoption | **EXISTING D-GOV-37 AUTHORITY APPLIED 2026-09-07** — owning Runtime acceptance manifest `e90c7850…` binds owner acceptance `0329293b…`, subject `37141786…`, audit `432aa2e1…`, index `ffac4201…`, pointer `da47241b…`, and exact SOW postimages `2e66ee86…` / `0d154c00…` | New immutable four-entry policy and narrow format-aware proof-chain verification; prior three entries preserved; App DEL-02-05 excluded; branch-local recognition pending publication with no execution/release grant. |
| D-GOV-41 | Four-role agent and workflow overhaul | **OWNER-DIRECTED CANDIDATE IMPLEMENTATION 2026-09-09** — “PLEASE IMPLEMENT THIS PLAN:” followed by the complete accepted four-role plan; Root candidate changes authorized, merged adoption pending | Four concise roles, explicit workflows, registry/configuration separation, faithful 34-agent/45-method migration, Root validation and routed notices; incompatible-consumer adoption hold, no downstream repin or release. |
| D-GOV-42 | Chirality v3 role, skill, and workflow adoption | **OWNER-DIRECTED CANDIDATE IMPLEMENTATION 2026-09-09** — “PLEASE IMPLEMENT THIS PLAN:” followed by the complete Chirality v3.0 adoption plan; grouped checkpoint design and coordinated Root/Runtime/App/distribution candidate implementation authorized against `c16812685831a1cae3d44bf478d08b033c605c3a`; exact reviewed-byte acceptance remains pending | Adds canonical skills, source-qualified layered discovery, Runtime-owned selective context and history, ordered method selection, native Plan/permission separation, grouped decomposition/scope-change checkpoints, compatibility records, and routed notices; no merge, receiving-loop adoption, supplier qualification, packaging, publication, or release. |
| D-GOV-43 | Codex host re-platform: stock App Server owned by the App host | **RULED 2026-09-11** — “I rule D-GOV-43 accepted as revision 3 at commit 3ef2ef524, with the post-build minimum-not-ceiling clarification. The three folded choices stand.”; record `D-GOV-43_codex_host_replatform.md`; publication SHA `d2878462be59a43b4afc175a8cce85abca9cf696` (merge of PR #767, 2026-09-12; K-AUTH-2); application tranche being applied on branch `claude/chirality-codex-replatform-3999f1`, ApplicationSHA to be filled at merge | Stock pinned App Server child over stdio with the full protocol; Chirality effective Codex home with separated authentication; user-chosen policy; daemon and supplier-admission retirement; bounded coordinated Root/Runtime/App application; eight-check spike on the production path; no release, publishing or local-model work. |
| D-GOV-43 (supplement) | Host topology selected: A2, application-owned Runtime service | **RECORDED 2026-09-12** — “We are all in agreement this is the path forward.”; supplement `D-GOV-43_supplement_topology_A2.md`; publication SHA `d2878462be59a43b4afc175a8cce85abca9cf696` (merge of PR #767, 2026-09-12); items 1, 7, 2 and 13 re-expressed, others stand | Runtime service retained as an App-owned child speaking the existing socket API; stock Codex; admission, supplier, launchd and supervisor-socket machinery retired; cross-product constraint (host independent of Electron and Next); Piping and local models deferred. |

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
