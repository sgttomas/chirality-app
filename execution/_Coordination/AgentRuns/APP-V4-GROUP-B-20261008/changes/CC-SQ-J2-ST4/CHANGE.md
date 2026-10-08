# CC-SQ-J2-ST4 — correction candidate

Standing: prepared for independent review; not adopted, accepted, or candidate qualification. No examination opened. Base: `462f66975d` (full identity in SOURCE_BASIS.json).

## Source-grounded correction

The source conflict is retained here: SQ §3.1 J-2 requires a bounded delegation; §3.4 explicitly stages ST-4 at J-2, S11-1 and S11-6, and requires each named step to carry it toward its scenario outcome. The map's ST-4.staged_at says the same, but scenarios.V4-EXM-10[J-2].stimuli was empty. SQ §5/SQ-R9 consumes that array, so an illustrative recorded J-2 could pass without ST-4. Baseline prototype nevertheless reported 114/0: it checked that every stimulus was used somewhere, not each required staging point.

The precise interface correction is J-2.stimuli: [] → ["ST-4"]. All other map values are identical. Counts, step order, scenario membership, supplier citations, five stimuli, schema, outcome aggregation and SQ-R1…10 implementations remain unchanged. SQ §4/EXP-R4 native requirements and conditional ST-4/required ST-5 replay remain unchanged. The correction implements already stated intent rather than choosing new case intent or an owner-reserved semantic. Independent review must confirm this before adoption.

## Examples and checks

Only recorded J-2 entries in SQ-EX-03/04/05 and SQ-RV-04/09/10/11/12 gain expressly ILLUSTRATIVE native ST-4 entries. Awaiting/planned examples and all eight schema-invalid vectors stay untouched. Existing exact violation sets are preserved (vector-parity.json); the existing illustrative recovery-specific failure in SQ-EX-05 stays at S11-6. Illustrations are rule probes, not coherent native witness records or candidate observations.

The maintained prototype adds one documented staging check and four paired J-2 probes: omission rejected by SQ-R9; not-produced/pass rejected; not-produced/blocked allowed with blocked scenario aggregate; declared replay counterpart allowed at the dossier-rule level. EXP still determines whether evidence supports a native part. The same omission passes the old map and fails the correction, showing sensitivity to this defect. Offline Python 3.13/jsonschema 4.26.0: baseline 114/0, candidate 119/0, 65 supplier case citations; all 17 existing valid/rule vectors retain exact rule outcomes; git diff --check passed. These are definition checks only.

## Consumer propagation

- DEL-09-02 prototype and illustrative recorded J-2 consumers are updated in this candidate. Schema and semantic-rule code require no change. Future dossier preparation must bind the corrected map and treat J-2's missing ST-4 as unavailable evidence, never infer production.
- Group B B7 preparatory helper is an active downstream consumer on its own branch. Manager must send the reviewed correction and candidate identity to its author, refresh its source hashes and J-2 preparation expectations, then recheck. This candidate does not write B7 code.
- DEL-11-03 REPLACEMENT_PACKET.md pins SQ prose and valid-example digests. Its owner must assess/adopt refreshed source identities; candidate-field mapping remains unchanged. Historical pass-4 F/fixtures/FX-RP1* copies of SQ-EX-05 remain frozen historical evidence, not silently rewritten. Manager carries the notice to Group E/DEL-11-03.
- No SoW, dependency, graph, status, instruction or shared app files changed. Manager owns the contract-issue entry, integration/adoption record and eventual MEMORY/closeout. No group ordering or supplier interface changes arise.
- Any future/existing real dossier bound to the old map requires the owning examiner's EXP §6.2 impact assessment for J-2 and dependent scenario claims; no old evidence is upgraded here.

## Execution and return boundary

Actual mechanism: delegated-harness-native TASK child `/root/group_b_manager/sq_st4_design`, parent WORKING_ITEMS `/root/group_b_manager`, under HELP_HUMAN. No child delegation. Supplied brief restricts writes to DEL-09-02 Design and this change folder in the isolated worktree/branch `codex/app-v4-group-b-sq-st4`. Host initially denied sibling-worktree writes; an authorized escalation allowed those bounded writes. No downloads, credentials, user Codex home, native execution, human acts or public release. Source identities and selected context are in SOURCE_BASIS.json (manual headings, Field Book full, User Manual §§7/13/14; EXP §§3.5/6–8). Full candidate identity will be returned after commit; independent review and manager adoption remain pending.
