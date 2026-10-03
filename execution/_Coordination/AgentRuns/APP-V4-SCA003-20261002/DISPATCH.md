# Dispatch — APP-V4-SCA003-20261002

Mechanism: harness-native descendants (Claude Code Agent tool) of the
HELP_HUMAN session, under D-GOV-35, agent type `type2-opus-high`.

| Node | State |
|---|---|
| S0 | Run opened from design pass 3's closeout; owner direction recorded; briefs written |
| P3 | Pre-change baseline: 0 BLOCKER, 35 WARNING, 93 INFO (scope PKG-01…05, 09, 10; 32 deliverables); expected source SCA-V4-002 over GROUP3, 148/148 files equal; DAG-003 130/130 and 37/37; all differences from SCA-V4-002's post-acceptance audit attributed (no new findings). Notes: R22-5 would move 16 INFO to WARNING (attribute it, not a regression); C1-A's DEL-01-04 _STATUS hash prefix slip (actual `12de2a18b401688c…`); expect DAG-004 for the new admitted arcs. Fence verified |
| P1 | AMENDMENT_ID SCA-V4-003 (zsh); ledger 209 rows (185 INCLUDE, 9 DEFER, 15 DROP); 10 new arcs (5 admitted, 5 held in SCC-002), 30 mirror groups; SCCs unchanged alone, pairwise and together; expected departure 202→212 arcs, 19 SoW and 20 registers change bytes → DAG-004; 16 owner items Q-1…Q-16. Fence verified. P2-A/P2-B launched |
| P2-B | SOW_REVISIONS_B.md: 84 blocks for 14 deliverables outside PKG-01 (57 INCLUDE rows + R22-7 block G-0403-03); dry-run 14/14 pass on all three validators; blocks for open owner items written for the recommended option and marked. R22-7 rows proposed for the ledger |
| P2-A | SOW_REVISIONS_A.md: 63 blocks for the 44 INCLUDE rows in PKG-01 (DEL-01-01…05; DEL-01-04 gains OUT-005/REQ-008/AC-008/VER-008 for the act control; DEL-01-05 REQ-010/AC-011/VER-011); dry-run in four variants, all pass (5/5 validators). Departure noted: REQ-008 reworded so DEL-04-01 gains no supplier (source wording kept as a Q-5 alternative); backticks dropped in four requirements to avoid false boundary flags |
| V23 | HOLD: B-1 (group-2 exact amendment exists only for ScopeOfWork: no Amendment_Actions.csv draft, no exact OI-009/OI-018 text, no Decision Log entry or pointer text, no supersession delta bytes, no Q-10 status word), M-1 (packet not updated after P2: G-0403-03 has no ledger row), M-2 (P2 departures not put to the owner; the REQ-008 source wording is not a safe alternative: SCC-002 13 → 16; agent-drafted criteria presented as carried decisions), 8 MINOR. All 147 blocks sound; dry-runs reproduce; arc effect confirmed over 1,023 combinations. P1 resumed as RP1 to repair |
| RP1 | Packet repaired per V23: Amendment_Actions.draft.csv (23 rows), exact OI-009/OI-018 bytes, DC-01 and pointer text, supersession row D-021, Q-10 word RESOLVED_BY_OWNER_DECISION; R22-7 rows; Q-5 departure explained; drafted-text section; Q-17 (15 extra mirror rows). Ledger 216 rows (191 INCLUDE, 10 DEFER, 15 DROP); 10 links, SCCs unchanged. V23b recheck launched |
| V23b | READY FOR CHECKPOINT: B-1, M-1, M-2 and m-1…m-8 fixed (m-5 by note); three new MINOR record items n-1…n-3 fixed by HELP_HUMAN in place (no fence or exact-byte field changed) |
