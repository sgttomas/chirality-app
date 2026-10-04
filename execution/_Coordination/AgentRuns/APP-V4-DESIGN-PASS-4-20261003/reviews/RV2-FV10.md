# RV2-FV10: review of DEL-06-02 FV-10 with DEL-06-01 RF-5a

- **Reviewer:** RV2 (Type 2 TASK), model **Claude Opus 5.5** (`claude-opus-5-5`). Run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04. Method: `coordinated-knowledge-work` §3.
- **Basis:** R23-34.10, R23-37.4, R23-39 and R23-40. Reviewed against the restated CS-R2 (R23-40), not against CFB-v0.1's old wording.
- **Unit:** owner O-A, `OWNERS/O-A.md` "CURRENT", as committed at `d43665498d`. For PKG-06 the working tree equals the commit (`git diff --quiet d43665498d`). All six hashes match:

| File | sha256 (prefix) |
|---|---|
| `FLEET_RECORDS.md` | `c328ebfc…` |
| `fleet_store.py` | `75c07f44…` |
| `run_fleet.py` | `efb37ed4…` |
| `FLEET_VIEWS.md` | `eb0c6734…` |
| `fleet_views.py` | `a187fd4f…` |
| `run_views.py` | `9c39d9bb…` |

- **Change read:** `git diff 75604b3c49 d43665498d` over PKG-06, covering the six files (+256/−13).

## Verdict: **REPAIR**

There is no BLOCKING finding. There are **2 MAJOR** findings, one of them cross-owner (for HELP_HUMAN), plus **1 MINOR** and **3 NOTE**.

**What is right and should be kept:**
- RF-5a's rule as written, and FV-10 wording DEL-06-01's facts with no override (C8).
- The R23-40 wording. FV-10's CS-R2 bullet now carries all six of R23-40's points.
- C3/C4, which show that satisfying a need is not readiness.
- C7, which shows that no other row changes.

**The two defects:**
1. A connector need is recognised only by the record file's content, so a damaged or drifted record falls back to the presence reading that R23-39 removed.
2. RF-5a and FV-10 depend on DEL-07-02's schema and O-D's records. Neither is in the candidate commit, neither is pinned in the code, and both are being repaired now.

## Findings

### FV10-R1 — MAJOR: a torn or drifted connector record is satisfied by its presence (FR RF-5a; FV §2 input row; `fleet_store.connector_need`)

**Evidence.**

- FR RF-5a defines a connector need by the file's content: "An input need whose file is a connector receiving record (a JSON record with `response_standing`) is a **connector need**".
- `connector_need()` returns `None` when the JSON cannot be parsed, when it is not a dict, or when it lacks `response_standing`. `Reader.item_facts` then falls back to `("satisfied", "input present") if os.path.exists(p)`.
- FV §2's input row states the same fallback: "The need is an ordinary input (presence), since the file is not a connector record".
- Scratch probe `$TMPDIR/rv2/probe_fv10.py` imports the committed `fleet_store` unchanged. Results:

| Probe input | Outcome |
|---|---|
| O-D's PR-P6 (PEC absent) truncated to half its bytes | `connector_need` → `None`, so the Reader says **satisfied (input present)** |
| PR-P6 with `response_standing` renamed (a format drift) | **satisfied (input present)** |
| A missing record | outstanding "input not present" (the connector route reference is lost) |

**Consequence.**

- Take an absent-PEC record that is damaged. RF-5a would call it *outstanding*; the damage makes it *satisfied*. Under FV-4, an item whose only need it is then becomes *ready*.
- That is the defect R23-39 named ("its facts would call a connector receiving record 'satisfied' whatever its standing"), reached through a damaged file.
- It also contradicts FR's own treatment of torn records: RF-10 and RF-11 make a torn line a limit and the need *unknown*, never satisfied.

**Repair.**

- Declare a connector need in the graph or brief rather than detecting it by content. For example, an input need with `connector: pec|domains`, or its own need kind. This is FR's schema enum, O-A's to choose.
- For a declared connector need:
  - missing record → *outstanding*, with the connector named;
  - unreadable record, no standing, or a nonconformant standing → *unknown* (CS-R5);
  - never the presence reading.
- Add the three probes above as cases in `run_fleet.py` and `run_views.py`.

### FV10-R2 — MAJOR (cross-owner, for HELP_HUMAN): the unit relies on files that are not in the candidate commit, are not pinned in code, and are under repair (RF-5a; FV-10; R23-21, R23-41)

**Evidence.**

The two inputs are absent from the commit:
- `git ls-tree d43665498d` has no DEL-07-02 `Design/` folder (no `connector.standing.schema.json`) and no `RUN/D/` folder (no `build/records/PR-P*.json`).
- In the working tree, `git status` shows DEL-07-02 `Design/` as untracked.

Nothing pins them in the code:
- `fleet_store.py` reads `STANDING_SCHEMA` from DEL-07-02's working folder at run time.
- RF-5a says the schema is used "as it is", with no hash.
- `run_fleet.py` and `run_views.py` copy O-D's records from `RUN/D/build/records/` at run time.
- FV's change note does name `589f2c5d…`, but nothing checks that hash before use.

Both inputs are being changed:
- O-D is repairing CFB and its records under R23-40.4 and EUD1-R2…R5. The repairs include adding per-connector tier rules to the schema and changing the record dates.

**Consequence.**

- A checkout of the candidate commit cannot rerun 37/37 or 31/31.
- When O-D refreezes, FR and FV will change behaviour silently. The cross-tier cases in my probe are an example: today they read *satisfied*; under a repaired schema they would read *unknown*.
- The evidence in this unit would then rest on bytes nobody can name.
- This is the R23-21 situation (dependents keep the version they relied on) together with R23-41's recoverability rule. The candidate commit took only the unit's own paths, not its inputs.

**Repair (O-A and HELP_HUMAN).**

- HELP_HUMAN: commit O-D's frozen EU-D1 inputs (schema and records), or a pinned copy, at a commit this unit can name.
- O-A: pin the standing schema and the example records by sha256 in RF-5a's and FV-10's text, and check the hashes in `run_fleet.py` and `run_views.py` before use.
- O-A adopts O-D's repaired schema as a deliberate re-pin after O-D refreezes, and reruns C1…C8 against it.

### FV10-R3 — MINOR: a *satisfied* connector need hides that the record still needs the route for part of its question (RF-5a; FV-10 "Satisfied")

**Evidence.**

- RF-5a reads `response_standing` only.
- PR-P1 (adopted and current) has `response_standing.supports_reliance: true`, yet its own `route` is `{needed: true, account_ref: "ra:EUD1-Q1"}`, because Q1(b) is outside PEC's coverage (PRC §2; CFB §3 "Reliance supported for some parts … route needed for the other parts").
- The satisfied fact's text is "connector reliance supported (pec: …; pr:EUD1-P1)" and does not mention the route.
- In C4, W13 ("Q1 answered") becomes *ready (qualified)* on PR-P1 alone.

**Consequence.** A person reading W13's row is not told that part of the question must still come from files. This is not a wrong category, since the route is part of W13's own work. It is a missing fact.

**Repair.**

- When the record's `route.needed` is true, the satisfied fact and the row name the route account ("reliance supported for the covered parts; the source-file route ra:… is needed for the rest").
- Alternatively, let a need name the parts it requires.

### FV10-R4 — NOTE: FV-10 inherits the cross-tier gap from EUD1-R2 (O-D's to fix; tracked there)

The same probe shows two readings that should not be possible:
- PR-P1 with `claim_tier: admitted` reads *satisfied* ("pec: … claim tier admitted").
- PR-P1 relabelled `connector: domains` (claim tier `record`) also reads *satisfied*.

RF-5a correctly applies the schema "as it is". The fix belongs in DEL-07-02's schema (EUD1-R2). FV10-R2's re-pin is where FV adopts it.

### FV10-R5 — NOTE: the "done" pointer is correct by R23-40.2, but its target is not yet repaired

FV-10 says "The prohibited conclusions are those listed in DEL-07-02 CFB §3 and stated with CS-R5". At `ae49d654…`, CFB §3 is the "Condition → route" table, and the prohibited list is in §2.4 CS-R2. R23-40.4 routes the move to O-D.

I will confirm that the pointer resolves when O-D refreezes. No FV change is needed unless O-D's §3 ends up different.

### FV10-R6 — NOTE: what I confirmed

**Read as frozen.**
- FV-10 and RF-5a use DEL-07-02's facets and values without redefining them. They add no value, no tier and no ordering.
- The validator is built on `$defs/standing` of the schema as it is.
- *Unknown* covers CS-R5 and nonconformance.
- A standing that is conformant but inconsistent the other way (adopted, current and `record`, yet `supports_reliance: false`) reads *outstanding*. That is conservative. CS-R1's "those three values give reliance" direction is O-D's prototype check, not FR's, which is acceptable.

**Satisfied only under reliance.** `connector_need` returns *satisfied* only when `supports_reliance` is true and the standing validates. The schema forces envelope `adopted`, condition `current` and tier `record` or `admitted` in that case.

**Not readiness (R23-40.3).**
- C3: W12 has an adopted, current connector, yet still waits for W2.
- C4: W13 is *ready (qualified)* only because its one need is met, and it is still qualified by `thr-cx`.
- FV-4 is unchanged.

**Wording.** All six R23-40 points appear in FV-10's CS-R2 bullet:
- categories come from files only;
- a need is satisfied only under CS-R1/RF-5a;
- satisfying a need is not readiness;
- absence or limitation implies nothing;
- a relied claim reports only what its record states;
- "done" points to CFB §3 with CS-R5.

The change note records it.

**C8.** DEL-06-01's facts give the same states FV shows:

| Item | State |
|---|---|
| W10 | outstanding |
| W11 | outstanding |
| W13 | satisfied |
| W14 | unknown |
| W15 | unknown |

FV only words them (`fleet_views.waiting` uses `n["why"]` and adds the record to `sources`). The new `root` parameter of `waiting()` is unused and harmless.

**C7.** `run_views.py` compares every base item's category and causes with the r3 copy. They are equal.

## What I checked and how

- **Reran, not rebuilt.**
  - `python3 -B run_fleet.py`: **37/37**, including that the committed FX-FL1 equals the one built now.
  - `python3 -B run_views.py`: **31/31**.
  - No `__pycache__` was left, and PKG-06 is unchanged (`git status`).
- **Diff.** I read every hunk of the change against `75604b3c49`.
- **Probes.** `$TMPDIR/rv2/probe_fv10.py` (FV10-R1, FV10-R4) imports `fleet_store` unchanged. Its temporary folder was removed.
- **Commit contents.** `git ls-tree -r d43665498d` for PKG-07 and `RUN/D/` (FV10-R2).
- **Basis.** R23-39 and R23-40, read in full. CFB-v0.1 §2–§3 at `ae49d654…`. PR-P1's `route` element.
- **Not done:**
  - I did not check O-D's CFB repair; that confirmation follows O-D's refreeze.
  - I did not rerun DEL-04-03's or E's checks, because this unit does not touch them.

## Repair confirmation (FV-10 + RF-5a refrozen; commit `289248709f`; 2026-10-04)

**Reviewer.** RV2, Claude Opus 5.5 (`claude-opus-5-5`).

### Verdict: **READY.** The repairs are confirmed.

FV10-R1…R5 are adopted in the committed files. R12 (P8) yields one new MINOR for O-A, FV10-R7. There are three NOTEs (FV10-R8). Nothing is BLOCKING or MAJOR.

### What I checked

**Hashes.** All 12 files in O-A "CURRENT" match the working tree, including the five vendored files and `VENDOR.json` (`0cba60f4…`).

**Commit check under R23-48.1.** `git status --short --ignored` on the PKG-06 paths prints nothing: no untracked or ignored file. `git ls-files` lists the five vendored files.

**Clean checkout under R23-44.**
- Method: `git archive 289248709f projects/chirality-app-v4 | tar -x` into `$TMPDIR/rv2/clean`. This is read-only git, with no worktree.
- From there, `run_fleet.py` gives **42/42** and `run_views.py` gives **34/34**.
- A grep of the prototypes finds no absolute path, home path or `RUN/D/build` reference. The DEL-07-02 folder is not read.
- The unit is reproducible from git alone.

**Vendored bytes (FV10-R2).**
- `connector.standing.schema.json` is `bf4cef4d…0719`. It equals `git show 25054b04df:` of DEL-07-02's schema (CFB-v0.2).
- `PR-P1` (`b9cd7cce…`), `PR-P3` (`fcacb91a…`) and `PR-P6` (`98aa1d8e…`) equal O-D's records. They are listed with those hashes in O-D's reader-input manifest. That manifest is on disk as `e68154c6…`, the value O-D's committed "CURRENT" table names. (The `build/` folder itself is not in git; see EUD1-R9.)
- `fleet_store.vendored()` hashes each file against `VENDOR.json` before use and raises `VendoredInputChanged` on a mismatch. A case in `run_fleet.py` tests that refusal.
- The re-pin from v0.1 is stated in `VENDOR.json`.

### Per finding

| Finding | State | Evidence |
|---|---|---|
| FV10-R1 (MAJOR) | **Confirmed** | See below |
| FV10-R2 (MAJOR) | **Confirmed** | See "What I checked" above |
| FV10-R3 | **Confirmed** | A satisfied need whose record has `route.needed` says "reliance covers only the record's covered parts: the source-file route ra:EUD1-Q1 is still needed for the rest" and sets `routeNeeded`. FV C9 checks this on W13, and `run_fleet` checks it on C8b |
| FV10-R4 | **Confirmed** | The vendored v0.2 schema refuses cross-connector tiers. My probe's PR-P1 with tier `admitted` reads *unknown* (nonconformant). RF-5a also checks the declared connector: a record whose standing says `domains` under a declared `pec` need reads *unknown* |
| FV10-R5 | **Confirmed** | FV-10 now points to "DEL-07-02 CFB-v0.2 §3". At `cf805bb8…` that section holds "Prohibited conclusions" |

**FV10-R1 in detail.**
- `fleet.record.schema.json` adds need kind `connector`, with a required `connector` field.
  - INV-FL-8 refuses a connector need that omits it.
  - INV-FL-9 refuses `connector` on a plain input.
- I re-ran my probes against the committed `fleet_store` (`$TMPDIR/rv2/probe_fv10b.py`), with declared `pec` needs:

  | Record | State |
  |---|---|
  | Half-truncated PR-P6 | *unknown* ("unreadable (torn or not JSON)") |
  | Standing key renamed | *unknown* ("has no standing") |
  | Missing | *outstanding*, with the connector named |
  | Unaltered PR-P1 | *satisfied*, with the route note |

- The presence reading never applies to a declared connector need.
- RF-5b makes a connector record named as a plain input *unknown*. Both checks carry the probes as cases.

### FV10-R7 — MINOR (new; EUD1-R12 as R23-48 directs): RF-5a lets record-level reliance hide a claim-level `unknown`

**Evidence.**
- `connector_need()` reads only `response_standing`, plus `route`. It never reads the claims.
- Probe `$TMPDIR/rv2/probe_p8.py` used O-D's PR-P8, in which c3 is `unknown` under PR-7 (an unresolvable anchor):
  - **As built.** The result is "connector reliance supported (pec: envelope adopted, condition current, claim tier record; pr:EUD1-P8); reliance covers only the record's covered parts: the source-file route ra:EUD1-Q1 is still needed for the rest". c3 is not named.
  - **With `route.needed` set to false and nothing else changed.** The result is a bare "connector reliance supported … condition current", with `routeNeeded: false`. No signal remains.

**Consequence.**
- In O-D's builds, PR-6 sends any part with an unrelied claim to the route, so the route note appears. In practice the user is told that files are still needed, but not that a claim is `unknown`.
- Under CS-R5 an `unknown` is never shown as current. RF-5a's fact still says "condition current" for a record that holds an `unknown` claim. The only safeguard is the record's `route.needed` value, which neither the standing schema nor RF-5a cross-checks.

**Repair (O-A).** Either:
- have RF-5a list, in the satisfied fact, every record-tier claim whose standing does not support reliance (id and condition, for example "c3 unknown: PR-7"); or
- refuse *satisfied*, making it *unknown*, when such a claim exists but `route.needed` is false.

Vendor PR-P8 (O-D's frozen bytes) and add both probe variants as cases.

### FV10-R8 — NOTES

- **`VENDOR.json` is not pinned.** It holds the pins but is not itself pinned: editing a vendored file and its entry together would pass `vendored()`. FR or FV could record `VENDOR.json`'s sha256 (`0cba60f4…`), or the check scripts could compare it.
- **Stale schema label.** In `fleet.record.schema.json`, the description of `connector` still says "DEL-07-02 CFB-v0.1 §2". The vendored schema is CFB-v0.2's.
- **RF-5b cannot see a torn record.** RF-5b recognises a connector record named as a plain input only if the record parses. A torn connector record used as a plain input still reads by presence. Declaring the need is the contract, and INV-FL-9 and RF-5b cover the readable case. Recorded only.

**Not done.** I did not re-read DEL-04-03's or E's checks; this unit does not change them.
