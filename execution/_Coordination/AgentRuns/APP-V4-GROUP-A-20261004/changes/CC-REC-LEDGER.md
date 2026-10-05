# CC-REC-LEDGER — bounded App recovery ledger placement

TASK `/root/group_a_execution/design_records_exec`, parent WORKING_ITEMS `/root/group_a_execution`, no delegation. Separate technical owner choice for U-R7/TBD-002, authorized within-group by parent; independent review required. Prose only: RECOVERY §7 and U-R7. No App/code/schema change or human gate. Source remains SoW CLM-002/REQ-005/REQ-006 and existing pointer-only append-only ledger that outlives the process.

Select `<App-own-user-data>/runtime/recovery.ledger.jsonl`, App-local UTF-8 JSON Lines, pointer-only and App-observed facts. Tests retain explicit caller-selected scratch path. Distinct from project RS logs and portable library A15 acts; outside Codex homes and no common service. Preserve prior facts, schema conformance and durable publication before persisted claim. Storage failure/incomplete/unreadable content is visible with no silent relocation or invented missing facts/approval. Ledger failure never suppresses supplier-owned required protocol replies. No payload, credential, transcript copy.

Readiness: source-coherent bounded location/technology choice now prepared; production file/directory durability, corruption/failure and relaunch witnesses remain required, not supplied by prototype. U-R3 retains unresolved retention/deletion duration, compaction, and effects of the person's conversation deletion; App recovery owner with owner privacy input at that point of need. Placement selects none of those, and no automatic deletion is authorized. Existing schema unchanged; source consistency checked. Shared RECOVERY candidate also includes CC-REC-R9; its four new cases and existing 16/16 suite pass, but are not ledger storage qualification.

Consumers: I1 runtime ledger path injection/discovery/lifetime; native reconnect/relaunch display; receiver run tags and own custody summaries; packaging App-user-data convention. No consumer code changed. Parent routes supplier-owner adoption and fresh independent review.

Prior RECOVERY source (R9 candidate) SHA-256 `fad35e9f515dbdb66802f8463d6777ef61e5dc81973f30299a58579ea0ba9023`.

| Source/returned Design | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `a19beb59638a954078e093658d326bdeae4a2c9d1241d5ff69d262abc3e9b4b5` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/ScopeOfWork.md` | `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/prototype/recovery_model.py` | `521c9440267943cd3e06f104558254431cae372d822df10609481726863e82cf` |
