# O-A — DEL-06-01, DEL-06-02 (owner notes and returns)

Owner O-A: Type 2 TASK, Claude Opus 5.5, high effort, standing assignment
from HELP_HUMAN (run `APP-V4-DESIGN-PASS-4-20261003`). Read-only git; no
network. Paths are relative to `projects/chirality-app-v4/execution`.

## CURRENT — GUIDE ACT re-pin (tranche-2 closeout item), done (2026-10-04)

DEL-03-04 `HOST_INTEGRATION_GUIDE.md`.

- **Reliance unaffected.** v0.10 (`1bf0ce8e…`, git `09ca67d094`) → v0.11
  (`597f13bd…`, git `0bd6e4b4e9`) changes exactly three lines, by
  `git diff -U0`:
  - L2: the label;
  - L4: the change note;
  - L1749: the §10.3 DEL-10-03 receiver row.

  The A16 rows the GUIDE adopted at v0.7 (§2.1, §2.4, §2.5, §4.1, §9, §10.1)
  are byte-identical. A correction to the coordinator's summary: v0.11 does
  not contain the claim-connector check. That was DEL-06-01's
  `fleet_store.py`, a separate change in the same commit.
- **Edit.**
  - L26: the ACT row now reads ACT-POLICY-v0.11 with sha256 `597f13bd…`,
    and its version cell names the v0.10→v0.11 step.
  - L75: a new one-paragraph re-pin note after the last one (closeout G),
    in the GUIDE's own re-pin-note style.

  No GUIDE version step. Nothing else changed (`git diff -U0`: `@@ -26
  +26`, `@@ -74,0 +75,2`).
- **Pin check.** B8's `pins.py` (sha256 `b943319d…5423`, unchanged;
  `$TMPDIR/c1/pins.py`), check mode: 24/25 before (ACT differed),
  **25/25 after**.
- **Other GUIDE rows pinning a file changed in tranche 2: none.** Every other
  row's pin equals its file's current bytes (24/25 before the edit).
- **GUIDE sha256:** `a656682e…fdae59` before, **`5050658818c24a8600e53686d16a7f6ca6aba9724ee558ecc17d3d9a184b113b`** after.

## ACT-POLICY-v0.11 (O-E's request, R23-31.10) and the FV10-R9 case, frozen (2026-10-04)

Two independent changes. Commit them by path.

### ACT-POLICY-v0.11 (DEL-04-01)

- **§10.3, DEL-10-03 row.** It now maps what DEL-10-03 RA-v0.1 (`caed56b8ea`,
  entry S-6) reads:
  - §2.1: the acts, with decision actor, subject and evidence;
  - §3: S1–S12;
  - §8: DECISION-1's reserved acts (§8.2) and the values still open (§8.4).

  It also notes that ACT shapes nothing for DEL-10-03, and that the missing
  ScopeOfWork receiver and mirror row are RA F-RA1, for the next amendment.
  Not fixed here.
- **Version label (R23-21).** v0.10 → **v0.11**, with a one-line change note.
  No rule, act or value changed, so v0.10 pins keep their reliance (R23-21
  item 3).
- **Changed lines:** L2 (label), L4 (change note), L1749 (the row).
- **Check.** `validate_policy.py`: 6 PASS, all expectations held. ACT's
  schema is unchanged.
- **sha256:** `ACT_AND_POLICY_CONTRACT.md`
  597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2
  (v0.10 was `1bf0ce8e…`).
- **Files that pin v0.10's hash `1bf0ce8e…`.** Found by a script search of
  prefixes 64/16/12/10 over the project. Not edited; for the closeout:
  - DEL-03-04 `HOST_INTEGRATION_GUIDE.md`;
  - DEL-09-05 `DECISION_ATTRIBUTION_CASE.md`;
  - DEL-09-11 `READER_METHOD.md`;
  - run records `SURVEY/S2-D.md`, `S2-E.md`, `S2-F.md` (historical);
  - this file.

  ACT's own line 2 names it as the superseded version.

### FV10-R9 claim-connector case (DEL-06-01, offered for the closeout; separate case)

- RF-5a now counts a claim tagged with a connector other than the declared
  one as not relied ("c1 tagged domains, not the declared pec").
- New case P8x: PR-P8 without c3, with `route.needed` false, and with c1
  tagged `domains`/`admitted`. The need is *unknown*.
- FR records the other FV10-R9 limit (a claim missing from the record), which
  stays with the record's producer (PRC PR-6).
- **Checks.** `run_fleet.py` 46/46 (45 before); `run_views.py` 36/36,
  unchanged. No vendored file changed. No `__pycache__`.

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` | dbfcaf9a53c8e3913967eaf0809977cc42ee2bcd2e551834644cf50e8455f4a1 |
| DEL-06-01 `Design/prototype/fleet_store.py` | 68032697fd25b583259bd97a14efe247b54892630326fa0296c4f85da087bda9 |
| DEL-06-01 `Design/prototype/run_fleet.py` | caa28faea23bf6a2240a2483048654da080e9c4b7bfaf3bb35f1281735663cac |

`git status --short --ignored` on PKG-04 and PKG-06 lists exactly these four
files: ACT plus the three above.

## FV10-R7/R8 round frozen (2026-10-04); FV-10 + RF-5a READY at 289248709f before it

Commit by path:
- the eight changed files below;
- the new `vendored/EU-D1/PR-P8.json`;
- the changed `VENDOR.json`.

`git status --short --ignored` on PKG-06 lists exactly these, with no ignored
file.

- **FV10-R7 (MINOR).** RF-5a now reads each claim's own standing when the
  record supports reliance:
  - a record- or admitted-tier claim that does not support reliance is
    listed in the fact (`unreliedClaims`, e.g. "c3 unknown: …");
  - if the record's `route.needed` is false, the need is **unknown**, not
    satisfied, so record-level reliance never hides a claim-level gap;
  - presence-advisory claims are listed as advisory, not as gaps.

  Cases on vendored PR-P8:
  - `route.needed` true → satisfied, naming c3 and the route (run_fleet P8a;
    FV C13);
  - `route.needed` false, nothing else changed → unknown (run_fleet P8b;
    FV C14).
- **FV10-R8 (notes).**
  - `VENDOR.json` is pinned in `fleet_store.py` (`VENDOR_SHA256`). A case
    edits a vendored file and its entry together, and it is refused.
  - The schema's connector label now says CFB-v0.2.
  - FR RF-5b states that the declaration is the contract: a torn record used
    as a plain input reads by presence, as any plain input does.
- **PR-P8 vendored** from O-D's `D/evidence/records/` (`174e1291…`), after
  the R23-48.1 move. It was not yet in git when I copied it, so if O-D's
  committed bytes differ I re-pin (VENDOR.json says so).
- **Checks.** `run_fleet.py` 45/45 (42 before); `run_views.py` 36/36 (34
  before). FX-FL1 is unchanged. No `__pycache__`.

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` | 0af6a1893801936dd51cbbfa8ca215cc904afc1da12a202e354a5cd5cc65e66f |
| DEL-06-01 `Design/fleet.record.schema.json` | 191ca7b16912a095ee2650d975d60b1ab65d0e3f585d2391d6b8e6db288b0918 |
| DEL-06-01 `Design/prototype/fleet_store.py` | eb391dbbd61c34b5d7b16aa20662188865f077b25a6b6b939f5bd7767d010016 |
| DEL-06-01 `Design/prototype/run_fleet.py` | efffb67b19bdc559b6dacf52c09f89b6c5c92d5f54919abac8b1ccabe21063ad |
| … `vendored/EU-D1/VENDOR.json` (pinned as `VENDOR_SHA256`) | d02ffe5d90c2a96292f085194860313cbeb33e3fe26fa0a4355b8846d1ebe811 |
| … `vendored/EU-D1/PR-P8.json` (new) | 174e129146ad13932211a5c1407eb5089969c62fca5f53f5fb299ef44bbe4fec |
| … `vendored/EU-D1/` schema, PR-P1, PR-P3, PR-P6 | unchanged (`bf4cef4d…`, `b9cd7cce…`, `fcacb91a…`, `98aa1d8e…`) |
| DEL-06-02 `Design/FLEET_VIEWS.md` | 8c4e83781262d1212c5e462c5b9b2ce65c8b8c5c03fc3aaa5191b18e35a54645 |
| DEL-06-02 `Design/prototype/fleet_views.py` | 6be29240168e2fff3305277e41dbb3a319c0df4fc1a2b16f727b4fd2fb30a8ec (unchanged) |
| DEL-06-02 `Design/prototype/run_views.py` | a831199c6c9dc8bda020f5b4023e74602c52174ce318246e4ee9e5342ed999da |

## FV-10 + RF-5a refrozen after RV2-FV10 (READY at 289248709f) (2026-10-04), with vendored inputs

This section supersedes the FV-10 and RF-5a sections below. Commit the unit
**with** `DEL-06-01 Design/prototype/fixtures/vendored/EU-D1/` (5 files).

- **FV10-R1 (MAJOR): declared connector needs.**
  - New need kind `connector` with `connector: pec|domains` in
    `fleet.record.schema.json`. INV-FL-8 refuses one with no connector;
    INV-FL-9 refuses `connector` on a plain input.
  - RF-5a reads a declared need from the record's standing, never by
    presence:
    - missing → *outstanding*, with the connector named;
    - unreadable, standing-less, nonconformant or from another connector →
      *unknown*, consistent with RF-10 and RF-11.
  - RF-5b: a connector record named as a plain input is *unknown* ("declare
    it as a connector need").
  - RV2's probes are now cases in both checks: a half-truncated record
    (*unknown*), a renamed standing key (*unknown*) and a missing record
    (*outstanding*).
- **FV10-R2 (MAJOR, R23-44): vendored inputs.**
  - Copied into DEL-06-01 `prototype/fixtures/vendored/EU-D1/`, with
    `VENDOR.json` recording each file's sha256 and source.
  - `fleet_store.vendored()` checks each hash before use and refuses changed
    bytes (`VendoredInputChanged`). A case in `run_fleet.py` tests the
    refusal.
  - **Re-pin, noted:** the frozen v0.1 bytes (schema `589f2c5d…`, records
    `8d0cb89a…`, `4e759148…`, `03dd7244…`) were never committed. They had
    already been replaced in the working tree when I copied. The vendored
    bytes are **EU-D1 v0.2 (CFB-v0.2)**:
    - schema `bf4cef4d…0719`, equal to git `25054b04df`;
    - PR-P1 `b9cd7cce…`, PR-P3 `fcacb91a…` and PR-P6 `98aa1d8e…`, equal to
      O-D's frozen reader-input manifest `e68154c6…`.

    C1…C8 behave the same against v0.2. CS-R1 per connector now refuses
    cross-tier standings (FV10-R4, by O-D's schema).
- **FV10-R3 (MINOR):** a satisfied need whose record has `route.needed`
  names the route ("reliance covers only the record's covered parts: the
  source-file route ra:EUD1-Q1 is still needed for the rest"), and sets
  `routeNeeded`. Checked on W13 (FV C9) and C8b (`run_fleet.py`).
- **FV10-R5:** FV-10's "done" pointer now names CFB-v0.2 §3, where O-D's
  refreeze put the list.
- **Checks.**
  - `run_fleet.py` gives 42/42 (37 before: +FV10-R3, the probes,
    vendored-hash refusal, INV-FL-8 and INV-FL-9).
  - `run_views.py` gives 34/34 (31 before: +C9…C12).
  - FX-FL1 is unchanged (`0489bc61…`).
  - No `__pycache__` left.

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` (FR-v0.1, repaired in place) | 823989cd23dc715a8327f993c2d5abfdfc7e27dab7c4b8650136ed0721cc43fb |
| DEL-06-01 `Design/fleet.record.schema.json` (need kind `connector`) | d3897bbddc99c1a856390e63627153186fd2525118399faa38262d6f2ee9c8e8 |
| DEL-06-01 `Design/prototype/fleet_store.py` | 42e72011519784b6e984ca16f1fa869e3d8b25c8e5c82bee6538d7f805940bae |
| DEL-06-01 `Design/prototype/run_fleet.py` | 8df857a9457d2bb3323e4b6326472139fe469677dbf88d170b8d91efee8d6c62 |
| DEL-06-01 `Design/prototype/fixtures/vendored/EU-D1/VENDOR.json` | 0cba60f44d43ccaa8fa703841127ffe706e1dddd7190c3a59bb82ec463d380e3 |
| … `vendored/EU-D1/connector.standing.schema.json` | bf4cef4df1ef16bc4a2a8e8fbb341798a90a48abbbe3689d68d5ce9019650719 |
| … `vendored/EU-D1/PR-P1.json` | b9cd7cce7fbf459d06a26e29ad3f2d6bc94384d3c8f4f4b3dcf359b91ab24689 |
| … `vendored/EU-D1/PR-P3.json` | fcacb91a8a4e4e981cbe602cefd8283334d89f2d2394ad295ba470eac413acce |
| … `vendored/EU-D1/PR-P6.json` | 98aa1d8e14dbaff525d9a0462583157fe90aedf7d7a516012ca9deb50bac95e8 |
| DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1, repaired in place) | ece59b9a997c8d3b9405fa7d4e569ad156167a90634080d47e43810b23727a7f |
| DEL-06-02 `Design/prototype/fleet_views.py` | 6be29240168e2fff3305277e41dbb3a319c0df4fc1a2b16f727b4fd2fb30a8ec |
| DEL-06-02 `Design/prototype/run_views.py` | aee27d721b8a2974036e0af42aea8cc245218b2fe708c74c6013108def43ea0c |

## FV-10 with RF-5a (R23-39), first freeze (superseded above)

This section supersedes the FV-10 section below. The two units are reviewed
together.

- **RF-5a (DEL-06-01 FR-v0.1, repaired in place with a change note).**
  - The connector reading (`connector_need`) moved from DEL-06-02's prototype
    into DEL-06-01's reader. A connector need is *satisfied* only when its
    standing supports reliance (CS-R1). It is *unknown* when the condition is
    unknown (CS-R5) or the standing is nonconformant. It is otherwise
    *outstanding*, with the facets, reasons and the route account.
  - Other input needs keep the presence reading.
  - FR §5 gains the need row and §6 gains RF-5a.
- **FV-10 (FV-v0.1).** It now words DEL-06-01's facts and does no reading of
  its own. C8 was adjusted:
  - before: DEL-06-01 says "satisfied" and FV overrides it;
  - now: DEL-06-01's facts give the same states FV shows (absent and stale
    outstanding, adopted and current satisfied, nonconformant and unknown
    *unknown*), with no override.
- **Cases in `run_fleet.py`, on a scratch FX-FL1 with revision r3 and O-D's
  records, read as they are:**
  - C2: adopted but stale → outstanding, with `ra:EUD1-Q1`;
  - C5: a stale standing altered to claim reliance → nonconformant,
    *unknown*;
  - C8: absent → outstanding; adopted and current → satisfied; a plain input
    still reads by presence.
- **Checks.** `run_fleet.py` gives 37/37 (34 before). `run_views.py` gives
  31/31. FX-FL1 is unchanged (`0489bc61…`), as is the schema.
- **R23-40 (wording only).** FV-10's CS-R2 bullet is restated:
  - FV's categories derive from project files only;
  - a connector need is satisfied only under CS-R1 / RF-5a;
  - satisfying a need is not readiness (evidence: C3 and C4);
  - absence or limitation never implies empty work, readiness, completion
    or permission;
  - a relied record-tier claim reports only what its record states;
  - "done" points to CFB §3, with CS-R5.

  The change note says so. Behaviour is unchanged: `run_views.py` gives
  31/31, and only C7's label changed.
- **Write fence.** Only the six files below and this note.

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` (FR-v0.1 + RF-5a) | c328ebfc3bbb1bd5c2efa789691be8fdc1e8f1b8f1f744448a3c0daae7d10e97 |
| DEL-06-01 `Design/prototype/fleet_store.py` | 75c07f4489a02c39aa8b8f06b6d55ce607e409b06759485343fc9cdf9f5c04d4 |
| DEL-06-01 `Design/prototype/run_fleet.py` | efb37ed4629d93f005f797032872263eca30a58e937688feaf1c29919a4f7190 |
| DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1 + FV-10, CS-R2 wording per R23-40) | eb0c6734bae5c108530215972bb1a91fd22fe1bbe876751d8c2998d8ed65d788 |
| DEL-06-02 `Design/prototype/fleet_views.py` | a187fd4f7c3ea4718b04e069c4742f789bdbc95fe0e4ab7184ab0f023da7c427 |
| DEL-06-02 `Design/prototype/run_views.py` (C7 label only) | 9c39d9bba42d2a5c666d4a0a7e5efdc970f4296f0f7dfb562dc61b8ad4fa27dc |

## Tranche-2 item: FV's connector waiting cause (FV-10), frozen for review (2026-10-04)

E-1 and E-2 are READY (RV). This unit changes only DEL-06-02's FV files.

- **What.** FV-10, the connector waiting cause (S-3; R23-34.10, R23-37.4),
  added as a row. FV keeps the label FV-v0.1, repaired in place with a
  change note.
- **Inputs, read as they are.** DEL-07-02 CFB-v0.1 §2 and
  `connector.standing.schema.json` `589f2c5da8a9b4bc…` (frozen at EU-D1).
  Each receiving record's `response_standing` and `route.account_ref`.
- **Rules applied:**
  - satisfied only if the standing supports reliance (CS-R1);
  - *unknown* if the condition is unknown (CS-R5) or the standing is
    nonconformant;
  - otherwise outstanding, with every reason and the route account;
  - a connector, or its absence, never makes anything *ready*, *done* or
    permitted (CS-R2), and connector rows change no other row.
- **Cases** (`run_views.py`, scratch copy of FX-FL1 with revision r3 and O-D's
  `RUN/D/build/records/PR-P6.json`, `PR-P3.json`, `PR-P1.json`):
  - C1: absent → waits, with the route ra:EUD1-Q1;
  - C2: adopted but stale → waits;
  - **C3: adopted and current, yet still waiting for W2** (another cause);
  - C4: adopted and current alone → ready (qualified by thr-cx);
  - C5: a stale standing altered to claim reliance → nonconformant, *unknown*;
  - C6: condition unknown → *unknown*;
  - C7: no other row changes;
  - C8: DEL-06-01's presence reading is not used.
- **Checks.**
  - `run_views.py` gives 31/31 (23 before).
  - `run_fleet.py` still gives 34/34; DEL-06-01 is unchanged.
  - The standing check uses the installed `jsonschema`, because DEL-07-02's
    schema uses `if`/`then`, which DEL-04-03's subset validator does not
    read. This is noted in `fleet_views.py`.
- **Raised, not changed** (DEL-06-01, READY; outside this instruction).
  DEL-06-01's RF-5 reads every input need by presence, so its facts call a
  connector record "satisfied". FV-10 overrides that, but another consumer
  of DEL-06-01's facts would not. I propose RF-5a in DEL-06-01's next
  revision: read connector needs by CS-R1, as FV-10 does. It is recorded in
  FV §8.
- **Write fence.** Only the three FV files and this note. O-D's records and
  DEL-07-02's files were read, not written.

| File | sha256 |
|---|---|
| DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1 + FV-10) | 095b1fc1e9034eef0328ababd1ed113cc9efd67788e9c0d48258d48e5450cf8a |
| DEL-06-02 `Design/prototype/fleet_views.py` | 581ed6c50ccb13765b52be517f430a0b5cab9ceaa17b40e8b5ba5c183f17b0f2 |
| DEL-06-02 `Design/prototype/run_views.py` | 7b207a22c515def08e322fe90ee1f405f1be2b680731cb91db441434ee6bf523 |

## E-1 READY; E-2 refrozen after RV-E2 (2026-10-03; RV confirmed READY with E2-R4). FV hashes there are superseded by the section above

This section is authoritative. Hash tables in the sections below it are
history. The E-1 table in the next section stands as RV confirmed it, except
`RECORD_SEMANTICS.md`, which changed for the R23-25 L-0 row below.

### E-2 repairs (RV-E2)

| Finding | Repair |
|---|---|
| **E2-R1 MAJOR** | The DEL-06-01 reader now reports every unread coordination-log line by number (RF-10, `logIncomplete`) and every orphaned observation, an observation of a child with no `dispatch_observed` (RF-12, `orphanChildren`, a limit). The DEL-06-02 views apply FV-8a: while a line is unread, every not-done row is *unknown* ("coordination log incomplete: line(s) ‹n› unread …", then what the readable records show), no row is *ready*, and `queueComplete` is false. The queue is also incomplete with an orphan or with no graph. A brief named in the graph but unreadable also gives *unknown*. VER-006 gains RV's probes, which lose a real record: **P1** (W8's return line truncated: queue not complete, W8 *unknown*, nothing *ready*) and **P2** (W2's dispatch line truncated: W2 *unknown*, the orphan reported). `run_fleet.py` checks RF-10 and RF-12 on the same truncation |
| **E2-R2** | RS lines are read tolerantly (RF-11): a torn line is a limit, and a decision need with no satisfying act becomes *unknown* while any RS line is unread. Checked in `run_fleet.py` (RF-11) and as **P3** in `run_views.py` (the A16's RS line truncated: no crash, W4's need *unknown*) |
| **E2-R3** | FV-4a: while an unassociated or orphaned child exists, every *ready* row names it ("a dispatch for this item may be unrecorded") and carries `readinessQualified`. The category stays *ready*, and FV-4a states why. In FX-FL1, W4 and W9 are qualified by `thr-cx` |
| **E2-R4** (after RV confirmed READY) | A qualified row is labelled **ready (qualified)**, and the qualifier is its **first** cause. `run_views.py` checks that no qualified row renders as bare *ready* (by label, or by label and first cause), and that `readinessQualified` holds exactly when the label is *ready (qualified)*. 23/23 |
| E2-N1 | FR §3.1: `enforced-by-host` is FR's own PROPOSED value, never handed from ROLE or NPTD |
| E2-N2 | FR-D1 cites HOSTING-v0.9 L783 |
| Coordinator (A16 in RS §7 L-0) | L-0 gains A16. It is lapse-evaluated as an App file and supersedes as A12 does (a later A16 on the same package; HA-11; R23-25). A correction is not a supersession. The RS-v0.10 change note names L-0 |

**Checks.**
- `run_fleet.py`: 34/34 (+2: RF-10/RF-12 and RF-11).
- `run_views.py`: 23/23 after E2-R4 (22 before it: +6 for FV-4a, queue
  completeness, P1 ×2, P2, P3).
- DEL-04-03 `run_prototype.py`: 67 PASS.
- `E/run_e.py`: 56/56.
- Same inputs: FX-FL1 `0489bc61…`, FX-DP1 `9501ef81…`.

**E-2 files and the changed RS file, current sha256:**

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` (FR-v0.1, repaired in place) | 3e3ba16c9c73f941336a626eed0e6817dfcb5943f5b35c65c78dea9d2b533d5c |
| DEL-06-01 `Design/fleet.record.schema.json` | e4dd5100b96419078532bbc1144017a39f8a041842e78c6eebb01778a2b45abe (unchanged) |
| DEL-06-01 `Design/prototype/fleet_store.py` | c88c13444b7355556e30659be17e88b58ea2fbf613a396de5bf8accb0b82bf38 |
| DEL-06-01 `Design/prototype/run_fleet.py` | eac21c3b78e239ad85873614f643a76249615eb09bc9f9ed210663996f041e79 |
| DEL-06-01 `Design/prototype/fixtures/FX-FL1/MANIFEST.sha256` | 0489bc6157e0e150e3fc080644fd5fa0f407c00bc53f4ee073c7fd79fa5d37d6 (unchanged) |
| DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1, repaired in place; E2-R4) | 15e25a24f53feb2a1704733a84c8a07ad5c7cc59509bf0aa6abe89a6f18c1b85 |
| DEL-06-02 `Design/prototype/fleet_views.py` (E2-R4) | 207de7a7b8e0720dcbdbee726cb8eadaed115112b374b269eee64d9b1f1b75d3 |
| DEL-06-02 `Design/prototype/run_views.py` (E2-R4) | dc49bff047626a287fdfe5b8a3f4d7e4d516004d61b78218c495a7531fc30724 |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` (RS-v0.10, L-0 row and change note) | 2e7afb1bb8b872c0ba30a514a034b1aa7174e63ee782505438c95d7cd78430ff |

## Unit E-1 refrozen after RV-E1 (2026-10-03; RV confirmed READY), and Unit E-2 first freeze (superseded above)

This section is authoritative. Hash tables in the sections below it are
history (E1-R6).

### E-1 repairs (RV-E1; R23-24, R23-25)

| Finding | Repair | Where |
|---|---|---|
| **E1-R1 MAJOR / R23-24** | The package file has its own shape: DEL-02-03 `$defs/decisionPackageFile` {format `chirality.decision-package`, formatVersion, packageId (`pkg:…`), actKind, subject, purpose, scope, `reservedBy` (the basis reserving the decision), alternatives each with consequences}. No recorder element and no self-hash. The act_request is the recorder's record. The mapping is stated in RS §13.6 and in the CE-4 descriptions, and implemented as DEL-02-03 `request_from_file`. New examples: `decision-package-file.example.valid.json` and `.invalid.json` (INV-PKG-1…6, including "the act_request body offered as the file"). FX-DP1's package files now validate, and each request equals the mapping of its file | EXEC schema `$defs`; RS §13.6; DECISION_VIEW §1, basis line, §7, §9; EXEC `run_all.py` |
| E1-R2 | ACT's A16 row cites AAC-v0.3 §1.2 and RS-v0.10 §6.1, HA-1, HA-11 and the package shape. §4.1 names A16 beside A15 as outside the closed list | ACT §2.1, §4.1 |
| E1-R3 | EXEC L3 reworded into separate sentences, stating that the line was corrected in place under R23-23 item 2 without a new label | `EXECUTION_COMPATIBILITY.md` L3 |
| E1-R4 | AAC §5.1 states the escapes (control characters short or `\u00xx`; everything else as itself, including U+2028/2029 and U+007F), integers (decimal; non-integers make the method undefined, so the offer is not offered), literals and key order. The FX-DP1 offer and AAC's A16 example now carry ü, ≈ and U+2028. `run_e.py` recomputes the digest with an implementation written from the text, and checks integers on the A4 example | AAC §5.1; AAC A16 examples; `run_e.py` |
| E1-R5 (note) | Not changed. actClass is not bound per kind; RV notes this predates the unit | — |
| E1-R6 | This table | — |
| **E1-R7 / R23-25 (my decision)** | A later A16 on the same package is a new decision by the person. It supersedes the earlier one for current standing, as a later established A12 does (RS L-0); both stay recorded. A correction (RS OF-5 `corrects`) fixes a mis-recording and is not a new decision. The rule is stated in the ACT A16 rows of §2.1 and §2.5, RS HA-11 and DECISION_VIEW DV-6. It is implemented in `E/decision_view.py` (RV-8, RV-9) and in DEL-06-01's decision reading (`fleet_store.py`, FR RF-6) | — |
| E1-R8 (note) | No action | — |

**Checks, all on the files as they are:**

| Check | Result |
|---|---|
| DEL-04-03 `run_prototype.py` | 67 PASS |
| DEL-02-03 `run_all.py` | 126 ok, 0 failures (118 before; +8 for the package file and the mapping). Independent `jsonschema` 4.26.0: 14 outputs valid, the invalid set rejected, the package-file valid and invalid examples as expected |
| DEL-01-04 `run_cases.py` | 159, 0 failed (its `jsonschema` cross-check agrees) |
| DEL-04-01 `validate_policy.py` | All held |
| `E/run_e.py` | 56/56 |
| FX-DP1 `shasum -c` | 6/6 OK |
| DEL-06-01 `run_fleet.py` | 32/32 |
| DEL-06-02 `run_views.py` | 16/16 |

**New FX-DP1 manifest (O-C's EP units re-run on it):**
`9501ef81b94c24b71a00c3611cbfa5b8eed2214eb575208283be4c3b46f034c5`.
- All five content files changed: both package files (new shape), the
  records (the requests now carry the mapping of the new files and their
  identities), the offer and the capture (new bound content, digest and
  non-ASCII text).
- `conversation/agent-message.txt` is unchanged.
- Record ids, thread ids, the chosen alternative (ALT-2 on PKG-1) and PKG-2's
  pending state are unchanged.

**E-1 files, current sha256:**

| File (relative to `execution/`, `PKG-*/1_Working/` dropped) | sha256 |
|---|---|
| DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.10) | 1bf0ce8e413d2b8fb3825808e3ce50bf8c56584c8b40bdb990bc81d2863525c1 |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` (RS-v0.10) | 75a32e55d443d0ee3fbf765e114dd6bb41f4f767b901c3eb4619e0f259abb234 |
| DEL-04-03 `Design/RS_RECORD.schema.json` | 44331659c01472a1e2f96de21b66d1cd05e357f6b6332756bd077228a58a7137 |
| DEL-04-03 `Design/RS_RECORD.invalid.examples.json` | 0eca6b276a0ed63fea6b711ce401375cded7b50a8abc05842b884a1655db899f |
| DEL-04-03 `Design/RS_RECORD.valid.act-log.example.jsonl` | b34997bb5168b747a9fe0c91ffa2ca8f5708c518eb1844331b65b294d3895e0a |
| DEL-02-03 `Design/EXECUTION_COMPATIBILITY.md` (L3 only) | 3add943d047bb249b7135a03fedd864ec964447bcd06cd37115a0c0f9ac2eb84 |
| DEL-02-03 `Design/checkpoint-record-entries.schema.json` (0.7) | a5271857c8bf71f67077fc52760a35d41ee0c30f8bd6d487a93d3c882308b45c |
| DEL-02-03 `Design/checkpoint-record-entries.example.invalid.json` | c214e5b00fd91095616b2eeb289e18749ba0c898b0c9f6515b3c96e61abf7a3e |
| DEL-02-03 `Design/checkpoint-record-entries.example.decision-package.valid.json` | d895f036af97f4c80472eb2a280193ad3347d6fe416a06476bdc92863969ecee |
| DEL-02-03 `Design/decision-package-file.example.valid.json` (new) | 3ea08ff575698e769784e0c4788a21c01be81020ad0a3c0534114f5c87895fbe |
| DEL-02-03 `Design/decision-package-file.example.invalid.json` (new) | b35d37c0c0b8140b8e84110e371b6fac643bccba5449040bdfcbd80d022b907c |
| DEL-02-03 `Design/prototype/run_all.py` | 0bc95d07799c5a61cd298c0dca26e25a2fed0bfe79f3d90ca8ced94fed586025 |
| DEL-02-03 `Design/prototype/README.md` | e18529e581aeeb3a7c4f37f6b1c8fa335b1267314e43fcc7b571f8fd16763107 |
| DEL-01-04 `Design/APP_ACT_CONTROL.md` (AAC-v0.3) | de39976e93500c9455c000b78363ad192fe56fd8aa87c680284f78db939acf65 |
| DEL-01-04 `Design/NATIVE_INTERACTION_RECEIVING.md` (NIR-v0.3) | aca40c0e326dae03a06fe5767c2c2e81b79600286b393bfa0dee68cc819cc6cb |
| DEL-01-04 `Design/aac.offer.schema.json` | 662083f8b569bd0ec0b954dd6c4adac0f6a3b9d7c35735b51bde5ffa53ce0e59 |
| DEL-01-04 `Design/aac.capture-evidence.schema.json` | 54af340140bb5896157348910917ebf7abcbaab839a14113cfcfa1b66b205b43 |
| DEL-01-04 `Design/aac.offer.example.valid.json` | f80957322793888d13e0c48c2cc312f91ff38b7cf6c60b622a103cb8cf7e967f |
| DEL-01-04 `Design/aac.offer.example.invalid.json` | 966fc02f9c0d5f473d2775e24ae99248a8b15f3933903b7134eafed4bcbcf0eb |
| DEL-01-04 `Design/aac.capture-evidence.example.valid.json` | e086bdafb4d24c13f24e8fecee151bd803633294adc51d43ed16fe8523528da4 |
| DEL-01-04 `Design/aac.capture-evidence.example.invalid.json` | bcc46c98a95e6e0a35fd5743510314218642f8415c786d0e2809eace7578d12e |
| DEL-06-02 `Design/DECISION_VIEW.md` (DV-v0.1) | b944b0be081a56a4796d85e9175dcfb202b50f6fa717e0e6211f8f8b5b4a206d |
| `E/README.md` | 78a4df929d6933aef30a741ac3f0a43d2a225f1064f5d43572dfeb58771cf7ed |
| `E/decision_view.py` | 6fae1738275cadf5599de98e2b06a09014b471cb3e31f34081993d44f3b2d65b |
| `E/make_fixture.py` | 6179030efed379c2e84e285c74200fd451855365ebed0bd8804cbb8eda57fe28 |
| `E/proposed_rows.json` | 9b58806a4e78efba8c03f0fd0df8d0b5140a797c7190f3d92b85a63a0532348d |
| `E/run_e.py` | 81c973de992de646aeb57ddf7b0245e972b1657ca9345cccbb9c0feb78609774 |
| `E/fixtures/FX-DP1/MANIFEST.sha256` | 9501ef81b94c24b71a00c3611cbfa5b8eed2214eb575208283be4c3b46f034c5 |

### Unit E-2 frozen for review (DEL-06-01 records; DEL-06-02 queue and waiting views)

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` (FR-v0.1; RF-6 with R23-25) | c37edc599ad775a00afcb457d77fb659319b08ebb1f8500c8db1b0b626003fa4 |
| DEL-06-01 `Design/fleet.record.schema.json` (`chirality.fleet.record` 0.1) | e4dd5100b96419078532bbc1144017a39f8a041842e78c6eebb01778a2b45abe |
| DEL-06-01 `Design/prototype/fleet_store.py` | fa9590c1c0bb99d8ad4fac38d13f30753094946807fedde0ba9a8b013b43d7c1 |
| DEL-06-01 `Design/prototype/run_fleet.py` | 5b1f6ec8368309db60a26b7e7e1a8c1b1d1b1684e1f481567c17617db4cf557e |
| DEL-06-01 `Design/prototype/fixtures/FX-FL1/MANIFEST.sha256` (9 files) | 0489bc6157e0e150e3fc080644fd5fa0f407c00bc53f4ee073c7fd79fa5d37d6 |
| DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1, with FV-2a) | 5d88a2a64ee67df5bd68c3c3aba0536633f9ff0e5585cb8f8e06420df98b0239 |
| DEL-06-02 `Design/prototype/fleet_views.py` | b79ae18361aaa380010f6a7985b13d34d3c7cf87b045f7b813e0eac485eafdcf |
| DEL-06-02 `Design/prototype/run_views.py` | d04d2c83e2f9d1aaa094cb8068db354a999d1eb488bf112eb893940a8931a8a3 |

- **Claims.**
  - DEL-06-01: the records keep selected, dispatched, observed, returned,
    reviewed and integrated facts apart, each on its own record (FR §3, §5).
  - Briefs carry the seven elements and the enforcement standing of each
    limit.
  - The App writes only what it observes, and the child index lives in
    DEL-06-01 (R23-4).
  - A related conversation or an external result is never a dispatch
    (R23-9).
  - Decision needs read RS records (R23-8, R23-25).
  - DEL-06-02 derives the queue and waiting views from those facts only,
    names no examiner the records do not give (FV-2a), and writes nothing.
- **Checks.**
  - `run_fleet.py` 32/32: VER-001…005 and 007, W-1, W-2, RF-1, RF-9 and
    INV-FL-1…7. It reads FX-DP1's records at their current manifest.
  - `run_views.py` 16/16: VER-001, 002, 005 and 006.
  - The schema loads under DEL-04-03's subset validator and passes
    `jsonschema` `check_schema`.
  - The FX-FL1 fixture rebuilds byte-identically.
- **Open:**
  - the brief reference in the spawn prompt is guidance, not enforcement
    (FR AS-1);
  - connector states wait for DEL-07-02;
  - the content-identity method is still a TEST VALUE;
  - delegation is observed only through an adapter;
  - OI-008 placement.
- **Basis note.** Decision needs use FX-DP1 at manifest `9501ef81…`; the
  results were the same at `346191ff…`.

## Unit E-1 refrozen (2026-10-03, after R23-18, R23-21 and R23-22)

**What it claims now:**
- PR-1…PR-13 are applied in their files under R23-18. PR-5 keeps its meaning
  but is written in the keyword subset that EXEC's own checker reads (`anyOf`,
  `const`, `enum`, `false`), not in `allOf`/`not`.
- The R23-18 item 2 list rows are added: RS §13.3 row, RS §6.2 HA-11, ACT §2.4,
  §9 ("decide"), §10.1 V-01 and the A9 row, and AAC §2 AI-9.
- The package file is the CE-4 body with form "decision package file"
  (R23-18 item 3).
- Every changed shared file has a new version label and a one-line change
  note:
  - RS-v0.10, ACT-POLICY-v0.10, AAC-v0.3, NIR-v0.3;
  - DEL-02-03 schema `$id` `…/proposed-0.7`.

  The AAC schemas stay at 0.3 and the RS record format at 0.1: these are
  additive rows taken in place, the RV21 and RS-v0.9 precedent. Their files
  carry the change note in their description.
- NIR (R23-22): the §5.1 `Turn.error` source line now holds at 0.158.0 and
  0.160.0 (VC Δ3), and TO-4 keeps an interrupted turn that carries an error
  interrupted. Its Codex message is shown as "Codex reported: ‹message›",
  never as the cause or as Failed. Re-pinned under R23-5.
- DECISION_VIEW adopts the A16-carrying versions (R23-21 item 3).
- `E/run_e.py` runs on the files as they are: 47/47, with the addendum's
  digest check. Every PR row is present.
  Both package `act_request` entries, the A16 `human_act`, the A16
  `act_lapsed`, the offer and the capture evidence are valid. INV-E-1…7 are
  rejected. The decision view and RV-1…RV-7 hold, and the input set is
  unchanged.
- The fixture FX-DP1 is unchanged except the offer and capture (addendum:
  offer digest); the manifest is now `346191ff…`. Its act requests are now
  valid against the files as they are, so its condition is lifted.

**Prototype counts before → after (each existing check, run unchanged except as noted):**

| Prototype | Before | After | Note |
|---|---|---|---|
| DEL-04-03 `run_prototype.py` | 63 PASS | 67 PASS, 0 fail | +INV-RS-25…28 |
| DEL-02-03 `run_all.py` | 114 ok | 118 ok, 0 fail | `run_all.py` gains the decision-package example file (2 outputs) and INV-EXEC-8…10; `--write-examples` regenerated the files, and the existing examples are byte-identical except the appended invalid cases. Third-party `jsonschema` 4.26.0 cross-check: 14 valid outputs valid, 10 invalid rejected |
| DEL-01-04 `run_cases.py` | 151 PASS | 159 PASS, 0 fail | +2 valid A16 instances, +INV-OF-17…19, +INV-CE-13…15; its own `jsonschema` cross-check (S-4) agrees |
| DEL-04-01 `validate_policy.py` | 6 PASS | 6 PASS | No ACT schema change |
| `E/run_e.py` | 39/39 (rows in memory) | 47/47 (files as they are) | — |

**Files (sha256) and changed lines (line numbers in the new file):**

| File | sha256 | Lines |
|---|---|---|
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.10) | b45cd1131ea1251128af25e02ab231db4c48e93f22de5d783d9fab6f3aa9fa05 | L2 label; L4 change note and re-pin; L334 A8; L335 A9 list; L342 A16 row; L355 list pointer; L413 §2.4 act kind; L1666 §9 "decide"; L1681 V-01 |
| DEL-04-03 `RECORD_SEMANTICS.md` (RS-v0.10) | 0d700f54d323682d439b1e44bc23dab52339873205604aa17a6c657c6e432ab2 | L2 label; L4 change note and re-pin; L520–521, L526–527, L532 §6.1 rows; L587–598 HA-11; L1043 §13.3 R9 row; L1194–1206 §13.6 bullet |
| DEL-04-03 `RS_RECORD.schema.json` | 44331659c01472a1e2f96de21b66d1cd05e357f6b6332756bd077228a58a7137 | L5, L26–27, L1288–1289, L1378–1382, L1580–1636 (unchanged since the first freeze) |
| DEL-04-03 `RS_RECORD.invalid.examples.json` | 0eca6b276a0ed63fea6b711ce401375cded7b50a8abc05842b884a1655db899f | L133–152 |
| DEL-04-03 `RS_RECORD.valid.act-log.example.jsonl` | b34997bb5168b747a9fe0c91ffa2ca8f5708c518eb1844331b65b294d3895e0a | L5 |
| DEL-02-03 `checkpoint-record-entries.schema.json` (schema 0.7) | e56d33dc3d142f848ebf716b3dd7f1e3baefe2779b51ed642d1be74eff792e96 | L3 `$id`; L5 change note; L115–116 actRef A16 (PR-13); L475–476 form (PR-2); L490–491 actKind A16 (PR-1); L542–583 alternatives, consequences (PR-3, PR-4); L585–615 the PR-5 rule |
| DEL-02-03 `checkpoint-record-entries.example.invalid.json` | 25b8d91348711f329fc44d1ccb4401ad613665b40ed4f1a2777239a8a086de81 | L122–257 INV-EXEC-8…10 |
| DEL-02-03 `checkpoint-record-entries.example.decision-package.valid.json` (new) | 2404eead1a298990ed7f553bcb2b651b0873738c03dcd3e25daa3d35c565ac67 | new |
| DEL-02-03 `prototype/run_all.py` | 2fc3605a1673adf06fb19c099d3a29cb347b07cd43127622d4e2d06c069c4413 | L315–340, L371–383, L394 |
| DEL-02-03 `prototype/README.md` | 6407bf4c61f13c006ce38ce14863b5f3b367a32c6fd19ce0dc3f0bb056430e0b | L26, L34–37 |
| DEL-01-04 `APP_ACT_CONTROL.md` (AAC-v0.3) | 03f5b1fcc838c1ee97f0f9fc7d106d0a2ff353839c09eebb30d904aa7f40a799 | L3–5 label; L8 NIR label; L16 change note and re-pin; L98 §1.2 A16 row; L123 AI-9 |
| DEL-01-04 `aac.offer.schema.json` | 662083f8b569bd0ec0b954dd6c4adac0f6a3b9d7c35735b51bde5ffa53ce0e59 | L5, L131–132, L141–142, L290–320, L580–650 |
| DEL-01-04 `aac.capture-evidence.schema.json` | 54af340140bb5896157348910917ebf7abcbaab839a14113cfcfa1b66b205b43 | L5, L149–150, L375–379, L539–580 |
| DEL-01-04 `aac.offer.example.valid.json` / `.invalid.json` | 3093812875c3be909efb4555c464604a83d2aeb48f3da6dfdc9ea3624934b3ef / 0a36776f6cbd3d82458e0c795cf372ce7d97e6e585f3421b43aa2e7bb7e89b3b | L2, L139–182 / L784–911 |
| DEL-01-04 `aac.capture-evidence.example.valid.json` / `.invalid.json` | e94ff643e51bc25eae70008a0d6169dbc3240d1f15563c86b1b382411bc41f95 / 080259493f1579b3dc757307e02e38ab51a660bd04501f4cc0849786e4f7c3e8 | L2, L146–185 / L925–1054 |
| DEL-01-04 `NATIVE_INTERACTION_RECEIVING.md` (NIR-v0.3) | aca40c0e326dae03a06fe5767c2c2e81b79600286b393bfa0dee68cc819cc6cb | L3–5 label; L7–15 change note and re-pin; L407–411 §5.1 source line; L421 TO-4 |
| DEL-06-02 `Design/DECISION_VIEW.md` | f4aa62065a48361c4ce9c888473e2bed50da8dd4939bd21d697d55b00bd1c2c3 | basis line; §7; §9 |
| `E/README.md`, `E/proposed_rows.json`, `E/run_e.py` | 82e3fe38a752fc7a4a6e05041657488b8a915d613a104aa01dd1870be2a5422e, 9b58806a4e78efba8c03f0fd0df8d0b5140a797c7190f3d92b85a63a0532348d, 6ad9d82e14497e819aa7abae4b2f74135de859455279fa4477872282219ce8f9 | — |
| `E/make_fixture.py`, `E/decision_view.py`, `E/fixtures/FX-DP1/*` | unchanged since the first freeze | — |

**Open:**
- ACT §2.5's per-kind content-binding table (the A15 row near L451) has no
  A16 row. R23-18 item 2 named §2.4, not §2.5, so I did not add one.
- `EXECUTION_COMPATIBILITY.md` still says its schemas are "v0.6, unchanged at
  v0.7"; the schema is now 0.7. That file is outside my area.
- `aac` schema format 0.3 and the RS format 0.1 are kept, as stated above. If
  you want those bumped, the AAC prototype's `act_control.py` writes
  `formatVersion` "0.3" and is outside my area.

### Addendum: offer digest (RR-E finding), included in this refreeze

- **Checked:** neither AAC nor RS named a serialization. AAC §5.1 said only
  "offer digest". The AAC prototype computes it with `nir_model.canonical()`:
  keys sorted, separators `,` and `:`, `ensure_ascii=False`, over the offer
  before `offerDigest` is added. RS selects no canonicalization (U-04).
  My fixture had used yet another serialization (Python's default
  separators, ASCII escapes), so the reader's failure was correct.
- **Named:** AAC-v0.3 §5.1 (L240–257) now states the serialization as
  `aac-offer-digest/0.1`: sha-256, lowercase hex, of the UTF-8 JSON of the
  offer without `offerDigest`, keys sorted, no whitespace outside strings,
  non-ASCII unescaped. It is not claimed to equal RFC 8785, and that was not
  checked. It is a TEST VALUE until DEL-03-01 TBD-003 / RS U-04 selects one.
  The v0.3 change note says so.
- **Applied:**
  - the fixture's offer and capture carry `{"method": "aac-offer-digest/0.1",
    "value": "c346f3ca…bff3e"}`;
  - `E/run_e.py` recomputes the digest from the offer file alone (47/47);
  - the AAC A16 example instances and their invalid cases carry the same
    digest (`run_cases.py` 159/159).
- **New hashes:**
  - `APP_ACT_CONTROL.md` 45b13f155a0c97949b60e0dfbe0c086fa5c9e9b1afcb0db1ef4f28f82a726057;
  - `aac.offer.example.valid.json` f595c2ddd30ea544106a7c18cf4df7b42e980c508c2fcaee3783a43278dbd1be;
  - `aac.offer.example.invalid.json` 94667c147987ca06dc78320243359f7d392200c84ed523d0d6c0cb02a96738f8;
  - `aac.capture-evidence.example.valid.json` f6bf269f85a2efbdae11845e6559bb1022a10f5fedc51826e938a0795fd0cdb8;
  - `aac.capture-evidence.example.invalid.json` ddcd74dd2ad891ba7d500996bdf6e4963dd63113652fa4e40d4b7cd6a1e0ef53;
  - `E/make_fixture.py` 804c81c40111ec8ed9fc0e4a67daf6c0e32bd534e9de14e1180d44de30f28ce3;
  - `E/run_e.py` 11ccd3197294374880b8adbbb78ed0ea6bd8dc5230a4d6c766c7d800b95dcd9c;
  - FX-DP1 `MANIFEST.sha256` 346191ff346ff788efec7aced9f46666fa46e5374dc288a85c69181bde928be9.

  These supersede the same files' hashes in the table above.
- **Who pins the previous fixture** (manifest `e3c8c5ea…`, offer `92d49511…`,
  capture `cc66321d…`): O-C's DEL-09-05 `DECISION_ATTRIBUTION_CASE.md`,
  DEL-09-11 `READER_METHOD.md` and `prototype/fixtures/IS-FX-DP1.input-set.json`,
  and `E/RR-E/SUPPLIED.sha256`. Under R23-21 those pins stay valid for what
  they relied on. The previous bytes are in git history.
  - The records file and the two package files are unchanged.
  - Only `aac/offer-PKG-1.json` and `aac/cap-decide-PKG-1.json` changed, and
    only in `offerDigest` and the offer's key order.
  - A reader relying on the digest adopts the new manifest.

## Unit E-2: DEL-06-01 records, then DEL-06-02 queue and waiting (in progress; not frozen while E-1 awaits review)

DEL-06-01 part, prepared 2026-10-03:

| File | sha256 |
|---|---|
| DEL-06-01 `Design/FLEET_RECORDS.md` (FR-v0.1) | bc294b1553e24a99ac9202f8fe308cc861a3d1f72cd368a2514c85c78c05187d |
| DEL-06-01 `Design/fleet.record.schema.json` (`chirality.fleet.record` 0.1) | e4dd5100b96419078532bbc1144017a39f8a041842e78c6eebb01778a2b45abe |
| DEL-06-01 `Design/prototype/fleet_store.py` | a643aeede3a09c8ab7e7c9a4b1be5e24939a66b080ee8d0940b2ce34bd5e0b21 |
| DEL-06-01 `Design/prototype/run_fleet.py` | 5b1f6ec8368309db60a26b7e7e1a8c1b1d1b1684e1f481567c17617db4cf557e |
| DEL-06-01 `Design/prototype/fixtures/FX-FL1/MANIFEST.sha256` (9 files) | 0489bc6157e0e150e3fc080644fd5fa0f407c00bc53f4ee073c7fd79fa5d37d6 |

- **Checks.** `run_fleet.py` gave 32/32: VER-001…005 and 007, the writer and
  reader limits, and INV-FL-1…7. The schema loads under DEL-04-03's subset
  validator and passes `jsonschema` 4.26.0 `check_schema`. The fixture
  builds deterministically and equals the committed copy.
- **Ordinary decisions, with reasons in FR §2:**
  - FR-D1: agents and the person write their records with ordinary file
    tools; the App writer records only what it observes. No App-offered tool,
    so HOSTING is unchanged.
  - FR-D2: the App's own versioned JSON format; the method's Markdown graphs
    are unchanged.
  - FR-D3: no path selected.
  - FR-D4: the child index is held here (R23-4).
  - FR-D5: what a delegation is (R23-9).
  - FR-D6: decision needs cite the package's RS request (R23-8).
- **Escalation:** none. No register row, no change to another owner's file.
- **DEL-06-02 part, prepared 2026-10-03:**

  | File | sha256 |
  |---|---|
  | DEL-06-02 `Design/FLEET_VIEWS.md` (FV-v0.1) | 5d88a2a64ee67df5bd68c3c3aba0536633f9ff0e5585cb8f8e06420df98b0239 |
  | DEL-06-02 `Design/prototype/fleet_views.py` | b79ae18361aaa380010f6a7985b13d34d3c7cf87b045f7b813e0eac485eafdcf |
  | DEL-06-02 `Design/prototype/run_views.py` | d04d2c83e2f9d1aaa094cb8068db354a999d1eb488bf112eb893940a8931a8a3 |

  `run_views.py` gives 16/16 over FX-FL1 and FX-DP1's RS records:
  - VER-001: queue membership only on records;
  - VER-002: waiting categories and causes;
  - VER-005: a separate process rebuilds identical views, inputs unchanged;
  - VER-006: missing inputs give limits or *unknown*, never empty or ready.

  `run_fleet.py` still gives 32/32.
- **Examiner decision (FV-2a, 2026-10-03; coordinator's constraint: no
  invented examiner).**
  - **Decision:** when no brief records a preparer, the queue row says
    "examiner not established".
  - **Why not fall back to the graph's item owner:** that owner is usually
    the executor (in FX-FL1, the TASK child). Naming the executor as the
    examiner would invent an examination owner the records do not give.
  - **Check:** a scratch variant adds a return on W9, which has no brief, and
    the row shows "examiner not established".
- **E-2 is held, not frozen** (R23-23), until RV returns on E-1.

### R23-23 follow-ups (done; part of E-1, already with RV)

- **ACT §2.5:** new A16 row at L451 (bound content: the package file's content
  identity, with the request and the chosen alternative; lapse-evaluated as an
  App file; a revised package needs a new A16). The v0.10 change note names it.
  ACT's line numbers from §2.5 down shift by one: §9 "decide" is now L1667 and
  V-01 L1682. `ACT_AND_POLICY_CONTRACT.md` sha256
  d8e7449c7364609cc7dab435bcb745accdb31dee416d39a74c0ea4b98487f268.
  `validate_policy.py`: all expectations held.
- **DEL-02-03 `EXECUTION_COMPATIBILITY.md` L3:** the stale "Beside it (v0.6,
  unchanged at v0.7)" now says the compatibility-report schema is v0.6 and the
  checkpoint-entry schema is 0.7 since pass 4 (R23-18), with the document text
  otherwise EXEC-v0.7. Only this line changed. sha256
  202a0f8f997b0cb8e0ba21f03eac8c6e69e62cc1963b81d038915db644c4865a; HEAD
  sha256 69e6e79af078980ba16d154f05b462100576908c49901634ea8d6518990a3de7. Pins of that HEAD hash (16-hex prefix search): DEL-03-04 GUIDE,
  DEL-01-01 VERSION_ADVANCE, DEL-09-02 STANDALONE_QUALIFICATION, DEL-09-07
  LOCAL_HOST_QUALIFICATION, pass-3 closeout C0 and the SCA-V4-003 closure
  manifest. Only the schema-version line changed, so those pins' reliance is
  untouched. `run_all.py`: 118 ok, 0 failures.

## Pins of the old hashes (R23-21 item 4; for the closeout; not edited)

Each heading below is a file I changed, with its sha256 at HEAD (before my
change). Under it are the files that contain that hash. The number is the
longest matching prefix found (64 = the full hash; 8 may be a coincidental
match). The search covered every tracked and untracked text file with a
script, looking for prefixes of 64, 16, 12, 10 and 8 hex characters. Paths
are relative to `execution/` with `PKG-*/1_Working/` dropped.

```text
## DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md HEAD sha256 062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7
   64  DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md
   64  DEL-01-06_macOS packaging and distribution evidence/Design/PACKAGING_AND_DISTRIBUTION.md
   64  DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md
   64  DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/EXAMINATION_PROTOCOL.md
   64  DEL-09-02_Standalone App candidate qualification/Design/STANDALONE_QUALIFICATION.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-E2.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/C1-A.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/reviews/V21b-A.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/SURVEY/S1-A.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/reviews/RV-EXP-U1.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md HEAD sha256 49e180907d39db3d5e6c7fedfaadf9d964aba57b328d84cca1f58fb1aec38ca0
   16  DEL-01-01_Stock Codex hosting and supplier contract/Design/VERSION_ADVANCE_0.160.0.md
   64  DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md
   64  DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md
   64  DEL-09-02_Standalone App candidate qualification/Design/STANDALONE_QUALIFICATION.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/G.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/reviews/V22.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.example.invalid.json HEAD sha256 2e5aa2d2caf8bc93831abd746be3f2890dcb24a3bdd749077a0ffc439a9af07e
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.example.valid.json HEAD sha256 7fe4092cbf758d657ed5f0872aa6deccb25e59ecf6b6f91301f43df32ce2c106
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.schema.json HEAD sha256 1b75bba70a9dfa6d778a7652793e37c5da5b063b955f67f1364e053d359e2a06
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.example.invalid.json HEAD sha256 54c17edc2b468a20d80c8868c5ff31f9ee332cac4df6c9b01846850991a1f9bf
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.example.valid.json HEAD sha256 24cf7c46fb41f011fe4096204a16afc3bcf546e27ce9604246c7bc59de73a0f0
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.schema.json HEAD sha256 8e6acaf1fe3a6a5481168122444eb5a6d1f305a647385d90cdb0c0cb8c919eec
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.example.invalid.json HEAD sha256 09763173be0eca98f8f03c601b369229a505500c98be27ea63d50d0f36d8785b
   12  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/RP-1.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.schema.json HEAD sha256 55c65bd83908bdd3aa69243cb75bbb33a17fde8075aa5b8548ba7cad94bbf8dd
   16  DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md
   12  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/RX.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-B.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-C.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-02-03_Workflow execution compatibility and round-trip support/Design/prototype/README.md HEAD sha256 03d53193f8ff31e466ebc89671344db24008bccc048ec1797bc44ba54f34c826
   16  DEL-01-01_Stock Codex hosting and supplier contract/Design/VERSION_ADVANCE_0.160.0.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-B.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-02-03_Workflow execution compatibility and round-trip support/Design/prototype/run_all.py HEAD sha256 3fc0d650f5cdb3c5d6adf350664164a1eb5c3e2cacf69e1d2a7ffc005dbff4ae
    8  DEL-09-06_Connected activity contract and workflow round trip/Design/CONNECTED_ACTIVITY_CONTRACT.md
   64  DEL-09-06_Connected activity contract and workflow round trip/Design/w14-result-record.example.invalid.json
   64  DEL-09-06_Connected activity contract and workflow round trip/Design/w14-result-record.example.valid.json
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-E2.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-B.md
## DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_AND_POLICY_CONTRACT.md HEAD sha256 4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229
   64  DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md
   64  DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_AND_POLICY_CONTRACT.md
   64  DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-E2.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/RV21-B.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNERS/O-C.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/SURVEY/S1-A.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md HEAD sha256 a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5
   16  DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md
   64  DEL-03-04_Host boundary and integration guide/Design/HOST_INTEGRATION_GUIDE.md
   64  DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md
   64  DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md
   64  DEL-09-07_Local host candidate qualification/Design/QUALIFICATION_DOSSIER.md
   64  DEL-09-07_Local host candidate qualification/Design/TRAFFIC_OBSERVATION_PLAN.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/C0.md
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/G.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/reviews/V22.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNERS/O-C.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/SURVEY/S1-A.md
   16  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/SURVEY/S1-C.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.invalid.examples.json HEAD sha256 d577ab6fad6edce58e931a3ba10c428614db49a0768c9d7e9a4254f15c418087
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-C.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json HEAD sha256 ea2a8ea2033b6aaed0b9c7342b59e06901af85ffbf95ce0123655a002d8c1018
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/closeout/C0.md
    8  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/reviews/V22.md
   64  _Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/INPUT_MANIFEST.sha256
## DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.act-log.example.jsonl HEAD sha256 5b34591e25051486102681083fbe1e1e59d890dcbcc28f0ccccad585651a4e51
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/F/F-E2.md
## _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/proposed_rows.json HEAD sha256 dbcc4bd54db4efff0510d94003a7b9427e49acfd7f8814017d264a6a9163ad4b
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNERS/O-A.md
## _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/run_e.py HEAD sha256 15434339d7f2eaaa2e1e5e91ad73678b72afb5228332964d2fbd88230a623167
   64  _Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNERS/O-A.md
```

Live Design-file dependents among these (the rest are run records and the
SCA-V4-003 closure manifest, which are historical):
- APP_ACT_CONTROL.md is pinned by DEL-01-06 PACKAGING, DEL-03-04 GUIDE,
  DEL-09-01 EXAMINATION_PROTOCOL and DEL-09-02 STANDALONE_QUALIFICATION.
- NIR is pinned by DEL-01-01 VERSION_ADVANCE (prefix), DEL-03-04 GUIDE and
  DEL-09-02.
- ACT is pinned by DEL-03-04 GUIDE and DEL-09-07 LOCAL_HOST_QUALIFICATION.
- RECORD_SEMANTICS.md is pinned by DEL-01-02 RECOVERY (prefix), DEL-03-04
  GUIDE and DEL-09-07 (three files).
- The EXEC schema is pinned by RECORD_SEMANTICS.md's own historical input
  line (prefix).
- EXEC `run_all.py` is pinned by DEL-09-06 CA (prefix) and its two w14
  examples.

## Fixture for O-C (DEL-09-05 VER-004; DEL-09-11 reader)

- **Path:** `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1/`
- **Manifest:** `MANIFEST.sha256` in that folder, sha256
  `346191ff346ff788efec7aced9f46666fa46e5374dc288a85c69181bde928be9` (six files;
  since the offer-digest fix. The previous manifest `e3c8c5ea…` differs only in
  the offer and capture files).
  Check: `cd …/FX-DP1 && shasum -a 256 -c MANIFEST.sha256`.
- **Frozen.** Since R23-18 every entry is valid against the files as they are
  (E-1 refreeze); the fixture bytes did not change.
- Content: PKG-1, an A16 package decided by "Engineer A" (ALT-2); PKG-2,
  pending; an agent message claiming PKG-2 was decided, which is not a record.
  All of it is invented.

## Unit E-1, first freeze (superseded by the refreeze above; kept as history)

**Claims.**
1. A16 *decide* exists as rows, per R23-8, in:
   - ACT §2.1 (with the A8 package elements and the "no canonical name" list);
   - RS §6.1 and §13.6 and `RS_RECORD.schema.json`, with its examples;
   - AAC §1.2.

   Each changed file is re-pinned under R23-5. Nothing else in those files
   changes.
2. DEL-06-02's decision view is defined (`DECISION_VIEW.md`, DV-1…DV-9) and
   derived from records and package files only.
3. The path runs end to end in the prototype `E/`:

   fixture package → `act_request` → offer at the act control → capture →
   A16 record → decision view → lapse.

   It does so with the 13 proposed rows below applied in memory. Without
   them, it fails exactly where those rows apply.

**Checks run.**
- DEL-04-03's `run_prototype.py`: 67/67 PASS, "all expectations held". The
  baseline before my edits was 63/63; the four new checks are INV-RS-25…28.
- `E/run_e.py`: 39/39 PASS.
- Fixture determinism: `make_fixture.py` rerun gives the same manifest hash.
- `shasum -a 256 -c` on the manifest: OK.
- No register row is proposed, so the reach script was not needed.

**Files and sha256.**

| File | sha256 | Change |
|---|---|---|
| DEL-04-01 `Design/ACT_AND_POLICY_CONTRACT.md` | e5bf830c0d1c30962096ffede9bdb4e29a09af25aecf024d3c5e68e11fae9d16 | L4 new header bullet (pass-4 rows; re-pin to SoW 2cd1dc9e…, G-0401-01…04 read); L334 A8 row, subject cell extended (package names alternatives and consequences); L342 new A16 row; L355 list bullet now points to A16 |
| DEL-04-03 `Design/RECORD_SEMANTICS.md` | 1068e295fa367142e2d3d7305d8277f94becbdfab6a4ba2cd7863bcf09684fac | L4 new header bullet (re-pin to SoW b8b58d67…, G-0403-01…06 read); L520 Act kind + A16; L521 Act class + A16; L526 Bound subject + package; L527 Bound content + A16; L532 Relations + A16's requestRef/alternativeChosen; L1182–1193 new §13.6 bullet "Decision packages" |
| DEL-04-03 `Design/RS_RECORD.schema.json` | 44331659c01472a1e2f96de21b66d1cd05e357f6b6332756bd077228a58a7137 | L5 description: one sentence appended; L26–27 actKindPerson + "A16"; L1288–1289 actClass + "person's act (V4-PM-04)"; L1378–1382 relation `alternativeChosen`; L1580–1636 two allOf rules (A16 requires requestRef and alternativeChosen; alternativeChosen is A16's only) |
| DEL-04-03 `Design/RS_RECORD.invalid.examples.json` | 0eca6b276a0ed63fea6b711ce401375cded7b50a8abc05842b884a1655db899f | L133–152 INV-RS-25…28 |
| DEL-04-03 `Design/RS_RECORD.valid.act-log.example.jsonl` | b34997bb5168b747a9fe0c91ffa2ca8f5708c518eb1844331b65b294d3895e0a | L5 one A16 entry |
| DEL-01-04 `Design/APP_ACT_CONTROL.md` | eca9a079f2b4ca405291a4ce665db39a447f6c7df8ed0a138521cf20951d392b | L14 new header bullet (re-pin to SoW 8434cc47…, G-0104-01…14 read); L96 new §1.2 A16 row |
| DEL-06-02 `Design/DECISION_VIEW.md` (new) | 48820640f0a3a90221c034d6e3f2ab34252fe54b00d9df6b057ba53fd0b996b6 | DV-v0.1 |
| `E/README.md` | 6a7c6001af22e3d966de2412b44349501bbe800efaa1d1478e9e9c563e5decac | new |
| `E/make_fixture.py` | ae796110b9a4616b299ca7535e597cf6e65bf0626037d8bb7d7bb21a47f1d2a9 | new |
| `E/decision_view.py` | f0f838a13aa19015d29057480a6785daa052ca0126de57b02289a3fa9ef041a8 | new |
| `E/proposed_rows.json` | dbcc4bd54db4efff0510d94003a7b9427e49acfd7f8814017d264a6a9163ad4b | new |
| `E/run_e.py` | 15434339d7f2eaaa2e1e5e91ad73678b72afb5228332964d2fbd88230a623167 | new |
| `E/fixtures/FX-DP1/MANIFEST.sha256` | e3c8c5eac3b6ab40a2b1c3ba734583dc8cbbd0eb7c056bb1afd5c3cf4e0d3b6f | new, with the six files it lists |

Pin basis (R23-3): nothing in this unit depends on a Codex fact.

**Escalation: the rows are needed in files outside my write boundary.**
`E/proposed_rows.json` states them exactly. Each adds; none narrows or
relaxes a constraint.
- **DEL-02-03 `checkpoint-record-entries.schema.json`** (first-increment):
  - States: RS `act_request` has no body of its own; it references
    `actRequest` (CE-4) there (RS §13.3; R14-1). That body has
    `additionalProperties: false`, `actKind` without A16, and `form` without
    any package form.
  - So R23-8 item 1 cannot be met in RS alone. Rows: PR-1 A16, PR-2 form
    "decision package file", PR-3 `alternatives`, PR-4 `consequences`, PR-5
    the rule tying them to that form.
  - Also PR-13: CE-10's `actRef` lacks A16, so a lapse of an A16 cannot be
    recorded.
- **DEL-01-04 `aac.offer.schema.json` and `aac.capture-evidence.schema.json`**
  (pass 3): their `actKind` has no A16 and nothing carries the alternatives
  or the chosen one (PR-6…PR-12).
- **Inference: the package file's shape.** Neither file nor R23-8 defines the
  shape of the file the agent writes. The prototype uses exactly the
  request's elements. It belongs with PR-2's form, so with DEL-02-03, unless
  you rule otherwise.

**Open items** (not changed: they are outside the authorized rows; each is a
listing or table that does not yet name A16):
- RS §13.3 table row "R9, §6".
- RS §6.2: no HA rule for A16 as HA-10 has for A15. A16's constraints are in
  the §6.1 rows and the schema.
- ACT §2.4 recorded-act table, §9 label rules ("decide"), §10.1 V-01 ("A1–A15")
  and the A9 row's act list.
- AAC §2: no AI row for the runtime value from DEL-06-02.
- DEL-04-01 SoW REQ-002 names A15 but not A16, which goes to the next
  amendment under R23-11.

**Not in this unit:** DEL-06-01 Design. Under R23-8 no PKG-06 record holds a
package; the graph's reference to a pending package comes in the next unit.
