# Shared commitments and consumer responsibility account

- **Contribution:** DEL-10-03/RA-v0.2. It supersedes RA-v0.1 (`531b65b7…`, committed at `caed56b8ea`; RV3: READY with RA1-R1 and RA1-R2 MINOR); see "Changes". It serves OUT-001 (§2),
  OUT-002 (§1, §3) and OUT-003 (§4); verification design is in §5.
- **Status: DRAFT DEFINITION, frozen for RV3.** Owner O-E (Type 2 TASK, Claude Opus 5.5),
  run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04.
- **What it is (R23-31.1, 31.7):** an index over the supplier Design files'
  own responsibility sections. It does not restate them (SQ-E2): WD §9 in
  particular is indexed, not copied.
- **Basis:**
  - this deliverable's `ScopeOfWork.md`, sha256
    `31bc607defa42914520959234f2400858d4c1d5272ac5fa523fcea39d1b94166`.
    SCA-V4-002 revised REQ-005 and added AX-005; read with that block.
    SCA-V4-003 changed no block here;
  - `Dependencies.csv` `7b9bcfaf…`, equal to DAG-004's source hash.
- **Rulings:** R23-2, R23-21, R23-30, R23-31 (items 1, 7, 8, 10), R23-32
  (F-R11, F-R15, F-R16), R23-34 (H-1), R23-44 (the checker's inputs are
  committed).
- **Labels:** SETTLED, DERIVED, INTEGRATION and PROPOSED. **States**,
  **Inference** and **Checked by O-E** are kept apart.
- **Paths:** `E/` = `projects/chirality-app-v4/execution/`.

## 1. Population bound: which promises the account covers (REQ-002; AC-002; R23-31.7)

### 1.1 Rule (DERIVED, R23-31.7)

- **What a promise is.** The SoW says: "A promise is an accepted obligation,
  not every incidental historical mechanism". REQ-002 covers promises
  "affected by proposed relocation or changed supply".
- **The population.** The obligations the nine admitted supplier rows hand
  to DEL-10-03, plus the cross-project consumer layer DEP-006 names, plus
  the four open allocations OI-013, 014, 018 and 024.
- **The tests for an entry.** An entry is in the population only if both
  hold:
  - (a) an accepted contract or decision states it;
  - (b) its owner, supply route or placement differs from the v3/Root
    arrangement, or is still unallocated.

### 1.2 Supplier entries (the nine admitted rows; DAG-004)

Each entry indexes its supplier Design file at the hash read (2026-10-04).

| ID | Row | Supplier and Design file (label, sha256 prefix) | Section the account indexes | Class | Why it is affected |
|---|---|---|---|---|---|
| S-1 | DEP-10-03-008 | DEL-02-01, WD-v0.9 `262c9e54…` | §4.3, §5 (semantics); §9 "Shared contract/component responsibility map", rows A-1… ("every Confirmation cell remains 'None'"; U-17) | Concept and technical commitment | Shared allocation unconfirmed (OI-014). Workflow supply moves from v3's packaged instruction root to v4's bundle (PKG-v0.2 P-2, via DEL-02-02) |
| S-2 | DEP-10-03-009 | DEL-02-03, EXEC-v0.7 `138b04eb…` | Its receiver row names "§2, §3, §4, §10" | Technical commitment | Checkpoint receiving in host loops (OI-013); hold machine in a governance phase |
| S-3 | DEP-10-03-010 | DEL-02-04, ROLE-v0.2 `c8474d91…` | O-5 row, "§3–§6" | Guidance supply | Product `AGENTS.md`, role files and `roles.json` are supplied by v4's bundle (PKG-v0.2 P-3), not v3's script (CLM-007). Root instruction change D-GOV-52 (R23-30) |
| S-4 | DEP-10-03-011 | DEL-03-01, C-v0.8 `0e3ba39c…` | §8 "Three-surface responsibility map — skeleton"; its rows naming "DEL-10-03 account" (OI-013/014 UNRESOLVED) | Technical commitment | Placement unresolved (OI-013, OI-014) |
| S-5 | DEP-10-03-012 | DEL-03-02, P-v0.8 `ad6a3083…` | §1 authority map; §13 "Provide to DEL-10-03" row | Technical commitment | Shared meaning; any common implementation is unagreed |
| S-6 | DEP-10-03-013 | DEL-04-01, ACT-POLICY-v0.11 `597f13bd…` (re-pinned deliberately from v0.10, sha256 prefix 1bf0ce8e; R23-21) | §2.1 act list (A1–A16), §3, §8. Its §10.3 receivers row for DEL-10-03 now maps exactly these sections | Concept and human-act responsibility | Act ownership is split across App, host and person. The consumer row is filled by O-A under R23-21 when RA §2 maps it (R23-31.10). **Request to O-A, not an edit by O-E** |
| S-7 | DEP-10-03-014 | DEL-04-03, RS-v0.10 `2e7afb1b…` | Its row: "§2 authority rules, §13 format, §14 writer and reader sequences … no common service or implementation is inferred" | Technical commitment | Record format shared across App and hosts; host writers external |
| S-8 | DEP-10-03-015 | DEL-05-01, LOOP-v0.9 `2bac33a8…` | Receiver row "§5, §10, §12"; §10.1 "Responsibility map" | Technical commitment | Host loop is constructed externally (SWBPIPE); placement (OI-013) |
| S-9 | DEP-10-03-016 | DEL-05-02, PANEL-v0.9 `4898b6f8…` | §6 "Reusable-component allocation account" | Technical commitment | Panel components: shared vs per host unagreed (OI-014) |

### 1.3 Cross-project and open-allocation entries

| ID | Source | What the account carries | Owner and point of need (as stated) | Waits for |
|---|---|---|---|---|
| X-1 | DEP-006 | Consumer, packaging and tool-path consequences for Root, Runtime, App v3 and Piping. Handed to PKG-11 (DEP-10-03-019). DEL-11-02's consumers come from here (R23-32 F-R11) | Owners of affected consumers; "Before each consumer transitions or old arrangement retires"; NOT_ADOPTED_BY_THIS_DRAFT | Each consumer's adoption (DEL-11-02). Static traces are possible now |
| X-2 | OI-013 | Loop placement, parsing, persistence and panel assembly: S-2, S-4, S-8, S-9 rows | Shared contract owner with SWB implementation owner; "Before shared/host implementation boundary contracts" | Host joins (DECISION-3 of `APP-V4-SWBPIPE-INTAKE-20260928`) |
| X-3 | OI-014 | Shared contract and component placement: WD §9, C §8, PANEL §6 | App/shared contract owners, that is, the deliverable owners (R23-31.8); "Before structural/production contract allocation" | Owners' confirm-or-object at the next comparison (WD U-17). The SWBPIPE half waits for the host joins |
| X-4 | OI-018 | Instruction distribution. For the App: K3 K-9 as amended by L-2. Latest instance: D-GOV-52, adopted by App v4 (R23-30); App v3 and Runtime "notice delivered; receiving decision not recorded" (F-R16) | Owner with shared/project instruction owners; "Before instruction changes or dependent supply" | Hosts' and other loops' own decisions |
| X-5 | OI-024 | Staged adoption and retirement | Owner with affected consumers; "Before each adoption/retirement decision" | PKG-11 (P-4 in R23-32) |

### 1.4 Excluded, with the reason (so the bound can be checked both ways)

| Excluded | Reason |
|---|---|
| Hosting, native and packaging deliverables (DEL-01-0x) as suppliers | No DEL-10-03 row names them. Packaging enters only as a *supply route* for S-1 and S-3 (PKG-v0.2 P-2/P-3), traced under REQ-004 |
| Product behaviour that keeps its owner and supply in v4 | Not affected by relocation or changed supply (test (b) fails) |
| Manual editions | DEL-10-01's (DEP-10-03-017 is an input basis, not a promise) |
| Historical v3 mechanisms with no accepted v4 obligation | "not every incidental historical mechanism". Kept as history under REQ-003, not traced as promises |

**Count (states).** 9 supplier entries and 5 cross-project or
open-allocation entries, 14 in all. Every entry is traced to a register row
or an Open_Issues/External_Dependencies row.

**Cycle guard (R23-2; S2-E SQ-E5).** All 14 entries are read by DEL-10-03.
No row is proposed in which a PKG-02…05 deliverable consumes DEL-10-03;
DEL-10-03 reaches all of them, so such a row would form an SCC. The S-6
mapping is a row in ACT's own consumer table, not a register row.

## 2. Responsibility map (OUT-001; REQ-001, REQ-005; AC-001, AC-005)

### 2.1 Homes (states)

- **Conceptual and organisational home:** Root, while the human governs
  consequential direction (CLM-001).
- **Working guidance:** the manuals and selected methods (DEL-10-01's
  account; out of this population).
- **Technical commitments:** develop in accountable SoWs and their
  derivatives (CLM-001).
- **Runtime supply:** goes through the App's bundle (PKG-v0.2 P-2 and P-3,
  proposed) and Codex's own discovery (Root `AGENTS.md`).
- **Human decision responsibility:** stays with the person (ACT §2.1).

### 2.2 Map

Each row indexes the supplier's own section. Its content is not restated
here. **Host part** is what the record leaves with the host owner (SWBPIPE
or a later host). **Confirmation** is the owner response the supplier
records.

| Entry | Class | Meaning (one line) | App v4 accountable owner | Host or external part | Consuming contracts (as the supplier states) | Open allocation | Confirmation | Indexed section |
|---|---|---|---|---|---|---|---|---|
| S-1 | Concept + technical | Portable workflow, role and checkpoint meaning; identity tuple; compatibility vocabulary; the shared-allocation map A-1…A-12 | DEL-02-01 (semantic owner). Supply of bundled workflows: DEL-02-02 | Host workflows and their use in loops (A-9, A-10) | WD Receivers line and §8 | OI-014 for A-1…A-6, A-10…A-12; OI-013 for A-4, A-9, A-10; A-7 and A-8 sit with DEL-04-03 and DEL-03-01 | **"None"** for every row (U-17; WD §9: "every Confirmation cell remains 'None'") | WD-v0.9 §4.3, §5, §9 |
| S-2 | Technical | Required-tool compatibility check; checkpoint receiving. Phase 1 is guidance and recording (PH-1…PH-10); the hold machine is the governance phase | DEL-02-03 for App runs | Checkpoints in host loops: DEL-05-01 receiving, external construction (EXEC §2 table) | EXEC Receivers line | OI-013 (host loops); OI-014 (sharing, WD A-4) | Not applicable within the App; the host part waits | EXEC-v0.7 §2, §3, §4, §10 |
| S-3 | Guidance (supply) | Role selection; product guidance plus role supplied at conversation start (K-9 as amended by L-2) | DEL-02-04; packaging DEL-01-06 (PKG-v0.2 P-3) | Each host's own role and guidance supply | ROLE O-1…O-5 | OI-018 remainder (hosts, other instruction owners) | Not applicable | ROLE-v0.2 §3–§6 |
| S-4 | Technical | Catalog, read basis and exposure across the three surfaces (H/E/X) | DEL-03-01 | Host owner produces every element (C §8: all "unagreed") | C Receivers line | OI-014 ("Shared types / components … DEL-10-03 account"); OI-013/014 for loop-side checking | **"unagreed"** throughout | C-v0.8 §8 |
| S-5 | Technical | Proposal, validation and outcome meaning; receiving semantics | DEL-03-02 | Domain truth, validation, the application route, receipts and views (P §1) | P §13 "Provide to" rows | Residual policy with App/SWB owners (P §1 row "Act names …") | Not applicable | P-v0.8 §1, §13 |
| S-6 | Concept + human-act responsibility | Acts A1–A16: canonical names, decision actors, subjects, evidence; reserved acts (D2) | DEL-04-01 | The host offers, enforces its own list and captures acts (V4-HI-30); OI-021 operation-specific additions | ACT §10.3 receivers table | OI-021 (owner via the SWB session and App/shared owner) | Not applicable. ACT-POLICY-v0.11's DEL-10-03 receiver row maps RA's reading (§2.3) | ACT-POLICY-v0.11 §2.1, §3, §8, §10.3 |
| S-7 | Technical | Act and run record format; ordinary-file authority rules OF-1…OF-9; writer and reader sequences | DEL-04-03 | Host-agent runs keep records with the host project (OF-9); host receipts stay with the host (OF-3) | RS Receivers line | None for meaning ("no common service or implementation is inferred") | Not applicable | RS-v0.10 §2, §13, §14 |
| S-8 | Technical | Loop receiving requirements, fixtures and cases | DEL-05-01 (receiving only) | Loop construction, placement, parsing and persistence (SWBPIPE) | LOOP §10.4 receivers | OI-013; common loop implementation "Not allocated" (OI-014/013) | LOOP §10 records "no candidate, evidence, commitment or contribution received" from SWBPIPE | LOOP-v0.9 §10.1 |
| S-9 | Technical | Panel receiving; candidate shared presentation components | DEL-05-02 (receiving) | Panel assembly (SWBPIPE) | PANEL Receivers line | OI-013 (assembly); OI-014 (whether any candidate is shared) | **"None"** for every candidate | PANEL-v0.9 §6 |
| X-1…X-5 | Consumer adoption and open allocations | §1.3 | PKG-11 (X-1, X-5); the deliverable owners (X-3) | SWBPIPE (X-2) | — | §1.3 | — | §1.3, §4 |

### 2.3 Rules carried, not restated (REQ-005; AC-005)

- **Compatibility of meaning is not shared execution.** "Shared meaning does
  not prescribe one executable service" (V4-ARC-20). WD §9 lists no
  confirmed candidate; PANEL §6 has three proposed candidates and no
  agreement. The account therefore names **no** common implementation.
- **The chosen direction is retained** (SCA-V4-002 revision of REQ-005):
  stock Codex with App-owned hosting, Tauri, and the minimal host loop on a
  person-chosen model.
- **S-6 consumer row (R23-31.10): done.**
  - RA-v0.1 asked O-A, through HELP_HUMAN, to map ACT-POLICY §10.3's row
    "DEL-10-03 | DEP-10-03-013 | none | Not mapped in detail".
  - O-A's ACT-POLICY-v0.11, committed at `0bd6e4b4e9` (sha256 `597f13bd…`),
    now reads: RA-v0.1 "reads, by section: §2.1, the acts with their
    decision actor, subject and supporting evidence; §3, the settled
    distinctions S1–S12; §8, the policy representation, namely DECISION-1's
    reserved acts (§8.2) and the values still open (§8.4)".
  - That matches what RA consumes. Adoption was checked in the returned
    file, not assumed (workflow §5).
  - RA's ACT pin is re-pinned deliberately to v0.11 (R23-21). Sections §2.1,
    §3, §8, §8.2, §8.4 and §10.3 keep their headings in v0.11, checked by
    O-E.

## 3. Promise trace (OUT-002; REQ-002; AC-002)

### 3.1 Forward: accepted source → current decision → SoW → Design → verification

The accepted source for every entry is ScopeLedger SOW-234 ("Begin shared
renewal with compatible workflow, identity, human-act and evidence
contracts while retaining the chosen Codex/Tauri/minimal-loop direction"),
with HTML d1/d2. The supplier-specific promise is the supplier SoW clause
that hands its obligation to DEL-10-03. SoW hashes were **checked by O-E**
on 2026-10-04.

| Entry | Supplier SoW (sha256 prefix) and clause naming DEL-10-03 | Supplier mirror row | Later decisions bearing on it | Design label and section | Supplier's verification section |
|---|---|---|---|---|---|
| S-1 | DEL-02-01 `9479fc88…` CLM-002 | DEP-02-01-040 | Receiver clause SC2-02-01-2 (applied by SCA-V4-003) | WD-v0.9 §9 | WD §13 "Verification cases (designed, not run)" |
| S-2 | DEL-02-03 `625b299e…` CLM-003 | DEP-02-03-040 | DECISION-4 D4-1 (Phase 1); R8-1 | EXEC-v0.7 §2, §3, §4, §10 | EXEC §3 (VER-001), §4 (VER-002, VER-003) |
| S-3 | DEL-02-04 `2327508f…` CLM-002 (SC3-02-04-9) | DEP-02-04-018 | K-9 as amended by L-2; D-GOV-52 (R23-30) | ROLE-v0.2 §3–§6 | ROLE §11 "Verification (designed; nothing qualified)" |
| S-4 | DEL-03-01 `48f0496c…` CLM-002 | DEP-03-01-042 | — | C-v0.8 §8 | C "Verification cases" |
| S-5 | DEL-03-02 `e2f8d49d…` CLM-004 | DEP-03-02-033 | R5-2; R8-1 | P-v0.8 §1, §13 | P §1 (VER-003, VER-014); "Verification cases" |
| S-6 | DEL-04-01 `2cd1dc9e…`: **no clause names DEL-10-03** | **None** | DECISION-1 D2; R23-8 (A16) | ACT-POLICY-v0.11 §2.1, §3, §8 | ACT §11 (VER-008); "Verification cases" |
| S-7 | DEL-04-03 `b8b58d67…` REQ-005 (SC2-04-03-1) | DEP-04-03-045 | R23-8, R23-24 (A16, package record) | RS-v0.10 §2, §13, §14 | RS "Verification cases" |
| S-8 | DEL-05-01 `6fdf4d59…`: **no clause names DEL-10-03** | **None** | SCA-V4-001 (V4-HOST-01, person-chosen model); DECISION-3 | LOOP-v0.9 §10.1 | LOOP "Verification cases" |
| S-9 | DEL-05-02 `beb9c66c…`: **no clause names DEL-10-03** | **None** | DECISION-3 | PANEL-v0.9 §6 | PANEL "Verification cases" |

### 3.2 Reverse: does any supplier record name DEL-10-03 outside the population?

Checked by O-E with `prototype/ra_check.py`:
- **Supplier SoWs.** Every supplier SoW clause naming DEL-10-03 belongs to an
  entry in §1.2: DEL-02-01 CLM-002, DEL-02-03 CLM-003, DEL-02-04 CLM-002,
  DEL-03-01 CLM-002, DEL-03-02 CLM-004, DEL-04-03 REQ-005.
- **Registers.** Every ACTIVE register row in the repository that targets
  DEL-10-03 is either one of DEL-10-03's own rows or a supplier mirror in
  §3.1: DEP-02-01-040, 02-03-040, 02-04-018, 03-01-042, 03-02-033 and
  04-03-045, plus DEL-10-04's (DEP-10-04-007), DEL-11-01's and DEL-11-02's consumer rows (X-1).

**Result.** No promise handed to DEL-10-03 lies outside the bound, and no
entry lacks an accepted source.

### 3.3 Relocation check: the seed's shared layer (REQ-002, REQ-003)

- **The seed.** Seed V4-ARC-20 (original-seed `ARCHITECTURE.md`
  `8d147421…`) put five things in "a shared TypeScript layer":
  - the workflow format and its declared checkpoints;
  - role guidance;
  - the record format;
  - the capability-catalog contract types;
  - interface components used by the App and hosts.
- **Current V4-ARC-20** keeps the meanings ("Shared contracts cover
  workflow/checkpoint meaning, role guidance, record identity, catalog
  semantics and human acts"). It makes their allocation "follow actual
  consumer responsibilities in the SoWs".
- **Every seed item has a v4 owner** (S-1/S-2, S-3, S-7, S-4 and S-9/S-8),
  and its placement is open under OI-014.

**Inference.** The relocation drops the *layer*, not any promise; nothing
was lost.

### 3.4 Finding F-RA1: three joins are recorded on one side only

**States.** DEL-04-01, DEL-05-01 and DEL-05-02 supply DEL-10-03 on admitted
arcs (DEP-10-03-013, 015, 016). Yet:
- their SoWs do not name DEL-10-03;
- their registers hold no DOWNSTREAM mirror.

Their Design files do acknowledge the consumer: ACT §10.3, LOOP §10.4 and
the PANEL Receivers line.

**Inference.** Each would be a supplier-side DOWNSTREAM row of an existing
admitted arc, dispositioned **MIRROR (SR-6)** as DAG-004 treats every such
row (its six existing siblings to DEL-10-03 are all MIRROR). So no new arc
and no SCC (R23-2).

**Precedent.** DAG-004 `HANDOFF_STATE.md` "Open matters" routes "Five
expected mirror rows not extracted … Each arc exists through the
consumer's row; no graph effect" to a named owner. F-RA1's three are not
among those five; they are added to the same kind of routing. Adding register rows or
SoW clauses is outside O-E's write area and is an escalation condition. It
goes to the register and SoW owners at the next amendment, as R23-32 F-R15
treats missing rows. Nothing depends on it now: the consumer rows carry the
arcs.

## 4. Historical applicability; consumer, packaging and tool-path account (OUT-003; REQ-003, REQ-004; AC-003, AC-004)

### 4.1 Historical applicability

| ID | Original statement (preserved at) | Later decision | Present applicability | Continuing obligation kept |
|---|---|---|---|---|
| H-1 | Seed V4-OPS-12 "**Precedence.** Root governance, then the v4 project's own instructions, then the accepted v4 basis … then the manuals" (original-seed `OPERATING_METHOD.md` `8f53b266…`) | Directions A/C; HTML-D01 (accepted under J); current V4-OPS-12: "The original draft's Root-first hierarchy is superseded by A/C and accepted HTML 01 at this scope" | Superseded for v4's purpose and commitments. Root governance still governs work in the Root repository (Root `AGENTS.md`), which the current text does not remove ("Root location alone supplies no blanket precedence over that direction") | Root's own instructions for repository work |
| H-2 | Seed V4-OPS-14: adoption "needs … a thin project loop file … created … as an instruction change" | Current V4-OPS-14: "not a mandatory new hierarchy … exact form is implementation definition" | Superseded as a mandate. The actual entry is `init/` plus `loop/LOOP_INIT.md` (EB B-19); there is no project `AGENTS.md` | LOOP_INIT's loop procedure |
| H-3 | Seed V4-ARC-20: one shared TypeScript layer (§3.3) | Current V4-ARC-20 (B-HTML 01–02) | Superseded as an allocation; meanings kept (§3.3) | OI-014 placement before structural allocation |

Each original remains intact under `original-seed/` (EB §6 rows; V4-OPS-13).
The complete thesis is preserved under `foundation/thesis/` (LOOP_INIT
"Project pointers"); the account touches neither.

### 4.2 Active consumers, packaging and tool paths (static traces only; VER-004 forbids network or migration)

| Consumer | Selector, path or record | Standing | Outstanding check and point of need |
|---|---|---|---|
| App v3 (`projects/chirality-app-dev`) | `frontend/scripts/prepare-packaged-instruction-root.mjs` (`fe0fa50d…`): `ROOT_FILES`, `PRODUCT_AGENTS_SOURCE` = `projects/chirality-app-dev/instructions/AGENTS.md`, `DOC_FILES`, `TOOL_FILES` (CLM-007) | Historical exemplar and fallback; the source inspection proves no build | None for v4. v3 retirement is DEL-11's (OI-024) |
| App v4 | PKG-v0.2 P-2 `Contents/Resources/workflows/` (DEL-02-02), P-3 `Contents/Resources/instructions/` (DEL-02-04) | PROPOSED; not built | Before relying on a v4 package's supply: compare P-2/P-3's actual contents with their Root and App sources (DEL-01-06's first-package checks) |
| Root | `AGENTS.md` (`f96feb19…`, D-GOV-52 applied); `workflows/` (bundled source tree) and generated `workflows/index.json` | Current | None now. Each Root instruction change routes notices (tranche manifests, `m6_notice`) |
| Runtime (`projects/chirality-runtime`) | D-GOV-52 notice | "notice delivered; receiving decision not recorded" (R23-32 F-R16) | Runtime's own decision (DEP-006; DEL-11-02) |
| Piping (`projects/chirality-piping`) and PEC | No D-GOV-52 notice. The tranche manifest states that they "hold no pin or copy of either passage and read Root AGENTS.md live" | States, from the manifest | Their own adoption arrangements (DEP-006) |

Handover: this section and §1.3 go to PKG-11 (DEP-10-03-019; F-R11) as the
consumer basis for DEL-11-02. No adoption is performed or claimed (CLM-005).

## 5. Verification design (VER-001…VER-006)

| VER | How | Status |
|---|---|---|
| VER-001 | Map (§2) against SOW-230 and CLM-001…006; each entry to its accepted source | Done for the population (§2, §3.1) |
| VER-002 | Two-way promise comparison (§3.1, §3.2), relocation (§3.3) | Done; checks by `prototype/ra_check.py` |
| VER-003 | Applicability against SEED and later direction (§4.1) | Done for H-1…H-3, with the seed hashes checked by O-E |
| VER-004 | Selector and tool-path chain from CLM-007 (§4.2), static only | Done as static traces; build and runtime checks are outstanding at their points of need |
| VER-005 | Against PKG-02…05 interfaces and ARCH (§2.3) | Done: no common implementation named; direction retained |
| VER-006 | Exclusions and attribution | `check_boundary_owner_resolution.py` on this SoW: 1 checked, 0 failing (O-E, 2026-10-04). Semantic follow-up: §2 assigns every act to its owner; F-RA1 is routed, not performed; the S-6 row was made by O-A, its owner |

**`prototype/ra_check.py` (checked by O-E).** It recomputes:
- the sha256 of each supplier Design file and supplier SoW cited in §1.2 and
  §3.1, against this file's prefixes;
- DEL-10-03's ACTIVE EXECUTION rows against the population;
- the reverse scan in §3.2;
- that F-RA1's three suppliers still lack a mirror (so a later mirror is
  noticed).

Negative cases are in its `--self-test`.

## Changes

**RA-v0.2 (2026-10-04), after RV3-RA1 (RA-v0.1 READY; 2 MINOR):**

| Change | Cause |
|---|---|
| F-RA1 names the missing rows MIRROR (SR-6), not SAME_ARC, and cites DAG-004's handoff "Open matters" as the routing precedent | RA1-R1 |
| S-6 re-pinned deliberately to ACT-POLICY-v0.11 (`597f13bd…`, committed at `0bd6e4b4e9`). The §10.3 mapping is recorded as done, and adoption is checked in the returned file | RA1-R2; R23-21 |
| `ra_check.py` H-1 reports a moved supplier as a NOTICE with a re-pin instruction, not a failure. `--strict` restores failure on drift. The self-test checks both | RA1-R2 |
