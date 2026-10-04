# RV-LHQ-U2 — review of DEL-09-07 LHQ-U2 (traffic observation plan, dossier, schemas)

- **Reviewer.** RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- **Basis.** Rulings cited by ID: R23-14, R23-15, R23-19, R23-20, R23-21. `R23_RESOLUTIONS.md` is append-only now, current sha256 `037ce86b…`.
- **Unit.** DEL-09-07 `Design/`. All 11 files match the hashes in `OWNERS/O-C.md` ("LHQ-U2 — frozen"), checked with `shasum -a 256`:
  - `TRAFFIC_OBSERVATION_PLAN.md` (TOP-v0.1) `73fac0c0…f78a`
  - `QUALIFICATION_DOSSIER.md` (DOS-v0.1) `301e5290…e148`
  - `lhq.candidate-identification.schema.json` `194f8419…50dd`
  - `lhq.traffic-observation.schema.json` `edafac0a…2615`
  - `lhq.dossier-manifest.schema.json` `d39c1a7b…d3d7`
  - their six example files.

## Verdict: **REPAIR**

There are 2 MAJOR findings, 5 MINOR and 2 NOTE, and no BLOCKING finding.

## Findings

### U2-R1 — MAJOR — attribution gaps never reach the part outcomes, so P23-A, P23-C and P23-D can pass on traffic the capture could not attribute (TOP §3, §4 BS-1 and BS-8, §5 OV-2, §7 completeness rule; LHQ §5.4)

- **What TOP states.**
  - §7: each capture-based part "passes only if OV-1, OV-3 and OV-4 held and the window is complete". OV-2 is left out of that condition.
  - §4 BS-8 says that until OV-2 holds, "delegated traffic is 'attribution not established'". That is a recorded limit, with no effect on any part's outcome.
  - §3 sends a system process with no effective-process mark to the "System, not attributed" annex. Such an entry is "never counted as a host contact and never as 'clean'". When its timing coincides with a host action it carries the limit "possibly caused by the host, not attributed", again with no effect on outcomes.
  - LHQ §5.4, which TOP serves, makes parts *inconclusive* "if TOP's calibration did not hold". That covers all of OV-1…OV-4, so the two files disagree.
- **Why it matters (my inference, not stated by TOP).**
  - The subject set in §2.3 is the host process and the processes it starts.
  - Work done for the host by a system service is attributable only through the effective-process mark. Examples are the interface's webview network requests (OV-2 exists for this) and BS-1's background sessions and lookups. The man page states that mark only as a filter keyword (`eproc`, `epid`).
  - If the mark does not cover such traffic, host-caused contacts land in the annex. P23-C ("nothing else is contacted") and P23-A can then pass while host traffic went unexamined.
- **Accepted basis.** AC-006: "Limited or unavailable observation remains incomplete qualification". VER-006 requires accounting for "the observation boundary and any gaps". R23-15: "A partial capture is *inconclusive*, never *passed*".
- **Consequence.** The blind spots are named honestly, but the pass rule ignores them. A run with OV-2 *not held*, or with coincident annex entries, can produce a P23-C pass.
- **Repair.**
  - Make OV-2 a pass condition for P23-A, P23-C and P23-D, or limit those parts to traffic that does not depend on the effective-process mark, stated as such.
  - Make any annex entry with `possibly_caused_by_host` turn P23-C, and P23-A where its destination is not allowed, *inconclusive* unless it is resolved by evidence, such as a baseline window without the host.
  - Align TOP §7 with LHQ §5.4's "calibration did not hold".

### U2-R2 — MAJOR — the DEL-09-11 handoff can pass author content and derived views as the reader's record set (DOS §5 record-set row, DJ-1; `handoff_del_09_11.record_set`)

- **What DOS states.**
  - The record set is "each project file of the run (host run record, act records, findings, **the dossier's own records**), path and sha256".
  - The dossier's own records include the EXP case results, written by the assembler, and the review record of the examiner's reconstruction (§3).
  - DOS's own run-author list names "the dossier assembler, the examiner" as run authors.
  - DJ-1 withholds only "Harness transcripts, session stores and private memory".
- **What the schema allows.** `record_set` items are `{path, sha256}`, with no class to separate authority from derived material.
- **What DEL-09-11 requires.**
  - ScopeOfWork REQ-004: "Private agent memory, a harness transcript/session store, and a derived view … shall not become authority".
  - O-C's own receiving method, `READER_METHOD.md`, lists "the author's working memory and **derived views**" as **withheld**, and keeps `not_authority` items apart.
  - R23-6's purpose is to test "whether the files and host receipts stand on their own".
- **Consequence.** As specified, the handoff would give the week-later reader an earlier reconstruction of the same journey and the run authors' own results, so a pass would not show the files stand alone. The agent's own run summary (20-13, *agent-prepared*) has the same problem unless it is marked `not_authority`.
- **Repair.**
  - Limit the record set to the run's primary project records: the host run record, act records, findings and the receipt references.
  - Name the dossier's results, the examiner's reconstruction and review, and the agent's summary as withheld, or as `not_authority`, using DEL-09-11's input-set classes.
  - Add an item class to `record_set` and an invalid example to the schema.

### U2-R3 — MINOR — DOS pins EXP-v0.1 but relies on an element only EXP-v0.2 has (DOS header, §1, UNRESOLVED; R23-21 item 3)

- **The conflict.**
  - The DOS header pins EXP-v0.1 (`dc6b6a0c…`, result schema `7c994445…`) as "the bytes relied on" and calls the v0.2 result schema "not relied on".
  - §1's case-results rule ("Parts declared not applicable before the run are listed with their reason and left out of aggregation (R23-19)") needs `parts_not_applicable`. That element exists only in v0.2, and the header says so.
  - v0.2 also changes `format` to `EXP-v0.2`, requires `blocked_by` for every `blocked` outcome, and forbids `scenario` on non-candidate records.
- **The rule.** R23-21 item 3: "An owner that relies on the new rows … adopts the new version and says so."
- **What has changed since.** O-B has refrozen EXP-v0.2 (`fc5b8230…`), and my repair confirmation in `reviews/RV-EXP-U1.md` found it READY.
- **Repair.**
  - Adopt EXP-v0.2 and pin its bytes.
  - Close the "EXP-v0.1 is in progress" UNRESOLVED row.
  - Settle D-F1 and D-F2 against v0.2:
    - D-F1: v0.2 has `configuration.host_profile`. Its example EXP-EX-08 is an LHQ-shaped `candidate` record on route `seam_live` with `model_server.kind: local_provider`. I built a P20-A-style record with `codex_pin: not_applicable`, `home: not_applicable` and route `seam_live`, and it validates against v0.2.
    - D-F2: v0.2 adds a change kind `case_definition`.

### U2-R4 — MINOR — the applicability map reopens fewer cases than EXP's own reliance rule (DOS §2)

- **The mismatch.** In the map, "Local model server or model → LHQ-20, LHQ-23". LHQ-21 and LHQ-22 also run the embedded agent on that model. Every `candidate` EXP record carries `configuration.model` and `model_server`. EXP §6.2 rule 2 says "a result is affected if the changed thing appears in any of them". So EXP would reopen LHQ-21 and LHQ-22, while DOS calls itself "DEL-09-07's reliance map".
- **A missing row.** There is no row for a change of case definition. Under R23-19 a case definition also fixes which parts are declared not applicable. v0.2 now has the change kind `case_definition`.
- **Repair.** Derive the map from the elements each record carries, add LHQ-21 and LHQ-22 to the model row, and add a case-definition row.

### U2-R5 — MINOR — the method claim goes beyond the man page, and the blind-spot list is incomplete (TOP §2.1, §4)

I read `man tcpdump` on this machine (`col -b`). It states:
- `pktap,all` captures "packets from all interfaces, including loopback and tunnel interfaces";
- the metadata display letters N (process name), P (process ID), U (process UUID) and f (flow identifier);
- the filter keywords `eproc` and `epid`;
- the "dropped by kernel" count.

TOP's quotations are accurate. Three points go further than the manual:
- **(a) Process metadata on every packet.** §2.1 says the method "records every packet with the process that sent it". The manual does not state that every packet carries process metadata. Inbound, kernel-generated or forwarded packets are not covered by it. This is inference; there should be a blind spot for packets without process metadata, with an attribution rule for them.
- **(b) How the effective process is read.** The effective process appears only as a filter keyword, not among the `-k` display letters. How §6 extracts it per contact is not stated (for example, filtered passes with `-Q`).
- **(c) Proxied traffic.** No blind spot covers a configured system proxy or relay, where the captured destination is the proxy rather than the real destination.

**Repair.** Mark (a) as inference, add the missing blind spots, and state the extraction method.

### U2-R6 — MINOR — the traffic schema does not enforce the completeness rule its description claims (`lhq.traffic-observation.schema.json`)

- **The claim.** The description says "the completeness rule is checked against 'window'".
- **Probes** (scratch file `$TMPDIR/rv`; nothing written in the unit), each run against the valid example:
  - **T1.** OV-1 and OV-4 set to `not_held` while `window.complete` stays `true` → accepted.
  - **T2.** `calibration` listing OV-1 four times → accepted, so `minItems: 4` does not mean four distinct checks.
  - **T3.** An annex entry with `possibly_caused_by_host: true` and no matching limit → accepted. The valid example itself has that entry without the limit TOP §3 requires.
- **Repair.** Add conditionals: any calibration check other than `held` → `complete: false` with `calibration_not_held`. Require distinct checks. Require the "possibly caused by the host, not attributed" limit whenever an annex entry is flagged. Add invalid examples for each.

### U2-R7 — MINOR — declining the capture privilege is recorded as *not run*, which conflicts with R23-20 (TOP §2.1; LHQ LF-10)

- **The conflict.** TOP §2.1: "If the person declines, LHQ-23 is *not run* (LHQ LF-10)". The privilege is asked for when the capture runs (R23-14 item 1), so the case was attempted at its start and a stated precondition stopped it. That is R23-20 item 2's *blocked*.
- **Relation to LHQ-U1.** This is the same residue as LHQ-R15 in `reviews/RV-LHQ-U1.md`. Repairing LF-10 there carries over here.

### U2-R8 — NOTE — privilege handling otherwise meets R23-14

- TOP §2.1 and §5 step (2) have the person start the capture "with their own administrator authentication, at run time", and say "No agent holds or uses the person's credentials".
- The schema's `capture.privilege` requires `granted_by`, `granted_at` and `source: stated_by_person`.
- **Wording.** §2.1 says "a permission the host asks for". In this file "host" otherwise means SWBPIPE, so "the operating system asks for" would avoid ambiguity.

### U2-R9 — NOTE — what is claimed and not claimed is honest

- No capture, host observation or SWBPIPE observation is claimed. Every example is labelled illustrative or invented.
- The raw capture stays off the repository, with no payloads, and other applications are kept only as counts.
- TOP's tool facts reproduce on this machine:
  - `sw_vers`: macOS 26.6.2, build 25G83;
  - `tcpdump --version`: 4.99.1, Apple version 158, libpcap 1.10.1;
  - `ls -l /dev/bpf0 /dev/bpf1`: `crw------- root wheel`;
  - the man page text quoted above.
- The OBS-1 citation also checks out: B.5, line 322, has the ~30 ms process missed by 250 ms snapshots.
- DH-1, DH-2 and DJ-2, DJ-3 match DEL-11-03's OUT-002 and VER-002 and DEL-09-11's REQ-001 and TBD-001 as quoted.
- DOS treats EXP outcomes as consumed rather than relabelled: "nothing re-labelled here".

## What I checked and how

- **Hashes.** The 11 unit files match O-C.md.
- **O-C's schema checks, rerun (not rebuilt).**
  - `Draft202012Validator.check_schema` passes for all three schemas.
  - Each valid example validates.
  - Each of the 14 invalid examples is rejected with exactly one error, for its stated rule, under `jsonschema`.
  - Under DEL-01-01's `prototype/jsonschema_subset.py` (`errors(instance, schema)`): valid examples give 0 errors and invalid examples 1 each.
- **TOP against its sources.** I compared TOP with the man page, OBS-1 B.5, LOOP NW-9, NW-11, NW-14 and NW-16, LHQ §5.4, and R23-14 and R23-15.
- **Dossier against its sources.**
  - EXP-v0.2's result and change-impact schemas: I also checked that an LHQ-shaped record is expressible.
  - DEL-09-11 `ScopeOfWork.md` (`e4ee1a57…`), REQ-001…004.
  - O-C's `READER_METHOD.md` §input set: its withheld and `not_authority` classes, for U2-R2.

## Not checked

- No capture was run, and none was required.
- DEL-11-03 ScopeOfWork beyond the lines DOS quotes. Its pin `01773543…` matches, and DOS's three quotations each occur verbatim (grep).
- The CIR schema beyond its examples. Its CI-1 and BR-2 invalid cases behave as stated.
- EP-05 and EP-11 (O-C's early-path drafts), which are not frozen units.

## Repair confirmation (2026-10-03)

- **Bytes reviewed** (`shasum -a 256`; all match O-C.md "LHQ-U2 — repaired"):
  - `TRAFFIC_OBSERVATION_PLAN.md` `9126e9a197474f674266c93aeaea4f0b16dc8b4ed43de216981002e08b5ce208`
  - `QUALIFICATION_DOSSIER.md` `08430bb6e0029e755fdf13452d46b64aa46e98096ae1d38f4526506aa23c1659`
  - traffic schema `0b3f9fdd…` with examples `bf60f943…` and `f3a38b8b…`
  - dossier schema `0e8e8917…` with examples `4d659926…` and `8dce976d…`
  - CIR schema and examples, unchanged.
- **O-C's checks, rerun.**
  - All three schemas pass `check_schema`.
  - Valid examples: 3/3 valid under `jsonschema` and under DEL-01-01's `jsonschema_subset`.
  - Invalid examples: 19/19 rejected under both validators, each for its stated rule. My T1 is rejected with two errors from the same rule, as O-C says.
- **Further probes** (scratch only; nothing written in the unit): P1 and P2 below.

### Verdict: **CONFIRMED — READY**

No BLOCKING or MAJOR finding is open. Two new MINOR findings and one NOTE are below; none blocks.

| Finding | Status | Confirmed against |
|---|---|---|
| U2-R1 MAJOR | **Repaired** | TOP §7: every capture-based part needs all of OV-1…OV-5. This matches LHQ §5.4. P23-C fails with any unresolved flagged annex entry, and P23-A with one whose destination is outside the allowed set. BS-1, BS-8 and BS-10 state their effect on outcomes, and B-0 "resolves flags; it never adds a pass". Probe P2: OV-2 *not_run* with `complete: true` is now rejected |
| U2-R2 MAJOR | **Repaired** | DOS §5 and DJ-1 limit the record set to the run's primary records, each with a standing. Withheld as `derived_view`: the dossier's case results, the examiner's reconstruction and its review. The agent's summary appears only as `not_authority`. The schema's `withheld.kind` enum equals RRM's `withheld.kind` enum exactly. `record_set.standing` is required and excludes `derived_view`. Two invalid examples cover this |
| U2-R3 MINOR | **Repaired** | DOS pins EXP-v0.2 (`fc5b8230…`, `f7871c96…`, `b8fcb458…`, `b3294a40…`), which match O-B's refrozen files. The two v0.2 elements relied on are named: `parts_not_applicable` and `case_definition`. D-F1 is closed by `host_profile` and D-F2 by `case_definition` |
| U2-R4 MINOR | **Repaired** | The map is now derived from the elements each record carries. The model row reopens all four cases. A case-definition row is added. The dossier schema's `change_kind` enum equals EXP-v0.2's change-impact enum exactly (compared by script) |
| U2-R5 MINOR | **Repaired** | §2.1 marks the per-packet claim as inference. It states the method for reading the effective process (`-Q "epid = …"` / `"eproc = …"` passes, using the manual's filter keywords) and a flow-identifier join. BS-10 covers packets without metadata. BS-11 covers relays, checked by OV-5 |
| U2-R6 MINOR | **Repaired** | Calibration is an object requiring OV-1…OV-5 and B-0 once each. A top-level `if`/`else` forces `complete: false` with `calibration_not_held` when any OV check is not *held*. A flagged annex entry requires `limit` and `resolution`, and a `resolution_ref` when resolved. T1…T3 are invalid examples |
| U2-R7 MINOR | **Repaired** | TOP §2.1 now says *blocked* at the start, with its cause, which equals LHQ LF-10 |
| U2-R8 NOTE | **Adopted** | "the operating system asks for" |
| U2-R9 NOTE | No change needed | — |

### New items

- **U2-R10 — MINOR — the calibration order needs the host before the host is launched (TOP §5 sequence).**
  - The sequence runs "(3) … OV-5, then baseline B-0, then OV-1…OV-4. (4) Launch the host candidate."
  - OV-1 needs "one request from the host's native layer", and OV-2 "one request from the host's interface", so both need a running host.
  - This was already in v0.1 and I missed it then.
  - **Repair:** launch the host between B-0 and OV-1…OV-4, inside the capture window, and say whether calibration contacts are excluded from the LHQ-20 comparison or recorded as calibration.
- **U2-R11 — MINOR — the schema does not enforce the B-0 rule (traffic schema).**
  - Probe P1: with `calibration.B-0.outcome: not_run`, an annex entry resolved as `not_host_caused_baseline` still validates.
  - TOP §5 makes baseline resolution depend on B-0 having run.
  - **Repair:** add a conditional — `not_host_caused_baseline` requires B-0 *held* — and an invalid example.
- **U2-R12 — NOTE — duplicate enum value.** The dossier schema's `applicability.changed` enum lists `operation_binding` twice. It is harmless for validation, but should be deduplicated.
