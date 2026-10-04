# O-A — DEL-06-01, DEL-06-02 (owner notes and returns)

Owner O-A: Type 2 TASK, Claude Opus 5.5, high effort, standing assignment
from HELP_HUMAN (run `APP-V4-DESIGN-PASS-4-20261003`). Read-only git; no
network. Paths are relative to `projects/chirality-app-v4/execution`.

## Fixture for O-C (DEL-09-05 VER-004; DEL-09-11 reader)

- **Path:** `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1/`
- **Manifest:** `MANIFEST.sha256` in that folder, sha256
  `e3c8c5eac3b6ab40a2b1c3ba734583dc8cbbd0eb7c056bb1afd5c3cf4e0d3b6f` (six files).
  Check: `cd …/FX-DP1 && shasum -a 256 -c MANIFEST.sha256`.
- **Frozen**, with one condition: the two `act_request` entries are valid only
  with PR-1…PR-5 (see E-1, obstacle). Applying those rows changes no fixture
  byte. The A16 `human_act` is valid against `RS_RECORD.schema.json` as it now
  is.
- Content: PKG-1, an A16 package decided by "Engineer A" (ALT-2); PKG-2,
  pending; an agent message claiming PKG-2 was decided, which is not a record.
  All of it is invented.

## Unit E-1 — the early path (frozen for review, 2026-10-03)

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
