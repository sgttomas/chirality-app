# RV2-EUD1: review of EU-D1 (connector standing; PEC and Domains receiving; connector witness)

- **Reviewer.** RV2, a Type 2 TASK. Model: **Claude Opus 5.5** (`claude-opus-5-5`, Anthropic).
- **Run and method.** Run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04. Method: `coordinated-knowledge-work` §3.
- **Reviewer standing.** I authored none of the reviewed files. I was not the isolated reader, and I did not open `RUN/D/key/` until I had derived the Q1 answers myself (see "What I checked").

**Unit (owner O-D, `OWNERS/O-D.md` "CURRENT").** All 16 listed hashes match (`shasum -a 256`). That includes these files:

| File | sha256 (prefix) |
|---|---|
| `CONNECTOR_FALLBACK.md` (CFB-v0.1) | `ae49d654…` |
| `connector.standing.schema.json` | `589f2c5d…` |
| `connector.route-account.schema.json` | `a3fec8d9…` |
| `PEC_RECEIVING.md` (PRC-v0.1) | `1a8acc85…` |
| `pec.receiving-record.schema.json` | `ca7bbd7b…` |
| `DOMAINS_RECEIVING.md` (DRC-v0.1) | `098ff6a1…` |
| `domains.receiving-record.schema.json` | `d871cd4c…` |
| `CONNECTOR_WITNESS.md` (CW-v0.1) | `f836c746…` |
| `RUN/D/run_d.py` | `9974d76d…` |
| `eud1.py` | `c00835bf…` |
| `make_fixture.py` | `4593bf87…` |
| fixture manifest | `0d23fba7…` |
| reader manifest | `65700ab7…` |
| key | `7e8422b9…` |

**Basis read.**
- `SURVEY/S2-D.md` §0.1 and Part 6.
- R23-34 and R23-37.
- DEL-09-10's ScopeOfWork.
- PRD V4-CON-01…05.
- HOST V4-HI-60…63.
- EXP-v0.2's result schema and `check_exp.py`.
- The work graph at both commits.

## Verdict: **REPAIR**

There are no BLOCKING findings. There is **1 MAJOR**, which needs a cross-owner check (FV adoption), and there are **4 MINOR** and **3 NOTE** findings.

What holds and should be kept:
- the three-facet vocabulary with "unknown";
- the CS-R1 rule as stated;
- consumption through H-1 only;
- Domains independence;
- the EXP records, including `inconclusive` for CW-QC;
- the Q1 route answer;
- both departures.

The MAJOR finding concerns one rule, CS-R2. Its wording conflicts with the reliance PRC permits for Q1(a), and the fixture cannot reveal the conflict.

## Findings

### EUD1-R1 — MAJOR (cross-owner: FV adopts this now) — CS-R2 says no connector material establishes `ready`, yet PRC relies on PEC to say which nodes are READY. EU-D1 never exercises a READY node. The hand-off to FV adds "done", which CS-R2 does not contain.

**Evidence.**

The two rules that conflict:
- CFB §2.4 CS-R2: "No connector material, limitation or absence establishes: `no_work` …, `ready` (readiness), `permitted` …, `correct_by_presence`."
- PRC §2 Q1(a) asks "which work-graph nodes are READY, ACTIVE or BLOCKED". PR-6 then relies on PEC "where every needed claim supports it and covers the part". PR-P1 relies on claim c1 for part (a) (`connector_reliance`).

What the basis allows:
- V4-CON-02 allows "Record-tier operational reliance … limited to qualified, released coverage adopted by the receiving consumer".
- V4-CON-03 and V4-HI-62 prohibit only what *absent, stale, partial or failing* feeds imply: "a missing feed cannot imply empty work, readiness or permission".

What EU-D1 does and does not exercise:
- At R (`e086dfff32`) no node is READY, so (a) is empty in every case.
- No case has an adopted, current claim that a node *is* READY.
- So the fixture cannot show which rule wins.

The hand-off to FV in `OWNERS/O-D.md` "CURRENT" says: "nothing about a connector, or its absence, makes any item *ready*, *done* or *permitted* (CS-R2)". The CS-R2 enum (`prohibited_conclusion`) has no "done" value.

**Consequence.**

Suppose PEC is adopted and current, and reports "node Z is READY". The frozen vocabulary then gives two answers:
- **PR-6 (relied):** Z is READY.
- **CS-R2 (never established):** Z is not ready.

FV (O-A) is adopting this vocabulary now. It could implement either reading, or expect a `done` value that does not exist.

The likely intended meaning is that a relied record-tier claim reports the state the cited file records, at the pin, and confers no dispatch, completion or permission. That meaning is not written down anywhere.

**Repair.**
1. Restate CS-R2 in the basis's terms:
   - (i) absence or any limitation never implies empty work, readiness, completion or permission;
   - (ii) a relied record-tier claim reports what its cited record states at the pin, and nothing more. Presence, and the connector itself, never establishes readiness to start, completion or permission.
2. Either add "done"/"satisfied" to the prohibited set, or make the FV hand-off cite CFB §3 and CS-R5 for "never satisfied". Align the wording in `OWNERS/O-D.md` with whichever is chosen.
3. Add one cheap case: Q1 asked at S (`e4a0c2c4c3`), where O-B1 and O-C1 are READY, with an adopted, current PEC response pinned at S. The record should show what is relied on ("recorded READY at S") and still list `ready`/`permitted` as unsupported for dispatch.
4. Re-check FV's adoption against the restated rule, not the current wording (workflow §5).

### EUD1-R2 — MINOR — The schemas accept a tier from the other connector, so CS-R1 can be met by a cross-connector label

**Evidence.** I ran three probes (`$TMPDIR/rv2/probe_eud1.py`, using the three schemas through a `referencing` registry). The schemas accepted all three:

| Probe | Record | What it carries | Result |
|---|---|---|---|
| Q-a | PEC claim | tier `admitted`, adopted + current, `supports_reliance: true` | valid |
| Q-b | Domains result | tier `record`, adopted + current, `supports_reliance: true` | valid |
| Q-c | PEC record | a claim standing with `connector: domains` | valid |

CFB §2.3 defines `record` and `presence_advisory` as PEC tiers, and `admitted` and `located_not_admitted` as Domains tiers. CS-R1 accepts "`record` or `admitted`" for either connector. PR-4 and DR-4 never produce the cross values, but a record or consumer outside the prototype can.

**Repair.**
- State CS-R1 per connector: PEC `record`; Domains `admitted`.
- Add `if connector then tier ∈ …` to the standing schema.
- Require each record's standings to name that record's connector.

### EUD1-R3 — MINOR — PRC §7 and the O-D record predate R23-37

**Evidence.**
- PRC §7 still says "Whether that settles HOSTING §6.8's point is HELP_HUMAN's ruling".
- `O-D.md` still lists "P-H1 ruling | HELP_HUMAN".
- R23-37.1 has since ruled:
  - App-origin reads stay unused;
  - one follow-up probe with a local model is allowed;
  - the reads may be used only if the model input shows no trace.
- R23-37.2 records the -32601 note for DEL-01-01's owner.

**What the probe record supports (`RUN/D/probe/results/observations.json`, read).**
- The probe ran within R23-34.3's limits.
- The kept results contain neither the user name nor the host name (grep).
- `thread/items/list` failed both before and after the call ("not supported yet"). So "no entry in thread items" rests on two things: no `item/*` notification, and the rollout file. It does not rest on an items read. R23-37.1's conclusion stands on that basis; PRC should say which observations support it.

**Repair.**
- Cite R23-37.1 in PRC §7 and state its condition.
- Record the follow-up probe's result when it runs.
- Update O-D's open table.

### EUD1-R4 — MINOR — PR-5 compares citation revisions, so it can mark current claims stale

**Evidence.**
- PR-3 tests freshness by **content**: "if a cited source path has different content at the pin than at the asked revision → `stale`".
- PR-5 tests by **revision**: "A claim whose own citation revision differs from the asked revision is `stale` even in a current response".
- PEC-ORI-004 citations carry "path, anchor and/or SHA". A citation SHA may name the commit that last changed the file, which differs from R even when the content is unchanged.

**Consequence.** The error is false staleness, which is conservative: it adds route use and never adds reliance. But it contradicts PR-3's own test.

**Repair.** Apply PR-3's content test at the claim's citation, and record "revision not comparable" as `unknown`.

### EUD1-R5 — MINOR — Constant times are labelled as observed

**Evidence.**
- `eud1.py` sets `WRITTEN_AT = "2026-10-04T09:00:00Z"   # fixed so the build is deterministic`, and `build(..., date_value="2026-10-04")`.
- The EXP records carry `"date": {"value": "2026-10-04", "source": "observed_clock"}`.
- The route accounts carry that `written_at`, together with a `performed` `locate_compare` duty.
- B-2 requires the committed build to equal a fresh build, so a rerun on any later day still writes the same "observed" date.

**Consequence.** EXP F-9 says the date is recorded "with its source". DEL-09-10 REQ-004 binds each outcome to its actual date. A constant is neither.

**Repair.** Choose one:
- label these values `stated_by_person` or `record_timestamp`, with a limit saying the build is deterministic and the dates are fixed; or
- write the actual time and leave those fields out of B-2's equality check.

### EUD1-R6 — NOTE — The work-graph evidence is labelled `constructed`, but those bytes are real

The EXP part evidence for `records/RA-Q1.json` carries `fixture_standing: constructed`. The route account's two sources are the real committed `WORK_GRAPH.md` bytes; T-7 checks them against `git show`. The PEC/Domains inputs are constructed; the route's sources are not.

A per-source label would let DEL-09-10's dossier distinguish real-file route evidence from constructed connector input. Labelling everything `constructed` is the cautious direction, so this is a NOTE only.

### EUD1-R7 — NOTE — CW-QC's `inconclusive` is right, and should stay visibly a rehearsal

The QC record aggregates as follows:
- QC-1 is `not-run`, with `not_run_because` and record-level `missing_inputs` (PEC release; App adoption);
- UQ-1 and QA-1 are `pass`;
- by EXP-R1 (R23-19 item 3), that gives `inconclusive`, with `limits` present.

This is the honest state. A `blocked` would be wrong, because nothing was attempted (R23-20).

The record's criterion is AC-001 and its run basis is `rehearsal`. Its own limit says it "stands for no scenario", and EXP-R3 forbids a rehearsal standing for a VER criterion. DEL-09-10's later dossier should carry that limit forward, so that no one reads "AC-001: inconclusive" as a candidate result.

### EUD1-R8 — NOTE — Confirmed

**Vocabulary.**
- Three facets. `unknown` is in each, and nothing promotes it:
  - CS-R5;
  - CFB §2.2's order puts `current` last;
  - the schema forces `envelope: unknown` and no reliance when `absent`.
- CS-R1 is schema-enforced in one direction. The prototype checks the other direction on every claim and result (E-Pn).
- `prohibited` must list all four values (enum, `minItems: 4`, `uniqueItems`).

**Departures (R23-37.3).** Both are sound:
- The Domains envelope `adopted` means "identified query contract + established admission basis". Without that value, CS-R1 could never permit Domains reliance. DR-2 and DR-4 still require the result's admission to be found in the basis.
- `unknown` is added to each facet.

**H-1.** PRC §7 and the O-D record agree:
- PEC is reached only as an agent `mcpToolCall` through the person's configuration;
- App-origin reads are unused;
- the App holds no client, socket or token.

Nothing in `eud1.py` or `run_d.py` models an App PEC client.

**Independence (CS-R4).**
- DRC §3: "PEC's state plays no part in admission".
- I-1 rebuilds each connector's records with the other connector's inputs removed, and they are unchanged. I read the code (`run_d.py independence()`).
- The pairs OC-1 (P6 + DM-1) and IA-2 (P1 + DM-2) each keep their own standing.

**EXP records.** All three are valid against EXP-v0.2's schema and pass `check_exp.rule_violations` with no rule fired. `aggregate` gives:

| Record | Outcome |
|---|---|
| CW-EUD1-LC | `pass` |
| CW-EUD1-OC | `pass` |
| CW-EUD1-QC | `inconclusive` |

I ran these checks myself, importing EXP's checker read-only. Each record has `run_basis: rehearsal` and route `model_only`, with the EXP-R3 limit stated.

**No claim beyond constructed inputs.**
- Every PEC and Domains input and the adoption account say "constructed".
- Records carry `simulated: true` with `simulated_terms`.
- DRC §5 states that REQ-004's admitted-source fixtures stay unexercised.
- The one SWBPIPE mention (DRC §6, DEC-051) defers the matter to the host joins.

## What I checked and how

**Rerun, not rebuilt.**
- `python3 -B run_d.py "$TMPDIR/rv2/eud1"` gave **221/221 checks held**, including B-2 (committed `build/` equals a fresh build) and R-1.
- No `__pycache__` was left, and nothing in `RUN/D/` changed (`git status`).

**Q1 ground truth (independent).**
- I read the "Nodes" table of `WORK_GRAPH.md` at `e4a0c2c4c3` (sha256 `a6fb741d…`) and at `e086dfff32` (`1ad91afc…`) with `git show`.
- S is an ancestor of R, and R is in `HEAD`.
- My reading at R:
  - (a) no node is READY, ACTIVE or BLOCKED;
  - (b) the other open node is T2, PLANNED;
  - (c) six changes:

    | Node | Change |
    |---|---|
    | VC | ACTIVE → COMPLETE (R23-22) |
    | E | ACTIVE → COMPLETE (RR-E, RR-F) |
    | O-B1 | READY → COMPLETE |
    | O-C1 | READY → COMPLETE |
    | D | PLANNED → COMPLETE (PR) |
    | T2 | added as PLANNED |

  - No node was removed.
- `RA-Q1` facts f-a…f-c and the six P records agree with this.
- Only after forming this view did I open `key/EUD1_KEY.json` (`7e8422b9…`). Its `q1_truth` matches mine exactly.

**Records read.**
- RA-Q1.
- PR-P1…P6: standing, claims, conclusions, adoption, `simulated_terms`.
- DR-DM-1 and DR-DM-2.
- The three EXP records.
- The constructed adoption account.

**Probes** (`$TMPDIR/rv2/probe_eud1.py`). Q-a, Q-b and Q-c were accepted (EUD1-R2). Q-d (`unknown` condition with reliance) was refused, as it should be.

**Not done here.**
- I did not compare the isolated reader's account (it is separate).
- I did not run the R23-37.1 follow-up probe; it is O-D's.
- I did not read DEL-08-02 RTD (not in the unit).
- I did not check FV's adoption (O-A's, after EUD1-R1).

## Repair confirmation (CFB-v0.2, PRC-v0.2, CW-v0.2; commit `25054b04df`; 2026-10-04)

**Reviewer.** RV2, Claude Opus 5.5 (`claude-opus-5-5`).

### Verdict: **READY.** The repairs are confirmed.

EUD1-R1…R7 are all adopted in the returned files. I raise 3 new MINOR findings and 2 NOTEs (EUD1-R9…R13). None is BLOCKING or MAJOR. Two of the MINORs bear on HELP_HUMAN's own records (R23-41/R23-44 and R23-45.2), so they are flagged for HELP_HUMAN.

### What I checked

**Bytes.** All 20 hashes listed in O-D "CURRENT" match the working files. For the unit's paths the working tree equals the commit (`git diff --quiet 25054b04df`), with one exception: `build/` is not in git (see EUD1-R9). That means `build/reader_input/MANIFEST.sha256` (`e68154c6…`) exists only on disk.

**Prototype.** `python3 -B run_d.py "$TMPDIR/rv2/eud1b"` gives **297/297**, including:
- B-2 (the on-disk `build/` equals a fresh build);
- F-1;
- E-P7 and E-P8;
- the R2 negatives and the control;
- T-9…T-11;
- R-2.

No `__pycache__` was left behind, and nothing in `RUN/D/` changed.

**Independent probes.**
- `$TMPDIR/rv2/probe_eud1.py`, unchanged from round 1: **Q-a, Q-b and Q-c are now refused** by the standing schema's per-connector `if`/`then`. Q-d is still refused.
- I re-validated all three EXP records with EXP-v0.2's schema and `check_exp` (read-only). All are valid, no rule fires, and the aggregates are LC `pass` (now with LC-5), OC `pass`, and QC `inconclusive` (now with QA-2).

### Per finding

| Finding | State | Evidence |
|---|---|---|
| EUD1-R1 | **Confirmed** | See "EUD1-R1" below |
| EUD1-R2 (and FV10-R4) | **Confirmed** | CS-R1 is now per connector ("PEC `record`; Domains `admitted`"), and §2.3 marks each tier "PEC only" or "Domains only". The standing schema refuses a tier from the other connector. The PEC and Domains record schemas require their own connector. My probes Q-a, Q-b and Q-c are refused, and unaltered PR-P1 validates |
| EUD1-R3 | **Confirmed** | PRC §7 cites R23-37.1. It says the "no entry" finding rests on there being no notification and on the rollout, and that no items read was made. It records P-H1b and its scope. The open table is updated |
| EUD1-R4 | **Confirmed** | PR-5 compares the cited file's **content** at the citation, and records "revision not comparable" as `unknown` |
| EUD1-R5 | **Confirmed** | EXP dates are `record_timestamp` with the limit "date is the build constant BUILD_DATE … not a clock observation". The route accounts carry `written_at_source: build_constant` |
| EUD1-R6 | **Confirmed** | Evidence is labelled per source. Work graphs are `recorded`/`static_inspection` (the `git show` bytes). Route accounts carry no fixture label. Constructed records stay `constructed` |
| EUD1-R7 | **Confirmed** | The CW-QC record carries "AC-001 is not examined … do not read this record as a candidate result". CW §4 has the dossier carry this forward |

**EUD1-R1.**
- CFB §2.4 CS-R2 now reads in R23-40's words:
  - (i): absence or limitation never implies empty work, readiness, completion or permission;
  - (ii): a relied record-tier claim "reports only what its cited record states at its pin".
- §3's "Prohibited conclusions" list includes completion. "Done" is not a value of the standing vocabulary.
- **FV10-R5's pointer now resolves:** CFB §3 holds the list.
- **New case P7 (Q1-S).** I checked it against the work graph at S:
  - **Reliance:** adopted and current; c1 is relied on as "PEC reports, from the work graph recorded at e4a0c2c4c3: … VC ACTIVE, E ACTIVE, O-B1 READY, O-C1 READY". That matches my own reading of the S node table.
  - **(b) from the route:** D PLANNED, from `ra:EUD1-Q1S`.
  - **Named as unsupported:** "O-B1 or O-C1 may be started or dispatched now because PEC reports them READY", and "any item is ready to start, complete or permitted".
- PRC PR-6 states every relied part as a report of the record.

### New items

**PR-7 and P8 (from OD-F1): confirmed as a sound rule.**
- A record-tier citation must resolve: the file exists, the revision is readable, and the anchor heading is present. Otherwise the claim is `unknown` and supports no reliance.
- In PR-P8, c3's `#no-such-section` makes c3 `unknown`, `supports_reliance: false`, with the reason "PR-7: anchor … not in …". Because PR-6 needs every claim of a part, (c) goes to the route.
- Presence claims now cite `pec-presence:session/O-A`, not a file. The disabled-PR-7 mutation is reported as caught. I did not rerun the mutation.
- See EUD1-R12 for one consequence at response level.

**The comparison checker (R23-45.1).** The checker is not tuned to the reader in a way that inflates the result. I confirmed 46/46 by reading the account myself (below). However, its forbid check passes paraphrases (EUD1-R10).
- **My scoring of `RR-EUD1/ACCOUNT.json` (`3b31e598…`).** `compare_eud1.py` gives 45 met, 0 not met, 1 referred. I read every case's answer, notes and `cannot_conclude`:
  - every K3 answer equals the truth I derived in round 1;
  - no answer or note states a forbidden conclusion affirmatively;
  - each K5 item is named in substance.
- **The referred P1 K4 item, ruled met under R23-45.1, is fair.**
  - The key's "connector" tests whether the reader relies on the connector where CS-R1 supports it.
  - The reader relied on exactly c1–c7 (K2 met). It wrote "Every claim c1-c7 agrees with the work-graph files, so (a) and (c) rest on both", and still used the route for (b).
  - CFB §3 says the route is "not needed" for relied parts, not that it is forbidden. Checking the files as well removes no reliance.
  - The checker's own guard condition ("when the relied-on claims are exactly the key's K2 set") is the right one. My probe R-7 shows it bites: with an empty relied set, K2 is not met.
- **Sensitivity.** `compare_sensitivity.py` catches its 9 alterations (9/9), all derived from the real account. I tested 7 more in `$TMPDIR/rv2/probe_compare.py`:
  - R-6 ((a) based on files while relying on c1–c7) is caught: K4 not met.
  - R-7 is caught: K2 not met, as above.
  - R-1, R-2, R-3 and R-5 pass; see EUD1-R10.

**P-H1b (R23-45.2).** The record supports the ruling's central claim.
- **Method.** `probe/results_b/model_requests.json` holds the one request Codex sent to the capture-only tap.
- **Contents of that request.**
  - Its `input` is three `message` items: developer, user (`environment_context`), and user (the prompt).
  - None of `P-EX-1`, `toolReceivedAtMs`, "invented example material", `queued` or `proposal` appears anywhere in the body (I counted each).
  - `example_lookup` and `EX-1` appear only once each, in the offered tool definition.
- **Probe hygiene.** The results contain neither the user name nor the host name (grep), and the call and markers are as described.
- **Scope.** The stated scope is incomplete, and the capture keeps some identifying values; see EUD1-R11.

### EUD1-R9 — MINOR (for HELP_HUMAN; R23-41, R23-44): `build/` is ignored by git, so the frozen records and the reader's input set are not in git

**Evidence.**
- The root `.gitignore` line 46 is `**/build/` (`git check-ignore -v`).
- `git ls-tree -r 25054b04df` lists no `D/build/` file. So these are absent from git:
  - the receiving records and route accounts;
  - the EXP records;
  - `RUN_LOG.json`;
  - the reader input set and its manifest.
- B-2's label ("committed build/ equals the fresh build") and O-D's table both say "committed", but this means on disk.
- The round-0 unit (`run_d.py` `9974d76d…`, the 221/221 build and the input set `65700ab7…` that RR-EUD1 actually read) was never in git either (`d43665498d` has no `RUN/D/`). Only RR-EUD1's `SUPPLIED.sha256` records it.

**Consequence.**
- The current build can be regenerated from committed inputs, because the build is deterministic (B-1, F-1, T-7).
- The bytes the reader read, and the bytes RV2 reviewed in round 1, cannot be recovered from git. That is what R23-41.2 is meant to prevent.
- O-A's FV-10 repair vendors copies under R23-44, which covers O-A. It does not cover RR-EUD1's evidence.

**Repair.**
- Commit `RUN/D/build/` with a negated ignore rule, or a vendored copy, at the next path-limited commit.
- State in the RR-EUD1 record that its input set is identified by hash only.
- Relabel B-2 as "the on-disk build".

### EUD1-R10 — MINOR: the checker's forbid test (K6) defaults to "met", so paraphrased forbidden conclusions pass

**Evidence.** In `compare_eud1.py`, K6 is "not met" only for P3's stale states. Otherwise it is "referred" if one of seven literal phrases appears, and "met" if none does. My probes on copies of the real account:

| Probe | Change made to the copy | K6 verdict |
|---|---|---|
| R-1 | P1 notes "T2 can begin now" | **met** |
| R-2 | P6 notes "Nothing is outstanding; the undertaking is finished" | **met** |
| R-3 | P1 answer (b) "T2 PLANNED, ready to dispatch" | **met** (K3 also met) |

O-D's own standard in round 0 was: "A 'forbid' item fails if the reader states that conclusion as supported, in any wording."

A related gap (R-5): P6's K5 checks only the first half of the key item ("nothing … from PEC"), not "its silence is not empty work".

**Consequence.**
- For RR-EUD1 the eight K6 "met" verdicts are right, but only because I checked by reading.
- On a later account, the checker would report "met" for a forbidden conclusion stated in other words.

**Repair.**
- Make K6 "referred" unless notes and answers are absent or have been checked. Alternatively, add paraphrase alterations (such as R-1, R-2 and R-3) to `compare_sensitivity.py` and make them bite.
- Check both halves of P6's K5.
- Record that RR-EUD1's K6 items were confirmed by a person or reviewer reading, not by the checker.

### EUD1-R11 — MINOR (for HELP_HUMAN; R23-45.2): P-H1b's stated scope leaves out two conditions App views will meet, and the committed capture keeps values HOSTING §9.1 lists for redaction

**Scope evidence.**
- `probe_model_input.py` and `observations.json` show the following order of events:
  - the App-origin call was made on a thread with **no prior turn**;
  - it was made **between turns**: the call returned, then `turn/start` followed;
  - only the first request of that next turn was captured.
- R23-45.2's scope names the pin, the route and "the first request of the next turn". It does not name:
  - a thread that already has history (and compaction);
  - a call made **during** an active turn.

  An App view reading PEC while the agent works would meet both.

**Redaction evidence.** The committed `model_requests.json` contains:
- `<timezone>America/Edmonton</timezone>`;
- `x-codex-installation-id` and `installation_id`, which come from the scratch home;
- session, thread and turn ids.

HOSTING §9.1 names "the host's time zone" and the "installation identifier" among the categories a captured provider exchange carries and that the redaction record covers. The probe's own check covered only the user name and the host name.

**Repair.**
- Add the two conditions to R23-45.2's scope, or run the follow-up probe for a call during an active turn.
- Redact the time zone and the identifiers in the kept capture, or record why each is kept.

### EUD1-R12 — NOTE: P8's response-level standing does not show that a claim is `unknown`

PR-P8's `response_standing` stays `adopted`/`current`/`record`, with `supports_reliance: true`, while c3 is `unknown` and part (c) needs the route.

This is correct at claim level and in PR-6's per-part conclusions. A consumer that reads only `response_standing`, as RF-5a does, would still treat the record as fully reliable. It belongs with FV10-R3 (route still needed for some parts) in O-A's FV-10 re-review.

The CFB rule could also say so: §3's "Reliance supported for some parts" row should be visible at response level, for example by adding the uncovered parts to `reasons`.

### EUD1-R13 — NOTE: two labels left behind

- CFB §1 still names "PRC-v0.1". PRC is v0.2.
- CFB §3 item 3 ("complete, done or satisfied", said of an item) sits beside "A connector need counts as met only when CS-R1 supports reliance". Reserving "satisfied" for needs only would avoid a reader taking the two sentences as conflicting.

**Not done.**
- I did not rerun the PR-7 mutation.
- I did not re-run P-H1b. Its bytes and scripts were read, not executed.
- I have not checked O-A's re-pin to the new schema; that review follows.
