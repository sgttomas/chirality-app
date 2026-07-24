# tools/practitioner_harness — Charter

A practitioner bench tool over the Chirality governance corpus: it reads
authored files and git history, reports facts with sources, and refuses
objectively broken lifecycle writes. It is not a control plane, not a task
database, and none of its output is authority.

**Basis:** `plans/governance_harness_proposal-B_2026-07-01/governance_harness_plan_v3_2026-07-01.html`
(plan of record; terminal planning artifact) under decisions **D-GOV-01..07**
(`docs/governance_harness/_DECISIONS/`, ruled by the owner 2026-07-01, SHA-bound
at publication commit `82a35c545`) and **D-GOV-08** (ruled 2026-07-01,
publication commit `5f0f45c2b`; Option B — the warrant ladder is an audit-time
diagnostic, implemented by `evidence-check`). Design changes from here
supersede a D-GOV-* record or arrive as PR review — never a new plan document.

**Pilot scope (D-GOV-03):** `projects/chirality-app-dev`,
`projects/chirality-piping`, and the `_DomainEngines/` control area
(read + report only). `domains/*` deferred; `projects/chirality-governance/`
out of scope by construction; `.archive/` trees excluded from every walk.

## Commands

```sh
python3 tools/practitioner_harness/harness.py status --project app-dev
python3 tools/practitioner_harness/harness.py status --project piping
python3 tools/practitioner_harness/harness.py status --domain-engines
python3 tools/practitioner_harness/harness.py drift --all            # status-vs-history vs the recorded baseline
python3 tools/practitioner_harness/harness.py self-check             # restated-state surface audit
python3 tools/practitioner_harness/harness.py bridge-status          # bridge owner-shaped act pick-list (the tool never selects)
python3 tools/practitioner_harness/harness.py next                    # active-work pick-list (the practitioner selects)
python3 tools/practitioner_harness/harness.py brief --project piping --deliverable DEL-02-04
python3 tools/practitioner_harness/harness.py brief --verify-adoption docs/governance_harness/briefs/TRB-….md
python3 tools/practitioner_harness/harness.py run-validations --brief docs/governance_harness/briefs/TRB-….md [--list] [--timeout-seconds N]
python3 tools/practitioner_harness/harness.py scope-check --brief docs/governance_harness/briefs/TRB-….md --diff <rev-or-A..B>
python3 tools/practitioner_harness/harness.py evidence-check --brief docs/governance_harness/briefs/TRB-….md
python3 tools/practitioner_harness/harness.py closeout-digest --brief docs/governance_harness/briefs/TRB-….md --diff <rev-or-A..B> [--write-digest]
python3 tools/practitioner_harness/harness.py coord-check --diff <rev-or-A..B>
```

Markdown report to stdout; machine-readable JSON via `--json-report` (must
resolve under the declared generated root). `--strict` makes REVIEW findings
exit nonzero.

## Authority classes (plan v3 §Authority Classes)

| Artifact | Class |
|---|---|
| `_STATUS.md`, `_CONTEXT.md`, decision records, dependency registers, DAG approvals, domain profiles | **Authority**, subject to each artifact's own ratification/ruling status, which reports label |
| Engine-owned domain stores (OpenPipeStress persistence) | **Authoritative domain truth** under K-DOMAIN-1 and the adopted profile; outside this tool's cache rule |
| `_harness/adapter.yaml` | **Harness configuration authority only** — governed, committed, human-reviewed; never lifecycle or project truth |
| Tranche brief (CANDIDATE) | **Generated projection** — source-cited, rebuildable, non-authority footer |
| Tranche brief (HUMAN_ADOPTED) | **Committed governed fence** (D-GOV-04); an adoption existing only in a scratch directory does not exist. Detected — never granted — by `brief --verify-adoption` (see the Phase 3 section below) |
| Evidence records (`run-validations`, schema `practitioner-harness-evidence/v1`) | **Factual evidence artifact** — never approval, never lifecycle state; readable back as facts for its own tranche only (see Self-exclusion) |
| Closeout digest (`closeout-digest --write-digest`) | **Generated digest** — an input to the human CHANGE closeout; never a lifecycle transition or judgment |
| Status / drift / self-check / bridge-status / coord-check reports | **Generated view** — never authority, never read back as input |
| Local index cache (none yet) | **Rebuildable projection** — gitignored, one-command regeneration, never cited (D-GOV-01) |
| `write_status.sh` guard | **Refusal mechanism** — blocks objectively broken transitions; never approval, never authorship |

## Write posture — three categories, no unqualified "read-only"

1. **Read-only inspection** — `status`, `drift`, `self-check`,
   `bridge-status`, `next`, `scope-check`, `evidence-check`, `closeout-digest` without
   `--write-digest`, `coord-check`, `run-validations --list`: byte-identical guarantee over
   governed files (tested).
2. **Generated-artifact output** — `brief`, `run-validations` evidence
   records, `closeout-digest --write-digest`, report emission: writes land
   only under the declared generated root `{REPO_ROOT}/_harness_generated/`
   (gitignored; safe to delete; rebuildable). Path containment is enforced
   (symlinks, `..`, absolute paths resolved before the check; violations
   refuse, exit 2).
3. **Write-path guard** — `tools/scaffolding/write_status.sh` preconditions:
   ships with the harness, lives outside it. Refuses; never authors.

## Self-exclusion — two classes

Narrative projections (status/drift/self-check reports) are never read back by
any harness component as input. Evidence records (written by
`run-validations`, read back only by `evidence-check`) may be read as facts
for the tranche that produced them and never promote to lifecycle, approval,
plan, or project status.

## Cache contract

For Chirality governance state and harness projections, the only permitted
database pattern is a rebuildable, gitignored cache regenerated from files by
one command, safe to delete, never cited as authority (D-GOV-01). This rule
does not reach developer tooling caches, and it does not reach engine-owned
domain stores (K-DOMAIN-1; D-GOV-01 scope note). No cache is implemented:
the Phase 5 cache precondition (query pain) was measured unmet on 2026-07-02
(slowest command, `self-check`, ~4 s) and the cache half stays closed until
the owner directs otherwise.

## CI wrapper (Phase 5, CI half)

`.github/workflows/governance-harness.yml` runs the harness test suite and
`self-check` on every pull request and push to main. Objective BLOCK findings
exit nonzero per the D-GOV-02 contract and fail the run; REVIEW and below
exit 0 and never gate — human judgment stays human. The wrapper adds no
checks and holds no authority; authority stays in authored files (D-GOV-01).
Landed 2026-07-02 on owner re-ruling of the Phase 5 CI half after Phases 3-4
made the BLOCK surface real (register item 10 addendum).

## Claim language

No harness output says approved, issued, professionally accepted, certified,
sealed, safe, ready for construction, or closed — unless quoting a labeled
human-authored governed artifact. It says narrower things: the artifact is
present or absent; the approval SHA is missing, TBD-pending-publish, reachable,
or unreachable; two current-truth sources conflict; human review required.
Lifecycle state names (`CHECKING`, `ISSUED`) appearing as parsed data values
are quotations of governed sources, not claims. Enforced by
`test_claim_language.py`.

## Severities and exit codes (D-GOV-02)

| Severity | Meaning | Exit behavior |
|---|---|---|
| BLOCK | Objective violation within the declared observation boundary | exit 1 (override: human only, recorded) |
| REVIEW | Material issue requiring human judgment | exit 0 (`--strict`: exit 1) |
| WARN / INFO / NOT_APPLICABLE | Hygiene / context / preconditions absent | exit 0 |

Exit 2 = operational error or refusal (missing identity allowlist per
D-GOV-04, unparseable manifest, output-path containment violation). The
harness adopts 0/1/2 aligned with the newest validator class
(`tools/validation/validate_domain_engine_profile.py`); older tools vary.
`Ruling SHA: TBD` is conditional per D-GOV-02: REVIEW when the artifact
self-declares bind-at-publish; BLOCK only when relied on as bound authority.
No BLOCK ever attaches to the CHECKING→ISSUED judgment itself (K-GATE-1).
Findings against a brief that is not committed + HUMAN_ADOPTED cap at REVIEW
(D-GOV-04).

## Ratification labeling (K-CLAIM-1)

Every report labels the ratification status of each invariant it checks.
Basis: full ratification of docs/CONTRACT.md by owner act on 2026-07-11
(recorded in the docs/CONTRACT.md status block; app-dev loop Receipt 9) —
the entire K-* Invariant Index (27 IDs) is RATIFIED, alongside the
source-of-truth rule (DIRECTIVE §2.1/§2.3), the generated-output rule
(D-GOV-01), and the D-GOV-02 severity taxonomy (TYPES §11). D-GOV-05
(ruled 2026-07-01) is kept as the historical record of the earlier partial
basis. The DRAFT-advisory downgrade rule remains in force for any future
not-yet-ratified invariant (uncataloged K-* IDs label DRAFT fail-closed):
findings on DRAFT invariants are advisory (never BLOCK), except purely
local technical checks — path containment, source-file existence,
generated-output labeling — which may BLOCK regardless.

## Identity (D-GOV-04)

`docs/governance_harness/human_actors.md` is the identity source for
RuledBy/AdoptedBy/HumanRuling attribution matching. Identity-dependent checks
refuse (exit 2) when it is absent or an attributed actor does not match —
refuse rather than guess.

## Brief adoption and committed-adoption verification (Phase 3)

Brief lifecycle (metadata on harness artifacts only — never the deliverable
lifecycle): `CANDIDATE → HUMAN_ADOPTED → EXECUTED → CHECKED → HUMAN_REVIEWED
→ CLOSED/SUPERSEDED`.

**Adoption is a human act (D-GOV-04).** A brief becomes an enforceable fence
only when a human sets its state to `HUMAN_ADOPTED`, attributes themselves
(`adopted_by:` matching `docs/governance_harness/human_actors.md`), and the
brief is **committed** to the governed record. No harness command flips a
brief's state — `brief` emits CANDIDATEs (with adoption placeholder fields
and an `## adoption` section stating the human steps), `next` lists active
work, and `brief --verify-adoption <path>` detects the adoption posture;
none of them adopts, and verification of adoption metadata is not a judgment
on the work and never a lifecycle transition.

Verification semantics (`brief_adoption.verify_adoption`; nothing here BLOCKs
— Phase 3 introduces only REVIEW/WARN/INFO findings and exit-2 refusals per
D-GOV-05):

| Brief posture | Result |
|---|---|
| state `CANDIDATE` | fence inactive; INFO `BRIEF_NOT_ADOPTED` (a candidate projection fences nothing; no identity check — no human is attributed) |
| adoption claimed (`HUMAN_ADOPTED`/`EXECUTED`/`CHECKED`/`HUMAN_REVIEWED`), file under `_harness_generated/` (path components matched **case-insensitively** — fail-closed for adoption on case-insensitive filesystems; the write guard stays case-sensitive, fail-closed for writes) | fence inactive; REVIEW `ADOPTION_IN_SCRATCH_DIR` — an adoption existing only in a scratch directory does not exist for reliance (D-GOV-04) |
| adoption claimed, file untracked by git | fence inactive; REVIEW `ADOPTION_NOT_COMMITTED` (K-AUTH-2 / D-GOV-04) |
| adoption claimed, tracked but working copy differs from HEAD | fence inactive; REVIEW `ADOPTION_UNCOMMITTED_EDITS` — K-AUTH-2 binds adoption to committed content; the uncommitted edit is not part of the adopted fence |
| adoption claimed, committed clean, actor matched | **fence active**; `bound_sha` = the publication commit (`git log -1 --format=%H -- <path>`; K-AUTH-2), reported as the sourced fact `brief.adoption_bound_sha` |
| state `CLOSED`/`SUPERSEDED` | same identity + committed checks (a terminal brief still claims adoption), then fence inactive; INFO `BRIEF_LIFECYCLE_TERMINAL` — a terminal-state brief no longer fences new work. When the adoption is committed clean, `bound_sha` is still populated with an explicit caveat: the SHA binds the committed adoption record, not an active fence — `fence_active` alone gates enforcement |

The scratch classification is a lexical read-path check (the resolved brief
path against `{REPO_ROOT}/_harness_generated`), deliberately decoupled from
the write guard: a symlinked `_harness_generated/` (which the write side
refuses) does not break verification of an unrelated, correctly committed
brief.

**Refusal rules (exit 2, never findings):** when the identity allowlist is
absent, or the brief claims adoption with no `adopted_by`, or the attributed
actor matches no allowlist entry, verification REFUSES rather than guesses
(D-GOV-04). Unknown brief state, a missing brief file, or a path outside the
repo root are operational errors (exit 2, K-INVENT-1) — never guessed. A
brief path carrying a `..` component, or passing through a **symlink** at any
component, is likewise refused (exit 2): resolving it would silently verify a
different file than the one named — committed-adoption verification requires
the real committed path (the write-side machinery refuses symlinks for the
same fail-closed reason).

**`next` and CLI aliases:** the ready-made `brief --project … --deliverable …`
command line in a `next` row is emitted only for project roots with a
registered CLI alias (reverse-mapped from `harness.py` `PROJECT_ALIASES`;
where two aliases share a root the shorter wins). A root with no registered
alias gets a labeled note in place of the command — a command line is never
fabricated (K-INVENT-1).

**`blocked-on` status tokens:** a deliverable `_STATUS.md` may include an
optional field line `blocked-on: D-XX[, D-YY]` or `**blocked-on:** D-XX[, D-YY]`.
The adapter treats these as decision-link metadata only: they do not change
`Current State`, do not resolve decisions, and do not select work. `next`
quotes the tokens beside active rows, and `bridge-status` builds the reverse
index from owner-side decision rows to tagged deliverables.

**fence_active and the REVIEW cap:** the Phase 4 `scope-check` BLOCK runs
only against verified fences (`fence_active` true). Findings referencing
anything else — candidates, scratch-dir/untracked/dirty adoptions, terminal
briefs — cap at REVIEW via
`harness_common.cap_severity_for_unadopted_brief`, with
`BriefFence.cap_reason` as the recorded reason. (The `run-validations`
mutation BLOCK is deliberately outside this cap — see Phase 4 below.)

**Location posture:** the harness does not dictate where adopted briefs live —
any committed governed path works; suggested convention:
`docs/governance_harness/briefs/`. The generated root `_harness_generated/`
is gitignored scratch and never qualifies.

## Phase 4 checks (run-validations, scope-check, evidence-check, closeout-digest)

Four commands, all brief-anchored (`--brief`; committed-adoption posture is
verified first, and identity refusals execute/judge/verify nothing — exit 2):

| Command | What it does |
|---|---|
| `run-validations --brief [--list] [--timeout-seconds N]` | Executes the validation commands declared in the adapter manifest (the governed declaration source; the brief's validations text is cross-checked and drift surfaced as WARN `VALIDATION_DECLARATION_DRIFT` — the manifest governs) for the project resolved from the brief's first `write_scope` entry, under the mutation-control contract below. One evidence record per command, regardless of outcome. `--list` prints the resolved command list and stops: nothing executed, nothing written. Facts, never approval; a completed exit-0 run is structural evidence only (K-DOMAIN-4 analogue). |
| `scope-check --brief --diff <range>` | Compares tracked paths changed in the git range (`git diff --name-status`; rename entries contribute both sides; the range is validated with `git rev-parse` first — unresolvable = exit 2, K-INVENT-1), plus currently observed untracked non-ignored files, to the brief's fence. Findings report only; path judgment is never lifecycle judgment (K-GATE-1). |
| `evidence-check --brief` | Verifies evidence COMPLETENESS for the manifest-declared validations per the provenance ladder (D-GOV-08 Option B: the warrant ladder is an audit-time diagnostic, never a producer-emitted state). Evidence older than the newest commit touching the `write_scope` is flagged `EVIDENCE_STALE` (naming both timestamps). For dating the scope, each `write_scope` glob reduces to its literal directory prefix before the first wildcard component (never passed verbatim as a git pathspec — git's `*` semantics differ from the fence matcher's); an all-wildcard scope (e.g. a bare `**`) dates against the newest commit in the WHOLE repository (pathspec `.`), stated in the output — never silently skipped. Unreadable record files are `EVIDENCE_UNPARSEABLE` — labeled, never guessed. Completeness, never sufficiency; nothing here BLOCKs. |
| `closeout-digest --brief --diff <range> [--write-digest]` | Composes scope-check + evidence-check IN-PROCESS (imported run functions, never shelled out): changed files by fence classification, captured evidence, the two check summaries, skipped (NOT_APPLICABLE) checks, caveats, and the brief's open human decision points. Findings are the union of the sub-checks', deduplicated by (code, source, line) — but the digest is a composition, NEVER a gate: any sub-check BLOCK is carried downgraded to REVIEW with a caveat naming the gating command (run scope-check for the gating exit code), so a composed BLOCK never makes the digest exit 1 (D-GOV-02: exit 1 iff a BLOCK finding is in the digest's own report). `--write-digest` writes the digest to `_harness_generated/closeout/<tranche_id>.md`; without it, nothing is written. |

**The run-validations mutation-control contract** (plan v3, applied in
order): (1) record pre-run `git status --porcelain` (taken with `--ignored`
so ignored-cache writes are observable at all) plus a content fingerprint
(`git hash-object` over worktree bytes) of every tracked porcelain entry;
(2) run only declared commands — the adapter manifest is the governed
declaration source; (3) capture stdout/stderr, exit code, duration, tool
versions where cheap; (4) record post-run porcelain and re-fingerprint the
union of pre/post tracked entries — a file that was ALREADY dirty before
the run and is mutated further keeps its status code (" M" stays " M"), so
same-status content mutation of already-dirty tracked files is caught by
content comparison, not status codes; (5) classify changed paths:
`expected_evidence_output` | `ignored_cache` | `unexpected_tracked_change` |
`review_required_untracked`; (6) BLOCK if a validation command modified
governed files outside the declared evidence/output paths.

**"Declared evidence/output paths" means:** the generated root
(`_harness_generated/`, harness-owned gitignored scratch — D-GOV-01)
ALWAYS, plus the brief's `evidence_targets` ONLY when the fence is active
(a human adopted those targets — D-GOV-04). An unadopted/CANDIDATE brief's
`evidence_targets` exempt nothing: run-validations deliberately runs on
unadopted briefs, and an agent-authored brief must not be able to declare a
broad governed path as an evidence target and swallow governed-file
mutations — the mutation BLOCK protects the substrate and is not
suppressible by anything agent-authored (K-WRITE-2).

**Known mutation-detection boundary (stated, not papered over):** appends
to a PRE-EXISTING untracked file remain invisible to porcelain diffing —
the entry reads `??` both before and after the run, and untracked files are
not fingerprinted. New untracked files ARE observed
(`review_required_untracked`), and tracked files are covered by status +
content comparison.

**Exactly two BLOCK-capable findings exist in Phase 4:**

1. `scope-check` objective tracked-path fence violations
   (`PROHIBITED_PATH_TOUCHED`, `SCOPE_VIOLATION`; deny wins over allow) —
   **only when `fence_active` is true** (D-GOV-04). Against an unadopted /
   uncommitted / terminal brief the finding is created at BLOCK and
   immediately capped at REVIEW with the fence's `cap_reason`. Observed
   untracked files are judged the same way but sit outside the objective
   tracked-path boundary, so they cap at REVIEW always (stated in the
   caveat).
2. `run-validations` governed-file mutation outside declared evidence/output
   paths (`VALIDATION_MUTATED_GOVERNED_FILES`) — **unconditional**. This
   BLOCK protects the substrate (K-WRITE-2, ratified basis per D-GOV-01/05
   and the 2026-07-11 full ratification of docs/CONTRACT.md),
   not the fence, so the D-GOV-04 adoption cap never applies: a validation
   command must not be a backdoor write tool no matter whose brief invoked
   it (plan v3 risk table: "Backdoor writes through validation commands →
   BLOCK on governed-file mutation outside declared paths"). For the same
   reason the exemption side is fence-gated: only the generated root and an
   ADOPTED brief's `evidence_targets` count as declared evidence/output
   paths (see above) — an unadopted brief cannot carve holes in this BLOCK.

Nothing in `evidence-check` or `closeout-digest` ever BLOCKs — completeness
is never sufficiency, and no BLOCK ever attaches to a lifecycle judgment
(K-GATE-1). `closeout-digest` composes the sub-checks' findings but carries
any sub-check BLOCK downgraded to REVIEW with the gating command named: the
digest is never a gate, and its exit code (D-GOV-02: exit 1 iff a BLOCK
finding is in ITS report) therefore never turns 1 through composition.

**Fence path matching** (`scope_fence.py`): `write_scope` /
`prohibited_paths` glob entries compile to anchored regexes over POSIX
repo-relative paths — `**` matches across segments (a trailing `/**` is
strictly under the directory), `*` within one segment, `?` one character;
case-sensitive full match (the fence is what the human adopted, case-exact);
deny (prohibited) wins over allow (write_scope); no dotfile carve-out.

**Provenance ladder** (`evidence-check`; D-GOV-08 Option B): (1)
harness-captured evidence records satisfy completeness; (2)
timestamp-consistent external artifacts at declared `evidence_target` paths
outside the generated root satisfy at REVIEW (`EVIDENCE_EXTERNAL_ARTIFACT`);
(3) bare prose attestations never pass silently — an absent artifact is
reported as `EVIDENCE_MISSING`, never accepted on narrative.

**Blind-spot honesty:** every `scope-check` and `closeout-digest` output
(refusals included) carries the fixed statement of what it cannot see:
untracked files beyond those listed, writes outside the repository, changes
made and reverted inside the diff range (revert games), and gitignored
paths.

**Evidence records** (`evidence_records.py`, schema
`practitioner-harness-evidence/v1`): land at
`_harness_generated/evidence/<tranche_id>/NNN_<slug>.json` (NNN = 3-digit
per-command-slug run ordinal — re-invocations append, never overwrite) plus
a sibling `.md` summary carrying the standard generated header. Fields:
brief posture (source path, state, bound SHA, `fence_active`), command, cwd,
`declared_in`, exit code (null when timed out) / `timed_out`, duration,
`captured_at` (UTC), cheap tool-version probes, stdout/stderr (200 000-byte
cap per stream with an explicit truncation marker), pre/post porcelain
snapshots, classified `changed_paths`, disclaimer. A timed-out command is
recorded TIMED_OUT — an unobserved outcome is never inferred (K-INVENT-1).
Two-class self-exclusion reminder: these records are readable as FACTS for
the tranche that produced them (that is what lets `evidence-check` work) and
never promote to lifecycle, approval, plan, or project status.

**closeout-digest posture:** the digest is an INPUT to the human CHANGE
closeout — never a lifecycle transition, never a lifecycle judgment, never
acceptance of residual risk, and never a gate. The gates are the sub-checks
(`scope-check` for the fence, `run-validations` for mutations): a sub-check
BLOCK appears in the digest downgraded to REVIEW with a caveat naming the
gating command to run for the gating exit code. The human decides; the
digest only collects.

## Drift baseline

Measured and verified 2026-07-01: **92 of 154** `_STATUS.md` files under the
two pilot `execution/` trees disagree with their own last parsed history
assertion — all 92 in chirality-piping (101 files), app-dev 0/53 clean. The
shared signature: history records an approved advance to CHECKING while the
frontmatter `Current State:` line still reads IN_PROGRESS. `drift` reports
run-over-run counts against this baseline, split by project and caveat class
(`PARSED` / `PARSED_WITH_ASSUMPTIONS` / `UNPARSEABLE`; unparseable histories
are labeled, never guessed). Success is this number trending down; failure is
this tool becoming a cleaner-looking second source of truth.

**Resolved to 0/154 on 2026-07-02**: the owner ruled the class-wide
K-CONFLICT-1 conflict ("all shall be IN_PROGRESS" — header authoritative;
the 2026-06-16 header reversals were affirmed and the missing reversal
history entries authored, one parser-verified line per file). Ruling record:
`projects/chirality-piping/execution/_Reconciliation/LifecycleCorrection/LIFECYCLE_CORRECTION_2026-07-02_2050/Decision_Log.md`.
The recorded adapter baseline was re-measured to 0/101 in the same act; the
live pin in `test_live_baseline.py` carries the matching conscious update.

## Project-tree abs-path lint (GEN-8) and agent-registry currency (GEN-9)

**GEN-8 (SPEC §0.2.4).** GEN-1 stays control-area per-line; GEN-8 extends the
machine-absolute-path audit through the shared `surface_roles.py` policy.
Active managed-run and live-entry surfaces have one structural role:
`CONTROL`, `EVIDENCE`, or `UNCLASSIFIED`. Control classification takes
precedence. Evidence is limited to exact registered names (`RETURN.md`,
`RETURN_V<n>.md`, `HANDOFF_STATE.md`, `STATUS.json`, `STATUS_V<n>.json`,
`RUN_RECORD.md`, `INTERRUPTION_RECORD.md`, and `TOOL_ERROR_RECORD.md`) or the
structural `_run_records/` directory. Token-bearing near matches never inherit
evidence status; unknown AgentRuns artifacts fail closed.
Historical and non-active project files remain aggregate observability facts,
not an exact path baseline and not implicit evidence.

Projects may declare `validation/portability_policy.json`. Its migration
overrides and historical control exceptions are bound to normalized
repo-relative paths, whole-file SHA-256, non-empty reason, and authority.
Missing targets, hash drift, duplicates, role mismatch, or entries whose path
has disappeared are actionable policy findings. Valid control exceptions stay
visible as sourced facts. Acceptance is semantic: zero unacknowledged active
control paths, zero active unclassified paths, and zero policy issues.
GEN-8 audits **git-tracked files only**: gitignored build output (`dist/`,
`target/`, `.next/`, packaged `.app` bundles) is not authored governance
truth (D-GOV-01) and is excluded. Outside a Git worktree the fixture walk is
unrestricted. No aggregate severity total or full-tree path set is pinned.
`validate_path_anchors.py` consumes the same role policy for managed project
records while retaining its narrower repo-level live-entry boundary.
HB-10 closes the same class at the pre-commit seam: `coord-check --diff`
uses the same role classifier to flag machine-absolute paths on lines a diff
ADDS to controls or unknown coordination artifacts (`COORD_ABS_PATH_ADDED`).
Thus newly changed coordination remains fail-closed even when an older record
is outside the active self-check boundary.

Raw reproduction `stdout/*.txt` and `stderr/*.txt` are a separate storage
concern. The piping project marks only those checksum-governed files
`-diff -merge -text`; this preserves exact bytes and prevents raw output from
being treated as authored text. Markdown, JSON, briefs, and all other authored
surfaces remain subject to normal Git whitespace checks.

**GEN-9 (K-AGENTS-1).** Runs once per invocation against the repo-root
`AGENTS.md` + `agents/` regardless of `--root` (same posture as GEN-4);
`NOT_APPLICABLE` when either is absent. Forward direction: every distinct
backticked `AGENT_*.md` file token cited in `AGENTS.md` must resolve to a
live file under `agents/` outside `.archive/`, else `REGISTRY_TARGET_MISSING`
(REVIEW, anchored at the first citing line; a same-named copy under the
gitignored `agents/.archive/` is noted only when the runtime probe finds it —
fresh worktrees never materialize gitignored trees). Reverse direction: every
live top-level `agents/AGENT_*.md` file must appear in the registry text,
else `AGENT_FILE_UNINDEXED` (WARN). Per K-AGENTS-1, where live registries and
narrative disagree, the live registry governs and the discrepancy is
surfaced; fix-vs-retain is a human disposition. v1 observation boundary: file
tokens only — role-name narrative mentions (a bare DELIVERABLE_TASK word in
prose) are out of scope. Neither check ever BLOCKs — by the checks' own
severity design (hygiene surfacing; fix-vs-retain is a human disposition);
SPEC §0.2.4 and K-AGENTS-1 are RATIFIED (owner ratification 2026-07-11).

## Parser: prose-bullet-v1

Versioned parser plugin agreeing with the TypeScript prior art
(`projects/chirality-app-dev/frontend/src/lib/lifecycle/status-parser.ts`) on
the strict grammar, plus eight prose rules for the piping dialect (each hit
labeled `PARSED_WITH_ASSUMPTIONS`). Deliberate v1 limits (documented in the
module): "preserved/retained/kept/verified as X" prose and evidence-lifecycle
bullets ("promoted to COMMITTED") do not yield deliverable states — they are
UNPARSEABLE by design until the History trailer grammar rides D-GOV-05.
Configuration first, parser code only for a genuinely new dialect.

## Guard reconciliation (write_status.sh vs transition.ts)

`tools/scaffolding/write_status.sh` now enforces preconditions reconciled with
chirality-app-dev's `frontend/src/lib/lifecycle/transition.ts` (DEL-07-04):
same six-state order with backward-transition blocking; same allowed from→to
pairs; HUMAN-only CHECKING/ISSUED; same approval-SHA format rule
(`^[0-9a-f]{7,64}$`). Adapter-declared per root (D-GOV-03): app-dev declares
approval-SHA fields, so the git-verifiable SHA precondition blocks there;
piping's status schema carries no SHA fields, so an absent SHA surfaces as
REVIEW and proceeds (schema alignment is a separately-ruled parked item).
Recorded divergences from transition.ts:

1. **Laxer pre-human actor vocabulary.** `transition.ts` binds each transition
   to a fixed actor list (e.g. OPEN→INITIALIZED only `4_DOCUMENTS`); the guard
   accepts any non-empty actor for pre-CHECKING transitions because the live
   corpus contains more spellings (`PREPARATION`, `TASK+*`, `ORCHESTRATOR*`,
   `CHIRALITY_FRAMEWORK`, `WORKING_ITEMS`) and hard enforcement would
   false-block lawful scaffold flows. CHECKING/ISSUED remain HUMAN-only, with
   the same actor normalization (uppercase, whitespace→`_`,
   USER/OPERATOR/HUMAN*→HUMAN).
2. **Same-state re-assert allowed with WARN** (`transition.ts` refuses it as
   TRANSITION_NOT_ALLOWED); the corpus contains lawful re-assert history lines.
3. **New-file creation permitted at OPEN** (`transition.ts` only transitions
   existing documents); creation at any other state is refused.
4. **`--force-human-override <reason>` exists** (HUMAN-only; reason recorded in
   the history line as `[override: ...]`; never overrides usage errors) —
   BLOCK override is human-only and recorded, per D-GOV-02. `transition.ts`
   has no override path.
5. **Approval-SHA requirement is adapter-conditional**
   (`guard_requires_approval_sha` in `_harness/adapter.yaml`), not
   unconditional as in `transition.ts`; no-schema roots get REVIEW-and-proceed.
   The SHA is additionally checked for git reachability
   (`git cat-file -e <sha>^{commit}`), which `transition.ts` does not do.
   Format matched case-insensitively, mirroring `transition.ts`.
6. **Invalid state is exit 2 (usage)** rather than the pre-guard script's
   exit 1, aligning with the adopted operational-error convention.

Stated honestly: tool usage is guided operationally, not enforced — hand edits
bypass any guard. The guard hardens the sanctioned path; drift detection
exists precisely because hand edits happen.

## Generated-view header

Every generated report and brief carries:

> **Generated view — not authority.** Produced by tools/practitioner_harness.
> Sources cited per finding; on any disagreement the cited source files govern.
> Regenerate from project files; safe to delete. Structural checks are not
> approval, issue, authentication, or acceptance of residual risk (K-AUTH-1;
> D-GOV-01).

Missing this header on a file under the generated root is a BLOCK
(`generated_disclaimer_missing`).

## Tests

Co-located pytest (`python3 -m pytest tools/practitioner_harness -q`):
read-only guarantee (byte-identical governed files), drift fixtures modeled on
the `_DomainEngines/` contradictions, path containment (absolute, `..`,
symlink, case), exit-code contract, parser grammar + caveat classes, claim
language, guard behavior matrix, the stale-open-issue (`STALE_OPEN_ISSUE`,
K-STALE-2) and draft-basis-used-as-binding (`DRAFT_BASIS_AS_BINDING` /
`DRAFT_BASIS_RULED_CLOSED`, K-CLAIM-1) checks with their archive fixture
corpus (`test_archive_fixture_corpus.py`), the `_LATEST*` pointer-currency
check (`POINTER_TARGET_UNRESOLVED` / `POINTER_TARGET_NOT_NEWEST`, K-PROV-1 /
K-STALE-2; REVIEW only — judgment-adjacent per D-GOV-02, never BLOCK;
`NOT_APPLICABLE` for roots without pointer files; `test_pointer_currency.py`),
the project-tree abs-path lint (`ABS_PATH_IN_PROJECT_SURFACE`, SPEC §0.2.4;
per-file REVIEW, evidence/unclassified counted as facts, GEN-1 control-area
per-line behavior pinned unchanged; `test_abs_path_lint_fixtures.py`, with
all synthetic-`fixture`-home-prefix content as in-module string constants), the
agent-registry currency check (`REGISTRY_TARGET_MISSING` REVIEW /
`AGENT_FILE_UNINDEXED` WARN / `REGISTRY_CHECK_NOT_APPLICABLE`, K-AGENTS-1;
never BLOCK; `test_agent_registry_fixtures.py`), and a live-tree baseline
test (0/154 after the 2026-07-02 class correction, originally 92/154; the
three owner-retained stale surfaces must be detected by
`self-check`; `STALE_OPEN_ISSUE`/`DRAFT_BASIS_AS_BINDING` pinned at zero and
`DRAFT_BASIS_RULED_CLOSED` at seven on the live tree; the retired piping
reconciliation pointer pinned as the pointer check's first detection target;
the GEN-8 19-file instruction-class baseline with
`plans/pi-agent-harness-assessment.md` pinned worst at 21 hit lines; the
GEN-9 `AGENT_DELIVERABLE_TASK.md` registry drift pinned at `AGENTS.md:89`
with the reverse direction clean). Phase 3 brief-adoption coverage
(`test_brief_adoption.py`, tmp-git-repo fixtures): parse exactness for the
brief format (including the header/section boundary — a `- state:`-shaped
bullet after the first H2 never overrides the header), the committed-adoption
verification matrix above (candidate, committed-clean SHA binding, scratch-dir
including case-variant spellings, untracked, dirty, terminal — with the
terminal `bound_sha` caveat and cap-reason stacking), symlinked and
`..`-containing brief-path refusals, identity refusals (allowlist absent /
unmatched actor → exit 2), CLI exit-code pins (REVIEW = 0 default / 1 under
`--strict`; clean adoption = 0 with nothing on stderr), a generate→parse
round-trip, and the `next` pick-list (counts, precedence ordering, DEL-id
rule, the no-alias posture, explicit truncation). Phase 4 coverage
(`test_run_validations.py`, `test_scope_evidence_closeout.py`; harmless
`echo`/`python3 -c` fixture commands only — the real pilot manifests are
never executed): the mutation-control contract end to end (happy path,
unconditional mutation BLOCK with and without an active fence, the
fence-gated evidence_targets exemption — a CANDIDATE brief's broad governed
target exempts nothing and still BLOCKs, an ADOPTED brief's target classifies
the same write as expected_evidence_output; already-dirty tracked files
mutated further are caught by content fingerprints, with no false positive
when untouched; ignored-cache and untracked classifications, TIMED_OUT,
stream truncation, `--list` running/writing nothing, declaration drift,
refusal executing nothing), the evidence-record schema/writer/reader
(UNPARSEABLE labeling, per-slug ordinals), the fence matcher (case-variant
no-match, nested `**`, deny-wins, dotfiles, strictly-under `/**`),
scope-check (in-fence clean + blind-spot presence, active-fence BLOCK =
exit 1, candidate cap to REVIEW with cap_reason, prohibited hits with
deny-wins exercised through the integration path and the exit-1 pin,
untracked REVIEW-never-BLOCK, rename both sides, unresolvable range =
exit 2), evidence-check (satisfied / missing / stale / unparseable /
no-validations NOT_APPLICABLE / mutation-flagged / external-target ladder
rungs — never a BLOCK; whole-repo `**` write_scope dated against the newest
repo commit and labeled, plus pathspec-prefix derivation units),
closeout-digest (in-process composition with (code, source, line) dedup,
sub-check BLOCK downgraded to REVIEW with the gating-command caveat — the
digest exits 0 where scope-check exits 1 on the same state, `--write-digest`
containment + generated header, claim-language-clean output, 0/2 CLI pins
with `--strict` as the REVIEW escalation), and the Phase 4 read-only
additions in `test_readonly_guarantee.py` (scope-check, evidence-check, and
closeout-digest without `--write-digest` leave the governed tree
byte-identical and write nothing).

**Fixture corpus.** The adversarial fixtures in
`test_archive_fixture_corpus.py` are verbatim pre-images from
`git show 15c958e06^` (the state before the D-GOV-06 cleanup slice), with
machine-absolute paths re-anchored to a synthetic `fixture` home-directory
prefix. They live as string constants inside `test_`-prefixed modules on
purpose: loose fixture data files under `tools/` carrying home-dir-absolute
content would fail `tools/validation/validate_path_anchors.py`, and `tools/`
ships verbatim into the public export.
