# Dispatch — APP-V4-DESIGN-PASS-4-20261003

Mechanism: harness-native descendants (Claude Code Agent tool) of the
HELP_HUMAN session, under D-GOV-35, agent type `type2-opus-high`. Fences are
verified afterwards by `git status`.

| Node | State |
|---|---|
| S0 | Owner direction recorded (items 1–4). Graph and briefs written. Tranche 1: eight deliverables |
| S1 | Three surveys launched in parallel (S1-A, S1-B, S1-C), read-only, one report each |
| VC | Codex version-advance check to 0.160.0: waiting for the owner's explicit yes to the named download |
| VC | Owner said "yes, download it" for the named file; VC launched |
| S1-C | Returned: [SURVEY/S1-C.md](SURVEY/S1-C.md) (DEL-09-05, 09-07, 09-11; 69 OUT/REQ/AC/VER items; 8 owner choices; structural questions S-1…S-5). Fence held: only the run folder written |
| S1-A | Returned: [SURVEY/S1-A.md](SURVEY/S1-A.md) (DEL-06-01, 06-02; 51 items; owner choices K-A…K-F; structural S-1…S-7). Fence held |
| S1-B | Returned: [SURVEY/S1-B.md](SURVEY/S1-B.md) (DEL-01-06, 09-01, 09-02; 77 items; 7 owner choices; SQ-1…SQ-6). Fence held |
| IC | Returned: `docs/governance_harness/_PROPOSALS/D-GOV-52_agents-md-app-v4-alignment_2026-10-03/` (PACKET, inactive patch, proposal manifest). `AGENTS.md` untouched. Correction to its report: the home path at `_Coordination/_COORDINATION.md:18` is hash-bound and was deliberately left by the redaction, so `validate_path_anchors.py` still fails on it |
| S0 | Owner selected `coordinated-knowledge-work`; coordination re-arranged (work graph "Coordination"); R23 ruled; K prepared |
| O-B | S1-B's agent (`a4ebaae556bc8cde3`) resumed by SendMessage as standing owner of DEL-01-06, 09-01, 09-02; started on DEL-09-01 and K-4 facts. Write area: DEL-09-01 `Design/`; `OWNERS/O-B.md` |
| O-C | S1-C's agent (`a59950c21bd9eb15e`) resumed by SendMessage as standing owner of DEL-09-05, 09-07, 09-11; started on DEL-09-07's designable-now set. Write area: DEL-09-07 `Design/`; `OWNERS/O-C.md` |
| O-A | S1-A's agent (`a5d59923b9c8069e8`) named owner of DEL-06-01, 06-02; not started — waits for K-1…K-3 |
| K | Owner returned K-1…K-10 to HELP_HUMAN; ruled R23-8…R23-14; R23-6 revised |
| O-A | S1-A's agent (`a5d59923b9c8069e8`) resumed by SendMessage as standing owner of DEL-06-01, 06-02; started on the early path. Write area: DEL-06-01/06-02 `Design/`; rows only in ACT §2.1, RS §6.1/§13.6 + `RS_RECORD.schema.json` + examples, AAC §1.2; prototype under `E/`; `OWNERS/O-A.md` |
| O-C | Froze LHQ-U1: DEL-09-07 `Design/LOCAL_HOST_QUALIFICATION.md` (sha256 `2668d955…`). F-1/F-2/F-3 ruled R23-15, R23-16. Stopped at the boundary; restarted on LHQ-U2 and the early-path cases |
| RV | Standing reviewer started (fresh `type2-opus-high`) on LHQ-U1. Write area: `reviews/` |
| O-B | Froze U1: DEL-09-01 EXP-v0.1 (protocol + 3 schemas + prototype, 52/52). Signing facts in `OWNERS/O-B.md`. U-EXP-1/2/3/4 ruled R23-17. Stopped at the boundary; restarted on DEL-01-06. U1 queued for RV after LHQ-U1 |
| O-A | Froze E-1 (A16 rows, DEL-06-02 `DECISION_VIEW.md`, prototype `E/` 39/39, fixture FX-DP1) and escalated PR-1…PR-13. Ruled R23-18; restarted to apply them |
| RV | Returned RV-LHQ-U1 (REPAIR: 4 MAJOR, 8 MINOR) and RV-EXP-U1 (REPAIR: 4 MAJOR, 7 MINOR). Cross-owner EXP-R-A/B ruled R23-19, R23-20; pin churn ruled R23-21. Findings routed to O-C and O-B |
| VC | Returned: `DEL-01-01/Design/VERSION_ADVANCE_0.160.0.md`, `prototype/version_advance/va_harness.py`, `VC.md`. Ruled R23-22 (pin stays 0.158.0 for definition; NIR L396 to O-A) |
| O-C | Repaired LHQ-U1 (`2f648e5b…`); froze LHQ-U2 (traffic plan, dossier, 3 schemas); drafted EP-05 (DEL-09-05 FW-04) and EP-11 (DEL-09-11 reader method) on FX-DP1. Asked for the isolated reader |
| RR-E | Isolated reader dispatched by HELP_HUMAN (fresh `type2-opus-high`) with exactly the files in `E/RR-E/SUPPLIED.sha256`; supplied context in `E/RR-E/DISPATCH_RECORD.md`. Early-path consumption check |
| RV | Queued: confirm LHQ-U1 repair; confirm EXP-v0.2 repair; review LHQ-U2 |
| O-B | Repaired EXP to v0.2 (77/77); signing option B recorded (FP-0…FP-5; A fallback). U2 (DEL-01-06) and U3 (DEL-09-02) drafted; told to freeze both for a second reviewer RV2 (review was the constraint) |
| O-B | Froze U2 (DEL-01-06 PKG-v0.1, 36/0) and U3 (DEL-09-02 SQ-v0.1, 72/0) |
| RV2 | Second standing reviewer started (fresh `type2-opus-high`) on O-B's U2 and U3 |
| RR-E | Reader returned a schema-valid account from the nine supplied files only (its report). Examiner check 7/9; RC-6 and RC-9 traced to the checker, not the reader (`E/RR-E/RESULT.md`). Repair to O-C; offerDigest serialization question to O-A |
| RV | LHQ-U1 repair CONFIRMED READY (+LHQ-R15 MINOR, R16 NOTE); EXP-U1 repair CONFIRMED READY; LHQ-U2 REPAIR (2 MAJOR, 5 MINOR, 2 NOTE). Routed to O-C; U-EXP-1 closure to O-B |
| O-A | Refroze E-1 (R23-18 rows; RS-v0.10, ACT-POLICY-v0.10, AAC-v0.3, NIR-v0.3, DEL-02-03 schema proposed-0.7; offer digest `aac-offer-digest/0.1`; run_e 47/47; all affected prototypes pass). E-2 (DEL-06-01 FR-v0.1, 32/32) in progress. Ruled R23-23. E-1 to RV |
| O-A | R23-23 fixes applied (ACT §2.5 A16 row; EXEC L3); E-2 held (DEL-06-01 FR-v0.1 32/32; DEL-06-02 FV-v0.1 16/16; examiner-not-established rule FV-2a) |
| O-C | RC-6/RC-9 checker repaired; RR-E 9/9 on the unchanged account with HELP_HUMAN's C-09 "absence" judgment (RESULT.md); standing check 12/12. LHQ-R15/R16 and LHQ-U2 U2-R1…R8 repaired. EP-05 and EP-11 frozen on E-1 versions (input set IS-FX-DP1-2 with the digest rule). All queued to RV after E-1 |
| RV | E-1 REPAIR (1 MAJOR E1-R1, 3 MINOR, 4 NOTE). E1-R1 traced to HELP_HUMAN's R23-18 item 3; superseded by R23-24. Routed to O-A |
| RV2 | PKG-U2 REPAIR (2 MAJOR, 7 MINOR, 2 NOTE); SQ-U3 REPAIR (2 MAJOR, 6 MINOR, 3 NOTE). PKG-R10 ruled R23-26; SQ-R-A/B ruled R23-27. Routed to O-B |
| RV | LHQ-U1 (R15/R16) READY; LHQ-U2 repair READY (+U2-R10/R11 MINOR, R12 NOTE); EP-05+EP-11 READY (3 MINOR, 4 NOTE). Minors routed to O-C; EP rerun waits for E-1 under R23-24 |
| O-A | E-1 repaired under R23-24/R23-25 (run_e 56/56; FX-DP1 `9501ef81…`); E-2 frozen (FR 32/32, FV 16/16). Both to RV; new manifest to O-C |
| RV | E-1 repair CONFIRMED READY (R23-24 adoption checked in files). E-2 REPAIR (1 MAJOR torn-line, 2 MINOR, 2 NOTE). Routed to O-A |
| O-C | Minor repairs done; EP-05 22/0 and EP-11 on IS-FX-DP1-3 (standing check 17) on FX-DP1 `9501ef81…`. Queued to RV |
| RR-F | Second isolated reader dispatched on IS-FX-DP1-3 (`E/RR-F/DISPATCH_RECORD.md`), to test the changed package shape and O-C's last-segment matching rule against a real account |
| O-A | E-2 repaired (run_fleet 34/34, run_views 22/22 incl. RV probes; RS L-0 A16 row). E2-R3 qualified-ready accepted by HELP_HUMAN. Queued to RV |
| RR-F | Reader returned; examiner comparison 9/9, 0 referred; digest recomputed from the rule (`E/RR-F/RESULT.md`) |
| RV | LHQ-U2 READY (second confirmation); EP READY. Notes: `calibration_check` tagging unbounded; last-segment overlap gap. Both to O-C |
| O-B | U2 → PKG-v0.2 (check_pkg 64/0) and U3 → SQ-v0.2 (check_sq 108/0) repaired; EXP-v0.2 U-EXP-1 closed in place (`1371ddb2…`). To RV2 for confirmation. Note: HELP_HUMAN's WIP checkpoint landed mid-repair and moved HEAD under owners' pins; later checkpoints wait for a quiet point or are announced |
| RV | O-C minors + EP rerun READY; E-2 repair READY (+E2-R4 MINOR: qualifier must show in the label). E2-R4 to O-A |
| RV | E2-R4 CONFIRMED; E-2 READY, no open findings. Downstream note (DEL-09-05 must read "ready (qualified)") to O-C |
| O-C | RR-F added as second independent case (standing 19/19); last-segment and whole-identifier matching hardened; CB-1 calibration binding + top_check.py; DAC RW-1 for "ready (qualified)"; RS re-pinned to L-0 A16. To RV |
| RV2 | PKG-v0.2 and SQ-v0.2 repairs CONFIRMED READY (+PKG-R12, SQ-R-L, SQ-R-M MINOR; 3 NOTE). To O-B |
| RV | O-C hardenings CONFIRMED (fw04 22, standing 19, top_check). EP, LHQ-U1/U2 no open findings. ISO time-form note to O-C |
| O-C | ISO-8601 UTC time form stated, schema-enforced, top_check parses instants (`cf128073…`). Small mechanical change; covered by the pre-merge integration review rather than a separate RV round. O-C done for tranche 1 |
| S0 | Eight tranche-1 deliverables INITIALIZED → IN_PROGRESS by write_status.sh (R23-28) |
| O-B | Last minors fixed (check_pkg 66/0, check_sq 114/0; ST-5 replay = real Codex capture, U-SQ-6 owned by DEL-01-01 with DEL-01-02, before RUN-A). O-B done for tranche 1 |
| C1 | Integration closeout dispatched (fresh `type2-opus-high`): stale sibling pins (R23-21.4), SoW re-pins (R23-5), cross-owner interfaces, all prototypes once, fences. Write area: pin lines only + `closeout/C1_INTEGRATION.md` |
| C1 | Closeout returned: 40 sibling re-pins, 17 SoW re-pins, DEL-09-06 W14 break found and repaired (44/0), all prototypes pass, fences hold. GUIDE pin check 22/25 (A16). Ruled R23-29; C2 dispatched |
| C2 | GUIDE-v0.7 (A16; pin check 25/25), ACCESS §13 row + SoW re-pin, VERSION_ADVANCE §7.1 note; all counts held. Remaining cascade TOP/DOS→LHQ and RRM→DOS re-pinned by HELP_HUMAN with a script (mechanical). Pre-existing pins to older committed GUIDE/ACCESS versions (RELAY, ADAPTER, LOOP) predate this pass; noted for the pre-merge review |
| RV2 | O-B's last minors CONFIRMED at d150856784 (closeout changed only pins, verified by reversing them). PKG and SQ READY; SQ-R-O optional NOTE carried (ST-5 capture method) |
| P1 | Pre-merge review of `d150856784`: MERGE (0 BLOCKING, 0 MAJOR, 2 MINOR, 5 NOTE). P1-F1: EXP's U-EXP-1 closure (`fc5b8230…` → `1371ddb2…`, no rule/schema/example change, 77/0) is confirmed by P1 itself. P1-F2: TOP §7's comparison with RS grant/decline times on instants — carried to DEL-09-07's next revision, not changed in the reviewed candidate. P1-N2: the three cascade pin lines marked "C1/C2 re-pin" were made by HELP_HUMAN (C2 row above) |
