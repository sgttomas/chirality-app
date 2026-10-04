# Consumer-specific renewed-basis adoption

- **Contribution:** DEL-11-02/AA-v0.3, amended in place for RV3's AA3-R1 (unit **EU-F3R3**, the last tranche-2 round): SR-3 refuses an adoption act whose record is a notice the change routes. Checker and Design only; AA-1 v2 is unchanged, so the version label stays (AA-v0.3 as frozen in EU-F3R2: sha256 `c17c5d8ceed3d32a39f44d460b7321e0a4641fd4ac5641679e595a968fc37f4a`, commit `821f236649`). AA-v0.3 binds delivery and adoption evidence to the renewal (RV3 AA2-R1, in the addendum to RV3-AA1.md; unit **EU-F3R2**). The built account AA-1 v2 and its record format AA-v0.2 are unchanged, so DEL-11-01's and DEL-11-03's built content is unchanged. AA-v0.2 (sha256 `3d4ba2ec9fbd614a1e36c897aca45b7f4ed33cb859cb506f6af833d4639edba3`, unit EU-F3R, commit `0e0036b685`, READY) stays in git as history. AA-v0.2 was the repair of AA-v0.1 for RV3's review RV3-AA1 (AA1-R1 MAJOR; AA1-R2, AA1-R3 MINOR; notes N1–N3). Frozen as unit **EU-F3R**, together with DEL-11-01 CA-v0.3 and DEL-11-03 RP-v0.6, which consume its status hand-over. AA-v0.1 (unit EU-F3, commit `b2fbfdbac8`) stays in git as history.
- **Status:** DRAFT DEFINITION — proposed, not accepted. Beside it is the PROPOSED schema `aa.adoption-account.schema.json`. The prototype is under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/aa/` (RUN/F/aa): `build_aa.py`, `check_aa.py`, and the built account `records/AA-1.adoption-account.json` with its status hand-over `records/AA-1.status.json`. Its one instruction-change entry (D-GOV-52) is **real**: every fact cites evidence read from git at commit `122c5abcf516f31ffdb1fdb17d9d5b0f96603154` (unchanged from AA-v0.1; the repair changes the rules, the act fields, the Root search and the status wording, not the commit read).
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
| Approving a Root instruction change | The owner. This run's OWNER_DECISIONS.md: HELP_HUMAN "brings the owner only acts the governing texts reserve to the person, such as applying an instruction change"; Root `AGENTS.md`: "Instruction changes require their own authorized scope and tranche manifest" | Recorded as human act A-1 for D-GOV-52 (`act_class` change_approval), by faithful recording: actor the owner, recorder HELP_HUMAN |
| Adopting a changed instruction in a loop | That receiving loop (F-R10; Root `AGENTS.md`: "each receiving loop decides its adoption") | App v4's adoption is agent act AD-1 (R23-30; `act_class` adoption), by **direct capture**: HELP_HUMAN, App v4's integrator, recorded its own ruling, so actor and recorder are the same agent (RV3 N1). For other loops, only what their own records show |
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
- `design_file_state`;
- `candidate_record` and `observation_record` (PROPOSED in AA-v0.2): a record of a built candidate or of observed behaviour. None exists yet; the kinds are reserved so that the candidate-side facts have an evidence kind of their own.

**Acts.** Each act carries `act_class` (`adoption`, `change_approval` or `other`) and `recording_mode` (`direct capture`: the actor recorded it; `faithful recording`: someone else recorded it from the actor's words). A-1 is a change approval, faithfully recorded; AD-1 is an adoption, directly captured.

**Evidence each fact accepts (PROPOSED; schema `$defs` per fact and `check_aa.py` SR-1).** Evidence for one fact never establishes another. When a fact is `established`, every evidence item must be of a kind its row allows:

| Fact | Evidence kinds accepted when established |
|---|---|
| `prepared_notice` | `manifest_statement` (the tranche manifest's routing) |
| `delivered` | `file_at_commit`, the notice file **inside the receiving lane** (SR-2) |
| `published` | `file_at_commit` (the change bytes), `git_commit` |
| `resolved`, `supplied`, `provider_adopted`, `observed_behavior` | `candidate_record`, `observation_record` only: never a notice, a manifest statement, a commit, publication bytes or an absence search |
| `consumer_adopted` | `act` (required, SR-3), and optionally `file_at_commit` naming that act's own record |

`absence_search` and `design_file_state` never establish a fact; they support `not_established` and `unknown`.

**Separation rules (PROPOSED, checked by `check_aa.py` K-6; each with negative cases, §7):**
- **SR-1:** an established fact's evidence is only of the kinds its row above accepts.
- **SR-2:** `delivered` is shown only by a file inside the receiving consumer's lane **that the renewal's own change record routes** (the notice paths listed in its tranche manifest; AA-v0.3, AA2-R1). A routing statement, a file in another lane, or any other in-lane file (for example the lane's README) is not delivery. A renewal with no change record (RN-2) routes nothing, so its `delivered` cannot be established.
- **SR-3:** `consumer_adopted` rests only on an adoption act of that consumer's own loop: the cited act is an `agent_act` (never a person's `human_act`, F-R10), its `act_class` is `adoption`, its `consumer_id` is the row's consumer, and its record lies inside that consumer's lane. A file cited beside it must be that act's record. **The act's record entry must name the renewal** (AA-v0.3, AA2-R1): the entry is the text from the last heading or top-level bold item (`- **…`) before the act's exact text, and it must contain one of the renewal's names (the identifiers in its `what`, such as D-GOV-52, or its change record's file stem, such as ROOT-DGOV52-APPLICATION-20261004). AD-1's entry is R23-30's head, "R23-30 Adopting D-GOV-52 in App v4". **The act's record is never a notice the renewal's change routes** (AA3-R1): the sending tranche's text is never the receiving loop's act (F-R10). App v4's adoption is never another loop's, and the owner's approval of a change is never any loop's adoption. The schema also requires the `act` evidence kind and an adoption point.
- **SR-4:** the act's exact text states an adoption: it contains "adopt", "adopts", "adopted" or "adoption", and no negation ("not", "no", "never", "without"). A status statement such as F-R16's "notice delivered; receiving decision not recorded" is not an adoption. This test is **keyword-based**: it cannot read meaning, so a text such as "App v3 adopts nothing" would pass it (§7, not enforced).

`unknown` stays unknown. It is never filled from a manifest's rationale. For example, "Piping and PEC … read Root AGENTS.md live" is the tranche's statement about a supply route, not an observation, and not an adoption.

## 4. The account at `122c5abcf5` (records/AA-1)

**RN-1: D-GOV-52**, an instruction change. Root `AGENTS.md` went from `c8ce87ef…` to `f96feb19…` in tranche `ROOT-DGOV52-APPLICATION-20261004` (commit `7bd2283dbc`). It was approved by human act **A-1**: "I approve A1 and B1, go ahead" (OWNER_DECISIONS_2.md; recorder HELP_HUMAN, as that file's custody line states).

| Consumer | Notice prepared / delivered | Published | Resolved, supplied, provider, behaviour | Consumer adopted |
|---|---|---|---|---|
| App v4 | established / established (notice `a643415c…` in its `_Coordination`) | established (Root bytes at `7bd2283dbc`) | **not established**: no App build or candidate yet | **established**: AD-1, R23-30 "App v4 adopts the changed Root text." Adoption point R23-30. Its Design files follow at their next revision (§5) |
| App v3 | established / established (notice `5f4fb4d9…` in its `_Coordination`; delivered, not shown read) | established | unknown | **not established**: "notice delivered; receiving decision not recorded" (F-R16). `git grep D-GOV-52` finds only the notice; 0 commits touch the lane after the tranche. The notice's "This loop: … No adoption work is expected" was written by the sending tranche, not by the loop |
| Runtime | established / established (byte-identical to App v3's) | established | unknown | **not established**, as for App v3. The shared text speaks of "the v3 idle-boundary path and RB-SETTINGS" (F-R16) |
| Piping | not applicable / not applicable: no notice routed; the manifest's rationale is quoted | established | unknown (the "reads live" statement is not observed) | **not established**: no record; 3 commits touch the lane after the tranche, and none mentions D-GOV-52 |
| PEC | not applicable / not applicable | established | unknown | **not established**; PEC is not a DEP-006 consumer |

**RN-2: the renewed App v4 basis** (APP-V4-BASIS-20260926), in staged adoption by the DEP-006 consumers Root, Runtime, App v3 and Piping. For each:
- `published`: established. The basis is in this repository, and publication is not adoption (V4-OPS-14).
- No notice has been prepared.
- `consumer_adopted`: not established; `git grep -F 'APP-V4-BASIS-20260926'` at the commit finds nothing in any of the four lanes. For Runtime, App v3 and Piping the search covers their project folder. For Root it covers the whole repository outside `projects/chirality-app-v4` (Root's `AGENTS.md`, `docs/`, `workflows/` and every other lane), widened in AA-v0.2 from `AGENTS.md` alone (AA1-R3). RV3 ran the same whole-repository search independently and found nothing; the record cites it as a second search, attributed to RV3.
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
- for RN-1, adopted by App v4; a notice delivered to App v3's and Runtime's coordination folders, with no receiving decision recorded; no notice to Piping or PEC;
- one plain statement: "No consumer has adopted the renewed App v4 basis; first adopters are the owner's decision with affected consumers (OI-024). Of the one instruction change traced (D-GOV-52), App v4 adopted it; a notice was delivered to App v3's and Runtime's coordination folders, and no receiving decision is recorded (whether either loop read it is not shown); no notice was routed to Piping or PEC, by design."

AA-v0.1's statement said App v3 and Runtime "received a notice". The evidence shows a file in their folders, which is delivery, not receipt (AA1-R2; F-R16's wording). The correction is carried into DEL-11-01 CA-v0.3 and DEL-11-03 RP-v0.6 S-6.

DEL-11-01's CA-v0.3 records it as `supplied`, and DEL-11-03's RP-v0.6 carries it as S-6.

**Sequence.**
1. A renewal is recorded when its change record exists (a tranche manifest, or an owner act for the basis).
2. Each consumer's facts are read from git at a commit (`build_aa.py --at <commit>`).
3. The account is checked (`check_aa.py`) and its status handed over.
4. A consumer's later record (an adoption ruling, a declined adoption, a Design revision) makes a new account version. Earlier versions stay as history.

## 7. Verification (designed; `check_aa.py` 47/47 at freeze)

`check_aa.py` computes every rule this file claims as a function of the account (`rule_errors`). Each negative case N-1…N-32 breaks the **real** account in memory and runs those same functions, naming the rule that must refuse it; a negative never re-derives its rule. P-1…P-4 are positive controls for the repairs.

| VER | Case | Held by |
|---|---|---|
| VER-001 | Coverage of consumers and scopes against X-1 and DEP-006; App-only acceptance never supplies another consumer | K-7, K-8, N-3, N-23, N-24 |
| VER-002 | Notice without adoption (App v3, Runtime); publication without supply (App v4); App v4's adoption without any other loop's; a human approval faithfully recorded (A-1) and an agent adoption directly captured (AD-1); fabricated or misattributed decisions refused | K-4, K-5, K-6, N-1…N-19 |
| VER-003 | Instruction identity: Root bytes before and after, at the commit; history preserved (the old bytes remain in git) | K-3, K-4, N-20, N-22, N-28 |
| VER-004 | Packaging (export manifest) and currency (no reliance, so no comparison) | K-4, N-21; §4 |
| VER-005 | Promise to derivative to state, recomputed | K-10, N-25 |
| VER-006 | Open owners and points of need kept; no invented mechanism or allocation | K-1 (schema `open`), K-9, N-7, N-26 |

**Claimed rules with a negative case** (each breaks the real account; the named check refuses it):
- schema: adoption needs an act (N-1), an adoption point (N-19); a human act's recorder is not its actor (N-5); `established` needs evidence (N-6); the per-fact evidence kinds (N-8…N-11).
- SR-1 per-fact evidence kinds: N-2, N-8, N-9, N-10, N-11.
- SR-2 delivery only by a routed notice in the receiving lane: N-11 (a manifest statement), N-17 (another lane's file), N-30 (RV3's AA2-R1 construction 1: App v3's README, a real in-lane file).
- SR-3 adoption only by the consumer's own loop's act, in its lane, whose entry names the renewal: N-1, N-3, N-8, N-12, N-13, N-14, N-15 (a person's act with every other field made right), N-18 (a file that is not the act's record), N-31 (RV3's AA2-R1 construction 2: a real, unrelated App v3 sentence, "UPD-133 adopts the stricter live rule …", with the status updated to match), N-32 (RV3's AA3-R1: the routed D-GOV-52 notice's own sentence "Your loop decides whether to adopt, amend or decline." offered as App v3's act). P-4 is the positive control (AD-1's entry names D-GOV-52).
- SR-4 adoption text: N-12 (F-R16's status statement), N-13, N-14, N-16 (App v4's own act with a negated text).
- K-2 manifest: N-27. K-3 rebuild: N-28. K-4 evidence: N-20 (sha256), N-21 (quote), N-22 (commit). K-5 act text in its record: N-4, N-16. K-7 coverage: N-23. K-8 routing: N-11, N-24. K-9 status: N-7 (RN-1), N-26 (RN-2). K-10 trace: N-25. K-11 home path: N-29.

**Claimed or implied rules without a negative case, or not enforced:**
- SR-4 is keyword-based: an act text that says "adopt" without a listed negation passes whatever it means ("App v3 adopts nothing"). Not enforced beyond the keywords.
- K-5's recorder test is a string comparison. It cannot tell whether a named recorder is true; `recorder_stated_by_record` says whether the record names the recorder. Not enforced.
- `candidate_record` and `observation_record` evidence is accepted by kind only; no check resolves its content, because none exists yet. Not enforced.
- `act_class` and `recording_mode` are checked against the act's fields, not against its record: a record could be mislabelled `adoption` and still pass SR-3 if its lane, entry and text pass. SR-4 limits this only by keywords.
- SR-3's renewal test is textual: an in-lane entry (other than the routed notice, AA3-R1) that names the renewal and says "adopts" passes, whatever it decides about it (for example "adopts nothing from D-GOV-52" passes SR-3 and fails only if SR-4's negation list catches it). The entry boundary is a heading or a top-level bold item; a record without either uses the whole text before the quote.
- SR-4's negation list also refuses a genuine adoption phrased with "without" or "no" (for example "adopts … without amendment"; RV3 AA2-N1). This errs towards refusing.
- K-8 checks the RN-1 notices against the one tranche manifest; it does not check RN-2 (no notice exists) or `prepared_notice` against the manifest's text beyond the quote (K-4).
- K-10 recomputes only `applied`. REQ-004's other states (`proposed`, `checked`) and "each needs its own evidence" are not enforced.
- Packaging's established / not established states and the currency rule (§4) have no check beyond the packaging quote; they are read by inspection.
- K-7 matches X-1 consumer names as strings in the vendored RA line.

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
| AA-v0.3, amended in place (2026-10-04) | RV3 AA3-R1 (unit EU-F3R3): SR-3 refuses an adoption act whose record is a notice the renewal's change routes (F-R10); RV3's construction is N-32. Checker and Design only; AA-1 v2 unchanged, so no version step (the coordinator's rule for this round). No further checker hardening in tranche 2 (coordinator's ruling); the remaining textual limits stay listed above |
| AA-v0.3 (2026-10-04) | RV3 AA2-R1 (unit EU-F3R2): SR-2 accepts only a notice the renewal's change record routes; SR-3 requires the adoption act's record entry to name the renewal. RV3's two constructions are N-30 and N-31; P-4 the positive control. The uncovered list states SR-3's textual limit and AA2-N1. Checker and Design only: AA-1 v2, its record format AA-v0.2 and the schema are unchanged, so CA and RP are unchanged |
| AA-v0.2 (2026-10-04) | RV3-AA1 repair, unit EU-F3R with CA-v0.3 and RP-v0.6. AA1-R1: per-fact evidence kinds (§3 table; schema and SR-1), delivery only by a lane file (SR-2), adoption only by the consumer's own loop's adoption act in its lane (SR-3), adoption text (SR-4, keyword-based); acts gain `act_class` and `recording_mode`; evidence kinds `candidate_record`, `observation_record` added; RV3's five variants are N-9…N-13. AA1-R2: "received a notice" replaced by delivery wording (F-R16), carried to CA and RP. AA1-R3: Root's RN-2 search covers the whole repository outside App v4, with RV3's search cited as a second one. N1: AD-1 named as direct capture. Coordinator's audit: every claimed rule computed by one function and broken on the real account; covered and uncovered rules listed in §7. Record format AA-v0.2, AA-1 version 2 |
