# SCA-V4-001 checkpoint group 1 — accepted proposed change and impact

Recorded 2026-09-28 by node AK1, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the HELP_HUMAN integrator of run
`APP-V4-BASIS-ALIGN-20260928`, which presented checkpoint A (K1) to the owner
under a recorded WORKING_ITEMS consultation. This record transcribes the
owner's act as it is recorded in the run's `OWNER_DECISIONS.md`. It is not a
new request for the same decision, and it claims no inspection the owner did
not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`, section "Checkpoint A: acceptance (owner, exact, 2026-09-28), DECISION-7" |
| Record sha256 at transcription | `cdc486801ae6315a8249459c3fd98cdc2d42390a178f5555b15c9fbee93d6d34` |
| Commit that added DECISION-7 | `f4ba34c2ca80550fed012840e470dcbf5f2fedc3` ("docs(app-v4): checkpoint A accepted (SCA-V4-001 groups 1-2), DECISION-7", 2026-09-28 21:48:01 -0600; it changes only that file) |
| Channel | The owner's reply in chat to the coordinating session, which recorded it verbatim in the record above. AK1 did not observe the chat; it relies on that record |
| Earlier partial answers | DECISION-6 (same record, "Checkpoint A: owner answers"). On the wording package the owner then answered "I want to review the packet first"; DECISION-6 accepted neither group (OWNER_ITEMS O-24 note) |

## What the owner had in front of them

As recorded in `OWNER_DECISIONS.md` (DECISION-7 "Context"): the owner
reviewed the amendment packet **revision 2** on the review page
https://claude.ai/artifact/3ek3uuPUR1v9jgpTjoF6ec. The record gives the
packet hashes by prefix; each matches the committed packet file in full:

| Packet file | Recorded prefix | Full sha256 |
|---|---|---|
| `AMENDMENT_PACKET/OWNER_ITEMS.md` | `2b90eb4a…` | `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef` |
| `AMENDMENT_PACKET/BASIS_AMENDMENT.md` | `04bdc916…` | `04bdc91622223510870ac8fe3994d708641c5e07a7853c5abc75ac59c0ed24cf` |
| `AMENDMENT_PACKET/SOW_REVISIONS.md` | `9b4d700d…` | `9b4d700ddc9d63d48135f84163f03eb8f1da99951ef813a84d17192515e7d27b` |
| `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` | `7fd523c2…` | `7fd523c26eb16a2d5bdf511c335c10403d7d7b2eb320601d72a5c0854e46348e` |

The record states that the page said: "To accept everything still open,
reply in chat: accept the remaining items as recommended". The page itself is
not a repository file; AK1 has not read it.

For group 1 the subject is the proposed change and its impact:
OWNER_ITEMS §A items O-1 and O-2 and the scope items O-8…O-19 and O-25/O-26,
with IMPACT_ASSESSMENT §§1–8 and 10–12 and the pre-change baseline (O-20,
`BASELINE/coverage_summary.json`, sha256
`d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9`).

## The owner's act (verbatim)

> "accept the remaining items as recommended"

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

The reply is the quick-answer form of OWNER_ITEMS revision 2 ("Declining an
item drops only the edits named against it"). DECISION-7 "Effects" records
its coverage as O-1 through O-15, O-17 through O-19 and O-21 through O-26;
O-16, O-20 and O-27…O-30 were already decided or done (DECISION-6). For
checkpoint group 1 it accepts:

| Item | Effect |
|---|---|
| O-1 | Amendment ID `SCA-V4-001`; `FIRST_AMENDMENT` posture (no `_LATEST.md` until group 3) |
| O-2 | The scope of the change: basis wording A01–A17; decomposition rows A18–A31 (ScopeLedger SOW-015, -016, -017, -052, -137, -138, -201, -202; "Declared checkpoint"; DEL-02-03/05-01/09-07 descriptions; the new `## Decision Log` section with the amendment entry, D-15; the corrected no-production sentence, D-16; the coverage recompute); 16 SoW revisions A32–A47. All actions `MODIFY`; no ID, mapping or count change |
| O-8 | "Local-first" amended in the PRD §1.1 purpose statement (A06) and PKG-05 (D-13), with the `_CONTEXT.md` mirrors |
| O-9 | The four C1 scope additions and protected criteria adopted: S-01-4, S-01-5, S-02-3, S-03-2 |
| O-10 | The "record and show the model destination" reading for App runs confirmed |
| O-11, O-12, O-13 | Direct consumption: DEL-04-02 consumed and received directly; PANEL consumes DEL-02-03 directly; GUIDE consumes HOSTING, RELAY and XT (S-04-6) |
| O-14, O-15 | DECISION-5 SoW allocation: host-agent destinations in the DEL-04-03 run-record SoW; the one DEL-04-02 sentence E-0402-08, no other SoW change |
| O-17 | OI-001/OI-002 pointers included; status stays OPEN |
| O-18, O-19 | DEL-08-01 (CLM-003) and DEL-09-07 included |
| O-25 | The R8-11 reading of DECISION-1 D2 "or a declared checkpoint" confirmed |
| O-26 | PRD V4-AUT-03/04 and OQ-02 "open detail" left for a later update |

The accepted intake is `Intake_Actions.csv` (47 rows, all `PROPOSED`), the
impact assessment is `Impact_Assessment.md`, and the pre-change baseline is
`Pre_Change_Coverage.json`, all bound in `ACCEPTED_MANIFEST.csv`. Those three
are transcriptions made after the act (the owner reviewed the packet files,
which are also bound).

## What this acceptance authorizes and does not authorize

It authorizes group-2 preparation from this snapshot. Because the same act
also accepted group 2 (see `../SCA-V4-001_GROUP-2_2026-09-28/`), no separate
group-2 preparation step follows.

On its own it applies no change to the docs, the decomposition package, any
`_CONTEXT.md`, `ScopeOfWork.md`, `_STATUS.md`, `Dependencies.csv`,
`_DEPENDENCIES.md` or `_DAG` file, and it creates no `_LATEST.md`.

## Basis

At the act (commit `f4ba34c2c`): the accepted decomposition
`_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` (via
`_LATEST_ACCEPTED.md`), with the working package inputs hashed in
`../../SCA-V4-001_2026-09-28_2155/Brief.md`; `execution/_ScopeChange/`
absent.
