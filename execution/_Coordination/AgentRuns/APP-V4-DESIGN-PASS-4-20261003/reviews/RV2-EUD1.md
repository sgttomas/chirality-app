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
