# CC-WR-RECONFIRM — re-confirming a registered revision after relaunch (proposed named WR change)

2026-10-07. Type 2 TASK, DEL-02-02 WR design-change author for run
`APP-V4-GROUP-A-20261004`. Dispatched by HELP_HUMAN (Claude Opus 5.5, Claude
Code); harness-native child, no delegation. Write fence: this record and
`CC-WR-RECONFIRM.patch` beside it. No Design, schema, code, register or
`Dependencies.csv` file was changed. No commit, network, Cargo, native act or
sign-in. Status: **PROPOSED**. Adoption needs independent review, then the WR
owner's application of the patch and each consumer's own adoption (LOOP_INIT
"Change control").

## Owner decision this implements

`OWNER_DECISIONS.md`, "Rerunning an unchanged workflow after relaunch —
2026-10-07". The owner answered **"A15 re-confirmation now (Recommended)"**.
Recorded effect: "A named, reviewed WR design change lets a new genuine A15
re-confirm identical bytes after the original in-process registration is gone.
Trust rests on the new act, not on a replay." SEAL-2 stays deferred, to be
weighed at the 90% gate. The decision approves no signing, credentials or
downloads. Problem statement: `app/CONTRACT_ISSUES.md` CI-21 (b) (J5 worktree,
branch `claude/app-v4-j5-reregistration` at `8d98de95a8`).

## Proposal

- PROPOSAL: Re-confirm a registered revision for use after its in-process registration result is gone
  - Evidence: WR §4.1 SP-4 DS-4 ("Identical to revision ‹k›; select it instead"); WR §2.1, ID-1, ID-2, SP-1, SL-1, SL-2; RS §6.2 HA-10; AAC §4.2, §4.4, §5.2a; owner SEAL-2 deferral (2026-10-05) and owner decision (2026-10-07); CI-21 (b).
  - Change: apply `CC-WR-RECONFIRM.patch` to `WORKSPACE_AND_REGISTRATION.md` and `workspace-registration.schema.json`. It adds DS-8 *re-confirmation*, SP-4a (the order of SP-3 and the identical-content check), new §4.8 RC-1…RC-10, notes in RB-3, RB-4, RB-8, §4.6, §5.1–§5.4, SQ-R, SQ-G, SQ-X, §7, §8, §9, verification rows WR-VC-16…WR-VC-20 and open items U-WR-21…U-WR-23. In the schema it adds `$defs/reconfirmed_revision` and a re-confirmation form of `registration_disposition`, `draft_transition`, `a15_descriptor` and `library_entry`.
  - Why: after a relaunch an unchanged registered workflow cannot run. Cold selection is held under SEAL-2 and DS-4 refuses identical bytes. The owner chose a new genuine A15 as the remedy.
  - Risk: each consumer must adopt its own text (below) before the App can offer DS-8. Until then the App keeps DS-4 and CI-21 (b) stands. U-WR-21 and U-WR-23 leave some relaunch paths without a route.
  - Status: PROPOSED

The patch is tagged in the WR file the way the file tags its in-place changes
(compare TX-4 "CC-WR-TEXT-METHOD-ADOPTION" and §16.8 "CC-WR-RECORD-PUBLICATION").
It adds a row to "Changes from v0.1" and keeps the schema's `$id` (`…:WR-v0.2`),
as those changes did.

## What the change specifies (brief items 1–7)

1. **When it is offered (RC-1, RC-2, SP-4a).** It is offered on review of a **draft** when all three hold:
   - SP-3 holds for the slot. K-6 is checked first, unchanged; see U-WR-23.
   - The reviewed content identity equals the revision value of a *registered* ledger line ‹k› of the target slot.
   - ‹k› is not selectable in this App process.

   "Selectable in this process" means the App holds, in memory, the result of ‹k›'s registration (G-4) or re-confirmation (G-4R), from an A15 captured in this process. When ‹k› is selectable, DS-4 still applies ("select it instead"). ‹k› may be any registered revision, not only the latest. Only one draft per act may be re-confirmed. Entries reviewed in place and the listing offer no re-confirmation (U-WR-21).
2. **The act (RC-3, RC-4).** It is a genuine A15 at DEL-01-04's act control, captured only from the person's native event. It is bound to the reviewed bytes, and its wording is "re-confirm workflow revision for use". The statement reads, in substance: "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." It records a **re-confirmation of revision ‹k›** in the ledger and registers **no new revision identity** (decision and sources below).
3. **Ledger and records (RC-6, RC-9, §8).**
   - **Ledger line.** A new `library_entry` outcome *re-confirmed*, with disposition *re-confirmation* and a required `reconfirms` {identity, `ledger_seq`, `sequence`} naming ‹k›'s registered line. Its `identity`, `sequence`, `prior_revision` and `store_path` are ‹k›'s, and it cites the **new** A15 record and capture evidence.
   - **Failed attempt.** A re-confirmation that does not complete writes *not completed* with disposition *re-confirmation* and `reconfirms`.
   - **RS A15 record.** Unchanged in shape: subject ‹k›, content ‹k›'s identity, `reviewedDraft` (this draft), `priorRevision` = ‹k›'s own prior, and the re-confirm purpose.
   - **Selection.** G-6R makes ‹k› selectable **in this process only**. Nothing rebuilds it from disk, and the earlier act and receipt are never made trusted (RC-2, RC-8).
4. **Failure behaviour (RC-5, RC-6, RC-7).** These reuse G-0…G-4, RB-3 and RB-8:
   - Bytes changed between review and act: AX-06, nothing captured.
   - The control closed or dismissed: the attempt is withdrawn, nothing captured.
   - The record write fails: AAC late write.
   - The slot moved on, the registered line changed, ‹k› became selectable, or the store conflicts: *not completed* citing the act.
   - The ledger cannot be read: the attempt stays pending with its cause.
   - An uncertain append: the intended line is reread, never appended twice.
   - The process is lost before G-4R: *not completed* at relaunch, never completed cold.
5. **What it is not (RC-8, §9).**
   - It is not cold replay and does not satisfy CI-10 or I3-CUST.
   - SEAL-2 and AAC §4.4 and §5.2a are unchanged.
   - It never carries an earlier A15 to other content.
   - If SEAL-2 or another custody mechanism is adopted later, a revision whose standing it verifies is selectable cold and DS-4 applies. Re-confirmation stays the fallback whenever that verification is absent or fails (RC-2).
6. **Consumers.** See "Consumers and propagation".
7. **Verification.** WR-VC-16 (re-confirm after relaunch and run), WR-VC-17 (revision selectable in this process: DS-4), WR-VC-18 (changed bytes take the ordinary route), WR-VC-19 (dismissal, staleness and loss have no effect) and WR-VC-20 (the ledger series accepts re-confirmation lines; schema and reader negatives).

## Decision (2): re-confirm revision ‹k›, no new revision identity

Chosen: the act **re-confirms revision ‹k›**. Its subject is ‹k›'s full tuple
as ‹k›'s registered line records it. The ledger records that act, and no tuple,
revision, sequence, store folder or published copy is created. Sources:

- WR §2.1 *Revision*: "numbered 1, 2, … by the App (the *sequence*, a display aid; identity is the revision value)". WR ID-2: "the revision registered from a draft equals the reviewed draft content identity". Identical bytes therefore give ‹k›'s revision value again. A "new revision" would duplicate ‹k›'s identity under a second sequence, and the tuple (ID-1) could not tell them apart.
- WR SP-1: "A slot holds a series of registered revisions. The App never overwrites or deletes a revision". DS-4 already refuses identical content as a new revision, and the series stays one revision per identity.
- K-6 (WR §1): "every run cites the revision it used". WR SL-2: "A selection stays on its revision". EXEC A-1: "The selection is the person's explicit choice of a registered revision (DEL-02-02's selection record…)". EXEC §6.1 *resolved*: "recomputed content identity **equals the revision**". Keeping ‹k› means `selection_record`, the run text (TX-1) and RS R2 *selected* cite exactly what they cited before, so EXEC and RS R2 need no change.
- RS HA-10: "A changed definition is a new revision and needs its own A15; an earlier A15 never carries over." Re-confirmation is a new A15 on unchanged bytes, so neither half is touched.

No source forbids keeping the identity. The alternative, a new ledger line
*registered* with the same revision value, would break the series check the
App enforces ("registers revision … a second time", `workflow_library.rs`
`latest()`). It would also make G-2's store reservation collide with itself.

## Decision (3): ledger line, RS linkage and in-process selection

- **New outcome, not a new record kind.** `library_entry` gains outcome *re-confirmed*, disposition *re-confirmation* and `reconfirms`. One record kind keeps the ledger a single append-only list that every reader already parses (WR §3 "Registration ledger"; §8 `library_entry`). Schema rules: `reconfirms` is present exactly when the disposition is *re-confirmation*; a *registered* line keeps its three dispositions; a re-confirmation is of a `reviewed_draft`, never a `reviewed_entry`.
- **Series reader (RC-9).** Only *registered* lines form the series. The App's `latest()` already filters `outcome == "registered"`. A *re-confirmed* line must cite an earlier registered line of the same slot, with equal identity, sequence, prior and store path. Its A15 is cited by no other line, because RB-8 ("never reused for other content or a later attempt") and RS HA-10 require one act per effect.
- **RS linkage.** `act.record_id` and `act.capture_evidence` on the line cite the new A15. The A15's `priorRevision` is ‹k›'s own prior, because RS defines it as "the revision this one follows in its slot (K-6)" (`RS_RECORD.schema.json` `relations.priorRevision`). The slot's latest stays in the descriptor's `freshness.slot_latest`, as RB-3 uses it. RS's `purpose` is free text (`"type": "string"`), so the re-confirm purpose needs RS text adoption only (HA-10 lists the purposes), not a schema change.
- **In-process selection only (RC-2).** This follows the owner's "Keep SEAL-2 deferred; continue other work" (2026-10-05) and AAC §5.2a: "After restart, an unverified capture/pending file cannot authorize a new act append". `I2-SELECTION-AUTHORITY-ROUTE.md` also says: "Do not make cold ledger/capture equality the registration authority constructor." The result exists only in memory, and a *re-confirmed* line read cold is an ordinary record. A *stored* re-confirmation attempt at relaunch is therefore written *not completed*, not finished by SQ-X X-2, because its only effect ended with the process.

## Consumers and propagation (exact proposed text; each owner adopts)

Register rows are named only, not changed: DEL-02-02 `Dependencies.csv`
(sha256 `a97be837…6c62`) DEP-02-02-013 and DEP-02-02-021 (DEL-01-04),
DEP-02-02-016 (DEL-04-01), DEP-02-02-017 and DEP-02-02-024 (DEL-04-03),
DEP-02-02-015 and DEP-02-02-022 (DEL-02-03), DEP-02-02-018 (DEL-09-02),
DEP-02-02-023 (DEL-09-06), and on the offer side DEP-01-04-009 and
DEP-02-03-010 (WR header).

| Consumer | Adoption | Exact proposed text |
|---|---|---|
| **WR** (DEL-02-02) Design and schema | Yes | `CC-WR-RECONFIRM.patch` |
| **AAC** `APP_ACT_CONTROL.md` (DEL-01-04) | Yes | (a) §1.2 A15 row, "Wording shown": after `"register workflow revisions" (from WR's `a15_multi_descriptor`, L-4; R21-3)` add `; "re-confirm workflow revision for use" (from WR's `a15_descriptor` with disposition *re-confirmation*, WR §4.8 RC-4; CC-WR-RECONFIRM)`. (b) §4.2, new paragraph before "**Why record at capture": "**Re-confirmation (CC-WR-RECONFIRM; WR §4.8).** Steps 1–8 apply unchanged to an `a15_descriptor` with disposition *re-confirmation*. The offer carries the descriptor's wording "re-confirm workflow revision for use" and its purpose; its one entry's subject is the registered revision ‹k› and its prior revision is ‹k›'s own. The native confirmation states, in substance: "Re-confirm revision ‹k› of ‹origin›:‹name› for use in this App session. This registers no new revision." At step 8 DEL-02-02 reports *re-confirmed* with ‹k›, or *registration not completed* with its cause. The capture is new evidence of the person's act; it makes no earlier capture or record trusted, and §4.4 and §5.2a are unchanged." (c) §5.1, the sentence ending `the wording "register workflow revision";` becomes `the wording "register workflow revision", or "re-confirm workflow revision for use" when WR's descriptor re-confirms a registered revision (WR §4.8; CC-WR-RECONFIRM);`. (d) §8 VC-AAC-08, append: "; a re-confirmation descriptor (WR §4.8) offered with its wording and statement, captured, recorded, outcome *re-confirmed* (CC-WR-RECONFIRM)" |
| AAC `aac.offer.schema.json` | Yes | Add `"re-confirm workflow revision for use"` to the `wording` enum and to the A15 branch's `wording` enum (`"register workflow revision", "register workflow revisions"`). The plural rule is unchanged |
| AAC `aac.capture-evidence.schema.json` | Yes | In `entries.items.properties.outcome.oneOf` add `{"type":"object","required":["registration","revisionIdentity"],"additionalProperties":false,"properties":{"registration":{"const":"re-confirmed"},"revisionIdentity":{"type":"string","minLength":1}}}` |
| **NIR** `NATIVE_INTERACTION_RECEIVING.md` §7 (DEL-01-04 draft view) | Yes | (a) `event` row: after `*registration not completed*` insert ` · *re-confirmed* (CC-WR-RECONFIRM)`. (b) `disposition` row: append `; *re-confirmation* (DS-8, WR §4.8)`. (c) `a15_record` row: "For *registered* and *registration not completed*" → "For *registered*, *registration not completed* and *re-confirmed*". `revision` row: "For *registered*: the revision identity" → "For *registered* and *re-confirmed*: the revision identity (for *re-confirmed*, the re-confirmed revision's own; no new revision)". (d) Display table, new row: `\| *registered, unchanged since*, reached by *re-confirmed* \| "re-confirmed as ‹revision› for use in this App session by ‹person› (identity not verified) at ‹t›; registered earlier (not verified in this session)", citing the new A15 record \|`. (e) "Refused by the view": add "*re-confirmed* when neither the transition nor `library_entry` gives the A15 record and the revision" |
| NIR `nir.draft-transition.schema.json` (0.2) | Yes | Add `re-confirmed` to `properties.event.enum` and `re-confirmation` to `properties.disposition.enum`. Add an `allOf` rule that event `re-confirmed` has `to` `registered, unchanged since` and disposition `re-confirmation`. Extend the C-02 `a15_record` and `revision` conditions to `re-confirmed` |
| **RS** `RECORD_SEMANTICS.md` HA-10 (DEL-04-03) | Yes, text only | (a) "Written only from capture evidence of the person's explicit registration at" → "Written only from capture evidence of the person's explicit registration, or re-confirmation (WR §4.8; CC-WR-RECONFIRM), at". (b) After "(ACT-POLICY-v0.9 §2.1)." insert: "**Re-confirmation (CC-WR-RECONFIRM; WR-v0.2 §4.8).** An A15 composed from a WR descriptor with disposition *re-confirmation* re-confirms a registered revision for use in the App session that captured it: bound subject that revision; bound content its identity; relations the reviewed draft and that revision's own prior revision (or none); purpose "make it available again in this App session from the project library" or "… from the user library". It registers no new revision. It is new capture evidence of the person's act; it makes no earlier A15, capture or record trusted, and §14.1a and R-7 are unchanged." No `RS_RECORD.schema.json` change. Optional structured relation: U-WR-22 |
| **ACT** `ACT_AND_POLICY_CONTRACT.md` §2.1 A15 row (DEL-04-01) | Yes, text only | After `for several entries: "make them available …", wording "register workflow revisions", WR ME-3)` add `; to re-confirm a registered revision for use in this App session: wording "re-confirm workflow revision for use", purpose "make it available again in this App session from the project library" or "… from the user library"; no new revision (WR §4.8; CC-WR-RECONFIRM)` |
| **EXEC** `EXECUTION_COMPATIBILITY.md` (DEL-02-03) | Yes, CAP-2 wording only | CAP-2: `from v0.7 "register workflow revision" for A15, or "register workflow revisions" when one act registers several entries, K-8, L-4)` → `from v0.7 "register workflow revision" for A15, or "register workflow revisions" when one act registers several entries, K-8, L-4, or "re-confirm workflow revision for use" when one act re-confirms a registered revision for use in this App session, WR-v0.2 §4.8, CC-WR-RECONFIRM)`. **No change** to A-1, T-1, §6.1 *selected* or *resolved*, or `selection_record` receiving: the identity is unchanged (decision 2) |
| GUIDE (DEL-03-04 M5.1), CA (DEL-09-06), PANEL (DEL-05-02), WD (DEL-02-01 OS-2), DV (DEL-06-02) | No | They name A15 *register workflow revision* and its relations. The kind and relations are unchanged, and re-confirmation is an App-side WR disposition. Their text stays true |
| Group B packaging (DEL-01-06 PKG P-2) | No | It reads bundled workflows and the shipped-revision manifest (WR §3; LS-5, LS-8), not the registration ledger |
| DEL-09-02 qualification (DEP-02-02-018) | Notice only | The §12 case inventory gains WR-VC-16…WR-VC-20 |
| **App code** (J5 branch `8d98de95a8`, `projects/chirality-app-v4/app/`) | Yes, after the Design adoptions | `src-tauri/resources/workflow_role/workspace-registration.schema.json` and its `SOURCE_MAP.json` hash; the AAC schemas through `src-tauri/schemas/manifest.json`. `src-tauri/src/workflow_library.rs`: `review_draft` DS-4 → DS-8 when no held result; `compose_descriptor`; the G-1R…G-6R attempt; `read_ledger` and `latest()` RC-9 checks; no cold completion. `src-tauri/src/workflow_workspace.rs`: `Review::open` DS-4 and the descriptor JSON wording and purpose; `RegisteredRevision` built from a re-confirmation citing the new act. `src-tauri/src/runtime_session.rs`: `WorkflowReviewContext.registered`, `select_hot_registered_copy`, listing text "registered — re-confirm to use in this App session". `src-tauri/src/act_control_a15.rs`, `act_control.rs`, `a15_native.rs`: wording, statement, outcome *re-confirmed*. `src/App.tsx`: DS-8 offer and display. `src-tauri/src/workflow_library_tests.rs` ~line 495 asserts "Identical content after relaunch stays DS-4"; this changes to DS-8 by this owner-chosen change, not by weakening a check. `app/CONTRACT_ISSUES.md` CI-21 (b) disposition |

## Verification done here

- `git apply --check` of the patch on the current checkout: clean. Applied to a copy, it reproduces the intended postimages (hashes below).
- Schema (scratch copy, `jsonschema` 4.26.0, Draft 2020-12, WD schema registered by `$id`):
  - The schema passes the metaschema.
  - All 14 valid conformance instances still validate. All 17 invalid instances are still refused.
  - DEL-04-03 `minischema.check_supported` accepts the new keywords.
  - 22 constructed cases ran as expected. The positive cases are a *re-confirmed* line, a *not completed* re-confirmation line, a DS-8 descriptor, a *re-confirmed* transition and a DS-8 disposition. The negatives are a missing `reconfirms`, a registration disposition on *re-confirmed*, *registered* with *re-confirmation*, `reconfirms` on a registration, an in-place entry, a missing store path, mismatched wording or purpose, and a re-confirmed transition without its record or revision.
  - The original schema refuses all five positive cases, so the delta is what admits them.
- Prototype: `wrproto.py` was **not** rerun as evidence. On an unmodified scratch copy of the current tree it already exits 1, before any WR check, because DEL-04-03's `minischema` rejects keyword `if` in the current `RS_RECORD.schema.json` (`#/$defs/suppliedGuidance/allOf/2`). This break predates this change and is outside its fence. The WR-VC-16…19 cases are DESIGNED, not run.

## Patch

| File | sha256 |
|---|---|
| `changes/CC-WR-RECONFIRM.patch` | `5daf6889a1e92c161ea7750500a2e7cb5bcc3118804146274523c27d9b79c9b9` |
| Preimage `…/DEL-02-02_…/Design/WORKSPACE_AND_REGISTRATION.md` | `094602acb5e1ba8b68bffc7475da8a80557749d134eddb60c8c4d4a676019656` |
| Preimage `…/DEL-02-02_…/Design/workspace-registration.schema.json` | `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9` (equal to the App resource copy) |
| Postimage `WORKSPACE_AND_REGISTRATION.md` | `528ad33e8a0212eb00cada7abcbe7d7be44908693f9f3d5ff775d042bd4a04c3` |
| Postimage `workspace-registration.schema.json` | `50c58c8a2cb62574c5266af23b5841951c0e8b913c254209209de9040ca261ad` |

## Basis read (sha256, working tree at `3b3c461647` plus the J5 worktree)

| Source | sha256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `.agents/skills/proposal-format/SKILL.md` (format) | `63e6d2545c31df939511a5a137c214d5444ca562f6abf9b048de3aa2f8dac59d` |
| Run `OWNER_DECISIONS.md` | `10258440536dea715b3781ae7a50c5e2792f838effb12d5ecbee517cc40f3f2c` |
| WR `WORKSPACE_AND_REGISTRATION.md` / schema | as preimages above |
| AAC `APP_ACT_CONTROL.md` | `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b` |
| AAC `aac.offer.schema.json` / `aac.capture-evidence.schema.json` | see note* |
| NIR `NATIVE_INTERACTION_RECEIVING.md` / `nir.draft-transition.schema.json` | see note* |
| RS `RECORD_SEMANTICS.md` / `RS_RECORD.schema.json` | `324ccd5f64093725f1e5ebb525c9ca13888e4036077bf320c75fa39b2810f4f1` / `84200fd0ad045c11ce82ca5531ea461388304c46c1ea49d30263de5d6fa0f72a` |
| EXEC `EXECUTION_COMPATIBILITY.md` | `dc7ed825629fbd9afa72e709068764edc12a43a003cf54e47bc7e81ae24e39cb` |
| ACT `ACT_AND_POLICY_CONTRACT.md` | `597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2` |
| `changes/I2-HOT-REGISTRATION-OWNER-PLAN.md` | `5ebfd8443ffe2c47b39cc0ec6c6208913a1f38d6b9475bb4020697c879fa93fe` |
| `changes/I2-SELECTION-AUTHORITY-ROUTE.md` | `2b482b5c8b3e1717718823768d467919c28a7fb70f765d71f4dde2e09dfa9b88` |
| `CAPTURE_CUSTODY_DECISION.md` | `79503829fdb59b0603743cba2670b33fa3b7b5dbc04e3499d49170536e505d2c` |
| J5 `app/CONTRACT_ISSUES.md` (CI-21) at `8d98de95a8` | `d4d3e50ac616cf06a0a0c26627979774aed0139d3389f20854c2999b7744535d` |
| DEL-02-02 `Dependencies.csv` | `a97be837fd0dfe9c6dc2b402876e6454130a68da288b68d6c0d1abf4b0806c62` |

\* Full values: `aac.offer.schema.json`
`f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066`;
`aac.capture-evidence.schema.json`
`4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba`;
`NATIVE_INTERACTION_RECEIVING.md`
`7d96396172af4e444654809bc6946acd350477faf51eaa5afc1905259cd1c7f4`;
`nir.draft-transition.schema.json`
`07ed73bcc5b6d1eedbec303ad1de139305f2d6c37e51f7769c6d4600950166bc`.

The J5 code was read for consumer locations only:
`workflow_library.rs`, `workflow_workspace.rs`, `runtime_session.rs` and
`act_control_a15.rs`.

MISSING: independent review of this change; consumer adoptions (AAC, NIR, RS,
ACT, EXEC CAP-2); implementation and the WR-VC-16…19 runs; repair of the
pre-existing `wrproto.py` / `minischema` `if` break before any prototype
evidence is claimed.

NEEDS_HUMAN_RULING:
- **U-WR-23 (owner; K-6 is the owner's).** May a draft with ‹k›'s exact bytes but no App-kept base reaching the slot re-confirm? Such a draft may have been written from scratch, or its base may have been lost (U-WR-12). K-6 reads "a same-name draft with no such origin is refused with a request for a new name". The patch therefore keeps DS-3 first (SP-4a) and does not decide this. The consequence matters: after a relaunch, if the registered draft was edited or removed, the person cannot reach DS-8 unless U-WR-21 (a) below is adopted.

DEPENDENCY_NOTES:
- **U-WR-21 (integrator, WR with DEL-01-04).** WR §4.6 already offers Refine on LS-1. The App's `create_selected_draft` requires a hot selection, so after a relaunch it cannot make the draft. Options: (a) allow Refine of an LS-1 revision from the store without selection, with the base disclosed and frozen as the I2 owner plan allows for a new A15; or (b) design re-confirmation from the listing. Neither is decided here.
- **RC-2** writes into WR the in-process admission rule the App already applies under the SEAL-2 deferral (`I2-SELECTION-AUTHORITY-ROUTE.md`; AAC §5.2a). WR was silent on it before. Reviewers should confirm this reading.
- No DAG, group-order or register change. No new B→A relationship: packaging does not read the ledger.
