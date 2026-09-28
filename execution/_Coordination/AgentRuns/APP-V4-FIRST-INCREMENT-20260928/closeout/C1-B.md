# C1-B — bounded closeout comparison: DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-01-01

- Node: C1-B, run `APP-V4-FIRST-INCREMENT-20260928`. Method:
  `chirality-root:bundled:workflow:bounded-reconciliation` (read-only
  comparison; proposals only). Executor: Type 2 TASK (Claude Code subagent);
  no delegation, read-only git, no network.
- **Candidate:** commit `c7f5513db`. Every file below was read with
  `git show c7f5513db:<path>` into a private scratch folder.
- **Boundary (BRIEFS "C1", binding).** DAG-001 `SOURCE_MANIFEST.sha256` binds
  every `ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`. This node
  therefore edits **none** of them, nor `_STATUS.md`, `_CONTEXT.md` or
  `_REFERENCES.md`. Each warranted change is returned below as a **proposed**
  change for a successor route: SoW revision for SoW text, and register update
  plus `project-dag` departure (DAG-002) for new arcs. Nothing here is applied.
- **Rulings read** (unchanged between `c7f5513db` and the working tree):
  - OWNER_DECISIONS `a9869129…` (DECISION-1 D1–D4; DECISION-2 D5, D6);
  - R1 `2f9c7e72…`; R2 `77cfb845…`; R3 `202d52c7…`; R4 `50a009b2…`;
    R5 `254d0b93…`.
  - Register findings: V1-A §6, V1-B §6, V1-C §7, IR1-B §5, R2-CANDIDATES
    X-16, R4 "Carried to C1", and each Design file's findings/UNRESOLVED.
  - Sibling returns `closeout/C1-A.md` and `C1-C.md` (as present in the
    working tree) were read only to align the arc numbering and to avoid
    double proposals.

| DEL | ScopeOfWork.md | Dependencies.csv | _STATUS.md | Design file(s) at `c7f5513db` |
|---|---|---|---|---|
| DEL-03-01 | `179a6d35…` | `36f9efd7…` | INITIALIZED | C-v0.5 `CATALOG_AND_READ_BASIS.md` `a6306bd4…` (772 lines) |
| DEL-03-02 | `42328987…` | `adabeccc…` | INITIALIZED | P-v0.5 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` `a5ee4946…` (705) |
| DEL-03-03 | `5ac5db97…` | `a962d4d5…` | INITIALIZED | ADAPTER-v0.3 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` `c9195851…` (1,099) |
| DEL-03-04 | `203c0928…` | `b41eacd0…` | INITIALIZED | GUIDE-v0.2 `HOST_INTEGRATION_GUIDE.md` `5a9507e9…` (621) |
| DEL-01-01 | `eddd122c…` | `008863b1…` | INITIALIZED | HOSTING-BOUNDARY-v0.5 `873e76f6…` (1,110); PIN-SPIKE-v0.1 `0e090a4c…` (351); `generated/0.158.0/` (18 committed files) |

**Drift after the candidate.** The working tree carries uncommitted R6
in-place edits (`R6_RESOLUTIONS.md`, untracked) to HOSTING, C, P and ADAPTER,
and to ACT. R6 changes no SoW or register. It amends the hold-support
classification (R6-1, by held actions). It also closes HOSTING U-25/F-22
(R6-4). Where this record cites R5-1 values, read them "as amended by R6-1".
The comparison itself stays bound to `c7f5513db`.

**Classification used.** *Developed* means the 60% definition is present and
what remains is only implementation, qualification, a host input or a
witness. *Partially developed* means some definitional content, or a choice
the definition must carry, is still open. Register proposals are either
*mirror only* (the arc already exists on one side; no topology change) or
*new arc* (a topology change; needs DAG-002). Arcs are written consumer →
supplier, as in DAG-001. "Rep. row" means the consumer's UPSTREAM row, which
DAG-001 SR-6 uses as the arc representative.

## Summary

| DEL | OUT developed / partial / not addressed | Proposed SoW changes | Proposed register changes: mirror only / new arc (rep. row here) | Lifecycle observation |
|---|---|---|---|---|
| DEL-03-01 | 2 / 1 / 0 (OUT-002 partial) | 5 | 8 / 1 (+1 notes-only row) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-03-02 | 3 / 0 / 0 | 5 | 7 / 2 (+1 notes-only row; 1 value normalization) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-03-03 | 2 / 1 / 0 (OUT-001 partial) | 5 | 2 / 5 (+1 notes-only row) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-03-04 | 1 / 2 / 0 (OUT-002, OUT-003 partial) | 6 | 12 / 3 (+1 notes-only row) | INITIALIZED; IN_PROGRESS would be truthful |
| DEL-01-01 | 1 / 3 / 0 (OUT-002, OUT-003, OUT-004 partial) | 3 | 4 / 0 (+2 notes-only rows; supplier of 6 proposed arcs) | INITIALIZED; IN_PROGRESS would be truthful |
| **Total** | 9 / 7 / 0 | **24** | **33 / 11** | — |

No OUT is *not addressed*. Mirror rows marked "(observed)" below come from a
row-level check of the candidate registers, not from a review finding. The 11
new arcs, together with every arc proposed in C1-A and C1-C (40 distinct arcs
in all), leave DAG-001's SCC membership unchanged. I checked this by
recomputing SCCs over the candidate registers plus the proposed arcs. Arcs
among SCC-002 members go to the non-gating candidate layer.

---

## 1. DEL-03-01 — Capability catalog and read-basis contract (C-v0.5)

### 1.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 catalog and read-basis schema meaning | §2, §3 (elements 1–9), §3.1–§3.3, §4, §5, §6, §7 | **Developed** | Representation, serialization and identity algorithm stay unselected (TBD-003; U-C1). This is *implementation agreement*, not a missing definition. The actual host catalog is a host input (U-C7; DEP-03-01-025) |
| OUT-002 three-surface responsibility map | §8 | **Partially developed** | The skeleton names every consumer, owner and receiving point. Every H/E/X cell is *unagreed*. Generation or check routes need agreement with the host owner, and the extension promise needs `UNRESOLVED{OI-003}`. Remaining: definitional agreement with the host (not implementation) |
| OUT-003 contract fixtures and comparison evidence | §10 (FX-PIPE-01), Verification cases VC-C-01…08 | **Developed** (designed, not run) | Execution, and any host-supplied integrated witness (DEL-09-09) |
| REQ-001 one catalog; three consumers | §2 inv. 1–2; §8 | Developed | Host conformance |
| REQ-002 entry fields; adopted classes | §3, §3.1 (D2/D3 applied; five class values) | Developed | Consequence vocabulary is empty pending DEL-04-01 U-02. Operation-specific additions wait on OI-021 |
| REQ-003 read parity; unavailable parity | §4.1, §4.2, §4.4, §6.1 | Developed | Host evidence |
| REQ-004 basis on every read; relied-on basis in later action | §5.1–§5.4, §9 | Developed | AC-004 is **held** until an actual candidate-bound M3-CP return exists (§9; U-C8). Host definitions of generation and subject-identity scope are pending (U-C2, U-C3) |
| REQ-005 standing; no strengthened claims; act separation | §6.2 | Developed | — |
| REQ-006 responsibility map; extension promise preserved | §8 | Partially developed | Same as OUT-002 |
| REQ-007 no foreign acts | §1 | Developed | — |

### 1.2 Result → commitment (beyond or outside the SoW)

| Addition | Where | Authority |
|---|---|---|
| Exposure per surface (element 9), independent of class | §3 #9; §2 inv. 5 | R-9; R2-4 (INTEGRATION) |
| Fifth class value *no policy basis* with reason | §3.1 | R2-1 (INTEGRATION) |
| Subject content identity and identity-method designation | §5.1, §5.3 | R-6 |
| Per-item "no longer holds" rule | §5.4 | R2-13 (INTEGRATION) |
| Catalog edition; version-equality rule; open description | §2, §3.2, §2 inv. 4 | **PROPOSED** by this contribution (V1-C D-27, AB-08, AB-09). No ruling. The open-description extension of V4-SHR-02 is flagged F-C9 |
| Non-mutating basis rule | §5.4 | PROPOSED (V1-B X-07); host confirmation U-C10 |
| Precondition versus validation error | §4.4 | IR1-B B-m6 |
| *Channel not enabled* reporter; model-destination note | §4.1 | R4-13, R4-16; D5 (SETTLED) plus R5-4 (INTEGRATION reading) |
| **Shared fixture catalogue FX-PIPE-01** (all files cite it) | §10 | R-9, R2-21. §10 itself states it is an integration assignment, **not SoW scope**. No SoW change is proposed. If it is to remain a maintained product after this undertaking, its custody is a decision for the integrator/owner (open item 1.5) |
| Evidence-label mapping (C/LOOP/PANEL) | Verification cases | V1-B D-19; IR1-B B-m5 |

None of these is unsupported: each is labeled with its ruling, or as PROPOSED.

### 1.3 Proposed SoW corrections (`DEL-03-01/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds |
|---|---|---|---|---|
| S-01-1 | REQ-002, last sentence | "Preserve the declared none/may-apply/proposal-only/reserved distinctions, with unresolved concrete assignments explicit rather than silently applying the historical blanket reserved list." | "Preserve the declared none/may-apply/proposal-only/reserved distinctions, and represent an operation without an adopted class explicitly (no policy basis) rather than silently applying the historical blanket reserved list. The first-increment App/shared reserved acts and routine-permission treatment are those adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 and carried by DEL-04-01; operation-specific additions remain OI-021 and host adoption remains DEP-001." | DECISION-1 D2/D3; R-2; R2-1; IR1-B §5 "Basis findings for C1"; C UNRESOLVED last row |
| S-01-2 | TBD-001 | "OI-001/OI-002 (P OQ-02): the owner with App/SWB contract owners must resolve concrete reserved-act and classifier policy before the affected operation-policy production contract or permission implementation. …" | "OI-001/OI-002 (P OQ-02): ruled for the first increment at App/shared level by owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 (five reserved acts) and D3 (routine tool permission is the App user's own Codex setting; no classifier mode in hosts), carried by App v4 DEL-04-01. Still open: operation-specific additions (OI-021) and host adoption and enforcement (DEP-001). The field obligations remain included; conformance claims that depend on an unadopted assignment remain held." | Same. OWNER_DECISIONS "Effects" leaves the pointer reconciliation to C1 |
| S-01-3 | OUT-001 ("canonical content hash"), REQ-004 sentence 1, VER-004 sentence 1 | "…workspace identity, generation, model revision and canonical content hash…" | Keep the four elements, and add after "canonical content hash": "(received as a canonical content identity with its identity-method designation; the algorithm stays unselected under TBD-003)". | R-6; C §5.1. The claim-granularity *lift*: the source (V4-HI-11) term is kept, and the stable claim is added. The anchor row DEP-03-01-017 (SOW-167) is accepted ledger text and is not changed |
| S-01-4 | REQ-004, new sentence (**scope addition; owning decision required**) | — | "Each object or row in a read result also carries a host-supplied subject content identity with its method designation, distinct from the read-level identity, for per-item basis checks, act binding and lapse." | R-6 (V1-B D-02, BLOCKING). DEL-04-03 L-1 and DEL-03-02 R2-13 rely on it. The SoW does not state it now |
| S-01-5 | REQ-002, element list (**scope addition; owning decision required**) | "…meaningful errors; and human-act/autonomy class…" | Add: "; and host-declared exposure per consumer surface, independent of class" | R-9; R2-4; C §3 #9. The SoW scope row SOW-165 already ties generated surfaces to the extension question |

Optional companion (not counted): add `OWNER_DECISIONS.md` DECISION-1 to
`_REFERENCES.md` as a pointer.

### 1.4 Proposed register changes

**Mirror only** (rows in `DEL-03-01/Dependencies.csv`; the arcs already exist):

| # | New row | Mirrors | Source |
|---|---|---|---|
| M-01-1 | DOWNSTREAM HANDOVER → DEL-05-01 | DEP-05-01-014 | V1-C RF-1 |
| M-01-2 | DOWNSTREAM HANDOVER → DEL-05-02 | DEP-05-02-006 | V1-C RF-1 |
| M-01-3 | Retire DEP-03-01-022 (DOWNSTREAM → **PACKAGE** PKG-02, non-topological in DAG-001). Replace it with DOWNSTREAM HANDOVER → DEL-02-01 | DEP-02-01-017 | V1-C RF-3 |
| M-01-4 | … and DOWNSTREAM HANDOVER → DEL-02-03 | DEP-02-03-011 | V1-C RF-3 |
| M-01-5 | DOWNSTREAM HANDOVER → DEL-03-03 | DEP-03-03-006 | (observed; C header Receivers) |
| M-01-6 | DOWNSTREAM HANDOVER → DEL-03-04 | DEP-03-04-005 | GUIDE F-4 (only DEL-03-02 mirrors the guide) |
| M-01-7 | DOWNSTREAM HANDOVER → DEL-09-09 | DEP-09-09-007 | (observed) |
| M-01-8 | DOWNSTREAM HANDOVER → DEL-10-03 | DEP-10-03-011 | (observed; DEL-10-03 is outside D1) |

**Notes only (no topology):** DEP-03-01-024 (UPSTREAM PREREQUISITE
DEL-04-01), Notes. Add: "OI-001/OI-002 ruled for the first increment by
DECISION-1 D2/D3 (App/shared); the adopted classes are carried in DEL-04-01
ACT §6. Operation-specific additions stay open (OI-021). The satisfaction
status is unchanged." Source: V1-A RF-04.

**New arc, rep. row here:**

| # | Arc | New row | Grounds | Layer |
|---|---|---|---|---|
| N-B1 | **DEL-03-01 → DEL-04-03** | UPSTREAM INTERFACE DEL-04-03: act field set (§6.1) and lapse vocabulary (§7) carried in read-result standing | C §6.2 rows "Human-act evidence" and "Lapse state"; V1-B RF-03. The only existing row is the package-level DEP-04-03-012 (→ PKG-03, non-topological). Same arc as C1-A N-11 | held (SCC-002) |

**Supplier side of arcs whose rep. row is elsewhere (concurred; the optional
DOWNSTREAM mirror would go here):**
- DEL-04-02 → DEL-03-01 (C1-A N-01; V1-B RF-05);
- DEL-04-03 → DEL-03-01 (C1-A N-10; V1-B RF-04; C §5.3 uses);
- DEL-09-06 → DEL-03-01 (C1-C #6).

**Considered, not proposed.** DEL-04-01 → DEL-03-01. C lists DEL-04-01 as a
receiver for fixture re-pointing only (R-9). That is a citation of the shared
fixture, not a production input. As an arc it would pull DEL-04-01 (and two
more nodes) into SCC-002, enlarging it to 16 members.

### 1.5 Open items

| Item | Owner | Point of need |
|---|---|---|
| `UNRESOLVED{OI-003}` extension promise (retain/narrow/defer); every §8 cell *unagreed* | Owner with host contract owner (DEP-03-01-027); trace from DEL-09-09 (DEP-03-01-030) | Before an extension claim or fixing the AC-007 criterion |
| U-C1 serialization, identity algorithm, method-designation scheme, placement (TBD-003) | App/shared capability-contract owner with host/consumer owners (DEP-03-01-028) | Before dependent schema implementation |
| U-C2 generation; U-C3 subject-identity scope and per-item stale rule; U-C4 multi-read reliance; U-C10 non-mutating basis | Host owner (DEP-001; relay SQ-03, SQ-07) | Before basis, stale and lapse conformance |
| U-C8 actual M3-CP return; AC-004 held | DEL-03-02 | AC-004 closure |
| Consequence vocabulary (DEL-04-01 U-02); `UNRESOLVED{OI-021}` additions | DEL-04-01 with host policy owner; owner via outside SWB session | Before class assignment for connected operations |
| `UNRESOLVED{OI-013}`/`{OI-014}` loop-side checking and shared types | Named owners | Before structural/production allocation |
| Custody of FX-PIPE-01 after this undertaking (see 1.2) | Integrator/owner (R-9 owner) | Before the next undertaking reuses it |

### 1.6 Lifecycle observation

The state is INITIALIZED (`_STATUS.md`, 2026-09-27). Active agent production
under the owner's undertaking has produced C-v0.1 to C-v0.5 in `Design/`, with
independent comparisons and reviews. SPEC §3.4 and TYPES define `IN_PROGRESS`
as "active human + agent work underway". **IN_PROGRESS would now be the
truthful state.** The transition belongs to the human or WORKING_ITEMS. It is
not made here.

---

## 2. DEL-03-02 — Proposal, validation and outcome contract (P-v0.5)

### 2.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 proposal/basis/origin/outcome schema meaning | §3.1–§3.4, §9 | **Developed** | Identity, encoding, de-duplication and recovery mechanics are open (U-P1; TBD-002; DEP-03-02-026): *implementation agreement* |
| OUT-002 lifecycle, one route, parity, host ownership, receiving seams | §1, §2, §4, §5–§8, §10, §13 | **Developed** | Host route, views and receipts are host inputs (U-P2) |
| OUT-003 contract fixtures | §11, §14, VC-P-01…14 | **Developed** (designed, not run) | Execution; the joined witness (DEL-09-09) |
| REQ-001 one route | §2 | Developed | Host evidence |
| REQ-002 host truth; no upgraded result | §1; VC-P-03 | Developed | — |
| REQ-003 origin/attribution/basis | §3.2, §3.3 | Developed | Host origin mark and caller verification (U-P2; SQ-14) |
| REQ-004 lifecycle and direct branch | §4.1–§4.4 | Developed | — |
| REQ-005 outcome unknown | §4.1 rule 3; §9 | Developed | Recovery mechanics (TBD-002) |
| REQ-006 stale refusal and re-draft | §5 | Developed | Host confirmation of the per-item rule (U-C3; U-P3) |
| REQ-007 no retargeting | §6 | Developed | — |
| REQ-008 repeated submission, one effect | §7 | Developed as a testable obligation | The one-effect evidence is a **host obligation** (R-7; DEP-001); the mechanism is unselected |
| REQ-009 host proposal views | §8 | Developed | Host-owned presentation (DEP-03-02-024) |
| REQ-010 success ≠ acceptance | §9, §10 | Developed | — |
| REQ-011 queued until recorded | §4.1 rules 1–2 | Developed | — |
| REQ-012 adopted policy; act distinctions | §2, §4.4, §10 | Developed (D2/D3 applied) | OI-021 additions; host adoption (DEP-001) |
| REQ-013 no foreign acts | §1, §13 | Developed | Registered boundary-owner checker not run (VC-P-14) |

### 2.2 Result → commitment

| Addition | Where | Authority |
|---|---|---|
| Change-item content identity; acceptance unit = change item | §3.1 | R-6 |
| Governing checkpoint constraint and constraint carriage assurance (only host-held satisfies R2-12; App-assured not available in this increment) | §3.3, §4.4 | R2-12; R4-14; R5-2 |
| *Refused — invalid/stale/not permitted*, *application error*, observer-attributed *outcome unknown* | §4.1, §4.2, §9 | R-7; R-3 |
| Per-item dispositions, item-left events, derived proposal state | §4.3 | R2-18; WD §4.3.7 confirmed by DEL-02-03 (R4-7) |
| Undo relation *reverses ⟨receipt⟩*; "applied, then reversed" | §4.5, §9 | R2-15; R3-4; R5-5 |
| Resulting objects in the applied association | §9 | R2-14 |
| Retry keeps identity; de-duplication before the basis check | §3.1, §5, §7 | R-7; R2-13 |
| Author identity *unverified* | §3.3 | R4-15 |
| Standing at drafting; two settings references | §3.3 | R-8; R2-6 |
| Pre-queue refusal leaves the proposal *drafted*; sibling drafts | §4.2; §3.1 rule 5 | **PROPOSED** (U-P4, U-P9) |
| M3-CP comparison design; SWBPIPE receiving risks | §11; §12 | BRIEFS W3 |

All are labeled; none is unsupported.

### 2.3 Proposed SoW corrections (`DEL-03-02/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds |
|---|---|---|---|---|
| S-02-1 | REQ-012 sentence 1; AC-013; TBD-001 | REQ-012: "…without assigning the unresolved global reserved list or routine-classifier policy." AC-013: "…preserves OI-001/OI-002 as unresolved at their stated points of need…" TBD-001: "OI-001 retains the global always-reserved human-act list … OI-002 retains routine-classifier permission treatment…" | REQ-012: "…consume adopted operation/autonomy and human-act distinctions — for the first increment the reserved acts and routine-permission treatment adopted by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 and carried by DEL-04-01 — without assigning operation-specific additions (OI-021)." AC-013: "…applies the adopted D2/D3 distinctions and preserves operation-specific additions (OI-021) and host adoption (DEP-001) as open at their points of need…" TBD-001: state the D2/D3 ruling, and name OI-021 additions and host adoption as what remains | DECISION-1; R-2; IR1-B §5; P UNRESOLVED last row |
| S-02-2 | CLM-003 sentence 2 | "HOST V4-HI-11 describes workspace identity, generation, model revision and canonical content hash; this deliverable carries that basis…" | "…and canonical content hash (received as a canonical content identity with its identity-method designation, plus the subject content identities of relied-on targets); this deliverable carries that basis…" | R-6; R2-13; P §3.2. A lift, as S-01-3 |
| S-02-3 | REQ-008 sentence 1; AC-009 | REQ-008: "Repeated submission of the same proposal shall have only one effect." AC-009: "…yields only one application effect; …" | REQ-008: "Repeated submission of the same proposal shall have at most one application effect per change item. This is a host obligation (CLM-002) that the contract makes testable; each submission is recorded separately with only the effects actually observed." AC-009: "…yields at most one application effect per item in the observed host receipts; an observed second effect is recorded as a failed host obligation, not hidden; …" | R-7 ("one effect is a host obligation to be evidenced, not a recorded fact"); P §7; GUIDE G-7. Touches a protected criterion, so it takes the owning route |
| S-02-4 | CLM-006; REQ-004 | CLM-006: "…or rejected, withdrawn or stale disposition." REQ-004: "…with rejected, withdrawn and stale dispositions from the queued proposal as stated in the source." | Keep the source-stated lifecycle. Add to REQ-004: "States and dispositions apply per change item (R-6). *Rejected* is only the person's A10 and *withdrawn* only the proposer's A11; a host refusal, including a stale one, is *refused*, not rejected (R-7)." | R-1; R-6; R-7; P §4.1 |
| S-02-5 | OUT-001 element list | "…including target binding, lifecycle meaning, host receipt references and the old/new-value information required by host proposal views." | Add: "; the change-item content identity; and any governing checkpoint constraint with its carriage assurance" | R-6; R2-12; R4-14; R5-2; P §3.1, §3.3. These are within SOW-170/171 meaning; stating them keeps OUT-001 truthful |

### 2.4 Proposed register changes

**Mirror only:**

| # | Register | New row | Mirrors | Source |
|---|---|---|---|---|
| M-02-1 | DEL-03-02 | DOWNSTREAM INTERFACE → DEL-03-01 (M3-CP return) | DEP-03-01-026 | V1-B RF-08; IR1-B §5; C §9 |
| M-02-2 | DEL-03-02 | DOWNSTREAM HANDOVER → DEL-05-01 | DEP-05-01-015 | V1-C RF-2 |
| M-02-3 | DEL-03-02 | DOWNSTREAM HANDOVER → DEL-05-02 | DEP-05-02-007 | V1-C RF-2 |
| M-02-4 | DEL-03-02 | DOWNSTREAM HANDOVER → DEL-10-03 | DEP-10-03-012 | (observed; outside D1) |
| M-02-5 | DEL-04-02 (C1-A register) | UPSTREAM INTERFACE ← DEL-03-02 | DEP-03-02-018 | V1-B RF-01 |
| M-02-6 | DEL-04-03 (C1-A register) | UPSTREAM INTERFACE ← DEL-03-02 | DEP-03-02-019 | V1-B RF-02 |
| M-02-7 | DEL-04-01 (C1-A register) | DOWNSTREAM HANDOVER → DEL-03-02 | DEP-03-02-017 | V1-A RF-02 |

**Notes only:** DEP-03-02-017, Notes. Replace "REQ-012 and TBD-001 preserve
OI-001/OI-002…" with a pointer to DECISION-1 D2/D3 and name the residual
OI-021. Source: V1-A RF-04.

**Value normalization (no topology):** DEP-03-02-016…026 carry
SatisfactionStatus `TBD`, while the neighbouring DEL-03-01, DEL-04-02 and
DEL-04-03 rows carry `PENDING` (V1-B RF-09). DEL-01-01 and DEL-03-04 rows also
use `TBD`. Both are valid enum values (TYPES §SatisfactionStatus). The
register owner should choose one convention for unfulfilled execution inputs
and apply it across registers in one pass.

**New arcs, rep. row here:**

| # | Arc | New row | Grounds | Layer |
|---|---|---|---|---|
| N-B2 | **DEL-03-02 → DEL-04-02** | UPSTREAM INTERFACE DEL-04-02: grant display states, grant value and scope, settings version identities | P §13 "Expect from DEL-04-02"; §3.3; §4.4; V1-B RF-06. Same arc as C1-A N-05 | held |
| N-B3 | **DEL-03-02 → DEL-02-01** | UPSTREAM INTERFACE DEL-02-01: workflow identity {kind, origin, source root, name, revision}; checkpoint declarations (required act, subject class, reached-when); WD §4.3.7 item rule | P §13 "Expect from DEL-02-01"; §3.3; §4.3; R-9; R2-12; R2-18. Not in C1-A | held |

**Supplier side (concurred):** DEL-02-01 → DEL-03-02 (C1-A N-18); DEL-02-03
→ DEL-03-02 (C1-A N-21); DEL-09-06 → DEL-03-02 (C1-C #7).

**Disagreement with C1-A N-12 (DEL-03-02 → DEL-04-03): not supported from
the supplier text.** P §13 has no "Expect from DEL-04-03" row. P receives
accepted/rejected acts from **host capture** (§4.1 "host-captured A5"; §10),
not from DEL-04-03 records. P cites RS L-6 and R11 only to say where its data
land (§3.3, §4.5). The package row DEP-04-03-012 (→ PKG-03) is fully
explained by C's use (N-B1). Recommend retargeting that package row to
DEL-03-01 only, and not adding N-12. The integrator should decide. Either way,
SCC membership is unchanged (checked).

### 2.5 Open items

| Item | Owner | Point of need |
|---|---|---|
| U-P1 identity/encoding/de-duplication/recovery mechanics (TBD-002) | Contract and host owners (DEP-03-02-026) | Before dependent implementation |
| U-P2 host route, views, receipts, resulting objects, capture evidence, settings at application | Host owner (DEP-03-02-023; SQ-01, SQ-05, SQ-08–SQ-10, SQ-22) | When integration or a witness relies on them |
| U-P10 host receipt of the governing constraint versus the host's own declaration copy | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 (SQ-02) | Before V-CP1 / LOOP FX-C9 / PANEL PC-24 / WD VC-11 |
| U-P3, U-P4, U-P5, U-P6, U-P7, U-P8 host confirmations | Host owner | Before application-path, withdrawal and undo implementation |
| U-P9 sibling-draft grouping | DEL-05-01 with DEL-03-02 and host owner | Before FX-M8 |
| `UNRESOLVED{OI-014}`; `UNRESOLVED{OI-021}`; `UNRESOLVED{OI-003}` | Named owners | As in the SoW TBDs |

### 2.6 Lifecycle observation

INITIALIZED. P-v0.1 to P-v0.5 were produced under active work, so
**IN_PROGRESS would be truthful**. Not changed here.

---

## 3. DEL-03-03 — Local external-agent receiving adapter (ADAPTER-v0.3)

### 3.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 App-side native MCP/CLI configuration and adapter "as needed" | §2, §4, §5, §6; §9 OC-1…OC-12 | **Partially developed** | Transport family, realization family, configuration locus and native-to-catalog mapping are **unselected** (TBD-007; OC-1, OC-2, OC-3, OC-8). Native mapping is PROPOSED and stays *not established* without a host mapping (NM-2; SQ-12). This is definitional choice work owed by the App external-host integration owner with the host, **plus** implementation (no code) |
| OUT-002 enablement and policy interface account | §1, §3, §6, §7, §9, UNRESOLVED | **Developed** | Host enablement facility (SQ-28) and host behavior (SQ-13) are host inputs |
| OUT-003 consumer fixtures | §10 (XF-01…XF-42, local subjects) | **Developed** (designed, labeled simulated) | Execution on a test double, then host variants (AWAITING INPUT), then the DEL-09-09 join |
| REQ-001 native receiving; identity, availability, standing, basis preserved | §4.1–§4.5 | Partially developed | Mapping (OC-8, SQ-12); transport choice |
| REQ-002 machine-local, off unless enabled; distinct disabled/unavailable; no grant | §3.1–§3.5 | Developed (D5 applied) | SQ-28; SoW text predates D5 (S-03-2) |
| REQ-003 same route and policy; checkpoints | §5.3, §6, §7.7 | Developed at definition | App holds `UNRESOLVED{D6}`; host holds depend on SQ-02 |
| REQ-004 shared outcome contract; acts not fabricated | §7.1–§7.6 | Developed | Capture-evidence reference (SQ-01) |
| REQ-005 no foreign acts | §1 | Developed | — |
| REQ-006 availability/candidate/contribution identification; handoff | §9, §10, §11, §12 | Developed (definition) | Actual endpoint and candidate identities exist only at implementation |

### 3.2 Result → commitment

| Addition | Where | Authority |
|---|---|---|
| Four channel states, and the qualifier *enablement unconfirmed* | §3.2 | BRIEFS W8; DERIVED from S-X2 and HOSTING H8 |
| App-side configuration is never A13 evidence; the host refusal is the authoritative "off"; the VER-002 reading | §3.3 E-2, E-3 | R4-13 (INTEGRATION) |
| App configuration is person-directed | §3.3 E-4 | **PROPOSED** |
| Model destination recorded per turn and shown; no gate | §3.1, §3.4 | D5 (SETTLED: flow, no gate); R4-1, R5-4 (INTEGRATION reading: record and show) |
| Carriage assurance on dispatch; hold-support values | §5.1–§5.3, §7.7 | R4-14; R5-1; R5-2 |
| Proposal-identity rules PI-1…PI-6 | §5.6 | PROPOSED; host SQ-08 |
| Draft PR #885 cited as evidence only | §9 | BRIEFS W8 (evidence, not commitment) |
| Relay mapping to RELAY SQ-01…SQ-32 | §12 | R5-9, R5-10 |

None is unsupported.

### 3.3 Proposed SoW corrections (`DEL-03-03/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds |
|---|---|---|---|---|
| S-03-1 | TBD-001, TBD-002 | TBD-001: "…Choose always-reserved acts by concrete operation and consequence. This adapter consumes the resulting adopted policy…" TBD-002: "…Distinguish routine tool permissions from professional acts and settle App/host treatment. No old drafting default is selected here." | TBD-001: "OI-001 ruled for the first increment by DECISION-1 D2 (App/shared); this adapter consumes the adopted list through DEL-04-01. Operation-specific additions: OI-021. Host adoption: DEP-001." TBD-002: "OI-002 ruled by DECISION-1 D3: in the App, routine tool-permission and sandbox modes are the user's own Codex setting; hosts have no classifier mode." | DECISION-1; ADAPTER F-10 (carried to C1 by R4) |
| S-03-2 | REQ-002 sentences 3–4; AC-002 | REQ-002: "The adapter shall carry the selected local/privacy data boundary without treating enablement as permission for another data destination. Host local operation retains V4-HOST-02's configured-model-server data limit; this requirement does not silently assign that host rule to every App conversation or select a model/transport." AC-002: "Disabled access produces an explicit disabled result and no host request; … enablement supplies no additional autonomy or data-destination grant." | REQ-002: "Host content read over the channel may flow to the model the person selected for the App conversation, cloud included; the App gates neither enablement nor requests on that destination and adds no other destination (no App relay, telemetry or remote endpoint) (DECISION-2 D5). The App records the observed model destination and shows it in the channel status as information (INTEGRATION, DECISION-2 reading). A host may restrict its own channel (DEP-001); V4-HOST-02 continues to govern the host's embedded agent." AC-002: "Disabled access produces an explicit disabled result and no App-originated host request; the host's refusal is the authoritative 'off' for agent-originated requests; … enablement supplies no autonomy grant and adds no destination beyond the conversation's selected model." | DECISION-2 D5; R4-1; R4-13; R5-4; ADAPTER F-14, F-2, §3.3 E-2, §3.4. Protected criterion, so the owning route applies |
| S-03-3 | REQ-003 sentence 2 | "Direct application is permissible only within the person's grant and operative host policy; otherwise the request remains a proposal." | "Direct application is permissible only under an effective direct treatment within the person's grant and operative host policy; otherwise a direct request is *not permitted* — never silently converted — and the agent may propose instead." | R-3 point 3 (INTEGRATION); P §2, §4.4; C §4.1. The present wording can be read as the conversion R-3 forbids |
| S-03-4 | REQ-003 sentence 3; VER-003 | REQ-003: "Workflow checkpoints retain their required human act." VER-003: "…exercise permitted direct operation, proposal-only, reserved-act refusal and checkpoint wait." | REQ-003: add "; on this channel the App claims no hold it cannot enforce: each checkpoint reports its hold support (EXEC §3.6 values per R5-1, as amended by R6-1) and records action during hold, with App-side holds `UNRESOLVED{D6}`." VER-003: replace "checkpoint wait" with "a checkpoint case that reports hold support and records action during hold (no App wait claimed while D6 is deferred)" | DECISION-2 D6; R4-2; R5-1; ADAPTER F-13 (carried to C1 by R4 with DEL-02-03 F-10) |
| S-03-5 | REQ-004 sentence 1 | "…duplicate submission's one-effect meaning…" | "…duplicate submission's at-most-one-effect-per-item meaning, which is a host obligation to be evidenced…" | R-7; P §7. Aligns with S-02-3 |

### 3.4 Proposed register changes

**Mirror only:**

| # | Register | New row | Mirrors | Source |
|---|---|---|---|---|
| M-03-1 | DEL-03-03 | DOWNSTREAM HANDOVER → DEL-03-04 | DEP-03-04-007 | ADAPTER F-11 (W8, carried by R4) |
| M-03-2 | DEL-04-01 (C1-A register) | DOWNSTREAM HANDOVER → DEL-03-03 | DEP-03-03-008 | (observed) |

**Notes only:** DEP-03-03-008 Notes, a pointer to DECISION-1 D2/D3 (as
DEP-03-02-017). DEP-03-03-009 stays EXTERNAL for the actual Codex capability.
If N-B4 is added, its Notes should name DEL-01-01 as the source of the pin
facts.

**New arcs, rep. row here** (all from ADAPTER F-11):

| # | Arc | New row | Grounds | Layer |
|---|---|---|---|---|
| N-B4 | **DEL-03-03 → DEL-01-01** | UPSTREAM INTERFACE DEL-01-01: supplier MCP/dynamic-tool surfaces and channel-status facts at pin 0.158.0; observed model destination | ADAPTER §3.5, §11 "Expect from DEL-01-01"; HOSTING §6.8, §8.3; F-11. DEP-03-03-009 names only an EXTERNAL "Codex native-tool capability" | admitted (no cycle) |
| N-B5 | **DEL-03-03 → DEL-04-02** | UPSTREAM INTERFACE DEL-04-02: grant display states and settings references | ADAPTER §5.5, §11; F-11. Same as C1-A N-06 | held |
| N-B6 | **DEL-03-03 → DEL-02-01** | UPSTREAM INTERFACE DEL-02-01: checkpoint declarations and derived constraints | ADAPTER §5.3, §11 (WD §4.2.2); F-11. Same as C1-A N-20 | held |
| N-B7 | **DEL-03-03 → DEL-02-03** | UPSTREAM INTERFACE DEL-02-03: hold machine, hold-support values, required-tool check | ADAPTER §7.7, §11 (EXEC §3.6); F-11. Same as C1-A N-27 | held |
| N-B8 | **DEL-03-03 → DEL-04-03** (conditional) | UPSTREAM INTERFACE DEL-04-03: record entry kinds R5/R7/R9/R11/R13 into which the adapter's evidence is written | ADAPTER header ("for joins only: DEL-04-03/RS … R5, R7, R11, R13"), §11 "Provide to DEL-04-03"; F-11 "rows to … DEL-04-03 (record entries)". C1-A proposes the reverse, N-14 (DEL-04-03 → DEL-03-03, RS consumes ADAPTER's entry list). Both directions are evidenced. Together they form a 2-cycle inside SCC-002 (no membership change). The register owner may keep only N-14 if the adapter is treated as supplier of entry content alone | held |

**Supplier side (concurred):** DEL-04-03 → DEL-03-03 (C1-A N-14); DEL-02-03
→ DEL-03-03 (C1-A N-24); DEL-09-06 → DEL-03-03 (C1-C #8).

**Considered, not proposed:**
- DEL-03-03 → DEL-09-06. ADAPTER expects RELAY as "the single relay channel",
  but the actual inputs are SWBPIPE answers, already carried by
  DEP-03-03-010/-011 (DEP-001).
- DEL-04-01 → DEL-03-03. ACT cites ADAPTER at v0.1/v0.2, but as an arc it
  would pull DEL-04-01 into SCC-002.
- DEL-04-02 → DEL-03-03 and DEL-05-01 → DEL-03-03. Their designs cite
  ADAPTER, but no review raised these. They stay inside SCC-002 if the
  register owner chooses to add them.

### 3.5 Open items

| Item | Owner | Point of need |
|---|---|---|
| TBD-007 / OC-1…OC-12 (transport, realization family, configuration locus, locality, authentication, carriage mechanism, mapping, hold mechanism) | App external-host integration owner with host owner | Before the App receiving implementation depends on the interface; before DEL-09-09 qualification |
| SQ-28 host enablement facility and capture-evidence reference (gates every live channel case) | Host owner (DEP-001) | Before enablement implementation and any live external case |
| `UNRESOLVED{D6}`: host-operation checkpoints on X wait for SQ-02; App-only checkpoints are a separate D6 follow-up (EXEC U-E23) | Owner | Before hold-machine fixtures on X |
| SQ-01 capture evidence; SQ-08 identity and durability; SQ-12 mapping; SQ-13 behavior; SQ-14 caller identity; SQ-16 host destination restriction | Host owner | As listed in ADAPTER UNRESOLVED |
| App restart custody (PI-6) | DEL-01-02 (later undertaking, D1) | Before XF-41 |
| Supplier behaviors not observed at 0.158.0 | DEL-01-01 with App implementation owner | Before implementation; at pin re-examination |
| G-9 / GUIDE F-13: ADAPTER §12 header still labels RELAY-v0.2 | DEL-03-03 | Next revision (label only) |

### 3.6 Lifecycle observation

INITIALIZED. ADAPTER-v0.1 to v0.3 were produced under active work, so
**IN_PROGRESS would be truthful**. Not changed here.

---

## 4. DEL-03-04 — Host boundary and integration guide (GUIDE-v0.2)

### 4.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 new-host checklist | §3 HC-0…HC-10 | **Developed** | HC-9/HC-10 conditional by design |
| OUT-002 responsibility/interface matrix | §2.0–§2.14 | **Partially developed** | Row 10 (connectors) is "not designed here" because DEL-07/08 are outside D1. Row 8 role supply and the App act control rest on SoW meaning only (G-1, G-2). These are definitions owed by deliverables outside this undertaking, not by the guide |
| OUT-003 completeness checks and recorded comparison | §4.1 CC-1…CC-11, §4.2–§4.4 | **Partially developed** | v0.2 has self-review only. The registered boundary-owner checker for VER-007 was **not run** (CC-7; F-9). Independent review of v0.2 is the running V4-B node |
| REQ-001 retain the map and HI §10 | §2.0–§2.10; CC-1, CC-3 | Developed, with limits G-1/G-2 | Outside-D1 definitions |
| REQ-002 catalog/proposal meanings | Rows 1–4 | Developed | Host evidence (relay pending) |
| REQ-003 act distinctions | Row 5 | Developed | SQ-01 |
| REQ-004 adopted policy; open classes | Row 6; §2.13 | Developed | SoW text predates D2/D3 (S-04-1) |
| REQ-005 workflow/loop/panel joins; data boundary | Rows 7–8; §2.14 | Partially developed | Role supply (DEL-02-04, outside D1); OI-013/OI-014; SQ-29…SQ-32 |
| REQ-006 PEC/Domains paths | Row 10 | Partially developed (by D1) | DEL-07-01/07-02/08-01/08-02 later |
| REQ-007 open issues and coordination states | §2.13; §4.3 | Developed | — |
| REQ-008 excluded acts | §2.12 | Developed | Checker not run |

### 4.2 Result → commitment

| Addition | Where | Authority |
|---|---|---|
| Hold-support map (four values; HS-1…HS-5) | §2.14 | R5-1 (R6-1 amends it in the working tree) |
| Relay-question homes (SQ-01…SQ-32) | §4.3 | R5-9, R5-10; coordinator instruction |
| Consumption of DEL-01-01 HOSTING/SPIKE, DEL-09-06 CA/RELAY and DEL-09-09 XT | Header; rows 7–9; §2.11 | Coordinator instruction for GUIDE-v0.2. **Not in the SoW receiving map** (CLM-002/CLM-003 list only DEL-02-xx, 03-01…03, 04-xx, 05-xx, 07-xx, 08-xx). Flagged: needs S-04-6 plus the new arcs N-B9…N-B11, or a statement that these are references only |
| Prefixing rule for colliding TBD identifiers | §0; F-12 | Local reading aid; no authority needed |

### 4.3 Proposed SoW corrections (`DEL-03-04/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds |
|---|---|---|---|---|
| S-04-1 | REQ-004 sentence 2; TBD-001; TBD-002 | REQ-004: "It shall carry each unresolved reserved-class and classifier decision at its exact owner and point of need in TBD-001/TBD-002." TBD-001: "…Choose always-reserved acts by concrete operation and consequence; global list not fixed…" TBD-002: "…settle App/host treatment; no historical drafting default is adopted." | REQ-004: "It shall carry the adopted D2/D3 distinctions (DECISION-1) and each remaining class decision (operation-specific additions, OI-021) at its exact owner and point of need." TBD-001/TBD-002: state the D2/D3 ruling for the first increment; the residue is OI-021 additions and host adoption (DEP-001) | DECISION-1; GUIDE F-5 |
| S-04-2 | Receiving map, row "Basis", column 3 | "…receive workspace identity, generation, model revision and canonical content hash" | "…canonical content hash (as a canonical content identity with its method designation) and per-subject content identities" | R-6; GUIDE G-7 |
| S-04-3 | Receiving map, row "Origin, undo and proposal presentation", column 4; REQ-002 | Row: "…stale/refusal, unchanged targets, duplicate-one-effect and unknown-outcome expectations from Q…" REQ-002: "…unchanged targets, duplicate-one-effect and truthful unknown/receipt outcomes…" | Replace "duplicate-one-effect" with "at-most-one-effect per item as a host obligation to be evidenced" in both | R-7; GUIDE G-7; aligns with S-02-3 |
| S-04-4 | Receiving map, row "Loop and panel", column 4; REQ-005 last sentence | Row: "…native endpoint/key boundary, local-server default and local-data constraint…" REQ-005: "Host local operation retains its configured-model-server-only data boundary." | Row: "…native endpoint/key boundary; for the host's embedded agent the local-server default and local-data constraint (V4-HOST-02); App conversations follow DECISION-2 D5…" REQ-005: "The host's embedded agent retains its configured-model-server-only data boundary (V4-HOST-02); App conversations reading host content follow DECISION-2 D5." | DECISION-2 D5; R4-1; GUIDE G-6 |
| S-04-5 | Receiving map, row "Autonomy", column 4 | "…declared checkpoints still wait; unresolved classes stay open" | "…declared checkpoints wait where hold support is enforced (host loop or host route); elsewhere hold support is reported and action during hold recorded, with App-run holds `UNRESOLVED{D6}`; unresolved classes stay open" | DECISION-2 D6; R4-2; R5-1 (as amended by R6-1); GUIDE §2.14, G-8 |
| S-04-6 | CLM-002 or CLM-003 (add sentence), with REQ-008 excluded-act list unchanged | — | "The guide also consumes App v4 DEL-01-01's supplier boundary (native surfaces for optional external access), DEL-09-06's relay questions (the host-contribution column) and DEL-09-09's external trace cases, citing them without performing their acts." | GUIDE F-4; header "Consumed inputs"; 4.2 above. Pairs with N-B9…N-B11 |

### 4.4 Proposed register changes

**Mirror only.** DEL-03-04 is only a consumer, so it needs no rows of its own.
Its suppliers lack DOWNSTREAM mirrors of DEP-03-04-008…019 (GUIDE F-4: "only
DEL-03-02 carries a mirror"). Twelve optional rows, one in each supplier's
register:
- DEL-02-01 → DEP-03-04-008;
- DEL-02-03 → -009;
- DEL-02-04 → -010;
- DEL-04-01 → -011;
- DEL-04-02 → -012;
- DEL-04-03 → -013;
- DEL-05-01 → -014;
- DEL-05-02 → -015;
- DEL-07-01 → -016;
- DEL-07-02 → -017;
- DEL-08-01 → -018;
- DEL-08-02 → -019.

The DEL-03-01 and DEL-03-03 mirrors are M-01-6 and M-03-1.

**Notes only:** DEP-03-04-011 Notes. Replace "OI-001 is needed before
operation-policy production contracts; OI-002 before permission-policy
implementation" with a pointer to D2/D3 and the OI-021 residue.

**New arcs, rep. row here** (GUIDE F-4):

| # | Arc | New row | Grounds | Layer |
|---|---|---|---|---|
| N-B9 | **DEL-03-04 → DEL-01-01** | UPSTREAM INTERFACE DEL-01-01: supplier boundary facts for rows 8–9 (HOSTING §6.7, §6.8, §8.2, §8.3; SPIKE) | GUIDE header; row 9 (M9.3); §2.11; F-4 | admitted |
| N-B10 | **DEL-03-04 → DEL-09-06** | UPSTREAM INTERFACE DEL-09-06: relay question identities and "App assumes meanwhile" texts (RELAY), connected-activity staging (CA) | §2.0 "Host contribution" column; §4.3; F-4 | admitted. DEL-09-06 does not reach DEL-03-04, because C1-C does not propose DEL-09-06 → DEL-03-04 |
| N-B11 | **DEL-03-04 → DEL-09-09** | UPSTREAM INTERFACE DEL-09-09: external trace and extension-trace cases for rows 1 and 9 | Row 9 "XT §3"; M1.6; F-4 | admitted |

**Reverse citations must not become arcs.** CA, RELAY and XT cite GUIDE-v0.1
as a reference.
- Adding DEL-09-09 → DEL-03-04 would merge DEL-03-04 and DEL-09-06 into
  SCC-002, making it 19 members.
- Adding DEL-09-06 → DEL-03-04 would create a new 2-node SCC with N-B10.

C1-C reaches the same conclusion ("considered, not proposed").

### 4.5 Open items

| Item | Owner | Point of need |
|---|---|---|
| Independent review of GUIDE-v0.2; run the registered boundary-owner checker (VER-007) | App manager (V4-B running; checker at a later node) | Before closeout acceptance of the guide |
| Every SQ-01…SQ-32 answer | SWBPIPE owner via the human relay | As stated per question |
| `UNRESOLVED{D6}` host-operation part (SQ-02); App-only follow-up U-E23 (G-8, F-10: E1 via X is *unsupported*) | Owner | Before any App-side positive hold case, and before offering such a workflow as supported |
| TBD-003 (OI-003), TBD-004 (OI-013), TBD-005 (OI-014), TBD-006 (OI-021), TBD-007…009 (OI-022/023/026) | As in the SoW | As in the SoW |
| G-1, G-2: definitions outside D1 (DEL-02-04, DEL-01-04, DEL-07-xx, DEL-08-xx) | Later undertaking | Before the guide claims rows 8 and 10 complete |
| F-11: CA-v0.3 §2.3 CA-H hold statement is unqualified by surface | DEL-09-06 (C1-C) | Before relay |

### 4.6 Lifecycle observation

INITIALIZED. GUIDE-v0.1 and v0.2 were produced under active work, so
**IN_PROGRESS would be truthful**. Not changed here.

---

## 5. DEL-01-01 — Stock Codex hosting and supplier contract (HOSTING-BOUNDARY-v0.5; PIN-SPIKE-v0.1)

### 5.0 Pin decision, spike record and generated output

- **D4 (DECISION-1).** Codex `0.158.0` is selected as the definition and
  generation pin for this undertaking. Upgrades are deliberate. The pin is
  re-examined before implementation starts, and the selection establishes no
  qualification (DEP-005). HOSTING applies this in its header, §7, §10, §11
  and U-01.
- **Spike W11** is recorded in `Design/PIN_SPIKE_0.158.0.md` (v0.1,
  `0e090a4c…`, "OBSERVATION RECORD … not qualification"). It gives the
  distribution identity and signing facts (§3), and deterministic generation
  of four variants (§4; SV-01 run twice, identical). The inventory is 170 TS
  client methods and 11 server-request kinds; TS and JSON Schema disagree on
  five elements (S-F-03). §5 covers the handshake, unknown-method error and
  exit facts. §6 has per-item verdicts P-01…P-15; the spike's own verdicts are
  kept in HOSTING §10. **Committed output:** the two JSON Schema experimental
  bundles, `MANIFEST.sha256` (lists all 2,359 generated files), `_spike/`
  (scripts, inventory, 8 redacted transcripts) and `COMMITTED_STATE.md`
  (2 OK / 2,357 not committed / 0 mismatched on the committed tree). Both TS
  trees (1,605 files) are **not committed**; they are regenerable and hashed.
- **Still unobserved** (HOSTING §10 "Still to observe"; U-19): live answer and
  settlement behavior, plan-revision requests, post-restart reads,
  resume-override adoption, the provider wire interface (L-2) and tool calling
  (L-3), configurability of the plugin fetch (L-4), relocation, the effect of
  `turn/interrupt`, and MCP-call permission paths. Live items need the owner's
  credential or an identified local provider.

### 5.1 Commitment → result

| SoW item | Design sections | Standing | What remains (kind) |
|---|---|---|---|
| OUT-001 App-owned stock child/protocol boundary (CODE) | §1, §3 (H1–H11), §4, §5, §6 (R1–R9, register), §6.6–§6.8 | **Developed** as definition | The CODE artifact is *implementation*. The DEL-01-02 split on unknown-request errors waits for a later undertaking (F-01; U-14) |
| OUT-002 selected pin, generated types, isolated supplement, version identity and verification, plan/revision seam | §7.1–§7.3, §8 S-2; SPIKE §3–§4; `generated/0.158.0/` | **Partially developed** | See 5.4 |
| OUT-003 responsibility account: Rust/TS allocation, plan/version handoff, local-provider requirements, optional reuse | §8, §8.1, §11, §12 | **Partially developed** | OI-008 is a **proposal only** (O-1 recommended; decision with the App implementation owner, U-02). L-2/L-3 are not observed (U-22). Qualifying the embedding protocol needs a candidate |
| OUT-004 qualification and deliberate-upgrade evidence | §9.1–§9.5; SPIKE SV-01…SV-06; `_spike/transcripts/` | **Partially developed** | See 5.4 |
| REQ-001 stock child over stdio; unknown-request error | §3, §4, §5, §6.3 | Developed (definition) | Implementation; VER-001 fixture on a candidate |
| REQ-002 types from the selected pin; small supplement; native items | §7.3; SPIKE §4 | Partially developed | Reference output unselected (U-15); supplement contingent on it |
| REQ-003 version identity, verification; plan/revision seam | §7.1, §7.2; §8 S-2 | Developed | Verifier implementation. At 0.158.0, plan updates carry no revision identity (P-10), so DEL-01-03 must derive one |
| REQ-004 record the Rust/TS decision; priorities; reuse assessment | §12 | Partially developed | OI-008 decision (U-02) |
| REQ-005 qualify embedding; local-provider requirements | §8.1; §10 | Partially developed | Qualification on an identified candidate; L-2/L-3 observation |
| REQ-006 bind pin and qualification; deliberate upgrades | §7, §9.5, §10; D4 | Partially developed | Pin selected for definition/generation. Qualification, re-examination and the first upgrade comparison are *implementation/qualification* |
| REQ-007, REQ-008 no foreign acts | §11 | Developed | — |

### 5.2 Result → commitment

| Addition | Where | Authority |
|---|---|---|
| Outstanding-request register rules R7–R9 (A14 origin; no affirmative App answer; answer-origin classes) | §6.3, §6.6 | D3; R-2; R-10 (DERIVED/INTEGRATION) |
| Run holds and the supplier: HP-1/HP-2 not adopted, HP-3/HP-4 best effort | §6.7 | R4-2; D6 deferred (R6-4 closes U-25/F-22 in the working tree) |
| MCP surfaces classified; App-initiated `mcpServer/tool/call` rules | §6.8 | R4-12 |
| Supplied-guidance evidence per thread and turn | §8.2 | R-10 (V1-C D-16) |
| Observed model destination per turn | §8.3 | D5 (flow, no gate) plus R5-4 INTEGRATION reading |
| Invariant H11 (supplier process tree); vendor-tree distribution identity | §3; §7.1 | Spike observations S-F-02, S-F-06 |
| "No notification filtering" (H7) kept as a **definition choice**, not a v4 prohibition | §2; U-07 | Labeled; the App implementation owner decides. Not unsupported, but a candidate for owner visibility |
| OI-008 option table and O-1 recommendation | §12 | BRIEFS W6 (labeled PROPOSAL) |

### 5.3 Proposed SoW corrections (`DEL-01-01/ScopeOfWork.md`)

| # | Locus | Current text | Proposed text | Grounds |
|---|---|---|---|---|
| S-11-1 | CLM-003 sentence 1 | "[I, N] OI-012 leaves the supplier pin with the App implementation owner before protocol generation and qualification; historical 0.154.0 and reported 0.157.1 are not adopted pins." | Keep it, and add: "Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D4 selected Codex 0.158.0 as the definition and generation pin for the first undertaking; it is re-examined before implementation, upgrades are deliberate, and the selection establishes no qualification (DEP-005)." | D4; HOSTING U-01 |
| S-11-2 | TBD-002 | "OI-012 is OPEN with the App implementation owner, needed **before protocol generation and qualification**. No v4 supplier version has been adopted by this contract. DEP-005 remains VERSION_AND_ENVIRONMENT_TO_DEFINE…" | "OI-012: 0.158.0 selected for definition and generation by DECISION-1 D4; observations recorded in `Design/PIN_SPIKE_0.158.0.md`. Remaining under OI-012, with the App implementation owner: re-examination before implementation and the pin used for qualification on an identified App candidate. DEP-005 remains VERSION_AND_ENVIRONMENT_TO_DEFINE for qualification witnesses." | D4; SPIKE; HOSTING §10, U-01, U-21 |
| S-11-3 | REQ-006 sentence 2 | "Pin selection is included work; neither historical version is selected by this contract." | "Pin selection is included work; the definition/generation pin 0.158.0 was selected by owner decision D4, neither historical version is selected, and the implementation/qualification pin follows re-examination." | D4 |

No change is proposed for OI-008 (TBD-001, still open; §12 is a proposal) or
for CLM-003's Responses-interface sentence (still unobserved, L-2).

### 5.4 What OUT-002 and OUT-004 still need

**OUT-002 (CONFIG and generated source).**
- *Done at definition level:* the pin is identified (D4). Generation is
  deterministic and hashed (manifest). The JSON Schema bundles are committed.
  Version identity and the verification rule are defined (§7.1, §7.2). The
  S-2 seam is defined.
- *Definitional choices still owed* (App implementation owner):
  - reference generator output O-R1/O-R2/O-R3 (U-15);
  - hence the supplement contents (empty unless O-R2);
  - location of committed TS types;
  - distribution-identity composition and launcher (U-17);
  - content-identity algorithm for records (U-08).
- *Implementation/qualification:*
  - the version verifier;
  - pin re-examination before implementation (U-01);
  - dependence on experimental API (F-12, F-13; U-21).

**OUT-004 (TEST fixtures and outcome record).**
- *Done:* the recorded-exchange method, standing labels, replay/comparison
  and the upgrade procedure (§9.1–§9.5). SV-01…SV-05 were run in the spike,
  with handshake and unknown-method transcripts.
- *Remaining, all implementation/qualification/witness:*
  - SV-06, the live seam set X-02…X-10 (DESIGNED; needs the owner's
    credential or a local provider, and an App candidate);
  - the U-19 live observations;
  - qualification of the embedding protocol on a candidate (VER-005/VER-006);
  - the first deliberate-upgrade comparison, once a second pin exists.
- No qualification is claimed anywhere.

### 5.5 Proposed register changes

**Mirror only** (rows in `DEL-01-01/Dependencies.csv`):

| # | New row | Mirrors | Source |
|---|---|---|---|
| M-11-1 | DOWNSTREAM HANDOVER → DEL-02-04 (additive guidance seam S-6) | DEP-02-04-010 | V1-C RF-6; HOSTING F-16 |
| M-11-2 | DOWNSTREAM HANDOVER → DEL-06-01 | DEP-06-01-013 | (observed; outside D1) |
| M-11-3 | DOWNSTREAM HANDOVER → DEL-09-01 | DEP-09-01-019 | (observed; outside D1) |
| M-11-4 | DOWNSTREAM HANDOVER → DEL-09-02 | DEP-09-02-009 | (observed; outside D1) |

**Notes only:**
- DEP-01-01-017 (UPSTREAM CONSTRAINT OI-012), Notes: "0.158.0 selected as
  the definition/generation pin by DECISION-1 D4; re-examined before
  implementation; not qualification." Keep SatisfactionStatus unchanged,
  because the row's point of need includes qualification.
- DEP-01-01-018 (DEP-005), Notes: "generated-type and handshake facts at
  0.158.0 are recorded (PIN_SPIKE-v0.1); no candidate qualification."
- The `_DEPENDENCIES.md` Run Notes line "OI-008 and OI-012 retain the App
  implementation owner's actual decisions…" gains the D4 pointer when the
  register is next regenerated.

**V1-A RF-03 (DEL-01-01 → DEL-04-01 / OI-002): no change, confirmed from the
DEL-01-01 side.** HOSTING §2 and §11 now carry D3 directly (R-10). R7 gives
A14 affirmative answers only to the person or the user's own Codex mode.
HOSTING F-16 records that DEP-01-01-021/-022/-024 then suffice. This agrees
with C1-A's "Not proposed".

**New arcs with DEL-01-01 as supplier** (rep. rows are in the consumers'
registers, not here):
- DEL-03-03 → DEL-01-01 (N-B4, this closeout);
- DEL-03-04 → DEL-01-01 (N-B9, this closeout);
- DEL-04-03 → DEL-01-01 (C1-A N-15; conditional on S-7 not riding DEL-01-02,
  which D1 defers);
- DEL-02-01 → DEL-01-01 (C1-A N-16; WD U-08, V1-C RF-7);
- DEL-02-03 → DEL-01-01 (C1-A N-23);
- DEL-09-06 → DEL-01-01 (C1-C #11).

All are concurred from the supplier text. HOSTING's Receivers line names
DEL-02-01/05-01/05-02 (J9), DEL-02-03 and DEL-03-03. The §8 seam table names
DEL-04-03 (S-7, "through DEL-01-02") and gives the 0.158.0 inventory to
DEL-02-01's naming. None changes SCC-001
({DEL-01-01, DEL-01-05}). DEL-05-01 → DEL-01-01 and DEL-09-09 → DEL-01-01
remain unproposed, as in C1-C.

### 5.6 Open items

| Item | Owner | Point of need |
|---|---|---|
| U-01 pin re-examination and qualification (D4) | App implementation owner | Before implementation and qualification |
| U-02 `UNRESOLVED{OI-008}` Rust/TS division (§12 proposal, O-1 recommended) | App implementation owner | Before architecture production contracts |
| U-15 reference generator output; U-17 identity composition; U-08 identity algorithm | App implementation owner (U-17 with DEL-01-06; U-08 with DEL-04-03) | Before R2/R5 implementation and qualification records |
| U-19 unobserved live behaviors; U-22 L-2/L-3 | App implementation owner; DEL-01-05 | Before settlement fixtures, handshake implementation, provider qualification |
| U-18 fresh-home plugin fetch (L-4) under priority 3 (not addressed by D5); F-18 `~/.codex` changes during the spike window | Owner with DEL-01-05 (OI-009) | Before any local-operation claim; before account integration |
| U-21 supplier labels app-server and generators `[experimental]` (F-12, F-13) | Owner visibility; App implementation owner at re-examination | Before implementation |
| U-03 OI-009 account home; U-05, U-06, U-07, U-09…U-14, U-16, U-20, U-24 | As in HOSTING UNRESOLVED | Before implementation |
| U-23 `UNRESOLVED{D6}` App-side run holds | Owner, via DEL-02-03 after SQ-02 | Before App-side hold implementation |
| Standalone-App receivers DEL-01-02…05 have no receiving comparison of S-1…S-4 (F-15) | Later undertaking (D1) | When those deliverables are defined |

### 5.7 Lifecycle observation

INITIALIZED. HOSTING-v0.1 to v0.5, the W11 spike and the committed generated
bundles were produced under active work, so **IN_PROGRESS would be truthful**.
Not changed here.

---

## 6. Proposed new arcs with a representative row in C1-B registers (consumer → supplier)

All need `project-dag` departure (DAG-002) before any register edit.
"Layer" is the effect on the DAG-001 selection rules. It was checked by
recomputing SCCs over the candidate registers with these 11 arcs, and again
with all 40 distinct arcs proposed across C1-A, C1-B and C1-C. SCC membership
is unchanged in both cases.

| # | Arc | Grounds | Also in | Layer |
|---|---|---|---|---|
| N-B1 | DEL-03-01 → DEL-04-03 | C §6.2 (act field set, lapse vocabulary); V1-B RF-03; replaces the package-level DEP-04-03-012 | C1-A N-11 | held (SCC-002) |
| N-B2 | DEL-03-02 → DEL-04-02 | P §13 "Expect from DEL-04-02", §3.3, §4.4; V1-B RF-06 | C1-A N-05 | held |
| N-B3 | DEL-03-02 → DEL-02-01 | P §13 "Expect from DEL-02-01" (workflow identity, checkpoint declarations, WD §4.3.7); R-9, R2-12, R2-18 | — | held |
| N-B4 | DEL-03-03 → DEL-01-01 | ADAPTER §3.5, §11; HOSTING §6.8, §8.3; W8 F-11 | — | admitted |
| N-B5 | DEL-03-03 → DEL-04-02 | ADAPTER §5.5, §11; W8 F-11 | C1-A N-06 | held |
| N-B6 | DEL-03-03 → DEL-02-01 | ADAPTER §5.3, §11 (WD §4.2.2); W8 F-11 | C1-A N-20 | held |
| N-B7 | DEL-03-03 → DEL-02-03 | ADAPTER §7.7, §11 (EXEC §3.6); W8 F-11 | C1-A N-27 | held |
| N-B8 | DEL-03-03 → DEL-04-03 (conditional) | ADAPTER header (RS R5/R7/R11/R13 consumed for joins), §11; W8 F-11. It pairs with C1-A N-14 (the reverse) | — | held |
| N-B9 | DEL-03-04 → DEL-01-01 | GUIDE header, row 9, §2.11; GUIDE F-4 | — | admitted |
| N-B10 | DEL-03-04 → DEL-09-06 | GUIDE §2.0 host-contribution column, §4.3; GUIDE F-4 | — | admitted |
| N-B11 | DEL-03-04 → DEL-09-09 | GUIDE row 9 (XT §3), M1.6; GUIDE F-4 | — | admitted |

**For the integrator.**
- **(a)** This closeout does not support C1-A N-12 (DEL-03-02 → DEL-04-03);
  see 2.4.
- **(b)** N-B9…N-B11 go with SoW correction S-04-6. If S-04-6 is not
  adopted, the guide's use of HOSTING, RELAY and XT should instead be stated
  as references only.
- **(c)** Do not register the reverse citations DEL-09-09 → DEL-03-04,
  DEL-09-06 → DEL-03-04 or DEL-04-01 → DEL-03-01/03-03. Each would enlarge
  SCC-002 or create a new SCC (4.4, 1.4, 3.4).

## 7. Completion of this node

- **Written:** only this file. No SoW, register, `_STATUS.md`, `_CONTEXT.md`,
  `_REFERENCES.md`, Design file or other file was edited.
- **Git and network:** read-only git; no network.
- **Proposals:** every proposed change above stays **unapplied**. Its route
  is:
  - SoW revision for S-01-1…S-11-3 (24 changes). S-01-4, S-01-5, S-02-3 and
    S-03-2 touch scope or protected criteria and need their owning decision;
  - a register update for the 33 mirror rows, 6 notes-only rows and one value
    normalization;
  - `project-dag` departure (DAG-002) for N-B1…N-B11.
- **Residuals:**
  - the lifecycle transitions (all five: IN_PROGRESS would be truthful);
  - custody of FX-PIPE-01;
  - the VER-007 checker run for DEL-03-04;
  - the N-12 disagreement with C1-A.

  Each is named above with its owner.
- **Limit:** R6 in-place edits to HOSTING, C, P and ADAPTER exist in the
  working tree after the candidate. They were not compared, beyond confirming
  that R6 changes no SoW or register and amends R5-1's classification (R6-1).
