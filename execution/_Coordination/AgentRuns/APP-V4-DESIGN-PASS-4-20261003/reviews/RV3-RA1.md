# RV3-RA1 — review of DEL-10-03 RA-v0.1 (owner O-E)

- **Reviewer:** RV3, a Type 2 TASK running as Claude Opus 5.5 (`claude-opus-5-5`). It was dispatched within the HELP_HUMAN session and did not author the unit (B-18). The review was written 2026-10-04. Method: `coordinated-knowledge-work` §3, which asks whether the unit is correct.
- **Unit**, as `O-E.md` "Freeze — DEL-10-03 RA-v0.1". Both files were re-hashed and match `caed56b8ea`, and `git status --ignored` is clean:
  - `RESPONSIBILITY_ACCOUNT.md` `531b65b7…8934`;
  - `prototype/ra_check.py` `ccbab0b3…9269`.
- **Basis read:**
  - DEL-10-03 `ScopeOfWork.md` (`31bc607d…`, which matches the pin);
  - every `Dependencies.csv`;
  - DAG-004's `DependencyEdges`, `ExcludedRows`, `GRAPH_BASIS` and `HANDOFF_STATE`;
  - the nine supplier Design files' indexed sections: WD §9, EXEC Receivers, ROLE O-5, C §8, P §1/§13, ACT §10.3, RS Receivers, LOOP §10, PANEL §6;
  - the original-seed `ARCHITECTURE.md` (`8d147421…`) and `OPERATING_METHOD.md` (`8f53b266…`), and the current `ARCHITECTURE.md` and `OPERATING_METHOD.md`;
  - App v3's `prepare-packaged-instruction-root.mjs` (`fe0fa50d…`);
  - the D-GOV-52 tranche manifest;
  - R23-2, R23-31.7/.8/.10, R23-32 F-R11/F-R15/F-R16 and R23-44.

## Verdict: **READY**

There are no BLOCKING or MAJOR findings. There are 2 MINOR findings and 3 NOTEs.

Several things hold:
- the population bound matches R23-31.7 exactly;
- the map indexes its supplier sections and names no common implementation;
- the two-way trace and the relocation check hold against the records;
- F-RA1 is a real and new gap, correctly routed.

## Findings

### RA1-R1 — MINOR — F-RA1 calls the missing rows "SAME_ARC"; in this graph's vocabulary they are MIRROR rows (§3.4)

- **Claim.** "Each would be a supplier-side mirror of an existing admitted arc (SAME_ARC), so no new arc and no SCC."
- **Evidence.**
  - DAG-004 `ExcludedRows.csv` counts NOT_TOPOLOGICAL 208, MIRROR 145 and SAME_ARC 2. Every supplier-side DOWNSTREAM row is `MIRROR` (rule SR-6); `SAME_ARC` marks a second UPSTREAM row on an arc.
  - The six existing supplier mirrors to DEL-10-03 (DEP-02-01-040, 02-03-040, 02-04-018, 03-01-042, 03-02-033, 04-03-045) are all dispositioned `MIRROR`.
- **Consequence.** The register owner reading F-RA1 at the amendment would look for the wrong disposition. The conclusion (no new arc, no SCC) stands.
- **Repair.** Write "MIRROR (SR-6)". Also cite DAG-004 `HANDOFF_STATE.md` "Open matters" as the precedent for routing. It already carries "Five expected mirror rows not extracted … no graph effect", with an owner. F-RA1's three joins are **not** among those five, which is why F-RA1 is new.

### RA1-R2 — MINOR — S-6's "Not mapped in detail" and the request to O-A are already overtaken; RA's ACT pin now fails its own check (§1.2 S-6; §2.3; H-1)

- **Evidence.**
  - ACT-POLICY is now v0.11 (working bytes `597f13bd…`, uncommitted, O-A). Its header reads "§10.3's DEL-10-03 row maps what DEL-10-03 RA-v0.1 reads (§2.1, §3, §8.2, §8.4)".
  - The row itself reads "RA-v0.1 … reads, by section: §2.1 …; §3, the settled distinctions S1–S12; §8 … (§8.2) and … (§8.4) … that is RA F-RA1, for the next amendment".
  - Rerunning `ra_check.py` now gives **PASS 30, FAIL 1**: "H-1 S-6 DEL-04-01: a cited prefix differs from today's Design or SoW bytes". RA pins v0.10 `1bf0ce8e…`, which is the committed blob, so the frozen 31/0 is reproducible from `caed56b8ea`.
- **Consequence.**
  - The check is doing its job: it detected supplier drift.
  - RA's S-6 text ("Not mapped in detail"; "Request to O-A") will read as stale once O-A commits.
  - O-A's row matches RA §2.3 exactly (§2.1, §3, §8 with §8.2/§8.4), so adoption is confirmed in the returned file (workflow §5).
- **Repair.** At RA's next revision, re-pin S-6 to ACT v0.11's committed hash (R23-21) and record the mapping as done. Consider having H-1 report a moved supplier as a NOTICE plus a re-pin instruction, as `check_rp.py` V-1 does, rather than failing. Then a frozen unit's check stays green while still flagging the drift.

## Notes

- **N1 — R-2 scans only the nine supplier SoWs, and only clause first lines.**
  - I checked the wider set. The SoWs naming DEL-10-03 are the six suppliers in §3.1 plus DEL-10-01, DEL-10-03, DEL-10-04, DEL-11-01 and DEL-11-02.
  - DEL-10-01 is DEL-10-03's input basis (DEP-10-03-017, excluded in §1.4). The last three are consumers. None hands DEL-10-03 a promise, so the reverse claim holds.
  - The regex would miss a clause that names DEL-10-03 only on a continuation line. Clauses here are single-line, so there is no effect now.
- **N2 — H-1 accepts a prefix matching either the Design or the SoW hash.** A Design prefix mistyped as the SoW's would still pass. This is a cosmetic weakness: every prefix I recomputed sits beside its own file.
- **N3 — S-1 summarises WD §9's allocation columns rather than restating content.** "OI-014 for A-1…A-6, A-10…A-12; OI-013 for A-4, A-9, A-10; A-7 and A-8 sit with DEL-04-03 and DEL-03-01" matches WD §9's Placement column row by row. That is index-level, consistent with SQ-E2.

## The brief's questions

- **Population bound against R23-31.7.**
  - R23-31.7 reads "bounded to its nine supplier rows plus DEP-006 and OI-013, 014, 018 and 024". RA §1 has S-1…S-9 (DEP-10-03-008…016) and X-1…X-5 (DEP-006; OI-013, 014, 018, 024): 14 entries.
  - The nine rows are DEL-10-03's only ACTIVE EXECUTION UPSTREAM rows to PKG-02…05, and each is **admitted** in DAG-004 `DependencyEdges.csv`.
  - The exclusions are justified by records:
    - DEP-10-03-017 (DEL-10-01) is an input basis;
    - no DEL-10-03 row names a DEL-01-0x supplier;
    - the SoW's own definition reads "A promise is an accepted obligation, not every incidental historical mechanism" (verified).
- **Map; SQ-E2; no common implementation.** I verified each indexed section against the supplier file. The WD §9 title and the "Confirmation … None" sentence (WD wording: every Confirmation cell remains "None") match. So do:
  - EXEC Receivers "§2, §3, §4, §10";
  - ROLE O-5 "§3–§6";
  - C §8 "Three-surface responsibility map", "DEL-10-03 account" and "unagreed";
  - P §13 "Provide to | DEL-10-03 …" (row DEP-10-03-012);
  - RS "no common service or implementation is inferred";
  - LOOP "Responsibility map" and "Not allocated";
  - PANEL §6 "Reusable-component allocation account".

  Rows give one-line meanings and index the rest. §2.3 quotes current V4-ARC-20, "Shared meaning does not prescribe one executable service" (verified), and names no common implementation.
- **Promise trace both ways.**
  - Forward: the six supplier SoW clauses and mirrors listed match the registers. DEL-04-01, 05-01 and 05-02 have no clause and no mirror (F-RA1).
  - Reverse: every ACTIVE row anywhere targeting DEL-10-03 is a listed mirror, or DEP-10-04-007, DEP-11-01-008 or DEP-11-02-008 (all admitted consumer rows).
  - **Relocation:** the seed V4-ARC-20 text names exactly the five items RA lists ("workflow format and its declared checkpoints, role guidance, the record format, the capability-catalog contract types, and interface components used by the App and hosts"). Each maps to an owning entry, and current V4-ARC-20 adds human acts (S-6).
  - **H-1…H-3:**
    - the seed V4-OPS-12 "**Precedence.** Root governance, then …" and V4-OPS-14 "a thin project loop file …" quotes are verbatim;
    - the current "superseded by A/C and accepted HTML 01 at this scope", "Root location alone supplies no blanket precedence", "not a mandatory new hierarchy" and "exact form is implementation definition" are verbatim;
    - the seed hashes are as cited.
- **Consumer account to PKG-11.**
  - DEP-10-03-019 is DOWNSTREAM HANDOVER to "Adoption and replacement continuity" (NOT_TOPOLOGICAL in DAG-004), which carries R23-32 F-R11.
  - §4.2's App v3 entry matches CLM-007 and the script (`fe0fa50d…`; `ROOT_FILES`, `PRODUCT_AGENTS_SOURCE` = `projects/chirality-app-dev/instructions/AGENTS.md`, `DOC_FILES`, `TOOL_FILES`).
  - Runtime and App v3: "notice delivered; receiving decision not recorded" (F-R16).
  - Piping and PEC: the tranche manifest's "hold no pin or copy of either passage and read Root AGENTS.md live" (verified).
  - No adoption is claimed.
- **F-RA1.**
  - Confirmed: no DOWNSTREAM row to DEL-10-03 exists in DEL-04-01's, 05-01's or 05-02's registers, and their SoWs do not name DEL-10-03.
  - Their Design files do acknowledge the consumer (ACT §10.3, now explicitly; LOOP and PANEL Receivers).
  - Routing to the next amendment matches R23-32 F-R15. See RA1-R1 for the terminology.

## Checks run

- `ra_check.py`: PASS 31, FAIL 0 at first (as frozen). On a rerun after O-A's ACT v0.11 edit: PASS 30, FAIL 1 (RA1-R2).
- `ra_check.py --self-test`: H-1, P-1, R-1, F-1 and R-2 each detected.
- My own scripts for:
  - register rows targeting DEL-10-03 and their DAG-004 dispositions;
  - the WD §9 Placement column;
  - SoW scans;
  - seed and current text quotes (whitespace-normalised).

## Not checked

- The content of each supplier section beyond the indexed headings and quoted lines.
- `check_boundary_owner_resolution.py` on DEL-10-03 (not rerun; O-E reports 1 checked, 0 failing).
