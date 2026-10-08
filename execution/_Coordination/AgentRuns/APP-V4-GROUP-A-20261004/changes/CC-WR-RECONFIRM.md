# CC-WR-RECONFIRM — re-confirming a registered revision after relaunch (proposed named WR change)

2026-10-07. Type 2 TASK, DEL-02-02 WR design-change author for run
`APP-V4-GROUP-A-20261004`. Dispatched by HELP_HUMAN (Claude Opus 5.5, Claude
Code); harness-native child, no delegation. Write fence: this record and
`CC-WR-RECONFIRM.patch` beside it. No Design, schema, code, register or
`Dependencies.csv` file was changed. No commit, network, Cargo, native act or
sign-in.

**Status: PROPOSED, revision 2.** Revision 2 repairs the findings of review V13
(`reviews/V13-CC-WR-RECONFIRM.md`, sha256
`5b1a8260816c19496a7af3c23b0cd810a89924e36717f034a31149790d837df7`; NOT READY)
and applies HELP_HUMAN's integrator rulings. Adoption needs a re-review of the
changed lines, then the WR owner's application of the patch and each consumer's
own adoption (LOOP_INIT "Change control").

## Owner decision this implements

`OWNER_DECISIONS.md`, "Rerunning an unchanged workflow after relaunch —
2026-10-07". The owner answered **"A15 re-confirmation now (Recommended)"**.
Recorded effect: "A named, reviewed WR design change lets a new genuine A15
re-confirm identical bytes after the original in-process registration is gone.
Trust rests on the new act, not on a replay."

SEAL-2 stays deferred under the owner's earlier words, **"Keep SEAL-2 deferred;
continue other work"** (2026-10-05). The decision approves no signing,
credentials or downloads. Problem statement: `app/CONTRACT_ISSUES.md` CI-21 (b).

## Proposal

- PROPOSAL: Re-confirm a registered LS-1 revision for use after its in-process registration result is gone
  - Evidence: WR §4.1 SP-4 DS-4 ("Identical to revision ‹k›; select it instead"); WR §2.1, ID-1, ID-2, SP-1, SL-1, SL-2, §4.6 LS-1/LS-4; RS §6.2 HA-10; AAC §4.2, §4.4, §5.2a; owner SEAL-2 deferral (2026-10-05) and owner decision (2026-10-07); CI-21 (b); HELP_HUMAN rulings on V13 (2026-10-07).
  - Change: apply `CC-WR-RECONFIRM.patch` to `WORKSPACE_AND_REGISTRATION.md` and `workspace-registration.schema.json`.
    - Design text:
      - DS-8 *re-confirmation*, for an LS-1 revision only.
      - DS-4 extended to cover a revision that is not LS-1, stating its exact cause.
      - SP-4a, the order of the checks.
      - RF-1, Refine without a selection.
      - New §4.8 RC-1…RC-10.
      - Notes in RB-3, RB-4 and RB-8, the §4.6 LS-1 row and note, §5.1–§5.4, SQ-R, SQ-G, SQ-X X-2 and X-4, §7, §8 and §9.
      - Verification rows WR-VC-16…WR-VC-20, open item U-WR-21 (deferred), and U-WR-22 and U-WR-23 (U-WR-23 closed).
    - Schema:
      - `$defs/reconfirmed_revision`.
      - A re-confirmation form of `registration_disposition`, `draft_transition`, `a15_descriptor` and `library_entry`.
      - An amended `a15_descriptor.freshness` description.
  - Why: after a relaunch an unchanged registered workflow cannot run. Cold selection is held under SEAL-2, and DS-4 refuses identical bytes. The owner chose a new genuine A15 as the remedy.
  - Risk: each consumer must adopt its own text (below) before the App can offer DS-8. Until then the App keeps DS-4 and CI-21 (b) stands. Version skew (App item F14): an App binary built before adoption refuses a ledger that holds a *re-confirmed* line.
  - Status: PROPOSED

The patch tags its text "CC-WR-RECONFIRM" in place, as the WR file does for its
in-place changes (TX-4 "CC-WR-TEXT-METHOD-ADOPTION"; §16.8
"CC-WR-RECORD-PUBLICATION"). It adds a row to "Changes from v0.1" and keeps the
schema `$id` (`…:WR-v0.2`).

## What the change specifies (brief items 1–7)

1. **When it is offered (RC-1, RC-2, SP-4a).** Re-confirmation is offered on review of a **draft** when all of these hold:
   - SP-3 holds for the slot. K-6 is checked first and is unchanged.
   - The reviewed content equals a *registered* revision ‹k› of the slot.
   - ‹k› has **LS-1** standing as read: its A15 record is found with the same bound content, and its store bytes recompute.
   - ‹k› is not selectable in this App process. "Selectable in this process" means the App holds, in memory, the result of ‹k›'s registration (G-4) or re-confirmation (G-4R) from an A15 captured in this process.

   DS-4 stays in force while ‹k› is selectable in this process, or while ‹k› is not LS-1. In the second case DS-4 states ‹k›'s standing and exact cause, and LS-4's route applies: the record or bytes are restored (§5.3), after which DS-8 applies. Only one draft per act may be re-confirmed. A draft with ‹k›'s bytes can be made by Refine without a selection (RF-1), also for a revision registered in place. Re-confirmation from the listing is deferred (U-WR-21).
2. **The act (RC-3, RC-4).** It is a genuine A15 at DEL-01-04's act control, captured only from the person's native event and bound to the reviewed bytes. Its wording is "re-confirm workflow revision for use", and its statement reads, in substance: "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." The act records a **re-confirmation of revision ‹k›** in the ledger. It creates **no new revision identity** (see Decision (2)).
3. **Ledger and records (RC-6, RC-9, §8).**
   - **Ledger line.** A new `library_entry` outcome *re-confirmed*, with disposition *re-confirmation* and a required `reconfirms` {identity, `ledger_seq`, `sequence`} naming ‹k›'s registered line. Its identity, sequence, prior revision and store path are ‹k›'s. It cites the **new** A15 record and capture evidence.
   - **Failed attempt.** A re-confirmation that does not complete is written *not completed* with disposition *re-confirmation*.
   - **RS A15 record.** The shape is unchanged. Subject ‹k›, content ‹k›'s identity, `reviewedDraft` this draft, `priorRevision` ‹k›'s own prior, and the re-confirm purpose.
   - **Freshness and the review's prior.** The slot's latest at review is carried in `freshness.slot_latest`, and RB-3 (b) and G-1R compare against it (RC-5). `registration_disposition.prior_revision` keeps its meaning for every review: the slot's latest at review.
   - **Selection.** G-6R makes ‹k› selectable **in this process only**. Nothing rebuilds that from disk, and the earlier act and receipt are never made trusted (RC-2, RC-8).
4. **Failure behaviour (RC-5, RC-6, RC-7, X-2).** These reuse G-0…G-4, RB-3 and RB-8.
   - Bytes changed between review and act: AX-06, nothing captured.
   - The control closed or dismissed: the attempt is withdrawn, nothing captured.
   - The act record cannot be written: AAC writes it late.
   - After capture, the attempt ends *not completed*, citing the act, when:
     - the slot moved on;
     - the registered line changed;
     - the act record is no longer found;
     - ‹k› became selectable;
     - the store no longer recomputes. A re-confirmation never creates or repairs a store.
   - The ledger cannot be read: the attempt stays pending with its cause.
   - The process is lost before the attempt is *stored*: AAC §4.4 governs, and WR writes nothing.
   - The process is lost after *stored*: at relaunch, X-2 first rereads the ledger for a line citing the A15. If one exists, X-2 writes nothing; otherwise it writes *not completed*. One act never gets two lines, and the attempt is never completed cold.
   - An abandoned DS-8 review that began from *registered, unchanged since* returns there.
5. **What it is not (RC-8, §9).**
   - It is not cold replay and does not satisfy CI-10 or I3-CUST.
   - SEAL-2 and AAC §4.4/§5.2a are unchanged.
   - It never carries an earlier A15 to other content.
   - If a custody mechanism such as SEAL-2 is adopted later, revisions whose standing it verifies are selectable cold and DS-4 applies to them. Re-confirmation stays the fallback (RC-2).
6. **Consumers.** See "Consumers and propagation".
7. **Verification.** Five rows are added:
   - **WR-VC-16:** re-confirm after relaunch and run, including the Refine draft.
   - **WR-VC-17:** a selectable revision, or an LS-4 revision, gets DS-4.
   - **WR-VC-18:** changed bytes take the ordinary route.
   - **WR-VC-19:** dismissal, staleness and loss have no effect. Covers `slot_latest` freshness, the capture-to-*stored* window, a crash after a durable G-4R, and the return to *registered, unchanged since*.
   - **WR-VC-20:** the ledger series accepts re-confirmation lines; schema and reader negatives.

## Decision (2): re-confirm ‹k›, no new revision identity

Chosen: the act **re-confirms revision ‹k›**. Its subject is ‹k›'s full tuple
as ‹k›'s registered line records it. The ledger records that act. No tuple,
revision, sequence, store folder or published copy is created. Sources:

- WR §2.1 *Revision* says the App numbers revisions "1, 2, … (the *sequence*, a display aid; identity is the revision value)". WR ID-2 says "the revision registered from a draft equals the reviewed draft content identity". Identical bytes therefore give ‹k›'s revision value again. A "new revision" would carry ‹k›'s identity a second time under another sequence, and the tuple (ID-1) could not tell the two apart.
- WR SP-1 says "A slot holds a series of registered revisions. The App never overwrites or deletes a revision". DS-4 already keeps one revision per identity.
- K-6 (WR §1) says "every run cites the revision it used". WR SL-2 says "A selection stays on its revision". EXEC A-1 says the selection is "the person's explicit choice of a registered revision". EXEC §6.1 *resolved* says the content "**equals the revision**". Keeping ‹k› therefore leaves `selection_record`, the run text (TX-1) and RS R2 *selected* unchanged, and EXEC needs no change there.
- RS HA-10 says "A changed definition is a new revision and needs its own A15; an earlier A15 never carries over." Re-confirmation is a new A15 on unchanged bytes, so neither half is touched.

No source forbids keeping the identity. The alternative, a second *registered*
line with the same revision value, breaks SP-1's series and the App's series
check ("registers revision … a second time", `workflow_library.rs`
`latest()`). Revision 1 also claimed that G-2's store reservation would collide
with itself. That was wrong: WR G-2 treats existing identical bytes as
idempotent ("Exists with identical bytes → continue"). The claim is withdrawn
(V13 F11).

## Decision (3): ledger line, RS linkage, freshness and in-process selection

- **New outcome, not a new record kind.** `library_entry` gains outcome *re-confirmed*, disposition *re-confirmation* and `reconfirms`. One record kind keeps the ledger a single append-only list. Schema rules:
  - `reconfirms` is present exactly when the disposition is *re-confirmation*;
  - a *registered* line keeps its three dispositions;
  - a re-confirmation is of a `reviewed_draft`.
- **Series reader (RC-9).** Only *registered* lines form the series; the App's `latest()` already filters `outcome == "registered"`.
  - A *re-confirmed* line must cite an earlier registered line of the same slot, with equal identity, sequence, prior and store path.
  - Its A15 is cited by no other line (RB-8; RS HA-10).
  - X-2's reread keeps this true across a process loss (V13 F3).
- **RS linkage.** `act.record_id` and `act.capture_evidence` cite the new A15. The A15's `priorRevision` is ‹k›'s own prior, because RS defines it as "the revision this one follows in its slot (K-6)". RS's `purpose` is free text, so RS needs a text adoption only.
- **Freshness (V13 F1).** For DS-8 the descriptor's `relations.prior_revision` is ‹k›'s own prior, not the slot's latest. SP-6's prior link does not apply, because a re-confirmation follows nothing. RB-3 (b) and G-1R therefore compare the slot's latest with `freshness.slot_latest`; the schema's `freshness` description now says so. `registration_disposition.prior_revision` keeps its ordinary meaning, the slot's latest at review. ‹k› is named in `reconfirms`.
- **In-process selection only (RC-2; INTEGRATION, accepted by HELP_HUMAN).** This follows the owner's "Keep SEAL-2 deferred; continue other work" (2026-10-05) and AAC §5.2a ("After restart, an unverified capture/pending file cannot authorize a new act append"). `I2-SELECTION-AUTHORITY-ROUTE.md` gives the same rule ("Do not make cold ledger/capture equality the registration authority constructor"). The result exists only in memory; a *re-confirmed* line read cold is an ordinary record.

## Consumers and propagation (exact proposed text; each owner adopts)

Register rows are named only, not changed. In DEL-02-02 `Dependencies.csv`
(sha256 `a97be837…6c62`):

| Rows | Other side |
|---|---|
| DEP-02-02-013, DEP-02-02-021 | DEL-01-04 |
| DEP-02-02-016 | DEL-04-01 |
| DEP-02-02-017, DEP-02-02-024 | DEL-04-03 |
| DEP-02-02-015, DEP-02-02-022 | DEL-02-03 |
| DEP-02-02-018 | DEL-09-02 |
| DEP-02-02-023 | DEL-09-06 |

On the offer side, the WR header names DEP-01-04-009 and DEP-02-03-010.

| Consumer | Adoption | Exact proposed text |
|---|---|---|
| **WR** (DEL-02-02) Design and schema | Yes | `CC-WR-RECONFIRM.patch` |
| **AAC** `APP_ACT_CONTROL.md` (DEL-01-04) | Yes | (a) §1.2 A15 row, "Wording shown": after `"register workflow revisions" (from WR's `a15_multi_descriptor`, L-4; R21-3)` add `; "re-confirm workflow revision for use" (from WR's `a15_descriptor` with disposition *re-confirmation*, WR §4.8 RC-4; CC-WR-RECONFIRM)`. (b) §4.2, new paragraph before "**Why record at capture": "**Re-confirmation (CC-WR-RECONFIRM; WR §4.8).** Steps 1–8 apply unchanged to an `a15_descriptor` with disposition *re-confirmation*. The offer carries the descriptor's wording "re-confirm workflow revision for use" and its purpose; its one entry's subject is the registered revision ‹k› and its prior revision is ‹k›'s own. The native confirmation states, in substance: "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." At step 8 DEL-02-02 reports *re-confirmed* with ‹k›, or *registration not completed* with its cause. The capture is new evidence of the person's act; it makes no earlier capture or record trusted, and §4.4 and §5.2a are unchanged." (c) §5.1, the sentence ending `the wording "register workflow revision";` becomes `the wording "register workflow revision", or "re-confirm workflow revision for use" when WR's descriptor re-confirms a registered revision (WR §4.8; CC-WR-RECONFIRM);`. (d) §8 VC-AAC-08, append: "; a re-confirmation descriptor (WR §4.8) offered with its wording and statement, captured, recorded, outcome *re-confirmed* (CC-WR-RECONFIRM)" |
| AAC `aac.offer.schema.json`: the Design copy, and the App copy `app/src-tauri/schemas/aac.offer.schema.json` (byte-identical) | Yes (revision 2: F2) | (1) `properties.wording.enum`: add `"re-confirm workflow revision for use"`. (2) `allOf/3`, the A15 branch's `wording.enum` `["register workflow revision", "register workflow revisions"]`: add the same value. (3) `allOf/6` (a15_descriptor), second branch: replace `"wording": {"const": "register workflow revision"}` with `"wording": {"enum": ["register workflow revision", "re-confirm workflow revision for use"]}`, and append to its description "; CC-WR-RECONFIRM adds 're-confirm workflow revision for use' for WR's re-confirmation descriptor". (4) Append to `allOf`: `{"description": "CC-WR-RECONFIRM: the re-confirm wording goes with a re-confirm purpose and an a15_descriptor, and a re-confirm purpose with the re-confirm wording (WR §4.8 RC-4).", "anyOf": [{"properties": {"wording": {"not": {"const": "re-confirm workflow revision for use"}}, "purpose": {"not": {"enum": ["make it available again in this App session from the project library", "make it available again in this App session from the user library"]}}}}, {"required": ["descriptorKind"], "properties": {"wording": {"const": "re-confirm workflow revision for use"}, "purpose": {"enum": ["make it available again in this App session from the project library", "make it available again in this App session from the user library"]}, "descriptorKind": {"const": "a15_descriptor"}}}]}` |
| AAC `aac.capture-evidence.schema.json` (and its App copy) | Yes | In `properties.entries.items.properties.outcome.oneOf` add `{"type":"object","required":["registration","revisionIdentity"],"additionalProperties":false,"properties":{"registration":{"const":"re-confirmed"},"revisionIdentity":{"type":"string","minLength":1}}}` |
| **NIR** `NATIVE_INTERACTION_RECEIVING.md` §7 (DEL-01-04 draft view) | Yes (revision 2: F6) | (a) `event` row: after `*registration not completed*` insert ` · *re-confirmed* (CC-WR-RECONFIRM)`. (b) `disposition` row: append `; *re-confirmation* (DS-8, WR §4.8)`. (c) `a15_record` row: "For *registered* and *registration not completed*" → "For *registered*, *registration not completed* and *re-confirmed*". `revision` row: "For *registered*: the revision identity" → "For *registered* and *re-confirmed*: the revision identity (for *re-confirmed*, the re-confirmed revision's own; no new revision)". (d) Display table, new row: `\| *registered, unchanged since*, reached by *re-confirmed* \| "re-confirmed as ‹revision› for use in this App session by ‹person› (identity not verified) at ‹t›; registered earlier (not verified in this session)", citing the new A15 record \|`. (e) "Refused by the view": add "*re-confirmed* when neither the transition nor `library_entry` gives the A15 record and the revision; *re-confirmed* for content other than the reviewed content". (f) After "**Accepted transitions** are WR §5.1's (prototype `DRAFT_ALLOWED`)" add: "CC-WR-RECONFIRM adds: *registered, unchanged since* → *under review* (*review shown*, DS-8); *registered, unchanged since* → *registered, unchanged since* (*registration refused*, DS-3 or DS-4); *under review* → *registered, unchanged since* (*re-confirmed*; *registration not completed* or *review stale* of a DS-8 review begun there); *under review* → *draft* (*registration not completed* of a DS-8 review begun at *draft*)." |
| NIR `nir.draft-transition.schema.json` (0.2) | Yes (revision 2: corrected) | (1) `properties.event.enum`: insert `re-confirmed` after `registration not completed`. (2) `properties.disposition.enum`: add `re-confirmation`. (3) `allOf/0` (content rule): add `re-confirmed` to the event list `["written", "changed", "review shown", "registered"]`. (4) Append to `allOf`: `{"description": "CC-WR-RECONFIRM (WR §4.8): 're-confirmed' ends in 'registered, unchanged since' with disposition 're-confirmation' and names the A15 record and the re-confirmed revision; it registers no new revision.", "anyOf": [{"properties": {"event": {"not": {"const": "re-confirmed"}}}}, {"required": ["disposition", "a15_record", "revision"], "properties": {"to": {"const": "registered, unchanged since"}, "disposition": {"const": "re-confirmation"}}}]}`. The existing `allOf/1` already keeps *registered* off *re-confirmation*. (Revision 1 asked to "extend the C-02 `a15_record`/`revision` conditions"; the NIR schema has no such conditions, so that text is withdrawn.) |
| NIR prototype `prototype/nir_model.py` (and `run_cases.py` cases) | Yes, minor | Add to `DRAFT_ALLOWED`: `("registered, unchanged since", "review shown"): {"under review"}`, `("registered, unchanged since", "registration refused"): {"registered, unchanged since"}`, `("under review", "re-confirmed"): {"registered, unchanged since"}`. Widen `("under review", "registration not completed")` to `{"draft", "registered, unchanged since"}` and `("under review", "review stale")` to `{"changed since review", "registered, unchanged since"}`. In `DraftView.receive`, apply the *registered* checks (`a15_record` `rec:`, `revision`, content equal to the reviewed content) to *re-confirmed* as well. Add a display word for *registered, unchanged since* reached by *re-confirmed* |
| AAC prototype `prototype/act_control.py` (and `run_cases.py`) | Yes, minor | Accept the re-confirm wording and purpose for an `a15_descriptor` with disposition *re-confirmation*, and the capture outcome *re-confirmed* |
| **RS** `RECORD_SEMANTICS.md` HA-10 (DEL-04-03) | Yes, text only | (a) "Written only from capture evidence of the person's explicit registration at" → "Written only from capture evidence of the person's explicit registration, or re-confirmation (WR §4.8; CC-WR-RECONFIRM), at". (b) After "(ACT-POLICY-v0.9 §2.1)." insert: "**Re-confirmation (CC-WR-RECONFIRM; WR-v0.2 §4.8).** An A15 composed from a WR descriptor with disposition *re-confirmation* re-confirms a registered revision for use in the App session that captured it: bound subject that revision; bound content its identity; relations the reviewed draft and that revision's own prior revision (or none); purpose "make it available again in this App session from the project library" or "… from the user library". It registers no new revision. It is new capture evidence of the person's act; it makes no earlier A15, capture or record trusted, and §14.1a and R-7 are unchanged." No `RS_RECORD.schema.json` change. Optional structured relation: U-WR-22 |
| **ACT** `ACT_AND_POLICY_CONTRACT.md` §2.1 A15 row (DEL-04-01) | Yes, text only (revision 2: F9) | (a) Meaning cell: `register a workflow; explicit registration of a reviewed draft` → `register a workflow; explicit registration of a reviewed draft; or re-confirmation of a registered revision for use in this App session (WR §4.8; CC-WR-RECONFIRM)`. (b) Content/purpose cell: after `for several entries: "make them available …", wording "register workflow revisions", WR ME-3)` add `; to re-confirm a registered revision for use in this App session: wording "re-confirm workflow revision for use", purpose "make it available again in this App session from the project library" or "… from the user library"; no new revision (WR §4.8; CC-WR-RECONFIRM)` |
| **EXEC** `EXECUTION_COMPATIBILITY.md` (DEL-02-03) | Yes, CAP-2 wording only | CAP-2: `from v0.7 "register workflow revision" for A15, or "register workflow revisions" when one act registers several entries, K-8, L-4)` → `from v0.7 "register workflow revision" for A15, or "register workflow revisions" when one act registers several entries, K-8, L-4, or "re-confirm workflow revision for use" when one act re-confirms a registered revision for use in this App session, WR-v0.2 §4.8, CC-WR-RECONFIRM)`. **No change** to A-1, T-1, §6.1 *selected*/*resolved* or `selection_record` receiving: the identity is unchanged |
| WR prototype `prototype/wrproto.py` and WR §13 | Minor, when the prototype runs again (CI-23) | Model DS-8, RF-1, G-1R…G-6R, X-2's reread and the RC-9 reader. The WR-VC-20 schema cases may be added as conformance instances to make the evidence replayable. That changes the instance counts §8 states, so it is left to the WR owner |
| GUIDE (DEL-03-04 M5.1); CA (DEL-09-06); PANEL (DEL-05-02); WD (DEL-02-01 OS-2 and `EXAMPLES.md`); P (DEL-03-02, A15 row); AS (DEL-04-02); LOOP (DEL-05-01); XT (DEL-09-09) | No | They name A15 *register workflow revision* only as the kind, or with its relations. Both are unchanged, and re-confirmation is an App-side WR disposition. Their text stays true |
| DV (DEL-06-02) and the App's act-log views (`record_relations.rs`) | No | An act-log view shows a re-confirmation as a further A15 on ‹k›, told apart from the registration only by its purpose. That is acceptable while U-WR-22 is open. `record_semantics.rs` checks correspondence only and stays correct |
| Group B packaging (DEL-01-06 PKG P-2) | No | It reads bundled workflows and the shipped-revision manifest (WR §3; LS-5, LS-8), not the registration ledger |
| DEL-09-02 qualification (DEP-02-02-018) | Notice only | The §12 case inventory gains WR-VC-16…WR-VC-20 |
| **App code** (`projects/chirality-app-v4/app/`, J5 lineage) | Yes, after the Design adoptions | See "App implementation items" below |

### App implementation items

- **Schema resources.** Update `src-tauri/resources/workflow_role/workspace-registration.schema.json` and its `SOURCE_MAP.json` hash. Update the AAC and NIR schema copies through `src-tauri/schemas/manifest.json`.
- **`src-tauri/src/workflow_library.rs`:**
  - `review_draft`: DS-8 when no result is held and ‹k› is LS-1; DS-4 with the cause otherwise.
  - `compose_descriptor`: the re-confirm form, with `freshness.slot_latest`.
  - The G-1R…G-6R attempt. A re-confirmation never creates a store.
  - The RC-9 checks in `read_ledger` and `latest()`.
  - The X-2 reread; no cold completion.
- **Whole-slot "moved on" comparison (F14).** `advance_entry` compares the whole slot (`slot_lines(...) != e.slot`). It must ignore *re-confirmed* lines and compare the slot's latest, per RC-9 and G-1. Otherwise a concurrent DS-2 attempt fails as "slot moved on".
- **Refine without a selection (RF-1).** Add a successor to `runtime_session.rs` `create_selected_draft`. It copies from the revision store of an LS-1 revision without a hot selection, after recomputing the bytes. It records the App-kept base, which is shown and frozen at review. It also covers revisions registered in place.
- **`src-tauri/src/workflow_workspace.rs`:** `Review::open` DS-4; the descriptor JSON wording, purpose and freshness; `RegisteredRevision` built from a re-confirmation citing the new act.
- **`src-tauri/src/runtime_session.rs`:** `WorkflowReviewContext.registered`, `select_hot_registered_copy`, and the listing text "registered — re-confirm to use in this App session".
- **`act_control_a15.rs`, `act_control.rs`, `a15_native.rs`:** the wording, the statement and the outcome *re-confirmed*.
- **`src/App.tsx`:** the DS-8 offer and its display.
- **`src-tauri/src/workflow_library_tests.rs`, about line 495.** It asserts "Identical content after relaunch stays DS-4". It changes to DS-8 by this owner-chosen change, not by weakening a check.
- **`app/CONTRACT_ISSUES.md`:** the CI-21 (b) disposition.
- **Rollback and version skew (F14).** Once a *re-confirmed* line exists, an App binary built on the preimage schema refuses the whole ledger: `read_ledger` → `wr_validate("library_entry")`. That is acceptable for development builds and should be stated in the implementation's evidence. Rolling back to such a binary needs the *re-confirmed* lines set aside by hand.

## Verification done here (revision 2, scratch copies only)

All checks used `jsonschema` 4.26.0, Draft 2020-12, with WD's schema registered
by `$id`.

- **Patch.** `git apply --check` is clean on the current checkout (HEAD `c59aaaa1b9`). The preimages are unchanged since revision 1. Applied to a copy, the patch reproduces the postimages below. The trailing newline is kept.
- **WR schema (revision 2):**
  - The postimage passes the metaschema.
  - 14 of 14 valid conformance instances validate, and 17 of 17 invalid instances are refused.
  - `minischema.check_supported` accepts it.
  - 29 constructed cases, all as expected:
    - the 22 cases of revision 1;
    - V13's gaps G1–G4, now refused: *re-confirmed* with `to` *draft*, with disposition *new revision*, or with no disposition, and *registered* with *re-confirmation*;
    - *re-confirmed* without `content`, refused;
    - the unchanged *registered* example, valid;
    - a *registration not completed* re-confirmation transition back to *registered, unchanged since*, valid.
  - The `freshness` description carries the RC-5 rule.
- **AAC offer schema, F2.** The proposed adoption (1)–(4) was applied to a scratch copy of the Design schema, which is byte-identical to the App copy.
  - It passes the metaschema. 4 of 4 valid examples still validate, and 19 of 19 invalid examples are still refused.
  - A re-confirmation offer built from `offer:0009` (re-confirm wording and purpose) is refused by the original schema at `properties/wording`, `allOf/3` and `allOf/6`, and is valid under the proposal.
  - `offer:0009` unchanged stays valid.
  - Refused under the proposal: the re-confirm wording with a registration purpose, the reverse, and the re-confirm wording on the multi descriptor `offer:0011`.
  - 6 of 6 cases as expected.
- **AAC capture-evidence schema.** All valid examples still validate. A capture whose entry outcome is *re-confirmed* is refused by the original and valid under the proposal.
- **NIR draft-transition schema.** The proposed adoption (1)–(4) was applied to a scratch copy.
  - It passes the metaschema. The valid example still validates, and 5 of 5 invalid examples are still refused.
  - A *re-confirmed* transition is refused by the original and valid under the proposal.
  - Refused under the proposal: `to` *draft*, disposition *new revision*, no `content`, no `a15_record`, and *registered* with *re-confirmation*.
  - 7 of 7 cases as expected.
- **Not run.** `wrproto.py` was not run as evidence; the pre-existing `minischema` `if` break is now logged as CI-23. WR-VC-16…19 are DESIGNED, not run.

## Patch (revision 2)

| File | sha256 |
|---|---|
| `changes/CC-WR-RECONFIRM.patch` | `38924fb728bcc228e2c1acab08346c7a0dbcf9670044d11c4d48b84cba28362b` |
| Preimage `…/DEL-02-02_…/Design/WORKSPACE_AND_REGISTRATION.md` | `094602acb5e1ba8b68bffc7475da8a80557749d134eddb60c8c4d4a676019656` (unchanged) |
| Preimage `…/DEL-02-02_…/Design/workspace-registration.schema.json` | `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9` (unchanged; equal to the App resource copy) |
| Postimage `WORKSPACE_AND_REGISTRATION.md` | `6bfb2277006a16e6089e7e862da24e9ed7fe749a08f0e63e35e50f25ea251838` |
| Postimage `workspace-registration.schema.json` | `6f772b3b0f51abf750fc0970a169ea3ff601d2015f3a6941308aff87c1ef51f5` |

## Revision 2 (after V13; 2026-10-07)

**Superseded revision 1 bytes:**

| Revision 1 file | sha256 |
|---|---|
| this record | `5d892e19339895491401ce900dcc3f3bdacd6f3149486802c0d91dc8b3568bb6` |
| patch | `5daf6889a1e92c161ea7750500a2e7cb5bcc3118804146274523c27d9b79c9b9` |
| postimage `WORKSPACE_AND_REGISTRATION.md` | `528ad33e8a0212eb00cada7abcbe7d7be44908693f9f3d5ff775d042bd4a04c3` |
| postimage `workspace-registration.schema.json` | `50c58c8a2cb62574c5266af23b5841951c0e8b913c254209209de9040ca261ad` |

The patch is regenerated against the same, unchanged Design preimages.

| Finding | Change |
|---|---|
| **F1 (MAJOR)** freshness | RB-3 gains a DS-8 sentence. RC-5: for DS-8, RB-3 (b) is read against `freshness.slot_latest`, never against ‹k›'s own prior. G-1R checks the slot's latest equals `freshness.slot_latest`. RC-4: SP-6's prior link does not apply, and `registration_disposition.prior_revision` keeps its meaning (the slot's latest at review). §8: the `registration_disposition` and `a15_descriptor` rows say so. Schema: the `a15_descriptor.freshness` description is amended, and the `registration_disposition.reconfirms` description names the meaning of `prior_revision`. WR-VC-19 adds the case |
| **F2 (MAJOR)** AAC offer schema | The AAC offer row now widens `allOf/6`'s `wording` and adds a pairing rule for the re-confirm wording and purpose. It names the App copy. Validated on a scratch copy with `offer:0009` |
| **F3 (MAJOR)** X-2 duplicate line | X-2 and RC-7: X-2 first rereads the ledger for a line citing the attempt's A15. If one exists it writes nothing and closes the attempt; otherwise it writes *not completed*. WR-VC-19 adds the crash-after-durable-G-4R case |
| F4 SEAL-2 wording | "To be weighed at the 90% gate" is removed. The owner's words, "Keep SEAL-2 deferred; continue other work", are quoted |
| F5 LS-1 only | DS-8, RC-1 and RC-5 (c) require ‹k›'s LS-1 standing as read. DS-4 covers a non-LS-1 ‹k›, with its standing and exact cause and LS-4's route (restore, §5.3, then DS-8). G-1R adds "act record no longer found". G-2R/G-3R no longer recreate a store: a store that no longer recomputes gives *not completed* (LS-4). RC-10 shows the LS-1 standing. WR-VC-17 adds the LS-4 case |
| F6 NIR transitions | §5.1: an abandoned, stale or failed DS-8 review returns to *registered, unchanged since* when it began there. X-4 likewise. The NIR adoption adds the accepted transitions and names `nir_model.py` `DRAFT_ALLOWED` with exact entries |
| F7 WR `draft_transition` | The schema now requires *re-confirmed* ⇒ `to` *registered, unchanged since*, disposition *re-confirmation*, and `content`, `a15_record` and `revision`. *Registered* never carries *re-confirmation*. G1–G4 are refused |
| F8 window | RC-7: before the attempt is *stored* (capture to G-3R), WR has no journal and writes nothing; AAC §4.4 governs. X-2 applies only after *stored*. G-3R names the point where the attempt is *stored* |
| F9 ACT meaning | Adoption text added for the ACT §2.1 A15 meaning cell |
| F10 LS-1 row and §5.4 | LS-1 row: runnable in a process holding the result (RC-2); Select there; Refine in any process (RF-1). §5.4: selection needs LS-1 and selectable in this process; the not-selectable row offers Refine |
| U-WR-23 | Closed: "K-6 unchanged; route via Refine (RF-1)". SP-4a points to it. No owner question remains |
| U-WR-21 | Option (a) is adopted as RF-1 in §4.6: Refine from the revision store without a selection. The base is App-recorded, shown and frozen at review. It also covers revisions registered in place, and the draft reviews as DS-8 by existing rules. Option (b), re-confirmation from the listing, is deferred in U-WR-21. The App's `create_selected_draft` successor is listed |
| RC-2 | Accepted as INTEGRATION text; unchanged |
| F11 | The store-collision argument is withdrawn. Decision (2) rests on ID-1/ID-2, SP-1 and the `latest()` series check |
| F12 | G-4R's uncertain-write reread and G-1R's pending-on-unreadable-ledger are labelled "new WR text, adopting the App's existing behaviour", not "as G-4" |
| F13 | Added with no or minor change: P, AS, LOOP, XT, WD `EXAMPLES.md`; DEL-01-04 prototypes `act_control.py`, `nir_model.py`, `run_cases.py`; WR `wrproto.py` and §13; NIR schema `allOf/0`. Conformance instances for WR-VC-20 are left optional, because they change §8's stated counts |
| F14 | Recorded as an App implementation item (compare the slot's latest, not the whole slot) and as a rollback and version-skew note |
| F15 | Not introduced here: the existing X-2 completes a *stored* registration cold. Returned to the WR owner for separate disposition. RC-7 keeps the stricter reading for re-confirmation |
| F16 | DV and act-log views noted: no adoption, purpose-only distinction while U-WR-22 is open |
| F17 | Noted. The one `reconfirmed_revision` shape is kept across disposition, descriptor and line |
| Correction | Revision 1's NIR schema text asked to "extend the C-02 `a15_record`/`revision` conditions", which do not exist in the NIR schema. It is replaced by an explicit new `allOf` rule (validated) |

## Basis read (sha256)

Checkout HEAD `c59aaaa1b9`. The J5 worktree was read at `8d98de95a8`.

| Source | sha256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `.agents/skills/proposal-format/SKILL.md` (format) | `63e6d2545c31df939511a5a137c214d5444ca562f6abf9b048de3aa2f8dac59d` |
| Run `OWNER_DECISIONS.md` (current; relevant sections unchanged since `10258440…`) | `7fa0723b0576dee8796c179282dea9580ee83835bc57958921096c68d6bdeeec` |
| Review `reviews/V13-CC-WR-RECONFIRM.md` | `5b1a8260816c19496a7af3c23b0cd810a89924e36717f034a31149790d837df7` |
| WR `WORKSPACE_AND_REGISTRATION.md` / schema | as preimages above |
| AAC `APP_ACT_CONTROL.md` | `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b` |
| AAC `aac.offer.schema.json` | `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066` |
| AAC `aac.capture-evidence.schema.json` | `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba` |
| NIR `NATIVE_INTERACTION_RECEIVING.md` | `7d96396172af4e444654809bc6946acd350477faf51eaa5afc1905259cd1c7f4` |
| NIR `nir.draft-transition.schema.json` | `07ed73bcc5b6d1eedbec303ad1de139305f2d6c37e51f7769c6d4600950166bc` |
| RS `RECORD_SEMANTICS.md` | `324ccd5f64093725f1e5ebb525c9ca13888e4036077bf320c75fa39b2810f4f1` |
| RS `RS_RECORD.schema.json` | `84200fd0ad045c11ce82ca5531ea461388304c46c1ea49d30263de5d6fa0f72a` |
| EXEC `EXECUTION_COMPATIBILITY.md` | `dc7ed825629fbd9afa72e709068764edc12a43a003cf54e47bc7e81ae24e39cb` |
| ACT `ACT_AND_POLICY_CONTRACT.md` | `597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2` |
| `changes/I2-HOT-REGISTRATION-OWNER-PLAN.md` | `5ebfd8443ffe2c47b39cc0ec6c6208913a1f38d6b9475bb4020697c879fa93fe` |
| `changes/I2-SELECTION-AUTHORITY-ROUTE.md` | `2b482b5c8b3e1717718823768d467919c28a7fb70f765d71f4dde2e09dfa9b88` |
| `CAPTURE_CUSTODY_DECISION.md` | `79503829fdb59b0603743cba2670b33fa3b7b5dbc04e3499d49170536e505d2c` |
| J5 `app/CONTRACT_ISSUES.md` (CI-21) at `8d98de95a8` | `d4d3e50ac616cf06a0a0c26627979774aed0139d3389f20854c2999b7744535d` |
| DEL-02-02 `Dependencies.csv` | `a97be837fd0dfe9c6dc2b402876e6454130a68da288b68d6c0d1abf4b0806c62` |

J5 code was read for consumer locations only: `workflow_library.rs`,
`workflow_workspace.rs`, `runtime_session.rs`, `act_control_a15.rs`. The
DEL-01-04 prototype `nir_model.py` was read for `DRAFT_ALLOWED`.

MISSING:
- A re-review of the revision 2 lines.
- Consumer adoptions: AAC Design and schemas, NIR Design, schema and prototype, RS, ACT, EXEC CAP-2.
- The App implementation, including RF-1 and F14, and the WR-VC-16…19 runs.
- Repair of CI-23 before any prototype evidence is claimed.

NEEDS_HUMAN_RULING: none. U-WR-23 is closed by HELP_HUMAN's ruling (K-6 is unchanged, so no owner question arises).

DEPENDENCY_NOTES:
- F15 (the existing X-2 completes a *stored* registration cold) is returned to the WR owner, separate from this change.
- RF-1 and RC-2 are INTEGRATION text under HELP_HUMAN's 2026-10-07 rulings.
- No DAG, group-order or register change.
- No new B→A relationship: packaging does not read the ledger.
