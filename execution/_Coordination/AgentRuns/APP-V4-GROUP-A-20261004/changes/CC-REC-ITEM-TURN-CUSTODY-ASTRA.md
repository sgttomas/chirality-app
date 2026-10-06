# CC-REC-ITEM-TURN-CUSTODY — private proposed source amendment

2026-10-05. TASK `/root/group_a_execution_astra/rec_custody_design`, parent
`/root/group_a_execution_astra`; fresh delegated-harness-native child, supplied
Astra/low, no delegation. Sole maintained write: this report. Private source,
schema and examples only; no maintained adoption, product code, Git, Cargo,
native/supplier, network, authentication or credential operations.

**Result: concrete source amendment prepared for independent review. Not adopted;
RC1-COLD and whole recovery completion remain open.** This is an ordinary bounded
technical source-fit proposal, not a new stage gate. The existing 39 author and
12 independent passes remain partial evidence, not evidence for this amendment.

## Exact candidate and compatibility

Private package: `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-rec-item-turn-design.rb2i2q3l`.
`source-amendment.patch` contains exact proposed changes to owning REC Design:
new §7.2; current ledger schema with distinct `$id` …:0.3 and one optional
nonempty opaque item `turnId`; preserved byte-exact 0.2 schema under the explicit
v0.2 filename; six focused valid/invalid example files. Custody/stop schemas and
historical examples are unchanged. `manifest.json` seals proposed files, patch
and validation output. Preparation script is `/tmp/prepare-rec-item-turn.py`.

Actual inspected schema0.2 has closed item objects and no row version/header.
Current product validator embeds one schema resource; its `$id` identifies the
schema, not each record. Therefore changing that identity to0.3 is necessary to
avoid silently redefining0.2; adding a per-record discriminator or new ledger
kind is unnecessary. New reader accepts old rows unchanged, absence is unknown.
Old reader rejects new correlated rows. No universal backward compatibility,
automatic downgrade guard or negotiation is claimed. Mixed ledgers require the
new reader; rollback preserves bytes and cannot strip pointers or install an
older writer against the upgraded ledger. The source states this explicitly.

All known item associations survive as `(turnId,itemId)` scoped by actual full
generation/home/thread; item-only evidence never sets liveTurn. Correlation
unknown on a legacy item remains unknown even if liveTurn happens to be present.
Known items remain independent of competing current-turn observations. Existing
custody schema0.2 already represents actual hot loss tuples; restart event has
no item member, and this proposal does not add one or replay a historical loss
as freshly observed. Cold pointer history separately preserves known tuples.

## Persistence and receiving work after review

1. REC author adopts the reviewed Design/schema and synchronizes the product
   resource/validator to exact0.3 bytes, preserving the archived0.2 identity.
   The actual Host source writes actual known turnId in immutable snapshots to
   the existing queue/sole writer; failed or queued rows stay visibly pending.
2. REC cold reader retains each optional association and original provenance;
   per-item unknowns are explicit. Completion/terminal handling uses matching
   tuples. Root renders known/unknown correlation and distinct metadata versus
   execution provenance beside native History, with no read-side append/flush.
3. Exercise actual Host→ledger→loss→reopen paths: item-only, competing turns,
   same item label in two turns, legacy absence, late/terminal frames, and actual
   IO failure/retry/retired queue. Assert exact association after restart and
   no manufactured liveTurn/restart-live-work. Validate hot custody events and
   valid restart events against unchanged custody schema. Preserve metadata,
   ordered tags, historical project P, forks and full generation isolation.
4. Propagate named change through REC source/resource/prototype format checks,
   Root recovery reader/UI, contract issue and Group A graph. Notify actual
   downstream REC consumers (DEL-01-03/01-04 display; ADAPTER/RS receiving owners)
   of the pointer-format/read boundary; their later external mapping is not
   supplied here. Existing downstream custody schema identity is unchanged.
   Parent owns cross-group notices/adoption and decides whether an actual
   downstream completed consumer is affected; no cross-group topology change
   was found in this narrow source change.
5. Separate actor reviews the proposed source then backchecks actual code and
   consumer candidate. Native restart evidence and broader external PI-6 join
   remain their own unfinished requirements. Schema passes cannot close them.

## Authority and disposition

Applicable v4 LOOP says: “Agreed interfaces in any deliverable's Design change
only through named, reviewed changes that are propagated to their consumers.”
That is the specific adoption rule here, satisfied prospectively by this named
package, independent review and propagation; it does not reserve every field
extension to the human. The same LOOP says “The owner assesses each stage gate.”
No stage-gate act is sought or claimed. Root's owning-decision rule still applies
if Parent finds an explicit accepted choice being reversed. Field Book §1 says
ask the human about a change that “would make another group's finished work
wrong”; Parent must apply that if receiving evidence establishes it, rather
than inferring such a case merely from a version increment. The schema's known
older-reader incompatibility is expressly disclosed for that adjudication.
No protected scope/criterion is reduced; full reference preservation repairs
implementation's unmet requirement. Parent can route source review now.

## Offline checks and supplied basis

Python jsonschema4.26.0 Draft202012Validator validated the proposed schema and
six new examples (three valid, three invalid) plus all six existing examples
with their stated validity. New known references fail old0.2; legacy example
passes both. These are schema/format checks only, not production behavior.
`validation.json` retains per-example outcomes; no installed dependencies changed.

Read Root/TASK/v4 LOOP, actual REC Design/schema/custody example, current product
validator entry, I1 custody/NEXT reports, original V6 and appended V6-R1/RC1-COLD
(the latter are sections of V6, not separate files), selective Group A graph,
manual index, guide headings/decision section and full Field Book. Initial path
lookup also read App v3 AGENTS/LOOP in error before identifying App v4; those
instructions were not applied to this assignment. That deliberate provenance
clarification prevents silently borrowing v3's gates or authority.

### Read-source hashes

- `AGENTS.md` — `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md` — `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-dev/AGENTS.md` — `41995dfe123041e1d0235a73e532fddb913f2c2124a9e8ec43857a87d7e5822c`
- `projects/chirality-app-dev/loop/LOOP_INIT.md` — `8b975c10acf6c4394f5423d4def20aeb4583159c691e8d3d11a41ce7451e6a25`
- `docs/alignment-manual/README.md` — `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` — `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` — `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` — `e78b9ead452b0a1adb20cf07493a1eccbd2ee651e68d4f75772c440a6a228056`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.app-ledger-entry.schema.json` — `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.custody-event.schema.json` — `033398508abc813e90aee0a074a18cb91bd59be88b6991111504ae5662653773`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-ASTRA.md` — `3b1d63acfaa0f18f797a830ee61deba90205e8391a19f33b6df05927a68b5240`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-RECOVERY-CUSTODY-NEXT-ASTRA.md` — `073710657bf0ebcc583565a88e876dac30f2506ceca3c7f43c33ecd900043d9c`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V6-RECOVERY-CUSTODY-CORE.md` — `9b16ad56f368eac5802742b79cf2ec0145c6a946ea9bf5a04b700c8737ff5582`
- `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` — `f0fff309d2f8eec23046b5349e4969308ef26319a4e5b6eedf46b3c4da50bc31`

Private patch SHA-256: `2549bd3d1d1c146c0bab83291df0db9bbc5f24ad738df86b1cf96934aca8f7f8`.
