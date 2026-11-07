# Library 2.1.0 operational receiving

**Subject.** App development-agent practice and its compatibility harness receive
Chirality library 2.1.0 (`library-v2.1.0`, commit
`c35b7bbc463f81c1fed566c744ea49d168d29eee`). Source identity and the partial
test-source fixture are in [`reference/library-v2.1.0/`](../../../../reference/library-v2.1.0/README.md).
This serves SOW-216/217 (identified editions, deliberate change, owning adoption
record); the ScopeOfWork and its dependency conditions are unchanged.
`deliverable.yaml` names the focused harness in `checks`; no dependency or
maturity condition changes.

**Authority.** The owner requested deliberate operational/harness receiving on
2026-11-07. The prior operational selection was `library-v2.0.0`
(`2f981163d76772d3779697d9def1a9e951d978e7`), with
`coordinated-knowledge-work` as the governing method. That method's
`WORKFLOW.md` bytes are identical in both editions. App Agent 0 retains receiving/design choices, independent review and final
integration. Owner-reserved acceptance/release decisions remain reserved.

## What App practice receives

- **Opt-in INTERLOCUTOR.** A fifth official role, Type 2, used only when a
  session selects it. It is not a direct entry or a default. HELP_HUMAN,
  HELPS_HUMANS and WORKING_ITEMS may delegate it; it delegates nothing and has
  no generalist Agent 2. It advises Agent 0 on its effectiveness and direction.
  Where selected, Agent 0 supplies periodic summaries and consults it at least
  before every PR merge. After three rounds without convergence, Agent 0
  explains its view and proceeds within its authority. The advice carries no
  sign-off, veto, permission or override. Models and preferences are not
  inferred. Recorded in `AGENTS.md`; `docs/OPERATING_METHOD.md` V4-OPS-03 gains a
  forward clarification retaining the accepted four-role basis.
- **Method eligibility.** `chirality-method-index/v1` remains, now with 76
  entries; none names INTERLOCUTOR. Inclusion in the index does not make a
  method eligible for every project or role. A method without an execution
  companion still serves the four original roles. INTERLOCUTOR needs a method
  whose `compatible_roles` names it, and it needs no method for its advisory
  brief. The resolver keeps existing inheritance for other registered roles and
  for an omitted role list; the builder treats that omission as malformed. These
  differ intentionally. String role lists are malformed and an empty list denies.
- **Capabilities.** Role tool lists are ceilings. Writes still need explicit
  brief targets and actual host permission.
- **Normal roles.** The four original role files are byte-identical to 2.0.0;
  their registry entries change only by INTERLOCUTOR eligibility.

## Removed evaluator: dependence finding

2.1.0 removes `tools/undertaking_evaluation/`, which had five files in 2.0.0,
and provides no public replacement. `audit-agents` and
`evaluate-repository-change` are absent from 2.1.0 discovery; neither existed
in the 2.0.0 `workflows/` tree or index either. A search of every tracked App
file for `undertaking_evaluation`, `audit-agents`,
`evaluate-repository-change`, `tools/evaluation`, `evaluation-protocol` and
`evaluation-report` found no reference in tools, loop, CI, docs or Work. **No
App consumer depends on the removed evaluator**, so no 2.0.0 or pre-removal
dual source is retained. No private Root replacement or service is selected or assumed. `evaluation-protocol`, `evaluation-report` and
`tools/evaluation/` remain public in the Library; App does not use them.

## Unchanged by this receiving

- Packaged product instructions under `app/src-tauri/resources/instructions/`:
  `roles.json`, the four guidance files, `ROLE_SET_SOURCE_BINDING.json`
  (basis `89acac6a3983c605820496d0d121c73bb2297706`) and `SOURCE_MAP.json`.
- Product code: `role_supply.rs`, `instruction_store.rs`, `child_roles.rs` and
  `ConversationRoles.tsx`. Also the DEL-02-04 prototype `role_supply.py`.
- `reference/migration/shared-inputs.json`, the copied deliverable utility and
  the `workflows/coordinated-knowledge-work/` test input.
- Packaging pins. `AGENTS.md` is only a root marker for the packaging readers
  (`app/packaging/successor/check.py` `source_dependencies`), so its bytes are
  not pinned.

The product therefore keeps its explicit four-role pin. **No full 2.1.0 product
adoption is claimed.** The harness fixture is test source, not live product
role supply. This receiving makes no R24 claim.

## Product boundary: recommendation for a future additive migration

The read-only inspection found these closed four-role assumptions:

| Surface | Current assumption |
|---|---|
| `role_supply.rs` `Role` | Four variants; `ALL: [Role; 4]`; `primary_entry` is `!= TASK`; `child_roles` is hard-coded; `limit()` has TASK as the only non-delegator |
| `RoleSet::parse` | `chirality.app.roles/1`, `deny_unknown_fields`; requires exactly four rows, fixed meanings, `agents/AGENT_<ROLE>.md` and binary delegation |
| Seeded guidance | `Guidance::seeded`/`read_seeded` path allowlist; `instruction_store.rs` expects `Role::ALL.len() + 1` files |
| Request guard | `config` keys `agents.<ROLE>.{description,config_file}` limited to `Role::ALL` |
| `child_roles.rs` | Offers children from `Role::ALL` × `child_roles()` |
| Resources | `roles.json` (four rows), `agents/` (four files), source binding `chirality.app.roles.source-binding/2` at `89acac6a` |
| `ConversationRoles.tsx` | `CONVERSATION_ROLES` contains the three direct-entry roles |
| Prototype | `role_supply.py` `ROLES` 4-tuple and `len(names) == 4` |

Recommended shape, for a separately selected additive product migration under
App Agent 0's design/integration authority and independent review:

1. Add `INTERLOCUTOR` to `Role` and extend `ALL`. Make `primary_entry` false
   for both Type 2 roles. List it as a child of the three direct-entry roles,
   with no children of its own. Use `does-not-delegate` for both Type 2 roles
   in `parse` and `limit()`.
2. Version the closed role set (for example `chirality.app.roles/2`). Keep
   reading `/1` for existing records rather than widening `/1` silently. Make
   the matching additive enum changes in the supply-record schema, API and
   request config allowlist. Extend the seeded path allowlist and the
   `instruction_store` count.
3. Write new product guidance for `agents/AGENT_INTERLOCUTOR.md`. Product
   guidance is App-authored ("no verbatim Root-role adoption"). Re-bind
   `ROLE_SET_SOURCE_BINDING.json` to a new basis that names Library
   `c35b7bbc…` as a source-qualified input, and keep the `89acac6a` binding
   for existing records.
4. Leave `CONVERSATION_ROLES` with three entries, because INTERLOCUTOR is not a
   conversation start. Use a per-session opt-in control for selection. Decide
   how its advisory consultation routes, including what replaces "before every
   PR merge" in a product session, and offer it through the child-role
   surface.
5. Update the DEL-02-04 prototype and tests in the same change. Reconcile the
   DEL-02-04 ScopeOfWork/Work meaning.

## Reserved choices

- **App Agent 0:** select and integrate this operational receiving after the
  independent review/interlocutor route; decide the source-qualified scope,
  timing and implementing design for any later packaged-role migration,
  including App-authored guidance, versioning, opt-in surface and advisory
  routing. This is an implementing recommendation, not a demand for a new
  owner question or a prerequisite for native J1.
- **Owner:** commitment, acceptance, release and other actually reserved
  authority changes remain reserved. No new product commitment is chosen here.
- **Each undertaking's authorized brief:** select any relevant Library method;
  76 indexed holdings do not establish a blanket project method selection.
- **Session steering:** whether a given App session selects INTERLOCUTOR, and
  its model and effort.

## Checks (2026-11-07, uncommitted candidate on base `2b5134f6`)

Python 3.13.14 with existing pytest 9.1.1 and PyYAML 6.0.3, offline. Commands
ran under the slot wrapper with a scratch `CODEX_HOME`/`TMPDIR` and no bytecode.

- `python3 -m pytest -q tools/validation/test_library_v2_1_operational_adoption.py`:
  38 passed. The same run with bytecode enabled (scratch prefix) also passed and
  wrote no bytecode into the fixture.
- A constructed compatibility probe loads the 2.0.0 resolver against the new
  five-role registry and constructed packages: it admits INTERLOCUTOR without a
  companion and accepts a `"TASK"` string as a role list. The 2.1.0 resolver
  refuses both. This distinguishes old consumer code on new inputs; it does
  not claim that the original 2.0.0 registry included INTERLOCUTOR.
- `python3 -m tools.deliverables --project . check`: 41 deliverables, 0 errors.
  `app/examination/repin.py --check`: the pins agree.
- The new harness ran together with `tools/ci/test_selection.py`,
  `tools/deliverables/test_cli.py` and `tools/test_run_recorded_prototype.py`:
  119 passed.
- `git diff --check` found no whitespace errors in changed or new files. The
  repository credential patterns and conflict-marker scan found nothing in the
  20 changed or new files. These ran locally before commit; the base/head forms
  of those validators run in hosted CI.

Not run: the Library suite, index rebuild, App build, Rust/Node tests and native
or model probes. The release archive checksum was not re-derived because no
asset was downloaded.

Manager inspection additionally verified all 11 fixture files byte-for-byte
against the local c35 Git objects and the annotated tag target. The Library's
`LICENSE.md` is byte-identical to App's existing root license (SHA256
`495c4cd17baafde07be4c358bd47237f259bb2e01914e94114efc97d7fa721da`);
its terms cover this retained source fixture. The product-boundary test checks
the existing role-set and every guidance source digest rather than coupling
CI to Rust/JSX formatting. Source inspection of those unchanged runtime
consumers remains distinct from executing their product suites. After that
manager test refinement, the focused harness again passed 38/38 (log
`/tmp/app-lib21-scratch.BpunGI/manager-adoption.log`). The earlier 119-test
repository run remains applicable to the unchanged existing consumers. No build,
native or model qualification is inferred.
