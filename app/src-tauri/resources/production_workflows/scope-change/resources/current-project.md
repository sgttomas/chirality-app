# Current PROJECT/SOFTWARE scope amendment

Use this profile where the project has adopted `ScopeOfWork.md` and
consumer-local `deliverable.yaml`. It replaces the retained contract/method's
phase/control-file obligations for this use. DOMAIN and explicitly adopted
legacy lifecycle projects keep those resources. Existing old files alone do
not select a legacy route. If governing project instructions conflict, identify
the conflicting requirement before acting; do not silently combine profiles.

WORKING_ITEMS owns the amendment through independent examination and its return.
The human owns changed commitments and the three grouped decisions below.
TASK can supply bounded contributions; delegation does not transfer integration
ownership. This profile changes no project scope merely by being selected.

## Basis and permitted changes

Identify the requested change, project root, accepted PRD/decomposition and
relevant companions, actual working carriers, affected localities, and exact
allowed writes. An immutable accepted snapshot is evidence, never the amendment
target. Where the only decomposition carrier is a snapshot, prepare a successor
working candidate and name its eventual pointer change in the propagation plan.
Keep the preceding basis recoverable. Preserve stable IDs and reserve retired IDs;
renumbering needs an explicit owner decision.

Separate changed purpose/commitments, decomposition allocation and downstream
implementation. A PRD revision keeps its actual approval route. This amendment
can carry exact PRD or ScopeOfWork edits only when the accepted propagation plan
names those carriers and their authorized decisions; otherwise return them to
the owning assignment. Approval of a PRD alone does not amend decomposition.
Ordinary factual reconciliation under unchanged commitments uses
`bounded-reconciliation`, not this formal amendment route.

Use the project's existing review/change record for the amendment. It must bind
an amendment identity, each grouped decision to its exact reviewed revision or
content, actions by entity/ID, impact, exact edits, allowed writes, propagation
owners, checks and remaining obligations. A committed reviewable document can
carry these together; separate registers or checkpoint directories are not
required unless the project adopted them. Preserve the decision-bearing basis
for each group before the next group relies on it. An action cannot gain authority
from a mutable proposal or an unaccepted poststate. Source history preserves
prior records; do not overwrite historical acceptance evidence.

## Group 1 — change and impact

Prepare the requested change and evidence-backed impact before asking for the
first decision. Identify the relevant objectives, PRD clauses, packages,
deliverables, criteria, inputs/consumers and derived publications. Distinguish
actual effects from assumptions and unknowns. Name which sources are governing
working carriers, accepted historical evidence or derivatives.

Check ADD IDs and parents, and account for every affected child and scope mapping
in REMOVE, MERGE, SPLIT or RECLASSIFY actions. Preserve the originating
partition, coverage and identity invariants. If a proposal changes the meaning
of those invariants, surface it as a contract-level change. Determine actual
consumer consequences rather than treating every reference as a whole-deliverable
finish-to-start constraint. The human accepts or returns the change and impact;
no governing source is changed by this first proposal.

## Group 2 — exact amendment and propagation

Prepare the exact amendment against the accepted predecessor and group-1 decision.
Name each action, affected entity, changed commitment/reference, file and exact
write boundary. Identify any changed requirement in the PRD and its actual owner
approval. List propagation work, its owner, required examination and disposition:
apply in the candidate, carry after acceptance, or explicitly leave outside scope
with the consequence stated. Do not represent a deferred obligation as fulfilled.

Where a source fact is intentionally superseded, identify its source location,
old meaning/value and accepted replacement in the amendment. An extension that
does not contradict the prior fact remains distinguishable. There is no need for
a parallel supersession register unless a selected consumer requires it.

ScopeOfWork edits may be included directly in the accepted boundary. Otherwise,
hand their exact revision scope to `scope-of-work MODE=REVISE` after group 3.
New localities are prepared by `project-setup` after group 3; do not create blank
contracts or new lifecycle/control files to represent the candidate. Retire an
entity in the governing decomposition with its amendment reference and retained
source; do not delete its files or fabricate a lifecycle transition. Retained
consumer conditions need their own disposition, not automatic removal.

The human accepts or returns the exact amendment and propagation plan. Record
the exact reviewed basis and allowed edits. Internal checks and repairs within
that basis add no approval prompts.

## Group 3 — independently examined poststate

Apply only the group-2 edits to the reviewable candidate. Keep accepted discovery
pointers on their preceding basis until this poststate is accepted. Re-derive
changed generated artifacts from maintained sources. Produce an action-by-action
comparison with the predecessor, applicable checks and unresolved obligations.

A separate reviewer who did not author/apply the amendment examines the entire
affected poststate against groups 1 and 2, source meanings, scope coverage,
identity/parent integrity, write boundaries and propagation dispositions. A
missing new locality deliberately deferred to setup is a pending setup obligation,
not an implementation success or an unexpected amendment defect. Keep both the
raw finding and its accepted disposition visible. New findings get their own
assessment; do not label them expected simply to obtain a pass.

Use actual current capabilities for the claims they support:

- Compare the affected decomposition/PRD sections and mappings directly against
  the accepted amendment and predecessor. No current decomposition validator is
  assumed merely because a legacy audit exists.
- For existing authored localities, run
  `zsh tools/validation/check_min_viable_fileset.sh --current <DEL-path> <DEL-ID>`
  and `python3 tools/scope_of_work/validate_scope_of_work.py <ScopeOfWork-path> --json`
  where relevant. The first needs zsh/Python/PyYAML; the second checks contract
  format, not substantive adequacy.
- Use `python3 -m tools.deliverables --project <project> check` and scoped queries
  for native declarations when Git/HEAD and Python/PyYAML are available. These
  observe structure/references, not satisfaction. If unavailable, read the
  affected declarations directly and state the unavailable check.
- Do not use legacy `_STATUS`/`_CONTEXT` structure audits as current-locality
  validators, even via an inventory option. Do not create their expected files.

Present the audited candidate, checks, remaining obligations and exact
acceptance-conditional edits: pointer changes, accepted-basis references and
any other changes that require group-3 acceptance. The human accepts or returns
that poststate. Apply only those listed conditional edits after acceptance and
check that the actual result matches the accepted candidate. Preserve the
reviewed evidence and identify the applied revision. A new substantive change
returns to the affected decision; unaffected decisions remain valid.

## Propagate and return

The accepted amendment is the hand-back to `project-setup`'s
[current-project route](../../project-setup/resources/current-project.md).
Use accepted IDs and changed scope only. Missing ScopeOfWork contracts use
`INIT`; existing valid contracts whose authorized changes were deferred use
`REVISE` under the current-project profile. `dependency-extract` authors/refreshes
actual affected consumer needs after their scope exists.

Check the accepted actions and deferred propagation against actual results,
using the current-project route of `audit-scope-closure`. Return amendment acceptance,
implementation/propagation completion and open conditions separately. Neither a
passing structure check nor amendment acceptance establishes product acceptance,
release or consumer adoption. The project retains its actual owners and holds.

On interruption, recover the last accepted decision basis, candidate state,
actual applied operations and remaining actions from the owning work/review.
Do not replay a write merely because its confirmation is missing. Preserve useful
partial work and request only a genuinely missing reserved decision.
