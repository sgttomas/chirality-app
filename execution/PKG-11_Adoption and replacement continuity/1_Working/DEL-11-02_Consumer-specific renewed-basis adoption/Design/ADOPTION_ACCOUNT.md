# Consumer-specific renewed-basis adoption

- **Contribution:** DEL-11-02/AA-v0.1, the first Design file of DEL-11-02. Frozen as part of unit **EU-F3**, together with DEL-11-01 CA-v0.2 and DEL-11-03 RP-v0.5, which consume its status hand-over.
- **Status:** DRAFT DEFINITION — proposed, not accepted. Beside it is the PROPOSED schema `aa.adoption-account.schema.json`. The prototype is under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/aa/` (RUN/F/aa): `build_aa.py`, `check_aa.py`, and the built account `records/AA-1.adoption-account.json` with its status hand-over `records/AA-1.status.json`. Its one instruction-change entry (D-GOV-52) is **real**: every fact cites evidence read from git at commit `122c5abcf516f31ffdb1fdb17d9d5b0f96603154`.
- **Run and owner:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; owner O-F (Type 2, Claude Opus 5.5); 2026-10-04.
- **Serves:** OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; designed cases for VER-001…VER-006 (§7).
- **Rulings (cited by ID):**
  - R23-30 (App v4 adopts D-GOV-52);
  - R23-32: F-R9 (adoption is recorded through the existing tranche-and-notice route, with no new mechanism), F-R10 (a routine adoption is the receiving loop's act; OI-024 covers the staged adoption of the renewed basis), F-R11 (consumers come from DEL-10-03), F-R16 ("notice delivered; receiving decision not recorded"); P-4;
  - R23-44 (vendoring).
- **ScopeOfWork pin (R23-5):** `ScopeOfWork.md` sha256 `2d962646f8b24a1b76fcd30307859f7c7632c25e78864c28b5fd04fb687a057c`. This is the INIT contract; no SCA-V4 block changed it. Its TBD-001 and TBD-002 read OI-017 and OI-018 as open; they are resolved for this run and answered for the App, respectively. The wording is carried to the next amendment (R23-11). SCA-V4-003 ledger row R22-7-open (DEFER) records that DEL-11-02 owes a consumer-side row for DEP-02-04-013; under F-R15 it goes to the next amendment after the reach script.
- **Evidence read** (sha256 now; the account cites each by its git blob at the commit):
  - Root `AGENTS.md` `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` (was `c8ce87ef…`);
  - tranche manifest `ROOT-DGOV52-APPLICATION-20261004.yaml` `559dcf4316d1e0e1e2057c1b9332ed906ec575a988092ee97303c1386ef2d92c`;
  - notices: App v4 `a643415cb3109edf…`; App v3 and Runtime `5f4fb4d995cdf7e8…` (byte-identical);
  - `exports/chirality-app/export-manifest.csv` `8e532540fdea30eb…`;
  - ROLE-v0.2 `c8474d919bceec7d…`;
  - DEL-10-03 RA-v0.2 (vendored at `RUN/F/ca/vendor/`, `811c868cf4689ab5…`, committed `ce64a97a2a`).
- **Labels.** *States* means a file says it; *inference* marks this file's reading; PROPOSED marks a rule introduced here.

## 0. What the account is

For each renewal and each consumer, the account records eight **separately warranted facts**, each with its own evidence:
- prepared notice;
- delivered;
- published;
- resolved;
- supplied;
- provider adopted;
- observed behaviour;
- consumer adopted.

These are REQ-001's and CLM-005's distinctions. **Evidence for one fact never establishes another** (§3).

The account records receiving decisions; it never makes one (REQ-007). It uses the route that already exists:
- Root's instruction tranches, with their `m6_notice` routing;
- the receiving loops' own records;
- the App's own adoption ruling.

It adds no distribution mechanism (F-R9). Its outputs are linked views of those records, not a new register (the ScopeOfWork, below OUT-003).

## 1. Act boundary (REQ-005, REQ-007)

| Act | Who | Here |
|---|---|---|
| Approving a Root instruction change | The owner. This run's OWNER_DECISIONS.md: HELP_HUMAN "brings the owner only acts the governing texts reserve to the person, such as applying an instruction change"; Root `AGENTS.md`: "Instruction changes require their own authorized scope and tranche manifest" | Recorded as human act A-1 for D-GOV-52, faithfully: actor the owner, recorder HELP_HUMAN |
| Adopting a changed instruction in a loop | That receiving loop (F-R10; Root `AGENTS.md`: "each receiving loop decides its adoption") | App v4's adoption is agent act AD-1 (R23-30). For other loops, only what their own records show |
| Staged adoption of the renewed v4 basis; first adopters; retirement | The owner with affected consumers (OI-024; P-4) | Rows carried as *not established*, with that owner and point of need |
| Shared responsibility allocation | DEL-10-03 | X-1 consumed (§2) |
| Changing a Design file to follow an adoption | That file's owner | Traced, not done (§5) |

## 2. Interfaces

| ID | Input or output | Other end | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| I-1 | Consumers and responsibility (X-1: Root, Runtime, App v3, Piping) | DEL-10-03 RA-v0.2 | DEP-11-02-008, admitted | Each account version | Rows from DEP-006, provisional |
| I-2 | Role supply evidence (O-3: "the same evidence, no adoption claim") | DEL-02-04 ROLE-v0.2 | DEP-02-04-013, admitted (supplier's row; R22-7-open) | When a candidate supplies role guidance | `supplied`, `provider_adopted` and `observed_behavior` stay *not established* |
| I-3 | Manual and edition pins | DEL-10-01 | DEP-10-01-020, admitted | Before a row cites a manual edition | None cited |
| I-4 | Change records: Root tranche manifests, notices, loop rulings | Root governance; receiving loops | DEP-006 (external) | Each renewal | The renewal is not traced |
| O-1 | Status hand-over `$defs/adoption_status` | DEL-11-01 | DEP-11-01-010, admitted | Each continuity-account version | DEL-11-01 records *not supplied* |
| O-2 | The same hand-over | DEL-11-03 | DEP-11-02-015, admitted | Each packet version | The packet records *not supplied* |

## 3. Facts and the separation rules (OUT-001; REQ-001, REQ-002, REQ-005)

A fact's state is `established`, `not_established`, `unknown` or `not_applicable`. `established` needs at least one evidence item (schema). The evidence kinds are:
- `file_at_commit` (path and sha256 at the commit, with an optional quote checked against the bytes);
- `git_commit`;
- `manifest_statement` (with its quote checked);
- `act` (an act id in the account);
- `absence_search` (the exact `git grep` and its count);
- `design_file_state`.

**Separation rules (PROPOSED, checked by `check_aa.py` K-6):**
- **SR-1:** `resolved`, `supplied`, `provider_adopted`, `observed_behavior` or `consumer_adopted` is never established by a manifest statement or a commit alone.
- **SR-2:** none of those is established only by the publication evidence.
- **SR-3:** `consumer_adopted` is established only by a recorded act. The schema also requires the `act` evidence kind and an adoption point.
- **SR-4:** an adoption act counts only for the consumer it names (`consumer_id`). App v4's adoption is never another loop's.

`unknown` stays unknown. It is never filled from a manifest's rationale. For example, "Piping and PEC … read Root AGENTS.md live" is the tranche's statement about a supply route, not an observation, and not an adoption.

## 4. The account at `122c5abcf5` (records/AA-1)

**RN-1: D-GOV-52**, an instruction change. Root `AGENTS.md` went from `c8ce87ef…` to `f96feb19…` in tranche `ROOT-DGOV52-APPLICATION-20261004` (commit `7bd2283dbc`). It was approved by human act **A-1**: "I approve A1 and B1, go ahead" (OWNER_DECISIONS_2.md; recorder HELP_HUMAN, as that file's custody line states).

| Consumer | Notice prepared / delivered | Published | Resolved, supplied, provider, behaviour | Consumer adopted |
|---|---|---|---|---|
| App v4 | established / established (notice `a643415c…` in its `_Coordination`) | established (Root bytes at `7bd2283dbc`) | **not established**: no App build or candidate yet | **established**: AD-1, R23-30 "App v4 adopts the changed Root text." Adoption point R23-30. Its Design files follow at their next revision (§5) |
| App v3 | established / established (notice `5f4fb4d9…`) | established | unknown | **not established**: "notice delivered; receiving decision not recorded" (F-R16). `git grep D-GOV-52` finds only the notice; 0 commits touch the lane after the tranche. The notice's "This loop: … No adoption work is expected" was written by the sending tranche, not by the loop |
| Runtime | established / established (byte-identical to App v3's) | established | unknown | **not established**, as for App v3. The shared text speaks of "the v3 idle-boundary path and RB-SETTINGS" (F-R16) |
| Piping | not applicable / not applicable: no notice routed; the manifest's rationale is quoted | established | unknown (the "reads live" statement is not observed) | **not established**: no record; 3 commits touch the lane after the tranche, and none mentions D-GOV-52 |
| PEC | not applicable / not applicable | established | unknown | **not established**; PEC is not a DEP-006 consumer |

**RN-2: the renewed App v4 basis** (APP-V4-BASIS-20260926), in staged adoption by the DEP-006 consumers Root, Runtime, App v3 and Piping. For each:
- `published`: established. The basis is in this repository, and publication is not adoption (V4-OPS-14).
- No notice has been prepared.
- `consumer_adopted`: not established; `git grep` of the basis id finds nothing in any of the four lanes.
- `open`: "Owner with affected consumers (OI-024)", "Before each adoption/retirement decision". First adopters are the owner's decision (P-4).

**Packaging and tool paths (OUT-002; REQ-003):**
- The public export manifest pins Root `AGENTS.md`. It was regenerated in the tranche, and its row reads `AGENTS.md,14481,f96feb19…`: established.
- The export's staging tree "is written outside the repository and is not committed", and no publication act is recorded: not established.

**Currency (REQ-003; SOW-257).** No consumer in this account relies on the pinned research (`e548d4c…`) as a current implementation map, so the later-mainline comparison is not run. REQ-003 requires it before such reliance, which is when a row would cite it.

## 5. Promise trace (OUT-003; REQ-004)

DEL-10-03's S-3 entry (guidance supply) names D-GOV-52. Ruling R23-30 says the affected App v4 Design files are "updated at its next revision":

| Derivative | Owner | Change state at `122c5abcf5` | Evidence |
|---|---|---|---|
| ROLE-v0.2 F-R9 (DEL-02-04) | DEL-02-04 owner | **pending next revision** | ROLE_SUPPLY.md does not mention D-GOV-52 or R23-30 |
| HOSTING-v0.9 §2/§8.2 (DEL-01-01) | DEL-01-01 owner | **pending next revision** | Same check |
| ACCESS-v0.2 §9/U-A9 (DEL-01-05) | DEL-01-05 owner | **pending next revision** | Same check |

The states are `proposed`, `pending_next_revision`, `applied`, `checked` and `not_affected`. A prepared handoff, an accepted change, an applied change and a performed check each need their own evidence (REQ-004). `check_aa.py` K-10 recomputes each state from the Design file at the commit.

## 6. Status hand-over (O-1, O-2) and sequence

`records/AA-1.status.json` (`$defs/adoption_status`) carries:
- for the renewed basis, no consumer adopted; four not recorded; owner and point of need from OI-024;
- for RN-1, adopted by App v4; not recorded by App v3 or Runtime; no notice to Piping or PEC;
- one plain statement.

DEL-11-01's CA-v0.2 records it as `supplied`, and DEL-11-03's RP-v0.5 carries it as S-6.

**Sequence.**
1. A renewal is recorded when its change record exists (a tranche manifest, or an owner act for the basis).
2. Each consumer's facts are read from git at a commit (`build_aa.py --at <commit>`).
3. The account is checked (`check_aa.py`) and its status handed over.
4. A consumer's later record (an adoption ruling, a declined adoption, a Design revision) makes a new account version. Earlier versions stay as history.

## 7. Verification (designed; `check_aa.py` 19/19 at freeze)

| VER | Case | Held by |
|---|---|---|
| VER-001 | Coverage of consumers and scopes against X-1 and DEP-006; App-only acceptance never supplies another consumer | K-7, K-8, N-3 |
| VER-002 | Notice without adoption (App v3, Runtime); publication without supply (App v4); App v4's adoption without any other loop's; a human approval faithfully recorded (A-1) and an agent adoption (AD-1); fabricated decisions refused | K-4, K-5, K-6, N-1, N-2, N-3, N-4, N-5, N-8 |
| VER-003 | Instruction identity: Root bytes before and after, at the commit; history preserved (the old bytes remain in git) | K-3, K-4 |
| VER-004 | Packaging (export manifest) and currency (no reliance, so no comparison) | K-4; §4 |
| VER-005 | Promise to derivative to state, recomputed | K-10 |
| VER-006 | Open owners and points of need kept; no invented mechanism or allocation | K-1 (schema `open`), K-9, N-7 |

K-5's actor-not-recorder test is a string comparison. It cannot tell whether a named recorder is true, so `recorder_stated_by_record` says whether the record itself names the recorder.

## 8. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| AF-1 | A notice listed in a manifest is missing in the receiving lane | `delivered` not established; K-8 fails | Report to the tranche's integrator |
| AF-2 | A loop's record mentions the change but its decision is unclear | `consumer_adopted` *unknown*, with the search result | Ask that loop's owner; never infer |
| AF-3 | DEL-10-03's consumer list changes | V-1 NOTICE in `check_ca.py` (shared vendor) | Re-pin deliberately (R23-21) |
| AF-4 | A Design file named in the trace is revised | K-10 recomputes `applied`; `checked` needs its own evidence | — |

## 9. Open matters

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-AA-1 | App v3's and Runtime's receiving decisions on D-GOV-52 | Those loops' owners | Their own |
| U-AA-2 | First adopters of the renewed v4 basis; end of coexistence | Owner with affected consumers (OI-024; P-4) | Before each adoption/retirement decision |
| U-AA-3 | The consumer-side register row for DEP-02-04-013 (R22-7-open) | Next amendment, after the reach script (F-R15) | — |
| U-AA-4 | Supply, provider adoption and behaviour for App v4 | DEL-02-04, DEL-01-01 (ROLE O-3; HOSTING §8.2) | When a candidate supplies guidance |

## 10. Changes

| Version | Change |
|---|---|
| AA-v0.1 (2026-10-04) | First Design file; unit EU-F3 with CA-v0.2 and RP-v0.5 |
