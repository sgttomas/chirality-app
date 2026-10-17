# SWBPIPE operation corpus received in App terms

- Contribution: DEL-03-02/SWB-CORPUS-v0.1, with DEL-03-01's SH-1 profile `swbpipe`
  (C-v0.8 §10.8). Status: PROPOSED mapping and test double. Evidence labels:
  *illustrative* (the corpus mapping) and *test-double* (the profile). No SWBPIPE
  run, App run or person act is observed, and nothing here is a SWBPIPE commitment
  (DECISION-3).
- Source basis: SWBPIPE files read only, at repository commit
  `8212c765ec0bcc812ad4c4f7079bc661b55d70ab` (2026-10-17). Every file read is
  byte-pinned in `swbpipe-corpus-pins.json` beside this file: the 84 cases and
  README of `projects/chirality-piping/fixtures/model_operations/contract_corpus/`,
  the operation engine (`core/model_operations/operation_applier/src/lib.rs`,
  `atomic_batch.rs`, `bend_authoring.rs`), the canonical hash
  (`core/serialization/canonical_json/src/lib.rs`, `fixtures/canonical_hash/cases.json`),
  the desktop Apply, receipt and intake sources, and the DEL-16-03 audit-trail
  constructor. `prototype/swbpipe_corpus_map.py` refuses to run on drifted bytes.
- Contracts applied: this deliverable's P-v0.8 (§2, §3.5, §4.1–§4.3, §5, §9,
  §9.1, §10) and DEL-03-01's C-v0.8 (§4.1, §5.1–§5.4), under ScopeOfWork REQ-002,
  REQ-004, REQ-010, REQ-011 and REQ-012.
- Outputs: `swbpipe-corpus-mapping.json` (one row per case), this account, the
  profile (`../../DEL-03-01/Design/prototype/simhost_swbpipe.py`, driver
  `run_swbpipe_profile.py`, documents `swbpipe-profile-documents.json`), and the
  App receiving tests `app/src-tauri/tests/swbpipe_receiving.rs`.

## 1. What was mapped, and the rules used

Each corpus case is one call of SWBPIPE's operation engine (`apply` or
`validate_only`) on one change, with the outcome the engine is held to. The
mapping asks what that outcome would mean in App contract terms if it reached
an App receiver (an embedded loop under DEL-05-01, the panel under DEL-05-02,
or the external adapter under DEL-03-03). On SWBPIPE's main branch no agent
route carries it there today (NR-09).

Three rules govern every row:

1. **Nothing gains stronger standing than the source gives it.** SWBPIPE's
   Apply records `acceptance_basis: "user_initiated_apply_in_local_session"`
   and nothing else about the act. It is never received as an A5, never as a
   per-change act, and never as a named person's act. A receipt is not an
   acceptance. A host refusal is *refused*, never A10 (P REQ-004).
2. **The App computes no host identity** (C §5.3, §5.5). What SWBPIPE does
   not supply stays *not supplied*. The evaluated basis of every row copies the
   host's whole-model hash and marks the model revision *omitted*; workspace
   identity and generation are *host declares none*, because SWBPIPE stated it
   has none on main (SQ-07 (a)).
3. **A host term is received as the host states it** (P §9.1). The App's own
   reading is added beside it, never in its place.

## 2. Result

| Host outcome | Cases | Contract outcome | App record formable now |
|---|---|---|---|
| `apply`, `applied_to_session_model` | 34 | **none** (§3 NR-01, NR-05; §4 A-01) | no |
| `apply`, `blocked`, a stale code (`OP-STALE-BEFORE-VALUE` ×2, `OP-CLAIMED-MODEL-HASH-MISMATCH` ×1) | 3 | *refused — stale*, item-left cause `refused_stale` | no |
| `apply`, `blocked`, any other code | 45 | *refused — invalid* with the host's code, item-left cause `refused_invalid` | no |
| `validate_only`, passed (case 14) | 1 | *success* of a non-mutating host check (the DEL-16-02 preview): old and new values; nothing queued, applied or accepted | no |
| `validate_only`, blocked (case 38, incomplete intent) | 1 | C §4.1 *error* of that check | no |

Notes on particular rows:

- The before-value stale refusals name their target (`failing_targets`), and
  the scope is recorded as SWBPIPE's per-field before-value check. The claimed-hash
  mismatch is scope *whole model*, failing targets not supplied (P §5; R8-3).
- `OP-CLAIMED-MODEL-HASH-METADATA-INVALID` and `-UNSUPPORTED` (cases 80, 81) are
  *refused — invalid*: a malformed or other-method basis claim is incomparable
  (C §5.2 rule 6), never stale.
- `OP-DIRECT-MUTATION-BLOCKED` (case 35) is the host refusing a request to
  bypass its one route; it supports P S-P1.
- Case 84 (`OP-BEND-FLEXIBILITY-USER-ENTRY-REQUIRED`, an agent-authored bend
  flexibility factor) is received as the host states it, *refused — invalid*.
  It is an authority difference, which P §2 reports as *not permitted* naming
  the governing treatment; SWBPIPE supplies no treatment to name (NR-11).
- Deletions (12 applied cases) have no App resulting-object relation (A-02).
- Author identity is *unverified* on every row: `author_type` is supplied by
  the caller (SQ-14; the batch route records
  `source_identity_verification: "not_performed_asserted_metadata_only"`).

No case lands on *accepted*, *rejected*, *withdrawn* or *applied*, and no row
carries a decision. `swbpipe_corpus_map.py` checks this, and so do the App
receiving tests.

## 3. What SWBPIPE would need to add (for the piping project)

Each item names what the App contract needs, what SWBPIPE has at the pinned
commit, and the cases or route it affects. Paths are under
`projects/chirality-piping/`; line numbers are at the pinned commit.

| Id | The App needs | SWBPIPE at the pinned commit | Affects |
|---|---|---|---|
| **NR-01** | An acceptance record per change: who accepted (the person's identity), an act reference, the capture time, a capture-evidence reference, bound to that change's content identity (P §3.1 rules 1–2, §10) | The Apply outcome carries one record per call or per batch: `acceptance_basis: user_initiated_apply_in_local_session`, `acceptance_is_professional_approval: false`, `persistence_status: session_state_only_not_yet_saved`. There is no actor, act reference or time (`operation_applier/src/lib.rs:2222-2227`; `atomic_batch.rs:194-198`; `apps/desktop/src/types.ts:1109-1113`) | All 34 applied cases; every per-batch Apply |
| **NR-02** | A rejection record (A10) per change, by the person | There is no rejection on the Apply route: "Clear pending changes and batches" discards queued batches with no record (`apps/desktop/src/features/toolkit/BatchReviewPanel.tsx:37`). The DEL-16-03 constructor that writes accepted, rejected and held records with actor fields (`core/model_operations/audit_trail/engine.py:137-236`) is called only by tests, not by Apply | V4-EXM-20's rejection |
| **NR-03** | A decision per change within one submission (row-by-row accept and reject) | Agent proposals arrive as batches, which are validated and applied atomically, all or nothing (`atomic_batch.rs:1-16`, `:184`; offline intake applies `frozenSubmission.batch` at `apps/desktop/src/features/workspace/workspaceSession.ts:1305-1306`). Per-intent Apply exists only for the person's own editor intents (`apps/desktop/src/features/operations/OperationApplyPanel.tsx`) | V4-EXM-20's row-by-row acceptance |
| **NR-04** | A change-item content identity, assigned by the host when it first receives the change, with its method designation (P §3.5 PM-6) | Only caller-supplied `operation_id` and `change_id`, plus `batch_hash` for a batch (`atomic_batch.rs:188`) | Every case: without it no item state can be recorded |
| **NR-05** | A receipt reference on the application outcome, readable by the proposer, durable or with its durability stated | The engine outcome has none. The desktop mints `receipt_id: applied-<review>` in UI session state (`workspaceSession.ts:1329-1330`). It is reset on project create or open (`:1945-1948`, `:2015-2018`) and readable by no agent | All 34 applied cases |
| **NR-06** | A complete basis on outcomes: a model revision (C §5.2 rule 1). Without one, a basis is *basis incomplete* | Outcomes carry only the whole-model hash (sha256 over RFC 8785 canonical JSON of the model payload; `operation_applier/src/lib.rs:44`). The desktop keeps a revision counter in session (SQ-07 (c)), but no outcome carries it | Every case |
| **NR-07** | The relied-on basis carried through to the outcome (P §3.2) | 77 of 84 cases carry no claimed hash. Their binding is `no_claimed_hash_before_state_check_is_the_staleness_guard` (`lib.rs:7999`). Batches do require one (`OP-BATCH-MODEL-HASH-REQUIRED`, `atomic_batch.rs:90`) | 77 cases |
| **NR-08** | A proposal record under the proposer's identity: de-duplication before the basis check, a submission count, a time, and observation by identity (P §3.5 PM-3–PM-5, §5) | None on main. Each queue action is a new session entry. PR #885's `status` by ticket was closed unmerged on 2026-10-09. A retry after an unobserved Apply is therefore refused stale by its own effect, and an unknown outcome cannot be resolved | Every case; the profile shows both (SW-P6, SW-P7) |
| **NR-09** | A route that carries agent-originated proposals and their outcomes | On main, proposals arrive only as JSON files in the offline intake: "Author attribution is supplied by the file and is not verified identity. This workflow has no connected agent provider." (`apps/desktop/src/features/offline-proposal-intake/OfflineProposalIntakePanel.tsx:26`). The agent strip reads "Agent: not available yet" (`apps/desktop/src/features/workspace/shellLayout.ts:147`) | Every case |
| **NR-10** | A capability catalog: operation identity and version, declared errors and preconditions, class, exposure per surface, catalog edition (C §2–§3) | 27 change kinds under one engine version `0.1.0` (`lib.rs:39`); diagnostic codes are stable but not declared per operation | Every case |
| **NR-11** | Authority rules stated as treatments, held on a verified actor: an agent asking for something only the person may do is *not permitted*, naming the rule (P §2) | Rule O5 ("an agent never writes" the bend flexibility factor k) is a blocking validation diagnostic keyed on caller-asserted `author_type` (`lib.rs:1356-1369`), so an agent that asserts `user` is not distinguished | Case 84; any later actor rule |

Not blockers. The App records these as evidence limits and can receive them:

- **Whole-model identity only** (SQ-03). It is received as the identity of every
  subject (R8-4). Any change then stales every item and lapses every act;
  the App errs toward reporting a lapse, never misses one.
- **Resulting objects without identities.** Received as *not supplied*.
- **No workspace identity or generation** (SQ-07 (a)). Received as *host declares
  none*, with the limit "basis lineage not supplied". Comparisons across reads
  then read *unknown (incomparable)*, never *same* or *changed*.

## 4. App-side gaps (not for the piping project)

| Id | Gap | Consequence |
|---|---|---|
| **A-01** | P's *applied* state requires branch `after_acceptance` with a supplied A5, or `direct_under_grant`. Neither fits an application made at a person-initiated host Apply that records no attributable act. The App receiver (`app/src-tauri/src/proposal.rs`, `validate_host_state`) refuses the first without an A5. The second would claim a grant SWBPIPE does not have | A choice for the App coordinator: (i) keep such an application unrepresentable until SWBPIPE supplies NR-01; or (ii) add a weaker App form, "applied at the host's Apply; no attributable act recorded". Option (ii) changes an interface received by DEL-04-03 (record format), DEL-02-01 and DEL-02-03 (checkpoint mapping), DEL-05-01, DEL-05-02 and DEL-03-03. Until one of the two is done, an App record cannot show the person's acceptance of a SWBPIPE change |
| **A-02** | `resulting_object.relation` has no *removed* | 12 deletion cases cannot list the removed object |
| **A-03** | No element states that an application is to session state only, not yet saved | Recorded today only as a known limitation |

The profile also shows a smaller App gap. An observation answered *not exposed*
by a host that offers none is held by App custody as an invalid host claim. The
outcome correctly stays *unknown*, but custody has no record kind for "host
offers no observation".

## 5. SH-1 profile `swbpipe`

`simhost_swbpipe.py` extends SH-1 without changing it; the SH-1 files pinned by
DEL-09-06's W14 record and DEL-09-09's XT record keep their bytes. The profile
has:

- a whole-model identity standing for every subject, and no workspace identity
  or generation;
- whole-model staleness;
- atomic validation of a submission;
- no direct mode;
- no observation by identity;
- no de-duplication;
- no enablement facility;
- SWBPIPE's person controls: **apply** (one atomic application, one commit; only
  the host-stated acceptance basis and a session receipt, both in the double's
  own state), **clear** (no record) and **restart** (session records lost).

It supplies the change-item content identity and the model revision, which
SWBPIPE does not (NR-04, NR-06). Those are the double's, not SWBPIPE's.

`run_swbpipe_profile.py` appends a run to an SH-1 run directory, over both native
paths. Its 16 checks cover:

- discovery and reads on whole-model identities;
- a queued submission with no act;
- *not exposed* for observation and for direct requests;
- the person's Apply, which leaves no per-item act and nothing an agent can read;
- every subject identity changing after Apply;
- the whole-model stale refusal;
- the atomic invalid refusal;
- a lost answer staying unknown;
- Clear leaving no record;
- a resubmission refused stale by its own effect, which is why NR-08 matters.

Its documents are committed as `../../DEL-03-01/Design/swbpipe-profile-documents.json`
and received by the App tests.

## 6. Bearing on the replacement witness

V4-EXM-20 and DEL-11-03 AC-002 expect the person to accept proposed changes
row by row, with one rejection, recorded as the person's acts. In SWBPIPE that
needs NR-01, NR-02 and NR-03, on a route that exists (NR-09). Then either the
App records the acceptance from those host records, or the owner rules on A-01.
On the evidence here, no SWBPIPE outcome at the pinned commit can be recorded
as the person's acceptance.

## Verification

From `projects/chirality-app-v4/execution/PKG-03/`:

```sh
python3 -B DEL-03-02/Design/prototype/swbpipe_corpus_map.py
D=$(mktemp -d)/run
python3 -B DEL-03-01/Design/prototype/run_fixture.py --out "$D"
python3 -B DEL-03-01/Design/prototype/run_swbpipe_profile.py --out "$D"
python3 -B DEL-03-01/Design/prototype/validate_all.py --run "$D"
python3 -B DEL-03-03/Design/prototype/observe_map.py --run "$D"
python3 -B DEL-03-02/Design/prototype/proposal_states.py --check "$D"
```

From `projects/chirality-app-v4/app/src-tauri/`, with the offline route of
`app/README.md`: `cargo test --offline --locked --test swbpipe_receiving`.
