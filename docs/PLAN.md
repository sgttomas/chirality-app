# PLAN — Active Roadmap

> **Status: ACTIVE — maintainer-adopted 2026-07-01** (supersedes the
> 2026-06-15 DRAFT skeleton). §2–§4 record ruled direction and measured
> findings only, prepared at the owner's explicit request following the
> D-GOV-01..07 rulings of 2026-07-01 (ruled and SHA-bound at commit
> `82a35c545`; see `docs/governance_harness/_DECISIONS/_REGISTER.md`); per
> K-INVENT-1 nothing is invented. The Control-Plane Boundary is unchanged
> from the 2026-06-15 restoration; §1 is unchanged except for the
> domain-engine containment bullet added 2026-07-02 at owner direction
> (restating the D-GOV-06-ruled direction and `CONTRACT.md` K-DOMAIN-1..4;
> nothing invented).

## Control-Plane Boundary

This document is the active **framework roadmap**. It is strategic and
non-governing: `DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, and `TYPES.md` govern;
this file records direction and intended work, not binding requirements.
Tactical sequencing, blocker policy, and completed-work detail live in
issue/branch/release records — not here. Working roots (`projects/*`,
`domains/*`) maintain their own `docs/PLAN.md` for project-level roadmaps; this
file does not supersede them. `docs/governance_harness/PLAN_INDEX.md`
classifies planning artifacts and their standing; it is an index, not a
competing roadmap surface.

---

## 1. Current Architectural Direction

The established direction (reflected in `AGENTS.md` and the agent suite):

- **Agent 0/1/2 are runtime delegation positions.** HELP_HUMAN is the sole
  Agent 0; Agent 1 managers remain direct human entry points; Agent 2 may be
  TASK plus a skill, an ephemeral bounded generalist, or an approved dedicated
  specialist. Standards constrain all layers from outside the hierarchy.
- **Multi-agent orchestration supports terminal fan-out/fan-in, supervised
  many-to-many agency, and arbitrary dependency-valid mixed work graphs.** The
  human may prescribe or delegate pattern selection. Agent 0 manages
  cross-package work; package-level WORKING_ITEMS manages intra-package work.
- **`TASK` is the default recurring-method Agent 2 shell.** A dedicated
  specialist requires evidence that TASK and ephemeral-generalist forms are
  inadequate, a HELPS_HUMANS proposal, and explicit human approval.
- **Workflow-component standards are separate from applying personas.**
  `docs/WORKFLOW_COMPONENT_STANDARD.md` is the normative design surface;
  HELPS_HUMANS applies and maintains it as an Agent 1 manager. Existing agents
  requalify under the same agent/skill/tool/brief boundary as new components
  (D-GOV-11, superseding conflicting D-GOV-10 conclusions).
- **Method logic lives in `skills/`; deterministic operations live in
  `tools/`; Agent 1 managers handle human-facing orchestration.**
- **Governance is two-layered.** The framework root (`AGENTS.md`, root `docs/`,
  `agents/`, `skills/`, `tools/`) defines Chirality-wide rules; working roots
  specialize them without weakening framework invariants (`CONTRACT.md`
  K-AGENTS-1).
- **One shared instruction root serves many working roots** under `projects/*`
  and `domains/*`; path anchoring and task write-scope containment make
  per-working-root and git-worktree isolation safe (`SPEC.md` §0.2;
  `CONTRACT.md` K-WRITE-2).
- **Chirality is the governed environment around domain engines, not the
  solver.** Domain engines own authoritative domain truth; Chirality governs
  the work around them — profiles, manifests, proposals, review gates, records
  (`CONTRACT.md` K-DOMAIN-1..4; tier-0 OpenPipeStress profile ADOPTED, affirmed
  by D-GOV-06). The division of labor: agents propose, domain engines compute,
  humans rule, the record binds.

Details of in-flight work live in issue/branch/release records, not in this
planning surface.

---

## 2. Active Roadmap Themes

| Theme | Status |
|---|---|
| Governance harness (practitioner bench tool) | RULED + FIRST PR LANDED — D-GOV-01..07 ruled 2026-07-01 (SHA-bound at publication commit 82a35c545); plan of record: `governance_harness_plan_v3_2026-07-01`; first PR merged 2026-07-01 (PR #1, commit 71a67d0b1: `tools/practitioner_harness/` + `write_status.sh` guard); next slices per plan §Roadmap Phases 2–5 at owner direction |
| Root governance ratification | COMPLETE — owner ratification 2026-07-11 of the full root canon (DIRECTIVE/SPEC/TYPES/CONTRACT status blocks; D-GOV-09 register record), completing the track D-GOV-05 sequenced (minimal harness basis first, ruled 2026-07-01; full ratification followed on its own track); harness label propagation landed with the lifecycle-semantics amendment PR |
| Tier-0 domain-engine integration (OpenPipeStress) | ACTIVE — profile ADOPTED (affirmed by D-GOV-06); surface-cleanup slice directed; live-build conditions per `_DomainEngines/` records |

Unsplit backlog: History trailer grammar (rides D-GOV-05); domain-shape
verifier + D-GOV-07 re-binding (deferred per D-GOV-03); obligations /
applicability register (deferred).

---

## 3. Roadmap Detail

### Architecture and Governance

- **Root governance restoration + path anchoring.** Ratify the root `docs/`
  governance set (DIRECTIVE/SPEC/TYPES/CONTRACT/PLAN); wire the `K-WRITE-2`
  ScopePath-containment rule (`SCOPE_OUTSIDE_WORKTREE`) into `AGENT_TASK.md`;
  derive `REPO_ROOT` in `init/init-prompt.md` and de-absolutize
  coordination/handoff files. Basis:
  `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`.
  **Amended 2026-07-01 per D-GOV-05:** ratification is sequenced — the minimal
  harness basis (source-of-truth, human authority, generated-output rule, path
  containment, approval-SHA binding, provenance, status canonicity, verifier
  severities) ratifies first; the full root set proceeds on its own track; the
  append-only History trailer grammar (SPEC §3.1) rides that ruling.

- **Governance harness build.** Read/report bench tool over
  `projects/chirality-app-dev`, `projects/chirality-piping`, and
  `_DomainEngines/` (D-GOV-03 scope): adapters + manifests, `status`,
  `drift`/`self-check` against the 92/154 status-history baseline (verified
  2026-07-01, all in piping), source-cited candidate briefs with human
  adoption (D-GOV-04), tool-run validations under the mutation contract, and
  the `write_status.sh` precondition guard (canonical copy + export source;
  the staging copy is a gitignored regenerated artifact). Basis:
  `governance_harness_plan_v3_2026-07-01` + `PLAN_INDEX.md`; authority:
  D-GOV-01..07 (ruled 2026-07-01, SHA 82a35c545). Planning is closed
  (terminal-artifact rule). **First PR landed 2026-07-01** (PR #1, merge
  commit 71a67d0b1); remaining phases (fixtures, brief adoption,
  run-validations/scope-check/evidence-check, cache/CI) proceed per plan
  §Roadmap at owner direction.

- **D-GOV-06 cleanup slice.** CHANGE-published correction of the six
  contradicting `open_pipe_stress` current-truth surfaces
  (`RULINGS_PUBLISHED.md` stale closing paragraph; both halves of the
  `DOMAIN_ENGINE_INDEX.md` banner — "No profile is ADOPTED" and "No decision
  is ruled"; the profile YAML header comments plus the open_issues "Profile
  stays DRAFT" entry; the `.DRAFT` filename; D-T0-06's stale HumanRuling
  line; the `_DomainEngines/_LATEST.md` "PROPOSAL, not yet owner-accepted"
  framing); the diff becomes the harness's first live self-check fixture.

### Workflow Normalization

- **Drift reduction as a standing objective.** Framework-wide target: the
  status/history mismatch count trends down from the 92/154 baseline as
  measured by the harness `drift` command; restated-state surfaces (pointers,
  banners, index tables, header comments, filenames) are audited on the same
  cadence. First measured run (2026-07-01, at merge commit 71a67d0b1):
  92/154 — all 92 in chirality-piping; app-dev 0/53; 0 unparseable documents.

---

## 4. Known Risks

- **State drift.** 92/154 deliverable status files disagree with their own
  histories (verified 2026-07-01; all 92 in chirality-piping, app-dev 0/53
  clean); control-area surfaces have contradicted each other about single
  facts. Mitigation: harness drift metric with run-over-run trend; D-GOV-06
  cleanup; consistency checks over every restated-state surface.
- **Plan resurrection.** Settled architectural forks re-derived by fresh
  sessions (the SQLite control plane was independently re-proposed twice).
  Mitigation: ruled decision records with supersession clauses (D-GOV-01);
  `PLAN_INDEX.md` standing markers; terminal-artifact rule.
- **Planning outproducing execution.** The 2026-06 archive shows heavy
  meta-work against 92/101 piping deliverables IN_PROGRESS and 53/53 app-dev
  deliverables in CHECKING. Mitigation: PR-first sequencing; success defined
  as tranches closing and drift falling, not documents produced.

---

## 5. Historical Record

Completed roadmap slices are historical and are not tracked as active surface
here; they live in git history, release records, and per-project completion
logs.

---

## 6. Shared Runtime Execution Order

D-GOV-20 activates the following bounded sequence:

1. close and preserve the D-APP-72 Pi/oMLX tranche;
2. reconcile root, app-dev, domain-engine, and PEC authority;
3. promote provider-neutral contracts and orchestration into `runtime/`
   without behavioral change;
4. establish the authenticated Unix-socket daemon, client, and bundled CLI;
5. convert Desktop into a daemon client and add explicit residency controls;
6. prove one direct Agent 1 → read-only local Agent 2 workflow in app-dev;
7. migrate PEC’s model/session/delegation ownership to the daemon while
   retaining deterministic PEC acts and RBAC in its project adapter;
8. include only generic runtime surfaces in the public export.

Each compatibility stage reruns the existing app baseline. Fake providers
cover automated residency and protocol tests; downloaded local models are used
only in an opt-in live proof. Automatic scheduling, multiple resident primary
LLMs, local Agent 1, piping, and production PEC remain later owner decisions.
