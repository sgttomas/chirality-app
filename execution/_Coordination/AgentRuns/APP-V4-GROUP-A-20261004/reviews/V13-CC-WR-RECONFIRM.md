# V13 — independent design-source review of CC-WR-RECONFIRM

2026-10-07. Type 2 TASK reviewer for run `APP-V4-GROUP-A-20261004`, dispatched
by HELP_HUMAN (Claude Opus 5.5, Claude Code). Harness-native child, no
delegation. I did not author the proposal. Read-only on the checkout at
`b9a818d580` (branch `claude/app-v4-group-a-resume`). My only write is this
file. No commit, network, credentials, Cargo, `~/.codex` or native act. The
patch was applied only to a scratch copy made with `git archive HEAD`.

**Verdict: NOT READY for adoption.** The change follows the owner's decision.
The identity choice is right, and the ledger and schema form is sound. But
three MAJOR defects must be repaired in the patch or in the proposed consumer
text before adoption: F1, F2 and F3. Each needs only a few lines.

## Candidate and basis checked

| Item | sha256 | How checked |
|---|---|---|
| `changes/CC-WR-RECONFIRM.md` | `5d892e19339895491401ce900dcc3f3bdacd6f3149486802c0d91dc8b3568bb6` | `shasum -a 256` (matches the brief) |
| `changes/CC-WR-RECONFIRM.patch` | `5daf6889a1e92c161ea7750500a2e7cb5bcc3118804146274523c27d9b79c9b9` | as above (matches the brief) |
| WR preimage / postimage | `094602ac…6019656` → `528ad33e…4a04c3` | `git apply --check` clean; applied to a scratch copy; hashes equal the change record's |
| Schema preimage / postimage | `cfd6d3e2…7066e9` → `50c58c8a…61ad` | as above; the App resource copy also hashes `cfd6d3e2…` |
| `AGENTS.md`, `agents/AGENT_TASK.md`, `loop/LOOP_INIT.md` | `f96feb19…`, `1a13a5b0…`, `c2e88f81…` | read; "Change control" read |
| Run `OWNER_DECISIONS.md` at HEAD | `7fa0723b0576dee8796c179282dea9580ee83835bc57958921096c68d6bdeeec` | The author's basis `10258440…` is the `8c5e3156c6` version. HEAD only appends "Native journey witness launch". The relevant sections are unchanged (`git diff 8c5e3156c6 HEAD`) |
| AAC, offer and capture schemas, NIR, NIR schema, RS, RS schema, EXEC, ACT, `Dependencies.csv` | as listed in the change record | rehashed. All equal the change record's values |

Also read: WR §1–§9, §12, §15 (pre- and postimage); AAC §1.2, §3, §4.2, §4.4,
§5.1, §5.2a, §8; NIR §7; RS HA-10, R-7, `relations.priorRevision`;
`I2-SELECTION-AUTHORITY-ROUTE.md`; and the App's `workflow_library.rs`
(`review`, `lineage_reaches`, `read_ledger`, `latest`, `advance_entry`,
`fail_entry`). Commit `8d98de95a8` (J5) is an ancestor of HEAD. Only
`runtime_session.rs` differs from it under `src-tauri/src`.

## Validation run (scratch copy)

Python `jsonschema` 4.26.0, Draft 2020-12, with WD's schema registered by `$id`.
Script: `$TMPDIR/…/scratchpad/validate.py`.

- Metaschema: the postimage schema passes.
- Existing conformance files: 14/14 valid instances still validate, and 17/17
  invalid instances are still refused. The preimage gives the same result.
- DEL-04-03 `minischema.check_supported` accepts the postimage schema.
- 38 constructed cases ran: 34 with a stated expectation (0 mismatches) and 4 gap probes (G1–G4).
  - Positives, each refused by the preimage:
    - a *re-confirmed* line;
    - a *not completed* re-confirmation line;
    - a DS-8 descriptor;
    - a *re-confirmed* transition;
    - a *not completed* re-confirmation transition;
    - a DS-8 disposition.
  - Unchanged positives:
    - an ordinary *not completed* line;
    - a descriptor without a disposition;
    - DS-4.
  - Negatives, all refused:
    - `reconfirms` missing on *re-confirmed*, on *not completed* re-confirmation, on DS-8 and on a DS-8 descriptor;
    - a registration disposition on *re-confirmed*;
    - *re-confirmed* without disposition, sequence or store path;
    - `reconfirms` with an in-place entry;
    - *registered* carrying *re-confirmation* or `reconfirms`;
    - DS-2 with `reconfirms`;
    - re-confirm wording with a registration purpose, and the reverse;
    - registration wording on DS-8;
    - a registration descriptor with `reconfirms`;
    - `reconfirms` with `ledger_seq` 0, an extra key, or an identity without revision;
    - a *re-confirmed* transition without `a15_record` or `revision`.
  - Reader-only (the schema admits these, as the patch says): a `reconfirms.sequence` differing from the line's.
  - Gaps the schema admits: see F7.
- Proposed AAC adoption applied to a scratch AAC copy: see F2. The capture-evidence `oneOf` addition validates a *re-confirmed* entry outcome.

## Findings

| ID | Severity | Where | Evidence | Consequence |
|---|---|---|---|---|
| **F1** | **MAJOR** | WR postimage §4.8 RC-5 (line 226) "RB-3 (a) and (b) apply unchanged"; RC-6 G-1R (line 232) "the slot's latest is still the one bound"; schema `a15_descriptor.freshness.description` (line 794) "the slot's latest revision is still prior_revision" | RB-3 (b) (line 162) and G-1 compare the slot's latest with "the prior revision bound". RC-4 binds `relations.prior_revision` to **‹k›'s own prior** (RS: "the revision this one follows in its slot"), not to the slot's latest. Read literally, (b) fails at once for every DS-8 descriptor. For the J5 case, ‹k› is revision 1 with prior null, and "the slot is still empty" is false. The change record's statement "the slot's latest stays in `freshness.slot_latest`, as RB-3 uses it" is not what RB-3 says. `registration_disposition.prior_revision` for DS-8 (required on a review) is also not specified: is it ‹k›'s prior or the slot's latest? | A literal implementation offers DS-8 and then always withdraws it. An implementer who "fixes" this by binding `prior_revision` to the slot's latest breaks RS `priorRevision` semantics and RC-9's equality check. **Repair:** state that, for DS-8, RB-3 (b), G-1R and the `freshness` description compare the slot's latest with `freshness.slot_latest`. Name the value DS-8's `registration_disposition.prior_revision` carries. Amend the schema `freshness` description |
| **F2** | **MAJOR** | Change record, consumer row "AAC `aac.offer.schema.json`" | The proposed text widens only the top-level `wording` enum and `allOf/3`. `allOf/6` ("An a15_descriptor … wording 'register workflow revision'") still holds `"wording": {"const": "register workflow revision"}` for `descriptorKind` `a15_descriptor`. I applied the proposed edits to a scratch copy and took the valid A15 example (`offer:0009`). Its original stays valid. With the re-confirm wording and purpose, it is **refused at `allOf/6/anyOf`**. Widening `allOf/6` as well makes it valid. AAC §5.1 prose (adoption (c)) is right; only the schema text is incomplete. The App copy `src-tauri/schemas/aac.offer.schema.json` has the same rule | The "exact proposed text" for AAC would refuse every re-confirmation offer, so DS-8 cannot be offered through the act control. **Repair:** add `allOf/6`'s `wording` (an enum with both singular wordings) to the AAC offer row. Consider an AAC rule that pairs the re-confirm wording with the re-confirm purpose, mirroring WR's `a15_descriptor` rule |
| **F3** | **MAJOR** | WR postimage §6 SQ-X X-2 (line 383) "A re-confirmation attempt is never completed here: write *not completed* …"; RC-7; RC-9 (line 240) "the A15 it cites … is cited by no other ledger line" | §5.2 makes *stored* → *committed* on the G-4 append. The attempt journal therefore says *stored* if the process is lost after the *re-confirmed* line is durable but before the journal records *committed*. X-2 then writes a *not completed* line citing the same A15, unconditionally. RC-9 makes two lines citing one A15 a breach, which makes "the ledger ambiguous at that line". RC-6's "reread, never append twice" rule is in-process only; at relaunch the intended line is not held. The same applies to a *not completed* G-1R line written just before the loss. In the App, an ambiguity error stops `review` for the whole slot (`read_ledger`/`latest` return `Err`) | A crash in one window leaves a slot that can no longer be reviewed until the ledger is repaired by hand. The design's own rule causes it. **Repair:** X-2 for a re-confirmation first rereads the ledger for a line citing the attempt's A15. If one exists, it writes nothing and closes the attempt, and ‹k› is not selectable. Otherwise it writes *not completed* |
| F4 | MINOR | Change record, "Owner decision this implements": "SEAL-2 stays deferred, to be weighed at the 90% gate" | `OWNER_DECISIONS.md` (the corrected version the author cites as basis, `10258440…`) says: "HELP_HUMAN *proposed* weighing it at the 90% gate; the owner did not say so (correction from review V12 F1)". The patch does not repeat it | The change record misattributes a statement to the owner. Correct the sentence |
| F5 | MINOR | RC-1 (line 222); RC-10; G-2R/G-3R "Absent → G-2 and G-3 from the snapshot" | DS-8 keys on a *registered* ledger line, not on LS-1 standing. Take a ‹k› that is LS-4: its A15 record is missing or bound to other content, or its store bytes are absent. It is still offered "re-confirm … registered earlier", and G-2R recreates the store. §4.6 routes LS-4 to "Review to register". RS HA-10 says "a registration ledger line without a capture … is not evidence". The person's new A15 is genuine, so nothing unreviewed runs. But the statement and the review describe a registration the records do not support | Re-confirmation would quietly repair LS-4 under re-confirm wording. **Repair (integrator):** either require ‹k›'s cold-read standing to be LS-1 at review, with LS-4 keeping its own route, or disclose LS-4 in RC-10 and in the statement. Either way, say which |
| F6 | MINOR | §5.1 new rows (lines 258–261), with the existing "Review closed without an act → *draft*" and X-4 | A DS-8 review is opened from *registered, unchanged since*. If it is closed, goes stale or ends *not completed*, the draft returns to *draft*. NIR then shows "draft — not registered" for a folder whose bytes equal ‹k› and whose App base is ‹k›. The NIR adoption adds the event, disposition and display, but no accepted transitions. NIR §7 accepts "WR §5.1's (prototype `DRAFT_ALLOWED`)", and `nir_model.py` `DRAFT_ALLOWED` lacks (*registered, unchanged since*, *review shown*), (*registered, unchanged since*, *registration refused*) and (*under review*, *re-confirmed*) | The draft view becomes less truthful after any abandoned re-confirmation. The NIR prototype refuses the new transitions. **Repair:** return to *registered, unchanged since* when the review began there. Add the transitions to the NIR adoption and name NIR's prototype |
| F7 | MINOR | Schema `draft_transition` (postimage) | WR's own schema admits event *registered* with disposition *re-confirmation* (via `disposition_code`). It also admits *re-confirmed* with any `to`, with any disposition, or with none (cases G1–G4: valid; the preimage refuses them all). The proposed NIR schema rule is stricter | WR, the owning format, is looser than its receiver's restatement. **Repair:** mirror NIR's rule in WR. *Re-confirmed* ⇒ `to` *registered, unchanged since* and disposition *re-confirmation*. *Registered* ⇒ disposition not *re-confirmation* |
| F8 | MINOR | RC-7 (line 238) "The process is lost after capture and before G-4R: at relaunch SQ-X writes *not completed*" | SQ-X X-1/X-2 act only on attempts in *stored*, which is reached at G-2R/G-3R. The window from capture to report (AAC §4.2 steps 5–7, then G-0, G-1R) leaves no WR journal. AAC §4.4 holds that capture as unverified and appends nothing | Over-claim. **Repair:** "after the attempt is *stored* and before G-4R". Before that, AAC §4.4 governs and WR writes nothing |
| F9 | MINOR | ACT adoption row | ACT §2.1's A15 row gives the meaning "register a workflow; explicit registration of a reviewed draft". The adoption touches only the content and purpose cell. Re-confirmation is explicitly not registration (RC-3) | ACT's meaning for A15 would not cover one of its two uses. **Repair:** extend the meaning cell, for example "…; or re-confirmation of a registered revision for use in this App session (WR §4.8)" |
| F10 | MINOR | §4.6 LS-1 row (line 196, unchanged: "Runnable Yes; Offered Select; Refine") with the new note (line 207) and RC-2 | The note says LS-1 gives no selection after a relaunch, but the row is unchanged. U-WR-21 asks whether Refine of a non-selectable LS-1 revision is offered, yet the row already offers Refine. The App's `create_selected_draft` requires a hot selection, which is an implementation limit | The text is inconsistent, and an open question is framed as one the row already answers. **Repair:** qualify the LS-1 row ("Select in this process, RC-2; Refine"). See Q7 for U-WR-21 |
| F11 | NOTE | Change record, Decision (2): "It would also make G-2's store reservation collide with itself" | WR G-2: "Exists with identical bytes → continue (idempotent)". The App code does the same | That part of the reasoning is wrong. The decision stands on ID-1/ID-2, SP-1 and the App's series check (`latest()`: "registers revision … a second time"), which I confirmed |
| F12 | NOTE | RC-6 G-4R "As G-4: … an uncertain write keeps the intended line and rereads it" | WR G-4 says only "lock held … wait; process lost before G-4 → SQ-X". The reread rule is the App's (`Progress::Intended`, `advance_entry`) | Cite it as new WR text, or as the App's behaviour adopted, not "as G-4". Likewise "Ledger unreadable or malformed → pending" in G-1R is new text, consistent with the App's `Progress::Pending` |
| F13 | NOTE | Consumer list completeness | Other Designs name A15 *register workflow revision* only as the kind name and need no adoption, but are not listed: DEL-03-02 P §(A15 row), DEL-04-02 AS, DEL-05-01 LOOP, DEL-09-09 XT and WD `EXAMPLES.md`. Also not listed: DEL-01-04's prototypes (`act_control.py`, `nir_model.py`, `run_cases.py`), WR's own `prototype/wrproto.py` and §13, and NIR schema `allOf/0` (the *content* rule: add *re-confirmed*). WR-VC-20's schema cases are not preserved as conformance instances ("adds no instance to the two conformance files") | Add them to the list for completeness. Consider committing the WR-VC-20 schema cases as conformance instances so the evidence is replayable |
| F14 | NOTE | App adoption (`workflow_library.rs` `advance_entry`) | The App's G-1 compares the whole slot (`slot_lines(...) != e.slot`). A *re-confirmed* line from another draft would therefore fail a concurrent DS-2 attempt as "slot moved on", where WR G-1 (the latest is unchanged) would not. An older binary's `read_ledger` (`wr_validate("library_entry")`) rejects the whole ledger once a *re-confirmed* line exists | Name this in the App row: compare the slot's latest, per RC-9. The version skew is acceptable for development builds, but should be stated |
| F15 | NOTE | §6 X-2 (pre-existing) | X-2 completes a *stored* registration cold, citing the same A15. That sits uneasily with AAC §4.4/§5.2a and the I2 route ("Do not make cold ledger/capture equality the registration authority constructor"). The App implements no cold completion | Not introduced by this change. RC-7 takes the stricter reading for re-confirmation. Return to the WR owner separately |
| F16 | NOTE | RS linkage; U-WR-22 | In the RS record, a re-confirmation A15 differs from a registration A15 of ‹k› only by its free-text purpose. Act-log views (DV, `record_relations.rs`) would show a second A15 on ‹k›. `record_semantics.rs` checks correspondence only, so it stays correct | Acceptable while U-WR-22 is open. Saying so would make the "no adoption" claim for DV exact |
| F17 | NOTE | `reconfirmed_revision` on `library_entry` | `reconfirms.identity` and `reconfirms.sequence` duplicate the line's own `identity` and `sequence`, and RC-9 requires them equal. `ledger_seq` is the pointer that carries the meaning | Harmless redundancy. Keeping one shape across the disposition, descriptor and line is a reasonable choice |

## Answers to the review questions

1. **Fidelity.** Yes.
   - DS-8 arises only when content equals a *registered* ‹k› of the slot and ‹k› is not selectable in this process. DS-4 keeps the other case. Together they cover every identical-content outcome.
   - SP-3 is decided first. SP-4a matches the App's existing order (`lineage_reaches`, then DS-4).
   - The trust basis is the new act only. It is not cold replay: RC-2 and RC-8 hold nothing from disk as authority.
   - No obligation is narrowed (GC-6). DS-4's purpose, one revision per identity, is kept, because DS-8 registers nothing. RB-8, SEAL-2, AAC §4.4/§5.2a, CI-10 and I3-CUST are untouched.
   - Partial: routes for edited or removed drafts and for in-place entries are open (U-WR-21; F10).
   - F1 and F2 currently stop DS-8 working as written.
2. **Identity.** Correct. ID-2 makes the re-confirmed bytes ‹k›'s revision value. A new line *registered* with the same value would break SP-1's series and the App's `latest()` check ("a second time"). Keeping ‹k› leaves the following unchanged: SL-2, K-6 ("every run cites the revision it used"), EXEC A-1 and §6.1 *selected*/*resolved* ("equals the revision"), `selection_record`, TX-1 and RS R2. RS HA-10 is respected: there is a new A15 on unchanged bytes, and no carry-over. The store-collision part of the reasoning is wrong (F11).
3. **Ledger and schema.**
   - Well-formed and validated: the metaschema, the unchanged examples, and 38 cases.
   - The form is minimal enough (F17).
   - "Only *registered* lines form the series" leaves existing readers correct. `latest()`, sequence counting and `lineage_reaches` already filter `outcome == "registered"`. DS-4's identity check also filters *registered*.
   - Exceptions:
     - the App's whole-slot "moved on" comparison (F14);
     - schema-validating readers on older schema copies (F14);
     - the draft-transition looseness (F7).
4. **RC-2.**
   - It faithfully states the premise the owner decided on. `OWNER_DECISIONS.md` context: "Its old registration cannot be selected cold (SEAL-2 deferred)". It is also the I2 selection-authority route the App already enforces.
   - It is neither a new grant nor a new restriction on the App. It is new WR text, correctly labelled INTEGRATION.
   - Its forward clause matches HELP_HUMAN's explanation the owner accepted ("remains the fallback if SEAL-2 is adopted later").
   - Writing *not completed* at relaunch is consistent with X-2's existing not-completed branch and with AAC §4.4 (no cold upgrade). But see F3 (duplicate line) and F8 (window).
5. **Failure semantics.** These reuse AAC and the G-steps correctly:
   - stale bytes go to AX-06;
   - dismissal goes to AC-5 / *withdrawn*;
   - a late act-record write follows AAC step 6, and G-0 waits for the report;
   - when the slot moved on or the line changed, the attempt ends *not completed* citing the act;
   - an unreadable ledger leaves the attempt pending.

   The gaps are F3 (a crash after a durable append), F8 (the capture-to-report window) and F6 (the draft state after abandonment).
6. **Consumers.**
   - The listed set is right in substance. The AAC offer schema text is incomplete (F2).
   - The ACT meaning cell (F9) and NIR's accepted transitions and prototype (F6) are missing.
   - Other no-adoption Designs, prototypes and the WR-VC-20 instances are unlisted (F13). The App's G-1 comparison is not named (F14).
   - I found no other consumer that reads `library_entry` outcomes. In App code, only `workflow_library.rs` reads the ledger. The DEL-01-04 prototype's `DraftView.receive` reads `library_entry` for `a15_record`/`revision` (F13).

### Q7 — the three flagged points

- **U-WR-23 (K-6, identical bytes but no App-kept base): no owner decision is needed to adopt.** SP-4a keeps K-6 exactly as the owner wrote it ("a same-name draft with no such origin is refused with a request for a new name"). It matches the App's existing order. The question is owner-reserved only if someone proposes to *relax* K-6 for identical bytes. Recommended: do not propose that. Resolve the lost-base path through U-WR-21's Refine instead, which gives the draft an App-recorded base. Close U-WR-23 as "K-6 unchanged; route via Refine".
- **U-WR-21 (no DS-8 route when the registered draft was edited or removed, or for in-place entries): integrator call (WR owner with DEL-01-04).** WR §4.6 already offers Refine on LS-1, and nothing in RC-2 withholds Refine. The gap is the App's `create_selected_draft` requiring a hot selection.
  - Recommended: option (a). Implement Refine of an LS-1 revision from the revision store without a selection, with the base disclosed as App-recorded and frozen at review (as the I2 plan allows).
    - The draft then reviews as DS-8 by existing rules.
    - This also covers entries registered in place.
  - Defer (b), re-confirmation from the listing. It needs a draft-less descriptor form.
  - Fix F10's wording, and resolve this before the relaunch journey's interface, as the patch says.
- **RC-2 as new WR text: integrator call; accept.** It records the owner-accepted premise and the existing I2 route, labelled INTEGRATION. It neither grants cold selection nor restricts beyond current App behaviour. Make the LS-1 row and §5.4 agree with it (F10). The owner is not needed.

### Q8 — pre-existing `wrproto.py` break: confirmed

- On an unmodified `git archive HEAD` copy, `python3 wrproto.py` exits 1. The cause is `minischema.SchemaError: … RS_RECORD.schema.json #/$defs/suppliedGuidance/allOf/2: unsupported keyword 'if'`.
- DEL-04-03's own `run_prototype.py` exits 1 on the same error.
- `minischema.py` `SUPPORTED` has no `if`/`then`.
- `git log -S'"nativeTurn"'` shows the keyword entered the RS Design schema in `0a2ed81b47` (2026-10-05, "Checkpoint App v4 Group A at owner-requested pause"), carrying the CC-RS-WR-SUPPLY-FIT candidate. That candidate's own check used installed `jsonschema`, not `minischema`.
- **Owner: DEL-04-03 (RS).** Its schema now exceeds its own design validator's subset.
- Repair options:
  - restate the `if/then` as `anyOf [{not: {required: [nativeTurn]}}, {…}]`; or
  - extend `minischema` with `if`/`then`.
- The App copy `src-tauri/schemas/RS_RECORD.schema.json` should follow.
- I found it logged nowhere except the CC-WR-RECONFIRM record. It should go to `app/CONTRACT_ISSUES.md` or to DEL-04-03.

## Verdict

**NOT READY for adoption.**
- Repair F1, F2 and F3.
- Make the record correction F4.
- The integrator should take a position on F5, F6, F7, F8, F9 and F10. Each is a small text change.
- After repair, a re-review limited to the changed lines and a rerun of the scratch validation would suffice.
- The decision fidelity (Q1) and the identity choice (Q2) need no rework.

## Revision 2 re-review (2026-10-07)

Same reviewer and method: read-only, scratch copies only, no commit. The
checkout is now at `c59aaaa1b9`, which adds this review (committed at
`5b1a8260…`) and CI-23.

**Verdict: READY for adoption.** F1–F3 are repaired. F4–F10 are applied
as HELP_HUMAN ruled, and U-WR-21, U-WR-23 and RC-2 are disposed. No BLOCKING,
MAJOR or MINOR finding remains; two NOTEs follow. This covers the WR Design and
schema patch and the exact consumer text. Each consumer still adopts its own
text, and the App implementation follows (LOOP_INIT "Change control").

### Basis

| Item | sha256 | Check |
|---|---|---|
| `changes/CC-WR-RECONFIRM.md` (revision 2) | `0b3678ceef06e1b8ea672442c4ed49e0bfc84d2401dbb21a1462fb35c4799b6f` | `shasum -a 256` (matches the brief) |
| `changes/CC-WR-RECONFIRM.patch` (revision 2) | `38924fb728bcc228e2c1acab08346c7a0dbcf9670044d11c4d48b84cba28362b` | as above |
| Preimages | `094602ac…6019656`, `cfd6d3e2…7066e9` | unchanged; `git apply --check` is clean on a fresh `git archive HEAD` copy |
| Postimage WR / schema | `6bfb2277…251838` / `6f772b3b…ef51f5` | reproduced by applying the patch |

I diffed the revision 1 and revision 2 postimages (WR: 103 diff lines; schema:
52) and read every changed line, together with the revision 2 change record.

### Rerun of the scratch validation (`scratchpad/validate2.py`)

- **WR schema.** The postimage passes the metaschema. 14/14 valid and 17/17 invalid conformance instances behave as before. `minischema.check_supported` accepts it.
- **My 38 revision-1 cases.** All behave as expected, 0 mismatches. V13's gap probes G1–G4 are now **refused**:
  - G1: *re-confirmed* to *draft*;
  - G2: *re-confirmed* with *new revision*;
  - G3: *re-confirmed* with no disposition;
  - G4: *registered* with *re-confirmation*.
- **F1–F3 scenarios and new cases.** All as expected:
  - a DS-8 descriptor with `relations.prior_revision` null (‹k›'s own prior) and `freshness.slot_latest` = ‹k› is valid;
  - *re-confirmed* without `content` is refused;
  - a *registration not completed* DS-8 transition back to *registered, unchanged since* is valid;
  - the *registered* example is unchanged.
- **AAC offer adoption (1)–(4)**, applied to a scratch copy of the Design schema:
  - It passes the metaschema. 4/4 valid examples still validate and 19/19 invalid examples are still refused.
  - A re-confirmation offer built from `offer:0009` is valid. Before adoption it was refused at `allOf/6`; the F2 repair fixes this.
  - Refused as expected: re-confirm wording with a registration purpose; the reverse; re-confirm wording on the multi-entry descriptor; re-confirm wording without `descriptorKind`.
  - `offer:0009` unchanged stays valid.
- **NIR draft-transition adoption (1)–(4)**, on a scratch copy:
  - It passes the metaschema.
  - *re-confirmed* is valid.
  - Refused as expected: `to` *draft*; no `content`; *registered* with *re-confirmation*.
  - A not-completed DS-8 transition back to *registered, unchanged since* is valid.
- **Capture-evidence addition.** Unchanged from revision 1, which validated (see above).

### Disposition of V13 findings

| V13 | Revision 2 | Judgement |
|---|---|---|
| F1 MAJOR | RB-3 sentence; RC-5 reads (b) against `freshness.slot_latest`; G-1R checks that the slot's latest equals `freshness.slot_latest`; RC-4 says SP-6's prior link does not apply; `registration_disposition.prior_revision` keeps its meaning (slot's latest), stated in §8 and in the schema descriptions of `reconfirms` and `freshness`; WR-VC-19 case | **Closed.** Text, schema descriptions and the case agree |
| F2 MAJOR | AAC offer row: (3) widens `allOf/6`'s `wording`; (4) adds a wording/purpose/`descriptorKind` pairing rule; the App copy is named | **Closed.** Validated above |
| F3 MAJOR | X-2 and RC-7: reread the ledger for a line citing the A15; write nothing if one exists; otherwise *not completed*. WR-VC-19 adds the crash-after-durable-G-4R case | **Closed.** RC-9's one-line-per-act rule now holds across a process loss |
| F4 | The gate phrase is removed and the owner's words are quoted | Closed |
| F5 | DS-8 and RC-1 require LS-1 as read. DS-4 names a non-LS-1 cause. G-1R adds "act record no longer found". G-2R/G-3R never create or repair a store. RC-5 (c) and RC-10 show LS-1. WR-VC-17 adds the LS-4 case | Closed |
| F6 | §5.1 and X-4: an abandoned, stale or not-completed DS-8 review returns to *registered, unchanged since* when it began there. NIR (f) lists the transitions, and the `nir_model.py` `DRAFT_ALLOWED` entries are exact | Closed |
| F7 | WR `draft_transition` mirrors NIR: *re-confirmed* ⇒ `to`, disposition, `content`, `a15_record`, `revision`; *registered* never carries *re-confirmation* | Closed. G1–G4 are refused |
| F8 | RC-7 splits the windows. Before *stored*, WR writes nothing and AAC §4.4 governs. After *stored*, X-2 applies. G-3R marks *stored* | Closed |
| F9 | ACT meaning-cell adoption text added | Closed |
| F10 | LS-1 row: runnable or selectable in a process holding the result; Refine in any process. The §5.4 rows match RC-2 | Closed |
| U-WR-21 | Option (a) written as RF-1 in §4.6 (no selection; store recomputed; App-recorded base shown and frozen; covers revisions registered in place; LS-4 gives no draft). Option (b) deferred | Faithful to the ruling. It gives the edited/removed-draft path a DS-8 route without new authority: trust still rests on the new A15 on reviewed bytes |
| U-WR-23 | Closed: "K-6 unchanged; route via Refine (RF-1)" | Faithful. No owner question remains |
| RC-2 | Unchanged, INTEGRATION | Accepted as ruled |
| F11–F17 | Withdrawn, relabelled or recorded (F12 "new WR text, adopting the App's existing behaviour"; F13 consumers added; F14 App item and version-skew note; F15 returned to the WR owner) | Adequate |

### Remaining notes (non-blocking)

| ID | Severity | Where | Evidence and consequence |
|---|---|---|---|
| R2-N1 | NOTE | WR §4.6 LS-4 row (postimage line 199, unchanged): "Offered: Review to register" | A draft with an LS-4 revision's bytes now reviews as DS-4, citing LS-4's restore route. Re-registration through review was already refused as DS-4 before this change, so this is a pre-existing mismatch, now made explicit. The WR owner may amend the row to "Restore the record or bytes (§5.3)" when convenient. Nothing in this change depends on it |
| R2-N2 | NOTE | RC-1 / RF-1 | LS-1 "as read" (A15 record found, bytes recompute) is a cold read of App-kept files. RC-10 discloses it as "not verified in this session", and it only gates the offer; authority comes from the new A15. This is consistent with RC-2 and RC-8. Recorded so the WR-VC-16/17 implementation tests do not treat LS-1 as a trust signal |

Pre-existing and outside this change, as before: CI-23 (DEL-04-03
`minischema` `if`) and F15 (X-2's cold completion of a registration).

**Verdict: READY for adoption.**

## Adoption verification (2026-10-07)

Same reviewer, working read-only. I checked the uncommitted adoption in the
HELP_HUMAN checkout (HEAD `c59aaaa1b9`) against
`changes/CC-WR-RECONFIRM-SOURCE-ADOPTION.json` (sha256
`61f072c6a0f9809a1c0098cf116a322daf3a9b5128d0ad4c7517f2137feaa9c0`). Every
build and test ran in a scratch copy: a `git archive HEAD` with the
working-tree changes copied over, compared with `cmp`. The App's `target/`
was APFS-cloned into that copy. No commit, network, credentials or `~/.codex`.

**Verdict: ADOPTION CONFIRMED.** The adoption applies exactly the reviewed
text and nothing more. The App copies and pins are correct, and the suites
pass. Two NOTEs follow; neither blocks.

### 1. Diffs against the reviewed text

- **Scope.** `git status` shows the 16 files the adoption record lists, plus the record itself, the revision 2 change record and patch, and this review. No other file changed.
- **Hashes.** For all 16 files, the preimage (`git show HEAD:`) and the postimage equal the record's hashes.
  - WR postimages: `6bfb2277…1838` and `6f772b3b…51f5`, the reviewed values.
- **JSON schemas.** I rebuilt each reviewed proposal from its HEAD preimage, using the exact text in the change record, and compared it with the adopted file:
  - AAC offer: equal, including every description string; only `allOf/6` and the new `allOf/9` descriptions differ from the preimage.
  - AAC capture-evidence: exactly equal.
  - NIR draft-transition: exactly equal.
  - Each preimage round-trips byte for byte through indent 2 with `ensure_ascii` false, so the serialization adds no change.
- **Text adoptions.** `git diff --word-diff` shows only the proposed strings, at the named anchors:
  - AAC (a)–(d): (b) sits before "**Why record at capture"; (d) is appended to the VC-AAC-08 row.
  - NIR (a)–(f).
  - RS HA-10 (a)–(b): (b) sits after "(ACT-POLICY-v0.9 §2.1).", before "**Several entries in one act".
  - ACT (a)–(b).
  - EXEC CAP-2.
- **`nir_model.py`.** Only the five `DRAFT_ALLOWED` entries changed, as the record states. Imported, the table reads exactly as proposed. The `DraftView.receive` checks are listed as not applied (a minor prototype adoption).
- **Mirrors.** These App copies are byte-equal to their Design sources:
  - `resources/workflow_role/workspace-registration.schema.json`;
  - `schemas/aac.offer.schema.json`;
  - `schemas/aac.capture-evidence.schema.json`.
- **Pins.**
  - `SOURCE_MAP.json` changes only the workspace-registration hash, to `6f772b3b…`. All 9 rows match their source bytes and sources.
  - `manifest.json` changes only the two AAC hashes, to `34e61d5a…` and `53e4a553…`. Its IDs are unchanged and correct.

### 2. The ".;" suffix in AAC offer `allOf/6`

The adopted description reads `… wording 'register workflow revision'.; CC-WR-RECONFIRM adds …`.
This is the literal reviewed text: the proposal said to append
"; CC-WR-RECONFIRM adds …" to a description that ends in a full stop.

It is cosmetic. It is a description, not an assertion, so validation is
unaffected. **Acceptable as adopted (NOTE AV-N1).** Correcting it now would
move the file off the reviewed bytes and would need new manifest pins. Tidy it
at the next AAC schema change.

### 3. `resources/policy_standing/basis.json`

**The author is right to leave it unchanged.**
- It is an earlier TASK's basis record: role, parent, model, base commit `38bb2bc87a`, and the sources it read.
- 11 of its 26 hashes already differ from current bytes (for example `LOOP_INIT.md`). It is a historical snapshot, not a maintained pin.
- No code or test reads it.
  - `tests/policy_standing.rs` reads only `ACT_POLICY_CLASS_RECORD.valid.example.json` and `AS_SETTINGS_IN.valid.examples.json` from that folder.
  - Neither `include_str!` nor `include_bytes!` in `src` refers to it.
  - `sync.py` does not cover it.
- Updating it would falsify what that TASK read.

### 4. Suites (scratch copy of the working tree)

The cargo environment was `CARGO_HOME=~/Library/Caches/chirality-dev/cargo-home-group-a` with `CARGO_NET_OFFLINE=true`.

| Command | Result |
|---|---|
| `python3 schemas/sync.py` (verify mode) | exit 0: "6 schema resources match source bytes, hashes and declared IDs" |
| `SOURCE_MAP.json` check (script) | 9 of 9 rows: copy equals source, and the pin is correct |
| `cargo test --offline --locked --no-run` | exit 0 (64 s) |
| `cargo test --offline --locked --lib -- workflow` | 126 passed, 0 failed |
| `… --lib -- schema` | 9 passed, 0 failed |
| `… --lib -- a15` | 7 passed, 0 failed |
| `… --lib -- record` | 34 passed, 0 failed |
| `… --lib -- act_control` (each matching binary) | all passed: 1+1+1+1 and 24 (1 ignored) |
| `cargo test --offline --locked --test policy_standing --test workflow_catalog --test workflow_receiving --test workflow_role` | exit 0; `policy_standing` 22 passed |

The library compiles the adopted schema resources in, so the `workflow`,
`schema`, `a15` and `record` subsets exercise the new copies. I did not repeat
the full suite or `npm test`. The adoption record reports 681 passed and 3 of 3,
with log hashes.

**NOTE AV-N2.** The DEL-01-04 prototype `run_cases.py` exits 1 both before
and after adoption. It fails on the same RS `minischema` `if` error (CI-23),
so the prototype run does not exercise the `nir_model.py` change. That is
pre-existing and tracked as CI-23; it is not caused by this adoption.

**Verdict: ADOPTION CONFIRMED.**
