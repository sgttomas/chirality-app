# PLAN_INDEX — Governance Harness Planning Artifacts

Status: ACTIVE/RULED: D-GOV-01..07 ruled by owner 2026-07-01 (the scope this
index was published against — historical; the decision family has since
grown, and `_DECISIONS/_REGISTER.md` is the live authority for the current
D-GOV inventory); index published
under `docs/governance_harness/`. Purpose: one navigable record of which plan
governs, so no successor session or agent re-litigates a settled fork or
builds from a superseded document. Maintained under `docs/governance_harness/`;
decision records live at `docs/governance_harness/_DECISIONS/`, per the
repo-wide `_DECISIONS/` convention.

## Standing

| # | Artifact | Date | Substrate verdict | Standing |
|---|---|---|---|---|
| 1 | `plans/.archive/task-management-planning-26-06-22.md` | 2026-06-22 | Option C: SQLite authority, coordinator, leases | **Historical / design seed.** Concern-to-closure model retained; substrate recommendation superseded by D-GOV-01. |
| 2 | `plans/.archive/task_management_harness_plan_2026-06-22.html` (titled "Governance Harness Detailed Plan v2.1" — filename/title mismatch noted) | 2026-06-22 | Rejects Option C; read-only verify CLI, Checks 0–6 | **Superseded as plan; findings imported.** Verified findings carried in v3 (guard, drift baseline, six roots, readiness≠approval vocabulary) and in D-GOV-04/07. |
| 3 | `plans/.archive/governance_harness_integration_assessment_2026-06-23.md` | 2026-06-23 | Re-imports control plane (control.sqlite, leases, gates) | **Superseded on substrate by D-GOV-01.** Entity vocabulary and generated-views material remain reference. |
| 4 | `plans/.archive/governance_harness_detailed_plan_2026-06-23.html` ("Practitioner Bench Tool, Not Governance Theater" v1) | 2026-06-23 | Bench tool; read-mostly | **Superseded by merge into v3.** |
| 5 | `plans/governance_harness_proposal-A_2026-07-01/governance_harness_detailed_plan_2026-07-01_revised.html` (revision A; earlier drafts of this index cited a filename `governance_harness_detailed_plan_2026-07-01_v2.html` that exists nowhere on disk. The same directory holds a byte-identical duplicate — same SHA-256 — named `governance_harness_detailed_plan_2026-06-23_REVISED_2026-07-01.html`) | 2026-07-01 | Bench tool + D-GOV-01, guard, drift, run-validations, self-exclusion | **Merged into v3.** Corrected per cross-review: unqualified "read-only" language; self-exclusion vs evidence-check tension; unscoped cache rule; "closed" phrasing. |
| 6 | `plans/governance_harness_proposal-A_2026-07-01/governance_harness_detailed_plan_2026-06-23_REVISED_2026-07-01.html` (revision B; on-disk home is the proposal-A directory, where this file is byte-identical to row 5's — revisions A and B as merged were the two independent 2026-07-01 revision documents, but the surviving on-disk pair is one document under two names) | 2026-07-01 | Bench tool + decision set, severity taxonomy, sourced facts, adoption lifecycle | **Merged into v3.** Corrected per cross-review: missing write_status.sh guard; unconditional SHA-TBD BLOCK; no quantitative baseline; no run-validations. |
| 7 | `plans/.archive/chirality_architecture_explainer_2026-06-23.html` | 2026-06-23 | — | **Superseded by explainer v3** (corrections recorded in explainer §11). |
| 8 | `plans/governance_harness_proposal-A_2026-07-01/chirality_architecture_explainer_governance_harness_2026-07-01.html` (revision B explainer) | 2026-07-01 | — | **Merged into explainer v3** (artifact taxonomy, four lifecycle tracks, claim prohibitions, degrade-gracefully epistemics adopted). |
| 9 | **`plans/governance_harness_proposal-B_2026-07-01/governance_harness_plan_v3_2026-07-01.html`** | 2026-07-01 | Per D-GOV-01 | **Plan of record; substrate settled by D-GOV-01 (ruled 2026-07-01).** Terminal planning artifact. |
| 10 | **`plans/governance_harness_proposal-B_2026-07-01/chirality_architecture_explainer_v3_2026-07-01.html`** | 2026-07-01 | — | **Current explainer** (companion to v3 plan). |
| 11 | `docs/governance_harness/_DECISIONS/D-GOV-01..07_*.md` | 2026-07-01 | — | **RULED 2026-07-01 by owner; SHA binds at publication commit.** |
| 12 | `plans/.archive/governance_harness_proposal-B-part-2_2026-07-01/` | 2026-07-01 | — | **Superseded at arrival.** Stale parallel copies of the pre-correction corpus (101/154 baseline, pending-publish framing). Its two novel artifacts were adopted in corrected form: roadmap → `docs/PLAN.md` (maintainer-adopted 2026-07-01); register → `_DECISIONS/_REGISTER.md`. Remainder archived; do not build from it. |

Note on rows 1–4 and 7: `plans/.archive/` is gitignored — these lineage
artifacts live outside version control.

### Sibling proposal directory

`plans/governance_harness_proposal-A_2026-07-01/` is the sibling proposal
directory: superseded by merge into v3
(`plans/governance_harness_proposal-B_2026-07-01/`), it retains the
pre-rename D-GH-001..006 decision numbering and contains the byte-identical
duplicate pair noted in rows 5–6 (plus an `SHA256SUMS.txt`).

## Terminal-artifact rule

v3 is the last planning document for this harness. From here:

- Design changes ride **decision records** (supersede a D-GOV-*) or **PR
  review** — never a new plan document.
- The reconciliation debt of prior generations (the substrate fork flipped
  three times because rejections were prose, not records) is the reason this
  rule exists.
- The next artifact after the D-GOV rulings is the first pull request, exactly
  as scoped in v3 §First PR.

## Provenance

Prepared 2026-07-01 by merging revisions A and B after mutual cross-review;
both reviews converged on the identical feature set and accepted each other's
corrections (recorded in v3 §Convergence Record). This index is itself
planning material; per K-AUTH-1 it binds nothing until published.

Verification pass (2026-07-01): a full-repo-access verification corrected the
inherited figures and claims in this corpus. The status-drift baseline is
**92 of 154** `_STATUS.md` files (all 92 in chirality-piping; app-dev is fully
self-consistent) — initially reported as 101/154 by the June inspection,
corrected to 92/154 by live verification. Lineage paths in the Standing table
were corrected to their actual on-disk locations (`plans/.archive/`,
gitignored, for rows 1–4 and 7; `plans/governance_harness_proposal-A_2026-07-01/`
for rows 5, 6 and 8), and the D-GOV-06 contradiction surfaces were confirmed
live at HEAD.

Publication note: this corpus was committed 2026-07-01 (commit 836ff76f0);
the rulings were recorded and this index published to
`docs/governance_harness/` the same day.
