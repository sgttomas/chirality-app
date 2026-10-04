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
